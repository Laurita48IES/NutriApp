import sqlite3

CHISTES = {
    "agua": "¿Qué le dijo una gota de agua a otra? ¡Quedate cerca, que juntas hacemos un charco! 💧",
    "banana": "¿Por qué la banana no sabe guardar secretos? ¡Porque se pela y se le ve todo! 🍌",
    "brocoli": "¿Por qué el brócoli parece un arbolito? ¡Porque quiere que lo planten en tu plato! 🥦",
    "cebolla": "¿Por qué llora la cebolla cuando la cortan? ¡Porque se muere de la risa con las cosquillas! 🧅",
    "chicle": "¿Qué le dijo un chicle al zapato? ¡Me pegué a vos porque me caés muy bien! 😄",
    "chupetin": "¿Por qué el chupetín siempre está contento? ¡Porque tiene un palito para agarrarse de la vida! 🍭",
    "dulce_de_leche": "¿Qué le dijo la cuchara al dulce de leche? ¡No me sueltes, que me encanta estar pegada a vos! 🥄",
    "empanada": "¿Qué le dijo una empanada a otra? ¡Qué lindo repulgue que tenés! 🥟",
    "ensalada": "¿Por qué la ensalada nunca se pelea con nadie? ¡Porque siempre está bien mezclada con todos! 🥗",
    "frutilla": "¿Por qué la frutilla se puso colorada? ¡Porque le dijeron que era la fruta más linda del mundo! 🍓",
    "galletitas": "¿Qué le dijo una galletita a la leche? ¡Con vos me ablando de felicidad! 🍪",
    "gaseosa": "¿Por qué la gaseosa no sabe guardar secretos? ¡Porque cuando la abrís hace pssss y lo cuenta todo! 🥤",
    "hamburguesa": "¿Qué le dijo un pan de hamburguesa al otro? ¡Qué bien nos abrazamos, con la carne en el medio! 🍔",
    "helado": "¿Por qué el helado nunca se enoja? ¡Porque siempre mantiene la calma y está bien frío! 🍦",
    "huevo": "¿Por qué el huevo no cuenta chistes? ¡Porque tiene miedo de romperse de la risa! 🥚",
    "jugo": "¿Qué le dijo el vaso al jugo? ¡Estoy lleno de felicidad con vos! 🧃",
    "lechuga": "¿Qué le dijo la lechuga al tomate? ¡Tomate un ratito para charlar conmigo! 🥬",
    "manzana": "¡Una manzana al día, y el doctor se va de vacaciones! 🍎",
    "naranja": "¿Por qué la naranja siempre está de buen humor? ¡Porque tiene un gajo de alegría en cada rodajita! 🍊",
    "pan": "¿Qué le dijo un pan a otro? ¡Qué miga de amigos que somos! 🍞",
    "papa": "¿Cuál es el colmo de una papa? ¡Tener ojos y no poder ver! 🥔",
    "papas_fritas": "¿Qué le dijo una papa frita a otra? ¡Qué crujiente que estás hoy! 🍟",
    "pastas": "¿Qué le dijo un fideo a otro? ¡Qué lío, estamos todos enredados! 🍝",
    "pizza": "¿Por qué la pizza siempre está feliz? ¡Porque tiene muchas porciones de alegría! 🍕",
    "pollo": "¿Por qué el pollito cruzó la calle? ¡Para llegar al otro lado, claro! 🐥",
    "queso": "¿Qué se dice cuando sacás una foto? ¡Queso! Por eso el queso siempre sale sonriendo. 🧀",
    "tomate": "¿Por qué el tomate se puso colorado? ¡Porque vio a la ensalada sin aderezo! 🍅",
    "torta": "¿Por qué la torta es la reina de las fiestas? ¡Porque siempre llega con velitas y todos le cantan! 🎂",
    "uva": "¿Qué le dijo la uva verde a la uva morada? ¡Respirá, que te estás poniendo violeta! 🍇",
    "yogur": "¿Qué le dijo un yogur a otro? ¡Qué lindo estar en la heladera, te veo muy fresco! 🥛",
    "zanahoria": "¡La zanahoria es muy buena para la vista! ¿O acaso viste a un conejo con anteojos? 🐰",
    "pera": "¿Qué le dijo una pera a otra? ¡Pera, pera, esperame que ya voy! 🍐",
    "durazno": "¿Qué le dijo el durazno al carozo? ¡Vos sos el corazón de esta familia! 🍑",
    "anana": "¿Qué le dijo un ananá a otro? ¡Qué lindo peinado que tenés! 🍍",
    "sandia": "¿Por qué la sandía se fue a nadar? ¡Porque estaba llena de agua y quería más! 🍉",
    "kiwi": "¿Por qué el kiwi fue a la peluquería? ¡Porque estaba muy despeinado! 🥝",
    "limon": "¿Qué le dijo un limón a otro? ¡Qué cara de ácido tenés hoy! 🍋",
    "mango": "¿Por qué el mango siempre baila? ¡Porque le encanta el ritmo tropical! 🥭",
    "cereza": "¿Qué le dijo una cereza a otra? ¡Siempre juntitas, como orejitas! 🍒",
    "alfajor": "¿Qué le dijo un alfajor a otro? ¡Qué bien nos abrazamos con tanto dulce en el medio! 🍪",
    "chocolate": "¿Por qué el chocolate nunca se pelea con nadie? ¡Porque se derrite de amor! 🍫",
    "gomitas": "¿Por qué las gomitas son tan flexibles? ¡Porque hacen yoga todos los días! 🐻",
    "caramelos": "¿Qué le dijo un caramelo a otro? ¡Qué bien que nos envolvieron para viajar juntos! 🍬",
    "malvaviscos": "¿Por qué el malvavisco es tan blandito? ¡Porque duerme sobre una nube todas las noches! ☁️",
    "sandwich_milanesa": "¿Qué le dijo la milanesa al pan? ¡Quedate cerca, que juntos somos un sándwich de campeones! 🥪",
}

con = sqlite3.connect("nutriapp.db")
columnas = [c[1] for c in con.execute("PRAGMA table_info(alimentos)")]
if "chiste" not in columnas:
    con.execute("ALTER TABLE alimentos ADD COLUMN chiste TEXT")
for nombre, chiste in CHISTES.items():
    con.execute("UPDATE alimentos SET chiste = ? WHERE nombre = ?", (chiste, nombre))
con.commit()
sin_chiste = [r[0] for r in con.execute("SELECT nombre FROM alimentos WHERE chiste IS NULL")]
con.close()

print("Chistes cargados:", len(CHISTES))
print("Alimentos sin chiste:", sin_chiste)