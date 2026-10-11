'use strict';
const Packs=(()=>{
 const tasks=new Map(),ready=new Set();
 const files={"collection":["packs/data-0232905240f7.json","packs/sources-7a75b6fc5c69.json","packs/usage-3b6f48b1eb35.json"],"dictionary":["packs/reference-358a5a4288b4.json"],"classification":["packs/taxonomy-2034b6f871cd.json"],"expressions":["packs/expressions-005f19921c80.json"],"families":["packs/family-lessons-4dbdc5191fe5.json"]};
 async function load(name){
  if(ready.has(name))return;
  if(tasks.has(name))return tasks.get(name);
  const task=(async()=>{
   const values=await Promise.all(files[name].map(async f=>{const r=await fetch(f);if(!r.ok)throw Error('Could not download '+f);return r.json();}));
   if(name==='collection'){DATA=values[0];SOURCES=values[1];USAGE=values[2];BYID=Object.fromEntries(DATA.map(w=>[w.id,w]));WORDS=Object.fromEntries(DATA.map(w=>[w.word,w]));}
   if(name==='dictionary'){REFERENCES=values[0];referenceState='ready';}
   if(name==='classification'){TAXONOMY=values[0];registerTaxSenses();}
   if(name==='expressions')expressionData=values[0];
   if(name==='families')FAMILY=values[0];
   ready.add(name);
  })();tasks.set(name,task);
  try{await task;}finally{tasks.delete(name);}
 }
 async function forRoute(route){
  if(['home','path','session','learn','areas','settings','progress'].includes(route))return;
  const names=['collection'];if(['library','reference','categories','category-practice','about'].includes(route))names.push('classification','expressions','dictionary');
  if(route==='expressions')names.push('expressions','classification');
  await Promise.all(names.map(load));if(ready.has('classification'))registerTaxSenses();
 }
 function loadedFor(route){if(['home','path','session','learn','areas','settings','progress'].includes(route))return true;return ready.has('collection')&&(!['library','reference','categories','category-practice','about'].includes(route)||['classification','expressions','dictionary'].every(n=>ready.has(n)))&&(route!=='expressions'||ready.has('expressions')&&ready.has('classification'));}
 return {load,forRoute,loadedFor,ready,files};
})();
async function retryRoute(){render();}
async function downloadOfflinePack(name){
 const status=$('offlineStatus');if(status)status.textContent='Downloading '+name+'… Keep this page open.';
 try{await Packs.load(name);if(!('caches'in window))throw Error('Offline storage unavailable');const cache=await caches.open('wordcraft:'+new URL('.',document.baseURI||location.href).pathname+':v11-optional');for(const f of Packs.files[name]){const r=await fetch(f);if(!r.ok)throw Error(f);await cache.put(f,r);}if(status)status.textContent=name+' is available offline on this browser.';}
 catch(e){if(status)status.textContent='Download did not complete. Check your connection and retry.';}
}

async function showOfflineAvailability(){const el=$('offlineStatus');if(!('caches'in window)){el.textContent='Offline storage is unavailable.';return;}const cache=await caches.open('wordcraft:'+new URL('.',document.baseURI||location.href).pathname+':v11-optional');const rows=await Promise.all(Object.entries(Packs.files).map(async([name,files])=>[name,(await Promise.all(files.map(f=>cache.match(f)))).every(Boolean)]));el.textContent=rows.map(([n,ok])=>n+': '+(ok?'downloaded':'not downloaded')).join(' · ');}
