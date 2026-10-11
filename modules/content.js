'use strict';
const Content = (() => {
 const senses=new Map(),aliases=new Map(),selected=new Map();
 function register(units,kind){for(const u of units)u.lessons.forEach((e,i)=>{
  const same=[...senses.values()].find(x=>x.wordId===e.wordId&&x.pos===e.pos&&x.meaning===e.meaning);const id=same?.senseId||e.senseId||`${kind}:${u.id}:${i}`;
  e.senseId=id;senses.set(id,e);aliases.set(`${kind}:${u.id}:${i}`,id);
 });}
 function resolve(key){return senses.get(aliases.get(key)||key)||null;}
 function select(entryKey,sense){if(sense?.senseId){senses.set(sense.senseId,sense);selected.set(entryKey,sense.senseId);}}
 function forEntry(entryKey){return resolve(selected.get(entryKey))||[...senses.values()].find(s=>'w'+s.wordId===entryKey)||null;}
 function keyForWord(id){return (resolve(selected.get('w'+id))?selected.get('w'+id):null)||[...senses.values()].find(s=>s.wordId===id)?.senseId||'word:'+id;}
 return {register,resolve,select,forEntry,keyForWord,senses,selected};
})();
