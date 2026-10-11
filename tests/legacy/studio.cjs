const fs=require('fs'),vm=require('vm'),assert=require('assert');
const base=require('path').resolve(__dirname,'..')+'/';
const expectedQuality=JSON.parse(fs.readFileSync(base+'quality-audit.json'));
const expectedMeta=JSON.parse(fs.readFileSync(base+'meta.json'));const expectedWordCount=expectedMeta.wordCount,expectedLevels=expectedMeta.levelCounts;
const elements={};function el(id){return elements[id]||=( {id,innerHTML:'',textContent:'',value:'',open:false,disabled:false,classList:{add(){},toggle(){}},addEventListener(){},showModal(){this.open=true},close(){this.open=false},click(){},focus(){},setSelectionRange(){},setAttribute(){},querySelector(){return null}})}
const context={console,Date,Math,JSON,Number,String,Object,Array,Set,Map,RegExp,Promise,Blob,URL,setTimeout:()=>0,clearTimeout(){},location:{hash:''},document:{getElementById:el,querySelectorAll:()=>[],body:{classList:{toggle(){}}},addEventListener(){},createElement:()=>el('download')},localStorage:{setItem(k,v){this[k]=v},getItem(k){return this[k]||null}},navigator:{},window:{addEventListener(){}},fetch:async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(base+url,'utf8'))})};
let testHash='';Object.defineProperty(context.location,'hash',{get:()=>testHash,set:v=>{testHash=v&&!String(v).startsWith('#')?'#'+v:String(v)}});
vm.createContext(context);
for(const file of ['app','enhancements','design','cards','comprehensive','studio','taxonomy'])vm.runInContext(fs.readFileSync(base+file+'.js','utf8'),context);
const run=s=>vm.runInContext(s,context);
(async()=>{
 await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));
 assert.equal(run('DATA.length'),expectedMeta.wordCount);assert.equal(run('REFERENCES.length'),expectedMeta.dictionaryReferenceWords);assert.equal(run('expressionData.length'),3000);
 const original=JSON.parse(fs.readFileSync(base+'preservation-manifest.json')).wordEntries;
 for(const w of original)assert(run(`DATA.some(x=>x.id===${w.id}&&x.word===${JSON.stringify(w.word)})`),'preserved '+w.word);
 const oldExpressions=JSON.parse(fs.readFileSync(base+'preservation-manifest.json')).expressionEntries;
 for(const e of oldExpressions)assert(run(`expressionData.some(x=>x.id===${JSON.stringify(e.id)}&&x.phrase===${JSON.stringify(e.phrase)})`));
 for(const old of JSON.parse(fs.readFileSync(base+'preservation-manifest.json')).dictionaryEntries)assert(run(`REFERENCES.some(w=>w.id===${JSON.stringify(old.id)}&&w.word===${JSON.stringify(old.word)})||DATA.some(w=>w.legacyReferenceId===${JSON.stringify(old.id)}&&w.word===${JSON.stringify(old.word)})`),'reference ID resolves '+old.id);
 assert.equal(run('new Set([...DATA,...REFERENCES].map(w=>w.word.toLowerCase())).size'),expectedMeta.totalUniqueWords);
 assert.equal(run('new Set(allTaxItems().map(r=>r.key)).size'),expectedMeta.totalUniqueWords+3000);
 assert.equal(run('allTaxItems().filter(r=>!taxMeta(r.key).categories.length).length'),0);assert.equal(run('Object.keys(TAXONOMY.entries).length'),25652);assert.equal(run('Object.values(TAXONOMY.entries).filter(m=>m.review==="general").length'),expectedQuality.generalFallbackEntries);
 assert.equal(run('CURRICULUM.length'),24);assert(run('studioEntries().every(e=>e.exampleUrdu&&contextGap(e))'));
 for(const c of run('TAXONOMY.categories')){assert.equal(c.count,run(`Object.values(TAXONOMY.entries).filter(m=>m.categories.includes('${c.id}')).length`));run(`browseCategory('${c.id}')`);assert.equal(run('filteredTaxItems().length'),c.count,'category filter count '+c.id);}
 for(const route of ['home','path','library','categories','areas','progress','more','settings','session','expressions','writing','reading','practice','trainer','usage','about']){context.location.hash='#'+route;run('render()');assert(el('view').innerHTML.length>150,route);assert(!el('view').innerHTML.includes('undefined'),route+' undefined');}
 run("browseCategory('phrasal');taxFilter.topic='Workplace';taxFilter.register='neutral';taxFilter.pos='verb'");assert(run('filteredTaxItems().length')>=4);assert(run("filteredTaxItems().every(r=>taxMeta(r.key).contexts.some(c=>c.categories.includes('phrasal')&&c.topic==='Workplace'&&c.register==='neutral'&&c.pos==='verb'))"));
 run("studioQuery='carry out'");assert.equal(run('filteredTaxItems().length'),1);assert.equal(run('filteredTaxItems()[0].item.id'),'p163');
 run("taxFilter.topic='Health'");assert.equal(run('filteredTaxItems().length'),0,'incompatible filters give empty state');
 run('resetTaxFilters()');assert.equal(run('filteredTaxItems().length'),expectedMeta.totalUniqueWords+3000);
 run("taxFilter.category='academic';studioScope='all'");assert.equal(run('filteredTaxItems().length'),run('TAXONOMY.categories.find(c=>c.id==="academic").count'));
 run("taxFilter.register='slang'");assert.equal(run('filteredTaxItems().length'),0,'no invented slang assignments');
 run('resetTaxFilters();studioScope="all";taxFilter.category="slang"');assert.equal(run('filteredTaxItems().length'),4,'four reviewed slang senses');run('resetTaxFilters();studioScope="all";taxFilter.category="abbreviation"');assert.equal(run('filteredTaxItems().length'),12);run('resetTaxFilters();studioScope="lessons"');assert.equal(run('filteredTaxItems().length'),expectedWordCount+3000);
 run("state.words[DATA[0].id]={stage:4,due:Date.now()+86400000,attempts:8,correct:5,bookmark:true};studioScope='saved'");assert(run('filteredTaxItems().some(r=>r.key===\'w\'+DATA[0].id)'));
 run("startCoreUnit('core-1');render()");assert(el('view').innerHTML.includes('hello'));assert(el('view').innerHTML.includes('سلام'));
 for(let i=0;i<6;i++){
  run("profile().session.step='recall';renderStudioSession()");const id=run('studioEntry(profile().session.keys[profile().session.index]).wordId');
  const correct=run('profile().session.options.indexOf(studioEntry(profile().session.keys[profile().session.index]).meaning)');
  const attempts=run(`progress(BYID[${id}]).attempts`);run(`answerStudioRecall(${correct});answerStudioRecall(${correct})`);assert.equal(run(`progress(BYID[${id}]).attempts`),attempts+1);
  run("profile().session.step='context';renderStudioSession()");const before=run(`JSON.stringify(progress(BYID[${id}]))`);
  el('studioAnswer').value=run('contextGap(studioEntry(profile().session.keys[profile().session.index])).answer');run('checkStudioContext()');assert.equal(run('profile().session.contextResult'),'correct');assert.equal(run(`JSON.stringify(progress(BYID[${id}]))`),before,'context is guided practice, not extra scheduling credit');
  run("profile().session.step='write';renderStudioSession();finishStudioWord(false)");
 }
 assert.equal(run('profile().session.step'),'done');assert(run("profile().completed.includes('core-1')"));
 run("startCoreUnit('core-1');profile().session.step='recall';renderStudioSession()");const firstId=run('studioEntry(profile().session.keys[0]).wordId'),stageBefore=run(`progress(BYID[${firstId}]).stage`);run('answerStudioRecall(profile().session.options.indexOf(studioEntry(profile().session.keys[0]).meaning))');assert.equal(run(`progress(BYID[${firstId}]).stage`),stageBefore,'same-day repeat cannot inflate retention');
 run("startCoreUnit('core-2');profile().session.step='recall';profile().session.assisted=true;renderStudioSession()");const aid=run('studioEntry(profile().session.keys[0]).wordId'),assistedBefore=run(`progress(BYID[${aid}]).attempts`);run('answerStudioRecall(profile().session.options.indexOf(studioEntry(profile().session.keys[0]).meaning))');assert.equal(run(`progress(BYID[${aid}]).attempts`),assistedBefore,'hints cannot earn recall credit');
 run("profile().session.step='write';renderStudioSession()");el('studioSentence').value='My friend helps me learn new words.';const notes=run('state.notes.length');run('finishStudioWord(true)');assert.equal(run('state.notes.length'),notes+1);
 run("browseCategory('phrasal');startCategoryPractice();render()");assert(run('categorySession.rows.length')>0);const q=run('categorySession.question');assert.equal(new Set(q.options).size,4);assert(q.options.includes(q.answer));run('answerCategoryQuestion(categorySession.question.options.indexOf(categorySession.question.answer))');assert(el('view').innerHTML.includes('Correct answer'));
 const ep=run('JSON.stringify(state.expressions)');run('answerCategoryQuestion(0)');assert.equal(run('JSON.stringify(state.expressions)'),ep,'no duplicate expression credit');
 for(const cat of ['everyday','academic','idiom','phrasal','collocation','fixed','linker','formal','informal','proverb','slang','abbreviation']){
  run(`browseCategory('${cat}');startCategoryPractice();renderCategoryPractice()`);assert(run('categorySession.rows.length')>0,cat);
  for(const row of run('categorySession.rows')){context.testRow=row;const question=run('categoryQuestion(testRow)');assert.equal(new Set(question.options).size,4);assert(question.explanation);assert(question.prompt);assert(question.options.includes(question.answer));}
 }
 run('resetTaxFilters();studioScope="all";taxFilter.category="everyday";taxFilter.topic="General";taxFilter.pos="noun"');assert(run('filteredTaxItems().length')>1000);assert(run('filteredTaxItems().every(r=>matchingTaxContext(r).pos==="noun")'));
 run('studioScope="lessons";startCategoryPractice();renderCategoryPractice()');assert(run('categorySession.rows.every(r=>taxMeta(r.key).review==="general")'));assert(!el('view').innerHTML.includes('undefined'));
 run('resetTaxFilters();studioScope="all";taxFilter.category="technical";taxFilter.topic="Science";studioQuery="current"');const electrical=run('filteredTaxItems().find(r=>r.name==="current")');assert(electrical);run(`openTaxEntry('${electrical.key}')`);assert(run(`cardModel('${electrical.key}').meaning`).includes('electric charge'));assert.equal(run(`cardModel('${electrical.key}').item.urdu`),'برقی رو','selected sense has its own Urdu gloss');run('resetTaxFilters()');
 for(const row of run('allTaxItems().filter(r=>r.kind!=="reference"&&taxMeta(r.key).review==="editorial")')){context.testRow=row;for(const c of run('taxMeta(testRow.key).contexts')){context.testContext=c;const q=run('categoryQuestion({...testRow,context:testContext})');assert.equal(new Set(q.options.map(x=>String(x).toLowerCase().trim())).size,4,row.name);assert(q.answer&&q.explanation&&q.prompt,row.name+' complete feedback');assert(!q.prompt.includes('undefined'));}}
 run('exportProgress()');const completed=run('JSON.stringify(profile().completed)'),savedWords=run('JSON.stringify(state.words)');context.importText=context.exportedBackup;await el('restoreFile').onchange({target:{files:[{text:async()=>context.importText}],value:''}});assert.equal(run('JSON.stringify(profile().completed)'),completed);assert.equal(run('JSON.stringify(state.words)'),savedWords,'backup preserves old word progress');
 run("openTaxEntry('ep163');selectCardTab('ep163','writing','d')");assert(el('wordDetail').innerHTML.includes('Writing:'));run("selectCardTab('ep163','speaking','d')");assert(el('wordDetail').innerHTML.includes('Speaking:'));
 const html=fs.readFileSync(base+'index.html','utf8');for(const route of ['home','path','library','progress','more','categories'])assert(html.includes('href="#'+route+'"'));assert(html.includes('viewport-fit=cover'));assert(html.includes('skip-link'));const css=fs.readFileSync(base+'studio.css','utf8');assert(css.includes('@media(max-width:480px)'));assert(css.includes('env(safe-area-inset-bottom)'));assert(css.includes('prefers-reduced-motion'));assert(css.includes(':focus-visible'));
 console.log('PASS: original IDs; 25,652 unique entry keys; 24 bilingual core units; unique overlapping category counts; combined search/topic/type/POS/register filters; empty states; 4-step sessions; assisted and repeat-credit protection; category quizzes; writing; backup restore; legacy Writing/Speaking tabs; responsive navigation and accessibility hooks.');
})().catch(e=>{console.error(e);process.exit(1)});
