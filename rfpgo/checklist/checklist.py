from .prompts import *
from utils import call_llm
from summarize.summarizer import Summarizer
from pandas import Series

class Checklist(object):
    """Outlining RFP proposal

    Args:
        llm (llm object): llm object
        fn (str): file path to RFP
        llm_drafter (llm object): llm object for drafting, only used in workflow, not in checklist
    """

    # full RFP checklist
    full_rfp_prompt = full_rfp

    def _count_tokens(self, text):
        # standard - ~3.5 characters / token
        return round(len(text)/3.5)

    def __init__(self, llm, fn, llm_drafter=None):
        self.llm = llm
        self.llm_name = llm.dict()['model']
        if llm_drafter is not None:
            self.llm_drafter = llm_drafter
        else:
            self.llm_drafter = llm
        # TODO: summarizer is just used to split the doc
        self.summarizer = Summarizer(llm, fn)
        split_doc = self.summarizer.split_doc
        self.full_rfp_text = '\n'.join(split_doc)

    def _qa_turn(self):
        # ask questions
        self.c_questions = checklist_questions.format(outline=self.checklist_revisions[-1])
        self.c_questions_response = call_llm(self.c_questions, self.llm).split('</questions>')[0]

        # answer questions
        self.c_answers = checklist_answers.format(document=self.full_rfp_text,
            questions=self.c_questions_response)
        return call_llm(self.c_answers, self.llm).split('</response>')[0]

    def checklist(self, turns=2):

        # track revisions
        self.checklist_revisions = []
        self.questions_revisions = []

        self.c_full = self.full_rfp_prompt.format(document=self.full_rfp_text)
        self.c_full_tokens = self._count_tokens(self.c_full)
        self.c_full_response = call_llm(self.c_full, self.llm_drafter).split('</outline>')[0]

        # first version
        self.checklist_revisions.append(self.c_full_response)

        for i in range(turns):
            c_answers_response = self._qa_turn()
            # step 4 - update with answers
            self.c_update = checklist_update.format(
                outline=self.c_full_response,
                questions=c_answers_response)
            c_update_response = call_llm(self.c_update, self.llm_drafter).split('</outline_update>')[0]
            self.checklist_revisions.append(c_update_response)
            self.questions_revisions.append(c_answers_response)

        self.narrative = [
            self.checklist_revisions[0],
            self.questions_revisions[0],
            self.checklist_revisions[1],
            self.questions_revisions[1],
            self.checklist_revisions[2],
        ]

    def display(self):
        print('\n----\n'.join(self.narrative))

    def output(self):
        return Series(self.narrative)

