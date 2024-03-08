import streamlit as st
import json
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama

# Choose the MiniLM model version
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Create the LangChain embedding object
@st.cache_resource
def get_embeddings(model_name):
    return HuggingFaceEmbeddings(model_name=model_name)
embeddings = get_embeddings(model_name)

@st.cache_resource
def get_doc_store():
    # doc store is all companies - metadata can be about where they came from
    simple = json.load(open('./rfp_data/company_simple.json'))
    cond = json.load(open('./rfp_data/company_conditions.json'))
    all = simple + cond
    companies = []
    for d in all:
        text = d['response']['content']
        doc =  Document(page_content=text, metadata=d['prompt'][0]) 
        companies.append(doc)
    return FAISS.from_documents(companies, embeddings)

# vector store based on ollama embeddings of doc split
db = get_doc_store()

# specify source path
fp = 'rfps_combinations_ext'
# create metadata for rfps and save
# don't need to run this multiple times
# ollama model
# llm = Ollama(model="gemma:7b")
# rfps = json.load(open(f'./rfp_data/{fp}.json'))

# rfps_w_metadata = []
# for r in rfps:
#     prompt = f"""Briefly describe the key considerations from this RFP as bullet points. \
#         Do not preface your response: {r['response']['content']}"""
#     key_considerations = llm.invoke(prompt)
#     r['metadata'] = {'prompt': r['prompt'],
#                     'key_considerations': key_considerations}
#     rfps_w_metadata.append(r)

# json.dump(rfps_w_metadata, open(f'./rfp_data/{fp}_w_metadata.json', 'w'))

# Load the RFP data
rfps = json.load(open(f'./rfp_data/{fp}_w_metadata.json'))

# refresh workflow
for r in rfps:
    if 'metadata' not in r:
        llm = Ollama(model="gemma:7b")
        prompt = f"""Briefly describe the key considerations from this RFP as bullet points. \
        Do not preface your response: {r['response']['content']}"""
        key_considerations = llm.invoke(prompt)
        r['metadata'] = {'prompt': r['prompt'],
                    'key_considerations': key_considerations}
        json.dump(rfps, open(f'./rfp_data/{fp}_w_metadata.json', 'w'))

@st.cache_data
def get_sim_company(rfp_metadata):
    key_conds = rfp_metadata['key_considerations']
    sim = db.similarity_search(key_conds, k=1)
    return sim[0].page_content


def main():
    rfp_conditions = ['environmental sustainability',
             'vendor is minority-owned',
             'vendor is women-owned',
             'vendor is local']

    st.sidebar.title('Select RFP prompt')
    checked_conds = {}
    for i, c in enumerate(rfp_conditions):
        if i == 0:
            default=True
        else:
            default=False     
        checked_conds[c] = st.sidebar.checkbox(c, value=default)
    
    condition_key = set([k for k, v in checked_conds.items() if v])

    selected_rfp = None
    for r in rfps:
        if set(r['condition']) == condition_key:
            selected_rfp = r
            break

    st.title('RFP Analysis')
    col1, col2, col3 = st.columns(3)
    
    if selected_rfp:
        with col1:
            st.subheader('Selected RFP')
            st.write(selected_rfp['response']['content'])

        with col2:
            st.subheader('Key considerations')
            st.write(selected_rfp['metadata']['key_considerations'].split('\n\n')[1])

        with col3:
            st.subheader('Suggested company')
            suggested_company = get_sim_company(selected_rfp['metadata'])
            st.write(suggested_company)

if __name__ == "__main__":
    main()