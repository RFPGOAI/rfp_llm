page_summary = """The following is a page in a longer document. \
     Summarize it in one or two sentences.\
        \n\n{document}\
        \n\nSummary: """


consolidate_summary_long = """The following are summaries of pages in a \
Request for Proposal document. \
Consolidate them into a single detailed summary.\
Ensure you capture all information relevant to the proposal.\
\n\n{document}
\n\nSummary: """

consolidate_summary_short = """Shorten the following summary of a Request for Proposal.\n\
Capture information relevant to drafting a response to this document.
\n\n{document}
\n\nSummary: """

rag_sections = """What are the sections required for a response to this proposal?"""

get_sections = """The following document contains information about \
the relevant sections of a proposal. \
Return a list of the sections, one per line. \
No additional information is needed. \
Use the following format:\n\n

1. First section name\n
2. Second section name\n
...

{document}"""

rag_sections_detail = """What are the requirements for the {document} section?"""

get_sections_detail = """The following document contains information about \
the {section_name} section of a proposal. \
Return the requirements for drafting this section as a brief summary.

Document:\n
{document}
Summary:\n"""


section_questions = """Drafting the {document_1} section has the following requirements:\n\
{document_2}\n\n\
In drafting the section, what questions would you need to answer?"""

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