#importar la libreria
import streamlit as st
from groq import Groq 

#comando para arrancar es "py -m streamlit run chatbot.py" ctrl + c para pararlo

#configuracion ventana de la web
st.set_page_config(page_title= "Super IA", page_icon= "🤖")

#poner un titulo
st.title("Hola, bienvenido.")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#funcion para conectar a la api
def crear_usuario_groq():
    clave_secreta = st.secrets["clave_api"] #obtener la clave api
    return Groq(api_key = clave_secreta) #conectar la api

#configuracion del modelo que se usara
def configurar_modelo(cliente, modelo, mensaje_entrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role": "user", "content": mensaje_entrada}],
        stream = True
    )

#historial de mensaje
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] 

def configurar_pagina() :
    st.sidebar.title("Configuracion") #menu lateral
    elegirModelo = st.sidebar.selectbox(  #caja de opciones
        "Elegi un modelo", #el titulo
        MODELO,    #opciones
        index = 0    #valor por defecto

    )
    return elegirModelo

def actualizar_historial(rol, contenido, avatar) :
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial() :
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]) :
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina() # llamado de la funcion
    clienteUsuario = crear_usuario_groq() #crea el usuario para usar la api
    inicializar_estado() #crea el historial de mensaje
    area_chat()

    mensaje = st.chat_input("Escriba su mensaje...")

    #verificar si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "😀") #mostrar mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #obtener respuesta
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun() #actualizar la pagina

if __name__ == "__main__":
    main()
