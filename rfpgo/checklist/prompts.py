full_rfp = """The following is a government Request for Proposal document. \
Review it carefully for information about what is required for drafting a response to this document. \
Consolidate the information into a detailed outline of the sections required in a response. \
Include information about response format, important dates, and any other relevant information.

<document>
{document}
</document>

<outline>"""

checklist_questions = """Below is the outline of a proposal. \
What questions would you ask to get more detail for creating a draft of the proposal? \
Respond with no more than three questions, one per line. \
Response with questions only, nothing else.

Example:
<questions>
Question 1
Question 2
</questions>

<outline>
{outline}
</outline>

<questions>"""

checklist_answers = """Below is a government Request for Proposal document followed by \
a set of questions.  Answer the questions in detail as best you can based on the document. \
Include quotes from the document as necessary. \
Be truthful and honest, do not make information up. \
Respond with each question, followed by the answer, nothing else.

Example:
Question 1
Answer 1
Question 2
Answer 2

<document>
{document}
</document>

<questions>
{questions}
</questions>

<response>"""

checklist_update = """Below is the outline of a proposal followed by some additional details \
in the form of questions and answers.  Update the outline with the additional details. \
Response with outline only, nothing else.

<outline>
{outline}
</outline>

<questions>
{questions}
</questions>

<outline_update>"""
