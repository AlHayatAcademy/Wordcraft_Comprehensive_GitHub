"""Reproducible editorial expansion. Never infer a source publisher or CEFR label."""
import json,hashlib
from pathlib import Path
load=lambda f:json.loads(Path(f).read_text())
def write(f,x):Path(f).write_text(json.dumps(x,ensure_ascii=False,separators=(',',':')))
data=load('data.json');refs=load('reference.json');units=load('curriculum.json');tax=load('taxonomy.json');aliases=load('reference-aliases.json');families=load('family-lessons.json')
by={w['word']:w for w in data};rby={w['word']:w for w in refs};nid=max(w['id'] for w in data)+1
sections=[]
for line in Path('scripts/communication-course.txt').read_text().splitlines():
 if line.startswith('# '):sections.append({'title':line[2:],'rows':[]})
 elif line:sections[-1]['rows'].append(line.split('|'))
units=[u for u in units if not u['id'].startswith('communication-')]
for i,section in enumerate(sections):
 uid=f'communication-{i+1}';lessons=[]
 for j,(name,pos,meaning,urdu,combo,example,translation) in enumerate(section['rows']):
  if name not in by:
   r=rby.get(name);w={'id':nid,'word':name,'count':0,'articles':0,'sources':[],'forms':[name],'senses':[],'examples':[],'band':'Intermediate','category':'Communication','origin':'Original Wordcraft teaching','examTags':[]};nid+=1
   if r:w['legacyReferenceId']=r['id'];w['senses']=r['senses'];refs.remove(r);aliases[r['id']]=w['id']
   data.append(w);by[name]=w
  w=by[name];w.setdefault('teachingSenseIds',[]);sid=f'communication:{uid}:{j}'
  if sid not in w['teachingSenseIds']:w['teachingSenseIds'].append(sid)
  e={'senseId':sid,'wordId':w['id'],'word':name,'pos':pos,'meaning':meaning,'urdu':urdu,'collocation':combo,'example':example,'exampleUrdu':translation,'tip':f'Use {combo} with this meaning. Compare the model before changing the situation.','patterns':[combo],'register':'neutral','domain':'Communication','communicativeFunction':section['title'],'difficulty':{'label':'Communication elective','basis':'Internal sequence; not a CEFR rating'},'provenance':{'definition':'Original Wordcraft editorial lesson','publisherVerification':False},'editorialStatus':'bilingual-teaching','synonyms':[],'antonyms':[],'familyNote':'No opposite or family form is claimed without separate sense review.','stage':['Start here','Everyday English','Study and work','Advanced reading'][min(3,i//5)]}
  lessons.append(e)
  if not w['senses']:w['senses']=[{'pos':pos,'meaning':meaning,'examples':[example],'synonyms':[],'category':'communication'}];w.update(urdu=urdu,examples=[example],exampleUrdu=translation,collocation=combo,usageTip=e['tip'],exampleType='original')
  key='w'+str(w['id']);m=tax['entries'].setdefault(key,{'categories':[],'expressionType':'word','register':'neutral','topics':[],'origin':{'language':'unreviewed'},'review':'editorial','contexts':[]});m['review']='editorial';cats=['everyday']
  if pos=='phrasal verb':cats+=['phrasal'];m['expressionType']='phrasal verb';e['separability']='inseparable: lead to a result'
  elif pos=='linking expression':cats+=['linker'];m['expressionType']='linking expression'
  elif pos=='fixed expression':cats+=['fixed'];m['expressionType']='fixed expression'
  elif pos in ['noun phrase','verb pattern','prepositional expression']:m['expressionType']=pos
  c={**e,'categories':cats,'topic':'Communication','contextId':uid,'rationale':'Manually authored communicative sense; other senses retain separate metadata.'};m['contexts']=[x for x in m['contexts'] if x.get('senseId')!=sid]+[c];m['categories']=sorted(set(m['categories']+cats));m['topics']=sorted(set(m['topics']+['Communication']));families.setdefault(str(w['id']),{'family':[],'collocations':[],'reviewNote':'No family relationship reviewed for this new entry.'})
 # Short readings are linked model exchanges, with targets in their meaningful original sentences.
 reading='\n'.join(('Learner: ' if k%2==0 else 'Partner: ')+e['example'] for k,e in enumerate(lessons))
 units.append({'id':uid,'title':section['title'],'stage':lessons[0]['stage'],'goal':f'Use vocabulary for {section["title"].lower()} in a practical conversation.','icon':'chat','lessons':lessons,'reading':reading,'readingNote':'An original sequence of model turns for role-play; not an authentic transcript.','outcomes':['Explain each target meaning in your own words','Use two target combinations in a new situation'],'grammar':'Compare the labelled part of speech and the model construction. Keep prepositions with their target expression.','task':'With a partner, create a new situation and use two target combinations. Write your response, then read it aloud.'})
contexts=Path('scripts/communication-contexts.txt').read_text().splitlines()
for e,line in zip([e for u in units if u['id'].startswith('communication-') for e in u['lessons']],contexts):e['practiceExample']=line;e['reviewExample']=line
for w in data:
 if w.get('legacyReferenceId'):tax['entries'].pop('r'+w['legacyReferenceId'],None)
for c in tax['categories']:c['count']=sum(c['id'] in e['categories'] for e in tax['entries'].values())
for w in data:
 if w.get('origin')=='Original Wordcraft teaching':
  e=next(e for u in units for e in u['lessons'] if e['wordId']==w['id']);w.setdefault('sourceSenses',w['senses']);w['senses']=[{'pos':e['pos'],'meaning':e['meaning'],'examples':[e['example']],'synonyms':[],'category':'communication'}]+[s for s in w['sourceSenses'] if s['meaning']!=e['meaning']];w.update(urdu=e['urdu'],examples=[e['example']],exampleUrdu=e['exampleUrdu'],collocation=e['collocation'],usageTip=e['tip'],explanation=e['meaning'],exampleType='original')
write('data.json',data);write('reference.json',refs);write('reference-aliases.json',aliases);write('curriculum.json',units);write('taxonomy.json',tax);write('family-lessons.json',families)
domains=load('domains.json');ids={e['wordId'] for u in units+domains for e in u['lessons']};write('course-data.json',[w for w in data if w['id'] in ids])
meta=load('meta.json');meta['allWordIds']=[w['id'] for w in data];meta.update(wordCount=len(data),dictionaryReferenceWords=len(refs),totalUniqueWords=len(data)+len(refs),coreUnitCount=len(units),coreLessonCount=sum(len(u['lessons']) for u in units));meta['levelCounts']={l:sum(w['band']==l for w in data) for l in ['Foundation','Intermediate','Advanced','Challenging']};write('meta.json',meta)
quality=load('quality-audit.json');quality['generalFallbackEntries']=sum(m['review']=='general' for m in tax['entries'].values());write('quality-audit.json',quality)
write('reports/course-inventory.json',{'senseRecords':sum(len(u['lessons']) for u in units+domains),'uniqueWordPosDefinition':len({(e['word'],e['pos'],e['meaning']) for u in units+domains for e in u['lessons']}),'bilingualExampleRecords':sum(bool(e.get('exampleUrdu')) for u in units+domains for e in u['lessons']),'units':len(units),'topics':len(domains),'addedCommunicationLessons':len(sections),'addedCommunicationSenses':160,'externalEditorialValidation':False,'remainingGap':'Topic lessons need a full new example-translation and retrieval-context pass. Existing source-family collections remain inherited reference.'})
