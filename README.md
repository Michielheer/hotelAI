# Hotel Chatbot

Een eenvoudige chatbot voor hotelgasten die vragen kunnen stellen over het hotel.

## Functionaliteiten

- Beantwoordt vragen over check-in/check-out tijden
- Geeft informatie over faciliteiten (zwembad, restaurant, etc.)
- Beantwoordt vragen over WiFi, parkeren en meer
- Onthoudt de context van het gesprek

## Installatie

1. Kloon deze repository
2. Installeer de benodigde packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Maak een `.env` bestand met je OpenAI API key:
   ```
   OPENAI_API_KEY=jouw_api_key_hier
   ```

## Gebruik

### Flask versie

Start de Flask server:
```bash
python app.py
```

Open dan je browser op: http://localhost:5000

### Streamlit versie

Start de Streamlit app:
```bash
streamlit run streamlit_app.py
```

De app opent automatisch in je browser, of ga naar: http://localhost:8501

## Technische details

- Gebouwd met Flask/Streamlit voor de frontend
- Gebruikt LangChain en OpenAI voor de chatbot functionaliteit
- Maakt gebruik van ConversationBufferMemory voor het onthouden van gesprekken 