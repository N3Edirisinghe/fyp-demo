# Research Proposal → Platform Mapping

This document traces every element of the submitted proposal to where it is
implemented in this codebase, so a supervisor can audit the platform
against the proposal directly.

## Hypotheses & Study Design

The originally submitted proposal (Section 5) describes independent
tests of H1, H2, and H3. To run all three with the same 20 participants
efficiently, this platform uses a **3-session, within-subject design**:

| Session | Timing | Condition | Maps to proposal section |
|---|---|---|---|
| 1 | Week 1 | Voice input, live self-labeling, memory OFF | 5.1 (H1 ground truth collection) + 5.2 (H2 baseline/pre) |
| 2 | Week 2 | System recalls Session 1, memory ON | 5.2 (H2 post) + 5.3 (H3 integrated arm) |
| 3 | Week 2 (same visit as Session 2) | Plain memoryless, text-only, same LLM | 5.3 (H3 baseline arm) |

### Important deviations from a "textbook" between-subjects design

- **H2** is tested pre/post within the same participants (Session 1 vs.
  Session 2) rather than with two separate participant groups. This is a
  **repeated-measures/within-subject design**, consistent with the paired
  t-test / Wilcoxon signed-rank test specified in Section 5.5. Document
  this explicitly in your methodology chapter, and note the limitation:
  improvement from Session 1 to Session 2 could partly reflect familiarity
  with the system rather than memory alone. Mitigate by mentioning this
  explicitly as a limitation, or — if time allows — counterbalance order
  across a subset of participants.
- **H1 ground truth** comes from participant self-labeling immediately
  after each utterance in Session 1, *in addition to* offline evaluation
  against RAVDESS/TESS labels (see `training/scripts/evaluate_h1_classifiers.py`).
  Report both: the RAVDESS/TESS benchmark gives you a large, clean-label
  evaluation; the live self-labeled data gives you ecological validity on
  real (not acted) speech. Both matter for a strong defense.

## Objective → Code Mapping

| Proposal Objective | Implementation |
|---|---|
| Objective 1: voice emotion recognition model, benchmarked against text-only | `src/emotion/voice_emotion.py`, `src/emotion/text_emotion.py`, `training/notebooks/`, `training/scripts/evaluate_h1_classifiers.py` |
| Objective 2: structured long-term emotional memory + profiling | `src/memory/db.py`, `src/memory/vector_store.py`, `src/memory/profiling.py` |
| Objective 3: integrated system evaluated against conventional baseline | `src/conditions/memory_enabled.py`, `src/conditions/baseline.py`, `src/ui/pages/2_Session_2_*.py`, `src/ui/pages/3_Session_3_*.py` |

## Evaluation Metrics → Code Mapping

| Metric (Section 5.5) | Where computed |
|---|---|
| H1: Accuracy, Precision, Recall, F1 | `training/scripts/evaluate_h1_classifiers.py` (uses scikit-learn `classification_report`) |
| H2: Likert survey scores, memory-enabled vs. disabled | `surveys/h2_personalization_trust_companionship.md`, logged via `src/memory/db.py::log_survey_response`, exported via `src/ui/pages/4_Admin_Dashboard.py` |
| H3: satisfaction scores, integrated vs. baseline | `surveys/h3_satisfaction_survey.md`, same logging/export path |
| Paired t-test / Wilcoxon at α = 0.05 | Run offline (e.g. in a Jupyter notebook or R) on the exported CSVs from the admin dashboard — not embedded in the live app, to keep the app itself simple and auditable |

## What is intentionally NOT in this platform

Per Section 2 (Goal of the Project) of the proposal, the following are
explicitly out of scope and are not implemented here:
- Clinical mental health diagnosis
- Crisis intervention features
- Any claim of therapeutic equivalence

These exclusions should also be restated in your thesis's scope section
and in the participant-facing consent form.
