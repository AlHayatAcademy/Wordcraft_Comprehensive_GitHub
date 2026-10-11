'use strict';
function recordSenseAttempt(e,correct,mode='recognition',assisted=false){
 if(!e?.senseId)return;
 state.senses=state.senses||{};state.senses[e.senseId]=Learning.attempt(state.senses[e.senseId],{correct,mode,assisted});
 const entryKey=e.entryKey||(Number.isInteger(e.wordId)?'w'+e.wordId:null);if(entryKey)Content.select(entryKey,e);state.selectedSenses=Object.fromEntries(Content.selected);save();
}
function dueTeachingSenses(){return Object.entries(state.senses||{}).filter(([id,p])=>p.stage>0&&p.due<=Date.now()&&Content.resolve(id)).sort((a,b)=>a[1].due-b[1].due).map(([id])=>id);}
function selectTaxSense(row,c){
 const source=Content.resolve(c.senseId)||[...Content.senses.values()].find(e=>e.wordId===row.item.id&&e.meaning===c.meaning);
 const sense=source||{...c,entryKey:row.key,word:row.name,wordId:row.kind==='word'?row.item.id:null,senseId:c.senseId||`tax:${row.key}:${c.contextId||'source'}:${c.senseIndex||0}`,collocation:c.collocation||'',tip:c.tip||c.rationale||'',legacy:!c.exampleUrdu};
 Content.select(row.key,sense);state.teachingContexts=state.teachingContexts||{};state.teachingContexts[sense.senseId]=sense;if(row.kind==='word'){state.selectedSenses=Object.fromEntries(Content.selected);save();}return sense;
}
function registerTaxSenses(){for(const row of allTaxItems())for(const c of taxMeta(row.key).contexts||[]){
 const existing=[...Content.senses.values()].find(e=>e.wordId===row.item.id&&e.meaning===c.meaning);
 c.senseId=existing?.senseId||`tax:${row.key}:${c.contextId||'source'}:${c.senseIndex||0}`;
 if(!existing)Content.senses.set(c.senseId,{...c,entryKey:row.key,word:row.name,wordId:row.kind==='word'?row.item.id:null,collocation:c.collocation||'',tip:c.tip||c.rationale||'',legacy:!c.exampleUrdu});
}}
