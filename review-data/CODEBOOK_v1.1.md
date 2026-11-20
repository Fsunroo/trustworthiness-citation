# Operational codebook version 1.1

Parent decisions after source-based calibration of six varied articles. These rules supplement, and do not replace, the author-supplied 156-item checklist. No global trustworthiness score is permitted. The pilot independently assessed core indicators and selected numerical results, not two complete independent extractions of every checklist subfield.

## Reporting states and experiment boundaries

Use Y/N/NR/U/NA/UA as defined by the checklist. Missing patient-level safeguard is NR when no relevant statement exists; ambiguous 'patient split' wording in the presence of multiple admissions can be U. NA requires a concrete design reason. Explicitly retrospective evaluation can establish N for prospective inference in that experiment; a merely missing prospective statement cannot. A report may contain several different designs. Model/prompt stress variants within the same clinical task/cohort are configurations, not automatically additional experiments. The pilot's MIRA perturbation arm is linked within the corresponding MIRA experiment. Clinical task and validation/cohort changes remain separate experiments.

## Exact models prompts and settings

The core exact_model flag concerns **all material LLM roles** in the assessed system, including generators, clinical encoders and automated clinical judges, with important training-screening models noted. A uniquely named local checkpoint may qualify without a Git commit or hash; provider family alone is insufficient. Retain primary-model exactness separately in E01/E03 if an auxiliary role is unclear. Actual printed prompts can be partial/U when the retained optimized/adapted prompt is not identified.

The positive decoding rule requires actual used sampling/decoding configuration, including temperature or deterministic selection, output budget and the used nucleus/top-k settings where applicable; seed/repeat/termination details remain explicit subfields. Optional unused controls do not have to be invented. A single temperature is partial/U. A documented configuration including temperature, top-p, maximum tokens and seed can be Y while unreported stopping/default details remain noted. Next-token probability extraction without sampled generation may be NA for decoding and repeated-output tests, with a specific deterministic-feature explanation. Training-seed variation is not repeated-output reliability.

## Isolation timing and external evaluation

Test isolation requires explicit safeguards for documented adaptive stages: preprocessing fit, training/tuning, retrieval/exemplar construction and prompt/model selection where these occur. Do not demand assurance for hypothetical stages. When actual prompt/model development is unresolved, use U despite strong safeguards elsewhere. Post-hoc sensitivity analysis must remain separate from prespecified final model selection.

Input timing audit requires an actual test of decision-time availability. An output chronology audit is a different outcome. Fully retrospective completed-stay summarization using finalized records and no pre-event clinical forecast may receive NA for a pre-event input-availability audit; dynamic diagnosis/prognosis and prospective-use claims retain applicability. Known outcome intentionally supplied for retrospective explanation does not receive prediction-performance credit. Event-dependent asymmetric histories or incompatible observation-window descriptions are unresolved, not automatically demonstrated leakage.

External_data concerns independently sourced evaluation data, regardless of local adaptation. Internal clinical arms remain applicable and receive NR/explicit N when external evaluation is absent. MIMIC-version comparisons with unverified overlap remain U where independence is claimed or relevant. Frozen_transfer is separate: NA for a non-transfer internal arm or explicitly separately developed external system, N when an actual attempted transfer explicitly required changes, U if the source–target pathway is ambiguous, Y only for demonstrated unchanged complete-system transfer. Independent investigators are recorded separately.

## Performance endpoints and clinical content

Keep all quantitative measures attached to their exact task/cohort/endpoint. The broad auroc indicator may include ROC analysis of confidence detecting diagnostic correctness, but this must be labelled **correctness-detection AUROC**, counted separately from disease/outcome discrimination in synthesis, and never described as disease AUROC. Graphical presence of an evaluation can be Y even if exact plotted numbers cannot be read reliably; uncertain numerical values remain U.

Brier/ECE/plots qualify as calibration assessment methods, not proof of good calibration. The statistical_uncertainty flag records uncertainty reporting with its methods and unit limitations; it is not a formal judgment that the analysis is statistically valid. Display uncertainty type and missing clustering assumptions explicitly.

Generated clinical summaries, rationales and clinical intermediate representations retain factuality/omission applicability even when a downstream classifier consumes them. Pure latent yes/no severity features and rule-based input serialization may be NA for narrative-content checks. Factuality and clinically important omissions are distinct. Concept-overlap metrics alone do not establish a clinical omission assessment; use NR for that specific assessment, preserving the proxy in R04. Qualitative suspected omissions without a systematic denominator may be U. Numerical contradictions do not erase the presence of an evaluated method: keep method flag Y where justified, preserve literal result values and flag the conflict rather than repair it.

## Robustness subtypes and subgroups

Qualifying robustness tests include specified patient-input/noise/missingness perturbations, prompt/context order or length sensitivity, context filtering/compression consequences (K04), clinical domain/condition shifts, and operational inference/precision sensitivity when the same clinical task has outcome results. Preserve each subtype. Ordinary backbone/component substitutions and reduced-training-set learning curves alone do not qualify. Do not describe precision sensitivity as patient-input robustness. Care-unit comparisons intended as clinical case-mix assessment can qualify as observed subgroup performance when actual stratified outcomes are reported; distinguish them from demographic fairness. Cohort demographics alone and demographic counterfactual tests alone do not qualify. Never propagate a subgroup or stress result into an arm omitted from the test.

## Judges and artifact audit

Automated clinical-quality judgments include clinical fuzzy diagnosis matching as well as LLM judges where they underpin clinical-quality conclusions. Human validation is applicable to those judgments. A representative paired human comparison can be Y; targeted review of selected errors is partial/U. Human annotation used only for training/retrieval construction is not human evaluation of final outputs. Model-based training-case screening alone does not trigger final-output judge validation.

A generic repository or README does not establish cohort, inference or evaluation script availability. Inspect actual stage contents and retain commit/date/scope; this establishes accessible implementation content, not a successful rerun. Planned release with no identifiable current implementation source is NR for verified accessibility, with planned status retained; a known relevant source that cannot be retrieved/inspected is UA. A cache failure alone does not prove an inaccessible repository N. Record all material source attempts and avoid patient-level prediction downloads for this audit.

## Parent synthesis requirements

Count articles once when at least one applicable experiment meets a criterion; also show experiment coverage. Keep Y/N/NR/U/UA/NA separate, unknown applicability and denominator ranges explicit, and the broad AUROC and robustness subtypes interpretable. Reporting completeness, empirical evaluation and inspected artifact availability remain separate tables. Preserve cohort membership concerns and source version differences. No pooled model ranking, summed shared patient counts, formal risk-of-bias inference or safety certification is supported.

## Main synthesis scope versus linked comparator records

Retain pure non-LLM upstream/comparator evaluations as contextual linked records. Main LLM-system coverage denominators use evaluations involving an LLM system or its generated/intermediate clinical content. Pure non-LLM components do not make a narrative-only LLM's probability calibration applicable and do not supply LLM performance credit. Keep complete all-linked matrices and an explicitly labelled sensitivity table. Record each exclusion from the primary evaluation denominator in experiment_scope_decisions.json; no included article is removed. This applies the existing model-role distinction to synthesis, without altering per-experiment evidence codes or choosing records by their results.

## Medication interaction proxy clarification before synthesis

For clinical_errors, a potential drug–drug interaction rate alone does not establish assessment of clinically consequential prescribing errors. Preserve its formula, denominator and values as a safety-sensitive proxy. Use U when simultaneous exposure, consequential contraindication severity or clinical adjudication is unresolved; an interaction can be clinically necessary or sequential. Do not label this proxy as observed patient harm or a harmful-prescription incidence. Apply the same interpretation across medication studies. Parent decision P011 records harmonization of J0113 with SC0007 on 17 October 2026 before full-corpus synthesis; no numerical results were changed.
