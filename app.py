import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests

# 1. Seiten-Setup
st.set_page_config(page_title="Frage ☎️", page_icon="📞", layout="centered")

# 2. Modernes Dark-Design
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0c10;
        color: #f1f1f1;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .dark-card {
        background-color: #16181f;
        padding: 40px 30px;
        border-radius: 16px;
        border: 1px solid #282b36;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
        max-width: 440px;
        margin: 40px auto;
    }
    .main-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .sub-title {
        color: #9aa0a6;
        font-size: 15px;
        margin-bottom: 28px;
        line-height: 1.5;
    }
    div.stButton > button {
        background-color: #1f232d;
        color: #ffffff;
        border: 1px solid #363b48;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #2b303e;
        border-color: #5c6375;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Telegram-Daten
TELEGRAM_BOT_TOKEN = "8919322605:AAGrTOwGvLU2clKXabJ_NnFAdxDGtwxjApg"
TELEGRAM_CHAT_ID = "8480464169"

def send_telegram_notification(datum, zeit):
    text = (
        f"📞 *Neuer Termin eingetragen!*\n\n"
        f"📅 *Datum:* {datum.strftime('%d.%m.%Y')}\n"
        f"⏰ *Uhrzeit:* {zeit.strftime('%H:%M Uhr')}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Fehler: {e}")

# Schritt-Steuerung via URL/Query-Params & Session
current_step = st.query_params.get("step", "1")
if "step" in st.session_state:
    current_step = str(st.session_state.step)

# --- SCHRITT 1: Die Hauptfrage mit Ausweich-Button ---
if current_step == "1":
    interactive_card = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
        }
        .card {
            background-color: #16181f;
            width: 100%;
            max-width: 440px;
            padding: 35px 25px;
            border-radius: 16px;
            border: 1px solid #282b36;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            text-align: center;
            box-sizing: border-box;
            position: relative;
            min-height: 250px;
        }
        .title {
            color: #ffffff;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .sub {
            color: #9aa0a6;
            font-size: 15px;
            margin-bottom: 35px;
        }
        .btn-container {
            display: flex;
            justify-content: space-around;
            gap: 15px;
        }
        .btn {
            background-color: #1f232d;
            color: #ffffff;
            border: 1px solid #363b48;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
            user-select: none;
        }
        .btn:hover {
            background-color: #2b303e;
        }
        #noBtn {
            transition: all 0.15s ease-out;
        }
    </style>
    </head>
    <body>
        <div class="card" id="cardArea">
            <div class="title">Kurze Frage an dich</div>
            <div class="sub">Hättest du Lust, die Tage mal mit mir zu telefonieren?</div>
            <div class="btn-container">
                <button class="btn" onclick="accept()">Sehr gerne</button>
                <button class="btn" id="noBtn" onmouseover="flee()" onclick="flee()">Eher nicht</button>
            </div>
        </div>

        <script>
        function flee() {
            const btn = document.getElementById('noBtn');
            const card = document.getElementById('cardArea');
            const rect = card.getBoundingClientRect();
            
            const maxX = rect.width - 130;
            const maxY = rect.height - 60;
            
            const randomX = Math.floor(Math.random() * (maxX - 20)) + 20;
            const randomY = Math.floor(Math.random() * (maxY - 80)) + 80;
            
            btn.style.position = 'absolute';
            btn.style.left = randomX + 'px';
            btn.style.top = randomY + 'px';
        }

        function accept() {
            window.parent.location.search = '?step=2';
        }
        </script>
    </body>
    </html>
    """
    components.html(interactive_card, height=320)

# --- SCHRITT 2: Datum & Uhrzeit ---
elif current_step == "2":
    st.markdown("""
        <div class="dark-card">
            <div class="main-title">Wann passt es dir?</div>
            <div class="sub-title">Wähle einfach einen Tag und eine Uhrzeit aus:</div>
        </div>
    """, unsafe_allow_html=True)
    
    tag = st.date_input("Datum", min_value=datetime.date.today())
    uhrzeit = st.time_input("Uhrzeit", datetime.time(20, 0))
    
    if st.button("Termin bestätigen", use_container_width=True):
        st.session_state.tag = tag
        st.session_state.uhrzeit = uhrzeit
        send_telegram_notification(tag, uhrzeit)
        st.session_state.step = 3
        st.query_params["step"] = "3"
        st.rerun()

# --- SCHRITT 3: Bestätigung ---
elif current_step == "3":
    tag_str = st.session_state.get("tag", datetime.date.today()).strftime('%d.%m.%Y')
    zeit_str = st.session_state.get("uhrzeit", datetime.time(20, 0)).strftime('%H:%M')
    
    st.markdown(f"""
        <div class="dark-card">
            <div class="main-title">Abgemacht.</div>
            <div class="sub-title" style="margin-top: 15px;">
                Ich melde mich am <b style="color:#fff;">{tag_str}</b> um <b style="color:#fff;">{zeit_str} Uhr</b> bei dir.
            </div>
        </div>
    """, unsafe_allow_html=True)
