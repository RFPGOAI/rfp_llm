from pathlib import Path

def call_llm(prompt, llm):
    response = llm.invoke(prompt)
    if isinstance(response, str):
        return response
    return response.content

# utility to format output fn
def format_output_fn(fn, llm_name, module_name):
    # create parent filepath
    out_folder = fn.parts[-2]
    fn_formatted = fn.stem.replace(' ', '_')
    output_fn = Path(
        f'../data/output/{out_folder}/{fn_formatted}/{module_name}_{llm_name}.csv')
    output_fn.parent.mkdir(parents=True, exist_ok=True)
    return output_fn