'use strict';
const PREFIX='wordcraft:'+new URL(self.registration.scope).pathname+':',VERSION='v11',CACHE=PREFIX+VERSION+'-essential',OPTIONAL=PREFIX+VERSION+'-optional';
const FILES=['./','index.html','style.css','design.css','cards.css','comprehensive.css','studio.css','design.js','cards.js','comprehensive.js','studio.js','taxonomy.js','app.js','enhancements.js','modules/content.js','modules/learning.js','modules/persistence.js','modules/packs.js','modules/sessions.js','modules/bootstrap.js','modules/accessibility.js','course-data.json','curriculum.json','domains.json','sources.json','meta.json','usage.json','manifest.json','favicon.svg'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
self.addEventListener('message',e=>{if(e.data?.type==='ACTIVATE_UPDATE')self.skipWaiting();});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&!k.startsWith(PREFIX+VERSION+'-')).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
async function response(request){
 const url=new URL(request.url),scope=new URL(self.registration.scope);if(!url.pathname.startsWith(scope.pathname))return fetch(request);
 const cache=await caches.open(CACHE),optional=await caches.open(OPTIONAL);
 const hit=await cache.match(request)||await optional.match(request);if(hit)return hit;
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),8000);
 try{const r=await fetch(request,{signal:controller.signal});return r;}catch(error){if(request.mode==='navigate')return await cache.match('index.html')||Response.error();return new Response('This optional collection is not downloaded for offline use.',{status:503,headers:{'Content-Type':'text/plain'}});}finally{clearTimeout(timer);}
}
self.addEventListener('fetch',e=>{if(e.request.method==='GET'&&new URL(e.request.url).origin===self.location.origin)e.respondWith(response(e.request));});
