from flask import jsonify
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from sqlalchemy import create_engine, text
from prompts import DETECT_VALUE_PROMPT, PREDICT_VALUES_PROMPT, SUGGEST_IMPROVEMENT_PROMPT, UNSWER_UNRELATED_SUGGESTION

model = OllamaLLM(model="qwen3:8b", temperature=0.1)

db_config = {
    'username': 'root',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'database_name': 'kroshu'
}

connection_string = f"mysql+mysqlconnector://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database_name']}"

# Create engine
engine = create_engine(connection_string)

def suggest_actions(prompt):

    detect_value_prompt = ChatPromptTemplate.from_template(DETECT_VALUE_PROMPT)

    chain = detect_value_prompt | model

    detected_value = chain.invoke({
        "message": prompt
    }).strip()

    if detected_value == "none":
        unrelated_suggestion_prompt = ChatPromptTemplate.from_template(UNSWER_UNRELATED_SUGGESTION)

        chain = unrelated_suggestion_prompt | model

        response_message = chain.invoke({}).strip()

        return jsonify({
            "response": response_message
        })
    
    else:
        sql_query = f"SELECT * FROM indicator WHERE name = '{detected_value}';"

        print(sql_query)

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

            rows = result.fetchall()

            indicator_id = 0
            target = ""

            for row in rows:
                indicator_id = row.id
                target = row.target_per_week

            data_query = f"SELECT * from daily_value WHERE indicator_id = '{indicator_id}' ORDER BY day DESC LIMIT 7;"

            data_result = connection.execute(text(data_query))

            data_rows = data_result.fetchall()

            context = ""

            for row in data_rows:
                context += f"- {row.value} % logged in date : {row.day} \n"

            suggest_improvement_prompt = ChatPromptTemplate.from_template(SUGGEST_IMPROVEMENT_PROMPT)

            chain = suggest_improvement_prompt | model

            suggestions = chain.invoke({
                "indicator": detected_value,
                "target": target,
                "values": context
            }).strip()

            return jsonify({
                "response": suggestions
            })
        

def predict_data(prompt):
    detect_value_prompt = ChatPromptTemplate.from_template(DETECT_VALUE_PROMPT)

    chain = detect_value_prompt | model

    detected_value = chain.invoke({
        "message": prompt
    }).strip()

    if detected_value == "none":
        unrelated_suggestion_prompt = ChatPromptTemplate.from_template(UNSWER_UNRELATED_SUGGESTION)

        chain = unrelated_suggestion_prompt | model

        response_message = chain.invoke({}).strip()

        return jsonify({
            "response": response_message
        })
    
    else:
        sql_query = f"SELECT * FROM indicator WHERE name = '{detected_value}';"

        print(sql_query)

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

            rows = result.fetchall()

            indicator_id = 0

            for row in rows:
                indicator_id = row.id

            data_query = f"SELECT * from daily_value WHERE indicator_id = '{indicator_id}' ORDER BY day DESC LIMIT 15;"

            data_result = connection.execute(text(data_query))

            data_rows = data_result.fetchall()

            context = ""

            for row in data_rows:
                context += f"- {row.value} % logged in date : {row.day} \n"

            prediction_prompt = ChatPromptTemplate.from_template(PREDICT_VALUES_PROMPT)

            chain = prediction_prompt | model

            predictions = chain.invoke({
                "indicator": detected_value,
                "context": context,
                "message": prompt
            }).strip()

            return jsonify({
                "response": predictions
            })


    