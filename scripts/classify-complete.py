"""Explicit sense choices plus the user's conservative General fallback policy.
No spelling, difficulty, substring or inherited review flag determines a specialist category.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((root/n).read_text())
write=lambda n,v:(root/n).write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')))
tax=read('taxonomy.json');words=read('data.json');refs=read('reference.json');expr=read('expressions.json')
# Idempotent: rebuild this pass while retaining previously authored classifications.
for key,m in list(tax['entries'].items()):
 if m.get('review')=='general':del tax['entries'][key];continue
 m['contexts']=[c for c in m['contexts'] if not c.get('contextId','').startswith('knowledge:')]
 if not m['contexts']:del tax['entries'][key];continue
 m['categories']=sorted({cat for c in m['contexts'] for cat in c['categories']})
 m['topics']=sorted({c['topic'] for c in m['contexts']})
by={w['word'].casefold():('w'+str(w['id']),w) for w in words}
by.update({w['word'].casefold():('r'+w['id'],w) for w in refs})
# Individually inspected homographs and sense ordering, not guessed from the headword.
indices={'define':1,'distribution':1,'obtain':1,'response':2,'source':1,'demonstrate':1,'exemplify':1,'concur':1,'procure':1,'anemia':1,'artery':1,'inflammation':3,'syndrome':1,'radiology':1,'atom':1,'atomic':2,'molecule':1,'molecular':1,'mutation':1,'nucleus':1,'species':1,'acceleration':2,'momentum':1,'resistance':2,'current':1,'gravity':2,'firewall':2,'testament':1,'conviction':1,'bond':2,'deflation':1,'department':1,'director':3,'enterprise':1,'supervisor':1,'union':5,'apostrophe':1,'epithet':1,'tragedy':1,'thus':1,'kid':1,'agenda':1}
# Meanings are too broad/mixed, or no suitable specialist sense exists in this bank.
exclude={'authority','chronic','immunity','diagnosis','binary','protocol','cache','catalyst','solution','asset','surplus','deficit','competitor','interview','yeah','okay','insofar','lyric','epigram','irony','protagonist','epithet'}
corrections={'velocity':'The rate of change of position, including direction.','voltage':'The electric potential difference between two points.','hypertension':'A condition involving persistently high blood pressure.','genome':'The complete set of genetic material in an organism.'}
# A reference has no verified Urdu teaching translation. A non-first sense cannot borrow the first sense's Urdu gloss.
teaching={}
for line in (root/'scripts/sense-teaching.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 term,i,meaning,urdu,example,translation,combo,tip=line.split('|');teaching[(term,int(i))]={'meaning':meaning,'urdu':urdu,'example':example,'exampleUrdu':translation,'collocation':combo,'tip':tip}
sense_sources=read('scripts/sense-sources.json')
new=[]
for gi,g in enumerate(read('scripts/classification-groups.json')):
 for term in g['words'].split():
  if term in exclude or term not in by:continue
  key,w=by[term];i=indices.get(term,0)
  if i>=len(w['senses']):continue
  s=w['senses'][i];contextId='knowledge:'+g['topic']+':'+term+':'+str(i)
  examples=s.get('examples',[]) or (w.get('examples',[]) if i==0 else [])
  meaning=corrections.get(term,s['meaning'])
  c={'contextId':contextId,'senseIndex':i,'meaning':meaning,'pos':s['pos'],'categories':g['categories'],'register':g['register'],'topic':g['topic'],'example':examples[0] if examples else '', 'rationale':'Explicit sense-by-sense classification using the displayed meaning; no inference from word difficulty or an inherited category flag.'}
  if i==0 and key.startswith('w'):c['urdu']=w.get('urdu','')
  if (term,i) in teaching:c.update(teaching[(term,i)])
  if term in corrections:c['revisedDefinition']=True
  if term in sense_sources:c['sources']=[sense_sources[term]]
  m=tax['entries'].get(key,{'categories':[],'topics':['General'],'contexts':[],'origin':{'language':'unreviewed'}})
  # Keep the authored route sense rather than duplicate equivalent classifications.
  if any(c['meaning']==old['meaning'] and set(g['categories']).issubset(old['categories']) and old['topic']==c['topic'] for old in m['contexts']):continue
  m['contexts'].append(c);m['review']='editorial';m['categories']=sorted(set(m['categories']+g['categories']));m['topics']=sorted(set(m['topics']+[g['topic']]));m.setdefault('expressionType','word')
  regs={x['register'] for x in m['contexts']};m['register']=next(iter(regs)) if len(regs)==1 else 'sense-dependent';tax['entries'][key]=m;new.append({'key':key,'term':term,'senseIndex':i,'categories':g['categories'],'topic':g['topic']})
eby={e['phrase']:e for e in expr}
for g in read('scripts/expression-classification.json'):
 for phrase in g['phrases'].split('|'):
  if phrase not in eby:continue
  e=eby[phrase];key='e'+e['id']
  if key in tax['entries']:continue # Retain prior individually revised senses/grammar.
  cats=g['categories'][:];reg=g['register'];structure=g['structure'];pos=g['pos']
  if phrase=='every cloud has a silver lining':cats=['proverb'];reg='neutral';structure='proverb';pos='sentence'
  if phrase=='in the long run':cats=['fixed'];structure='fixed adverbial expression';pos='adverb'
  if 'idiom' in cats:pos='noun' if phrase=='a double-edged sword' else 'adjective' if phrase in {'in hot water','on cloud nine'} else 'verb'
  if phrase=='come across':structure='inseparable multiword verb' # No forced particle/preposition distinction.
  if phrase=='set a goal':meaning='Decide on a target to work towards.'
  else:meaning=e['meaning']
  c={'contextId':'knowledge:expression:'+phrase,'meaning':meaning,'pos':pos,'categories':cats,'register':reg,'topic':g['topic'],'example':e['example'],'urdu':e['urdu'],'tip':e['usageTip'],'structure':structure,'rationale':'Individually inspected meaning and example; grammatical type is independent of the inherited source collection.'}
  # Phrasal subtype follows the reviewed example. Do not assert one placement rule for every sense.
  if 'phrasal' in cats:
   intransitive={'break down','calm down','carry on','catch up','check in','close down','come back','come in','come out','end up','fall apart','get up','go ahead','go back','go on','grow up','hang up','hold on','keep on','move on','pass away','run out','show up','take off','turn up','wake up'}
   placement='intransitive in this example' if phrase in intransitive else 'separable in this sense; put a personal-pronoun object between the verb and particle'
   c['separability']=placement;c['tip']='Object placement: '+placement+'. '+e['usageTip']
  tax['entries'][key]={'categories':cats,'topics':[g['topic']],'contexts':[c],'origin':{'language':'unreviewed'},'register':reg,'expressionType':structure,'review':'editorial'}
  new.append({'key':key,'term':phrase,'categories':cats,'topic':g['topic']})
# Inspected expression meanings, including explicit proverb/fixed-expression exceptions.
for d in read('scripts/inspected-expressions.json'):
 if not d['include']:continue
 e=next(e for e in expr if e['id']==d['id']);assert e['phrase']==d['phrase'] and e['meaning']==d['meaning'],d['id']
 key='e'+e['id']
 if key in tax['entries']:continue
 cats=[d['category']]+(['informal'] if d['register']=='informal' else [])
 c={'contextId':'knowledge:inspected:'+e['id'],'meaning':d.get('revisedMeaning',e['meaning']),'pos':d['pos'],'categories':cats,'register':d['register'],'topic':d['topic'],'example':e['example'],'urdu':e['urdu'],'tip':d.get('tip',e['usageTip']),'rationale':'Meaning individually inspected. Figurative idioms, proverbs and fixed expressions are separated explicitly; register remains unspecified when uncertain.'}
 tax['entries'][key]={'categories':cats,'topics':[d['topic']],'contexts':[c],'origin':{'language':'unreviewed'},'register':d['register'],'expressionType':{'idiom':'idiomatic expression','fixed':'fixed expression','proverb':'proverb'}[d['category']],'review':'editorial'}
 new.append({'key':key,'term':e['phrase'],'categories':cats,'topic':d['topic']})
for d in read('scripts/inspected-collocations.json'):
 e=next(e for e in expr if e['id']==d['id']);assert e['phrase']==d['phrase'] and e['meaning']==d['meaning'],d['id'];key='e'+e['id']
 if key in tax['entries']:continue
 c={'contextId':'knowledge:combination:'+e['id'],'meaning':d.get('revisedMeaning',e['meaning']),'pos':d['pos'],'categories':d['categories'],'register':d['register'],'topic':d['topic'],'example':e['example'],'urdu':e['urdu'],'tip':e['usageTip'],'structure':d['structure'],'rationale':'Combination and meaning individually inspected; a topic does not automatically imply academic or formal register.'}
 tax['entries'][key]={'categories':d['categories'],'topics':[d['topic']],'contexts':[c],'origin':{'language':'unreviewed'},'register':d['register'],'expressionType':d['structure'],'review':'editorial'}
 new.append({'key':key,'term':e['phrase'],'categories':d['categories'],'topic':d['topic']})
# The fallback is organisational, not a claim of everyday frequency or neutral register.
for key,w in [('w'+str(w['id']),w) for w in words]+[('r'+w['id'],w) for w in refs]+[('e'+e['id'],e) for e in expr]:
 if key not in tax['entries']:
  tax['entries'][key]={'categories':['everyday'],'review':'general','expressionType':'unclassified expression' if key.startswith('e') else 'word','register':'unreviewed','topics':['General'],'contexts':[],'origin':{'language':'unreviewed'}}
 elif not tax['entries'][key]['categories']:
  tax['entries'][key]['categories']=['everyday']
  for c in tax['entries'][key]['contexts']:c['categories']=['everyday']
for c in tax['categories']:
 if c['id']=='everyday':c['name']='General vocabulary'
 c['count']=sum(c['id'] in m['categories'] for m in tax['entries'].values())
tax.update(schemaVersion=2,notes='Every entry has a category. General vocabulary includes uncertainty fallbacks; this is not a frequency or proficiency claim. Specialist classifications refer to explicitly selected senses. Register and origin remain unreviewed where uncertain.')
classified=sum(m['review']=='editorial' for m in tax['entries'].values());general=sum(m['review']=='general' for m in tax['entries'].values())
audit=read('quality-audit.json');audit.update(classifiedEntries=classified,generalFallbackEntries=general,authoredSenseLessons=len(teaching),specialistSenseDecisions=len(new),unassignedEntries=0,classificationPending=0,uncertainLearningEntries=sum(m['review']=='general' and not k.startswith('r') for k,m in tax['entries'].items()),dictionaryClassificationPending=0,uncertainDictionaryEntries=sum(m['review']=='general' and k.startswith('r') for k,m in tax['entries'].items()),categoryCounts={c['id']:c['count'] for c in tax['categories']},classificationPolicy='Specific labels only for reviewed senses; otherwise General vocabulary by user instruction. Fallback does not verify inherited content.')
write('taxonomy.json',tax);write('quality-audit.json',audit);write('classification-decisions.json',{'newSenseDecisions':new,'fallbackCount':general,'policy':audit['classificationPolicy']})
write('classification-review.json',[{'key':key,'assignedCategory':'everyday','reason':'General vocabulary fallback: specialist type/register/domain not confirmed; inherited content may still need editorial review.'} for key,m in tax['entries'].items() if m['review']=='general'])
print({'specialistOrReviewed':classified,'generalFallback':general,'newSenseDecisions':len(new),'authoredSenseLessons':len(teaching),'unassigned':0,'categoryCounts':audit['categoryCounts']})
