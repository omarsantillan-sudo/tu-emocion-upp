import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import io
import random

# CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title="Tu emoción UPP",
    page_icon="🧠",
    layout="centered"
)

# ESTILO PROFESIONAL
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    height: 50px;
    font-size: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# COLORES Y CONFIGURACIÓN DE EMOCIONES
emociones_config = {
    "Alegría": {"color": (255, 217, 61), "ojos": "feliz", "boca": "sonrisa"},
    "Tristeza": {"color": (77, 150, 255), "ojos": "triste", "boca": "triste"},
    "Enojo": {"color": (255, 76, 76), "ojos": "enojado", "boca": "enojado"},
    "Ansiedad": {"color": (255, 142, 60), "ojos": "ansioso", "boca": "ansioso"},
}

# PREGUNTAS
preguntas = [
    ("Cuando despiertas:", ["Motivado", "Cansado", "Molesto", "Preocupado"]),
    ("Cuando tienes problemas:", ["Lo resuelvo", "Lloro", "Me enojo", "Me preocupo"]),
    ("En clase:", ["Feliz", "Triste", "Molesto", "Ansioso"]),
    ("Cuando fallas:", ["Intento otra vez", "Me entristezco", "Me enojo", "Me preocupo"]),
    ("Con amigos:", ["Feliz", "Triste", "Molesto", "Ansioso"]),
    ("En examen:", ["Seguro", "Triste", "Enojado", "Ansioso"]),
    ("Cuando esperas:", ["Emocionado", "Triste", "Molesto", "Ansioso"]),
    ("Cuando te equivocas:", ["Aprendo", "Triste", "Molesto", "Ansioso"]),
    ("En grupo:", ["Cómodo", "Triste", "Molesto", "Ansioso"]),
    ("En casa:", ["Feliz", "Triste", "Molesto", "Ansioso"]),
    ("En futuro:", ["Feliz", "Triste", "Molesto", "Ansioso"]),
    ("Al aprender:", ["Feliz", "Triste", "Molesto", "Ansioso"]),
    ("Cuando pierdes:", ["Motivado", "Triste", "Molesto", "Ansioso"]),
    ("Cuando esperas resultado:", ["Seguro", "Triste", "Molesto", "Ansioso"]),
    ("Cuando algo cambia:", ["Motivado", "Triste", "Molesto", "Ansioso"]),
]

mapa = {
    0: "Alegría",
    1: "Tristeza",
    2: "Enojo",
    3: "Ansiedad"
}

archivo = "resultados_emociones.xlsx"

# CREAR ARCHIVO SI NO EXISTE
if not os.path.exists(archivo):
    df = pd.DataFrame(columns=["Nombre", "Grupo", "Emoción", "Fecha"])
    df.to_excel(archivo, index=False)

# FUNCIÓN PARA CREAR AVATAR PRO
def crear_avatar_pro(nombre, emocion):

    config = emociones_config[emocion]
    color = config["color"]

    img = Image.new("RGB", (500, 500), color)
    draw = ImageDraw.Draw(img)

    # brillo tipo Pixar
    for i in range(200):
        draw.ellipse(
            (random.randint(0,500), random.randint(0,500),
             random.randint(0,500), random.randint(0,500)),
            outline=(255,255,255,30)
        )

    # cara
    draw.ellipse((150, 120, 350, 320), fill=(255,255,255))

    # ojos según emoción
    if emocion == "Alegría":
        draw.ellipse((200,180,230,210), fill="black")
        draw.ellipse((270,180,300,210), fill="black")

    elif emocion == "Tristeza":
        draw.ellipse((200,190,230,210), fill="black")
        draw.ellipse((270,190,300,210), fill="black")

    elif emocion == "Enojo":
        draw.line((200,180,230,200), fill="black", width=4)
        draw.line((270,200,300,180), fill="black", width=4)

    elif emocion == "Ansiedad":
        draw.ellipse((200,180,235,215), outline="black", width=3)
        draw.ellipse((265,180,300,215), outline="black", width=3)

    # boca
    if emocion == "Alegría":
        draw.arc((200,220,300,280), 0, 180, fill="black", width=4)

    elif emocion == "Tristeza":
        draw.arc((200,240,300,300), 180, 360, fill="black", width=4)

    elif emocion == "Enojo":
        draw.line((210,260,290,260), fill="black", width=4)

    elif emocion == "Ansiedad":
        draw.arc((200,240,300,280), 180, 360, fill="black", width=3)

    # texto
    draw.text((180,350), nombre, fill="white")
    draw.text((180,400), emocion, fill="white")

    return img

# INTERFAZ
st.title("🧠 Tu emoción UPP")
st.write("Test socioemocional")

nombre = st.text_input("Nombre")
grupo = st.text_input("Grupo")

respuestas = []

for i, (pregunta, opciones) in enumerate(preguntas):
    r = st.radio(pregunta, opciones, key=i)
    respuestas.append(opciones.index(r))

if st.button("Descubrir mi emoción"):

    conteo = {
        "Alegría":0,
        "Tristeza":0,
        "Enojo":0,
        "Ansiedad":0
    }

    for r in respuestas:
        conteo[mapa[r]] += 1

    emocion_final = max(conteo, key=conteo.get)

    st.success(f"Tu emoción es: {emocion_final}")

    avatar = crear_avatar_pro(nombre, emocion_final)

    st.image(avatar)

    # GUARDAR EXCEL
    df = pd.read_excel(archivo)

    nuevo = pd.DataFrame({
        "Nombre":[nombre],
        "Grupo":[grupo],
        "Emoción":[emocion_final],
        "Fecha":[datetime.now()]
    })

    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_excel(archivo, index=False)

    # DESCARGA
    buf = io.BytesIO()
    avatar.save(buf, format="PNG")

    st.download_button(
        "Descargar Avatar",
        buf.getvalue(),
        f"{nombre}_avatar.png",
        "image/png"
    )
