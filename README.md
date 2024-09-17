# OTSD: Open-Target Stance Detection

## Abstract

Stance detection (SD) identifies a text's position towards a target, typically labeled as favor, against, or none. We introduce Open-Target Stance Detection (OTSD), the most realistic task where targets are neither seen during training nor provided as input. We evaluate Large Language Models (LLMs) GPT-4o, GPT-3.5, Llama-3, and Mistral, comparing their performance to the only existing work, Target-Stance Extraction (TSE), which benefits from predefined targets. Unlike TSE, OTSD removes the dependency of a predefined list, making target generation and evaluation more challenging. We also provide a metric for evaluating target quality that correlates well with human judgment. Our experiments reveal that LLMs outperform TSE in target generation when the real target is explicitly and not explicitly mentioned in the text. Likewise, for stance detection, LLMs excel in explicit cases with comparable performance in non-explicit in general.

## Data

The `data` folder is strucutred in the following way:

- `tse`: output files (explicit, non-explicit) extracted from TSE zero-shot dataset
- `vast`: output files (explicit, non-explicit) extracted from VAST original dataset

## BTSD Checkpoint

We follow same codebase as TSE and follow their training configuration and make the trained BTSD model publicly available [here](https://usherbrooke-my.sharepoint.com/:u:/g/personal/akaa2803_usherbrooke_ca/Eb03gh9Srk9CtQGcmZNpJf4BKZPtX_0brTs1bOiAb5rxXg?e=BwexQy).