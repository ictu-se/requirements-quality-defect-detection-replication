# Defect Detection Model Ranking

Selection score combines micro-F1, macro-F1, severity-weighted F1, any-defect accuracy, parse rate, exact match, span support, false alarms, missed defects, missed major/critical defects, Brier score, and ECE.

## Best Condition Per Model

| Rank | Model | Best condition | Family | Type | Score | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec | Why |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | gemma3:4b | rubric_guided |  |  | 43.094 | 0.286 | 0.183 | 0.301 | 0.850 | 0.133 | 0.008 | 0.116 | 3.542 | good any-defect accuracy; low missed-defect rate; well-grounded spans; well-calibrated confidence |
| 2 | qwen2.5-coder:32b | rubric_guided | Qwen2.5-Coder | code-specialized | 41.798 | 0.304 | 0.208 | 0.350 | 0.742 | 0.025 | 0.050 | 0.168 | 22.593 | good any-defect accuracy; low false-alarm rate; well-grounded spans; slow runtime; largest installed local code-specialized baseline |
| 3 | qwen2.5vl:3b | zero_shot |  |  | 41.399 | 0.340 | 0.092 | 0.363 | 0.833 | 0.117 | 0.017 | 0.120 | 1.812 | poor minority-defect coverage; good any-defect accuracy; low missed-defect rate; well-calibrated confidence; fast runtime |
| 4 | qwen3:4b | zero_shot |  |  | 40.316 | 0.295 | 0.146 | 0.336 | 0.717 | 0.050 | 0.033 | 0.132 | 49.830 | good any-defect accuracy; low false-alarm rate; well-grounded spans; well-calibrated confidence; slow runtime |
| 5 | qwen2.5-coder:1.5b | rubric_guided |  |  | 38.744 | 0.228 | 0.147 | 0.240 | 0.850 | 0.150 | 0.000 | 0.136 | 0.998 | good any-defect accuracy; low missed-defect rate; well-calibrated confidence; fast runtime |
| 6 | llama3.2:3b | zero_shot |  |  | 38.569 | 0.306 | 0.115 | 0.333 | 0.792 | 0.142 | 0.000 | 0.154 | 0.848 | good any-defect accuracy; low missed-defect rate; fast runtime |
| 7 | qwen2.5-coder:14b | rubric_guided |  |  | 18.409 | 0.126 | 0.096 | 0.154 | 0.308 | 0.017 | 0.258 | 0.152 | 4.810 | poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans |
| 8 | qwen2.5-coder:7b | zero_shot |  |  | 13.746 | 0.073 | 0.039 | 0.092 | 0.275 | 0.008 | 0.283 | 0.155 | 2.140 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; fast runtime |
| 9 | qwen2.5:3b | rubric_guided |  |  | 9.483 | 0.037 | 0.016 | 0.029 | 0.200 | 0.025 | 0.350 | 0.145 | 1.125 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; well-calibrated confidence; fast runtime |
| 10 | deepseek-coder:6.7b | zero_shot | DeepSeek-Coder | code-specialized | 6.433 | 0.005 | 0.003 | 0.004 | 0.158 | 0.000 | 0.358 | 0.150 | 1.662 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; fast runtime; non-Qwen code-specialized baseline |
| 11 | granite3.2-vision:latest | zero_shot |  |  | 3.534 | 0.026 | 0.011 | 0.029 | 0.158 | 0.008 | 0.350 | 0.127 | 0.922 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-calibrated confidence; fast runtime |
| 12 | qwen2.5-coder:3b | rubric_guided |  |  | 1.943 | 0.000 | 0.000 | 0.000 | 0.150 | 0.000 | 0.358 | 0.150 | 0.868 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; fast runtime |

## All Model-Condition Rows

| Rank | Model | Condition | Score | Parse | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | gemma3:4b | rubric_guided | 43.094 | 0.983 | 0.286 | 0.183 | 0.301 | 0.850 | 0.133 | 0.008 | 0.116 | 3.542 |
| 2 | gemma3:4b | zero_shot | 42.062 | 0.992 | 0.279 | 0.173 | 0.291 | 0.825 | 0.142 | 0.017 | 0.123 | 4.132 |
| 3 | qwen2.5-coder:32b | rubric_guided | 41.798 | 1.000 | 0.304 | 0.208 | 0.350 | 0.742 | 0.025 | 0.050 | 0.168 | 22.593 |
| 4 | qwen2.5vl:3b | zero_shot | 41.399 | 0.967 | 0.340 | 0.092 | 0.363 | 0.833 | 0.117 | 0.017 | 0.120 | 1.812 |
| 5 | qwen2.5vl:3b | rubric_guided | 40.337 | 0.958 | 0.335 | 0.091 | 0.356 | 0.817 | 0.108 | 0.042 | 0.144 | 1.934 |
| 6 | qwen3:4b | zero_shot | 40.316 | 1.000 | 0.295 | 0.146 | 0.336 | 0.717 | 0.050 | 0.033 | 0.132 | 49.830 |
| 7 | qwen3:4b | rubric_guided | 39.145 | 1.000 | 0.283 | 0.104 | 0.306 | 0.742 | 0.058 | 0.042 | 0.143 | 44.082 |
| 8 | qwen2.5-coder:32b | zero_shot | 38.844 | 1.000 | 0.276 | 0.211 | 0.325 | 0.675 | 0.025 | 0.067 | 0.162 | 13.641 |
| 9 | qwen2.5-coder:1.5b | rubric_guided | 38.744 | 1.000 | 0.228 | 0.147 | 0.240 | 0.850 | 0.150 | 0.000 | 0.136 | 0.998 |
| 10 | llama3.2:3b | zero_shot | 38.569 | 1.000 | 0.306 | 0.115 | 0.333 | 0.792 | 0.142 | 0.000 | 0.154 | 0.848 |
| 11 | llama3.2:3b | rubric_guided | 38.411 | 1.000 | 0.299 | 0.101 | 0.333 | 0.792 | 0.133 | 0.000 | 0.130 | 0.852 |
| 12 | qwen2.5-coder:1.5b | zero_shot | 36.620 | 0.992 | 0.181 | 0.130 | 0.194 | 0.858 | 0.142 | 0.000 | 0.133 | 1.007 |
| 13 | qwen2.5-coder:14b | rubric_guided | 18.409 | 1.000 | 0.126 | 0.096 | 0.154 | 0.308 | 0.017 | 0.258 | 0.152 | 4.810 |
| 14 | qwen2.5-coder:14b | zero_shot | 18.144 | 1.000 | 0.117 | 0.085 | 0.144 | 0.317 | 0.017 | 0.258 | 0.150 | 4.407 |
| 15 | qwen2.5-coder:7b | zero_shot | 13.746 | 1.000 | 0.073 | 0.039 | 0.092 | 0.275 | 0.008 | 0.283 | 0.155 | 2.140 |
| 16 | qwen2.5-coder:7b | rubric_guided | 12.781 | 1.000 | 0.063 | 0.035 | 0.077 | 0.258 | 0.008 | 0.300 | 0.154 | 2.198 |
| 17 | qwen2.5:3b | rubric_guided | 9.483 | 0.992 | 0.037 | 0.016 | 0.029 | 0.200 | 0.025 | 0.350 | 0.145 | 1.125 |
| 18 | qwen2.5:3b | zero_shot | 9.222 | 0.992 | 0.032 | 0.014 | 0.025 | 0.200 | 0.008 | 0.350 | 0.147 | 1.380 |
| 19 | deepseek-coder:6.7b | zero_shot | 6.433 | 1.000 | 0.005 | 0.003 | 0.004 | 0.158 | 0.000 | 0.358 | 0.150 | 1.662 |
| 20 | deepseek-coder:6.7b | rubric_guided | 6.421 | 1.000 | 0.005 | 0.003 | 0.004 | 0.158 | 0.000 | 0.358 | 0.151 | 1.605 |
| 21 | granite3.2-vision:latest | zero_shot | 3.534 | 0.992 | 0.026 | 0.011 | 0.029 | 0.158 | 0.008 | 0.350 | 0.127 | 0.922 |
| 22 | granite3.2-vision:latest | rubric_guided | 3.200 | 1.000 | 0.011 | 0.005 | 0.012 | 0.167 | 0.008 | 0.350 | 0.135 | 0.855 |
| 23 | qwen2.5-coder:3b | rubric_guided | 1.943 | 1.000 | 0.000 | 0.000 | 0.000 | 0.150 | 0.000 | 0.358 | 0.150 | 0.868 |
| 24 | qwen2.5-coder:3b | zero_shot | 1.943 | 1.000 | 0.000 | 0.000 | 0.000 | 0.150 | 0.000 | 0.358 | 0.150 | 0.845 |
