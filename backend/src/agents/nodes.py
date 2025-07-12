import os
from agents.prompts import custom_rag_prompt
from agents.states import State, AnswerWithSources
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


def generate(state: State):
    docs_content = "\n\n".join(
        f"context {idx} " + str(doc.metadata) + " " + doc.page_content for idx, doc in enumerate(state["context"]))

    messages = custom_rag_prompt.invoke(
        {"question": state["question"], "context": docs_content})

    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

    model_structured_output = model.with_structured_output(
        AnswerWithSources)

    response = model_structured_output.invoke(messages)

    return {"answer": response}


def retrieve(state: State):
    query_filter = None
    db_path = "src/agents/vector_store_db"

    # role based retrieval
    if state["access_level"] != "c_level":
        query_filter = {"access_level": state["access_level"]}

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004")

    vector_store = Chroma(
        collection_name="documentation",
        embedding_function=embeddings,
        persist_directory=db_path
    )

    retrieved_docs = vector_store.similarity_search(
        state["question"], filter=query_filter)

    return {"context": retrieved_docs}
