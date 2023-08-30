from flask import Flask, render_template, request, jsonify
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ChatMessageHistory
import tiktoken

MODEL_PATH = '/Users/deveshparagiri/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin'

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

def create_prompt() -> PromptTemplate:

    _DEFAULT_TEMPLATE: str = """You are Dev's personal A.I assistant named S.A.G.E. 
    You are a helpful, respectful and honest assistant. Please ensure that your responses are socially unbiased and positive in nature.
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    {query}
    S.A.G.E:
    """

    prompt: PromptTemplate = PromptTemplate(
        input_variables=["query"],
        template=_DEFAULT_TEMPLATE
    )
    return prompt

def load_model() -> LLMChain:
    callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    LLama_model: LlamaCpp = LlamaCpp(
        model_path=MODEL_PATH,
        temperature=0.2,
        max_tokens=4096,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True
    )
    prompt: PromptTemplate = create_prompt()
    
    llm_chain = LLMChain(
        llm=LLama_model,
        prompt=prompt
    )
    return llm_chain

llm_chain = load_model()
# history = ChatMessageHistory()

def get_chat_response(input):
    model_prompt: str = input
    response: str = llm_chain.run(model_prompt)
    # history.add_user_message(model_prompt)
    # history.add_ai_message(response)
    response = response[:-1] if response[-1]=='\n' else response
    return response

if __name__ == "__main__":
    app.run(debug=True, port=2000)