from output_paths import output_path
from pathlib import Path
import json,collections,textwrap,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
BASE=Path(__file__).resolve().parent/'output'
m=json.load(open(output_path('expanded_network.json')));allnodes={n['id']:n for n in m['nodes']}
refs=[n for n in m['nodes']if n['kind']=='cited_reference'][:25]
selected=[n for n in m['nodes']if n['kind']=='included']+refs
chosen={n['id']for n in selected};edges=[e for e in m['edges']if e['source']in chosen and e['target']in chosen]
byyear=collections.defaultdict(list)
for n in selected:byyear[n['year']].append(n)
positions={}
for yr,group in byyear.items():
 group.sort(key=lambda n:(n['kind']=='included',n['short_id']))
 for j,n in enumerate(group):positions[n['id']]=(yr,.07+.86*(j+.5)/len(group))
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42})
fig=plt.figure(figsize=(25,18),facecolor='white')
ax=fig.add_axes([.035,.12,.645,.77]);key=fig.add_axes([.705,.12,.275,.77]);key.set_xlim(0,1);key.set_ylim(0,1);key.axis('off')
fig.text(.035,.965,'Historical citation network: included papers and their references',fontsize=25,weight='bold',color='#193342')
fig.text(.035,.936,f"Focus view: all 45 included papers + the 25 most frequently cited external references | {len(edges)} direct links shown",fontsize=15,color='#526876')
fig.text(.035,.913,f"Complete reconstructed network: {m['counts']['total_nodes']:,} nodes and {m['counts']['direct_edges']:,} links; cited-reference years {m['counts']['earliest_reference_year']}–{m['counts']['latest_reference_year']}",fontsize=12,color='#526876')
for yr in range(min(byyear),max(byyear)+1):ax.axvline(yr,color='#e5eaee',lw=.8,zorder=0)
# Uniform node spacing within a year preserves the chronology without implying a vertical metric.
for e in edges:
 p=positions[e['source']];q=positions[e['target']]
 if p==q:continue
 focal=allnodes[e['target']]['short_id']=='R0006'
 color='#b57b28'if focal else'#6d8596';alpha=.65 if focal else .18
 curve=.09 if p[0]==q[0]else 0
 ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=7,connectionstyle=f'arc3,rad={curve}',lw=.75 if focal else .45,color=color,alpha=alpha,shrinkA=4,shrinkB=7,zorder=1))
for n in selected:
 x,y=positions[n['id']];isref=n['kind']=='cited_reference';color='#b57b28'if isref else'#326f99'
 size=30+7*n['cited_by_count']if isref else 28
 ax.scatter([x],[y],s=size,marker='o'if isref else'D',c=color,edgecolors='white',lw=.7,zorder=3)
 label=n['short_id']
 ax.annotate(label,(x,y),xytext=(7,0),textcoords='offset points',fontsize=8.4,va='center',color='#80571d'if isref else'#214e6d',bbox=dict(facecolor='white',edgecolor='none',alpha=.83,pad=.7),zorder=4,annotation_clip=False)
ax.set_xlim(min(byyear)-.45,max(byyear)+.8);ax.set_ylim(0,1)
ax.set_xticks(list(range(min(byyear),max(byyear)+1)));ax.tick_params(axis='x',labelsize=12,length=0,pad=12);ax.set_yticks([])
for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#c9d3db');ax.set_xlabel('Publication year recorded for each node',fontsize=12,labelpad=16,color='#526876')
key.text(0,1.025,'CITED REFERENCE KEY',fontsize=12,weight='bold',color='#193342')
for j,n in enumerate(refs):
 y=1-j*.0396
 key.text(0,y,f"{n['short_id']}   {n['year']}   ·   cited by {n['cited_by_count']}/45 papers",fontsize=9.3,weight='bold',color='#80571d',va='top')
 title=n['title'];lines=textwrap.wrap(title,width=69)
 if len(lines)>2:lines=lines[:2];lines[-1]=lines[-1][:65]+'…'
 key.text(0,y-.012,'\n'.join(lines),fontsize=9,linespacing=1.13,color='#304b5c',va='top')
fig.text(.035,.063,'Blue diamonds: included papers (review IDs). Gold circles: cited references; circle area increases with the number of included papers citing the work.',fontsize=11,color='#415b6b')
fig.text(.035,.044,'Arrows run from citing paper to cited work. Gold links highlight the 2017 reference “Attention is all you need”. Vertical placement is for readability.',fontsize=11,color='#415b6b')
fig.text(.035,.025,'The complete network and reference evidence are supplied separately. No citation links among external references were inferred. Five source-paper year conflicts and undated references remain in the audit.',fontsize=10,color='#617785')
for ext in ['png','svg','pdf']:fig.savefig(output_path('expanded_reference_historiograph.'+ext),dpi=220,facecolor='white')
plt.close(fig)
(output_path('focus_view.json')).write_text(json.dumps(dict(node_ids=sorted(chosen),reference_ids=[n['id']for n in refs],edge_count=len(edges),year_counts={y:len(g)for y,g in byyear.items()}),indent=2))
print('Focus figure:',len(selected),'nodes;',len(edges),'links. PNG, SVG and PDF saved.')
