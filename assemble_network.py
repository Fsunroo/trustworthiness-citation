from output_paths import output_path
from pathlib import Path
import json,re,csv,collections,hashlib,unicodedata
BASE=Path(__file__).resolve().parent/'output';ROOT=BASE.parents[1]
SEEDS=json.load(open(BASE.parent/'inputs/included_papers.json'))
records=json.load(open(output_path('reference_occurrences.json')))
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).lower())
items=[]
for ident,s in SEEDS.items():
 items.append(dict(item_id=ident,seed_id=ident,title=s['title'],year=s['database_year'],doi=s['doi'].lower(),arxiv=s['arxiv']or'',author=(s['authors'][0].get('family')or ident)if s['authors']else ident,title_basis='included_registry',raw=s['title']))
for r in records:items.append(dict(r,item_id=r['occurrence_id'],seed_id=''))
parent=list(range(len(items)))
def find(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(a,b):
 a=find(a);b=find(b)
 if a!=b:parent[max(a,b)]=min(a,b)
seen={};rules=collections.Counter()
for j,r in enumerate(items):
 keys=[]
 if r['doi']:keys.append('doi:'+r['doi'].strip().rstrip('.,').removeprefix('https://doi.org/'))
 if r['arxiv']:keys.append('arxiv:'+r['arxiv'])
 t=norm(r['title']);y=r['year']
 reliable=r['title_basis']in ['included_registry','reported_crossref_title','crossref_doi_metadata','quoted_title','literal_title_catalog_match','exact_identifier_peer_metadata','parsed_author_year_title','reviewed_literal_title']
 if reliable and y and(len(t)>=30 or t in ['attentionisallyouneed','languagemodelsarefewshotlearners']):keys.append(f'titleyear:{t}:{y}')
 for k in keys:
  if k in seen:union(j,seen[k]);rules[k.split(':')[0]]+=1
  else:seen[k]=j
 # Unidentified references remain their own evidence-based nodes, never merge on empty labels.
groups=collections.defaultdict(list)
for j,r in enumerate(items):groups[find(j)].append(r)
entities=[];itemmap={}
for root,group in sorted(groups.items()):
 seeds=[r['seed_id']for r in group if r['seed_id']];ident=seeds[0]if seeds else 'R'+hashlib.sha256('|'.join(sorted(r['item_id']for r in group)).encode()).hexdigest()[:10]
 priority={'included_registry':9,'reviewed_literal_title':8,'crossref_doi_metadata':7,'reported_crossref_title':6,'literal_title_catalog_match':5,'quoted_title':4,'exact_identifier_peer_metadata':3,'parsed_author_year_title':2,'parsed_citation_title':1,'raw_citation_only':0}
 best=max(group,key=lambda r:(priority.get(r['title_basis'],0),bool(r['title']),len(r['title'])if len(r['title'])<300 else 0))
 ys=[r['year']for r in group if r['year']];year=best['year']or(collections.Counter(ys).most_common(1)[0][0]if ys else None)
 if seeds:year=next(r['year']for r in group if r['seed_id'])
 citations=sorted({r['citing']for r in group if r.get('citing')})
 entity=dict(id=ident,kind='included'if seeds else'cited_reference',seed_ids=seeds,title=best['title']or best['raw'][:200],title_basis=best['title_basis'],author=best['author'],year=year,observed_years=sorted(set(ys)),doi=next((r['doi']for r in group if r['doi']),''),doi_aliases=sorted({r['doi']for r in group if r['doi']}),arxiv_ids=sorted({r['arxiv']for r in group if r['arxiv']}),cited_by=citations,cited_by_count=len(citations),reference_occurrence_count=sum(bool(r.get('citing'))for r in group),occurrence_ids=[r['item_id']for r in group if r.get('citing')])
 entities.append(entity)
 for r in group:itemmap[r['item_id']]=ident
edges={}
for r in records:
 pair=(itemmap[r['citing']],itemmap[r['occurrence_id']])
 if pair[0]==pair[1]:continue
 if pair not in edges:edges[pair]=dict(source=pair[0],target=pair[1],occurrence_ids=[],citing_seed=r['citing'])
 edges[pair]['occurrence_ids'].append(r['occurrence_id'])
entities.sort(key=lambda n:(n['kind']!='included',-n['cited_by_count'],n['year'] or 9999,n['title']))
# Stable short reference labels for readable plotting and tables, ranked by within-set citation count.
refs=[n for n in entities if n['kind']=='cited_reference']
for j,r in enumerate(refs,1):r['short_id']=f'R{j:04}'
for n in entities:
 if n['kind']=='included':n['short_id']=n['seed_ids'][0]
model=dict(nodes=entities,edges=list(edges.values()),seed_ids=list(SEEDS),scope='45 included reports plus their directly cited works; no references-of-references inferred',counts=dict(seed_papers=len(SEEDS),reference_occurrences=len(records),unique_cited_reference_nodes=len(refs),total_nodes=len(entities),direct_edges=len(edges),undated_reference_nodes=sum(n['year']is None for n in refs),dated_reference_nodes=sum(n['year']is not None for n in refs),earliest_reference_year=min(n['year']for n in refs if n['year']),latest_reference_year=max(n['year']for n in refs if n['year']),reference_nodes_2017=sum(n['year']==2017 for n in refs),included_with_outgoing_links=len({e['citing_seed']for e in edges.values()})))
(output_path('expanded_network.json')).write_text(json.dumps(model,ensure_ascii=False,indent=2))
for filename,rows in [('network_nodes.csv',entities),('network_edges.csv',list(edges.values()))]:
 with (output_path(filename)).open('w',newline='',encoding='utf-8-sig')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False)if isinstance(v,list)else v for k,v in r.items()})
print(model['counts'])
for r in refs[:35]:print(r['short_id'],r['cited_by_count'],r['year'],r['title'][:110],r['doi'])
