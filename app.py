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
        margin: 40px auto 20px auto;
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
        margin-bottom: 10px;
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

# Status-Speicher
if "step" not in st.session_state:
    st.session_state.step = 1

# --- SCHRITT 1: Die Hauptfrage ---
if st.session_state.step == 1:
    st.markdown("""
        <div class="dark-card">
            <div class="main-title">Kurze Frage an dich</div>
            <div class="sub-title">Hättest du Lust, die Tage mal mit mir zu telefonieren?</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sehr gerne", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

    with col2:
        # Der fangbare Ausweich-Button
        components.html("""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body { margin: 0; padding: 0; background: transparent; }
                #noBtn {
                    background-color: #1f232d;
                    color: #ffffff;
                    border: 1px solid #363b48;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-size: 15px;
                    font-weight: 500;
                    cursor: pointer;
                    width: 100%;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    box-sizing: border-box;
                    transition: left 0.18s ease-out, top 0.18s ease-out;
                    user-select: none;
                    white-space: nowrap;
                }
                #noBtn:hover {
                    background-color: #2b303e;
                }
            </style>
            </head>
            <body>
                <button id="noBtn" onmouseenter="dodge()" onclick="dodge()">Eher nicht</button>
                <script>
                let escapes = 0;
                function dodge() {
                    const btn = document.getElementById('noBtn');
                    escapes++;
                    
                    // Button wird fest auf dem Bildschirm verankert
                    btn.style.position = 'fixed';
                    btn.style.width = '140px';
                    btn.style.zIndex = '99999';

                    // Sichtbare Fenstermaße ermitteln mit 40px Rand als Puffer
                    const btnWidth = 140;
                    const btnHeight = 45;
                    const padding = 40;
                    
                    const screenWidth = window.top.innerWidth || window.innerWidth;
                    const screenHeight = window.top.innerHeight || window.innerHeight;
                    
                    const maxX = Math.max(padding, screenWidth - btnWidth - padding);
                    const maxY = Math.max(padding, screenHeight - btnHeight - padding);

                    // Zufällige Koordinate, die garantiert im Sichtbereich bleibt
                    const randomX = Math.floor(Math.random() * (maxX - padding)) + padding;
                    const randomY = Math.floor(Math.random() * (maxY - padding)) + padding;

                    btn.style.left = randomX + 'px';
                    btn.style.top = randomY + 'px';

                    // Wechselnde Texte beim Jagen
                    if (escapes === 1) btn.innerText = "Zu langsam! 😜";
                    if (escapes === 3) btn.innerText = "Fast gehabt 😂";
                    if (escapes === 5) btn.innerText = "Gib auf 🏃‍♂️";
                    if (escapes === 7) btn.innerText = "Niemals 👻";
                }
                </script>
            </body>
            </html>
        """, height=60)

# --- SCHRITT 2: Datum & Uhrzeit ---
elif st.session_state.step == 2:
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
        st.rerun()

# --- SCHRITT 3: Bestätigung ---
elif st.session_state.step == 3:
    st.markdown(f"""
        <div class="dark-card">
            <div class="main-title">Abgemacht.</div>
            <div class="sub-title" style="margin-top: 15px;">
                Ich melde mich am <b style="color:#fff;">{st.session_state.tag.strftime('%d.%m.%Y')}</b> um <b style="color:#fff;">{st.session_state.uhrzeit.strftime('%H:%M')} Uhr</b> bei dir.
            </div>
        </div>
    """, unsafe_allow_html=True)
