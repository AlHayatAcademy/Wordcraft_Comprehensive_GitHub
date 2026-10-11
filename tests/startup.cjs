const fs=require('fs'),vm=require('vm'),assert=require('assert');
const base=require('path').resolve(__dirname,'..')+'/';
const expectedMeta=JSON.parse(fs.readFileSync(base+'meta.json'));const expectedWordCount=expectedMeta.wordCount,expectedLevels=expectedMeta.levelCounts;
const elements={};function el(id){return elements[id]||=( {id,innerHTML:'',textContent:'',value:'',open:false,disabled:false,classList:{add(){},toggle(){}},addEventListener(){},showModal(){this.open=true},close(){this.open=false},click(){},focus(){},setSelectionRange(){},setAttribute(){},querySelector(){return null}})}
const context={console,Date,Math,JSON,Number,String,Object,Array,Set,Map,RegExp,Promise,Blob,URL,setTimeout:()=>0,clearTimeout(){},location:{hash:''},document:{getElementById:el,querySelectorAll:()=>[],body:{classList:{toggle(){}}},addEventListener(){},createElement:()=>el('download')},localStorage:{setItem(k,v){this[k]=v},getItem(k){return this[k]||null}},navigator:{},window:{addEventListener(){}},fetch:async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(base+url,'utf8'))})};

let releaseReference,releaseFamily,releaseExpressions;
const regularFetch=context.fetch;
context.fetch=async url=>{
 if(url==='expressions.json')await new Promise(resolve=>{releaseExpressions=resolve});
 if(url==='reference.json')await new Promise(resolve=>{releaseReference=resolve});
 if(url==='family-lessons.json')await new Promise(resolve=>{releaseFamily=resolve});
 return regularFetch(url);
};
context.localStorage.setItem('wordcraft-v1',JSON.stringify({version:1,words:{},notes:[],activity:{},expressions:{p163:{correct:3,attempts:4,due:99999999999999,saved:true}}}));
vm.createContext(context);
for(const file of ['app.js','enhancements.js','design.js','cards.js','comprehensive.js'])vm.runInContext(fs.readFileSync(base+file,'utf8'),context);
vm.runInContext('init()',context);const run=s=>vm.runInContext(s,context);
(async()=>{
 await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));
 assert.equal(run('DATA.length'),expectedWordCount,'core entries load without dictionary or families');
 assert.equal(run('referenceState'),'loading');assert.equal(run('state.expressions.p163.correct'),3,'slow expression load preserves saved progress');
 assert(el('view').innerHTML.includes('Words for life, study and work.'));
 context.location.hash='#library';run('render()');assert(el('view').innerHTML.includes('expanded dictionary is loading'));
 assert(el('view').innerHTML.includes('Full lesson'));
 releaseReference();releaseFamily();releaseExpressions();await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));
 assert.equal(run('referenceState'),'ready');assert.equal(run('state.expressions.p163.correct'),3);assert.equal(run('REFERENCES.length'),expectedMeta.dictionaryReferenceWords);
 assert(!el('view').innerHTML.includes('expanded dictionary is loading'));
 console.log('PASS: homepage and full lessons remain available while dictionary and families are delayed; dictionary refreshes when ready.');
})().catch(e=>{console.error(e);process.exit(1)});
