from flask import Flask, render_template, request
from utils import setup_dbqa

# MODEL_PATH = '/Users/deveshparagiri/Downloads/llama-2-7b-chat.ggmlv4.q8_0.bin'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    try:
        return get_chat_response(input)
    except ValueError:
        return "You have exceeded the token limit! Sorry for the inconvenience!"

# def create_prompt() -> PromptTemplate:

#     _DEFAULT_TEMPLATE: str = """You are Dev's personal A.I assistant named S.A.G.E. 
#     You are a helpful and honest assistant. Please ensure that your responses are socially unbiased and positive in nature.
#     If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
#     Do not end with a question.
#     {query}
#     S.A.G.E:
#     """

#     prompt: PromptTemplate = PromptTemplate(
#         input_variables=["query"],
#         template=_DEFAULT_TEMPLATE
#     )
#     return prompt

# def load_model() -> LLMChain:
#     callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
    
#     LLama_model: LlamaCpp = LlamaCpp(
#         model_path=MODEL_PATH,
#         temperature=0,
#         max_tokens=4096,
#         top_p=1,
#         callback_manager=callback_manager,
#         verbose=True
#     )
#     prompt: PromptTemplate = create_prompt()
    
#     llm_chain = LLMChain(
#         llm=LLama_model,
#         prompt=prompt
#     )
#     return llm_chain

# llm_chain = load_model()
# history = ChatMessageHistory()
dbqa = setup_dbqa()

def get_chat_response(input):
    # model_prompt: str = input
    response = dbqa({'query': input})
    source_docs = response['source_documents']
    # reply = f'{response["result"]}\n'
    # for i, doc in enumerate(source_docs):
    #     reply += f'\nSource Document {i+1}\n'
    #     # print(f'Source Text: {doc.page_content}')
    #     reply += f'Document Name: {doc.metadata["source"]} '
    #     reply += f'Page Number: {doc.metadata["page"]}\n'
    #     reply += '='* 50 # Formatting separator
    # print(source_docs)
    # response: str = llm_ch
    # ain.run(model_prompt)
    # history.add_user_message(model_prompt)
    # history.add_ai_message(response)
    return response['result']

if __name__ == "__main__":
    app.run(debug=True, port=2000)