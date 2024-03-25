from domain.entities import QueryInputSchema
from pathway.stdlib.ml.index import KNNIndex
from domain.entities import QueryInputSchema
from utils.wikipedia_connector import *
from utils.arxiv_connector import *
from pathway.xpacks.llm.splitters import TokenCountSplitter
from pathway.xpacks.llm.parsers import ParseUnstructured
from config.application_config import ApplicationConfig
from domain.entities import QueryInputSchema, DataInputSchema

class DocumentProcessingPipeLine:
    def __init__(self, google_drive_adapter, open_ai_embedder):
        self.google_drive_adapter = google_drive_adapter
        self.embed_text = open_ai_embedder

    def execute(self, object_id):
        # 1. Read files from Google Drive
        files = self.google_drive_adapter.read_files(object_id)

        parser = ParseUnstructured()

        documents = files.select(texts=parser(pw.this.data))
        documents = documents.flatten(pw.this.texts)
        documents = documents.select(texts=pw.this.texts[0])
    
        # Split documents into chunks
        splitter = TokenCountSplitter()
        documents = documents.select(chunks=splitter(pw.this.texts, min_tokens=80, max_tokens=200))
        documents = documents.flatten(pw.this.chunks).select(chunk=pw.this.chunks[0])
        enriched_documents = documents + documents.select(vector_data=self.embed_text(pw.this.chunk))

        query, response_writer = pw.io.http.rest_connector(
        host=ApplicationConfig.PATHWAY_REST_CONNECTOR_HOST,
        port=ApplicationConfig.PATHWAY_REST_CONNECTOR_PORT,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
        delete_completed_queries=False,
    )
        
        # Extract keywords for Wikipedia queries
        query = query + query.select(keywords=extract_key_terms(pw.this.query))

        # # get latest research papers arxiv api as per the search keywords and context keywords
        # get_latest_research_papers(pw.this.search_keywords, pw.this.context_keywords)

        articles_research_paper_ingestion  = pw.io.jsonlines.read(
        "./data",
        schema=DataInputSchema,
        mode="streaming"
        )

        # query.promise_universes_are_equal(research_paper_ingestion)
        content_enrichment = articles_research_paper_ingestion.select(chunk=pw.this.summary)
        content_enrichment = content_enrichment + content_enrichment.select(vector_data=self.embed_text(pw.this.chunk))

        query = query + query.select(vector=self.embed_text(pw.this.query))
        wiki_content = query + query.select(wiki_content=enrich_with_wikipedia(pw.this.keywords))
        wiki_content_chunk = query + wiki_content.select(wiki_chunks=splitter(pw.this.wiki_content, min_tokens=40, max_tokens=180))
        wiki_content_f = wiki_content_chunk.flatten(pw.this.wiki_chunks).select(chunk=pw.this.wiki_chunks[0])
        wiki_content_f = wiki_content_f + wiki_content_f.select(vector_data=self.embed_text(pw.this.chunk))
        content_enrichment.promise_universes_are_disjoint(wiki_content_f)
        combined_documents = content_enrichment.concat(wiki_content_f)
        combined_documents.promise_universes_are_disjoint(enriched_documents)
        combined_documents_final  = combined_documents.concat(enriched_documents)
        pw.io.csv.write(combined_documents_final , "output_stream_final.csv")
        # Create a KNN index using the vector data from enriched documents with Wikipedia content
        index = KNNIndex(
           combined_documents_final.vector_data,combined_documents_final, n_dimensions=1536
        )
        
        # Ensure the query includes difficulty level and context keywords for each entry
        query_context = query + index.get_nearest_items(query.vector, k=3, collapse_rows=True).select(
            documents_list=pw.this.chunk
    )

        return  query_context, response_writer
    

