# Trustworthiness and Reproducibility of Generative Large Language Models Using Public Critical Care EHR Data

## Supporting citation-network analysis

This repository contains the historical direct-citation analysis, figures, interactive explorer, and citation evidence supporting the manuscript **“Trustworthiness and Reproducibility of Generative Large Language Models Using Public Critical Care EHR Data.”**

**Manuscript status:** In preparation for journal submission.

**Manuscript DOI:** Not assigned.

The analysis starts from the 44 papers included in the review and expands the network to the works cited in their reference lists, including earlier foundational publications outside the inclusion set. The repository provides the materials needed to inspect and reproduce this citation-network analysis. It does not contain patient-level EHR data.

## Start here

- [Interactive reference-network explorer](output/explorer/reference_network_explorer.html): download and open locally to search included papers and cited references.
- [Main figure (PDF)](output/figures/expanded_reference_historiograph.pdf) · [PNG](output/figures/expanded_reference_historiograph.png) · [Editable SVG](output/figures/expanded_reference_historiograph.svg).
- [Citation evidence](output/evidence/reference_evidence.csv): recovered citation strings, identifiers, source locations, and graph-node mappings.
- [Output index](output/README.md): guide to all generated files.

## Manuscript and citation information

The manuscript has no DOI at this stage. The DOIs in the network and evidence tables identify the cited publications, not this manuscript. Publication details and the manuscript DOI can be added here when available.

When referring to this repository before publication, identify the manuscript by its full title and include the repository URL and the commit used for the analysis. The repository contains supporting materials for this specific analysis; it is not a complete reproducibility package for every component of the review.

## Main outputs

All generated artifacts are organized under `output/`; scripts, source inputs and vendored libraries remain at the repository root. See [the output index](output/README.md) for the folder layout and direct links.

- `output/explorer/reference_network_explorer.html`: self-contained interactive explorer. Search an included paper ID to inspect its bibliography; search a reference title to inspect the included papers citing it. Select **All references**, then **Overview**, to display the complete graph. Search or zoom to read a neighborhood. No external scripts or data service is needed to open this HTML.
- `output/figures/expanded_reference_historiograph.png`, `.svg`, `.pdf`: readable focus figure containing all 44 included papers and the 25 external reference nodes with the largest numbers of distinct citing included papers. This view contains 69 nodes and 197 direct links. The SVG is editable.
- `output/network/expanded_reference_network.graphml`: the complete directed graph, for Gephi/Cytoscape.
- `output/network/network_nodes.csv`, `output/network/network_edges.csv`: complete graph, including all long-tail and undated references.
- `output/evidence/reference_evidence.csv` / `output/evidence/reference_occurrences.json`: all 2,217 recovered reference entries, original citation strings, source locations, identifiers and their mapping to graph nodes.
- `output/bibliometrix/bibliometrix_expanded.csv`: prepared input for the final 44-report cohort. The edge table from the prior 44-report Bibliometrix run is included for comparison.

## Scope and results

The final manuscript cohort excludes **Foresight (J0176)**, which developed and pretrained a bespoke EHR foundation model from scratch. The eligibility amendment was made during manuscript revision. Studies that prompt or adapt existing generative LLMs remain eligible. The upstream screening database retains the original 45 records. The reproduction input is the frozen manuscript cohort in `inputs/included_papers.json`, with the exclusion reflected in `inputs/source.query.sql`.

There are **2,217 recovered reference entries**, represented by **1,858 external cited-reference nodes** plus the 44 included-paper nodes: **1,902 nodes and 2,210 distinct directed links** in total. All 44 included papers have outgoing reference links. Multiple references from one paper to the same resolved node count as one link; all original entries remain in the evidence ledger.

Known reference years span **1947–2026**. Thirty-four external reference nodes have no reliable year and remain in an undated lane in the explorer; they are retained in the graph and evidence tables. These are reconstructed reference identities, not an assertion that every bibliographic version has been resolved to a unique underlying study. Different versions can remain separate.

For example, the explicit 2017 citation **Attention is all you need** is cited by eight distinct included papers: J0015, J0042, J0045, J0060, J0093, J0102, J0216 and J0345. **GRAM: Graph-based attention model for healthcare representation learning** is another shared 2017 reference and is cited by nine included papers. These counts are within this review's reference lists, not global citations.

The graph covers direct references made **by the 44 source papers**. The reference lists of the external works were not recursively retrieved, so citation links among those external works are not inferred. An external node's absence of outgoing links means those reference lists were not collected; it does not mean the work cites nothing. Source-paper citation links to other included papers are retained where identifiers or title/year evidence resolve the reference back to an included node.

## Source extraction

- For 29 source papers, nonempty cached Crossref cited-reference lists supply 1,398 reference entries.
- For 15 papers without such lists, reference blocks were recovered from local full texts: 817 entries. Numbered lists were segmented by reference number and checked for consecutive numbering. The four unnumbered lists were segmented using PDF hanging-indent coordinates and bounded reference sections; first/last entries and starts were inspected.
- Two additional numbered entries present in local report versions beyond the cached reference-list lengths were retained, with explicit `fulltext_additional_reference` provenance. They are J0206 reference 54 and SC0376 reference 57. Thus the analysis reflects the available reference evidence, including labeled local-version additions.
- Local text helped recover metadata for cached references only through an identifier or literal-title match. Equal list length or reference ordinal was not accepted by itself as evidence of identity.
- Running headers, page footers, author-biography sections and appendices were excluded from reference blocks. The citing paper's own DOI in a repeated page header was not treated as a cited reference. Original citation text and source line ranges remain inspectable.
- Missing DOI metadata were retrieved from public Crossref records. Cached responses are under `output/metadata/doi_metadata/`; no reference lists of those external works were added as new edges.

`output/evidence/source_coverage.json` records source type and reference counts per paper. Raw full-text segmentation for the 29 cached-list papers is an alignment aid, not a replacement for their cited-reference metadata; some PDFs have extraction/order differences.

## Identity and date handling

Records were matched by exact normalized DOI, exact arXiv ID, or an eligible exact normalized title plus year. Short, distinctive title variants for *Attention is all you need* and GRAM were explicitly reviewed against citation text. Generic names or empty titles were not merged. Punctuation and hyphen variants were normalized, and every occurrence retains its original citation string and identifiers. Explicit arXiv identifiers can connect a preprint reference to an included work whose record carries that identifier.

DOI metadata are preferred for identifying a work when available. Otherwise titles/years may come from structured reference metadata, literal title matches, quoted titles or parsed citation text. When a clean title is unavailable the reference string is retained as the node label. `title_basis` and `metadata_title_basis` distinguish these cases; raw citation strings are not presented as independently verified article titles. Multiple reported years are retained in `observed_years`. Ambiguous versions and formatting errors may leave duplicates or missed matches in the long tail. This is a single-reviewer reconstruction, not an independently double-reviewed bibliography.

Report years follow the manuscript supplement (4 in 2024, 13 in 2025 and 27 in 2026), including CURENet (J0093) in 2026 and J0299's online publication year of 2026. Original database years are preserved in the input snapshot. Three links have a cited year later than the source report year and are listed in `output/audit/chronology_flags.json`. Conference-volume dates, preprints, later local versions and issue allocations can produce these differences.

The full graph is a descriptive reconstruction of the supplied evidence. It is not a complete history of the field, and shared references do not alone establish intellectual influence or clinical adoption. The 25-reference limit affects only the focus figure; it does not filter the complete graph.

## Bibliometrix execution and checks

The October 16, 2026 build for the same 44 report IDs was analyzed with **Bibliometrix 5.5.0** under **R 4.6.1**, using `histNetwork()` and `histPlot()`. The prepared input is `output/bibliometrix/bibliometrix_expanded.csv`: included-paper rows carry the recovered direct references, and added cited-work rows have no collected reference lists. Reference strings use canonical node labels for unambiguous matching. `DB = WOS` selects the normalized-reference parser; this is enriched input, not an original Web of Science export. `TC` / native `GCS` are computational zeros because a harmonized global-citation metric was not collected; do not report those zeros as observed global citations.

Two implementation cases are documented in `run_bibliometrix_expanded.R`:

1. Bibliometrix 5.5.0 trims empty-DOI labels while constructing its matrix. Adjacency was reconciled only from the package's returned local-reference strings (`LCR`), with every column sum checked against its native `LCS`.
2. Brier's 1950 DOI contains a semicolon, which conflicts with the reference separator. That DOI was omitted only from the computational matching field; the canonical node label still matches it, and its full DOI remains unchanged in the input/evidence records.

The final graph and the archived Bibliometrix run agree on all **2,210 source–target pairs**. The archived run assigned CURENet (J0093) to 2025. Its edge table is included as an adjacency check. The prepared final-year input assigns CURENet to 2026. Running the R command below on that input produces the year-sensitive native tables, R objects and plot. See `output/audit/bibliometrix_run_log.txt` for the archived run and `output/audit/validation.json` for the final graph counts.

## Reproduce from the committed data

Open `output/explorer/reference_network_explorer.html` directly in a browser, or run `python3 -m http.server 8000` in this directory and visit `http://localhost:8000/output/explorer/reference_network_explorer.html`. The HTML is self-contained.

```sh
python3 -m pip install -r requirements.txt
python3 assemble_network.py
python3 prepare_exports.py
python3 draw_expanded_network.py
python3 build_explorer.py
python3 verify_network.py
```

To generate the native Bibliometrix outputs, run `Rscript run_bibliometrix_expanded.R output` with Bibliometrix 5.5.0. The committed `output/bibliometrix/R_sessionInfo.txt` documents the archived edge-validation run. Opening the explorer and verifying the committed network require neither R nor network access. The explorer builder uses vendored vis-network assets with the upstream license notice.

`extract_references.py`, `build_reference_data.py`, `fetch_doi_metadata.py` and `prepare_exports.py` preserve the original extraction/export workflow. These archival scripts depend on the original scoping-review workspace, full texts, bounding-box extracts and database; those source documents and the review database are not bundled here. Use the committed reference evidence and portable commands above for this standalone repository. The original absolute source paths in the evidence ledger describe provenance, not repository file locations.

`verify_network.py` checks that the frozen cohort, evidence, final graph and archived Bibliometrix edge pairs agree.

## Suggested caption

Expanded historical direct-citation network from the reference lists of 44 included papers. The focus view displays all 44 source papers (blue diamonds) and the 25 external reference nodes cited by the largest numbers of included papers (gold circles), connected by 197 direct citation links. Arrows point from citing paper to cited work; gold-circle area increases with the number of distinct citing included papers. The full graph contains 1,902 nodes and 2,210 links, including long-tail references not shown in the focus view. References with unresolved dates remain in an undated lane in the accompanying explorer. Source-paper years follow the manuscript supplement; publication-version and year discrepancies are documented in the audit. No citation links among external references were inferred.

Software: Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959–975. https://doi.org/10.1016/j.joi.2017.08.007

Primary workflow: https://github.com/massimoaria/bibliometrix#historical-direct-citation-network
