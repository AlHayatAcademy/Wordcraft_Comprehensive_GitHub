'use strict';
let DOMAINS=[],REFERENCES=[],wordScope='all',domainPage=0,selectedDomain='',domainDrill=null,drillMode='spelling',drillIndex=0,drillWords=[];
const comprehensiveInit=init;
init=async function(){
 try{[DOMAINS,REFERENCES]=await Promise.all(['domains.json','reference.json'].map(p=>fetch(p).then(r=>{if(!r.ok)throw Error('Vocabulary unavailable');return r.json()})));}
 catch(e){$('view').innerHTML='<div class="empty">The expanded vocabulary could not load. Reconnect and refresh.</div>';return;}
 await comprehensiveInit();
};
const comprehensiveRender=render;
render=function(){
 const route=(location.hash.slice(1)||'home').split('?')[0];
 if(['areas','trainer','reference'].includes(route)){
  view=route;document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+route));
  $('crumb').textContent=route==='areas'?'English for the situations that matter':route==='trainer'?'Recall, spell and listen':'Explore the expanded dictionary';
  ({areas:renderAreas,trainer:renderTrainer,reference:renderReference})[route]();return;
 }
 comprehensiveRender();
};
const comprehensiveHome=renderHome;
renderHome=function(){comprehensiveHome();const box=$('view');box.innerHTML=`<section class="coverage-banner"><span>WORDCRAFT · COMPREHENSIVE</span><h2>Words for life, study and work.</h2><p>${(DATA.length+REFERENCES.length).toLocaleString()} unique headwords · ${DATA.length.toLocaleString()} full learning entries · ${DOMAINS.length} practical areas · 3,000 expressions</p><div class="lesson-actions"><a class="btn gold" href="#areas">Explore learning areas →</a><a class="btn white" href="#library">Search every word</a><a class="btn outline" href="#trainer">Spelling & dictation</a></div></section>`+box.innerHTML;};
const fullLibrary=renderLibrary;
renderLibrary=function(){
 const urdu=view==='urdu';if(urdu)wordScope='lessons';
 if(wordScope==='lessons'){fullLibrary();$('view').innerHTML=scopeControls()+$('view').innerHTML;return;}
 renderUnifiedLibrary(false);
};
function scopeControls(){return `<div class="scope-tabs" role="group" aria-label="Vocabulary collection">${[['all','All headwords'],['lessons','Full learning entries'],['reference','Dictionary reference']].map(([v,t])=>`<button class="btn small ${wordScope===v?'gold':'outline'}" aria-pressed="${wordScope===v}" onclick="setWordScope('${v}')">${t}</button>`).join('')}</div>`;}
function setWordScope(value){wordScope=value;page=0;renderLibrary();}
function searchExpanded(value){query=value;page=0;renderLibrary();const input=$('allSearch');input.focus();input.setSelectionRange(value.length,value.length);}
function renderUnifiedLibrary(referenceOnly=false){
 const needle=query.trim().toLowerCase();
 let core=referenceOnly||wordScope==='reference'?[]:filtered();
 let ref=REFERENCES.filter(w=>!needle||[w.word,...(w.forms||[]),...w.senses.map(s=>s.meaning)].join(' ').toLowerCase().includes(needle));
 const all=[...core.map(w=>({kind:'lesson',w})),...ref.map(w=>({kind:'reference',w}))];
 if(sort==='az')all.sort((a,b)=>a.w.word.localeCompare(b.w.word));
 const pages=Math.ceil(all.length/24);page=Math.max(0,Math.min(page,Math.max(0,pages-1)));
 $('view').innerHTML=title('ONE SEARCH · NO DUPLICATE HEADWORDS',referenceOnly?'Expanded dictionary':'The complete word library','Full entries include Urdu and learning activities. Dictionary entries give licensed English definitions; they do not claim completed Urdu or usage review.')+(referenceOnly?'':scopeControls())+`<div class="toolbar"><input id="allSearch" type="search" aria-label="Search all headwords" placeholder="Search a word, English meaning or Urdu meaning…" value="${esc(query)}" oninput="searchExpanded(this.value)"><select aria-label="Sort words" onchange="sort=this.value;page=0;renderLibrary()"><option value="rank" ${sort==='rank'?'selected':''}>Full lessons first</option><option value="az" ${sort==='az'?'selected':''}>Alphabetical</option></select></div><p class="muted">${all.length.toLocaleString()} matching headwords · ${core.length.toLocaleString()} full entries · ${ref.length.toLocaleString()} dictionary entries</p><div class="library-grid">${all.slice(page*24,(page+1)*24).map(({kind,w})=>`<article class="vocab-card" tabindex="0" role="button" onkeydown="if(event.key==='Enter'){${kind==='lesson'?`openWord(${w.id})`:`openReference('${w.id}')`}}" onclick="${kind==='lesson'?`openWord(${w.id})`:`openReference('${w.id}')`}"><span class="tag ${kind==='lesson'?levelClass(w.band):'reference-tag'}">${kind==='lesson'?'Full lesson · '+esc(w.band):'Dictionary reference'}</span><h3>${esc(w.word)}</h3><p>${esc(w.senses[0].meaning)}</p><small>${esc(w.senses[0].pos)}</small>${kind==='lesson'?`<p class="urdu" lang="ur" dir="rtl">${esc(w.urdu)}</p>`:'<p class="smallprint">English definition · WordNet 3.0</p>'}</article>`).join('')}</div>${all.length?'':'<div class="empty">No matching headword. Try a shorter search.</div>'}<div class="pagination"><button class="btn small" ${page===0?'disabled':''} onclick="page--;renderLibrary()">← Previous</button><span>${all.length?page+1:0} / ${pages}</span><button class="btn small" ${page+1>=pages?'disabled':''} onclick="page++;renderLibrary()">Next →</button></div>`;
}
function renderReference(){wordScope='reference';renderUnifiedLibrary(true);}
function openReference(id){
 const w=REFERENCES.find(x=>x.id===id);if(!w)return;
 $('wordDetail').innerHTML=`<span class="tag reference-tag">English dictionary reference</span><div class="word-title"><h1>${esc(w.word)}</h1><button class="audio-btn" onclick="speak(${JSON.stringify(w.word).replace(/"/g,'&quot;')})" aria-label="Hear pronunciation">♪</button></div><p class="smallprint">Browser speech is an audio aid, not independently verified IPA. Urdu translation and sense-specific lessons are not yet supplied for this entry.</p>${w.senses.map(s=>`<section class="card-section cc-slate"><h3>${esc(s.pos)}</h3><p>${esc(s.meaning)}</p>${s.examples.length?'<h4>Dictionary examples</h4>'+s.examples.map(e=>`<p>${esc(e)}</p>`).join(''):''}${s.synonyms.length?`<p><strong>Related words in this sense:</strong> ${s.synonyms.map(esc).join(', ')}</p><small>Compare context before substituting a related word.</small>`:''}</section>`).join('')}<p class="smallprint">Definition: Princeton WordNet 3.0. Listed in: ${w.selectionSources.map(esc).join('; ')}.</p><button class="btn gold" onclick="startReferenceDrill('${w.id}')">Practise spelling →</button>`;
 $('wordDialog').showModal();
}
function renderAreas(){
 if(selectedDomain){renderDomain();return;}
 $('view').innerHTML=title('ENGLISH FOR REAL SITUATIONS','Choose your learning area','Each area contains eight original contextual lessons. These practical topics complement the larger newspaper, academic and aptitude collections.')+`<div class="domain-grid">${DOMAINS.map(d=>`<button class="domain-card" onclick="selectedDomain='${d.id}';domainPage=0;renderAreas()"><span class="domain-icon" aria-hidden="true">${d.icon}</span><h2>${esc(d.name)}</h2><p>${esc(d.goal)}</p><small>${d.lessons.length} contextual lessons · ${d.lessons.filter(l=>progress(BYID[l.wordId]).correct>0).length} recalled</small><span class="domain-arrow">Explore →</span></button>`).join('')}</div>`;
}
function renderDomain(){
 const d=DOMAINS.find(x=>x.id===selectedDomain);if(!d){selectedDomain='';renderAreas();return;}
 $('view').innerHTML=`<button class="btn small outline" onclick="selectedDomain='';renderAreas()">← All areas</button>`+title(d.icon+' PRACTICAL ENGLISH',esc(d.name),esc(d.goal))+`<div class="lesson-actions"><button class="btn gold" onclick="startDomainLesson('${d.id}')">Study word cards</button><button class="btn teal" onclick="startDomainDrill('${d.id}')">Spell & listen</button><button class="btn outline" onclick="startDomainQuiz('${d.id}')">Recall quiz</button></div><div class="domain-lessons">${d.lessons.map(l=>`<article class="panel"><span class="tag">${esc(l.pos)}</span><h2><button class="word-link" onclick="openWord(${l.wordId})">${esc(l.word)}</button></h2><p>${esc(l.meaning)}</p><p class="urdu" lang="ur" dir="rtl">${esc(l.urdu)}</p><div class="context-example"><strong>${esc(l.collocation)}</strong><p>${esc(l.example)}</p></div><button class="btn small" onclick="speak(${JSON.stringify(l.example).replace(/"/g,'&quot;')})">♪ Listen to the example</button></article>`).join('')}</div><section class="panel"><h3>Your turn: use the vocabulary</h3><p>Write a short message or describe a situation in this area using three of these words. Open a word card to save your sentence in the notebook.</p><a class="btn gold small" href="#writing">Open sentence studio →</a></section>`;
}
function startDomainLesson(id){const d=DOMAINS.find(x=>x.id===id);lesson=d.lessons.map(l=>BYID[l.wordId]);lessonIndex=0;revealed=false;location.hash='learn';if(view==='learn')renderLesson();}
function startDomainQuiz(id){const d=DOMAINS.find(x=>x.id===id);practiceIds=d.lessons.map(l=>l.wordId);quiz=null;location.hash='practice';if(view==='practice')renderPractice();}
function startDomainDrill(id){const d=DOMAINS.find(x=>x.id===id);drillWords=shuffle(d.lessons);drillIndex=0;domainDrill=null;location.hash='trainer';if(view==='trainer')renderTrainer();}
function startReferenceDrill(id){const w=REFERENCES.find(x=>x.id===id);drillWords=[{word:w.word,meaning:w.senses[0].meaning,urdu:null}];drillIndex=0;domainDrill=null;$('wordDialog').close();location.hash='trainer';if(view==='trainer')renderTrainer();}
function renderTrainer(){
 if(!drillWords.length)drillWords=shuffle(DOMAINS.flatMap(d=>d.lessons));
 if(!domainDrill)domainDrill={...drillWords[drillIndex%drillWords.length],assisted:false,attempted:false};
 const q=domainDrill;
 $('view').innerHTML=title('ACTIVE RECALL','Spelling & dictation','Recall the word from its meaning, or listen and type it. Dictionary aids and revealed answers are marked as assisted.')+`<div class="scope-tabs">${[['spelling','Meaning → spelling'],['dictation','Listen → spelling']].map(([m,t])=>`<button class="btn small ${m===drillMode?'gold':'outline'}" onclick="drillMode='${m}';renderTrainer()">${t}</button>`).join('')}</div><section class="panel trainer-panel"><span class="tag">Item ${drillIndex+1} of ${drillWords.length}</span>${drillMode==='spelling'?`<h2>${esc(q.meaning)}</h2>${q.urdu?`<p class="urdu" lang="ur" dir="rtl">${esc(q.urdu)}</p>`:''}`:'<h2>Listen, then type the word.</h2>'}<div class="lesson-actions"><button class="btn teal" onclick="speakDrill()">♪ Hear the word</button><button class="btn outline" onclick="revealDrill()">Reveal answer</button></div><label for="drillAnswer">Your answer</label><input id="drillAnswer" autocomplete="off" spellcheck="false" onkeydown="if(event.key==='Enter')checkDrill()" placeholder="Type the English word…"><div class="lesson-actions"><button class="btn gold" onclick="checkDrill()">Check</button><button class="btn small" onclick="drillIndex=(drillIndex+1)%drillWords.length;domainDrill=null;renderTrainer()">Next →</button></div><p id="drillFeedback" role="status" aria-live="polite"></p></section><p class="smallprint">Speech availability depends on your browser. These activities assess spelling, not pronunciation or an official examination score.</p>`;
}
function speakDrill(){if(drillMode==='spelling')domainDrill.assisted=true;speak(domainDrill.word);}
function revealDrill(){domainDrill.assisted=true;$('drillFeedback').textContent='Answer: '+domainDrill.word+' · assisted practice';}
function checkDrill(){const q=domainDrill,value=$('drillAnswer').value.trim().replace(/\s+/g,' ').toLowerCase();if(!value){$('drillFeedback').textContent='Type an answer first.';return;}const correct=value===q.word.toLowerCase();$('drillFeedback').textContent=correct?(q.assisted?'Correct spelling · assisted practice.':'Correct spelling!'):'Try again, or listen and reveal the answer.';if(!q.attempted&&q.wordId&&!q.assisted){rate(q.wordId,correct?'good':'again',correct&&!q.assisted);}q.attempted=true;}
const comprehensiveAbout=renderAbout;
renderAbout=function(){comprehensiveAbout();$('view').innerHTML=`<section class="panel"><h2>What this edition includes</h2><p>${DATA.length.toLocaleString()} full learning entries, ${REFERENCES.length.toLocaleString()} additional WordNet reference headwords, 3,000 expressions and ${DOMAINS.reduce((n,d)=>n+d.lessons.length,0)} original domain lessons. All 2,999 headwords from the supplied aptitude bank are present.</p><p>Reference entries provide English dictionary senses, not newly verified Urdu lessons. Source lists identify candidate headwords; their publisher definitions and example sentences were not copied into the reference expansion. WordNet 3.0 definitions are used with the bundled licence.</p><p>Learning bands are internal guides, not certified CEFR levels or official examination lists. Topic pathways are starting points and do not cover every specialist term.</p><div class="lesson-actions"><a href="coverage-audit.json" class="btn small">Coverage audit</a><a href="word-review-queue.json" class="btn small">Unresolved word candidates</a><a href="phrase-candidates.json" class="btn small">Phrase review queue</a></div></section>`+$('view').innerHTML;};

init();
