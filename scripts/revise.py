from pathlib import Path
import json

def load(f):return json.loads(Path(f).read_text())
def write(f,x):Path(f).write_text(json.dumps(x,ensure_ascii=False,separators=(',',':')))
d=load('data.json'); refs=load('reference.json');tax=load('taxonomy.json');fam=load('family-lessons.json');core=load('curriculum.json');domains=load('domains.json')
by={w['word']:w for w in d}
# Keep all source sentences separately; amend the learner-facing monetary example.
w=by['currency'];w.setdefault('sourceExamples',w['examples'][:]);w['examples']=['You can exchange foreign currency at this bank.'];w['senses'][0]['examples']=w['examples'];w['exampleType']='original';w['exampleUrdu']='آپ اس بینک میں غیر ملکی کرنسی تبدیل کر سکتے ہیں۔'
by['current']['senses'][0]['category']='adj.all'
for r in refs:
 if r['word']=='commuter':
  r.setdefault('sourceSenses',r['senses'][:])
  person={'pos':'noun','meaning':'A person who regularly travels between home and a place of work or study.','synonyms':[],'examples':['The commuter takes the bus to work every morning.'],'urdu':'روزانہ کام یا تعلیم کے لیے سفر کرنے والا شخص','exampleUrdu':'یہ مسافر ہر صبح کام پر بس سے جاتا ہے۔','definitionSource':'Original teaching correction'}
  r['senses']=[person]+[s for s in r['sourceSenses'] if s['meaning']!=person['meaning']];r['editorialNote']='Person sense added; inherited train sense retained separately.'
for c in tax['entries']['w'+str(by['policy']['id'])]['contexts']:
 if 'school policy' in c.get('example',''):c['topic']='Education'
tax['entries']['w'+str(by['policy']['id'])]['topics']=list({c['topic'] for c in tax['entries']['w'+str(by['policy']['id'])]['contexts']})
# Explicit relationships, no semantic links presented as derivations.
for name in ['state','current','currency','issue']:
 f=fam[str(by[name]['id'])];f.setdefault('legacyFamily',f['family']);f['reviewNote']='Inherited links retained as reference evidence; curated relationships below apply only to the specified sense.'
fam[str(by['state']['id'])]['family']=[{'word':'statement','pos':'noun','meaning':'Something said or written to give information or an opinion.','urdu':'بیان','example':'Her statement explains why the meeting was postponed.','exampleUrdu':'اس کا بیان واضح کرتا ہے کہ اجلاس کیوں ملتوی ہوا۔','relationship':'derivation','senseNote':'Related to state as a verb meaning express in words, not the noun meaning a territory.','source':'Original teaching correction','wordId':by['statement']['id']}]
fam[str(by['state']['id'])]['relatedVocabulary']=[{'word':'civil','relationship':'related vocabulary','note':'Connected with citizens and public life; not a morphological derivative of state.'}]
fam[str(by['current']['id'])]['family']=[{'word':'currently','pos':'adverb','meaning':'At the present time.','urdu':'فی الحال؛ اس وقت','example':'The library is currently closed for repairs.','relationship':'derivation','senseNote':'From the adjective current meaning existing now.','source':'Original teaching correction'}]
fam[str(by['currency']['id'])]['family']=[]
fam[str(by['currency']['id'])]['relatedVocabulary']=[{'word':'current','relationship':'etymological relationship','note':'A historical relationship does not make these words interchangeable in the monetary sense.'}]
fam[str(by['issue']['id'])]['family']=[{'word':'issuer','pos':'noun','meaning':'A person or organisation that officially supplies or publishes something.','urdu':'جاری کرنے والا شخص یا ادارہ','example':'The issuer of the certificate must sign it.','relationship':'derivation','senseNote':'From the verb issue meaning supply or publish; not the noun meaning a problem.','source':'Original teaching correction'},{'word':'issuing','pos':'verb (-ing form)','meaning':'Providing or publishing something officially.','urdu':'جاری کرنا','example':'The office is issuing new identity cards this week.','relationship':'inflection','senseNote':'The -ing form of the supplying or publishing verb sense. It can also function as a verbal noun.','source':'Original teaching correction'}]
for name in ['state','current','currency','issue']:
 w=by[name];w['familyReview']='sense-specific';w['wordFamily']=[]
# Stable lesson IDs and explicit incomplete editorial fields.
for kind,units in [('core',core),('topic',domains)]:
 for u in units:
  for i,e in enumerate(u['lessons']):
   e['senseId']=f'{kind}:{u["id"]}:{i}';e['patterns']=[e.get('tip','Use the target combination in a complete sentence.')];e['register']='neutral';e['communicativeFunction']=u.get('goal','');e['domain']=u.get('name','Practical communication');e['difficulty']={'label':e.get('stage','Topic elective'),'basis':'Internal route ordering; not validated CEFR'};e['provenance']={'definition':'Original Wordcraft lesson','publisherVerification':False};e['editorialStatus']='bilingual-teaching' if e.get('exampleUrdu') else 'translation-review-needed';e['synonyms']=[];e['antonyms']=[];e['familyNote']='Consult the sense-specific family panel; no family member or opposite is implied by an empty list.'
write('data.json',d);write('reference.json',refs);write('taxonomy.json',tax);write('family-lessons.json',fam);write('curriculum.json',core);write('domains.json',domains)
ids={e['wordId'] for u in core+domains for e in u['lessons']};write('course-data.json',[w for w in d if w['id'] in ids])
write('reports/content-corrections.json',{'corrections':['state/civil moved to related vocabulary','currency monetary example separated from general-acceptance source example','commuter person and train senses separated','current adjective category and family corrected','issue supplying/publishing family distinguished from problem noun','school-policy topic changed from Politics to Education'],'preservedWords':len(d),'preservedReferences':len(refs),'preservedExpressions':len(load('expressions.json')),'teachingSenses':sum(len(u['lessons']) for u in core+domains),'bilingualExampleSenses':sum(bool(e.get('exampleUrdu')) for u in core+domains for e in u['lessons'])})
