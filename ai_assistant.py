from flask import jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from answer_company_question import answer_company_question
from prompts import INTENT_DETECTION_PROMPT
from answer_unrelated_question import answer_unrelated_question
from ai_agent import predict_data, suggest_actions


model = OllamaLLM(model="qwen3:8b", temperature=0.1)

def ai_assistant(prompt):

    intent_prompt = ChatPromptTemplate.from_template(INTENT_DETECTION_PROMPT)

    intent_chain = intent_prompt | model

    intent = intent_chain.invoke({
        "prompt": prompt
    }).strip()

    print(intent)

    if intent == "company_question":
        return answer_company_question(prompt)
    elif intent == "suggestion":
        return suggest_actions(prompt)
    elif intent == "prediction":
        return predict_data(prompt)
    elif intent == "other":
        return answer_unrelated_question(prompt)
    else:
        return jsonify({
            "response": "intent was unrecognized"
        })
