from flask import Flask, render_template, jsonify, request
from src.Guardrails import input_guardrail, REFUSAL_MESSAGE
from src.rag_chain import get_chains


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
    msg = request.form["msg"]
    input = msg
    print(f"input: {input}")

    # add input level Guardrail
    if not input_guardrail(input):
        print("Blocked by input guardrail")
        return REFUSAL_MESSAGE
    
    response = system_chain.invoke({"input":input})
    print(f"response: {response['answer']}")
    return str(response['answer'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

'''
question = "what punishments of intellectual property law in sri lanka?"
response = RAG_chain.invoke({"input":question})
print(response['answer'])
'''