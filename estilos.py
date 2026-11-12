import base64
import html
import os
import re

import streamlit as st
from PIL import Image

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

ESTADOS = {
    "si":         ("✅", "Apto", "t-verde"),
    "moderacion": ("⚠️", "Con moderación", "t-amarillo"),
    "depende":    ("🔎", "Depende: mirá la etiqueta", "t-amarillo"),
    "no":         ("🚫", "No apto", "t-rojo"),
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&display=swap');

:root {
  --texto: #4E3623;
  --crema: #FFF3BF;    --crema-b: #E3C96E;
  --menta: #DDF3D3;    --menta-b: #94C985;
  --celeste: #DAEFFB;  --celeste-b: #8CC4E4;
  --durazno: #FFE4D0;  --durazno-b: #EDB08A;
  --rosa: #FFDFE5;     --rosa-b: #F0A1B4;
}

/* ---------- Fondo: el pantano de la nutria ---------- */
.stApp {
  background-image: url("__FONDO__");
  background-size: cover;
  background-position: center bottom;
  background-attachment: fixed;
  font-family: 'Fredoka', 'Trebuchet MS', sans-serif;
  color: var(--texto);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"], .stDeployButton { display: none; }
.block-container { max-width: 760px; padding-top: 1.2rem; padding-bottom: 7rem; }
button, textarea, input { font-family: 'Fredoka', 'Trebuchet MS', sans-serif !important; }

/* ---------- Logo ---------- */
.logo {
  width: min(250px, 62vw); aspect-ratio: 1; margin: 0 auto 8px;
  border-radius: 50%;
  background: url("__LOGO__") center / cover no-repeat;
  box-shadow: 0 6px 0 rgba(78, 54, 35, .20);
}

/* ---------- Burbujas de diálogo ---------- */
.fila-nutria, .fila-usuario {
  display: flex; align-items: flex-end; gap: 16px; margin: 16px 0;
}
.fila-usuario { flex-direction: row-reverse; }

.avatar {
  width: 68px; height: 68px; flex: 0 0 68px; border-radius: 50%;
  background: url("__AVATAR__") center / cover no-repeat;
  border: 3px solid #fff; box-shadow: 0 3px 0 rgba(78, 54, 35, .20);
}
.avatar-usuario {
  width: 52px; height: 52px; flex: 0 0 52px; border-radius: 50%;
  background: #fff; border: 3px solid var(--celeste-b);
  display: flex; align-items: center; justify-content: center; font-size: 28px;
}

.burbuja {
  position: relative; max-width: calc(100% - 92px);
  padding: 14px 20px; border-radius: 26px;
  background: var(--fondo); border: 3px solid var(--borde);
  color: var(--texto); font-size: 1.05rem; line-height: 1.5;
}
.fila-nutria .burbuja { border-bottom-left-radius: 8px; }
.fila-usuario .burbuja { border-bottom-right-radius: 8px; }
.burbuja::before {               /* la colita de la burbuja */
  content: ""; position: absolute; bottom: 14px; width: 16px; height: 16px;
  background: var(--fondo); transform: rotate(45deg);
}
.fila-nutria .burbuja::before {
  left: -10px; border-left: 3px solid var(--borde); border-bottom: 3px solid var(--borde);
}
.fila-usuario .burbuja::before {
  right: -10px; border-right: 3px solid var(--borde); border-top: 3px solid var(--borde);
}

.crema   { --fondo: var(--crema);   --borde: var(--crema-b); }
.menta   { --fondo: var(--menta);   --borde: var(--menta-b); }
.celeste { --fondo: var(--celeste); --borde: var(--celeste-b); }
.durazno { --fondo: var(--durazno); --borde: var(--durazno-b); }
.rosa    { --fondo: var(--rosa);    --borde: var(--rosa-b); }

/* ---------- Insignias: celíacos, diabéticos, lactosa ---------- */
.insignias { display: flex; gap: 12px; flex-wrap: wrap; margin: 4px 0 14px; }
.insignia {
  flex: 1 1 150px; border-radius: 22px; padding: 12px 10px; text-align: center;
  border: 3px solid; font-size: .98rem; line-height: 1.35; color: var(--texto);
}
.insignia .ico { font-size: 30px; line-height: 1.2; }
.t-verde    { background: var(--menta);  border-color: var(--menta-b); }
.t-amarillo { background: var(--crema);  border-color: var(--crema-b); }
.t-rojo     { background: var(--rosa);   border-color: var(--rosa-b); }

/* ---------- Títulos y avisos ---------- */
.titulo-seccion {
  display: inline-block; background: #fff; border: 3px solid var(--crema-b);
  border-radius: 999px; padding: 6px 22px; margin: 26px 0 2px;
  font-weight: 600; font-size: 1.15rem; color: var(--texto);
}
.aviso {
  background: rgba(255, 255, 255, .88); border-radius: 16px; padding: 8px 14px;
  font-size: .85rem; margin-top: 12px; text-align: center; color: var(--texto);
}

/* ---------- Widgets de Streamlit ---------- */
[data-testid="stCameraInput"], [data-testid="stFileUploader"] {
  background: rgba(255, 255, 255, .92); border: 3px solid var(--celeste-b);
  border-radius: 26px; padding: 14px 16px; margin-bottom: 10px;
}
[data-testid="stCameraInput"] label p, [data-testid="stFileUploader"] label p {
  font-weight: 600; font-size: 1.05rem; color: var(--texto);
}
[data-testid="stImage"] img {
  border-radius: 24px; border: 5px solid #fff; box-shadow: 0 4px 0 rgba(78, 54, 35, .18);
}
.stButton > button {
  background: var(--menta); color: var(--texto); border: 3px solid var(--menta-b);
  border-radius: 999px; font-size: 1.1rem; font-weight: 500; padding: .5rem 1.2rem;
}
.stButton > button:hover {
  background: var(--crema); border-color: var(--crema-b); color: var(--texto);
}
[data-testid="stExpander"] {
  background: rgba(255, 255, 255, .93); border: 3px solid var(--durazno-b);
  border-radius: 20px;
}
[data-testid="stBottom"], [data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] { background: transparent; }
[data-testid="stChatInput"] {
  background: #fff; border: 3px solid var(--crema-b); border-radius: 30px;
}
</style>
"""


def _datauri(nombre, tipo):
    with open(os.path.join(CARPETA, nombre), "rb") as f:
        return f"data:{tipo};base64," + base64.b64encode(f.read()).decode()


@st.cache_resource
def _css():
    return (CSS.replace("__FONDO__", _datauri("fondo_pantano.jpg", "image/jpeg"))
               .replace("__LOGO__", _datauri("nutria_logo.png", "image/png"))
               .replace("__AVATAR__", _datauri("nutria_avatar.png", "image/png")))


def icono_pagina():
    return Image.open(os.path.join(CARPETA, "nutria_avatar.png"))


def aplicar_estilos():
    st.markdown(_css(), unsafe_allow_html=True)


def _texto(t):
    t = html.escape(str(t))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)
    return t.replace("\n", "<br>")


def logo():
    st.markdown('<div class="logo"></div>', unsafe_allow_html=True)


def burbuja_nutria(texto, color="crema"):
    st.markdown(
        f'<div class="fila-nutria"><div class="avatar"></div>'
        f'<div class="burbuja {color}">{_texto(texto)}</div></div>',
        unsafe_allow_html=True)


def burbuja_usuario(texto, color="celeste"):
    st.markdown(
        f'<div class="fila-usuario"><div class="avatar-usuario">🧒</div>'
        f'<div class="burbuja {color}">{_texto(texto)}</div></div>',
        unsafe_allow_html=True)


def fila_insignias(items):
    """items: lista de (titulo, valor) con valor = si / moderacion / depende / no."""
    tarjetas = ""
    for titulo, valor in items:
        icono, texto, clase = ESTADOS[valor]
        tarjetas += (f'<div class="insignia {clase}"><div class="ico">{icono}</div>'
                     f'<b>{html.escape(titulo)}</b><br>{texto}</div>')
    st.markdown(f'<div class="insignias">{tarjetas}</div>', unsafe_allow_html=True)


def titulo_seccion(texto):
    st.markdown(f'<div class="titulo-seccion">{html.escape(texto)}</div>',
                unsafe_allow_html=True)


def aviso(texto="NutriApp es informativa y no reemplaza la consulta con un "
                "médico o nutricionista."):
    st.markdown(f'<div class="aviso">{html.escape(texto)}</div>', unsafe_allow_html=True)
