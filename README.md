# Expanded historical citation network

This replaces the earlier within-review network with a one-step expansion: **the 45 included papers plus the works in their reference lists**, including papers outside the inclusion set and years before 2024. It is a directed reference network, not a keyword-flow or co-citation diagram.

## Main outputs

All generated artifacts are organized under `output/`; scripts, source inputs and vendored libraries remain at the repository root. See [the output index](output/README.md) for the folder layout and direct links.

- `output/explorer/reference_network_explorer.html`: self-contained interactive explorer. Search an included paper ID to inspect its bibliography; search a reference title to inspect the included papers citing it. Select **All references**, then **Overview**, to display the complete graph. Search or zoom to read a neighborhood. No external scripts or data service is needed to open this HTML.
- `output/figures/expanded_reference_historiograph.png`, `.svg`, `.pdf`: readable focus figure containing all 45 included papers and the 25 external reference nodes with the largest numbers of distinct citing included papers. This view contains 70 nodes and 199 direct links. The SVG is editable.
- `output/network/expanded_reference_network.graphml`: the complete directed graph, for Gephi/Cytoscape.
- `output/network/network_nodes.csv`, `output/network/network_edges.csv`: complete graph, including all long-tail and undated references.
- `output/evidence/reference_evidence.csv` / `output/evidence/reference_occurrences.json`: all 2,244 recovered reference entries, original citation strings, source locations, identifiers and their mapping to graph nodes.
- `output/bibliometrix/bibliometrix_expanded_histResults.rds`, `output/bibliometrix/bibliometrix_histData.csv`, `output/bibliometrix/bibliometrix_validated_edges.csv`: executed Bibliometrix results. `output/bibliometrix/bibliometrix_native_focus.png` retains the native histPlot view; the polished figure uses a separate readable layout of the same validated links.

## Scope and results

The current completed Include query was rechecked against the live local database and matches the same 45 unique IDs. The database and source documents were not modified.

There are **2,244 recovered reference entries**, represented by **1,879 external cited-reference nodes** plus the 45 included-paper nodes: **1,924 nodes and 2,237 distinct directed links** in total. All 45 included papers have outgoing reference links. Multiple references from one paper to the same resolved node count as one link; all original entries remain in the evidence ledger.

Known reference years span **1947–2026**. Thirty-five external reference nodes have no reliable year and remain in an undated lane in the explorer; they are retained in the graph and evidence tables. These are reconstructed reference identities, not an assertion that every bibliographic version has been resolved to a unique underlying study. Different versions can remain separate.

For example, the explicit 2017 citation **Attention is all you need** is cited by eight distinct included papers: J0015, J0042, J0045, J0060, J0093, J0102, J0216 and J0345. **GRAM: Graph-based attention model for healthcare representation learning** is another shared 2017 reference and is cited by nine included papers. These counts are within this review's reference lists, not global citations.

The graph covers direct references made **by the 45 source papers**. The reference lists of the external works were not recursively retrieved, so citation links among those external works are not inferred. An external node's absence of outgoing links means those reference lists were not collected; it does not mean the work cites nothing. Source-paper citation links to other included papers are retained where identifiers or title/year evidence resolve the reference back to an included node.

## Source extraction

- For 30 source papers, nonempty cached Crossref cited-reference lists supply 1,425 reference entries.
- For 15 papers without such lists, reference blocks were recovered from local full texts: 817 entries. Numbered lists were segmented by reference number and checked for consecutive numbering. The four unnumbered lists were segmented using PDF hanging-indent coordinates and bounded reference sections; first/last entries and starts were inspected.
- Two additional numbered entries present in local report versions beyond the cached reference-list lengths were retained, with explicit `fulltext_additional_reference` provenance. They are J0206 reference 54 and SC0376 reference 57. Thus the analysis reflects the available reference evidence, including labeled local-version additions.
- Local text helped recover metadata for cached references only through an identifier or literal-title match. Equal list length or reference ordinal was not accepted by itself as evidence of identity.
- Running headers, page footers, author-biography sections and appendices were excluded from reference blocks. The citing paper's own DOI in a repeated page header was not treated as a cited reference. Original citation text and source line ranges remain inspectable.
- Missing DOI metadata were retrieved from public Crossref records. Cached responses are under `output/metadata/doi_metadata/`; no reference lists of those external works were added as new edges.

The exact source query is the same completed-Include query used in `inputs/source.query.sql`. `output/evidence/source_coverage.json` records source type and reference counts per paper. Raw full-text segmentation for the 30 cached-list papers is an alignment aid, not a replacement for their cited-reference metadata; some PDFs have extraction/order differences.

## Identity and date handling

Records were matched by exact normalized DOI, exact arXiv ID, or an eligible exact normalized title plus year. Short, distinctive title variants for *Attention is all you need* and GRAM were explicitly reviewed against citation text. Generic names or empty titles were not merged. Punctuation and hyphen variants were normalized, and every occurrence retains its original citation string and identifiers. Explicit arXiv identifiers can connect a preprint reference to an included work whose record carries that identifier.

DOI metadata are preferred for identifying a work when available. Otherwise titles/years may come from structured reference metadata, literal title matches, quoted titles or parsed citation text. When a clean title is unavailable the reference string is retained as the node label. `title_basis` and `metadata_title_basis` distinguish these cases; raw citation strings are not presented as independently verified article titles. Multiple reported years are retained in `observed_years`. Ambiguous versions and formatting errors may leave duplicates or missed matches in the long tail. This is a single-reviewer reconstruction, not an independently double-reviewed bibliography.

The 45 included papers keep their current database years for consistency with the supplied cohort. Five source records differ from the local verified citation registry: J0093 (database 2026, registry 2025), J0216 (2024, 2025), J0238 (2025, 2026), J0299 (2025, 2027 issue allocation), and J0300 (2025, 2026). In addition, nine links have a referenced year later than the recorded source-paper year; these are retained and listed in `output/audit/chronology_flags.json`. Conference-volume dates, preprints, later local versions and issue allocations can produce these conflicts. Resolve a consistent publication-version/year policy before interpreting the timeline as a finalized historical sequence. Date differences were not used to invent or remove citation evidence.

The full graph is a descriptive reconstruction of the supplied evidence. It is not a complete history of the field, and shared references do not alone establish intellectual influence or clinical adoption. The 25-reference limit affects only the focus figure; it does not filter the complete graph.

## Bibliometrix execution and checks

The expanded collection was actually passed to **Bibliometrix 5.5.0** under **R 4.6.1**, using `histNetwork()` and `histPlot()`. The prepared input is `output/bibliometrix/bibliometrix_expanded.csv`: included-paper rows carry the recovered direct references, and added cited-work rows have no collected reference lists. Reference strings use canonical node labels for unambiguous matching. `DB = WOS` selects the normalized-reference parser; this is enriched input, not an original Web of Science export. `TC` / native `GCS` are computational zeros because a harmonized global-citation metric was not collected; do not report those zeros as observed global citations.

Two implementation cases are documented in `run_bibliometrix_expanded.R`:

1. Bibliometrix 5.5.0 trims empty-DOI labels while constructing its matrix. Adjacency was reconciled only from the package's returned local-reference strings (`LCR`), with every column sum checked against its native `LCS`.
2. Brier's 1950 DOI contains a semicolon, which conflicts with the reference separator. That DOI was omitted only from the computational matching field; the canonical node label still matches it, and its full DOI remains unchanged in the input/evidence records.

All **2,237** resulting native local-reference edges were checked against the prepared source-target pairs, with no duplicate edges or self-loops. All 2,244 occurrence IDs map to nodes, and all 45 source papers are present. The main PNG and a rendered PDF were visually inspected; the explorer's overview, full graph, 2017 reference search and source-paper bibliography search were exercised. See `output/audit/validation.json` and `output/audit/bibliometrix_run_log.txt`.

## Reproduce from the committed data

Open `output/explorer/reference_network_explorer.html` directly in a browser, or run `python3 -m http.server 8000` in this directory and visit `http://localhost:8000/output/explorer/reference_network_explorer.html`. The HTML is self-contained.

```sh
python3 verify_network.py
python3 -m pip install -r requirements.txt
python3 assemble_network.py
Rscript run_bibliometrix_expanded.R output
python3 draw_expanded_network.py
python3 build_explorer.py
```

The R step requires Bibliometrix 5.5.0; `output/bibliometrix/R_sessionInfo.txt` records the executed environment. Prepared R input and results are committed, so opening the explorer and validating the frozen data require neither R nor network access. `assemble_network.py` uses `inputs/included_papers.json` and the committed reference occurrences. The explorer builder uses the vendored vis-network assets. Their upstream license notice is retained in the JavaScript distribution.

`extract_references.py`, `build_reference_data.py`, `fetch_doi_metadata.py` and `prepare_exports.py` preserve the original extraction/export workflow. These archival scripts depend on the original scoping-review workspace, full texts, bounding-box extracts and database; those source documents and the review database are not bundled here. Use the committed reference evidence and portable commands above for this standalone repository. The original absolute source paths in the evidence ledger describe provenance, not repository file locations.

The original database cohort check is recorded in `output/audit/validation.json`; `verify_network.py` checks the frozen graph and its native Bibliometrix edge agreement without needing that database. No system-wide R installation was made for the original analysis.

## Suggested caption

Expanded historical direct-citation network from the reference lists of 45 included papers. The focus view displays all 45 source papers (blue diamonds) and the 25 external reference nodes cited by the largest numbers of included papers (gold circles), connected by 199 direct citation links. Arrows point from citing paper to cited work; gold-circle area increases with the number of distinct citing included papers. The full graph contains 1,924 nodes and 2,237 links, including long-tail references not shown in the focus view. References with unresolved dates remain in an undated lane in the accompanying explorer. Source-paper years follow the review database; publication-version and year discrepancies are documented in the audit. No citation links among external references were inferred.

Software: Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959–975. https://doi.org/10.1016/j.joi.2017.08.007

Primary workflow: https://github.com/massimoaria/bibliometrix#historical-direct-citation-network
