NOMBRES = {
    "sandwich_milanesa": "sándwich de milanesa",
    "anana": "ananá",
    "sandia": "sandía",
    "limon": "limón",
    "brocoli": "brócoli",
    "chupetin": "chupetín",
    "papas_fritas": "papas fritas",
    "dulce_de_leche": "dulce de leche",
}


def bonito(clave):
    return NOMBRES.get(clave, clave.replace("_", " "))