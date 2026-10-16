from pathlib import Path
import json,csv,sqlite3,hashlib,urllib.parse,xml.etree.ElementTree as ET,collections
BASE=Path(__file__).resolve().parent/'output';ROOT=BASE.parents[1]
m=json.load(open(BASE/'expanded_network.json'));ns={n['id']:n for n in m['nodes']};out=collections.defaultdict(list)
for e in m['edges']:out[e['source']].append(e['target'])
def sr(n):return n['id'].upper()+', '+str(n['year']or'0000')+', REFERENCE'
with (BASE/'bibliometrix_expanded.csv').open('w',newline='',encoding='utf-8')as f:
 w=csv.DictWriter(f,fieldnames=['ARTICLE_ID','AU','TI','SO','PY','DI','SR','SR_FULL','DB','DE','ID','TC','CR']);w.writeheader()
 for n in m['nodes']:
  refs=[]
  for target in sorted(set(out[n['id']])):
   t=ns[target];ref=sr(t)
   if t['doi']:ref+=', DOI '+t['doi'].upper()
   refs.append(ref)
  w.writerow(dict(ARTICLE_ID=n['id'],AU=n['author']or'UNRECORDED',TI=n['title'],SO='',PY=n['year']or'',DI=n['doi'],SR=sr(n),SR_FULL=sr(n),DB='WOS',DE='',ID='',TC=0,CR=';'.join(refs)))
with (BASE/'expected_edges.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['source','target']);w.writerows((e['source'],e['target'])for e in m['edges'])
occmap={oid:n for n in m['nodes']for oid in n['occurrence_ids']};rs=json.load(open(BASE/'reference_occurrences.json'))
fields=['citing_paper','reference_number','occurrence_id','reference_node_id','reference_label','title','year','doi','arxiv','metadata_title_basis','source_kind','source_path','source_text','source_start_line','source_end_line','source_pdf_page','citation_text']
with (BASE/'reference_evidence.csv').open('w',newline='',encoding='utf-8-sig')as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rs:
  n=occmap[r['occurrence_id']]
  w.writerow(dict(citing_paper=r['citing'],reference_number=r['reference_number'],occurrence_id=r['occurrence_id'],reference_node_id=n['id'],reference_label=n['short_id'],title=r['title']or r['raw'][:200],year=r['year'],doi=r['doi'],arxiv=r['arxiv'],metadata_title_basis=r['title_basis'],source_kind=r['source_kind'],source_path=r['source_path'],source_text=r['source_text'],source_start_line=r.get('source_start_line'),source_end_line=r.get('source_end_line'),source_pdf_page=r.get('source_pdf_page'),citation_text=r['raw']))
# A portable graph export usable in Gephi or Cytoscape; edge orientation is citing -> cited.
uri='http://graphml.graphdrawing.org/xmlns';ET.register_namespace('',uri)
root=ET.Element('{'+uri+'}graphml')
for key,kind in [('label','node'),('title','node'),('year','node'),('kind','node'),('doi','node'),('cited_by_count','node')]:ET.SubElement(root,'{'+uri+'}key',{'id':key,'for':kind,'attr.name':key,'attr.type':'string'})
g=ET.SubElement(root,'{'+uri+'}graph',{'id':'expanded_reference_network','edgedefault':'directed'})
for n in m['nodes']:
 el=ET.SubElement(g,'{'+uri+'}node',{'id':n['id']})
 for k in ['title','year','kind','doi','cited_by_count']:
  d=ET.SubElement(el,'{'+uri+'}data',{'key':k});d.text=str(n.get(k)or'')
 ET.SubElement(el,'{'+uri+'}data',{'key':'label'}).text=n['short_id']
for j,e in enumerate(m['edges']):ET.SubElement(g,'{'+uri+'}edge',{'id':str(j),'source':e['source'],'target':e['target']})
ET.ElementTree(root).write(BASE/'expanded_reference_network.graphml',encoding='utf-8',xml_declaration=True)
sql='''SELECT id FROM articles WHERE json_extract(payload,'$.data."Eligibility decision"')='Include' AND COALESCE(json_extract(payload,'$.secondaryReviewStatus'),'')!='Pending' ORDER BY id'''
c=sqlite3.connect('file:'+str(ROOT/'outputs/review_dashboard/review.sqlite3')+'?mode=ro',uri=True);current={x[0]for x in c.execute(sql)}
assert current==set(m['seed_ids'])and len(current)==45
assert len(rs)==len(occmap)==2244
assert all(e['source']in ns and e['target']in ns and ns[e['source']]['kind']=='included'for e in m['edges'])
assert len({(e['source'],e['target'])for e in m['edges']})==len(m['edges'])
assert all(e['source']!=e['target']for e in m['edges'])
assert {e['citing_seed']for e in m['edges']}==current
future=[dict(source=e['source'],target=e['target'],source_year=ns[e['source']]['year'],target_year=ns[e['target']]['year'])for e in m['edges']if ns[e['source']]['year']and ns[e['target']]['year']and ns[e['target']]['year']>ns[e['source']]['year']]
(BASE/'chronology_flags.json').write_text(json.dumps(future,indent=2))
validation=dict(m['counts'],live_db_cohort_matches=True,all_reference_occurrences_mapped=True,all_45_papers_have_reference_links=True,duplicate_edges=0,self_loops=0,chronology_flags=len(future),doi_metadata_files=len(list((BASE/'doi_metadata').glob('*.json'))),database_modified=False)
(BASE/'validation.json').write_text(json.dumps(validation,indent=2))
print('Exports prepared and source cohort verified.',validation)
