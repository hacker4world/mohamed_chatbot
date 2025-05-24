from flask import jsonify
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from prompts import ANSWER_QUESTION_PROMPT
import os


os.environ["PINECONE_API_KEY"] = "pcsk_3njQdj_JvBaU7wwJy1L3Gh4g1A9papKGqnzZDdEDqi81ipNDJw78CCNx8Gp5rRSRpxUzAW"

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

model = OllamaLLM(model="qwen2.5-coder:14b", temperature=0.1)


def answer_company_question(question):
    context = fetch_documents(question)

    answer_prompt = ChatPromptTemplate.from_template(ANSWER_QUESTION_PROMPT)

    answer_chain = answer_prompt | model

    response = answer_chain.invoke({
        "context": context,
        "question": question
    })

    return jsonify({
        "response": clean_data(response).strip()
    })



def fetch_documents(question):

    vectorstore = PineconeVectorStore(
        index_name="kroshu",
        embedding=embeddings
    )

    context = ""

    docs = vectorstore.similarity_search(question, k=5)

    for doc in docs:
        context += "## " + doc.page_content + "\n"

    return context


def clean_data(response):
    return response.replace("<think>", "").replace("</think>", "")