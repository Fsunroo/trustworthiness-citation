from output_paths import ROOT, output_path
import csv
import json

model = json.loads(output_path('expanded_network.json').read_text())
validation = json.loads(output_path('validation.json').read_text())
cohort = json.loads((ROOT / 'inputs/included_papers.json').read_text())
counts = model['counts']
seeds = set(model['seed_ids'])
nodes = {n['id']: n for n in model['nodes']}
edges = {(e['source'], e['target']) for e in model['edges']}
assert len(cohort) == 44 and 'J0176' not in cohort
assert seeds == set(cohort) == {n['id'] for n in nodes.values() if n['kind'] == 'included'}
assert len(nodes) == len(model['nodes']) == counts['total_nodes']
assert len(edges) == len(model['edges']) == counts['direct_edges']
assert all(a in seeds and b in nodes and a != b for a, b in edges)
assert {a for a, b in edges} == seeds
assert all(count == validation[key] for key, count in counts.items())

for name in ('expected_edges.csv', 'bibliometrix_validated_edges.csv'):
    with output_path(name).open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(edges)
    assert {(r['source'], r['target']) for r in rows} == edges

occurrences = json.loads(output_path('reference_occurrences.json').read_text())
assert len(occurrences) == counts['reference_occurrences']
assert {r['citing'] for r in occurrences} == seeds
assert {r['occurrence_id'] for r in occurrences} == {o for n in nodes.values() for o in n['occurrence_ids']}
print(f"Verified {len(seeds)} reports, {len(nodes):,} nodes, {len(edges):,} links "
      f"matching Bibliometrix edges, and {len(occurrences):,} reference occurrences.")
