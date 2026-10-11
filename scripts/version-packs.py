"""Content-address optional collections. Existing source JSON remains editable."""
import hashlib,json,re
from pathlib import Path
mapping={'collection':['data.json','sources.json','usage.json'],'dictionary':['reference.json'],'classification':['taxonomy.json'],'expressions':['expressions.json'],'families':['family-lessons.json']}
Path('packs').mkdir(exist_ok=True)
for name,files in mapping.items():
 for i,f in enumerate(files):
  raw=Path(f).read_bytes();dest='packs/'+Path(f).stem+'-'+hashlib.sha256(raw).hexdigest()[:12]+'.json';Path(dest).write_bytes(raw);files[i]=dest
p=Path('modules/packs.js');s=p.read_text();s=re.sub(r'const files=\{.*?\};','const files='+json.dumps(mapping,separators=(',',':'))+';',s);p.write_text(s)
Path('reports/pack-manifest.json').write_text(json.dumps(mapping,indent=2))

keep={f for files in mapping.values() for f in files}
for p in Path('packs').glob('*.json'):
 if str(p) not in keep:p.unlink()
