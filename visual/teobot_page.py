import streamlit as st

from models.teoBot_model import TeoBotModel

model = TeoBotModel()

class TeoBotPage:
    def __init__(self):
        
        # Escritura de primera interaccion con el chat
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "Como puedo ayudarte hoy?"}]
        
        # Escritura de todas las preguntas
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Boton para limpiar el chat
        st.sidebar.button('Clear Chat History', on_click=TeoBotPage.clear_chat_history)

        # Creacion de la barra de preguntas y guardarlas
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
                
        # Generacion de respuesta tanto del chat como de la categoria
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    
                    response = model.generate_response(prompt)
                    placeholder = st.empty()

                    placeholder.markdown(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
            
    
    @staticmethod
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "Como puedo ayudarte hoy?"}]



