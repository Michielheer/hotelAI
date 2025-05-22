import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()

# Context voor hotelvragen
HOTEL_CONTEXT = """
Je bent een vriendelijke hotelassistent. Je helpt gasten met hun vragen over het hotel.
Belangrijke info:

- Check-in: vanaf 15:00 uur bij de receptie (vroege check-in mogelijk tegen toeslag)
- Check-out: voor 11:00 uur (late check-out mogelijk tot 14:00 uur tegen toeslag van €30)
- Ontbijt: 07:00-10:00 uur in het restaurant (weekends tot 11:00 uur)
- Ontbijtkosten: inbegrepen bij de kamerprijs, €15 voor externe gasten
- Parkeren: gratis voor hotelgasten, 100 plaatsen beschikbaar
- WiFi: gratis in het hele hotel, netwerknaam: 'Hotel_Guest', wachtwoord bij receptie
- Zwembad: 08:00-20:00 uur, verwarmd binnenzwembad met sauna
- Sauna: 10:00-20:00 uur, handdoekservice beschikbaar
- Fitness: 24 uur geopend met je kamerpas
- Restaurant: 12:00-22:00 uur, reserveren aanbevolen
- Bar: 16:00-01:00 uur
- Roomservice: 07:00-22:00 uur, menukaart op de kamer
- Kamers: airco, TV, minibar, koffie/thee faciliteiten, gratis toiletartikelen
- Kamertypes: Standaard, Superior, Deluxe en Suite
- Prijzen: vanaf €89 per nacht voor een standaardkamer
- Huisdieren: toegestaan in specifieke kamers tegen toeslag van €15 per nacht
- Annuleren: tot 24 uur van tevoren gratis, daarna 100% kosten
- Bagage: gratis bagageopslag bij receptie
- Strijkservice: beschikbaar, vraag bij receptie
- Wasservice: inleveren voor 10:00 uur, terug dezelfde dag
- Taxi: kan worden geregeld bij de receptie
- Openbaar vervoer: bushalte op 100m, metrostation op 500m
- Toeristische attracties: stadscentrum op 1,5 km, museum op 800m
- Noodgevallen: receptie 24/7 bereikbaar via telefoon (kies 9)
- Kinderen: kinderbedje beschikbaar op aanvraag, kinderhoek in restaurant
- Vergaderruimtes: 3 zalen beschikbaar, capaciteit tot 50 personen
- Speciale wensen: geef aan bij reservering of neem contact op met receptie

Beantwoord alles in de taal waarin de gebruiker het stelt. Wees beleefd en behulpzaam. Weet je iets niet? Verwijs naar de receptie.
"""

# Pagina configuratie
st.set_page_config(
    page_title="Hotel Assistent",
    page_icon="🏨",
    layout="centered"
)

# Titel en beschrijving
st.title("🏨 Hotel Assistent")
st.markdown("Welkom bij onze hotel chatbot! Stel een vraag over ons hotel.")

# Initialiseer sessie state voor chat geschiedenis
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialiseer LLM en memory
@st.cache_resource
def get_conversation_chain():
    # Eenvoudigere instantiatie zonder extra parameters
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Geen OpenAI API key gevonden! Voeg een OPENAI_API_KEY toe aan je .env bestand of Streamlit secrets.")
        st.stop()
        
    llm = ChatOpenAI(
        model="gpt-4o",  # Gebruik gpt-4o-mini
        temperature=0.7,
        api_key=api_key  # Gebruik api_key in plaats van openai_api_key
    )
    
    memory = ConversationBufferMemory(
        memory_key="history",
        input_key="input",
        return_messages=True
    )
    
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=f"{HOTEL_CONTEXT}\n\nGespreksgeschiedenis:\n{{history}}\nGast: {{input}}\nAssistent:"
    )
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=False
    )
    
    return conversation

conversation = get_conversation_chain()

# Toon berichten uit geschiedenis
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accepteer gebruikersinvoer
if prompt := st.chat_input("Stel een vraag over het hotel..."):
    # Toon gebruikersbericht
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Voeg toe aan geschiedenis
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Genereer antwoord
    with st.chat_message("assistant"):
        with st.spinner("Even denken..."):
            response = conversation.predict(input=prompt)
            st.markdown(response)
    
    # Voeg toe aan geschiedenis
    st.session_state.messages.append({"role": "assistant", "content": response})

# Voeg wat styling toe
st.markdown("""
<style>
.stChatMessage {
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Voeg footer toe
st.markdown("---")
st.markdown("Ontwikkeld voor Hotel Gasten - Heeft u hulp nodig? Bel de receptie: 123") 