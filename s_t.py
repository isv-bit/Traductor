import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Traductor de Voz",
    page_icon="🎤",
    layout="centered"
)

# ------------------ ESTILOS PRO ------------------
st.markdown("""
<style>

/* Fondo degradado */
.stApp {
    background: linear-gradient(135deg, #ff4b2b, #ff416c, #7f00ff);
    color: white;
}

/* Títulos */
.main-title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 20px;
    text-align: center;
    margin-bottom: 30px;
}

/* Tarjeta tipo glass */
.card {
    background: rgba(255, 255, 255, 0.15);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.3);
    margin-top: 20px;
}

/* Botones */
.stButton>button {
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    color: black;
    border-radius: 12px;
    height: 50px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.05);
    transition: 0.2s;
}

/* Selectbox y inputs */
.stSelectbox, .stTextInput {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<p class="main-title">🎤 TRADUCTOR PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Habla y traduce en tiempo real 🚀</p>', unsafe_allow_html=True)

# ------------------ IMAGEN ------------------
image = Image.open('OIG7.jpg')
st.image(image, width=220)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.subheader("📌 Cómo usar")
    st.write("""
    1. Presiona 🎤  
    2. Habla  
    3. Elige idiomas  
    4. Traduce y escucha  
    """)

# ------------------ CARD PRINCIPAL ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.write("🎧 Presiona el botón y habla")

stt_button = Button(label="🎤 ESCUCHAR AHORA", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }

    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# ------------------ RESULTADO ------------------
if result:
    if "GET_TEXT" in result:
        st.success("📝 Texto detectado:")
        st.write(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()
    text = str(result.get("GET_TEXT"))

    st.subheader("⚙️ Configuración")

    in_lang = st.selectbox(
        "Idioma de entrada",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )

    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"

    out_lang = st.selectbox(
        "Idioma de salida",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )

    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"

    english_accent = st.selectbox(
        "Acento",
        ("Defecto","Español","Reino Unido","Estados Unidos","Canada","Australia","Irlanda","Sudáfrica"),
    )

    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"

    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("Mostrar texto traducido")

    if st.button("🔊 TRADUCIR Y ESCUCHAR"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("### 🎧 Audio:")
        st.audio(audio_bytes, format="audio/mp3")

        if display_output_text:
            st.markdown("### 📄 Texto:")
            st.write(output_text)

    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)

    remove_files(7)

st.markdown('</div>', unsafe_allow_html=True)
