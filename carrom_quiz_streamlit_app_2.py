import streamlit as st
import random
import time
import streamlit.components.v1 as components
import json
import os
import pandas as pd

st.set_page_config(page_title="Carrom Mastery Hub", layout="centered")


# ---------- Style ----------
st.markdown("""
<style>
div.stButton > button {
    background-color: #FFBF00;
    color: black;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #e6ac00;
    font-size: 18px !important;
    padding: 12px 24px !important;
}

html, body, [class*="css"] {
    font-size: 18px !important;
}

h1 { font-size: 36px !important; }
h2 { font-size: 30px !important; }
h3 { font-size: 24px !important; }

div[role="radiogroup"] label {
    font-size: 18px !important;
}

div.stButton > button {
    font-size: 18px !important;
    padding: 12px 24px !important;
}

</style>
""", unsafe_allow_html=True)


# ---------- Load Questions ----------
def load_questions():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading questions.json: {e}")
        return []


def generate_questions():
    data = load_questions()
    questions = []

    if not data:
        return []

    for i in range(500):
        base = data[i % len(data)]
        questions.append({
            "question": base["question"],
            "answer": base["answer"],
            "options": random.sample(base["options"], len(base["options"]))
        })
    return questions


# ---------- Leaderboard (Table, Top 5) ----------
LEADERBOARD_FILE = "leaderboard.json"


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def show_leaderboard(filter_questions=None):
    data = load_leaderboard()

    # Organize by category
    categories = [10, 20, 50, 100]

    def rank_badge(i):
        return "🥇 Gold" if i == 0 else "🥈 Silver" if i == 1 else "🥉 Bronze"

    st.markdown("## 🏆 Leaderboard (Top 3 per Category)")

    # Use Streamlit columns for categories
    cols = st.columns(len(categories))

    for col, q in zip(cols, categories):
        with col:
            st.markdown(f"### {q} Questions")

            # Filter and sort for category
            filtered = [d for d in data if int(d.get("questions", 0)) == q]
            filtered = sorted(filtered, key=lambda x: x["score"], reverse=True)[:3]

            if not filtered:
                st.info("Be First One to score")
                continue

            # Build table with badges
            table = {
                "Rank": [rank_badge(i) for i in range(len(filtered))],
                "Name": [entry["name"] for entry in filtered]
            }

            st.dataframe(table, use_container_width=False)  


def save_leaderboard(name, score, questions):
    data = load_leaderboard()
    data.append({
        "name": name,
        "score": score,
        "questions": questions,
        "time": time.strftime("%Y-%m-%d %H:%M")
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def calculate_score():
    total_attempted = st.session_state.right + st.session_state.wrong
    if total_attempted == 0:
        return 0
    return (st.session_state.right / total_attempted) * 100


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
        setTimeout(() => fireworks.stop(), 40000);
    </script>
    """, height=250)


def play_sound(correct=True):
    url = (
        "https://actions.google.com/sounds/v1/crowds/applause.ogg"
        if correct
        else "https://actions.google.com/sounds/v1/cartoon/boo.ogg"
    )
    st.audio(url, autoplay=True)


# ---------- Session State ----------
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "welcome"

if "question_bank" not in st.session_state:
    st.session_state.question_bank = generate_questions()

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "current" not in st.session_state:
    st.session_state.current = 0

if "right" not in st.session_state:
    st.session_state.right = 0

if "wrong" not in st.session_state:
    st.session_state.wrong = 0

if "skipped" not in st.session_state:
    st.session_state.skipped = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}


# ==========================================================
# ====================== WELCOME PAGE ======================
# ==========================================================
if st.session_state.app_stage == "welcome":

    st.title("🎯 Welcome to Carrom Mastery Hub")

    st.markdown("""
## Sharpen Your Skills. Test Your Knowledge.

## Whether you're a casual player or a passionate Carrom enthusiast,  
## this app is your interactive gateway to mastering the rules of the game.

## Dive into a fun, engaging, and skill-building experience designed for players at every level.

## Tap **Begin Quiz** to explore the world of Carrom rules in a fun, and structured way.

## Every question brings you one step closer to becoming a true Carrom pro.
""")

    if st.button("🚀 Begin Quiz", use_container_width=True):
        st.session_state.app_stage = "leaderboard"
        st.rerun()

    st.stop()


# ==========================================================
# ================== LEADERBOARD PAGE ======================
# (NEW PAGE)
# ==========================================================
if st.session_state.app_stage == "leaderboard":

    st.title("🏆 Leaderboard")

    show_leaderboard(100)

    if st.button("Continue to Quiz"):
        st.session_state.app_stage = "select"
        st.rerun()

    st.stop()

# ==========================================================
# ================== QUESTION COUNT SELECT =================
# ==========================================================
if st.session_state.app_stage == "select":

    st.title("📊 Choose Number of Questions")

    choice = st.radio(
        "How many questions would you like to attempt?",
        [10, 20, 50, 100],
        horizontal=False,
        index=None
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Begin Quiz", use_container_width=True):

            if choice is None:
                components.html("""
                <div style='color:red;font-weight:bold;font-size:18px;text-align:center;
                            animation: shake 0.5s;'>
                    ⚠ Please select at least one option to begin the quiz.
                </div>
                <style>
                @keyframes shake {
                    0% { transform: translateX(0); }
                    25% { transform: translateX(-5px); }
                    50% { transform: translateX(5px); }
                    75% { transform: translateX(-5px); }
                    100% { transform: translateX(0); }
                }
                </style>
                """, height=80)

            else:
                st.session_state.total_questions = choice
                st.session_state.quiz_questions = random.sample(
                    st.session_state.question_bank, choice
                )
                st.session_state.app_stage = "quiz"
                st.session_state.current = 0
                st.session_state.right = 0
                st.session_state.wrong = 0
                st.session_state.skipped = 0
                st.session_state.submitted = False
                st.session_state.selected_answers = {}
                st.rerun()

    with col2:
        if st.button("🏆 Show Leaderboard", use_container_width=True):
            st.session_state.app_stage = "leaderboard"
            st.rerun()

    st.stop()
# ==========================================================
# ========================= QUIZ ===========================
# ==========================================================
if st.session_state.app_stage == "quiz":

    if st.session_state.current >= st.session_state.total_questions:
        st.session_state.app_stage = "thankyou"
        st.rerun()

    q = st.session_state.quiz_questions[st.session_state.current]

    st.title(f"Question {st.session_state.current + 1} of {st.session_state.total_questions}")
    st.write("## " + q["question"])

    st.markdown(
        f"✅ Right: {st.session_state.right}   |   "
        f"❌ Wrong: {st.session_state.wrong}   |   "
        f"⏭ Skipped: {st.session_state.skipped}"
    )

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

        def format_option(option):
            if selected != q["answer"]:
                if option == q["answer"]:
                    return f"{option:<20}\t\t ✅ (Correct Answer)"
                elif option == selected:
                    return f"{option:<20}\t\t ❌ (You Answered)"
            return option

        st.radio(
            "Choose your answer:",
            q["options"],
            index=q["options"].index(selected),
            format_func=format_option,
            disabled=False,
            key=f"review_{st.session_state.current}"
        )

        if selected != q["answer"]:
            st.success(f"Correct Answer is: {q['answer']}")
        else:
            st.success("👏 Your Answer is Correct !!")

    col1, col2 = st.columns(2)

    with col1:
        label = "Strike" if not st.session_state.submitted else "Next Question"

        if st.button(label, use_container_width=True):

            if not st.session_state.submitted:
                if selected is None:
                    components.html("""
                    <div style='color:red;font-weight:bold;text-align:center;animation: shake 0.5s;'>
                    ⚠ Please select an answer.
                    </div>
                    """, height=50)
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

    st.stop()


# ==========================================================
# ===================== THANK YOU PAGE =====================
# ==========================================================
if st.session_state.app_stage == "thankyou":

    st.title("🎉 Thank You for taking this Quiz!")
    st.write(f"### Hope you have enjoyed this journey, If you have any suggestions or feedback feel free to reach out to me.")
    st.write(f"###\t\t\t\t\t                          -  Vishal Ghosalkar")
    
    
    if st.button("Check yor Final Score"):
        st.session_state.app_stage = "enter_name"
        st.rerun()

# ==========================================================
# ===================== ENTER NAME PAGE ====================
# ==========================================================
if st.session_state.app_stage == "enter_name":

    st.title("🏆 Enter your name.")

    st.write("### Last thing before you see your score. Enter the name you want print on the leaderboard.")

    name = st.text_input("Display Name")

    if st.button("Save & Continue"):

        if not name:
            st.warning("Please enter a name to continue.")
        else:
            score = calculate_score()
            save_leaderboard(name, score, st.session_state.total_questions)
            st.success("Score saved successfully!")
            
            time.sleep(1)
            st.session_state.app_stage = "completed"
            st.rerun()

    if st.button("Skip Saving name"):
        st.session_state.app_stage = "completed"
        st.rerun()

    
# ==========================================================
# ===================== COMPLETED PAGE =====================
# ==========================================================
if st.session_state.app_stage == "completed":

    st.title("🎉 Quiz Completed!")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 ReStart Quiz", use_container_width=True):
            st.session_state.app_stage = "select"
            st.rerun()

        total_attempted = st.session_state.right + st.session_state.wrong
        score = (st.session_state.right / total_attempted) * 100 if total_attempted > 0 else 0

        st.write(f"### Final Score: {score:.2f}%")
        st.write(f"✅ Right: {st.session_state.right} | ❌ Wrong: {st.session_state.wrong} | ⏭ Skipped: {st.session_state.skipped}")

        if score <= 50:
            st.error(" Keep Practicing!")
        elif score <= 80:
            st.warning("Nice Job ! Keep Practicing.")
        else:
            st.success("Awesome! Keep Practicing")
            show_fireworks()
            st.balloons()
        
    with col2:
        if st.button("🏆 Show Leaderboard", use_container_width=True):
            st.session_state.app_stage = "leaderboard"
            st.rerun()