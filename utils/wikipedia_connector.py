import pathway as pw
import requests
import spacy
# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

class WikipediaConnector():
    def __init__(self):
        pass

    def get_wikipedia_page_summary(self, title):
        try:
            url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                pages = response.json()['query']['pages']
                # Since 'pages' is a dictionary with the page id as the key, use next(iter()) to get the first key
                page_id = next(iter(pages))
                summary = pages[page_id]['extract']
                return summary
            return " "
        except Exception as e:
            # print(f"Error fetching Wikipedia page summary: {e}")
            return "None"

        


    def get_wikipedia_page_title(self, query):
        try:
            print(query)
            search_url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json'
            }
            response = requests.get(search_url, params=params)
            print(response)
            if response.status_code == 200:
                print("hi")
                results = response.json()['query']['search']
                print(results)
                if results:
                    # Return the title of the first search result
                    return results[0]['title']
            return " "
        except Exception as e:
            print(f"Error fetching Wikipedia page title: {e}")
            

# Function to extract key terms from a question
@pw.udf
def extract_key_terms(question):
    # Process the question with spaCy
    doc = nlp(question)
    
    # Extract named entities and key noun phrases
    entities = [ent.text for ent in doc.ents]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text not in entities]
    
    # Combine entities and noun_chunks for a more comprehensive set of key terms
    key_terms = entities + noun_chunks
    
    # Join the key terms into a single string query (if needed)
    query_terms = ' '.join(key_terms)

    return query_terms

wiki_connector = WikipediaConnector()

@pw.udf
def enrich_with_wikipedia(keywords):
    title = wiki_connector.get_wikipedia_page_title(keywords)
    print(title)
    summary = wiki_connector.get_wikipedia_page_summary(title)
    enriched_chunk = summary
    print(enriched_chunk)
    return enriched_chunk