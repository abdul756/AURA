import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
sys.path.append(os.path.dirname(__file__))
import urllib.request
import feedparser
import json
from datetime import datetime
from config.application_config import ApplicationConfig
import pathway as pw
import spacy
import file_utils
import argparse



def save_articles(articles):
    """
    Saves articles to a JSONL file, appending new articles.
    Each line in the file is a separate JSON object.
    """
    JSON_FILE_PATH = file_utils.get_path(ApplicationConfig.DATA_DIR, "research_papers_12.jsonl")
    with open(JSON_FILE_PATH, 'a', encoding='utf-8') as file:
        for article in articles:
            json_line = json.dumps(article, ensure_ascii=False)
            file.write(json_line + '\n')
# @pw.udf
def get_latest_research_papers(topic, domain=None, max_results=50):
    base_url = 'http://export.arxiv.org/api/query?'
    desired_year = datetime.now().year

    # Format the search query
    if domain:
        # Split the domain into individual terms if necessary and encode them
        domain_terms = [urllib.parse.quote_plus(term.strip()) for term in domain.split(',')]
        # Join the domain terms with '+AND+'
        domain_query = '+OR+'.join(domain_terms)
        search_query = f'(all:{urllib.parse.quote_plus(topic)}+OR+ti:({domain_query}))'
    else:
        search_query = f'all:{urllib.parse.quote_plus(topic)}'

    # Construct the complete query URL
    query = f'search_query={search_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    response = urllib.request.urlopen(base_url + query).read()
    feed = feedparser.parse(response)

    # Open the file in append mode
    research_articles = []
    for entry in feed.entries:
        published_year = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ').year
        if published_year >= desired_year - 1:  # Current or previous year
            paper_details = {
                'arxiv_id': entry.id.split('/abs/')[-1],
                'published': entry.published,
                'title': entry.title,
                'summary': entry.summary
            }
            research_articles.append(paper_details)
    save_articles(research_articles)


nlp = spacy.load("en_core_web_sm")

def extract_search_keywords(question, domain, max_results):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(question)
    potential_keywords = []

    for ent in doc.ents:
        potential_keywords.append(ent.text.replace(" ", ""))

    for chunk in doc.noun_chunks:
        if not any(ent.text == chunk.text for ent in doc.ents):
            potential_keywords.append(chunk.text.replace(" ", ""))

    if potential_keywords:
        get_latest_research_papers(potential_keywords[-1], domain,  max_results)
    else:
         " "
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch the latest research papers based on a question.')
    parser.add_argument('question', type=str, help='The question to extract keywords from and search for related research papers.')
    parser.add_argument('--max_results', type=int, default=50, help='Maximum number of results to fetch (default is 50).')
    parser.add_argument('--domain', type=str, default=None, help='Optional: Specify a domain to narrow down the search (default is None).')

    args = parser.parse_args()
    
    extract_search_keywords(args.question, args.domain, args.max_results)
