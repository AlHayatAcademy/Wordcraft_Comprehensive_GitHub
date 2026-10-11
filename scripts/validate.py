import json,re
from pathlib import Path
load=lambda f:json.loads(Path(f).read_text())
data,refs,expressions=map(load,['data.json','reference.json','expressions.json']);units=load('curriculum.json');topics=load('domains.json');tax=load('taxonomy.json');all_keys={'w'+str(w['id']) for w in data}|{'r'+w['id'] for w in refs}|{'e'+w['id'] for w in expressions}
assert len({w['id'] for w in data})==len(data)
assert len({w['word'].lower() for w in data+refs})==len(data)+len(refs)
assert all_keys==set(tax['entries']), 'orphan or unclassified metadata'
for c in tax['categories']:assert c['count']==sum(c['id'] in e['categories'] for e in tax['entries'].values())
lessons=[e for u in units+topics for e in u['lessons']];assert len({(e['word'],e['pos'],e['meaning']) for e in lessons})>=500
for e in lessons:
 assert all(e.get(k) for k in ['senseId','word','wordId','pos','meaning','urdu','example','collocation'])
 assert e['wordId'] in {w['id'] for w in data}
 assert re.search(r'[.!?]$',e['example'])
for e in [e for u in units for e in u['lessons']]:assert e.get('exampleUrdu')
for u in units:assert 5<=len(u['lessons'])<=8
attachment=load('reports/attachment-ids.json')
assert all(any(x['id']==w['id'] and x['word']==w['word'] for x in data) for w in attachment['words'])
assert all(any(x['id']==r['id'] and x['word']==r['word'] for x in refs) or any(x.get('legacyReferenceId')==r['id'] and x['word']==r['word'] for x in data) for r in attachment['references'])
assert all(any(x['id']==e['id'] and x['phrase']==e['phrase'] for x in expressions) for e in attachment['expressions'])
manifest=load('preservation-manifest.json')
assert all(any(x['id']==w['id'] and x['word']==w['word'] for x in data) for w in manifest['wordEntries'])
assert all(any(x['id']==r['id'] and x['word']==r['word'] for x in refs) or any(x.get('legacyReferenceId')==r['id'] and x['word']==r['word'] for x in data) for r in manifest['dictionaryEntries'])
assert all(any(x['id']==e['id'] and x['phrase']==e['phrase'] for x in expressions) for e in manifest['expressionEntries'])
report={'words':len(data),'referenceHeadwords':len(refs),'uniqueHeadwords':len(data)+len(refs),'expressions':len(expressions),'uniqueEntryKeys':len(all_keys),'courseRecords':len(lessons),'distinctTeachingSenses':len({(e['word'],e['pos'],e['meaning']) for e in lessons}),'bilingualExampleRecords':sum(bool(e.get('exampleUrdu')) for e in lessons),'guidedUnits':len(units),'topicUnits':len(topics),'sourceIdsPreserved':True,'sourceHeadwordDuplicates':0,'unclassifiedEntries':0,'rawStartupContentBytes':sum(Path(f).stat().st_size for f in ['course-data.json','sources.json','meta.json','usage.json','curriculum.json','domains.json']),'fullNewEditorialReviewOfAllSourceRecords':False}
Path('reports/verified-inventory.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
