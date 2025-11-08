# Knowledge Pipeline
> You can now convert your existing knowledge base to use the Knowledge Pipeline for document processing 
- Covert cannot be undone
- allow access to plugins from Dify marketplace
# Documents

max chunk size: < 4000
chunk overlap: 10%-25% of max chunk size

name is not unique: different documents can have same name


# Dataset 
Native Data source
- import from file
  - Max 5 in a batch
  - Max 15 MB each file
- Sync from Notion
- Sync from website (crawler)
  - Jina Reader: 20 subpages
    - cannot read this page
    - dedup: for different urls under same domain, top 20 Subpages is always the same  
  - Firecrawl


provision only
- Notion and website data source cannot be used after provision.
  - solution:　convert this dataset to pipeline mode 