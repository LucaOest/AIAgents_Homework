import gradio as gr
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

llm = Ollama(model="mistral:instruct", model_provider="ollama", request_timeout=300)

def get_response_from_model(user_input):
    prompt = f"""
    # Frage

    {user_input}

    # Identität

    Du bist Ernährungsberater. Gib dem Nutzer Hinweise, ob sein Essverhalten gesund, oder ungesund ist.

    # Anweisungen

    1. Antworte nur aufgrund der Dir gegebenen Richtwerte.
    2. Sollte der Nutzer die angegebenen Richtwerte nicht erfüllen, so teile dies mit.
    3. Je näher der Nutzer an den genannten Richtwerten liegt, desto besser, außer bei den Werten gesättigte Fettsäuren und Zucker; dort sind die Werte besser, je niedriger sie sind.
    4. Nenne in Form einer Tabelle, welche Richtwerte nicht erfüllt wurden.

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
    response = llm.chat(messages)
    return response.message.content

# Gradio-Oberfläche
def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Ernährungsberater KI")
        gr.Markdown("Gib deine Nährwertinformationen ein und erhalte eine Antwort.")
        
        user_input = gr.Textbox(label="Was hast du heute gegessen?", placeholder="Z. B. 400kcal, 70g Zucker...")
        output = gr.Textbox(label="Antwort vom Ernährungsberater")

        user_input.submit(get_response_from_model, inputs=user_input, outputs=output)

    demo.launch()

create_gradio_interface()
