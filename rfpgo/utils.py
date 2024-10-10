def call_llm(prompt, llm):
    response = llm.invoke(prompt)
    if isinstance(response, str):
        return response
    return response.content