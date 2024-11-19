# LLM workflow code

This repo contains the workflow for summarizing an RFP and outlining and drafting a proposal.  It has three components:

1) Summarize
- Ingests an RFP and splits it into pages
- Summarizes each page
- Creates a long-form summary of the page summaries
- Creates a short-form summary of the long-form summary
- Creates a summary from the entire RFP (not individual pages)

2) Checklist/Outline (very WIP right now)
- Ingests the RFP using the summarizer's functionality
- Creates the outline of a draft from an entire RFP
- Generates questions that need to be answered to improve the draft
- Answers those questions using the full RFP
- Edits the outline according to those answers
- Repeats the above (by default, 2 times)
- Outputs the final checklist

3) Draft
- Takes in the final checklist output, vendor information and general drafting criteria
- Generates a draft proposal based on these inputs

## Set up

Install the requirements.txt file.  If you want to use local LLMs, you will also need to install [Ollama](https://ollama.com/)

Create a file `credentials.py` in the `rfpgo/` directory.  Put your OpenAI and Anthropic tokens in this file with the following format:

```
OPENAI_KEY = '<token>'
ANTHROPIC_KEY = '<token>'
```

## Run it

A simple example run:
```
python run_workflow.py \                 
-fn "../data/labels/drafter_09262024/RFP_Study to evaluate methods to calculate area median income.pdf" \
-m haiku \
-v "../data/labels/drafter_09262024/vendor_community_attributes.txt"
```

The following flags are available:

- `-fn`: path to file or directory for RFP
- `-m`: model to use for summarization/outline (default: haiku)
- `-d`: model to use for drafting (default: opus)
- `-v`: path to vendor information file
