import streamlit as st
from io import BytesIO
import os
from app.etl.excel_ingest import parse_excel
from app.etl.pdf_ingest import extract_pdf_text
from app.vectordb.chroma_client import ChromaClient
from app.llm.mistral_chain import MistralLLM

# --- Sidebar Branding ---
# st.sidebar.image('https://img.icons8.com/ios-filled/100/000000/warehouse.png', width=60)
st.sidebar.title('SmartPT Inventory')

def get_chroma_client():
    """Singleton ChromaClient for session."""
    if 'chroma_client' not in st.session_state:
        st.session_state['chroma_client'] = ChromaClient()
    return st.session_state['chroma_client']

def get_llm():
    """Singleton MistralLLM for session."""
    if 'llm' not in st.session_state:
        st.session_state['llm'] = MistralLLM()
    return st.session_state['llm']

# --- Main App ---
st.title('Supply Chain SmartPT: Inventory Assistant')
st.markdown('''<span style="font-size:1.1em; color:#555;">Upload inventory files, ask questions, and get instant insights powered by a local LLM.</span>''', unsafe_allow_html=True)
st.markdown('---')

chroma_client = get_chroma_client()
llm = get_llm()

if 'uploaded_docs' not in st.session_state:
    st.session_state['uploaded_docs'] = []  # List of dicts: {filename, doc_text, embedding, metadata}
if 'docs_loaded' not in st.session_state:
    st.session_state['docs_loaded'] = False

# --- File Upload Section ---
st.header('📤 Upload Inventory Files')
uploaded_files = st.file_uploader('Choose one or more Excel or PDF files', type=['xlsx', 'xls', 'pdf'], accept_multiple_files=True)

# --- Default Sample Inventory File for Dry Run ---
sample_path = os.path.join('data', 'sample_inventory.xlsx')
if os.path.exists(sample_path):
    if st.button('Load Sample Inventory File'):
        try:
            with open(sample_path, 'rb') as f:
                sample_bytes = BytesIO(f.read())
                sheets = parse_excel(sample_bytes)
                doc_text = '\n'.join([df.to_csv(index=False) for df in sheets.values()])
                embedding = llm.get_embedding(doc_text)
                chroma_client.add_documents([doc_text], [embedding], metadatas=[{"filename": 'sample_inventory.xlsx'}])
                st.session_state['uploaded_docs'].append({
                    'filename': 'sample_inventory.xlsx',
                    'doc_text': doc_text,
                    'embedding': embedding,
                    'metadata': {"filename": 'sample_inventory.xlsx'}
                })
                st.session_state['docs_loaded'] = True
                st.success('✅ Sample inventory file loaded and embedded!')
        except Exception as e:
            st.error(f'❌ Error loading sample inventory: {e}')
else:
    st.info('No sample inventory file found in data/.')

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Avoid duplicate uploads by filename
        if any(doc['filename'] == uploaded_file.name for doc in st.session_state['uploaded_docs']):
            continue
        try:
            with st.spinner(f'Processing {uploaded_file.name}...'):
                # --- Extract text from file ---
                if uploaded_file.name.lower().endswith(('xlsx', 'xls')):
                    sheets = parse_excel(BytesIO(uploaded_file.read()))
                    doc_text = '\n'.join([df.to_csv(index=False) for df in sheets.values()])
                elif uploaded_file.name.lower().endswith('pdf'):
                    doc_text = extract_pdf_text(BytesIO(uploaded_file.read()))
                else:
                    st.error(f'❌ Unsupported file type: {uploaded_file.name}')
                    continue
                # --- Embed and store in ChromaDB ---
                embedding = llm.get_embedding(doc_text)
                chroma_client.add_documents([doc_text], [embedding], metadatas=[{"filename": uploaded_file.name}])
                st.session_state['uploaded_docs'].append({
                    'filename': uploaded_file.name,
                    'doc_text': doc_text,
                    'embedding': embedding,
                    'metadata': {"filename": uploaded_file.name}
                })
                st.session_state['docs_loaded'] = True
                st.success(f"✅ {uploaded_file.name} embedded and stored for Q&A!")
        except Exception as e:
            st.error(f'❌ Error processing {uploaded_file.name}: {e}')
st.markdown('---')

# --- Uploaded Documents List & Management ---
st.header('📄 Uploaded Documents')
if st.session_state['uploaded_docs']:
    cols = st.columns(2)
    for i, doc in enumerate(st.session_state['uploaded_docs']):
        with cols[i % 2].expander(doc['filename']):
            st.write('Preview (first 500 chars):')
            st.code(doc['doc_text'][:500] + ('...' if len(doc['doc_text']) > 500 else ''))
    if st.button('🗑️ Clear All Documents'):
        st.session_state['uploaded_docs'] = []
        st.session_state['docs_loaded'] = False
        st.success('All uploaded documents cleared.')
else:
    st.info('No documents uploaded yet.')
st.markdown('---')

# --- Advanced Search Controls ---
st.header('🔎 Inventory Q&A')
user_query = st.text_input('Ask a question about your inventory...')
top_k = st.slider('Number of top documents to search (k)', min_value=1, max_value=5, value=3)
filenames = [doc['filename'] for doc in st.session_state['uploaded_docs']]
filename_filter = st.multiselect('Filter by filename (optional)', filenames, default=filenames)

if st.button('Submit'):
    if not st.session_state.get('docs_loaded'):
        st.warning('⚠️ Please upload and process at least one inventory file first.')
    elif not user_query.strip():
        st.warning('⚠️ Please enter a question.')
    else:
        try:
            with st.spinner('Searching and generating answer...'):
                query_embedding = llm.get_embedding(user_query)
                results = chroma_client.similarity_search(query_embedding, top_k=top_k)
                sources = []
                context_parts = []
                if results and 'documents' in results and results['documents']:
                    for i, doc in enumerate(results['documents'][0]):
                        meta = results['metadatas'][0][i] if 'metadatas' in results and results['metadatas'] else {}
                        fname = meta.get('filename', 'Unknown')
                        if fname in filename_filter:
                            sources.append(f"Source {i+1}: {fname}")
                            context_parts.append(f"[Source: {fname}]\n{doc}")
                    context = '\n\n'.join(context_parts)
                # Fallback: if no context found, use all uploaded docs
                if not context_parts:
                    sources = [f"Source {i+1}: {doc['filename']} (fallback)" for i, doc in enumerate(st.session_state['uploaded_docs']) if doc['filename'] in filename_filter]
                    context = '\n\n'.join([doc['doc_text'] for doc in st.session_state['uploaded_docs'] if doc['filename'] in filename_filter])
                if not context:
                    st.warning('No relevant documents found for your query and filter.')
                else:
                    answer = llm.answer_question(context, user_query)
                    st.markdown('**Sources used:**')
                    for s in sources:
                        st.write(s)
                    st.success('✅ Answer generated!')
                    st.info(answer)
        except Exception as e:
            st.error(f'❌ Error during Q&A: {e}')
st.markdown('---')

st.caption('Powered by Mistral LLM, ChromaDB, and Streamlit') 