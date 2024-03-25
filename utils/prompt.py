import pathway as pw

@pw.udf
def build_prompt(documents, query, difficulty_level, context_keywords, mode='Deep Dive Mode'):
    """
    Constructs an enhanced prompt for Chat based on document chunks, query, 
    difficulty level, context keywords, and question type for explaining complex topics or providing specific answers in personalized educational content.
    
    Parameters:
    - documents: List of text chunks from relevant documents.
    - query: The main question or topic of interest.
    - difficulty_level: The intended difficulty level of the explanation (e.g., beginner, intermediate, advanced).
    - context_keywords: Keywords that provide context for the explanation.
    - question_type: The nature of the query - 'explanatory' for in-depth explanations, 'factual' for specific factual answers.
    """

    # Construct a string from document chunks
    docs_str = "\n".join([f"Document chunk ({idx + 1}): {doc}" for idx, doc in enumerate(documents)])
    keywords_str = ", ".join(context_keywords)

    if mode == 'Basic Mode':
        """
        Constructs a detailed prompt for OpenAI Chat based on document chunks, query,
        difficulty level, and context keywords for personalized educational content.
        """
        docs_str = "\n".join([f"Document chunk ({idx + 1}): {doc}" for idx, doc in enumerate(documents)])
        keywords_str = ", ".join(context_keywords)
        prompt = f"""
        Considering the documents provided and focusing on a difficulty level of '{difficulty_level}' with keywords '{keywords_str}', answer the following query:
        
        {query}
        
        Relevant document chunks:
        {docs_str}

        """
    else:
        # Enhancing the prompt for explanatory content
        prompt = f"""
        Context: The following query pertains to a complex topic that requires an in-depth explanation. Considering the documents provided and focusing on a difficulty level of '{difficulty_level}' with keywords '{keywords_str}', please:

        1. Explain the key concepts related to: {query}
        2. Answer the following specific questions or points of interest regarding the topic:
           - What are the most critical aspects to understand?
           - How do these concepts interrelate or contrast with each other?
        3. Provide examples or analogies to illustrate these concepts if possible.
        
        Relevant document chunks are provided for reference and should be used to inform the explanation:

        {docs_str}
        
        Aim for clarity and depth in the explanation, ensuring it's accessible to someone at the '{difficulty_level}' level of understanding.
        """
    return prompt.strip()
