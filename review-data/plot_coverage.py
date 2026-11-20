"""Reproduce scientific coverage figures from accepted CSV matrices (no pooled performance)."""
import argparse
import csv
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output_dir', type=Path, help='Directory for generated figures and source CSVs')
S = Path(__file__).resolve().parent
F = parser.parse_args().output_dir
F.mkdir(parents=True, exist_ok=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
C=['Y','N','NR','U','UA','NA'];colors=['#366b8c','#b87b63','#d6d9dc','#9f95b6','#d2b575','#f1f1f1'];labels=['Y: documented','N: explicit absence','NR: not reported','U: unclear / conflicting','UA: unavailable / unassessed','NA: not applicable']
def read(n):return list(csv.DictReader((S/n).open()))
def save(fig,n):
 for ext in ['png','svg','pdf']:fig.savefig(F/f'{n}.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
 plt.close(fig)
def csvsave(n,rows):
 with (F/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=read('article_coverage.csv');csvsave('figure_2_source.csv',rows)
fig,axs=plt.subplots(1,2,figsize=(17,10.7),sharex=True)
for ax,rs in zip(axs,[rows[:15],rows[15:]]):
 y=np.arange(len(rs));left=np.zeros(len(rs))
 for c,col in zip(C,colors):
  vals=np.array([int(r[c]) for r in rs]);ax.barh(y,vals,left=left,color=col,edgecolor='white',height=.78,label=c);left+=vals
 ax.set_yticks(y,[r['indicator'].replace('_',' ') for r in rs]);ax.invert_yaxis();ax.set_xlim(0,53);ax.set_xticks([0,10,20,30,40,44]);ax.set_xlabel('Number of articles (fixed corpus n = 44)');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
 for i,r in enumerate(rs):
  d=r['denominator_min'] if r['denominator_min']==r['denominator_max'] else r['denominator_min']+'–'+r['denominator_max'];ax.text(44.5,i,f"{r['Y']}/{d}",va='center',fontsize=9)
 ax.text(44.5,-1,'Y/applicable',fontsize=9,fontweight='bold')
fig.suptitle('Documented assessment and reporting coverage by indicator',fontsize=16,y=.99)
fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.035))
fig.text(.04,.005,'Article status uses at least one applicable LLM evaluation. Y is reported coverage, not methodological verification.\nNA excluded from denominators; unclear applicability yields a range. Bars retain every status; denominators differ across indicators.',fontsize=10)
fig.tight_layout(rect=[0,.12,1,.95]);save(fig,'figure_2_indicator_coverage')
m=read('article_indicator_matrix.csv');csvsave('table_s4_source.csv',m);ids=sorted({r['article_id'] for r in m});inds=[r['indicator'] for r in rows];lookup={(r['article_id'],r['indicator']):r['code'] for r in m}
for part in range(3):
 ix=inds[part*10:(part+1)*10];fig,ax=plt.subplots(figsize=(12,15.8));arr=np.array([[C.index(lookup[(a,i)]) for i in ix] for a in ids]);ax.imshow(arr,cmap=ListedColormap(colors),vmin=-.5,vmax=5.5,aspect='auto');ax.set_xticks(range(10),[i.replace('_','\n') for i in ix],fontsize=10);ax.xaxis.tick_top();ax.set_yticks(range(len(ids)),ids,fontsize=10)
 for y in range(len(ids)):
  for x in range(10):ax.text(x,y,C[arr[y,x]],ha='center',va='center',fontsize=8,color='white' if arr[y,x]==0 else '#252525')
 ax.set_xticks(np.arange(-.5,10,1),minor=True);ax.set_yticks(np.arange(-.5,len(ids),1),minor=True);ax.grid(which='minor',color='white',linewidth=.7);ax.tick_params(which='minor',length=0);ax.set_title(f'Article-by-indicator evidence states: panel {part+1}/3',pad=65,fontsize=16)
 fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],loc='lower center',ncol=2,frameon=False,bbox_to_anchor=(.5,.025));fig.text(.08,.006,'At least one applicable LLM evaluation per article; all six codes shown. No ranking or total score.\nU may include unclear applicability; see article matrix and coverage denominators.',fontsize=10);fig.subplots_adjust(left=.12,right=.99,bottom=.115,top=.87);save(fig,f'figure2_evidence_heatmap_{part+1}')
tr=[r for r in read('task_family_coverage.csv') if r['level']=='article'];choose=['auroc','calibration','clinical_factuality','clinical_omissions','human_evaluation','robustness'];task=sorted({r['task_family'] for r in tr});dat=[r for r in tr if r['indicator'] in choose];csvsave('figure_3_source.csv',dat);lookup={(r['task_family'],r['indicator']):r for r in dat};fig,axs=plt.subplots(2,3,figsize=(16,8.5))
for ax,ind in zip(axs.flat,choose):
 rs=[lookup[(t,ind)] for t in task];y=np.arange(len(task));left=np.zeros(len(task))
 for c,col in zip(C,colors):
  v=np.array([int(r[c]) for r in rs]);ax.barh(y,v,left=left,color=col,edgecolor='white');left+=v
 ax.set_yticks(y,[t.replace('_',' ') for t in task],fontsize=9);ax.invert_yaxis();ax.set_xlim(0,31);ax.set_xticks([0,10,20]);ax.set_title(ind.replace('_',' '));ax.set_xlabel('Articles within task family');ax.set_axisbelow(True);ax.grid(axis='x',alpha=.15)
 for i,r in enumerate(rs):
  d=r['denominator_min'] if r['denominator_min']==r['denominator_max'] else r['denominator_min']+'–'+r['denominator_max'];ax.text(sum(int(r[c]) for c in C)+.4,i,("NA" if r["denominator_max"]=="0" else f"{r['Y']}/{d}"),va='center',fontsize=8)
fig.suptitle('Task-specific article coverage: selected complementary assessments',fontsize=15);fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.04));fig.text(.025,.005,'Labels show Y/applicable denominator (range if uncertain). Families overlap across articles.\nAt-least-one-evaluation counting within each family; no cross-family performance comparison or pooled percentage.',fontsize=10);fig.tight_layout(rect=[0,.13,1,.95]);save(fig,'figure_3_task_coverage')
print('Saved five figure panels, three formats each, with source CSVs.')
