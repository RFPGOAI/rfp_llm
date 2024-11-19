from summarize.summarizer import Summarizer
from draft.drafter import Drafter
from checklist.checklist import Checklist
import sys
import os
import pandas as pd
from utils import format_output_fn
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_openai import OpenAI, ChatOpenAI
from pathlib import Path

# TODO: replace with whatever auth flow we decide
from credentials import *
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# model dict
model_dict = {}
model_dict['haiku'] = ChatAnthropic(model='claude-3-haiku-20240307')
model_dict['opus'] = ChatAnthropic(model='claude-3-opus-20240229')
model_dict['gemma'] = Ollama(model="gemma2")
model_dict['gpt35'] = ChatOpenAI(model='gpt-3.5-turbo')

# argparse 
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-fn', type=str, help='path to file or directory for RFP', 
                    required=True)
parser.add_argument('-m', '--model_name', type=str, 
                    help='model name, choose from gemma, gpt35, haiku, opus',
                    required=True)
parser.add_argument('-d', '--draft_model', type=str, 
                    help='model name for drafting, default opus',
                    default='opus')
parser.add_argument('-v', '--vendor_info', type=str, help='path to vendor info txt file',
                    default=None)

def run_summary(model, fn):
    summarizer = Summarizer(model, fn)
    
    output_fn = format_output_fn(fn, llm_name=summarizer.llm_name, module_name='summary')
    if output_fn.exists():
        print(f'{output_fn} already exists')
        return
    
    summarizer.summarize()
    # output to csv
    result = pd.DataFrame.from_records(zip(
        summarizer.split_doc, 
        summarizer.page_summaries),
        columns=['document', 'summary'])
    result.loc[0, 'long_summary'] = summarizer.summary
    result.loc[0, 'short_summary'] = summarizer.summary_short
    result.loc[0, 'full_summary'] = summarizer.summary_full
    result.loc[0, 'full_summary_format'] = summarizer.summary_format
    result.to_csv(output_fn, index=False)

def run_checklist(model, fn):
    checklist = Checklist(model, fn)

    output_fn = format_output_fn(fn, llm_name=checklist.llm_name, module_name='checklist')
    if output_fn.exists():
        print(f'{output_fn} already exists')
        return

    checklist.checklist()
    # checklist outputs different iterations
    narrative = checklist.output()
    narrative.to_csv(output_fn, index=False)

def run_draft(model, draft_model, fn, vendor_info=None):
    drafter = Drafter(model, draft_model, fn)
    
    output_fn = format_output_fn(fn, llm_name=drafter.llm_name, module_name='draft')
    if output_fn.exists():
        print(f'{output_fn} already exists')
        return
    
    if vendor_info is not None:
        drafter.add_vendor_info(vendor_info)

    drafter.draft()
    # output to csv, row is outline, draft
    df = pd.DataFrame({'outline': [drafter.raw_outline], 'draft': [drafter.draft_compiled]})
    df.to_csv(output_fn, index=False)


def main(model, draft_model, fn, vendor_info=None):
    run_summary(model, fn)
    run_checklist(model, fn)
    run_draft(model, draft_model, fn, vendor_info)
    pass


if __name__ == "__main__":
    args = parser.parse_args()
    fn = args.fn
    model_name = args.model_name
    draft_model_name = args.draft_model
    vendor_info = args.vendor_info

    if model_name not in model_dict:
        print(f'{model_name} not in model_dict')
        sys.exit(1)

    model = model_dict[model_name]

    if draft_model_name not in model_dict:
        print(f'{draft_model_name} not in model_dict')
        sys.exit(1)

    draft_model = model_dict[draft_model_name]

    fn = Path(fn)
    if fn.is_dir():
        fns = fn.glob('*.pdf')
        for f in fns:
            main(model, draft_model, f, vendor_info)
    else:
        main(model, draft_model, fn, vendor_info)

