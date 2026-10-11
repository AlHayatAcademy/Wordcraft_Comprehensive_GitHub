"""Apply original, individually authored senses; rerunnable without duplicate entries."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((root/n).read_text())
write=lambda n,v:(root/n).write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')))
words=read('data.json');refs=read('reference.json');expr=read('expressions.json');tax=read('taxonomy.json');families=read('family-lessons.json');aliases=read('reference-aliases.json')
by={w['word'].casefold():w for w in words};rb={w['word'].casefold():w for w in refs};eb={e['phrase'].casefold():e for e in expr};nextid=max(w['id'] for w in words)+1
sources={'no cap':'https://www.merriam-webster.com/slang/no-cap','rizz':'https://www.merriam-webster.com/slang/rizz','salty':'https://www.merriam-webster.com/wordplay/salty-meaning','lit':'https://www.merriam-webster.com/wordplay/lit-meaning-origin'}
rows=[]
for line in (root/'scripts/category-additions.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 term,pos,meaning,urdu,example,translation,combo,tip,cats,register,topic,structure=line.split('|');cats=cats.split(',');norm=term.casefold();contextId='added-'+norm.replace(' ','-')
 sense={'pos':pos,'meaning':meaning,'examples':[example],'synonyms':[],'category':'authored'}
 if norm in eb:
  w=eb[norm];key='e'+w['id']
  # Same source expression, revised teaching sense; ID and saved progress are unchanged.
  w.update(meaning=meaning,urdu=urdu,example=example,exampleUrdu=translation,usageTip=tip,explanation=meaning+' '+tip,register=register)
 else:
  if norm not in by:
   old=rb.get(norm);w={'id':nextid,'word':old['word'] if old else term,'count':0,'articles':0,'sources':[],'forms':[term],'band':'Intermediate','exampleType':'original','origin':'original category lesson','senses':([sense]+old.get('senses',[])) if old else [sense]}
   if old:w['legacyReferenceId']=old['id'];aliases[old['id']]=nextid;refs.remove(old);tax['entries'].pop('r'+old['id'],None)
   words.append(w);by[norm]=w;families[str(nextid)]={'family':[],'collocations':[]};nextid+=1
  w=by[norm];key='w'+str(w['id'])
  if w.get('origin')=='original category lesson':
   w.update(urdu=urdu,examples=[example],exampleUrdu=translation,category=topic,explanation=meaning+' '+tip,collocation=combo,collocations=[combo],usageTip=tip)
   w['wordFamilyNote']='No additional derivational family member is taught for this sense; other meanings may have different related forms.'
   opposites={'salty':['calm'],'heavy rain':['light rain'],'strong evidence':['weak evidence']}
   if norm in opposites:w['antonyms']=opposites[norm]
   else:w['antonymNote']='No single natural antonym is taught for this sense. Contrast the full meaning or situation instead.'
   w['senses']=[sense]+[s for s in w['senses'] if s['meaning']!=meaning]
   # Authored combination, not an invented derivational family or antonym.
   families[str(w['id'])]['collocations']=[{'phrase':combo,'meaning':meaning,'urdu':urdu,'example':example}]
 c={'contextId':contextId,'meaning':meaning,'pos':pos,'urdu':urdu,'example':example,'exampleUrdu':translation,'categories':cats,'register':register,'topic':topic,'rationale':'Individually authored and reviewed teaching sense; classifications apply to this sense.','tip':tip}
 if norm in sources:c['sources']=[sources[norm]]
 m=tax['entries'].get(key,{'categories':[],'topics':[],'contexts':[],'origin':{'language':'unreviewed'}})
 m['contexts']=[x for x in m['contexts'] if x.get('contextId')!=contextId]+[c];m.update(categories=sorted(set(x for c in m['contexts'] for x in c['categories'])),topics=sorted(set(c['topic'] for c in m['contexts'])),review='editorial',expressionType=structure)
 regs=set(c['register'] for c in m['contexts']);m['register']=next(iter(regs)) if len(regs)==1 else 'sense-dependent';tax['entries'][key]=m;rows.append({'key':key,'term':term,'contextId':contextId})
for c in tax['categories']:c['count']=sum(c['id'] in m['categories'] for m in tax['entries'].values())
assert all(c['count']>0 for c in tax['categories'])
assert len(set(w['word'].casefold() for w in words+refs))==len(words)+len(refs)
meta=read('meta.json');meta.update(wordCount=len(words),dictionaryReferenceWords=len(refs),referenceWordCount=len(refs),totalUniqueWords=len(words)+len(refs),categoryTeachingSenses=len(rows));meta['levelCounts']={l:sum(w['band']==l for w in words) for l in meta['levelCounts']}
audit=read('quality-audit.json');classified=tax['entries'];pending=[{'key':'w'+str(w['id']),'reason':'No new sense-by-sense classification review completed'} for w in words if 'w'+str(w['id']) not in classified]+[{'key':'e'+e['id'],'reason':'No new sense-by-sense classification review completed'} for e in expr if 'e'+e['id'] not in classified]
audit.update(fullEntries=len(words),referenceEntries=len(refs),classifiedEntries=len(classified),classificationPending=len(pending),dictionaryClassificationPending=sum('r'+r['id'] not in classified for r in refs),emptyCategories=[],categoryCounts={c['id']:c['count'] for c in tax['categories']},categoryTeachingSenses=len(rows))
coverage=read('coverage-audit.json');coverage.update(fullLessonWords=len(words),dictionaryReferenceWords=len(refs),totalUniqueWords=len(words)+len(refs))
for n,v in [('data.json',words),('reference.json',refs),('expressions.json',expr),('taxonomy.json',tax),('family-lessons.json',families),('reference-aliases.json',aliases),('meta.json',meta),('quality-audit.json',audit),('coverage-audit.json',coverage),('classification-review.json',pending),('category-additions.json',{'entries':rows,'sourceNotes':sources,'content':'Original teaching text; source links verify slang meanings and usage. No source examples copied.'})]:write(n,v)
print({'teachingSenses':len(rows),'words':len(words),'references':len(refs),'unique':len(words)+len(refs),'classified':len(classified),'pending':len(pending),'counts':audit['categoryCounts']})
