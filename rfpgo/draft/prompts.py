draft_prompt = """You are drafting the {section} section of a proposal. \
Build on the following outline to write a draft with complete paragraphs:
<section_outline>
{section_outline}
</section_outline>
{vendor_info}
When drafting, you ensure the draft meets the following criteria:
<criteria>
{criteria}
</criteria>

Draft the section in narrative form using the company details as best you can. \
Answer truthfully, to the best of your knowledge. \
If there is information you are missing, specify as a set of questions.

<draft>"""

vendor_info_prompt = """
Your company details are: 
<company_details>
{vendor_info}
</company_details>

"""
draft_revise = """Review the following draft of a proposal to a grovernment RFP. \
Revise the draft as necessary to avoid redundancy and provide clarity. \
Avoid dramatically changing the draft. \
Ensure the draft adheres to the following criteria:

<criteria>
{criteria}
</criteria>

<draft>
{draft}
</draft>

<revised_draft>"""

# excess criteria for drafting any section
# TODO: this is hard-coded - probably we extract from the RFP
criteria = """1. The technical proposal must contain sufficient detail to convey to members of the evaluation team the Proposer’s knowledge of the subjects and skills necessary to successfully complete the project. Include any required involvement of government staff. The Proposer may also present any creative approaches that might be appropriate and may provide any pertinent supporting documentation."
2. Project schedule must ensure that all required deliverables are provided. Include a project schedule with deliverables outlining a plan for addressing the question content and reports.
3. The Proposer must identify potential risks that are considered significant to the success of the project in sufficient detail to convey to members of the evaluation team the manage these risks, including timely reporting of risks..
4. Fully describe deliverables to be submitted under the proposed contract. Deliverables must support the purpose of this RFP."""
