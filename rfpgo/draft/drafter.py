from .prompts import *
from utils import *
import pandas as pd

# sample vendor info
vendor_info = """About Community Attributes Inc (https://communityattributes.com)
* Founded: In 2005 by Chris Mefford, CAI is a Seattle-based consulting firm that focuses on community and economic development. The firm uses demographic, economic, and strategic planning to provide impactful solutions that help communities grow and thrive.
* Specialties: Data storytelling, economic analysis, strategic planning, GIS mapping, and stakeholder engagement. CAI helps clients visualize complex data and make informed decisions for urban planning and organizational development.
Key Management Team
* Chris Mefford (Founder & CEO): Chris has an extensive background in economic development and urban planning. Before founding CAI, he worked in transportation planning and economic analysis. Chris holds an MBA from the University of Washington, an MS in Urban and Regional Planning from the University of Iowa, and a BA in Mathematics and Economics from the University of Northern Iowa. He is a certified planner (AICP) and frequently presents on topics related to regional economic trends and community development?.
* Michaela Jellicoe (Senior Economist): With an MS in Agricultural Economics from Purdue University and a BA in Economics and Political Science from Western Washington University, Michaela specializes in economic impact studies and data analysis. She translates complex data into clear and actionable insights for clients across various sectors?.
* Bryan Lobel (Senior Planner): An expert in urban and economic planning, Bryan focuses on strategies for economic resilience and sustainability in rural communities. He has contributed to numerous statewide impact studies and is known for his work in economic recovery planning?.
* Elliot Weiss (Project Manager): Elliot brings expertise in urban planning and real estate development, holding a Master’s in Urban and Regional Planning and a Graduate Certificate in Real Estate Development from the University of Michigan. His work focuses on urban design, community engagement, and affordable housing projects?.
Past and Ongoing Projects
* Nisqually Earthquake Recovery (2001): CAI supported post-earthquake recovery efforts by providing economic and social impact assessments for the City of Seattle.
* Washington State Agricultural Fairs (Ongoing): CAI is conducting ongoing economic impact studies to evaluate the contributions of regional fairs to the state’s economy.
* City of Bremerton (Ongoing): Urban planning projects in Bremerton have focused on improving traffic management and public infrastructure near Naval Base Kitsap.
* Okanogan County (Ongoing): Economic resilience planning for rural communities, with an emphasis on addressing climate change-related challenges?.


Unique Business Offering
* CAI Live Platform: CAI stands out in the marketplace with its proprietary CAI Live platform, which integrates economic and planning expertise into a dynamic tool for real-time data visualization. This platform helps clients, such as municipalities and state governments, communicate their development strategies more effectively?.
* Data Storytelling Focus: Known for turning complex economic data into visual narratives, CAI excels in using data to tell compelling stories that inform decision-making processes. The firm is widely recognized for its ability to create actionable insights from detailed demographic and economic analyses?.
Capabilities
* Expertise spans GIS mapping, economic development, financial modeling, urban planning, and community engagement. The firm supports organizations in both urban and rural development planning, particularly in areas affected by economic or environmental challenges?.
Delivery Approach
* Collaborative and Technology-Driven: CAI integrates stakeholder feedback with cutting-edge technology to create tailored solutions. The firm's collaborative approach ensures clients are involved throughout the strategic planning process, and the CAI Live platform enhances transparency and data accessibility."""

# excess criteria for drafting any section
criteria = """1. The technical proposal must contain sufficient detail to convey to members of the evaluation team the Proposer’s knowledge of the subjects and skills necessary to successfully complete the project. Include any required involvement of government staff. The Proposer may also present any creative approaches that might be appropriate and may provide any pertinent supporting documentation."
2. Project schedule must ensure that all required deliverables are provided. Include a project schedule with deliverables outlining a plan for addressing the question content and reports.
3. The Proposer must identify potential risks that are considered significant to the success of the project in sufficient detail to convey to members of the evaluation team the manage these risks, including timely reporting of risks..
4. Fully describe deliverables to be submitted under the proposed contract. Deliverables must support the purpose of this RFP."""

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

    # TODO: leftover from previous checklist work
    # def _process_checklist(self, checklist_dict):
    #     checklist_section_dict = {}
    #     for k, kk in checklist_dict:
    #         # need to process, this is named something different
    #         trans_k = ' '.join(k.split()[:2])
    #         if trans_k not in checklist_section_dict:
    #             checklist_section_dict[trans_k] = []
    #         checklist_section_dict[trans_k].append(kk)
    #     checklist_section_contents = {}
    #     for (k, kk), contents in checklist_dict.items():
    #         checklist_section_contents[kk] = contents
    #     return checklist_section_dict, checklist_section_contents

    # def _create_checklist_req_prompt(self, section):
    #     prompt = ''
    #     # translate section
    #     trans_section = ' '.join(section.split()[:2])[:-1]
        
    #     for subsection in self.checklist_section_dict[trans_section]:
    #         prompt += f"{subsection}\n"
    #         prompt += '\n'.join(self.checklist_section_contents[subsection])
    #     return prompt

    # def review(self):
    #     # review entire draft, revise as needed
    #     prompt_info = {
    #         'draft': self.draft_compiled,
    #         'criteria': self.criteria
    #     }
    #     prompt = draft_revise.format(**prompt_info)
    #     response = call_llm(prompt, self.llm)
    #     self.draft_revised = self._store_req_resp(prompt, response)
    