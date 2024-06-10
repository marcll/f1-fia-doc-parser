import os
from datetime import datetime

from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback


from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

from src.pdf_retriever import get_season_urls, retrieve_fia_pdfs, BASE_URL

# Load environment variables from .env file
load_dotenv()

def extract_text_from_pdf(pdf_files):
    """
    This function takes a list of PDF files, extracts the text from each file, and returns a vector representation of the text.
    """
    docs = []

    for pdf_path in pdf_files:
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue
        pdf_loader = PyPDFLoader(pdf_path)
        docs.extend(pdf_loader.load())

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(documents, embeddings)
    return vector

def create_agent_chain():
    """
    This function creates an agent chain using the OpenAI API. The agent chain is used to process and answer questions.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
    model_name = "gpt-4o"
    llm = ChatOpenAI(model_name=model_name)
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def get_llm_response(question, vector, context=None):
    """
    This function takes a question and a vector representation of a document, and returns the response from the language model.
    """
    chain = create_agent_chain()

    matching_docs = []
    for id, doc_id in vector.index_to_docstore_id.items():
        document = vector.docstore.search(doc_id)
        matching_docs.append(document)
        
    with get_openai_callback() as cb:
        answer = chain.invoke({"input_documents":matching_docs, "question": question, "context":context})

    logger.info(f"Total Tokens: {cb.total_tokens}")
    logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
    logger.info(f"Completion Tokens: {cb.completion_tokens}")
    logger.info(f"Total Cost (USD): ${cb.total_cost}")

    return answer['output_text']

def summarize_event_notes(vector):
    """
    This function takes a vector representation of a document and returns a summary of the event notes.
    """
    questions = [
        "What is the Grand Prix the document refers to?",
        "What is the publication date of each of the documents?",
        "What are the compounds selection for the gp?",
        "What are the mandatory race tyres and the Q3 tyre?",
        "What are the minimmum starting pressure for front and rear on each type?",
        "What are the camber limits for front and rear?",
    ]
    context = "Tyre compounds include intermediate, wet and slicks which are named by compound, C1, C2 ... compounds do not start with Q"

    summary = {}

    for question in questions:
        response = get_llm_response(question,vector, context=context)
        logger.debug(response)
        summary[question] = response

    return summary

def summarize_event_infringiments(vector):
    """
    This function takes a vector representation of a document and returns a summary of the event infringements.
    """
    questions = [
        "Which drivers and cars had received penalty or fine decision? Check Infringement, Summons and Decisions documents",
        "Which drivers/cars had received no further actions",
        "What penalties are meant to be served on next race?",
    ]
    context = None

    summary = {}

    for question in questions:
        response = get_llm_response(question,vector, context=context)
        logger.debug(response)
        summary[question] = response

    return summary

def is_event_notes_document(filename):
    keywords = ["pirelli", "event-notes", "eventnotes", "notes"]
    return any(keyword in filename.lower() for keyword in keywords)

def is_event_infringiments_document(filename):
    keywords = ["infringement", "decision", "summons", "offence"]
    return any(keyword in filename.lower() for keyword in keywords)


def process_documents(season, gp, actions=['event_notes','event_infringiments'],force=False):

    season_urls = get_season_urls(f"{BASE_URL}/documents/championships/fia-formula-one-world-championship-14/")
    season_url = season_urls.get(f"SEASON {season}")
    
    if not season_url:
        print(f"No URL found for season {season}")
        return
    
    download_dir = f"data/raw_pdfs/{season}/{gp.replace(' ', '_')}"
    retrieve_fia_pdfs(season_url, gp=gp, season_year=season, force=force)
    
    if 'event_notes' in actions:
        event_notes_files = [
            os.path.join(download_dir, f) for f in os.listdir(download_dir)
            if is_event_notes_document(f)
        ]
    
        if not event_notes_files:
            logger.info(f"No event notes found for {gp} in season {season}.")


        logger.debug(f"List of the Event Notes found: {event_notes_files}")


        # Extract the text to vectors and run the summarisation
        vector = extract_text_from_pdf(event_notes_files)
    
        summary = summarize_event_notes(vector)

        print(f"\n")
        print("="*40)
        print(f"Summarized event notes for {gp} in season {season}.")
        print("="*40)

        for key, value in summary.items():
            print(f"\n")
            print(f"{key}\n{'-'*len(key)}\n{value}\n")


    if 'event_infringiments' in actions:
        event_infringiments_files = [
            os.path.join(download_dir, f) for f in os.listdir(download_dir)
            if is_event_infringiments_document(f)
        ]
    
        if not event_infringiments_files:
            logger.info(f"No event infringiments found for {gp} in season {season}.")


        logger.debug(f"List of the Infringiment documents found: {event_infringiments_files}")


        # Extract the text to vectors and run the summarisation
        vector = extract_text_from_pdf(event_infringiments_files)
        
        summary = summarize_event_infringiments(vector)

        print(f"\n")
        print("="*40)
        print(f"Summarized Infringiments for {gp} in season {season}.")
        print("="*40)

        for key, value in summary.items():
            print(f"\n")
            print(f"{key}\n{'-'*len(key)}\n{value}\n")
