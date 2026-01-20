# Model Provider

## Hugging Face Model
Error: `Model Qwen/Qwen3-VL-8B-Instruct is not a valid task, must be one of ('text2text-generation', 'text-generation').`
- Cause: Qwen/Qwen3-VL-8B-Instruct 是一个多模态模型（Vision-Language），没有 text-generation 或 text2text-generation 标签
