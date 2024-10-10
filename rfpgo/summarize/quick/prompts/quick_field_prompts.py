fields = ['Project Name',
 'Agency/Department/Organization',
 'Solicitation Number',
 'Contact Person',
 'Email',
 'Submission Deadline',
 'Contract Term',
 'Source Link',]

field_prompt = """You are filling in structured information from a document.\\n   

What is the {field} in the document below?\\n  

If there is no {field} in the document, respond with "Not specified".\\n  

Provide no additional information, just the structured information.\\n

{document}\\n  

{field}: """

summary_prompt = """The following is a Request for Proposal by a government.\\n  
Write a one or two sentence summary of it, focusing on the requirements.\\n
Provide no additional information, just return the summary.\\n
{document}"""
