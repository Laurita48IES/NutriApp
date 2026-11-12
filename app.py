import json
import sqlite3

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from nombres import bonito

from estilos import (aplicar_estilos, icono_pagina, logo, burbuja_nutria,
                     burbuja_usuario, fila_insignias, titulo_seccion, aviso)
from nutria import responder, nueva_sesion, SALUDO_INICIAL

st.set_page_config(page_title="NutriApp", page_icon=icono_pagina(), layout="centered")
aplicar_estilos()

UMBRAL = 0.70

# icono, mensaje y color de la burbuja para cada veredicto
VEREDICTOS = {
    "muy_bueno":  ("🌟", "¡Este alimento es muy bueno!", "menta"),
    "frecuente":  ("😊", "Este alimento puede ser consumido con frecuencia", "celeste"),
    "moderacion": ("🌈", "Te recomendamos comer este alimento con moderación", "durazno"),
}


@st.cache_resource
def cargar():
    modelo = tf.keras.models.load_model("modelo/nutriapp_modelo_v4.keras")
    with open("modelo/clases_v4.json") as f:
        clases = json.load(f)
    return modelo, clases



def buscar_info(nombre):
    con = sqlite3.connect("nutriapp.db")
    con.row_factory = sqlite3.Row
    fila = con.execute("SELECT * FROM alimentos WHERE nombre = ?", (nombre,)).fetchone()
    con.close()
    return dict(fila) if fila else None


def mostrar_resultado(elegido):
    info = buscar_info(elegido)
    if info is None:
        burbuja_nutria("Todavía no tengo información de este alimento 🙈", "durazno")
        return

    burbuja_nutria(f"**¡Es {bonito(elegido)}!** 🎉\n\n{info['beneficios']}", "crema")
    burbuja_nutria(f"**🍊 Vitaminas y minerales**\n\n{info['vitaminas']}", "rosa")

    burbuja_nutria("¿Lo pueden comer todos? Fijate acá 👇", "celeste")
    fila_insignias([
        ("🌾 Celíacos", info["apto_celiacos"]),
        ("🩸 Diabéticos", info["apto_diabeticos"]),
        ("🥛 Intolerantes a la lactosa", info["apto_lactosa"]),
    ])

    icono, mensaje, color = VEREDICTOS[info["recomendacion"]]
    burbuja_nutria(f"{icono} **{mensaje}**", color)

    with st.expander("👨‍👩‍👧 Para papás y mamás"):
        st.write(info["nota_padres"])

    aviso()


modelo, clases = cargar()

# ---------- Encabezado ----------
logo()
burbuja_nutria("**¡Hola! Soy Nutri** 🦦\n\nMostrame un alimento y te cuento todo sobre él.",
               "crema")

# ---------- Cámara o foto ----------
camara = st.camera_input("📸 Sacale una foto al alimento")
subida = st.file_uploader("…o elegí una foto", type=["jpg", "jpeg", "png"])
foto = camara or subida

if foto:
    # si es una foto nueva, olvidar la elección anterior
    foto_id = hash(foto.getvalue())
    if st.session_state.get("foto_id") != foto_id:
        st.session_state["foto_id"] = foto_id
        st.session_state["elegido"] = None
        st.session_state["alimento_chat"] = None

    img = Image.open(foto).convert("RGB")
    st.image(img, width=280)

    arr = np.expand_dims(np.array(img.resize((224, 224))), 0)
    p = modelo.predict(arr, verbose=0)[0]
    top3 = np.argsort(p)[::-1][:3]

    if p[top3[0]] >= UMBRAL:
        st.session_state["elegido"] = clases[top3[0]]
    elif st.session_state["elegido"] is None:
        burbuja_nutria("Mmm, no estoy segura 🤔 ¿Es alguno de estos?", "durazno")
        columnas = st.columns(3)
        for col, i in zip(columnas, top3):
            if col.button(bonito(clases[i]), key=f"op{i}"):
                st.session_state["elegido"] = clases[i]
                st.rerun()

    elegido = st.session_state["elegido"]
    if elegido:
        mostrar_resultado(elegido)

# ---------- Chat con Nutri ----------
titulo_seccion("💬 Charlá con Nutri")

if "chat" not in st.session_state:
    st.session_state["chat"] = [{"role": "assistant", "content": SALUDO_INICIAL}]
    st.session_state["sesion"] = nueva_sesion()
if "alimento_chat" not in st.session_state:
    st.session_state["alimento_chat"] = None

for m in st.session_state["chat"]:
    if m["role"] == "assistant":
        burbuja_nutria(m["content"], "crema")
    else:
        burbuja_usuario(m["content"], "celeste")

pregunta = st.chat_input("Preguntale algo a Nutri…")
if pregunta:
    st.session_state["chat"].append({"role": "user", "content": pregunta})
    actual = st.session_state["alimento_chat"] or st.session_state.get("elegido")
    respuesta, alimento = responder(pregunta, st.session_state["sesion"], actual)
    st.session_state["alimento_chat"] = alimento
    st.session_state["chat"].append({"role": "assistant", "content": respuesta})
    st.rerun()
