import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# Init LLM
llm = Ollama(model="mistral:instruct", model_provider="ollama", request_timeout=300)

# Richtwerte für späteres Nachschlagen (optional)
richtwerte = {
    "Energie": "2250 kcal",
    "Eiweiß (Protein)": "60 g",
    "Fett (gesamt)": "75 g",
    "gesättigte Fettsäuren": "maximal 22 g",
    "Kohlenhydrate": "275 g",
    "Zucker": "maximal 50 g",
    "Ballaststoffe": "30 g",
    "Wasser": "2000 ml",
}

# Titel
st.title("🥗 Ernährungs-Check mit KI")
st.write("Gib deine täglichen Nährwerte ein und erfahre, ob sie gesund sind.")

# Chatverlauf
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chatverlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Prompt
if user_input := st.chat_input("Was hast du heute gegessen (z. B. kcal, Zucker etc.)?"):
    # Anzeige User-Eingabe
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = f"""
# Frage

{user_input}

# Identität

Du bist Ernährungsberater. Gib dem Nutzer Hinweise, ob sein Essverhalten gesund, oder ungesund ist.

# Anweisungen

1. Antworte nur aufgrund der Dir gegebenen Richtwerte
2. Sollte der Nutzer die angegebenen Richtwerte nicht erfüllen, so teile dies mit.
3. Je näher der Nutzer an den genannten Richtwerten liegt, desto besser, außer bei den Werten gesättigte Fettsäuren und Zucker; dort sind die Werte besser, je niedriger sie sind.
4. Nenne in Form einer Tabelle, welche Richtwerte nicht erfüllt wurden

# Richtwerte
Energie: 2250 kcal
Eiweiß (Protein): 60 g
Fett (gesamt): 75 g
gesättigte Fettsäuren: maximal 22 g
Kohlenhydrate: 275 g
Zucker: maximal 50 g
Ballaststoffe: 30 g
Wasser: 2000 ml
"""

    messages = [ChatMessage(role="user", content=prompt)]
    try:
        response = llm.chat(messages)
        answer = response.message.content
    except Exception as e:
        answer = f"Fehler beim Modellabruf: {e}"

    # Anzeige Antwort
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
