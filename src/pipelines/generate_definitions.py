from src.llm_agents.scrapers.playwright_sync import get_paragraphs
from src.llm_agents.sources.wikipedia import WikipediaSource
from src.llm_agents.extractors.cohere_definition_extractor import cohereDefinitionExtractor
from src.neo4j_db.neo4j_connection import Neo4jConnection
from src.llm_agents.classifiers.classify_definition import classify_definition

def generate_definitions(worker_id="", domain="", sources=[{"type": "", "content": ""}], words=[]):
    for source in sources:
        if source["type"] == "url":
            input_paragraphs = get_paragraphs(source["content"])
        elif source["type"] == "wikipedia":
            wiki = WikipediaSource(domain=domain, n_docs=1)
            input_paragraphs = wiki.get_content()
        elif source["type"] == "file":
            input_paragraphs = source["content"]
        
        extractor = cohereDefinitionExtractor()

        conn = Neo4jConnection(uri='neo4j+s://5e2c94ef.databases.neo4j.io', user='neo4j', pwd='E53hCDHJjVnO8aTLMejfxtmz1G7q9LplVVO6K5L6drg')

        for paragraph in input_paragraphs:
            for word in words:
                if word in paragraph:
                    if classify_definition(paragraph):
                        extracted_text = extractor.extract(paragraph, word)
                        conn.add_definition(worker_id, word, extracted_text, domain)

        conn.close()
