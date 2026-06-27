import streamlit as st

st.set_page_config(page_title="Shopping Assistant", page_icon="🛍️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F7F8FC; }
#MainMenu, footer, header { visibility: hidden; }
.hero { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; color: white; }
.hero h1 { margin: 0 0 6px; font-size: 1.7rem; font-weight: 700; }
.hero p { margin: 0; opacity: .85; font-size: .95rem; }
.chat-wrap { background: white; border-radius: 16px; padding: 20px 24px; box-shadow: 0 2px 12px rgba(0,0,0,.07); min-height: 300px; max-height: 420px; overflow-y: auto; margin-bottom: 16px; }
.bubble-row { display: flex; margin-bottom: 14px; }
.bubble-row.user { justify-content: flex-end; }
.bubble-row.bot { justify-content: flex-start; }
.bubble { max-width: 72%; padding: 11px 16px; border-radius: 18px; font-size: .92rem; line-height: 1.5; }
.bubble-row.user .bubble { background: #4F46E5; color: white; border-bottom-right-radius: 4px; }
.bubble-row.bot .bubble { background: #F0F0F5; color: #1a1a2e; border-bottom-left-radius: 4px; }
.intent-badge { display: inline-block; font-size: .72rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; padding: 2px 10px; border-radius: 999px; margin-bottom: 6px; background: #EEF2FF; color: #4F46E5; }
.avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.avatar.bot { background:#EEF2FF; margin-right:10px; }
.avatar.user { background:#4F46E5; color:white; margin-left:10px; }
.stTextInput > div > div > input { border-radius: 12px !important; border: 1.5px solid #C7D2FE !important; padding: 12px 16px !important; font-size: .93rem !important; background: white !important; }
.stTextInput > div > div > input:focus { border-color: #4F46E5 !important; box-shadow: 0 0 0 3px rgba(79,70,229,.15) !important; }
.stButton > button { background: #4F46E5 !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 12px 28px !important; font-weight: 600 !important; font-size: .93rem !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)


def classify_intent(user_query):
    q = user_query.lower()
    if "where" in q and "order" in q:
        return "Track Order", "You can track your package by clicking the link in your confirmation email."
    elif any(w in q for w in ["payment", "pay", "options"]):
        return "Payment Options", "We accept Visa, Mastercard, PayPal, and Apple Pay."
    elif any(w in q for w in ["return", "refund"]):
        return "Return / Refund", "To return an item, visit our Returns Portal and enter your Order ID."
    else:
        return "Unknown", "I didn't catch that. Try asking about your order, payment methods, or returns."


if "messages" not in st.session_state:
    st.session_state.messages = []


def handle_send(text):
    text = text.strip()
    if not text:
        return
    intent, reply = classify_intent(text)
    st.session_state.messages.append({"role": "user", "text": text})
    st.session_state.messages.append({"role": "bot", "text": reply, "intent": intent})


st.markdown("""
<div class="hero">
  <h1>Shopping Assistant</h1>
  <p>Ask me about your order, payment options, or returns.</p>
</div>
""", unsafe_allow_html=True)

chat_html = '<div class="chat-wrap">'
if not st.session_state.messages:
    chat_html += '''<div class="bubble-row bot">
      <div class="avatar bot">🤖</div>
      <div><div class="intent-badge">Welcome</div><br>
      <div class="bubble">Hi! How can I help you today?</div></div></div>'''

for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'<div class="bubble-row user"><div class="bubble">{msg["text"]}</div><div class="avatar user">👤</div></div>'
    else:
        chat_html += f'<div class="bubble-row bot"><div class="avatar bot">🤖</div><div><div class="intent-badge">{msg["intent"]}</div><br><div class="bubble">{msg["text"]}</div></div></div>'

chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Where is my order?"):
        handle_send("Where is my order?")
        st.rerun()
with col2:
    if st.button("Payment options"):
        handle_send("What are the payment options?")
        st.rerun()
with col3:
    if st.button("Return an item"):
        handle_send("I want to return an item")
        st.rerun()

user_text = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
if st.button("Send"):
    handle_send(user_text)
    st.rerun()
