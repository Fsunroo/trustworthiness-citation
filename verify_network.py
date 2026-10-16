from output_paths import output_path
from pathlib import Path
import json, csv
base = Path(__file__).resolve().parent / "output"
model = json.loads((output_path('expanded_network.json')).read_text())
nodes = {n["id"]: n for n in model["nodes"]}
edges = {(e["source"], e["target"]) for e in model["edges"]}
assert len(nodes) == 1924 and len(edges) == len(model["edges"]) == 2237
assert len(model["seed_ids"]) == 45
assert all(a in nodes and b in nodes and a != b for a, b in edges)
assert {a for a, b in edges} == set(model["seed_ids"])
with (output_path('bibliometrix_validated_edges.csv')).open() as f:
    native = list(csv.DictReader(f))
assert len(native) == 2237
assert {(r["source"], r["target"]) for r in native} == edges
occurrences = json.loads((output_path('reference_occurrences.json')).read_text())
assert len(occurrences) == 2244
assert {r["occurrence_id"] for r in occurrences} == {o for n in nodes.values() for o in n["occurrence_ids"]}
print("Verified: 45 included papers, 1,924 nodes, 2,237 native-validated links, 2,244 reference occurrences.")
