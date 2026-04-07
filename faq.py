import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.documents import Document

load_dotenv()

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Chroma vectorstore (in-memory, initialized as None)
vectorstore = None

# Prompt template
prompt = ChatPromptTemplate.from_template("""
Based on the question and context below, generate a helpful answer.

If the context doesn't contain the answer, say "I don't have information about that. Please contact our customer support."

Question: {question}

Context: {context}
""")


def ingest_faq_data(path):
    """Load FAQ data into Chroma vectorstore (only if not already loaded)"""
    global vectorstore

    if vectorstore is not None:
        print("FAQ data already loaded!")
        return

    # Read CSV
    df = pd.read_csv(path)

    # Build LangChain Documents — question as content, answer as metadata
    docs = [
        Document(
            page_content=row["question"],
            metadata={"answer": row["answer"]}
        )
        for _, row in df.iterrows()
    ]

    # Create vectorstore from documents
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)
    print("FAQ data loaded successfully!")


def format_docs(docs):
    """Format retrieved docs by joining their answers"""
    return " ".join([doc.metadata.get("answer", "") for doc in docs])


def chain(query):
    """Main function to answer FAQ questions using LangChain LCEL chain"""
    try:
        if vectorstore is None:
            return "FAQ data not loaded"

        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

        
        rag_chain = (
            {
                "context": itemgetter("question") | retriever | format_docs,
                "question": itemgetter("question")
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain.invoke({"question": query})

    except Exception as e:
        return f"Sorry, I couldn't process your question. Error: {str(e)}"


if __name__ == "__main__":
    from config import FAQ_PATH
    ingest_faq_data(FAQ_PATH)
    result = chain("what is your policy on defective products?")
    print(result)