# Defect Detection Summary

| Model | Condition | N | Parse | Any acc | Micro F1 | Macro F1 | Sev F1 | False alarm | Missed major | Span support | Brier | ECE | Mean sec |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gemma3:4b | rubric_guided | 613 | 0.989 | 0.649 | 0.101 | 0.112 | 0.122 | 0.336 | 0.005 | 0.861 | 0.272 | 0.207 | 3.452 |
| gemma3:4b | zero_shot | 613 | 0.989 | 0.657 | 0.113 | 0.146 | 0.131 | 0.323 | 0.007 | 0.881 | 0.274 | 0.198 | 9.522 |
| granite3.2-vision:latest | rubric_guided | 613 | 0.997 | 0.354 | 0.011 | 0.009 | 0.009 | 0.005 | 0.121 | 0.000 | 0.310 | 0.584 | 0.871 |
| granite3.2-vision:latest | zero_shot | 613 | 0.995 | 0.354 | 0.011 | 0.006 | 0.009 | 0.003 | 0.119 | 0.000 | 0.298 | 0.583 | 0.930 |
| llama3.2:3b | rubric_guided | 613 | 0.995 | 0.623 | 0.066 | 0.071 | 0.076 | 0.323 | 0.029 | 0.052 | 0.270 | 0.189 | 0.856 |
| llama3.2:3b | zero_shot | 613 | 0.995 | 0.638 | 0.064 | 0.068 | 0.071 | 0.321 | 0.021 | 0.039 | 0.265 | 0.182 | 0.839 |
| qwen2.5-coder:1.5b | rubric_guided | 613 | 0.995 | 0.661 | 0.106 | 0.062 | 0.115 | 0.336 | 0.002 | 0.405 | 0.240 | 0.126 | 0.947 |
| qwen2.5-coder:1.5b | zero_shot | 613 | 0.992 | 0.657 | 0.124 | 0.063 | 0.130 | 0.334 | 0.003 | 0.429 | 0.238 | 0.121 | 0.966 |
| qwen2.5-coder:14b | rubric_guided | 613 | 0.998 | 0.478 | 0.187 | 0.112 | 0.175 | 0.033 | 0.078 | 0.975 | 0.337 | 0.501 | 4.858 |
| qwen2.5-coder:14b | zero_shot | 613 | 0.997 | 0.483 | 0.165 | 0.103 | 0.160 | 0.028 | 0.077 | 0.983 | 0.336 | 0.503 | 4.413 |
| qwen2.5-coder:3b | rubric_guided | 613 | 1.000 | 0.341 | 0.000 | 0.000 | 0.000 | 0.002 | 0.126 | 1.000 | 0.342 | 0.658 | 0.868 |
| qwen2.5-coder:3b | zero_shot | 613 | 1.000 | 0.341 | 0.000 | 0.000 | 0.000 | 0.002 | 0.126 | 1.000 | 0.342 | 0.659 | 0.830 |
| qwen2.5-coder:7b | rubric_guided | 613 | 1.000 | 0.462 | 0.061 | 0.072 | 0.064 | 0.023 | 0.109 | 0.900 | 0.343 | 0.542 | 2.270 |
| qwen2.5-coder:7b | zero_shot | 613 | 1.000 | 0.486 | 0.052 | 0.065 | 0.052 | 0.026 | 0.108 | 0.912 | 0.344 | 0.521 | 2.201 |
| qwen2.5:3b | rubric_guided | 613 | 0.992 | 0.409 | 0.029 | 0.026 | 0.037 | 0.015 | 0.091 | 0.949 | 0.239 | 0.345 | 1.106 |
| qwen2.5:3b | zero_shot | 613 | 0.992 | 0.405 | 0.030 | 0.028 | 0.035 | 0.002 | 0.100 | 0.900 | 0.241 | 0.350 | 1.337 |
| qwen2.5vl:3b | rubric_guided | 613 | 0.974 | 0.679 | 0.056 | 0.011 | 0.062 | 0.287 | 0.016 | 0.392 | 0.248 | 0.169 | 1.951 |
| qwen2.5vl:3b | zero_shot | 613 | 0.977 | 0.682 | 0.057 | 0.011 | 0.064 | 0.297 | 0.011 | 0.413 | 0.249 | 0.160 | 1.835 |
| qwen3:4b | rubric_guided | 613 | 1.000 | 0.631 | 0.066 | 0.069 | 0.064 | 0.212 | 0.054 | 0.969 | 0.279 | 0.229 | 45.131 |
| qwen3:4b | zero_shot | 613 | 1.000 | 0.631 | 0.079 | 0.103 | 0.094 | 0.223 | 0.052 | 0.978 | 0.277 | 0.233 | 48.734 |

## By Source Type

| Model | Condition | Source type | Label source | N | Parse | Any-defect acc | Type F1 | False alarm | Missed defect |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gemma3:4b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 0.979 | 0.260 | 0.088 | 0.719 | 0.021 |
| gemma3:4b | rubric_guided | function_spec | test_oracle_derived | 200 | 0.995 | 0.715 | 0.023 | 0.280 | 0.005 |
| gemma3:4b | rubric_guided | issue_statement | rule_seeded | 96 | 0.969 | 0.583 | 0.118 | 0.354 | 0.062 |
| gemma3:4b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.625 | 0.000 | 0.375 | 0.000 |
| gemma3:4b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 1.000 | 0.344 | 0.000 | 0.000 |
| gemma3:4b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 0.800 | 0.600 | 0.000 | 0.400 | 0.000 |
| gemma3:4b | zero_shot | acceptance_criterion | rule_seeded | 96 | 0.979 | 0.260 | 0.131 | 0.719 | 0.021 |
| gemma3:4b | zero_shot | function_spec | test_oracle_derived | 200 | 0.995 | 0.715 | 0.017 | 0.280 | 0.005 |
| gemma3:4b | zero_shot | issue_statement | rule_seeded | 96 | 0.969 | 0.656 | 0.156 | 0.260 | 0.083 |
| gemma3:4b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.625 | 0.000 | 0.375 | 0.000 |
| gemma3:4b | zero_shot | synthetic_defect | synthetic_injected | 96 | 0.990 | 0.990 | 0.356 | 0.000 | 0.010 |
| gemma3:4b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.600 | 0.000 |
| granite3.2-vision:latest | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.000 | 0.281 |
| granite3.2-vision:latest | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.285 | 0.034 | 0.000 | 0.715 |
| granite3.2-vision:latest | rubric_guided | issue_statement | rule_seeded | 96 | 0.979 | 0.417 | 0.000 | 0.031 | 0.552 |
| granite3.2-vision:latest | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.375 | 0.000 | 0.000 | 0.625 |
| granite3.2-vision:latest | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.031 | 0.000 | 0.000 | 0.969 |
| granite3.2-vision:latest | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| granite3.2-vision:latest | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.000 | 0.281 |
| granite3.2-vision:latest | zero_shot | function_spec | test_oracle_derived | 200 | 0.995 | 0.285 | 0.031 | 0.000 | 0.715 |
| granite3.2-vision:latest | zero_shot | issue_statement | rule_seeded | 96 | 0.990 | 0.417 | 0.000 | 0.021 | 0.562 |
| granite3.2-vision:latest | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.375 | 0.000 | 0.000 | 0.625 |
| granite3.2-vision:latest | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.031 | 0.000 | 0.000 | 0.969 |
| granite3.2-vision:latest | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 0.800 | 0.600 | 0.000 | 0.000 | 0.400 |
| llama3.2:3b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.281 | 0.086 | 0.719 | 0.000 |
| llama3.2:3b | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.720 | 0.023 | 0.280 | 0.000 |
| llama3.2:3b | rubric_guided | issue_statement | rule_seeded | 96 | 0.979 | 0.438 | 0.070 | 0.260 | 0.302 |
| llama3.2:3b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.625 | 0.000 | 0.375 | 0.000 |
| llama3.2:3b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 0.990 | 0.958 | 0.202 | 0.000 | 0.042 |
| llama3.2:3b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.600 | 0.000 |
| llama3.2:3b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.281 | 0.058 | 0.719 | 0.000 |
| llama3.2:3b | zero_shot | function_spec | test_oracle_derived | 200 | 1.000 | 0.720 | 0.023 | 0.280 | 0.000 |
| llama3.2:3b | zero_shot | issue_statement | rule_seeded | 96 | 0.969 | 0.490 | 0.069 | 0.250 | 0.260 |
| llama3.2:3b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.625 | 0.000 | 0.375 | 0.000 |
| llama3.2:3b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 1.000 | 0.208 | 0.000 | 0.000 |
| llama3.2:3b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.600 | 0.000 |
| qwen2.5-coder:1.5b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.281 | 0.127 | 0.719 | 0.000 |
| qwen2.5-coder:1.5b | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.720 | 0.108 | 0.280 | 0.000 |
| qwen2.5-coder:1.5b | rubric_guided | issue_statement | rule_seeded | 96 | 0.979 | 0.625 | 0.142 | 0.354 | 0.021 |
| qwen2.5-coder:1.5b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 0.992 | 0.633 | 0.000 | 0.367 | 0.000 |
| qwen2.5-coder:1.5b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 1.000 | 0.142 | 0.000 | 0.000 |
| qwen2.5-coder:1.5b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.600 | 0.000 |
| qwen2.5-coder:1.5b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.281 | 0.110 | 0.719 | 0.000 |
| qwen2.5-coder:1.5b | zero_shot | function_spec | test_oracle_derived | 200 | 0.995 | 0.715 | 0.201 | 0.280 | 0.005 |
| qwen2.5-coder:1.5b | zero_shot | issue_statement | rule_seeded | 96 | 0.990 | 0.594 | 0.143 | 0.365 | 0.042 |
| qwen2.5-coder:1.5b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 0.983 | 0.642 | 0.000 | 0.358 | 0.000 |
| qwen2.5-coder:1.5b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 1.000 | 0.104 | 0.000 | 0.000 |
| qwen2.5-coder:1.5b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 0.800 | 0.600 | 0.000 | 0.400 | 0.000 |
| qwen2.5-coder:14b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.044 | 0.010 | 0.271 |
| qwen2.5-coder:14b | rubric_guided | function_spec | test_oracle_derived | 200 | 0.995 | 0.485 | 0.284 | 0.075 | 0.440 |
| qwen2.5-coder:14b | rubric_guided | issue_statement | rule_seeded | 96 | 1.000 | 0.406 | 0.031 | 0.042 | 0.552 |
| qwen2.5-coder:14b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.425 | 0.000 | 0.000 | 0.575 |
| qwen2.5-coder:14b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.354 | 0.308 | 0.000 | 0.646 |
| qwen2.5-coder:14b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5-coder:14b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.044 | 0.010 | 0.271 |
| qwen2.5-coder:14b | zero_shot | function_spec | test_oracle_derived | 200 | 0.990 | 0.480 | 0.223 | 0.065 | 0.455 |
| qwen2.5-coder:14b | zero_shot | issue_statement | rule_seeded | 96 | 1.000 | 0.417 | 0.032 | 0.031 | 0.552 |
| qwen2.5-coder:14b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.442 | 0.000 | 0.000 | 0.558 |
| qwen2.5-coder:14b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.365 | 0.336 | 0.000 | 0.635 |
| qwen2.5-coder:14b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5-coder:3b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.000 | 0.281 |
| qwen2.5-coder:3b | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.275 | 0.000 | 0.005 | 0.720 |
| qwen2.5-coder:3b | rubric_guided | issue_statement | rule_seeded | 96 | 1.000 | 0.385 | 0.000 | 0.000 | 0.615 |
| qwen2.5-coder:3b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.375 | 0.000 | 0.000 | 0.625 |
| qwen2.5-coder:3b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| qwen2.5-coder:3b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5-coder:3b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.000 | 0.281 |
| qwen2.5-coder:3b | zero_shot | function_spec | test_oracle_derived | 200 | 1.000 | 0.275 | 0.000 | 0.005 | 0.720 |
| qwen2.5-coder:3b | zero_shot | issue_statement | rule_seeded | 96 | 1.000 | 0.385 | 0.000 | 0.000 | 0.615 |
| qwen2.5-coder:3b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.375 | 0.000 | 0.000 | 0.625 |
| qwen2.5-coder:3b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| qwen2.5-coder:3b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5-coder:7b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.000 | 0.281 |
| qwen2.5-coder:7b | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.430 | 0.000 | 0.045 | 0.525 |
| qwen2.5-coder:7b | rubric_guided | issue_statement | rule_seeded | 96 | 1.000 | 0.458 | 0.060 | 0.052 | 0.490 |
| qwen2.5-coder:7b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.550 | 0.000 | 0.000 | 0.450 |
| qwen2.5-coder:7b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.156 | 0.252 | 0.000 | 0.844 |
| qwen2.5-coder:7b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5-coder:7b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.729 | 0.000 | 0.000 | 0.271 |
| qwen2.5-coder:7b | zero_shot | function_spec | test_oracle_derived | 200 | 1.000 | 0.465 | 0.000 | 0.055 | 0.480 |
| qwen2.5-coder:7b | zero_shot | issue_statement | rule_seeded | 96 | 1.000 | 0.438 | 0.045 | 0.052 | 0.510 |
| qwen2.5-coder:7b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.608 | 0.000 | 0.000 | 0.392 |
| qwen2.5-coder:7b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.177 | 0.230 | 0.000 | 0.823 |
| qwen2.5-coder:7b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5:3b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.656 | 0.000 | 0.073 | 0.271 |
| qwen2.5:3b | rubric_guided | function_spec | test_oracle_derived | 200 | 0.980 | 0.290 | 0.000 | 0.000 | 0.710 |
| qwen2.5:3b | rubric_guided | issue_statement | rule_seeded | 96 | 0.990 | 0.510 | 0.045 | 0.021 | 0.469 |
| qwen2.5:3b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.408 | 0.000 | 0.000 | 0.592 |
| qwen2.5:3b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.302 | 0.080 | 0.000 | 0.698 |
| qwen2.5:3b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5:3b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.719 | 0.000 | 0.010 | 0.271 |
| qwen2.5:3b | zero_shot | function_spec | test_oracle_derived | 200 | 0.980 | 0.285 | 0.000 | 0.000 | 0.715 |
| qwen2.5:3b | zero_shot | issue_statement | rule_seeded | 96 | 0.990 | 0.438 | 0.049 | 0.000 | 0.562 |
| qwen2.5:3b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.400 | 0.000 | 0.000 | 0.600 |
| qwen2.5:3b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.302 | 0.080 | 0.000 | 0.698 |
| qwen2.5:3b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.600 | 0.000 | 0.000 | 0.400 |
| qwen2.5vl:3b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.250 | 0.059 | 0.719 | 0.031 |
| qwen2.5vl:3b | rubric_guided | function_spec | test_oracle_derived | 200 | 0.960 | 0.750 | 0.017 | 0.245 | 0.005 |
| qwen2.5vl:3b | rubric_guided | issue_statement | rule_seeded | 96 | 0.979 | 0.719 | 0.112 | 0.156 | 0.125 |
| qwen2.5vl:3b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 0.967 | 0.642 | 0.000 | 0.350 | 0.008 |
| qwen2.5vl:3b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.958 | 0.128 | 0.000 | 0.042 |
| qwen2.5vl:3b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 0.600 | 0.800 | 0.000 | 0.200 | 0.000 |
| qwen2.5vl:3b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.281 | 0.058 | 0.719 | 0.000 |
| qwen2.5vl:3b | zero_shot | function_spec | test_oracle_derived | 200 | 0.975 | 0.735 | 0.017 | 0.260 | 0.005 |
| qwen2.5vl:3b | zero_shot | issue_statement | rule_seeded | 96 | 0.979 | 0.708 | 0.118 | 0.198 | 0.094 |
| qwen2.5vl:3b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 0.967 | 0.642 | 0.000 | 0.350 | 0.008 |
| qwen2.5vl:3b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.979 | 0.126 | 0.000 | 0.021 |
| qwen2.5vl:3b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 0.400 | 1.000 | 0.000 | 0.000 | 0.000 |
| qwen3:4b | rubric_guided | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.490 | 0.091 | 0.323 | 0.188 |
| qwen3:4b | rubric_guided | function_spec | test_oracle_derived | 200 | 1.000 | 0.680 | 0.035 | 0.255 | 0.065 |
| qwen3:4b | rubric_guided | issue_statement | rule_seeded | 96 | 1.000 | 0.469 | 0.044 | 0.062 | 0.469 |
| qwen3:4b | rubric_guided | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.567 | 0.000 | 0.342 | 0.092 |
| qwen3:4b | rubric_guided | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.927 | 0.190 | 0.000 | 0.073 |
| qwen3:4b | rubric_guided | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.200 | 0.400 |
| qwen3:4b | zero_shot | acceptance_criterion | rule_seeded | 96 | 1.000 | 0.521 | 0.108 | 0.344 | 0.135 |
| qwen3:4b | zero_shot | function_spec | test_oracle_derived | 200 | 1.000 | 0.680 | 0.018 | 0.250 | 0.070 |
| qwen3:4b | zero_shot | issue_statement | rule_seeded | 96 | 1.000 | 0.417 | 0.059 | 0.083 | 0.500 |
| qwen3:4b | zero_shot | layout_change_spec | mutation_description_derived | 120 | 1.000 | 0.608 | 0.000 | 0.375 | 0.017 |
| qwen3:4b | zero_shot | synthetic_defect | synthetic_injected | 96 | 1.000 | 0.896 | 0.268 | 0.000 | 0.104 |
| qwen3:4b | zero_shot | testing_rule_spec | rule_spec_derived | 5 | 1.000 | 0.400 | 0.000 | 0.200 | 0.400 |
