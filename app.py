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
        padding: 35px 25px;
        border-radius: 16px;
        border: 1px solid #282b36;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
        max-width: 440px;
        margin: 20px auto;
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
        margin-bottom: 15px;
        line-height: 1.5;
    }
    div.stButton > button {
        background-color: #1f232d;
        color: #ffffff;
        border: 1px solid #363b48;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #2b303e;
        border-color: #5c6375;
        color: #ffffff;
    }
    .stTextArea textarea {
        background-color: #12141a !important;
        color: #ffffff !important;
        border: 1px solid #363b48 !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Telegram-Daten
TELEGRAM_BOT_TOKEN = "8919322605:AAGrTOwGvLU2clKXabJ_NnFAdxDGtwxjApg"
TELEGRAM_CHAT_ID = "8480464169"

def send_telegram_notification(datum, zeit, notiz):
    notiz_text = notiz.strip() if notiz.strip() else "Keine Notiz hinterlassen."
    text = (
        f"📞 *Neuer Termin eingetragen!*\n\n"
        f"📅 *Datum:* {datum.strftime('%d.%m.%Y')}\n"
        f"⏰ *Uhrzeit:* {zeit.strftime('%H:%M Uhr')}\n\n"
        f"💬 *Nachricht von ihr:*\n\"{notiz_text}\""
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

# Schritt-Steuerung
step = st.query_params.get("step", "1")
if "step" in st.session_state:
    step = str(st.session_state.step)

if "nachricht" not in st.session_state:
    st.session_state.nachricht = ""

# --- SCHRITT 1: Die Jagd-Karte ---
if step == "1":
    components.html("""
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
            height: 380px;
            padding: 35px 25px;
            border-radius: 16px;
            border: 1px solid #282b36;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            text-align: center;
            box-sizing: border-box;
            position: relative;
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
            margin-bottom: 25px;
        }
        .btn {
            background-color: #1f232d;
            color: #ffffff;
            border: 1px solid #363b48;
            border-radius: 10px;
            padding: 12px 20px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            box-sizing: border-box;
            user-select: none;
            transition: background 0.2s;
        }
        .btn:hover {
            background-color: #2b303e;
        }
        #yesBtn {
            position: absolute;
            bottom: 40px;
            left: 35px;
            width: 150px;
        }
        #noBtn {
            position: absolute;
            bottom: 40px;
            right: 35px;
            width: 150px;
            transition: left 0.15s ease-out, top 0.15s ease-out;
            white-space: nowrap;
        }
    </style>
    </head>
    <body>
        <div class="card" id="arena">
            <div class="title">Kurze Frage an dich</div>
            <div class="sub">Hast du Lust mit mir zu telefonieren?</div>

            <a href="/?step=2" target="_top" class="btn" id="yesBtn">Sehr gerne</a>
            <button class="btn" id="noBtn" onmouseover="dodge()" onclick="dodge()">Eher nicht</button>
        </div>

        <script>
        let counter = 0;
        function dodge() {
            const btn = document.getElementById('noBtn');
            const arena = document.getElementById('arena');
            counter++;

            const minX = 20;
            const maxX = arena.clientWidth - 170;
            const minY = 120;
            const maxY = arena.clientHeight - 60;

            const randomX = Math.floor(Math.random() * (maxX - minX + 1)) + minX;
            const randomY = Math.floor(Math.random() * (maxY - minY + 1)) + minY;

            btn.style.left = randomX + 'px';
            btn.style.top = randomY + 'px';
            btn.style.bottom = 'auto';
            btn.style.right = 'auto';

            if (counter === 2) btn.innerText = "musst schneller sein";
            if (counter === 4) btn.innerText = "nein akzeptier ich nicht";
            if (counter === 6) btn.innerText = "so wird es nichts";
        }
        </script>
    </body>
    </html>
    """, height=420)

# --- SCHRITT 2: Datum, Uhrzeit & Nachricht ---
elif step == "2":
    st.markdown("""
        <div class="dark-card">
            <div class="main-title">Wann passts für dich?</div>
            <div class="sub-title">Wähl einen Tag und eine Uhrzeit aus:</div>
        </div>
    """, unsafe_allow_html=True)
    
    tag = st.date_input("Datum", min_value=datetime.date.today())
    uhrzeit = st.time_input("Uhrzeit", datetime.time(20, 0))
    
    st.markdown("<p style='font-size: 13px; color: #9aa0a6; margin-bottom: 5px;'>Schnell-Antworten:</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Kaffee steht bereit ☕"):
            st.session_state.nachricht = "Kaffee steht bereit ☕"
            st.rerun()
    with c2:
        if st.button("Sei pünktlich! ⏰"):
            st.session_state.nachricht = "Sei pünktlich! ⏰"
            st.rerun()
    with c3:
        if st.button("Freu mich schon ✨"):
            st.session_state.nachricht = "Freu mich schon ✨"
            st.rerun()

    notiz = st.text_area("Möchtest du mir noch was sagen? (optional)", value=st.session_state.nachricht, placeholder="Schreib hier was rein...")
    
    if st.button("Termin bestätigen", use_container_width=True):
        st.session_state.tag = tag
        st.session_state.uhrzeit = uhrzeit
        st.session_state.notiz = notiz
        send_telegram_notification(tag, uhrzeit, notiz)
        st.session_state.step = 3
        st.query_params["step"] = "3"
        st.rerun()

# --- SCHRITT 3: Bestätigung ---
elif step == "3":
    st.balloons()
    tag_val = st.session_state.get("tag", datetime.date.today()).strftime('%d.%m.%Y')
    zeit_val = st.session_state.get("uhrzeit", datetime.time(20, 0)).strftime('%H:%M')
    notiz_val = st.session_state.get("notiz", "").strip()
    
    notiz_box = f"<br><br><i>Deine Notiz: „{notiz_val}“</i>" if notiz_val else ""
    
    st.markdown(f"""
        <div class="dark-card">
            <div class="main-title">Abgemacht.</div>
            <div class="sub-title" style="margin-top: 15px;">
                Ich meld mich am <b style="color:#fff;">{tag_val}</b> um <b style="color:#fff;">{zeit_val} Uhr</b> bei dir Süsse.{notiz_box}
            </div>
        </div>
    """, unsafe_allow_html=True)
