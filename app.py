from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()

app = Flask(__name__)

# Context voor hotelvragen
HOTEL_CONTEXT = """
Je bent een vriendelijke hotelassistent. Je helpt gasten met hun vragen over het hotel.
Belangrijke info:

- Check-in: vanaf 15:00 uur
- Check-out: voor 11:00 uur
- Ontbijt: 07:00-10:00 uur
- Parkeren: gratis
- WiFi: gratis (Hotel_Guest)
- Zwembad: 08:00-20:00 uur
- Restaurant: 12:00-22:00 uur
- Kamers: airco, TV, minibar
- Annuleren: tot 24 uur van tevoren gratis
- Huisdieren: toegestaan (kleine toeslag)

Beantwoord alles in het Nederlands. Wees beleefd. Weet je iets niet? Verwijs naar de receptie.
"""

# Initialiseer GPT-4o mini
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Gebruik standaard input_key = "input"
memory = ConversationBufferMemory(
    memory_key="history",
    input_key="input",
    return_messages=True
)

# Prompt template met juiste variabelen
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=f"{HOTEL_CONTEXT}\n\nGespreksgeschiedenis:\n{{history}}\nGast: {{input}}\nAssistent:"
)

# ConversationChain met juiste prompt en memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)

@app.route('/')
def home():
    return render_template('index.html')  # Zorg dat deze file bestaat in templates/

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    try:
        response = conversation.predict(input=user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({
            'response': f"Er ging iets mis: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)
