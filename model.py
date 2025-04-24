



model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash", 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key="AIzaSyAk_8gkj7XbM-1mbHplnjnygDRpit6uikA", 
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "gemini",
    },
)
