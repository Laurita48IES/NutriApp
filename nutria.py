import os
import uuid
import sqlite3
import streamlit as st
from google.cloud import dialogflow
from google.oauth2 import service_account
from nombres import bonito

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciales.json"
PROJECT_ID = "chatboties-neqx"

SALUDO_INICIAL = ("¡Hola! Soy Nutri, la nutria de NutriApp 🦦 Mostrame un alimento "
                  "con la cámara o preguntame, por ejemplo: «¿La banana es buena?»")

AVISO = "\n\n(Ante cualquier duda, consultá con tu médico o nutricionista 💚)"

VEREDICTOS = {
    "muy_bueno":  ("🌟", "¡Este alimento es muy bueno!"),
    "frecuente":  ("😊", "Este alimento puede ser consumido con frecuencia"),
    "moderacion": ("🌈", "Te recomendamos comer este alimento con moderación"),
}

QUIEN = {
    "apto_celiacos": "celíacos",
    "apto_diabeticos": "personas con diabetes",
    "apto_lactosa": "intolerantes a la lactosa",
}


@st.cache_resource
def _cliente():
    try:
        info = dict(st.secrets["gcp_service_account"])
        creds = service_account.Credentials.from_service_account_info(info)
        return dialogflow.SessionsClient(credentials=creds)
    except (KeyError, FileNotFoundError):
        return dialogflow.SessionsClient()   # en tu compu usa credenciales.json


def nueva_sesion():
    return str(uuid.uuid4())


def _alimento_de(q):
    valor = q.parameters.get("alimento")
    if not valor:
        return None
    if isinstance(valor, str):
        return valor
    try:
        return str(list(valor)[0])
    except Exception:
        return None


def preguntar_df(texto, sesion):
    cliente = _cliente()
    ruta = cliente.session_path(PROJECT_ID, sesion)
    consulta = dialogflow.QueryInput(
        text=dialogflow.TextInput(text=texto, language_code="es"))
    r = cliente.detect_intent(request={"session": ruta, "query_input": consulta})
    q = r.query_result
    return q.intent.display_name, _alimento_de(q), q.fulfillment_text


def buscar_info(nombre):
    con = sqlite3.connect("nutriapp.db")
    con.row_factory = sqlite3.Row
    fila = con.execute("SELECT * FROM alimentos WHERE nombre = ?", (nombre,)).fetchone()
    con.close()
    return dict(fila) if fila else None


def frase_apto(info, campo, nombre):
    valor = info[campo]
    quien = QUIEN[campo]
    n = nombre.capitalize()
    if valor == "si":
        return f"¡Buenas noticias! Para {quien}, {nombre}: sí, se puede ✅"
    if valor == "moderacion":
        return f"{n} se puede comer, pero con moderación, si hablamos de {quien} ⚠️"
    if valor == "depende":
        return (f"Con {nombre}, para {quien}, depende 🔎: "
                f"hay que mirar bien la etiqueta del producto.")
    return f"Para {quien}, {nombre}: no se recomienda 🚫"


def responder(texto, sesion, alimento_actual=None):
    """Devuelve (respuesta, alimento) para la pregunta del usuario."""
    intent, alimento, texto_df = preguntar_df(texto, sesion)

    # saludo, despedida, presentación y "no entendí": responde Dialogflow
    if not intent.startswith("consultar_"):
        return (texto_df or "Mmm, no te entendí 🙈 ¿Me lo preguntás de otra forma?",
                alimento_actual)

    alimento = alimento or alimento_actual
    if not alimento:
        return ("¿De qué alimento hablamos? 🦦 Mostrame uno con la cámara "
                "o decime cuál."), None

    info = buscar_info(alimento)
    if info is None:
        return "Todavía no conozco ese alimento 🙈", alimento_actual

    nombre = bonito(alimento)

    if intent == "consultar_saludable":
        icono, mensaje = VEREDICTOS[info["recomendacion"]]
        return f"{icono} {mensaje}\n\n{info['beneficios']}", alimento
    if intent == "consultar_beneficios":
        return info["beneficios"], alimento
    if intent == "consultar_vitaminas":
        return f"{nombre.capitalize()} tiene: {info['vitaminas']} 🍊", alimento
    if intent == "consultar_celiacos":
        return frase_apto(info, "apto_celiacos", nombre) + AVISO, alimento
    if intent == "consultar_diabeticos":
        return frase_apto(info, "apto_diabeticos", nombre) + AVISO, alimento
    if intent == "consultar_lactosa":
        return frase_apto(info, "apto_lactosa", nombre) + AVISO, alimento

    return "Mmm, no te entendí 🙈 ¿Me lo preguntás de otra forma?", alimento