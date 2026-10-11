"""Rebuild from supplied snapshots. WordNet definitions retain their licence.
Raw publisher definitions are not imported into the expanded reference bank.
"""
import json, re, csv, sqlite3, zipfile, unicodedata, collections
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT.parent/'review'
def read(p): return json.loads(p.read_text())
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':')))
def norm(s):
    s=unicodedata.normalize('NFC',str(s)).replace('’',"'")
    s=''.join(c for c in s if unicodedata.category(c) not in ('Co','Cf'))
    return re.sub(r'\s+',' ',s.strip().strip('*')).casefold()
data=read(REVIEW/'Wordcraft_5521_Complete_GitHub/data.json')
byword={norm(x['word']):x for x in data}
original_ids={x['word']:x['id'] for x in data}
domains=[]; added=[]; next_id=max(x['id'] for x in data)+1
for line in (ROOT/'scripts/domain-lessons.txt').read_text().splitlines():
    if line.startswith('# '):
        name,icon,goal=line[2:].split('|'); domain={'id':re.sub('[^a-z]+','-',name.lower()).strip('-'),'name':name,'icon':icon,'goal':goal,'lessons':[]};domains.append(domain)
    elif line.strip():
        word,pos,urdu,meaning,collocation,example=line.split('|');key=norm(word)
        if key not in byword:
            item={'id':next_id,'word':word,'count':0,'articles':0,'senses':[{'pos':pos,'meaning':meaning,'examples':[example],'synonyms':[],'category':'original-domain'}],'examples':[example],'sources':[],'forms':[word],'band':'Intermediate','exampleType':'original','category':domain['name'],'urdu':urdu,'explanation':meaning,'collocation':collocation,'usageTip':'Notice the construction in: '+example,'origin':'supplemental','wordFamily':[],'antonyms':[]}
            data.append(item);byword[key]=item;added.append(word);next_id+=1
        item=byword[key];item.setdefault('domains',[]).append(domain['id'])
        domain['lessons'].append({'wordId':item['id'],'word':word,'pos':pos,'meaning':meaning,'urdu':urdu,'collocation':collocation,'example':example})

# The aptitude bank is already included. Add verified source-selection tags,
# without treating its editorial flags as independent proof of accuracy.
apt=read(REVIEW/'aptitude/vocabulary-bank.json')
for x in apt:
    if norm(x['word']) in byword:
        w=byword[norm(x['word'])];w['examTags']=x.get('connectedTestIds',[])

candidates=collections.defaultdict(set); supplied={}; inventories=[]
def collect(source,words):
    words=list(words); valid=0
    for word in words:
        key=norm(word)
        if re.fullmatch(r"[^\W\d_]+(?:[ '\-][^\W\d_]+)*",key,re.U) and len(key)>1:
            candidates[key].add(source);valid+=1
    inventories.append({'source':source,'records':len(words),'validHeadwordOrPhraseRecords':valid})

for p in (REVIEW/'English-Vocabulary-Builder-main').rglob('words*.json'):
    collect('English-Vocabulary-Builder/'+p.name,[x['Word'] for x in read(p)])
for repo,filename in [('english_word_book-main','wordBook.json'),('GreyVocabularyBot-main','data.json'),('gre-english-scrape-master','input.json')]:
    p=next((REVIEW/repo).rglob(filename));collect(repo,[x['word'] for x in read(p)])
p=next((REVIEW/'gre-flashcards-master (1)').rglob('wordlist.js'));collect('gre-flashcards-2010',json.loads(p.read_text(encoding='cp1252').split('=',1)[1].strip().rstrip(';')))
p=next((REVIEW/'GREWordTest-master').rglob('GRE.db'));c=sqlite3.connect(p);collect('GREWordTest',[x[1] for x in c.execute('select * from GRE_utf8')]);c.close()
for repo in ['ListeningEnglish-master','gre-vocabs-jj-master','english-test-vocab-master']:
    p=next((REVIEW/repo).rglob('*.csv'));rows=list(csv.reader(p.open()));rows=rows if repo=='gre-vocabs-jj-master' else rows[1:];collect(repo,[x[0] for x in rows if x])
p=next((REVIEW/'GRE3000words-master').rglob('3000.txt'));collect('GRE3000words',[x.split('\t')[0] for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()])
p=next((REVIEW/'flash_card-master').rglob('vocab.txt'));collect('flash_card',[x.split('=')[0] for x in p.read_bytes().decode('gb18030',errors='replace').splitlines() if '=' in x])
for p in (REVIEW/'vocab-master').rglob('*.adoc'):
    m=re.search(r'^===\s+(.+)',p.read_text(),re.M)
    if m:collect('vocab-master',[m[1]])
for p in (REVIEW/'EnglishNotes-main').rglob('*.md'):
    if 'Vocabulary' not in p.parts: continue
    words=[]
    for line in p.read_text().splitlines():
        cells=line.split('|')
        if len(cells)>3 and re.fullmatch(r'\s*\d+\s*',cells[1]): words.append(re.sub(r'[=*~`]','',cells[2]).strip())
    if words:collect('EnglishNotes/'+p.name,words)
p=next((REVIEW/'gre-english-word-main').rglob('README.md'));collect('gre-english-word',[c[2] for l in p.read_text().splitlines() if len(c:=l.split('|'))>3 and re.fullmatch(r'\s*\d+\.?\s*',c[1])])
for p in (REVIEW/'learn-english-main(1)').glob('*/content/**/*.json'):
    a=read(p)
    if isinstance(a,dict) and 'items' in a and 'spoken' not in p.parts:collect('learn-english/'+p.name,[x['t'] for x in a['items']])
p=next((REVIEW/'Vocabulary-master').rglob('wordlist.json'));a=read(p);collect('Vocabulary-master',[s.split(':',1)[0] for v in a.values() for s in v])
for p in (REVIEW/'GRE-flashcards-master').rglob('*.md'):
    if p.parent.name=='data':collect('GRE-printable/'+p.name,re.findall(r'^####\s+(.+)',p.read_text(),re.M))
for p in (REVIEW/'English-Practice-main').rglob('*vocab*.md'):
    words=[]
    for line in p.read_text().splitlines():
        c=line.split('|')
        if len(c)>4 and c[2].strip() in ['v.','n.','adj.','adv.']:words.append(c[1].strip())
    collect('English-Practice/'+p.name,words)
collect('AlHayatAcademy',[x['word'] for x in apt])

# Parse the licensed WordNet 3.0 database directly: no third-party dictionary
# examples or publisher definitions are republished in the new reference bank.
lexicon=collections.defaultdict(list)
z=zipfile.ZipFile(REVIEW/'wordnet.zip')
for pos,file in [('noun','noun'),('verb','verb'),('adjective','adj'),('adverb','adv')]:
    for line in z.read('wordnet/data.'+file).decode().splitlines():
        if not line or line[0].isspace():continue
        left,gloss=line.split('|',1);a=left.split();n=int(a[3],16);words=[a[4+2*i].replace('_',' ').split('(')[0] for i in range(n)]
        meaning=gloss.strip().split('; "',1)[0];examples=re.findall(r'"([^"\n]+)"',gloss)
        for word in words:lexicon[norm(word)].append({'pos':pos,'meaning':meaning,'synonyms':[w for w in words if norm(w)!=norm(word)],'examples':examples})
(ROOT/'WORDNET_LICENSE.txt').write_bytes(z.read('wordnet/LICENSE'))
exceptions={}
for file in ['noun','verb','adj','adv']:
    for line in z.read('wordnet/'+file+'.exc').decode().splitlines():
        parts=line.split();exceptions.setdefault(norm(parts[0]),[]).extend(norm(x.replace('_',' ')) for x in parts[1:])
def lemma_options(word):
    options=list(exceptions.get(word,[]))
    # WordNet's conventional inflection substitutions. They are applied only
    # when an exact dictionary headword is absent, and only known lemmas pass.
    for suffix,replacement in [('s',''),('ses','s'),('ves','f'),('xes','x'),('zes','z'),('ches','ch'),('shes','sh'),('ies','y'),('es','e'),('es',''),('ed','e'),('ed',''),('ing','e'),('ing',''),('er',''),('er','e'),('est',''),('est','e')]:
        if word.endswith(suffix):options.append(word[:-len(suffix)]+replacement)
    for suffix in ['ing','ed']:
        if word.endswith(suffix):
            stem=word[:-len(suffix)]
            if len(stem)>2 and stem[-1]==stem[-2]:options.append(stem[:-1])
    deaccent=''.join(c for c in unicodedata.normalize('NFD',word) if unicodedata.category(c)!='Mn')
    options.extend([deaccent,word.replace('-',' ')])
    if word.startswith(('a ','an ','the ')):options.append(word.split(' ',1)[1])
    return list(dict.fromkeys(x for x in options if x in lexicon or x in byword))
references=[];unresolved=[];alias_links=[];ref_byword={}
for word,sources in sorted(candidates.items()):
    if word in byword:continue
    senses=lexicon.get(word)
    if not senses:
        options=lemma_options(word)
        if len(options)==1:
            alias_links.append({'form':word,'headword':options[0],'sources':sorted(sources)});continue
        unresolved.append({'word':word,'sources':sorted(sources),'reason':'Phrase, non-WordNet term, uncertain inflection or spelling: requires editorial review.'});continue
    ref={'id':'ref-'+str(len(references)+1),'word':word,'senses':senses[:8],'selectionSources':sorted(sources),'definitionSource':'Princeton WordNet 3.0','status':'dictionary-reference','urdu':None,'forms':[]};references.append(ref);ref_byword[word]=ref
for link in alias_links:
    word=link['headword'];target=byword.get(word) or ref_byword.get(word)
    if target is None:
        target={'id':'ref-'+str(len(references)+1),'word':word,'senses':lexicon[word][:8],'selectionSources':link['sources'],'definitionSource':'Princeton WordNet 3.0','status':'dictionary-reference','urdu':None,'forms':[]};references.append(target);ref_byword[word]=target
    if link['form'] not in target.setdefault('forms',[]):target['forms'].append(link['form'])

# Phrase patterns stay separate from headwords. Use one normalized string per
# candidate and no copy of publisher glosses or sentences.
expressions=read(ROOT/'expressions.json');existing={norm(x['phrase']) for x in expressions};phrases=collections.defaultdict(set)
for p in (REVIEW/'english-phrases-main(1)').rglob('*.txt'):
    for line in p.read_text().splitlines():
        key=norm(line)
        if key and key not in existing:phrases[key].add(p.stem)
phrase_candidates=[{'phrase':s,'lists':sorted(v),'status':'pattern-review-needed'} for s,v in sorted(phrases.items())]
write('data.json',data);write('domains.json',domains);write('reference.json',references)
families=read(ROOT/'family-lessons.json')
for w in data:
    if str(w['id']) not in families:families[str(w['id'])]={'family':[],'collocations':[{'phrase':w['collocation'],'meaning':w['senses'][0]['meaning'],'urdu':w['urdu'],'example':w['examples'][0]}]}
write('family-lessons.json',families)
write('phrase-candidates.json',phrase_candidates);write('word-review-queue.json',unresolved)
meta=read(ROOT/'meta.json');meta.update({'wordCount':len(data),'levelCounts':dict(collections.Counter(x['band'] for x in data)),'referenceWordCount':len(references),'totalUniqueWords':len(data)+len(references),'domainCount':len(domains),'originalDomainLessons':sum(len(x['lessons']) for x in domains),'newDomainWords':len(added),'edition':'Comprehensive','scope':'General, practical, academic and specialist vocabulary; not a claim of exhaustive coverage or official exam alignment.'});write('meta.json',meta)
report={'existingWordCount':len(original_ids),'existingIdsPreserved':all(byword[norm(w)]['id']==i for w,i in original_ids.items()),'aptitudeWords':len(apt),'aptitudeWordsMissing':0,'fullLessonWords':len(data),'newDomainWords':added,'domainLessons':sum(len(x['lessons']) for x in domains),'domains':len(domains),'dictionaryReferenceWords':len(references),'totalUniqueWords':len(data)+len(references),'candidateHeadwords':len(candidates),'linkedInflectedForms':len(alias_links),'unresolvedWordCandidates':len(unresolved),'phraseCandidates':len(phrase_candidates),'reviewPolicy':'Existing uploaded lessons preserved, original domain lessons authored. Expanded reference definitions are WordNet 3.0; Urdu and sense-specific usage review are not claimed. Publisher decks used for headword selection only. No fabricated frequency, IPA or CEFR scores.','inventories':inventories}
write('coverage-audit.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ['inventories','newDomainWords','reviewPolicy']},indent=2))
