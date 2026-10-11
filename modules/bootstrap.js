'use strict';
// One explicit startup pipeline. No sequential replacement of init().
async function init(){
 try{
  if(typeof initializeCourse==='function')await initializeCourse();if(typeof CURRICULUM!=='undefined'&&!CURRICULUM.length)throw Error('Course missing');
  if(typeof initializeTopics==='function')await initializeTopics();
  await initializeBase();if(!DATA.length)throw Error('Data missing');
  if(typeof cleanStudio==='function'){state.studio=cleanStudio(state.studio);save();render();}
 }catch(e){$('view').innerHTML='<section class="s-empty"><h1>The course could not load.</h1><p>Check your connection, then reload. Existing browser progress has been kept.</p><button class="btn" onclick="location.reload()">Retry</button></section>';}
}
