from output_paths import output_path
from pathlib import Path
import json,re,csv,collections,hashlib,unicodedata,itertools
from extract_references import SEEDS,OUT,ROOT,flat,norm
BLOCKS=json.load(open(output_path('fulltext_reference_blocks.json')));byseed=collections.defaultdict(list)
for b in BLOCKS:byseed[b['citing']].append(b)
CATALOG=[]
for seed in SEEDS.values():
 for r in seed['refs']:
  if r.get('article-title'):CATALOG.append((norm(r['article-title']),r))

# Included papers are identity anchors too, so their own bibliography entries
# can resolve back to a source node when title and recorded year agree.
for seed in SEEDS.values():
 CATALOG.append((norm(seed['title']),{'article-title':seed['title'],'year':str(seed['database_year']),'author':seed['authors'][0].get('family','')if seed['authors']else''}))

def getids(raw):
 ds=[]
 for m in re.finditer(r'(?i)\b10\.\d{4,9}/[a-z0-9][a-z0-9_.;/():-]+',raw):
  d=m.group(0).rstrip('.,;:')
  while d.endswith(')')and d.count(')')>d.count('('):d=d[:-1]
  ds.append(d.lower())
 ar=re.search(r'(?i)arxiv\s*[:/]?\s*(\d{4})[.]?(\d{4,5})',raw)
 aid=ar.group(1)+'.'+ar.group(2)if ar else''
 for d in ds:
  if '10.48550/arxiv.'in d:aid=d.split('arxiv.')[-1]
 return list(dict.fromkeys(ds)),aid

def rawmeta(raw):
 raw=flat(raw);title='';confidence='raw_citation_only'
 q=re.search(r'[“"‘]{1,2}(.{12,500}?)[”"’]{1,2}',raw)
 if q:title=q.group(1).rstrip(',.');confidence='quoted_title'
 clean=re.sub(r'https?\s*:\s*//\S+|\b10\.\d{4,9}/\S+|arXiv\s*:?\s*\d[\d.]+',' ',raw,flags=re.I)
 clean=re.sub(r'\b\d{1,6}\s*[-–]\s*\d{1,6}\b',' ',clean)
 clean=re.sub(r'(?:pp?\.|pages)\s*\d+',' ',clean)
 years=[y for y in re.findall(r'(?<![\d])((?:18|19|20)\d{2})(?:[ab])?(?![\d])',clean)if 1800<=int(y)<=2027]
 yr=None
 apa=re.search(r'\(((?:18|19|20)\d{2})[ab]?\)',clean)
 ay=re.search(r'(?<![\d.])((?:18|19|20)\d{2})[ab]?\.\s+(?=[A-Z])',clean)
 if apa and 1800<=int(apa.group(1))<=2027:yr=int(apa.group(1))
 elif ay and 1800<=int(ay.group(1))<=2027:yr=int(ay.group(1))
 elif years:yr=int(years[-1])
 if not title:
  n=norm(raw)
  matches=[(len(t),r)for t,r in CATALOG if len(t)>30 and t in n]
  if matches:
   _,r=max(matches,key=lambda x:x[0]);title=r['article-title'];confidence='literal_title_catalog_match'
   if r.get('year')and str(r['year']).isdigit():yr=int(r['year'])
 if not title:
  m=re.search(r'\b(?:18|19|20)\d{2}[ab]?\)?[.]?\s+(.+)',raw)
  # Author-year bibliographies put a full stop after the year.
  if m and(apa or ay):
   tail=m.group(1);title=re.split(r'\.\s+(?=[A-Z])|\.\s*(?:arXiv|In )',tail)[0].strip();confidence='parsed_author_year_title'
  else:
   m=re.search(r'(?:et al\.|[A-Za-z][A-Za-z-]+ [A-Z]{1,4}\.)\s+(.+)',raw)
   if m:title=re.split(r'\.\s*(?=[A-Z])',m.group(1))[0];confidence='parsed_citation_title'
 if len(title)<10 or len(title)>400:title='';confidence='raw_citation_only'
 author=re.split(r',|\.',raw)[0].strip()
 return dict(title=title,year=yr,author=author,title_basis=confidence)

records=[];audit=[]
for ident,seed in SEEDS.items():
 blocks=byseed[ident];refs=seed['refs'];used=set();source='cached_crossref'if refs else'fulltext'
 for k,r in enumerate(refs if refs else blocks):
  raw=r.get('unstructured','')if refs else r['raw'];block=None
  doi=str(r.get('DOI','')).lower().strip().translate(str.maketrans('‐‑‒–—−','------'))if refs else'';title=r.get('article-title','')if refs else''
  if refs:
   hits=[]
   for bi,b in enumerate(blocks):
    bn=norm(b['raw'])
    if doi and norm(doi)in bn:hits.append((3,bi,b))
    elif title and len(norm(title))>25 and norm(title)in bn:hits.append((2,bi,b))
   if hits:
    _,bi,block=max(hits,key=lambda x:x[0]);used.add(bi)
   if block:raw=block['raw']
  else:block=r
  meta=rawmeta(raw)
  if title:meta['title']=title;meta['title_basis']='reported_crossref_title'
  if str(r.get('year','')).isdigit():meta['year']=int(r['year'])
  if r.get('author'):meta['author']=str(r['author'])
  ds,aid=getids(raw)
  if doi:ds=[doi]
  else:ds=[d for d in ds if norm(d)!=norm(seed.get('doi',''))]
  rid=f'{ident}_R{k+1:03}'
  rec=dict(occurrence_id=rid,citing=ident,reference_number=k+1,source_kind=source,source_path=seed['crossref_path']if refs else seed['textpath'],source_text=seed['textpath'],raw=raw,reported_crossref=r if refs else None,doi=ds[0]if ds else'',arxiv=aid,**meta)
  if block:
   for field in ['source_start_line','source_end_line','source_pdf_page']:rec[field]=block.get(field)
  records.append(rec)
 # A local reference version may have extra entries; retain only evidence with unambiguous numbering and identifier/title.
 extras=[]
 if refs and len(blocks)>len(refs)and [b['ref_number']for b in blocks]==list(range(1,len(blocks)+1)):
  for bi,b in enumerate(blocks):
   if bi<len(refs)or bi in used:continue
   meta=rawmeta(b['raw']);ds,aid=getids(b['raw']);rid=f'{ident}_R{bi+1:03}'
   records.append(dict(occurrence_id=rid,citing=ident,reference_number=bi+1,source_kind='fulltext_additional_reference',source_path=seed['textpath'],source_text=seed['textpath'],raw=b['raw'],reported_crossref=None,doi=ds[0]if ds else'',arxiv=aid,**meta,source_start_line=b.get('source_start_line'),source_end_line=b.get('source_end_line')));extras.append(bi+1)
 audit.append(dict(article_id=ident,crossref_reference_items=len(refs),fulltext_blocks=len(blocks),analysis_reference_items=len(refs)if refs else len(blocks),extra_fulltext_reference_numbers=extras,source=source))
# Enrich from already downloaded primary DOI metadata, if present.
enrich=output_path('doi_metadata');enrich.mkdir(exist_ok=True)
for r in records:
 if not r['doi']:continue
 file=enrich/(hashlib.sha256(r['doi'].encode()).hexdigest()+'.json')
 if file.exists():
  obj=json.load(open(file));m=obj.get('message',obj)
  if m.get('title'):r['title']=m['title'][0];r['title_basis']='crossref_doi_metadata'
  dates=m.get('published',{}).get('date-parts',[[]])[0]
  if dates:r['year']=int(dates[0]);r['year_basis']='crossref_doi_metadata'
  if m.get('author'):r['author']=m['author'][0].get('family')or m['author'][0].get('name','')
# Propagate structured title/year among EXACT identifiers; never infer a year from a DOI string.
byid=collections.defaultdict(list)
for r in records:
 for key in [r['doi'],('arxiv:'+r['arxiv'])if r['arxiv']else'']:
  if key:byid[key].append(r)
for group in byid.values():
 good=[r for r in group if r['title']and r['title_basis']in ['reported_crossref_title','crossref_doi_metadata','quoted_title','literal_title_catalog_match']]
 best=max(good,key=lambda r:(r['title_basis']=='crossref_doi_metadata',r['title_basis']=='reported_crossref_title',len(r['title'])),default=None)
 years=[r['year']for r in group if r['year']]
 for r in group:
  if best and not r['title']:r['title']=best['title'];r['title_basis']='exact_identifier_peer_metadata'
  if years and not r['year']:r['year']=collections.Counter(years).most_common(1)[0][0];r['year_basis']='exact_identifier_peer_metadata'
  if best and not r['author']:r['author']=best['author']
# Reviewed short-title aliases: bibliographic wording variants, not new citations.
for r in records:
 raw_norm=norm(r['raw'])
 if 'attentionisallyouneed' in raw_norm and ('vaswani' in raw_norm or 'shazeer' in raw_norm):
  r['title']='Attention is all you need';r['title_basis']='reviewed_literal_title';r['year']=2017
 if r['doi']=='10.1145/3097983.3098126' or 'gramgraphbasedattentionmodelforhealthcarerepresentationlearning' in raw_norm:
  r['title']='GRAM: Graph-based attention model for healthcare representation learning';r['title_basis']='reviewed_literal_title';r['year']=2017
(output_path('reference_occurrences.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2))
(output_path('source_coverage.json')).write_text(json.dumps(audit,indent=2))
# Primary metadata requests needed for DOI-only or unparsed titles/years.
need=collections.Counter(r['doi']for r in records if r['doi']and(not r['title']or not r['year']or r['title_basis']in ['parsed_citation_title','raw_citation_only']))
(output_path('doi_metadata_requests.json')).write_text(json.dumps(need,indent=2))
print('Reference occurrences',len(records),'seeds',len(audit),'missing title',sum(not r['title']for r in records),'missing year',sum(not r['year']for r in records),'DOI metadata requests',len(need))
