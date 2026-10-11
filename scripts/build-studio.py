"""Build the editorial starter route while preserving existing headword IDs."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda name:json.loads((root/name).read_text())
write=lambda name,obj:(root/name).write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':')))
data=read('data.json');refs=read('reference.json');families=read('family-lessons.json');meta=read('meta.json')
byword={w['word'].casefold():w for w in data};original_ids={w['word']:w['id'] for w in data};nextid=max(w['id'] for w in data)+1
units=[];entries=[]
for line in (root/'scripts/starter-lessons.txt').read_text().splitlines():
 if not line.strip():continue
 if line.startswith('# '):
  name,stage,goal,icon=line[2:].split('|');unit={'id':'core-'+str(len(units)+1),'title':name,'stage':stage,'goal':goal,'icon':icon,'lessons':[]};units.append(unit);continue
 word,pos,meaning,urdu,combo,example,tip=line.split('|')
 assert re.search(r'\b'+re.escape(word)+r'\b',example,re.I),(word,example)
 if word.casefold() not in byword:
  w={'id':nextid,'word':word,'count':0,'articles':0,'senses':[{'pos':pos,'meaning':meaning,'examples':[example],'synonyms':[],'category':'authored'}],'examples':[example],'sources':[],'forms':[word],'band':'Foundation' if len(units)<=6 else 'Intermediate' if len(units)<=12 else 'Advanced','exampleType':'original','category':'Everyday communication','urdu':urdu,'explanation':meaning,'collocation':combo,'collocations':[combo],'usageTip':tip,'origin':'original starter lesson'}
  data.append(w);byword[word.casefold()]=w;families[str(nextid)]={'family':[],'collocations':[]};nextid+=1
 w=byword[word.casefold()];e={'wordId':w['id'],'word':word,'pos':pos,'meaning':meaning,'urdu':urdu,'collocation':combo,'example':example,'tip':tip,'stage':unit['stage'],'unitId':unit['id']};unit['lessons'].append(e);entries.append(e)
assert len(units)==24 and all(len(u['lessons'])==6 for u in units)
assert len({e['word'] for e in entries})==144
refs=[w for w in refs if w['word'].casefold() not in byword]
assert all(byword[word]['id']==id for word,id in original_ids.items())
assert len({w['word'].casefold() for w in data+refs})==len(data)+len(refs)
meta.update(wordCount=len(data),dictionaryReferenceWords=len(refs),totalUniqueWords=len(data)+len(refs),starterLessons=144,starterUnits=24)
meta['levelCounts']={level:sum(w['band']==level for w in data) for level in ['Foundation','Intermediate','Advanced','Challenging']}
quality={'fullEntries':len(data),'referenceEntries':len(refs),'starterLessons':144,'starterUnits':24,'originalIdsPreserved':True,'starterOrdering':'Editorial progression from practical requests to nuanced formal reading; not a certified CEFR placement.','starterContent':'Original sense-specific English definitions, Urdu meanings, complete contextual examples, combinations and usage distinctions.','catalogueQuality':'Inherited content is preserved; not all definitions, translations or examples have received a new sense-by-sense editorial review. Dictionary references remain English-only.','fragmentExamples':sum(any(not re.search(r'[.!?]$',e) for e in w['examples']) for w in data),'extendedOrdering':'Internal bands, then source frequency, example completeness and lexical complexity; not an externally validated difficulty scale.'}
translations=(root/'scripts/starter-urdu-examples.txt').read_text().splitlines()
assert len(translations)==len(entries)
for e,t in zip(entries,translations):e['exampleUrdu']=t
write('curriculum.json',units);write('data.json',data);write('reference.json',refs);write('family-lessons.json',families);write('meta.json',meta);write('quality-audit.json',quality)
audit=read('coverage-audit.json');audit.update(fullLessonWords=len(data),dictionaryReferenceWords=len(refs),totalUniqueWords=len(data)+len(refs),starterLessons=144,starterUnits=24);write('coverage-audit.json',audit)
print({'words':len(data),'reference':len(refs),'unique':len(data)+len(refs),'newStarterHeadwords':len(data)-len(original_ids),'units':len(units)})
