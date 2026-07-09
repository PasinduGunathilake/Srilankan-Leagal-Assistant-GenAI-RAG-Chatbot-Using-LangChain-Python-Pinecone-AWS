from flask import Flask, render_template, jsonify, request
#from src.Guardrails import input_regex_guardrail
from src.Guardrails import input_Multimodel_fallback_model_guardrail
from src.rag_chain import get_chains
import os
from dotenv import load_dotenv


# flask app initialize
app = Flask(__name__)



#system chain
system_chain = get_chains()



# default route
@app.route("/")
def index():
    return render_template("index.html")


# API route for question answering
@app.route("/get",methods=["GET","POST"])
def chat():

    # get json data from the request
    data = request.get_json()
    msg = data.get("msg")
    
    # validate if the message is empty
    if not msg:
        return jsonify({"error": "Message is empty"}), 400
    
    # Guardrail check

    '''
    # regex_guardrail
    if not input_regex_guardrail(input):
        return jsonify({
            "status": "blocked",
            "answer": "I apologize, but the query you have raised is outside the scope of our legal database. Please only inquire about legal matters."
        }), 200
    '''
    # mmfbm guardrail
    if not input_Multimodel_fallback_model_guardrail(msg):
        return jsonify({
            "status": "blocked",
            "answer": "I apologize, but the query you have raised is outside the scope of our legal database. Please only inquire about legal matters."
        }), 200
    
    # get the response through the system chain(rag_chain.py)
    try:
        response = system_chain.invoke({"input":msg})
        return jsonify({
            "status": "success",
            "answer": response.get('answer')
        }), 200
    except:
        return jsonify({
            "status": "error",
            "answer": "A system error occurred. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

'''
question = "what punishments of intellectual property law in sri lanka?"
response = RAG_chain.invoke({"input":question})
print(response['answer'])
'''