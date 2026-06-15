# OratorAI
AI-powered public speaking coach built with Python, Streamlit, Whisper and PostgreSQL.

OratorAI is an intelligent speech analysis platform that helps users improve their communication skills by analyzing recorded speeches and providing personalized feedback.

Built with **Python, Streamlit, Whisper, PostgreSQL, Pandas, and Plotly**, OratorAI tracks speaking performance over time and visualizes progress through interactive dashboards.

---

## ✨ Features

* 🎙️ Upload speech recordings
* 📝 Automatic speech transcription using OpenAI Whisper
* 📊 Speech metrics analysis

  * Word count
  * Speech duration
  * Words per minute (WPM)
* 🗣️ Potential filler word detection
* ⭐ Communication scoring system
* 🤖 Personalized coaching feedback
* 🎯 Suggested speaking exercises
* ☁️ PostgreSQL cloud database integration (Neon)
* 📜 History tracking of previous analyses
* 📈 Interactive progress dashboard
* 📉 Score and speaking pace trends using Plotly

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI

* OpenAI Whisper

### Database

* PostgreSQL (Neon)

### Data Analysis

* Pandas

### Visualization

* Plotly

---

## 📂 Project Structure

```
OratorAI
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── uploads/
└── venv/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/OratorAI.git
cd OratorAI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=YOUR_POSTGRES_CONNECTION_STRING
```

Run the application:

```bash
streamlit run app.py
```

---

## 📈 Current Capabilities

* Speech transcription
* Speech analytics
* Communication scoring
* Coaching recommendations
* PostgreSQL-based storage
* Historical analysis
* Progress tracking dashboard

---

## 🚀 Future Improvements

* Grammar analysis
* Vocabulary analysis
* Radar chart for communication dimensions
* Confidence scoring
* Better filler word detection
* Timestamp-based history
* User authentication
* Speech comparison between sessions
* Deploy to Streamlit Cloud

---

## 🎯 Motivation

Many students struggle with public speaking and communication. OratorAI aims to provide personalized feedback and progress tracking to help users become more confident speakers.

---

## 👨‍💻 Author

**Aakashh B**

Computer Science Engineering Student | Content Creator | Aspiring Software Engineer
