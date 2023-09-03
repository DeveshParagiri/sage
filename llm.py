# ================================================================================
# This script instantiates the llm object with the relevant parameters
# ================================================================================
from langchain.llms import CTransformers

# Local CTransformers wrapper for Llama-2-7B-Chat
llm = CTransformers(model='/Users/deveshparagiri/Downloads/models/sage-v2-q8_0.bin',
                    model_type='llama', # Model type Llama
                    config={'max_new_tokens': 256,
                            'temperature': 0.5})