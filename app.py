import streamlit as st
import whisper
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

def save_analysis(
    filename,
    word_count,
    duration_seconds,
    wpm,
    filler_count,
    score
):

    conn = psycopg2.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO speeches
        (filename, words, duration, wpm, filler_count, score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
    (
        filename,
        word_count,
        duration_seconds,
        wpm,
        filler_count,
        score
    ))

    conn.commit()
    conn.close()

st.set_page_config(
    page_title="AI Public Speaking Coach",
    page_icon="🎤"
)

st.title("🎤 AI Public Speaking Coach")

uploaded_file = st.file_uploader(
    "Upload your speech",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file:

    save_path = os.path.join("uploads", uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    if st.button("Analyze Speech"):

        with st.spinner("Transcribing speech..."):

            model = whisper.load_model("base")

            result = model.transcribe(save_path)

        transcript = result["text"]

        st.subheader("Transcript")
        st.write(transcript)

        # --------------------
        # Speech Metrics
        # --------------------

        words = transcript.split()
        word_count = len(words)

        duration_seconds = result["segments"][-1]["end"]

        wpm = round((word_count / duration_seconds) * 60)

        st.subheader("📊 Speech Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Words", word_count)

        with col2:
            st.metric("Duration", f"{round(duration_seconds)} sec")

        with col3:
            st.metric("WPM", wpm)

        # --------------------
        # Filler Word Detection
        # --------------------

        filler_words = [
            "um",
            "uh",
            "like",
            "actually",
            "basically",
            "you know"
        ]

        transcript_lower = transcript.lower()

        filler_count = 0
        filler_stats = {}

        for filler in filler_words:
            count = transcript_lower.count(filler)

            filler_stats[filler] = count

            filler_count += count

        st.subheader("🗣️ Filler Word Analysis")

        st.metric("Total Filler Words", filler_count)

        for filler, count in filler_stats.items():

            if count > 0:
                st.write(f"**{filler}** : {count}")

        # --------------------
        # Speaking Score
        # --------------------

        score = 10

        if wpm < 100 or wpm > 180:
            score -= 2

        if filler_count > 10:
            score -= 2

        if filler_count > 20:
            score -= 2

        score = max(score, 1)

        save_analysis(
            uploaded_file.name,
            word_count,
            duration_seconds,
            wpm,
            filler_count,
            score
        )

        st.subheader("⭐ Speaking Score")

        st.metric("Overall Score", f"{score}/10")

        # --------------------
        # AI Coach Feedback
        # --------------------

        st.subheader("🤖 AI Coach Feedback")

        strengths = []
        improvements = []

        # WPM Analysis

        if 130 <= wpm <= 170:
            strengths.append("Good speaking pace.")

        elif wpm < 130:
            improvements.append("Try speaking a little faster.")

        else:
            improvements.append("Slow down your speech slightly.")

        # Filler Analysis

        if filler_count <= 5:
            strengths.append("Minimal filler words.")

        elif filler_count <= 10:
            improvements.append("Reduce filler words for better clarity.")

        else:
            improvements.append("Too many filler words. Practice speaking more deliberately.")

        # Word Count Analysis

        if word_count > 100:
            strengths.append("Good amount of spoken content.")

        else:
            improvements.append("Try expanding your ideas further.")

        # Display

        st.markdown("### ✅ Strengths")

        for item in strengths:
            st.write(f"• {item}")

        st.markdown("### 🔧 Areas To Improve")

        for item in improvements:
            st.write(f"• {item}")

        st.markdown("### 🎯 Suggested Exercise")

        if filler_count > 10:

            st.info(
                "Record a 1-minute speech and focus on replacing 'um' and 'uh' with silent pauses."
            )

        elif wpm > 170:

            st.info(
                "Practice reading a paragraph slowly while maintaining clarity."
            )

        elif wpm < 130:

            st.info(
                "Practice explaining a topic continuously for 60 seconds."
            )

        else:

            st.info(
                "Try a 2-minute speech on any topic while maintaining your current pace."
            )

        st.subheader("📈 Progress Dashboard")

        conn = psycopg2.connect(DATABASE_URL)

        query = """
        SELECT
            id,
            filename,
            wpm,
            filler_count,
            score
        FROM speeches
        ORDER BY id
        """

        df = pd.read_sql(query, conn)

        conn.close()

        if not df.empty:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Score",
                    round(df["score"].mean(), 1)
                )

            with col2:
                st.metric(
                    "Average WPM",
                    round(df["wpm"].mean(), 1)
                )

            with col3:
                st.metric(
                    "Average Fillers",
                    round(df["filler_count"].mean(), 1)
                )

        if len(df) > 1:

            score_fig = px.line(
                df,
                x="id",
                y="score",
                markers=True,
                title="Score Progress"
            )

            st.plotly_chart(
                score_fig,
                use_container_width=True
            )

        if len(df) > 1:

            wpm_fig = px.line(
                df,
                x="id",
                y="wpm",
                markers=True,
                title="Speaking Pace Trend"
            )

            st.plotly_chart(
                wpm_fig,
                use_container_width=True
            )
        # --------------------
        # Previous Analyses
        # --------------------

        st.subheader("📜 Previous Analyses")

        conn = psycopg2.connect(DATABASE_URL)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                filename,
                wpm,
                filler_count,
                score
            FROM speeches
            ORDER BY id DESC
            LIMIT 5
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            st.write(
                f"📄 {row[0]} | WPM: {row[1]} | Fillers: {row[2]} | Score: {row[3]}/10"
            )