import os
import pathway as pw
from pathway.xpacks.llm.llms import  prompt_chat_single_qa
from utils.wikipedia_connector import *
from config.application_config import ApplicationConfig
from utils.prompt import build_prompt
from .interfaces.adapters.google_drive_adapter import GoogleDriveAdapter
from .interfaces.adapters.open_ai_adapter import OpenAIAdapter
from .use_cases import DocumentProcessingPipeLine


def run(*, 
        object_id: str = ApplicationConfig.GOOGLE_DRIVE_OBJECT_ID, 
        api_key: str = ApplicationConfig.OPEN_AI_API_KEY, 
        ):
    
    # Initialize Googledrive adapter
    google_drive_adapter = GoogleDriveAdapter(service_user_credentials_file=ApplicationConfig.SERVICE_ACCOUNT_CREDENTIALS_FILE, refresh_interval=30)

    # Initialize OpenAI Adapter
    openai_adapter = OpenAIAdapter(api_key)

    # Intisaite OpenAI Embedder
    embedder = openai_adapter.embed_text()

    # Intisaite OpenAI Model
    model = openai_adapter.model_initialise()

    # Intisaite DocumentProcessingPipeLine
    document_processing_pipline = DocumentProcessingPipeLine(google_drive_adapter, embedder)

    query_context, response_writer = document_processing_pipline.execute(object_id)

    # Adjust the selection to include the difficulty level and context keywords when building prompts
    prompts = query_context.select(
        prompt=build_prompt (
            pw.this.documents_list,
            pw.this.query,
            pw.this.difficulty_level,
            pw.this.context_keywords,
            pw.this.mode
        )
    )

    responses = prompts.select(
        query_id=pw.this.id,
        response=model(prompt_chat_single_qa(pw.this.prompt))
    )

    output = responses.select(
        result=pw.this.response
    )

    response_writer(output)

    pw.run()