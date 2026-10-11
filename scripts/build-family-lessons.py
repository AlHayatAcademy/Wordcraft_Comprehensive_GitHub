"""Build evidenced family lessons; never synthesize suffix forms or missing examples.
Inputs: existing site bank, WordNet 3.0 ZIP, explicitly authored lesson packs.
"""
import json,re,zipfile,sys,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]; d=root/'dist' if (root/'dist').is_dir() else root
data=json.loads((d/'data.json').read_text());bank={w['word'].casefold():w for w in data}; expressions=json.loads((d/'expressions.json').read_text())
z=zipfile.ZipFile(sys.argv[1]); synsets={}; lemmas=collections.defaultdict(list); links=collections.defaultdict(set)
posnames={'n':'noun','v':'verb','a':'adjective','s':'adjective','r':'adverb'}
for fname,pos in [('noun','n'),('verb','v'),('adj','a'),('adv','r')]:
 for line in z.read('wordnet/data.'+fname).decode().splitlines():
  if not line or line.startswith(' '):continue
  fields,gloss=line.split('|',1);t=fields.split();n=int(t[3],16);words=[re.sub(r'\([ap]\)$|\(ip\)$','',t[4+2*i]).replace('_',' ') for i in range(n)];p=4+2*n;np=int(t[p]);p+=1
  key=(pos,t[0]); definition=gloss.strip().split('; "')[0].rstrip('; ');examples=re.findall(r'"([^\"]+)"',gloss)
  synsets[key]={'words':words,'pos':posnames[t[2]],'meaning':definition,'examples':examples,'pointers':[]}
  for word in words:lemmas[word.casefold()].append(key)
  for _ in range(np):
   symbol,offset,tp,st=t[p:p+4];p+=4;tp='a' if tp=='s' else tp
   if symbol in ['+','\\'] and st!='0000':synsets[key]['pointers'].append((symbol,(tp,offset),int(st[:2],16)-1,int(st[2:],16)-1))
for key,s in synsets.items():
 for symbol,target,si,ti in s['pointers']:
  if target in synsets and si<len(s['words']) and ti<len(synsets[target]['words']):
   a=s['words'][si].casefold();b=synsets[target]['words'][ti].casefold()
   if re.fullmatch(r'[a-z]+(?:-[a-z]+)*',a) and re.fullmatch(r'[a-z]+(?:-[a-z]+)*',b):
    links[a].add((b,target));links[b].add((a,key))
def contains(word,text):return bool(re.search(r'(?<![a-z])'+re.escape(word)+r'(?:s|es|ed|ing)?(?![a-z])',text,re.I))
def lesson(word,key=None):
 w=bank.get(word);key=key or next(iter(lemmas.get(word,[])),None);s=synsets.get(key)
 if w and (not s or w['senses'][0]['pos']==s['pos']):
  return {'word':word,'pos':w['senses'][0]['pos'],'meaning':w['senses'][0]['meaning'],'urdu':w['urdu'],'example':w['examples'][0],'source':'Existing learning bank','wordId':w['id']}
 if s:
  ex=next((e for e in s['examples'] if contains(word,e)),'')
  return {'word':word,'pos':s['pos'],'meaning':s['meaning'],'urdu':'','example':ex,'source':'Princeton WordNet 3.0','dictionarySense':':'.join(key)}
 return None
curated=json.loads((d/'family-authored.json').read_text())
for word,value in curated.items():
 if word not in bank:raise ValueError('Unknown curated root '+word)
 for kind in ['family','collocations']:
  for item in value[kind]:
   for field in (['word','pos','meaning','urdu','example'] if kind=='family' else ['phrase','meaning','urdu','example']):
    assert isinstance(item.get(field),str) and item[field].strip(),(word,field)
   item['source']='Original learning lesson · editorially reviewed'
# Reuse reviewed family lessons on existing sibling headwords, preserving their IDs.
expanded=dict(curated)
for value in list(curated.values()):
 for member in value['family']:
  key=member['word']
  if key in bank and key not in expanded:
   expanded[key]={'family':value['family'],'collocations':[c for c in value['collocations'] if contains(key,c['phrase'])]}
exprindex=collections.defaultdict(list)
for e in expressions:
 if e['type']=='collocation':
  for word in set(re.findall(r'[a-z]+(?:-[a-z]+)*',e['phrase'].lower())):
   if word in bank:exprindex[word].append({'phrase':e['phrase'],'meaning':e['meaning'],'urdu':e['urdu'],'example':e['example'],'source':'Existing collocation studio','expressionId':e['id']})
result={}; unresolved=[]
for w in data:
 name=w['word']; base=lesson(name);family={(name,base['pos']):base}
 for f in w.get('wordFamily',[]):
  member=lesson(f.casefold())
  if member:family[(f.casefold(),member['pos'])]=member
  else:unresolved.append({'root':name,'familyWord':f,'reason':'No definition in available bank or WordNet; not expanded by guessing.'})
 # One lexical edge in either direction; do not turn distant semantic graphs into a root family.
 for f,key in sorted(links.get(name,[])):
  if f!=name:family.setdefault((f,synsets[key]['pos']),lesson(f,key))
 special=expanded.get(name,{})
 for item in special.get('family',[]):family[(item['word'].casefold(),item['pos'])]=item
 coll={i['phrase'].casefold():i for i in exprindex.get(name,[])}
 for item in special.get('collocations',[]):coll[item['phrase'].casefold()]=item
 result[str(w['id'])]={'family':list(family.values()),'collocations':list(coll.values()),'authored':bool(special)}
summary={'rootCount':len(result),'authoredRoots':len(curated),'rootsSharingAuthoredFamilies':len(expanded),'familyLessons':sum(len(v['family']) for v in result.values()),'familyLessonsWithExamples':sum(bool(i['example']) for v in result.values() for i in v['family']),'explainedCollocations':sum(len(v['collocations']) for v in result.values()),'rootsWithRelatedMembers':sum(len(v['family'])>1 for v in result.values()),'unexpandedLegacyFamilyWords':unresolved,'method':'Existing bank plus WordNet direct derivational/pertainym links and reviewed original lessons. No automatic suffix generation; no claim of exhaustive possible derivatives. Empty examples are explicitly shown as unavailable, not fabricated.'}
summary.update({'uniqueExplainedCombinations':len({i['phrase'].casefold() for x in result.values() for i in x['collocations']}),'originalFamilyLessons':sum(len(v['family']) for v in curated.values()),'originalCombinationLessons':sum(len(v['collocations']) for v in curated.values()),'exampleLimitation':'Dictionary entries without a target-word example are labelled explicitly; missing sentences and Urdu translations are not invented.'})
(d/'family-lessons.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')))
(d/'family-review.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='unexpandedLegacyFamilyWords'}))
