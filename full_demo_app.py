import streamlit as st
import PyPDF2

from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import LayeredLayout


# Function to summarize the uploaded file
def read_file(file_path):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file_path)\
    
    collect = []
    for p in pdf_reader.pages:
        text = p.extract_text()
        collect.append(text)
    return collect 

def summarize():

    # load summary
    with open('./data/output/full_demo_app_10152024/summary.txt', 'r') as f:
        summary = f.read()
    
    return summary

# Function to draft based on the summary and vendor description
def drafter():

    # load draft 
    with open('./data/output/full_demo_app_10152024/draft.txt', 'r') as f:
        draft = f.read()

    return draft

# Streamlit app
def main():
    
    st.title("Representative user flow")
    if 'summary_generated' not in st.session_state:
        st.session_state['summary_generated'] = False
    if 'draft_generated' not in st.session_state:
        st.session_state['draft_generated'] = False

    # with st.sidebar:
    #     st.title("RFP Assistant")
    #     nodes = [StreamlitFlowNode( id='1', 
    #                             pos=(0, 0), 
    #                             data={'content': 'Vendor Detail'}, 
    #                             node_type='input', 
    #                             source_position='bottom', 
    #                             draggable=False),
    #         StreamlitFlowNode(  '2',
    #                             (100, 0), 
    #                             {'content': 'RFP'}, 
    #                             'input', 
    #                             'bottom', 
    #                             'left', 
    #                             draggable=False),]
        
    #     edges = []

    #     st.session_state.curr_state = StreamlitFlowState(nodes, edges)    
            
    #     if st.session_state['summary_generated']:
    #         st.session_state.curr_state.nodes.append(StreamlitFlowNode('3', (200, 0), {'content': 'Summary'}, 'input', 'bottom', 'left', draggable=False))
    #         st.session_state.curr_state.edges.append(StreamlitFlowEdge('2-3', '2', '3', animated=True, marker_end={'type': 'arrow'}))
    #         st.rerun()

    #     st.session_state.curr_state = streamlit_flow('tree_layout',
    #                 st.session_state.curr_state,
    #                 #layout=LayeredLayout(direction='down'),
    #                 fit_view=True,
    #                 show_minimap=False,
    #                 show_controls=False,
    #                 pan_on_drag=False,
    #                 allow_zoom=False,
    #                 allow_new_edges=True,)

    # Upload file with vendor description
    st.markdown("#### Vendor description")
    vendor_description = st.text_area("", 
                                       value=open('./data/output/full_demo_app_10152024/vendor_description.txt', 'r').read(),
                                       height=200)

    # Upload file
    st.markdown("#### Upload an RFP")
    uploaded_file = st.file_uploader("")

    # Summarize button
    # Summarize button
    if uploaded_file is not None and vendor_description:
        if st.button("Summarize RFP"):
            summary = summarize()
            st.session_state['summary'] = summary
            st.session_state['summary_generated'] = True

        if st.session_state['summary_generated']:
            st.markdown("#### RFP Summary")
            st.text_area("", value=st.session_state['summary'], height=200)
           
            if st.button("Draft RFP proposal"):
                st.markdown("#### RFP proposal draft")
                draft = drafter()
                st.session_state['draft'] = draft
                st.session_state['draft_generated'] = True
            
            if st.session_state['draft_generated']:
                st.text_area("", value=st.session_state['draft'], height=300)


if __name__ == "__main__":
    main()


