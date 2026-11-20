# Article extraction checklist for trustworthiness and reproducibility of LLMs using public ICU EHR data

Version 1.0 — 16 October 2026

## Purpose and limits

Use this form to characterize what each eligible article reports, what it empirically evaluates, and what supporting resources are accessible. It is tailored to the review of existing generative LLM applications using public critical-care EHR data. It is a proposed extraction instrument, not a validated risk-of-bias scale, certification of clinical safety, or reproduction of a published reporting checklist. Pilot and finalize the codebook before applying it to the complete corpus. Document this additional extraction as an amendment to the review methods.

All sections must be considered for every article; conditional sections receive a reasoned not-applicable code when appropriate. An article is not expected to satisfy every item. Reuse previously extracted information only after verifying its source.

## How to record an answer

For each item record: article ID; experiment ID if relevant; item ID; applicability; response; extracted value or method; evidence quotation; source and locator; reviewer ID; extraction date; verification status; and unresolved notes. Keep literal source claims separate from reviewer interpretation.

Use these response codes for questions about whether something was reported or done:

| Code | Meaning | Coding rule |
|---|---|---|
| Y | Explicitly reported or performed | Identify the exact method or evidence; a general claim is insufficient to establish an empirical test. |
| N | Explicitly not reported as done or explicitly not performed | Use only for a direct statement of absence, or a verified negative observation such as an inaccessible repository on a recorded date. Do not infer N from silence. |
| NR | Not reported in assessed materials | No relevant information located after inspecting all retrieved relevant sources. This does not prove the procedure was not performed. |
| U | Unclear or conflicting | Record ambiguous wording or both conflicting accounts without silently choosing one. |
| NA | Not applicable | Give a task- or design-specific reason. The absence of a test is not a reason to mark it NA. |
| UA | Relevant source unavailable | Identify the missing supplement, repository, or other source and attempted retrieval. |
| PENDING | Not yet assessed | A workflow state only; resolve before synthesis or report as incomplete review work. |

For descriptive fields, enter the actual value or NR/U/NA/UA. Record units and denominators with numbers. If information is partial, record the known value plus the missing subfields; do not label an entire item complete. For compound checklist prompts below, preserve each named subfield separately whenever you intend to calculate its reporting frequency.

Maintain three separate columns where relevant:

1. **Reporting evidence:** what the article or supplementary source says.
2. **Empirical evaluation evidence:** what was tested, on which cases, against which reference, and with what result.
3. **Reviewer verification:** source checked; resource accessible; artifact contents inspected; or experiment independently rerun. State the level actually reached.

Example: “RAG used” may receive Y for use of retrieval, while empirical grounding evaluation remains NR. “Code will be released” is a planned release, not an accessible artifact. A calibration method used during development is not proof that calibration was evaluated on held-out data.

## Units and repeatable records

Keep one article-level record and linked experiment records. Create an experiment record when clinical task, evaluation cohort, observation cutoff, model role, or validation design changes materially. Link model variants within an experiment instead of treating every prompt ablation as a separate study.

Recommended linked tables are Articles, Experiments, Cohorts and splits, Model configurations, Evaluation results, Item responses and evidence, Artifacts, and Reviewer decisions. Use stable IDs. Keep different reports of the same underlying study linked to avoid confusing report counts with independent study counts.

For every result record: experiment and model configuration; cohort and split; task and horizon; metric and definition; estimate; uncertainty; sample unit and denominator; event prevalence if relevant; comparator; and source locator. Record whether the result is from the public ICU cohort or an additional comparator population.

## A Article identity and accessible evidence

- [ ] A01 Record article ID, full citation, DOI or stable identifier, venue, and publication status.
- [ ] A02 Record online publication date, issue/proceedings date, and version assessed; resolve or flag differences.
- [ ] A03 Identify related preprints, conference versions, extensions, corrections, and duplicate reports.
- [ ] A04 Record all retrieved sources: main article, supplements, protocols, repositories, model cards, and data documentation; retain version and access date.
- [ ] A05 Identify referenced sources that could not be retrieved and record retrieval attempts. Do not contact authors without an authorized communication workflow.
- [ ] A06 Record authors' stated objective, research question, and primary contribution.
- [ ] A07 Record funding, relevant conflicts, commercial relationships, and disclosed AI assistance in the study.
- [ ] A08 Record protocol or preregistration availability, date, planned primary outcomes, and disclosed deviations, where applicable.

## B Eligibility and intended clinical use

- [ ] B01 Identify the exact public ICU dataset and evidence that an identifiable ICU cohort was empirically used.
- [ ] B02 Identify any hospital-wide, emergency, outpatient, private, or non-ICU comparator populations separately.
- [ ] B03 Record which structured variables enter the LLM itself, which enter only a downstream model, and which are merely used for evaluation.
- [ ] B04 Record whether structured variables are serialized into text, processed numerically, or combined with clinical text or other modalities.
- [ ] B05 Identify the LLM role: clinical generator, predictor/classifier, feature extractor, synthetic-data generator, retriever, teacher, evaluator, or other. Allow multiple roles.
- [ ] B06 Record whether clinical output is generated autoregressively, obtained from a classification head, or produced by a hybrid pipeline.
- [ ] B07 Record intended task, user, clinical setting, decision supported, and whether the output is retrospective description or future prediction.
- [ ] B08 Record the intended moment of use and whether deployment is advisory, clinician-supervised, or autonomous. Do not infer deployment from an offline benchmark.

## C Clinical cohorts and representativeness

- [ ] C01 Record dataset release, originating institutions, countries, and collection years; distinguish patient-data origin from author affiliation.
- [ ] C02 Record cohort inclusion/exclusion criteria, ICU definition, index encounter, and repeated-admission handling.
- [ ] C03 Record screened, eligible, included, development, internal-test, external-test, and human-review counts separately, with their units.
- [ ] C04 Record age eligibility and observed distribution, sex/gender as defined, and race/ethnicity categories and missingness when available. Do not infer analytic demographics from the database name.
- [ ] C05 Record clinical conditions, severity, ICU types, and demographic or institutional representation relevant to the intended use.
- [ ] C06 Record outcome frequency, class imbalance, exclusions after outcome ascertainment, and any outcome-based sampling.
- [ ] C07 Record missingness, missingness-related exclusions, and differences between included and excluded patients if examined.
- [ ] C08 Identify overlapping cohorts within the article, shared benchmarks, or possible overlap across dataset versions; distinguish demonstrated independence from unverified independence.

## D Inputs and decision-time information

- [ ] D01 Record each input source, feature set, note type, sampling frequency, and preprocessing sequence.
- [ ] D02 Record index time, observation-window start and end, and prediction horizon for each task and class.
- [ ] D03 Determine whether timing is fixed at a prospective decision point or aligned retrospectively to an event; record differences between positive and negative cases.
- [ ] D04 Record which timestamps establish real-world availability: event, specimen, result, entry, note authoring, or note finalization time.
- [ ] D05 Check whether discharge diagnoses, completed stay duration, later treatments, post-event measurements, or retrospective summaries can reach the input.
- [ ] D06 Record checks that inputs precede the decision point and whether a temporal audit or feature-gating test was actually performed.
- [ ] D07 Record imputation, normalization, feature selection, label-informed filtering, and where their parameters were fitted.
- [ ] D08 Record truncation, compression, aggregation, unit conversion, and information lost through context-window constraints; extract any evaluation of their effects.

## E Model and implementation identity

- [ ] E01 Record exact provider, model name, checkpoint or dated API snapshot, parameter size if reported, and study inference dates.
- [ ] E02 Record access mode: local weights, API, or interactive interface; hosted deployment region if reported and relevant.
- [ ] E03 Record model role separately for generators, encoders, judges, teachers, agents, and auxiliary tools.
- [ ] E04 Record adaptation: frozen prompting, learned prompt tuning, adapters/LoRA, full fine-tuning, classification-head training, or other; identify updated components.
- [ ] E05 Record training data source, sample size, labels, synthetic augmentation, and separation from evaluation data.
- [ ] E06 Record optimization, hyperparameter search, early stopping, checkpoint selection, and validation criteria if training or tuning occurred.
- [ ] E07 Record software versions, hardware, precision/quantization, context limit, and inference framework.
- [ ] E08 Record stated pretraining provenance and cutoff, medical adaptation, and unknown or proprietary training details without assuming them from a model family name.

## F Prompts and inference procedure

- [ ] F01 Record availability and completeness of system instructions, user templates, exemplars, and task-specific prompts.
- [ ] F02 Record prompt development procedure, who selected prompts, and the development dataset.
- [ ] F03 Record exemplar number, selection method, source split, label content, ordering, and any retrieval-based selection.
- [ ] F04 Record temperature, top-p/top-k if used, maximum output tokens, seed controls, and decoding/stopping rules; mark unsupported settings NA.
- [ ] F05 Record number of calls per patient, repeats, retries, conversation resets, and whether prior cases remain in context.
- [ ] F06 Record output parsing, code mapping, probability construction, invalid-output handling, and any manual editing or adjudication before scoring.
- [ ] F07 Record whether test outcomes informed prompt refinement, retry selection, model selection, or selection of the final displayed answer.
- [ ] F08 Record demonstrations of prompt sensitivity or inference-setting sensitivity separately from the mere reporting of settings.

## G Evaluation independence and leakage safeguards

- [ ] G01 Record train/development/validation/test partitions, split fractions, actual counts, and split construction method.
- [ ] G02 Record separation unit: patient, stay, admission, visit, note, time point, institution, or other; identify repeated-patient handling.
- [ ] G03 Record whether test sets were isolated from all development, preprocessing, tuning, prompt selection, and model selection steps.
- [ ] G04 Record whether retrieval stores, patient memories, graphs, and few-shot pools were built from permitted data only and frozen before evaluation.
- [ ] G05 Record whether duplicate notes, reused cases, adjacent visits, or cross-database patient overlap were checked and addressed.
- [ ] G06 Record whether labels or reference answers entered generated reasoning, training-example filtering, judge prompts, or evaluated outputs; distinguish valid training use from test leakage.
- [ ] G07 Record author discussion of pretraining contamination separately from empirical contamination tests, their methods, and outcomes.
- [ ] G08 Record test-set reuse across iterations and whether the final test was untouched; separate explicit safeguards, unresolved reporting questions, and demonstrated leakage.

## H Clinical reference standards and comparators

- [ ] H01 Record exact target definition, clinical horizon, label construction, diagnostic criteria, and data fields used to establish truth.
- [ ] H02 Record reference type: observed outcome, billing code, historical treatment, expert consensus, guideline, reference text, or another model.
- [ ] H03 Record reference ascertainment timing and whether the reference is independent of model input and model output.
- [ ] H04 Record missing/uncertain labels, label-quality checks, assessor disagreements, and adjudication.
- [ ] H05 Record comparator types: standard clinical score, conventional ML, matched backbone, clinician, workflow, or ablation.
- [ ] H06 Record whether comparators received equivalent clinical information, observation windows, patient samples, and development opportunities.
- [ ] H07 Record whether comparator results were rerun in the same experiment or taken from other publications.
- [ ] H08 Record whether endpoints represent clinical correctness, documentation agreement, historical treatment imitation, explanation fidelity, or perceived usefulness; preserve these distinctions.

## I Statistical validity and completeness of evaluation

- [ ] I01 Record prespecified primary and secondary metrics and the reason for their choice.
- [ ] I02 Record sample-size rationale or precision/power calculation; for human evaluation record patients, outputs, and raters separately.
- [ ] I03 Record independent sample unit and treatment of repeated predictions, multiple outputs, multiple raters, and correlated observations.
- [ ] I04 Record confidence intervals or other uncertainty measures and their calculation/resampling unit.
- [ ] I05 Record paired comparative analyses, multiplicity handling, and whether the same cases were used for comparisons.
- [ ] I06 Record all attempted cases, failures, refusals, missing outputs, exclusions after generation, and denominators used for reported metrics.
- [ ] I07 Record development-selected thresholds and whether thresholds or postprocessing changed on the test set.
- [ ] I08 Record sensitivity analyses, inconsistencies among text/tables/figures, selective case presentation, and any explanation supplied by authors.

## J External validity and transportability

- [ ] J01 Classify each evaluation: random internal holdout, temporal holdout, hospital holdout, independent external dataset, prospective observation, or clinical intervention.
- [ ] J02 Record source and target institutions, collection periods, case mix, and data provenance to establish what changed.
- [ ] J03 Record whether the complete system transferred unchanged or underwent retraining, prompt revision, retrieval rebuilding, recalibration, or local adaptation.
- [ ] J04 Record external sample size, outcome prevalence, performance, uncertainty, and change relative to internal evaluation.
- [ ] J05 Record dataset harmonization, unavailable features, mapping assumptions, translation, and target-domain exclusions.
- [ ] J06 Record differences in performance across sites, periods, ICU types, severity groups, or task domains.
- [ ] J07 Record the independence of external investigators and evaluators separately from independence of the external data.
- [ ] J08 Record prospective data collection separately from prospective inference, clinician exposure, and measured workflow or patient effects.

## K Reliability and robustness

- [ ] K01 Record repeated inference on identical cases, repeat count, stochastic settings, and variation in clinically meaningful outputs.
- [ ] K02 Record prompt paraphrase, exemplar order, context order, or alternate instruction tests and their results.
- [ ] K03 Record sensitivity to measurement noise, missing inputs, unit changes, outliers, or realistic data-entry errors.
- [ ] K04 Record sensitivity to note length, irrelevant text, conflicting records, truncation, or summarization/compression choices.
- [ ] K05 Record out-of-distribution, rare-condition, distribution-shift, and unsupported-input tests.
- [ ] K06 Record robustness of the complete pipeline to retrieval failure, tool failure, parsing errors, or unavailable services when relevant.
- [ ] K07 Record degradation in clinical performance or harmful errors, rather than counting the existence of a stress test alone.
- [ ] K08 Record mitigation evaluation and residual failure modes; distinguish repeatability, factual correctness, and predictive accuracy.

## L Fairness and subgroup evaluation

- [ ] L01 Record whether subgroup evaluation was performed and the clinical or ethical rationale for the selected groups.
- [ ] L02 Record subgroup definitions, source of attributes, missingness, sample sizes, and event counts.
- [ ] L03 Record subgroup discrimination, calibration, error rates, clinical utility, or output quality as appropriate to the task.
- [ ] L04 Record disparity definitions, reference groups, estimates, uncertainty, and formal comparisons if used.
- [ ] L05 Record intersectional analysis and whether small or absent groups prevent reliable comparison.
- [ ] L06 Record counterfactual demographic tests separately from observed-population subgroup tests, including plausibility controls.
- [ ] L07 Record evaluated mitigation and its tradeoffs in overall performance, other groups, and clinically important errors.
- [ ] L08 Record limits on interpretation due to sample size, case mix, label bias, or missing attributes. Demographics as inputs are not fairness evaluation.

## M Clinical errors safety and uncertainty communication

- [ ] M01 Record definitions and assessment of clinically consequential errors, omissions, contraindications, and unsupported recommendations.
- [ ] M02 Record error severity, frequency, denominator, assessor qualifications, and adjudication.
- [ ] M03 Record abstention, refusal, escalation, uncertainty statements, and clinician-review mechanisms; distinguish implemented mechanisms from proposed ones.
- [ ] M04 Record empirical evaluation of these mechanisms, including missed unsafe cases and unnecessary abstention/escalation.
- [ ] M05 Record selective prediction results as paired coverage and performance, including performance in rejected cases if available.
- [ ] M06 Record whether explanation quality was evaluated for correctness or fidelity, rather than readability or persuasiveness alone.
- [ ] M07 Record safety-specific tests of misleading context, instruction conflicts, prompt injection, or unsafe tool use when the system is exposed to those risks.
- [ ] M08 Record reported adverse effects and unresolved failure modes. Absence of observed harm in an offline test does not establish clinical safety.

## N Human and automated evaluation

- [ ] N01 Record human evaluator number, profession, expertise, recruitment, conflicts, training, and access to clinical context.
- [ ] N02 Record how cases and outputs were sampled for review and whether they represent the full evaluation cohort.
- [ ] N03 Record blinding to model identity, output origin, comparator, and reference answer where relevant.
- [ ] N04 Record rubric, rating scale, acceptability thresholds, assessor instructions, and their development or validation.
- [ ] N05 Record assignment of outputs to raters, independent rating, adjudication, and inter-/intrarater agreement.
- [ ] N06 Record whether a model judge was used; its exact identity, prompts, settings, reference access, and relationship to the generating model.
- [ ] N07 Record human validation of automated or LLM judgments, including sample size, agreement, disagreements, and relevant bias checks.
- [ ] N08 Record whether conclusions concern perceived usefulness, content correctness, clinician behavior, or patient outcomes; avoid substituting one for another.

## O Reproducibility reporting and artifact audit

- [ ] O01 Record cohort-query code and executable preprocessing, feature construction, split generation, and label construction availability.
- [ ] O02 Record availability of prompts, exemplars or their selection procedure, inference scripts, output parsing, and evaluation scripts/rubrics.
- [ ] O03 Record weights/adapters or exact obtainable checkpoints and API snapshots, including licenses and access requirements.
- [ ] O04 Record environment lockfiles, dependency versions, hardware requirements, seeds, configurations, and instructions.
- [ ] O05 Record data-access procedure, dataset releases, linkage rules, and whether evaluation membership can lawfully be reconstructed; do not require prohibited patient-data redistribution.
- [ ] O06 Record repository URL, access date, release/commit identifier, license, status (released/planned/private/broken), and contents actually inspected.
- [ ] O07 Record whether saved outputs, run logs, aggregate results, and human annotations are available under appropriate governance.
- [ ] O08 Record evidence of reproduction: author rerun, independent rerun, or none reported; who reran what, with which inputs and environment, and how agreement was assessed. An accessible repository is not a successful rerun.

## P Governance and feasibility

- [ ] P01 Record ethics approval or waiver, data-use authorization, and relevant privacy safeguards as stated.
- [ ] P02 Record whether patient data were transmitted to external services and any stated permission, retention, or access arrangements; do not infer violations from missing reporting.
- [ ] P03 Record de-identification, memorization, patient-information disclosure, or re-identification tests if relevant and performed.
- [ ] P04 Record inference latency, token use, monetary cost, hardware, throughput, and the measurement conditions.
- [ ] P05 Record clinician workload, correction time, usability, automation bias, or decision changes if empirically evaluated.
- [ ] P06 Record actual deployment stage, monitoring, version-change handling, fallback procedures, and human accountability if applicable.
- [ ] P07 Record clinical utility, workflow effects, patient outcomes, and harms measured under actual use; describe study design and comparator.
- [ ] P08 Record authors' claimed readiness and whether it is supported by offline metrics, prospective observation, or interventional evidence.

## Q Prediction and classification module

Apply when an experiment predicts an outcome or assigns clinical categories, including hybrid classifiers. Explanation-only studies do not receive prediction-performance credit.

- [ ] Q01 Record AUROC, AUPRC and outcome prevalence; retain exact task, cohort, estimate, and uncertainty.
- [ ] Q02 Record sensitivity, specificity, PPV/NPV, F1, or other threshold metrics with threshold and selection method; for multiclass/multilabel tasks record averaging and class-wise results where available.
- [ ] Q03 Record calibration assessment: plots, intercept, slope, observed/expected ratio, Brier score, or other method. Preserve components separately; a Brier score alone does not establish good calibration.
- [ ] Q04 Record how a probability was obtained from the LLM or classifier and distinguish calibrated probability from verbal confidence or repeated-answer frequency.
- [ ] Q05 Record clinical decision thresholds, decision-curve/net-benefit or other utility evaluation when performed; do not demand a single measure across all tasks.
- [ ] Q06 Record censoring, competing events, repeated horizons, and time-dependent evaluation where relevant; otherwise NA.

## R Clinical text diagnosis and recommendation module

Apply to generated summaries, diagnoses, recommendations, or explanations; activate only the relevant subfields. A prediction-only numeric classifier need not receive text-generation checks.

- [ ] R01 Record factual correctness against patient records, including unsupported facts, wrong values, and incorrect attribution.
- [ ] R02 Record clinically important omissions, completeness, temporal consistency, and internal contradictions.
- [ ] R03 Record how evaluation units were defined: patient, output, statement, fact, medication, or recommendation; preserve denominators.
- [ ] R04 Record semantic/lexical metrics separately from clinical accuracy and any validation of automated scores against expert judgments.
- [ ] R05 For diagnostic outputs, record reference diagnosis, accepted alternatives, differential-list size, top-k definition, and matching/adjudication rules.
- [ ] R06 For recommendations, record guideline concordance, contraindication and interaction checks, and individualized appropriateness; historical clinician actions are not automatically optimal care.
- [ ] R07 Record explanation fidelity to the actual model or evidence separately from plausibility, readability, helpfulness, and perceived safety.
- [ ] R08 Record whether clinically consequential error categories and acceptable performance criteria were specified before evaluating outputs.

## S Retrieval tools and agents module

Apply only to experiments using retrieval, patient memory, tools, or multiple agents; record NA for unused components.

- [ ] S01 Record corpus source, version, collection date, document/patient membership, and evidence update policy.
- [ ] S02 Record embedding/retrieval model, chunking, indexing, top-k, reranking, filtering, and retriever-training details.
- [ ] S03 Record evaluation of retrieval relevance, factual grounding, citation correctness, and whether retrieved evidence supports the output; distinguish these outcomes.
- [ ] S04 Record presence and results of retrieval-disabled, token-matched, or other informative ablations, noting unequal context or computational budgets.
- [ ] S05 Record agent roles, model assignments, communication sequence, shared memory, routing, tools, and termination/retry conditions.
- [ ] S06 Record agent/tool trace availability, permission boundaries, error propagation, and tests of failures or conflicting agent recommendations.
- [ ] S07 Record whether external tools or retrieval expose the true outcome or post-index information and how that was checked.
- [ ] S08 Record whether the claimed benefit was established for an individual component or the complete deployed pipeline, with corresponding resource costs.

## T Reviewer synthesis and verification

- [ ] T01 List the article's strongest empirical evidence for each assessed domain, with source locators and task applicability.
- [ ] T02 List critical unresolved reporting questions separately from demonstrated methodological problems.
- [ ] T03 Record discrepancies across sources and how they were resolved, or why they remain unresolved.
- [ ] T04 Record which answers were independently verified, by whom, disagreements, and adjudicated final decisions.
- [ ] T05 Record changes to earlier coding and which article-level or experiment-level summaries must be updated.
- [ ] T06 Write a short evidence-limited conclusion for the article; do not assign a global trustworthiness score or clinical readiness certificate.

## Core synthesis matrix

Extract the full applicable form above. The following derived indicators provide a manageable main results table. Define each derived flag and retain links to its underlying item responses. Do not copy article-level labels into experiment records without checking them.

| Indicator | Items | Applicability and positive-evidence rule |
|---|---|---|
| Intended decision point defined | B07–B08, D02 | Each clinical experiment; explicit moment of use and task relationship. |
| Patient separation explicitly established | G01–G02 | Experiments with development/test partitioning or relevant repeated patients; patient-level separation documented, not assumed. |
| Test isolation from development established | F07, G03–G04, G08 | Experiments with tuning, retrieval construction or development; explicit isolation of all relevant stages. |
| Input timing empirically checked | D04–D06 | Tasks requiring decision-time availability; actual temporal audit, not a narrative assertion alone. |
| Pretraining contamination empirically tested | E08, G07 | Relevant pretrained-model evaluations; unknown training provenance is a limitation, not NA by itself. |
| Independent external-data evaluation | J01–J04 | Record external data independently of whether the system was frozen or adapted. Retain a separate frozen-transfer flag. |
| Temporal holdout evaluation | J01–J02 | Clinical experiments with relevant temporal transport questions; explicit temporal separation. |
| Discrimination evaluated | Q01–Q02 | Classification/prognostic tasks where applicable; record AUROC/AUPRC separately. |
| Calibration evaluated | Q03–Q04 | Experiments producing probabilities or making confidence-calibration claims; record each assessment method separately. |
| Repeated-output reliability tested | K01 | Experiments using generative/stochastic inference where relevant; empirical repeat evaluation. |
| Robustness tested | K02–K07 | At least one specified perturbation or shift test with results; retain test types separately. |
| Clinical factuality and omissions evaluated | R01–R03 | Generated clinical-content tasks; split factuality and omissions into separate flags. |
| Subgroup performance evaluated | L01–L04 | Clinically relevant patient-specific tasks; demographics alone do not qualify. |
| Clinically important errors evaluated | M01–M02, R08 | Clinical output tasks; explicit clinical error assessment and denominator. |
| Human evaluation performed | N01–N05 | Record whether human evaluation occurred; lack of human evaluation is not automatically methodological failure. |
| Automated judge checked against humans | N06–N07 | Only experiments using an automated judge for clinical-quality conclusions. |
| Matched comparator evaluation | H05–H07 | Comparative performance claims; matched cases, inputs and time windows, with limitations preserved. |
| Uncertainty appropriately reported | I03–I05 | Quantitative evaluation; extract method and clustering treatment without converting a reporting flag into formal risk-of-bias appraisal. |
| Exact model and inference configuration available | E01, F01, F04 | Split into model identity, prompt availability and decoding-settings flags. |
| Accessible implementation artifacts | O01–O06 | Inspect cohort, inference and evaluation artifacts separately; a single generic repository flag is insufficient. |
| Independent reproduction demonstrated | O08 | Claimed successful independent rerun with defined target and agreement, not merely code release. |
| Prospective observational inference | J08, P05–P07 | Prospective model evaluation with no intervention; distinguish prospective collection alone. |
| Clinical impact assessed under use | P05–P07 | Clinician exposure or intervention and measured effects; distinguish process from patient outcomes. |

## Analysis rules for the completed extraction

1. **Freeze applicability rules after the pilot.** Do not declare an item NA simply because a paper omitted the assessment. For example, no calibration test in a probabilistic mortality model is NR or explicit N, not NA. For a narrative-only summarizer without probabilistic claims, probability calibration can reasonably be NA.
2. **Use experiment-level extraction and article-level counting.** For an article-level domain frequency, count an article once if at least one applicable experiment meets the prespecified criterion. Label the result “at least one experiment.” Also report experiment-level coverage so a single well-tested arm does not conceal unevaluated arms.
3. **Report applicable denominators.** For each indicator give Y, explicit N, NR, U, UA, and NA counts. Report Y / all applicable articles as documented coverage, including unresolved applicable cases in that denominator. If applicability itself cannot be resolved, disclose a separate unknown-applicability count and a denominator range. A secondary assessed-source percentage may exclude UA, but must be labeled and shown alongside the full-corpus result.
4. **Separate claims from tests and artifacts.** Provide distinct tables for evaluation performed, implementation details reported, and artifacts verified accessible. Do not combine them as one quality percentage.
5. **Preserve clinical context.** Stratify findings by prediction, diagnosis/phenotyping, summarization, recommendations, and explanation/support tasks; also distinguish direct LLM outputs from hybrid downstream predictions.
6. **Avoid unsupported pooling.** Do not rank models across incompatible cohorts, prevalence, time horizons, or tasks. Do not sum shared patient counts or treat repeated outputs/ratings as independent patients.
7. **Treat external validation carefully.** Multiple datasets do not establish frozen transfer. Independent data and independent investigators are different properties. Check potential MIMIC-version overlap.
8. **Keep appraisal separate.** If formal risk-of-bias assessment is later added, select design-appropriate tools and a separate protocol. Reporting completeness is not a validated substitute.
9. **Do not apply hindsight as failure.** Evaluate the presence of information and tests; do not label earlier articles noncompliant with guidelines published after their conduct unless that is explicitly the analysis question.
10. **Keep amendments auditable.** Record codebook versions, pilot changes, retrieval cutoffs, reviewer decisions, and final machine-readable extraction data.

## Pilot and rollout

Pilot on five or six deliberately varied articles: a probabilistic predictor, a summarizer, a diagnostic agent, a hybrid feature-extraction pipeline, a retrieval system, and an article with incomplete supplements. These categories can overlap. Have two reviewers code independently, reconcile ambiguous fields, and revise definitions. Then recode pilot articles using the finalized version and apply it to all 44 reports. Double-check all core matrix indicators and the quantitative values used in the manuscript. Record the verification actually completed.

The final manuscript can then answer: which domains were evaluated, in which tasks and cohorts, using which methods, with what uncertainties, and with what accessible reproducibility support. Recommendations should follow the observed gaps rather than selected examples.

## Methodological references

The instrument is tailored to the review's clinical questions. The following sources support its reporting and review-method framework; this is not an item-by-item reproduction or validated extension of them.

- Gallifant et al. The TRIPOD-LLM reporting guideline for studies using large language models. Nature Medicine, 2025. https://doi.org/10.1038/s41591-024-03425-5 — reporting of clinical LLM studies; not a risk-of-bias score.
- The CHART statement and explanation and elaboration, 2025. https://doi.org/10.1136/bmjmed-2025-001632 and https://www.bmj.com/content/390/bmj-2024-083305 — relevant to chatbot advice and generated-response evaluation; not universally applicable to every ICU classifier.
- Peters et al. Updated methodological guidance for the conduct of scoping reviews. JBI Evidence Synthesis, 2020. https://doi.org/10.11124/JBIES-20-00167 — extraction procedures and transparent scoping-review methods.
- PRISMA-ScR checklist. https://www.prisma-statement.org/s/PRISMA-ScR-Fillable-Checklist_11Sept2019.pdf — reporting of the review itself, not a checklist for rating included LLM studies.
