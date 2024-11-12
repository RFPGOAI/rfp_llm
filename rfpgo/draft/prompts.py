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
