# WhatsApp Chat Analyzer

A dark-themed Streamlit dashboard for analyzing WhatsApp `.txt` exports.

## Features
- Chat overview, participant statistics, activity charts, emoji and word analysis
- Rule-based sentiment overview and local Smart Q&A
- Optional Gemini AI assistant (requires explicit consent before sending excerpts)
- Chat summary/story, possible event extraction, multi-chat comparison and interactive replay
- Interaction network approximation, historical activity baseline and message explorer
- PDF and CSV exports
- **WhatsApp Wrapped** yearly recap
- **Smart Chat Search** with ranked evidence excerpts and CSV export
- **Decision & Task Tracker** for candidate actions, agreements, deadlines and budget messages
- **Reply Time Analytics** (adjacent-message response-gap approximation)

## Run locally (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Upload a WhatsApp chat exported as a `.txt` file. For comparison, optionally upload a second export.

## Optional Gemini setup
1. Create a key at https://aistudio.google.com/apikey
2. Create `.streamlit/secrets.toml` with:
   ```toml
   GEMINI_API_KEY = "YOUR_API_KEY"
   ```
3. Restart Streamlit. Never commit `secrets.toml` or expose the key in screenshots/source control.

## Important limitations
- Search ranking uses query terms and a small related-term dictionary; it is not a true embedding-based semantic search engine.
- Decision/event extraction is heuristic and must be checked against original messages.
- Reply-time analytics estimates gaps between adjacent messages by different senders; it cannot reliably identify direct replies, especially in group chats.
- Sentiment is a basic keyword heuristic, not a validated emotion model.
- Interaction edges are approximated from consecutive messages.
- Gemini sends relevant chat excerpts to Google's service only after the user enables the consent checkbox. Avoid uploading sensitive conversations unless you have permission.
