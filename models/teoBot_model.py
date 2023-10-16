from ctransformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

class TeoBotModel:
    @st.cache_resource
    def __init__(_self):
        #self.llm = ctransformers(
        #model = "thebloke/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        #model_type="mistral",
        #max_new_tokens = 1048,
        #temperature = 0.3
        _self.llm = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
            model_file="mistral-7b-instruct-v0.1.Q2_K.gguf", 
            model_type="mistral", 
            gpu_layers=40
            )
     
    def generate_response(_self, question):
        return _self.llm(question)

