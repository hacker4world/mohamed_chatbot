from flask import jsonify
from langchain_ollama import OllamaLLM
from prompts import ANSWER_UNRELATED_QUESTION
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="qwen2.5-coder:14b", temperature=0.1)


def answer_unrelated_question(question):

    response_template = ChatPromptTemplate.from_template(ANSWER_UNRELATED_QUESTION)

    response_chain = response_template | model

    response = response_chain.invoke({
        "question": question
    })

    return jsonify({
        "response": response
    })