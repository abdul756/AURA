from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.llms import OpenAIChat
import pathway as pw
class OpenAIAdapter:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def embed_text(self):
        embedder = OpenAIEmbedder(api_key=self.api_key, model="text-embedding-ada-002")
        return embedder
    
    def model_initialise(self):
        model = OpenAIChat(
            api_key=self.api_key,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=800,
            retry_strategy=pw.asynchronous.FixedDelayRetryStrategy(),
            cache_strategy=pw.asynchronous.DefaultCache(),
            )
        
        return model

