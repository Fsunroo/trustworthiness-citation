from output_paths import output_path
from pathlib import Path
import json,hashlib,urllib.request,urllib.parse,concurrent.futures,time
BASE=Path(__file__).resolve().parent/'output'
requests=json.load(open(output_path('doi_metadata_requests.json')));cache=output_path('doi_metadata');cache.mkdir(exist_ok=True)
def fetch(doi):
 p=cache/(hashlib.sha256(doi.encode()).hexdigest()+'.json')
 if p.exists():return doi,'cached'
 for attempt in range(2):
  try:
   url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
   req=urllib.request.Request(url,headers={'User-Agent':'ScopingReviewReferenceNetwork/1.0 (academic bibliography analysis)'})
   with urllib.request.urlopen(req,timeout=30)as response:body=response.read()
   r=json.loads(body);assert r.get('status')=='ok'and r.get('message',{}).get('DOI')
   p.write_bytes(body);return doi,'ok'
  except Exception as e:
   if attempt==1:return doi,str(e)
   time.sleep(1)
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for count,(doi,status)in enumerate(pool.map(fetch,requests),1):
  results.append({'doi':doi,'status':status})
  if count%25==0:print(count,'/',len(requests),'requests completed',flush=True)
(output_path('doi_metadata_fetch_log.json')).write_text(json.dumps(results,indent=2))
print('Completed',len(results),'requests;',sum(r['status']in ['ok','cached']for r in results),'available metadata records.',flush=True)
