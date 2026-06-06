import streamlit as st
from db import SessionLocal
from models.question import Question
from datetime import date
import random

st.set_page_config(
    page_title="LeetCode Revision Assistant",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 LeetCode Revision Assistant")


def get_revision_questions(questions):
    easy = [q for q in questions if q.difficulty == "Easy"]
    medium = [q for q in questions if q.difficulty == "Medium"]

    selected = []

    if len(easy) >= 4:
        selected.extend(random.sample(easy, 4))
    else:
        selected.extend(easy)

    if len(medium) >= 1:
        selected.extend(random.sample(medium, 1))

    if len(selected) < 5:
        remaining = [q for q in questions if q not in selected]
        selected.extend(
            random.sample(remaining, min(5 - len(selected), len(remaining)))
        )

    random.shuffle(selected)
    return selected


session = SessionLocal()

try:
    questions = session.query(Question).all()

    total = len(questions)
    easy = len([q for q in questions if q.difficulty == "Easy"])
    medium = len([q for q in questions if q.difficulty == "Medium"])
    hard = len([q for q in questions if q.difficulty == "Hard"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Questions", total)
    col2.metric("Easy", easy)
    col3.metric("Medium", medium)
    col4.metric("Hard", hard)

    st.divider()

    st.subheader("⏱️ Revision Session")
    st.info("Solve today's 5 questions in a 60-minute focused session.")

    st.markdown("### 🍅 Pomodoro Timer")
    st.markdown("https://pomofocus.io")

    st.divider()

    st.subheader("📚 Today's Revision Questions")

    if total > 0:
        daily = get_revision_questions(questions)

        for i, q in enumerate(daily, start=1):
            st.markdown(f"### {i}. {q.title}")

            if q.difficulty:
                st.write(f"Difficulty: {q.difficulty}")

            if q.slug:
                st.markdown(f"https://leetcode.com/problems/{q.slug}/")

            st.write(f"Times Revised: {q.times_revised or 0}")
            st.write(f"Last Revised: {q.last_revised}")

            if st.button(f"✅ Mark Practiced ({q.id})"):
                db_q = session.query(Question).filter_by(id=q.id).first()
                db_q.times_revised = (db_q.times_revised or 0) + 1
                db_q.last_revised = date.today()
                session.commit()
                st.success(f"{q.title} updated!")
                st.rerun()
    else:
        st.warning("No questions found. Run sync/import first.")

    st.divider()

    st.subheader("📋 All Questions")

    data = []
    for q in questions:
        data.append(
            {
                "ID": q.id,
                "Title": q.title,
                "Difficulty": q.difficulty,
                "Times Revised": q.times_revised,
                "Last Revised": q.last_revised,
                "Slug": q.slug,
            }
        )

    st.dataframe(data, use_container_width=True)

finally:
    session.close()