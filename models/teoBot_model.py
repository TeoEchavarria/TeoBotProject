from ctransformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

class TeoBotModel:
    def __init__(self):
        self.llm = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
            model_file="mistral-7b-instruct-v0.1.Q4_K_S.gguf", 
            model_type="mistral", 
            gpu_layers=40
            )
     
    def generate_response(self, question):
        return self.llm(question)

