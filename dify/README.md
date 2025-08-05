[wiki](https://github.com/davidkhala/AI/wiki/LangGenius#dify)


# Dify app
## type: completion
- 只进行一次问答：没有system prompt
- 支持多模型并发，适合用于模型对比评估



# Knowledge
Data source 只支持
- import from file
- Sync from Notion
- Sync from website (选择爬虫provider)
  - Jina Reader
  - Firecrawl

# Limit

Immutable
- 在 Workflow 的某个节点（比如某个 LLM 步骤）中，一旦设置了具体的模型，就不能更改了