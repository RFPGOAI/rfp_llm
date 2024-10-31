from process.prompts import *
import PyPDF2
from utils import call_llm

class Summarizer(object):
    page_prompt = page_summary
    consolidate_prompt_long = consolidate_summary_long
    consolidate_prompt_short = consolidate_summary_short

    def __init__(self, llm, fn):
        self.llm = llm
        self.llm_name = llm.dict()['model']
        self.split_doc = self._splitter(fn)

    def _splitter(self, doc):
        # Open the PDF file
        pdf_file = open(doc, 'rb')

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Loop through each page and extract the text
        collect = []
        for p in pdf_reader.pages:
            text = p.extract_text()
            collect.append(text)
        return collect 
    
    def summarize(self):
        # pagewise summaries
        self.page_summaries = []
        for s in self.split_doc:
            p = self.page_prompt.format(document=s)
            self.page_summaries.append(call_llm(p, self.llm))

        # consolidate
        self.joined_p = ''
        for i, p in enumerate(self.page_summaries):
            self.joined_p += f'Page {i+1}: {p}\n\n'
        c = self.consolidate_prompt_long.format(document=self.joined_p)
        self.summary = call_llm(c, self.llm)

        # short summary
        c = self.consolidate_prompt_short.format(document=self.summary)
        self.summary_short = call_llm(c, self.llm)

        
