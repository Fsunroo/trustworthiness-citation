"""Shared artifact locations for the analysis scripts."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
ARTIFACT_FOLDERS = {'R_sessionInfo.txt': 'bibliometrix',
 'bibliometrix_expanded.csv': 'bibliometrix',
 'bibliometrix_expanded_focus_histPlot.rds': 'bibliometrix',
 'bibliometrix_expanded_histResults.rds': 'bibliometrix',
 'bibliometrix_histData.csv': 'bibliometrix',
 'bibliometrix_native_focus.png': 'bibliometrix',
 'bibliometrix_run_log.txt': 'audit',
 'bibliometrix_validated_edges.csv': 'bibliometrix',
 'chronology_flags.json': 'audit',
 'data_build_log.txt': 'audit',
 'doi_metadata': 'metadata',
 'doi_metadata_fetch_log.json': 'metadata',
 'doi_metadata_requests.json': 'metadata',
 'expanded_network.json': 'network',
 'expanded_reference_historiograph.pdf': 'figures',
 'expanded_reference_historiograph.png': 'figures',
 'expanded_reference_historiograph.svg': 'figures',
 'expanded_reference_network.graphml': 'network',
 'expected_edges.csv': 'bibliometrix',
 'extraction_log.txt': 'audit',
 'focus_view.json': 'network',
 'fulltext_reference_blocks.json': 'evidence',
 'network_build_log.txt': 'audit',
 'network_edges.csv': 'network',
 'network_nodes.csv': 'network',
 'reference_evidence.csv': 'evidence',
 'reference_extraction_audit.json': 'evidence',
 'reference_network_explorer.html': 'explorer',
 'reference_occurrences.json': 'evidence',
 'source_coverage.json': 'evidence',
 'top_reference_metadata_requests.json': 'metadata',
 'validation.json': 'audit'}

def output_path(name):
    name = str(name)
    if name not in ARTIFACT_FOLDERS:
        raise KeyError(f"Unregistered output artifact: {name}")
    path = OUTPUT / ARTIFACT_FOLDERS[name] / name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
