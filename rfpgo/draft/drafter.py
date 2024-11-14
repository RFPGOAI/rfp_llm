from .prompts import *
from utils import *
import pandas as pd

class Drafter(object):
    # store a draft-specific version of this prompt
    draft_prompt = draft_prompt
    vendor_info = '\n'

    def __init__(self, model, draft_model, fn):
        self.llm = draft_model
        self.llm_name = self.llm.dict()['model']
        # retrieve checklist info
        checklist_fn = format_output_fn(fn, llm_name=model.dict()['model'], module_name='checklist')
        if not checklist_fn.exists():
            ValueError(f'{checklist_fn} does not exist')
        # get the final draft of the checklist
        self.raw_outline = pd.read_csv(checklist_fn).iloc[-1].values[0]
        self.outline = self._process_outline(self.raw_outline)

        # TODO: hardcoding this for now
        self.criteria = criteria

    def add_vendor_info(self, vendor_info):
        # add vendor_info to the prompt
        self.vendor_info = vendor_info_prompt.format(vendor_info=vendor_info)

    def _store_req_resp(self, req, resp):
        d = {
            'documents': req,
            'response': resp
            }
        return d
    
    def _process_outline(self, raw_outline):
        outline_dict = {}
        for section in raw_outline.split('\n\n')[1:-1]:
            lines = section.split('\n')
            outline_dict[lines[0]] = '\n'.join(lines[1:]).strip()
        return outline_dict
    
    def draft(self):
        self.sections = {}
        for section in self.outline:
            prompt = {
                'section': section,
                'vendor_info': self.vendor_info,
                'section_outline': self.outline[section],
                'criteria': self.criteria
                }
            f_prompt = draft_prompt.format(**prompt)
            response = call_llm(f_prompt, self.llm)
            # want to strip off the end tag
            response = response.split('</draft>')[0]
            self.sections[section] = self._store_req_resp(f_prompt, response)
        self.draft_compiled = '\n'.join(self.sections[section]['response'] for section in self.sections)
