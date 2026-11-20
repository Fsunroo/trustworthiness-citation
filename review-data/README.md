# Scoping review data

This release contains the coded results and source locators for 44 published reports on generative large language models using publicly accessible critical care electronic health record datasets. The coverage analysis uses 148 primary evaluations. Two contextual evaluations are retained for the all-linked sensitivity analysis.

| Manuscript output | Files |
| --- | --- |
| Figure 1, study selection | [Flow counts](figure_1_flow_counts.csv). The supplementary document reports the search strategies. |
| Table 2 and Table S1, corpus and task characteristics | [Table S1 source data](table_s1_characteristics.csv), [corpus](corpus_characteristics.csv), [evaluation characteristics](evaluation_characteristics.csv), and [task counts](task_characteristics.csv) |
| Table 3, Tables S2–S4, and Figures 2–3 | [Report coverage](article_coverage.csv), [evaluation coverage](experiment_coverage.csv), [task-family coverage](task_family_coverage.csv), [report indicator matrix](article_indicator_matrix.csv), and [evaluation indicator matrix](evaluation_indicator_matrix.csv) |
| Sensitivity analysis of all 150 linked evaluations | [All-linked coverage](all_linked_coverage.csv) and [contextual evaluation decisions](contextual_evaluation_decisions.json) |
| Figure S1 and Figure S2 | [Dataset coding](dataset_coding.json), [task coding](task_coding.json), and [model adaptation coding](adaptation_coding.json) |
| Figure S3 and Table S5, author-affiliation geography | [Report assignments](author_affiliation_country_assignments.csv) and [country or territory counts](author_affiliation_country_counts.csv) |
| Figure S4 and Table S6, citation network | [Citation-network outputs and code](../README.md#main-outputs) |
| Table S7, funding | [Included-report funding summaries](included_report_funding.csv) |

The [156-item instrument](checklist_v1.0.md), [operational codebook](CODEBOOK_v1.1.md), and [6,864 coded item responses](item_responses.csv) describe the charted evidence. The [784 reported numerical estimates](descriptive_result_ledger.csv) retain their original units and denominators. The [source locator index](source_locators.csv) maps evidence IDs to source locations. Table S1 and the citation-network input identify the publications. The repository distributes study-level data derived from publications.

The [source discrepancy ledger](source_discrepancies.csv), [eligibility scope annotations](corpus_scope_flags.json), [artifact availability](inspected_artifact_availability.csv), and [positive assessment scope](positive_assessment_scope.csv) document qualifications that affect interpretation. The flow count file transcribes the manuscript diagram and supports checking the arithmetic. The historical coding for supplementary Figures S1–S2 uses categories specific to those figures.

Run the following from the repository root with Python 3:

    python3 review-data/verify_review_data.py

The check recomputes report and evaluation coverage, task-family breakdowns, and sensitivity frequencies from the indicator matrix. It checks corpus and result counts, selection arithmetic, and affiliation counts. To check the citation network, run:

    python3 verify_network.py

To regenerate the main coverage plots, install the repository's Python requirements and run:

    python3 review-data/plot_coverage.py /path/to/output-directory
