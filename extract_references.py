from pathlib import Path
import json,re,csv,xml.etree.ElementTree as ET,unicodedata,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent/'output'
SEEDS=json.load(open(ROOT/'outputs/historical_citation_network_2026-10-16/nodes_working.json'))
COVER={r['id']:r for r in json.load(open(ROOT/'outputs/historical_citation_network_2026-10-16/reference_coverage.json'))}
# Explicit reference-section ends established from local text; exclusive numbered source line.
ENDS={'J0036':492,'J0216':956,'J0250':1215,'J0345':1069,'J0450':891,'J0519':1127,'SC0116':692,'SC0376':833}
UNNUMBERED={'J0216':(108,),'J0250':(70.86,306.14),'J0345':(70.86,306.14),'SC0116':(73.68,309)}
ENDPAGE={'J0216':17,'J0250':11,'J0345':12,'SC0116':8}

def flat(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
 s=re.sub(r'(?<=[a-zA-Z])-\s*\n\s*(?=[a-zA-Z])','',s)
 return re.sub(r'\s+',' ',s).strip()
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).lower())

def numbered(ident):
 seed=SEEDS[ident];ls=Path(seed['textpath']).read_text().splitlines();start=COVER[ident]['reference_headings'][0]-1
 end=ENDS.get(ident,len(ls)+1)-1;ls=ls[start:end]
 lines=[]
 for idx,l in enumerate(ls,start+1):
  l=re.sub(r'^L\d+\s*','',l)
  if seed.get('doi') and norm(seed['doi']) in norm(l):continue
  if re.search(r'This article has been accepted|content may change prior|©|but republication|Authorized licensed|Restrictions apply|^=== PDF|^Proc\. of SPIE|^Article in Press|^BMC Medical Informatics|AUTHORet al|CC-BY|is the author/funder|The copyright holder|medRxiv preprint|^\d+$|^\s*$',l):continue
  if re.search(r'Publisher.s Note|Authors and Affiliations|^Acknowledg|^Funding|^Author Contributions',l):break
  lines.append((idx,l))
 if ident=='J0077':
  raw='\n'.join(l for _,l in lines);hits=list(re.finditer(r'(?<!\d)\b(\d{1,3})\.\s+(?=[A-Z])',raw));selected=[];expect=1
  for m in hits:
   if int(m.group(1))==expect:selected.append(m);expect+=1
  out=[]
  for k,m in enumerate(selected):
   txt=raw[m.end():selected[k+1].start()if k+1<len(selected)else len(raw)]
   out.append(dict(ref_number=k+1,raw=flat(txt),source_start_line=32,source_end_line=32))
  return out
 bracket=any(re.match(r'^\[1\]',l)for _,l in lines[:8]);pat=r'^\[(\d+)\]\s*'if bracket else r'^(\d{1,3})\.\s*'
 out=[];current=None
 for idx,l in lines:
  m=re.match(pat,l)
  if m:
   if current:out.append(current)
   current=dict(ref_number=int(m.group(1)),raw=l[m.end():],source_start_line=idx,source_end_line=idx)
  elif current:
   current['raw']+='\n'+l;current['source_end_line']=idx
 if current:out.append(current)
 for r in out:r['raw']=flat(r['raw'])
 return out

def hanging(ident):
 p=OUT/'tmp'/(ident+'_bbox.html');ns={'x':'http://www.w3.org/1999/xhtml'}
 root=ET.fromstring(re.sub('[\x00-\x08\x0b\x0c\x0e-\x1f]','',p.read_text()));starts=[]
 for pno,page in enumerate(root.findall('.//x:page',ns),1):
  if pno>ENDPAGE[ident]:break
  page_lines=[]
  for line in page.findall('.//x:line',ns):
   txt=' '.join(w.text or''for w in line.findall('x:word',ns));x=float(line.attrib['xMin']);y=float(line.attrib['yMin'])
   if page_lines and abs(y-page_lines[-1]['y'])<.9 and x>page_lines[-1]['x']:
    page_lines[-1]['text']+=' '+txt;continue
   page_lines.append(dict(text=txt,x=x,y=y))
  for l in page_lines:
   if any(abs(l['x']-a)<1.2 for a in UNNUMBERED[ident]):starts.append((norm(l['text']),pno,l))
 seed=SEEDS[ident];source=Path(seed['textpath']).read_text().splitlines();lo=COVER[ident]['reference_headings'][0];hi=ENDS[ident]-1
 hits=[]
 for idx in range(lo,hi):
  text=re.sub(r'^L\d+\s*','',source[idx]);t=norm(text)
  if re.search(r'^=== PDF|^Published as|^ICAART |^\d+$',text):continue
  candidates=[(sn,pno,l)for sn,pno,l in starts if t==sn or (min(len(t),len(sn))>=22 and(t.startswith(sn)or sn.startswith(t)))]
  if candidates:
   _,pno,l=max(candidates,key=lambda x:len(x[0]));hits.append((idx,pno,l))
 entries=[]
 for k,(idx,pno,l)in enumerate(hits):
  stop=hits[k+1][0]if k+1<len(hits)else hi
  lines=[re.sub(r'^L\d+\s*','',s)for s in source[idx:stop]]
  lines=[s for s in lines if not re.search(r'^=== PDF|^Published as|^ICAART |^\d+$',s)]
  entries.append(dict(ref_number=k+1,raw=flat('\n'.join(lines)),source_start_line=idx+1,source_end_line=stop,source_pdf_page=pno,source_bbox_x=l['x'],source_bbox_y=l['y']))
 return entries

allrows=[];audit=[]
for ident,seed in SEEDS.items():
 raw=hanging(ident)if ident in UNNUMBERED else numbered(ident)
 for r in raw:r.update(citing=ident,source_text=seed['textpath'],source_kind='pdf_hanging_indent'if ident in UNNUMBERED else'numbered_fulltext')
 allrows.extend(raw)
 nums=[r['ref_number']for r in raw]
 audit.append(dict(citing=ident,extracted_reference_blocks=len(raw),crossref_items=len(seed['refs']),numbers_consecutive=nums==list(range(1,len(nums)+1)),parser='hanging_indent'if ident in UNNUMBERED else'numbered',sample_first=raw[0]['raw'][:100]if raw else'',sample_last=raw[-1]['raw'][:150]if raw else''))
(OUT/'fulltext_reference_blocks.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2))
(OUT/'reference_extraction_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
for a in audit:print(a)
