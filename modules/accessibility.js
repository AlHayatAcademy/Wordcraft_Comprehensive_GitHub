'use strict';
// Native dialog preserves modality; explicitly return focus to the opener.
let dialogOpener=null;
document.addEventListener('click',e=>{if(!$('wordDialog').open&&e.target?.closest?.('button'))dialogOpener=e.target.closest('button');},true);
$('wordDialog').addEventListener('close',()=>{dialogOpener?.focus?.();});
window.addEventListener('storage',e=>{if(e.key===KEY)notice('Progress changed in another tab. Back up this tab before reloading; automatic overwrites are blocked.');});
if('serviceWorker'in navigator){
 navigator.serviceWorker.ready.then(reg=>{
  function prompt(){if(!reg.waiting)return;const el=$('updateNotice');if(el){el.hidden=false;el.innerHTML='<p>An update is ready. Back up your progress, then reload to use the new version.</p><button class="btn" id="applyUpdate">Apply update</button>';$('applyUpdate').onclick=()=>{save();reg.waiting.postMessage({type:'ACTIVATE_UPDATE'});};}}
  prompt();reg.addEventListener('updatefound',()=>{const worker=reg.installing;worker?.addEventListener('statechange',()=>{if(worker.state==='installed'&&navigator.serviceWorker.controller)prompt();});});
 });
 let refreshing=false;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(refreshing)return;refreshing=true;location.reload();});
}
