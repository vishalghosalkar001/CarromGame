import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Carrom Rules Quiz", layout="centered")

TOTAL_QUESTIONS = 1

# ---------- Amber Button Style ----------
st.markdown("""
<style>
div.stButton > button {
    background-color: #FFBF00;
    color: black;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #e6ac00;
}
</style>
""", unsafe_allow_html=True)


# ---------- Generate Questions ----------
def generate_questions():
    base_pool = [
        ("What is the red coin called?", "Queen",
         ["King", "Queen", "Master", "Red Coin"]),
        ("How many points are needed to win a game?", "25 points",
         ["21 points", "25 points", "30 points", "50 points"]),
        ("What is a foul in carrom?", "Violation of rules",
         ["Pocketing a coin", "Violation of rules", "Winning a board", "None"]),
        ("What happens if queen is pocketed but not covered?", "Queen is placed back on board",
         ["Player wins", "Queen is placed back on board", "No action", "Game ends"]),
        ("How long can a player take for a stroke?", "15 seconds",
         ["10 seconds", "15 seconds", "30 seconds", "No limit"]),
    ]

    questions = []
    for i in range(TOTAL_QUESTIONS):
        base = base_pool[i % len(base_pool)]
        questions.append({
            "question": base[0],
            "answer": base[1],
            "options": random.sample(base[2], len(base[2]))
        })
    return questions


# ---------- Fireworks ----------
def show_fireworks():
    components.html("""
    <div style='position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;
                display:flex;align-items:center;justify-content:center;
                '>
        <div id='fireworks'></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/fireworks-js@2.x/dist/index.umd.js"></script>
    <script>
        const container = document.getElementById('fireworks');
        const fireworks = new Fireworks.default(container);
        fireworks.start();
        setTimeout(() => fireworks.stop(), 4000);
    </script>
    """, height=220)


# ---------- Sound ----------
def play_sound(correct=True):
    url = (
        "https://actions.google.com/sounds/v1/crowds/applause.ogg"
        if correct
        else "https://actions.google.com/sounds/v1/cartoon/boo.ogg"
    )
    st.audio(url, autoplay=True)


# ---------- Session State ----------
if "questions" not in st.session_state:
    st.session_state.questions = generate_questions()
    st.session_state.current = 0
    st.session_state.right = 0
    st.session_state.wrong = 0
    st.session_state.skipped = 0
    st.session_state.submitted = False
    st.session_state.selected_answers = {}
    st.session_state.show_checkpoint = False

questions = st.session_state.questions


# ---------- Quiz Completed ----------
if st.session_state.current >= TOTAL_QUESTIONS:
    st.title("🎉 Quiz Completed!")

    total_attempted = st.session_state.right + st.session_state.wrong
    score = (st.session_state.right / total_attempted) * 100 if total_attempted > 0 else 0

    st.write(f"### Final Score: {score:.2f}%")
    st.write(f"✅ Right: {st.session_state.right} | ❌ Wrong: {st.session_state.wrong} | ⏭ Skipped: {st.session_state.skipped}")

    if score <= 70:
        st.error("Your carrom knowledge is basic. You must read the carrom rules and retry.")
    elif score <= 90:
        st.warning("Your carrom knowledge is intermediate. Keep practicing to improve.")
    else:
        st.success("Your carrom knowledge is advanced. Well done!")
        show_fireworks()
        st.balloons()

    if st.button("Retry Quiz"):
        st.session_state.clear()
        st.rerun()

    st.stop()


# ---------- 10 Question Checkpoint ----------
if (
    st.session_state.current > 0
    and st.session_state.current % 10 == 0
    and not st.session_state.show_checkpoint
):
    st.session_state.show_checkpoint = True

if st.session_state.show_checkpoint:
    st.markdown("### ⏸️ Completed 10 Questions")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Continue"):
            st.session_state.show_checkpoint = False
            st.rerun()

    with col2:
        if st.button("❌ Quit"):
            st.session_state.current = TOTAL_QUESTIONS
            st.session_state.show_checkpoint = False
            st.rerun()

    st.stop()


# ---------- Current Question ----------
q = questions[st.session_state.current]

st.title(f"Question {st.session_state.current + 1} of {TOTAL_QUESTIONS}")
st.write("## " + q["question"])

st.markdown(
    f"✅ Right: {st.session_state.right} | "
    f"❌ Wrong: {st.session_state.wrong} | "
    f"⏭ Skipped: {st.session_state.skipped}"
)


# ---------- Answer Section ----------
radiokey = f"radio_{st.session_state.current}"

if not st.session_state.submitted:
    selected = st.radio(
        "Choose your answer:",
        q["options"],
        index=None,
        key=radiokey
    )
else:
    selected = st.session_state.selected_answers.get(st.session_state.current)

    for option in q["options"]:
        if selected != q["answer"]:
            if option == q["answer"]:
                st.markdown(
                    f"<div style='background-color:#d4edda;padding:8px;border-radius:6px;margin-bottom:4px;'>🟢 {option}</div>",
                    unsafe_allow_html=True)
            elif option == selected:
                st.markdown(
                    f"<div style='background-color:#f8d7da;padding:8px;border-radius:6px;margin-bottom:4px;'>🔴 {option}</div>",
                    unsafe_allow_html=True)
            else:
                st.write(option)
        else:
            st.write(option)

    if selected != q["answer"]:
        st.error(f"Correct Answer is: {q['answer']}")
    else:
        st.success("👏 Correct Answer !!")


# ---------- Strike / Next Toggle + Skip ----------
col1, col2 = st.columns(2)

with col1:
    label = "Strike" if not st.session_state.submitted else "Next Question"

    if st.button(label, use_container_width=True):

        if not st.session_state.submitted:
            if selected is None:
                st.warning("Please select an answer.")
            else:
                st.session_state.submitted = True
                st.session_state.selected_answers[st.session_state.current] = selected

                if selected == q["answer"]:
                    st.session_state.right += 1
                    play_sound(True)
                else:
                    st.session_state.wrong += 1
                    play_sound(False)

                st.rerun()
        else:
            st.session_state.current += 1
            st.session_state.submitted = False
            time.sleep(0.2)
            st.rerun()

with col2:
    if not st.session_state.submitted:
        if st.button("Skip", use_container_width=True):
            st.session_state.skipped += 1
            st.session_state.current += 1
            st.rerun()