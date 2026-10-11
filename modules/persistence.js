'use strict';
const Persistence = (() => {
 let baseRevision=0,blocked=false;
 function migrate(raw){
  if(!raw||typeof raw!=='object'||Array.isArray(raw)||raw.version!==1)throw Error('Unsupported or damaged progress');
  const s={...raw,schemaVersion:2};
  s.words=Learning.cleanProgress(raw.words);if(typeof META!=='undefined'&&Array.isArray(META.allWordIds)){const valid=new Set(META.allWordIds.map(String));s.words=Object.fromEntries(Object.entries(s.words).filter(([id])=>valid.has(id)));}s.senses=Learning.cleanProgress(raw.senses);
  s.notes=Array.isArray(raw.notes)?raw.notes.filter(n=>n&&typeof n.text==='string'&&Array.isArray(n.words)&&typeof n.date==='string').slice(-10000).map(n=>({...n,text:n.text.slice(0,20000),words:n.words.filter(w=>typeof w==='string')})):[];
  s.activity={};for(const [day,n]of Object.entries(raw.activity||{}))if(/^\d{4}-\d{2}-\d{2}$/.test(day)&&Number.isFinite(n))s.activity[day]=Math.max(0,n);
  s.drafts={};for(const [k,v]of Object.entries(raw.drafts||{}))if(typeof v==='string'&&k.length<180)s.drafts[k]=v.slice(0,20000);
  s.selectedSenses={};for(const [k,v]of Object.entries(raw.selectedSenses||{}))if(/^[wer][a-zA-Z0-9._-]+$/.test(k)&&typeof v==='string'&&v.length<180)s.selectedSenses[k]=v;
  s.teachingContexts={};for(const [k,v]of Object.entries(raw.teachingContexts||{})){if(k.length<180&&v&&v.senseId===k&&typeof v.meaning==='string'&&typeof v.word==='string'&&typeof v.example==='string'&&v.meaning.length<5000&&v.example.length<5000)s.teachingContexts[k]=v;}
  s.revision=Number.isSafeInteger(raw.revision)?raw.revision:0;
  return s;
 }
 function read(key,fallback){
  const text=localStorage.getItem(key);if(!text){baseRevision=0;return migrate(fallback);}
  try{const s=migrate(JSON.parse(text));baseRevision=s.revision;return s;}catch(e){
   try{localStorage.setItem(key+'-recovery',text);}catch(_){}
   blocked=true;return {...migrate(fallback),storageWarning:'Damaged progress preserved. Export it from recovery before resetting storage.'};
  }
 }
 function write(key,s){
  if(blocked)return false;
  const current=localStorage.getItem(key);if(current){let r;try{r=JSON.parse(current).revision||0;}catch(_){blocked=true;return false;}if(r>baseRevision){blocked=true;return false;}}
  const revision=baseRevision+1;localStorage.setItem(key,JSON.stringify({...s,revision,schemaVersion:2}));baseRevision=revision;s.revision=revision;return true;
 }
 function acceptRestore(){blocked=false;try{baseRevision=JSON.parse(localStorage.getItem('wordcraft-v1')||'{}').revision||0;}catch(_){baseRevision=0;}}
 return {migrate,read,write,acceptRestore};
})();
