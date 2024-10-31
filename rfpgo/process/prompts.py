summary_criteria = """Pay particular attention to information about the following:
1. The RFP’s purpose and budget (if budget known and if budget unknown state “unspecified”)
2. RFP’s scope of work
3. Timeline for scope of work 
4. RFP process timeline 
5. Proposal submission requirements
6. Proposal evaluation criteria (including weights for each criterion)
7. Important points of contact
8. Terms and conditions"""

page_summary = """The following is a page in a longer document. \
Summarize it in one or two sentences.\
Do not generate anything else.\
\n\n{document}\
\n\nSummary: """

consolidate_summary_long = """The following are summaries of pages in a \
Request for Proposal document. \
Consolidate them into a single detailed summary.\
Ensure you capture all information relevant to the proposal.\
Do not generate anything else.\
\n\n{document}
\n\nSummary: """

consolidate_summary_short = """Shorten the following summary of a Request for Proposal.\n\
Capture information relevant to drafting a response to this document.\
Do not generate anything else.\
\n\n{document}
\n\nSummary: """

vendor_answers = """You are drafting the {document} section of a proposal. \
Your company details are as follows: \n\
{company_details}\n\n
How would you answer the following question in your draft of the {document} section?\n\
Answer truthfully, to the best of your knowledge. \
If you do not know the answer, ask for additional information.\n\
{question}\n\
Response: """

vendor_requirements = """You are drafting the {section} section of a proposal. \
Your company details are as follows: \n\
{vendor_info}

The section you are drafting requires the following:
{section_reqs}

When drafting, you should make sure to address these questions and topic areas: 
{checklist_reqs}

Ensure that the section draft meets the following criteria:
{criteria}

Draft the section using the company details as best you can. \
Answer truthfully, to the best of your knowledge. \
If there is information you are missing, specify as a set of questions.

Draft: """

vendor_requirements_revise = """Review the following draft of the {section} section of a proposal. \
Ensure that the draft addresses these questions and topic areas: 
{checklist_reqs}

And ensure the draft meets the following criteria:
{criteria}

Avoid dramatically changing the draft.\
Draft: """


relevance = """The following is a page from a request for proposal. \
Is it relevant to your response to this proposal? \
Table of contents or forms are not relevant. \
Answer yes or no, provide no additional information. \
Provide your response between <response></response> tags\n\n\
{document}
"""

sections = ['table of contents', 'cover page', 'forms', 'other']

section = """The following is a section in a longer document. \
Is it one of the following sections: {sections}\\n
Return only {', '.join(sections[:-1]) + ' or ' + sections[-1]}.\n\n
{document}"""

merge_query = """The following are two pages from a document. \
Are they part of the same section? \
Answer only with "yes" or "no", generate no additional information. \n\n\
Document 1: {doc_1}\n\
Document 2: {doc_2}\n\
Answer: """

# placeholder
extra_info = """The following is a page from a government request for proposal (RFP). \
Does the page contain any information about the required sections for a proposal? \
Answer only with "yes" or "no", generate no additional information. \n\n\
{document}"""