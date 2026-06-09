# Defect Detection Model Ranking

Selection score combines micro-F1, macro-F1, severity-weighted F1, any-defect accuracy, parse rate, exact match, span support, false alarms, missed defects, missed major/critical defects, Brier score, and ECE.

## Best Condition Per Model

| Rank | Model | Best condition | Family | Type | Score | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec | Why |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | qwen2.5-coder:32b | rubric_guided | Qwen2.5-Coder | code-specialized | 38.316 | 0.247 | 0.220 | 0.260 | 0.672 | 0.175 | 0.036 | 0.284 | 21.777 | well-grounded spans; slow runtime; largest installed local code-specialized baseline |
| 2 | gemma3:4b | zero_shot | Gemma 3 | general-instruct | 30.465 | 0.113 | 0.146 | 0.131 | 0.657 | 0.323 | 0.007 | 0.274 | 9.522 | high false-alarm rate; low missed-defect rate; well-grounded spans; Google-family baseline |
| 3 | qwen3:4b | zero_shot | Qwen3 | general-instruct | 28.109 | 0.079 | 0.103 | 0.094 | 0.631 | 0.223 | 0.052 | 0.277 | 48.734 | weak defect-type discrimination; well-grounded spans; slow runtime; newer general Qwen-family baseline |
| 4 | qwen2.5-coder:14b | rubric_guided | Qwen2.5-Coder | code-specialized | 28.107 | 0.187 | 0.112 | 0.175 | 0.478 | 0.033 | 0.078 | 0.337 | 4.858 | low false-alarm rate; misses many defects; well-grounded spans; poor confidence calibration; larger code baseline |
| 5 | qwen2.5-coder:1.5b | zero_shot | Qwen2.5-Coder | code-specialized | 28.049 | 0.124 | 0.063 | 0.130 | 0.657 | 0.334 | 0.003 | 0.238 | 0.966 | poor minority-defect coverage; high false-alarm rate; low missed-defect rate; fast runtime; fast small code baseline |
| 6 | qwen2.5vl:3b | zero_shot | Qwen2.5-VL | vision-language | 24.625 | 0.057 | 0.011 | 0.064 | 0.682 | 0.297 | 0.011 | 0.249 | 1.835 | weak defect-type discrimination; poor minority-defect coverage; low missed-defect rate; fast runtime; Qwen multimodal robustness baseline |
| 7 | llama3.2:3b | zero_shot | Llama 3.2 | general-instruct | 23.090 | 0.064 | 0.068 | 0.071 | 0.638 | 0.321 | 0.021 | 0.265 | 0.839 | weak defect-type discrimination; poor minority-defect coverage; high false-alarm rate; low missed-defect rate; fast runtime; non-Qwen general baseline |
| 8 | qwen2.5-coder:7b | zero_shot | Qwen2.5-Coder | code-specialized | 21.798 | 0.052 | 0.065 | 0.052 | 0.486 | 0.026 | 0.108 | 0.344 | 2.201 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; poor confidence calibration; fast runtime; mid-size code baseline |
| 9 | qwen2.5:3b | rubric_guided | Qwen2.5 | general-instruct | 19.776 | 0.029 | 0.026 | 0.037 | 0.409 | 0.015 | 0.091 | 0.239 | 1.106 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; fast runtime; general Qwen baseline |
| 10 | deepseek-coder:6.7b | rubric_guided | DeepSeek-Coder | code-specialized | 14.898 | 0.016 | 0.016 | 0.025 | 0.357 | 0.000 | 0.119 | 0.344 | 1.612 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; poor confidence calibration; fast runtime; non-Qwen code-specialized baseline |
| 11 | qwen2.5-coder:3b | rubric_guided | Qwen2.5-Coder | code-specialized | 14.665 | 0.000 | 0.000 | 0.000 | 0.341 | 0.002 | 0.126 | 0.342 | 0.868 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; well-grounded spans; poor confidence calibration; fast runtime; small code baseline |
| 12 | granite3.2-vision:latest | rubric_guided | Granite 3.2 Vision | vision-language | 11.851 | 0.011 | 0.009 | 0.009 | 0.354 | 0.005 | 0.121 | 0.310 | 0.871 | weak defect-type discrimination; poor minority-defect coverage; low false-alarm rate; misses many defects; poor confidence calibration; fast runtime; IBM-family multimodal robustness baseline |

## All Model-Condition Rows

| Rank | Model | Condition | Score | Parse | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | qwen2.5-coder:32b | rubric_guided | 38.316 | 0.995 | 0.247 | 0.220 | 0.260 | 0.672 | 0.175 | 0.036 | 0.284 | 21.777 |
| 2 | qwen2.5-coder:32b | zero_shot | 36.975 | 0.995 | 0.220 | 0.219 | 0.232 | 0.661 | 0.153 | 0.042 | 0.286 | 14.330 |
| 3 | gemma3:4b | zero_shot | 30.465 | 0.989 | 0.113 | 0.146 | 0.131 | 0.657 | 0.323 | 0.007 | 0.274 | 9.522 |
| 4 | gemma3:4b | rubric_guided | 29.013 | 0.989 | 0.101 | 0.112 | 0.122 | 0.649 | 0.336 | 0.005 | 0.272 | 3.452 |
| 5 | qwen3:4b | zero_shot | 28.109 | 1.000 | 0.079 | 0.103 | 0.094 | 0.631 | 0.223 | 0.052 | 0.277 | 48.734 |
| 6 | qwen2.5-coder:14b | rubric_guided | 28.107 | 0.998 | 0.187 | 0.112 | 0.175 | 0.478 | 0.033 | 0.078 | 0.337 | 4.858 |
| 7 | qwen2.5-coder:1.5b | zero_shot | 28.049 | 0.992 | 0.124 | 0.063 | 0.130 | 0.657 | 0.334 | 0.003 | 0.238 | 0.966 |
| 8 | qwen2.5-coder:14b | zero_shot | 27.431 | 0.997 | 0.165 | 0.103 | 0.160 | 0.483 | 0.028 | 0.077 | 0.336 | 4.413 |
| 9 | qwen2.5-coder:1.5b | rubric_guided | 27.216 | 0.995 | 0.106 | 0.062 | 0.115 | 0.661 | 0.336 | 0.002 | 0.240 | 0.947 |
| 10 | qwen3:4b | rubric_guided | 26.855 | 1.000 | 0.066 | 0.069 | 0.064 | 0.631 | 0.212 | 0.054 | 0.279 | 45.131 |
| 11 | qwen2.5vl:3b | zero_shot | 24.625 | 0.977 | 0.057 | 0.011 | 0.064 | 0.682 | 0.297 | 0.011 | 0.249 | 1.835 |
| 12 | qwen2.5vl:3b | rubric_guided | 24.356 | 0.974 | 0.056 | 0.011 | 0.062 | 0.679 | 0.287 | 0.016 | 0.248 | 1.951 |
| 13 | llama3.2:3b | zero_shot | 23.090 | 0.995 | 0.064 | 0.068 | 0.071 | 0.638 | 0.321 | 0.021 | 0.265 | 0.839 |
| 14 | llama3.2:3b | rubric_guided | 22.800 | 0.995 | 0.066 | 0.071 | 0.076 | 0.623 | 0.323 | 0.029 | 0.270 | 0.856 |
| 15 | qwen2.5-coder:7b | zero_shot | 21.798 | 1.000 | 0.052 | 0.065 | 0.052 | 0.486 | 0.026 | 0.108 | 0.344 | 2.201 |
| 16 | qwen2.5-coder:7b | rubric_guided | 21.568 | 1.000 | 0.061 | 0.072 | 0.064 | 0.462 | 0.023 | 0.109 | 0.343 | 2.270 |
| 17 | qwen2.5:3b | rubric_guided | 19.776 | 0.992 | 0.029 | 0.026 | 0.037 | 0.409 | 0.015 | 0.091 | 0.239 | 1.106 |
| 18 | qwen2.5:3b | zero_shot | 19.477 | 0.992 | 0.030 | 0.028 | 0.035 | 0.405 | 0.002 | 0.100 | 0.241 | 1.337 |
| 19 | deepseek-coder:6.7b | rubric_guided | 14.898 | 1.000 | 0.016 | 0.016 | 0.025 | 0.357 | 0.000 | 0.119 | 0.344 | 1.612 |
| 20 | qwen2.5-coder:3b | rubric_guided | 14.665 | 1.000 | 0.000 | 0.000 | 0.000 | 0.341 | 0.002 | 0.126 | 0.342 | 0.868 |
| 21 | qwen2.5-coder:3b | zero_shot | 14.664 | 1.000 | 0.000 | 0.000 | 0.000 | 0.341 | 0.002 | 0.126 | 0.342 | 0.830 |
| 22 | deepseek-coder:6.7b | zero_shot | 14.425 | 0.998 | 0.012 | 0.012 | 0.018 | 0.359 | 0.000 | 0.117 | 0.345 | 1.683 |
| 23 | granite3.2-vision:latest | rubric_guided | 11.851 | 0.997 | 0.011 | 0.009 | 0.009 | 0.354 | 0.005 | 0.121 | 0.310 | 0.871 |
| 24 | granite3.2-vision:latest | zero_shot | 11.568 | 0.995 | 0.011 | 0.006 | 0.009 | 0.354 | 0.003 | 0.119 | 0.298 | 0.930 |
