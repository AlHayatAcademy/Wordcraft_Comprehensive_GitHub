'use strict';
// Pure, shared scheduling and validation. Historical word progress is not a sense score.
const Learning = (() => {
 const DAY_MS=86400000, intervals=[1,3,7,14,30,60,120];
 function attempt(previous={}, {correct=false,assisted=false,mode='recognition',now=Date.now()}={}) {
  const p=JSON.parse(JSON.stringify(previous));
  p.stage=Number.isInteger(p.stage)?Math.max(0,Math.min(7,p.stage)):0;
  p.attempts=(p.attempts||0)+1;p.correct=(p.correct||0)+(correct?1:0);
  p.metrics=p.metrics||{};const m=p.metrics[mode]||{attempts:0,correct:0,assisted:0};
  m.attempts++;if(correct)m.correct++;if(assisted)m.assisted++;p.metrics[mode]=m;
  if(assisted||mode==='productive'){p.updated=now;return p;}
  const day=new Date(now).toISOString().slice(0,10);
  if(!correct){p.stage=Math.max(1,p.stage);p.retry=true;p.due=now+600000;p.lapses=(p.lapses||0)+1;}
  else if(p.retry){p.retry=false;p.due=now+DAY_MS;p.creditDay=day;p.stage=Math.max(1,p.stage);}
  else if(p.creditDay!==day&&(!p.stage||!p.due||p.due<=now)){
   p.stage=Math.min(7,p.stage+1);p.due=now+intervals[p.stage-1]*DAY_MS;p.creditDay=day;
   if(previous.updated&&now-previous.updated>=DAY_MS){p.delayedCorrect=(p.delayedCorrect||0)+1;}
  }
  p.updated=now;return p;
 }
 function cleanProgress(raw){
  const count=v=>Number.isFinite(Number(v))?Math.max(0,Number(v)):0;
  if(!raw||typeof raw!=='object'||Array.isArray(raw))return {};
  const result={};for(const [key,p] of Object.entries(raw)){
   if(['__proto__','constructor','prototype'].includes(key)||!/^[a-zA-Z0-9:._-]{1,180}$/.test(key)||!p||!Number.isFinite(p.due)||!Number.isFinite(p.stage))continue;
   const c={stage:Math.max(0,Math.min(7,Math.floor(p.stage))),due:Math.max(0,p.due),attempts:count(p.attempts),correct:count(p.correct),bookmark:!!p.bookmark,retry:!!p.retry};
   for(const f of ['updated','lapses','delayedCorrect'])if(Number.isFinite(p[f]))c[f]=Math.max(0,p[f]);
   if(/^\d{4}-\d{2}-\d{2}$/.test(p.creditDay||''))c.creditDay=p.creditDay;
   c.metrics={};for(const mode of ['recognition','recall','context','spelling','listening','productive']){
    const m=p.metrics?.[mode];if(m)c.metrics[mode]=Object.fromEntries(['attempts','correct','assisted'].map(k=>[k,count(m[k])]));
   }result[key]=c;
  }return result;
 }
 return {attempt,cleanProgress};
})();
