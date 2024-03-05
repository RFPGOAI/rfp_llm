import streamlit as st
import json
from langchain.llms import Ollama
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama

# Choose the MiniLM model version
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Create the LangChain embedding object
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# ollama model
llm = Ollama(model="gemma:7b")

# doc store is all companies - metadata can be about where they came from
simple = json.load(open('./rfp_data/company_simple.json'))
cond = json.load(open('./rfp_data/company_conditions.json'))
all = simple + cond
companies = []
for d in all:
    text = d['response']['content']
    doc =  Document(page_content=text, metadata=d['prompt'][0]) 
    companies.append(doc)

# vector store based on ollama embeddings of doc split
db = FAISS.from_documents(companies, embeddings)

# create metadata for rfps and save
# don't need to run this multiple times
# rfps = json.load(open('./rfp_data/rfps_conditions.json'))

# rfps_w_metadata = []
# for r in rfps:
#     prompt = f"""Extract the key considerations from this RFP as bullet points, \
#         provide no additional information: {r['response']['content']}"""
#     key_considerations = llm.invoke(prompt)
#     r['metadata'] = {'prompt': r['prompt'],
#                      'key_considerations': key_considerations}
#     rfps_w_metadata.append(r)

# json.dump(rfps_w_metadata, open(f'./rfp_data/rfps_conditions_w_metadata.json', 'w'))

# Load the RFP data
rfps = json.load(open('./rfp_data/rfps_conditions_w_metadata.json'))


def get_sim_company(rfp_metadata):
    key_conds = rfp_metadata['key_considerations']
    sim = db.similarity_search(key_conds, k=1)
    return sim[0].page_content


def main():
    st.sidebar.title('Select RFP prompt')
    selected_rfp = st.sidebar.selectbox('Select prompt', 
                         [p['prompt'].split(':')[1].strip('.')  
                          for p in rfps])
    selected_index = [p['prompt'].split(':')[1].strip('.') for p in rfps].index(selected_rfp)

    st.title('RFPs and Companies')
    st.subheader('Selected RFP')
    st.write(rfps[selected_index]['response']['content'])

    st.subheader('Suggested company')

    suggested_company = get_sim_company(rfps[selected_index]['metadata'])
    st.write(suggested_company)

if __name__ == "__main__":
    main()