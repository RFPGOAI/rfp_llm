from summarize.summarizer import Summarizer
#from draft.drafter import Drafter
#from checklist.checklist import Checklist
import sys
import os
import pandas as pd
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain.llms import Ollama
from langchain_openai import OpenAI, ChatOpenAI

# TODO: replace with whatever auth flow we decide
from credentials import *
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# TODO: probably pick model per task, right now just implementing for summary
anth_haiku = ChatAnthropic(model='claude-3-haiku-20240307')
# gemma is useful for testing this stuff out
gemma = Ollama(model="gemma2")

# model dict
model_dict = {}
model_dict['haiku'] = ChatAnthropic(model='claude-3-haiku-20240307')
model_dict['gemma'] = Ollama(model="gemma2")
model_dict['gpt35'] = ChatOpenAI(model='gpt-3.5-turbo')

def run_summary(model, fn):
    summarizer = Summarizer(model, fn)
    
    # create parent filepath
    fn_formatted = fn.stem.replace(' ', '_')
    output_fn = Path(
        f'../data/output/{fn_formatted}/summary_{summarizer.llm_name}.csv')
    output_fn.parent.mkdir(parents=True, exist_ok=True)
    # if exists, do not continue
    if output_fn.exists():
        return
    
    summarizer.summarize()
    # output to csv
    result = pd.DataFrame.from_records(zip(
        summarizer.split_doc, 
        summarizer.page_summaries),
        columns=['document', 'summary'])
    result.loc[0, 'long_summary'] = summarizer.summary
    result.loc[0, 'short_summary'] = summarizer.summary_short
    result.loc[0, 'page_prompt'] = summarizer.page_prompt
    result.loc[0, 'consolidate_prompt_long'] = summarizer.consolidate_prompt_long
    result.loc[0, 'consolidate_prompt_short'] = summarizer.consolidate_prompt_short
    result.to_csv(output_fn, index=False)

def run_draft(model, fn):
    drafter = Drafter()
    drafter.draft()
    drafter.review()
    return drafter

def run_checklist(model, fn):
    checklist = Checklist()
    checklist.checklist()
    return checklist


def main(model, fn):
    run_summary(model, fn)
    pass


if __name__ == "__main__":
    # TODO: this is hacky - assuming certain position of args

    _, fn, model_name = sys.argv

    model = model_dict[model_name]

    fn = Path(fn)
    if fn.is_dir():
        fns = fn.glob('*.pdf')
        for f in fns:
            main(model, f)
    else:
        main(model, fn) 