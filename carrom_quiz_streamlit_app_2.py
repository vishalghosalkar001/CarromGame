import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Carrom Mastery Hub", layout="centered")

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
    font-size: 18px !important;
    padding: 12px 24px !important;
}

    /* Increase base font size */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }

    /* Headings bigger */
    h1 {
        font-size: 36px !important;
    }

    h2 {
        font-size: 30px !important;
    }

    h3 {
        font-size: 24px !important;
    }

    /* Radio and labels */
    div[role="radiogroup"] label {
        font-size: 18px !important;
    }

  
    div.stButton > button {
        font-size: 18px !important;
        padding: 12px 24px !important;
    }


</style>
""", unsafe_allow_html=True)


# ---------- Generate Large Question Bank ----------
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
         
        ("What does C/B stand for?", "Carrom Board",
         ["Carrom Board", "Carrom Ball", "Carrom Base", "Carrom Brick"]),

        ("What does C/m stand for?", "Carromman / Carrommen",
         ["Carrom Move", "Carromman / Carrommen", "Carrom Match", "Carrom Material"]),

        ("What is a Break in carrom?", "The first stroke of a board",
         ["First pocket", "The first stroke of a board", "Penalty stroke", "Queen shot"]),

        ("What does Placing mean?", "Keeping penalty or due coins in outer circle in flat position",
         ["Pocketing coins", "Keeping penalty or due coins in outer circle in flat position",
          "Moving coins anywhere", "Holding coins in hand"]),

        ("Where should a jumped coin or Queen be placed?", "Centre Circle by the umpire",
         ["Outer circle by player", "Centre Circle by the umpire",
          "Near pocket", "Any position"]),

        ("What is Pocketing?", "Putting C/m or Queen into pocket by proper or improper stroke",
         ["Moving coin", "Putting C/m or Queen into pocket by proper or improper stroke",
          "Touching coin", "Covering queen"]),

        ("What does Due mean?", "Pocketing the striker with or without coins or outstanding penalty",
         ["Bonus points", "Penalty to place coin",
          "Pocketing the striker with or without coins or outstanding penalty", "Extra turn"]),

        ("What is Penalty?", "Punishment for rule violation",
         ["Reward", "Punishment for rule violation",
          "Extra turn", "Loss of points"]),

        ("What is Covering the Queen?", "Pocketing own coin in same or next stroke after queen",
         ["Pocketing only queen", "Pocketing own coin in same or next stroke after queen",
          "Moving queen", "Touching queen"]),

        ("What is a Cannon?", "Two coins or coin and queen facing pocket without space",
         ["Two coins place with space", "Two coins or coin and queen facing pocket without space",
          "Direct pocket shot", "Illegal shot"]),

        ("What is Thumbing?", "Taking stroke using the thumb",
         ["Using finger", "Taking stroke using the thumb", "Using palm", "No stroke"]),

        ("What does Turn mean?", "Right to strike",
         ["Chance to speak", "Right to strike",
          "Extra move", "Board start"]),

        ("Who is an Umpire?", "Official supervising and controlling the match",
         ["Player", "Official supervising and controlling the match", "Spectator", "Organizer"]),

        ("What does Hand mean in rules?", "Portion of playing hand from fingers to wrist",
         ["Whole arm", "Fingers only", "Portion of playing hand from fingers to wrist", "Elbow area"]),

        ("What is a Stroke?", "Hitting the C/m by striker directly or indirectly",
         ["Moving hand", "Hitting the C/m by striker directly or indirectly",
          "Pocketing coin", "Placing coin"]),

        ("What is White Slam?", "Pocketing all nine white coins and queen in first turn",
         ["Pocket queen only", "Pocketing all nine white coins and queen in first turn", "Pocketing all black coins with or without queen in first turn", "Partial pocket"]),
        
        ("What is Black Slam?", "Pocketing all remaining black coins with or without queen in first turn",
         ["Pocket only black coins", "Pocketing all remaining black coins with or without queen in first turn",
          "Pocket queen only", "Pocketing all remaining white coins with or without queen in first turn"]),
                
        ("What are Imaginary Lines in carrom?", 
        "Lines extended from arrows between base circles",
         ["Lines drawn on board", 
          "Lines extended from arrows between base circles", 
          "Lines around pockets", 
          "Lines for seating"]),

        ("Can a player change sitting position during turn?", 
        "Yes, but chair or stool must not be moved",
         ["No, never", 
          "Yes, but chair or stool must not be moved", 
          "Only after game", 
          "Anytime"]),

        ("During the board, what part of body may touch the board?", 
         "Only the playing arm",
         ["Hand and elbow", 
          "Only the playing arm", 
          "Legs and hands", 
          "Any body part"]),

        ("Can wearing items (Bracelets/Bangles/) touch playing surface during turn?", 
         "No, they must not touch the playing surface",
         ["Yes, always allowed", 
          "No, they must not touch the playing surface", 
          "Only rings allowed", 
          "Only watches allowed"]),

        ("What is the maximum seat height allowed after board?", 
         "50 cm",
         ["40 cm", 
          "50 cm", 
          "60 cm", 
          "No limit"]),

        ("How far can body go beyond imaginary lines?", 
         "No part except hand",
         ["Whole body", 
          "No part except hand", 
          "Elbow allowed", 
          "Head allowed"]),

        ("How should the striker be used?", 
         "It must be struck, not pushed",
         ["Pushed gently", 
          "It must be struck, not pushed", 
          "Dragged", 
          "Touched lightly"]),

        ("How should stroke be made?", 
         "With finger (with or without support of other fingers)",
         ["With palm", 
          "With finger (with or without support of other fingers)", 
          "With any object", 
          "With thumb"]),

        ("Which hands can be used to play?", 
         "Any hand",
         ["Only right hand", 
          "Any hand", 
          "Only playing hand", 
          "Only left hand"]),

        ("Can hand touch playing surface during stroke?", 
         "Yes",
         ["No", 
          "Yes", 
          "Only fingers", 
          "Only palm"]),

        ("How far can elbow move during stroke?", 
         "It must not enter playing surface or extend beyond imaginary lines",
         ["No restriction", 
          "It must not enter playing surface or extend beyond imaginary lines", 
          "Any movement", 
          "Only small movement"]),

        ("Can hand cross the arrow during stroke?", 
         "Yes",
         ["No", 
          "Yes", 
          "Only partially", 
          "Not allowed"]),

        ("Is support of table or board allowed during stroke?", 
         "No",
         ["Yes", 
          "No", 
          "Only for balance", 
          "After stroke"]),

        ("What is allowed during stroke regarding legs?", 
         "They may rest on stool or chair",
         ["On table rim", 
          "They may rest on stool or chair", 
          "On board", 
          "Not allowed"]),

        ("What is toss in carrom?", 
         "Method to decide side or first strike",
         ["To choose coins", 
          "Method to decide side or first strike", 
          "To decide umpire", 
          "To start scoring"]),

        ("How is toss decided?", 
         "By coin spin or calling coin",
         ["By dice", 
          "By coin spin or calling coin", 
          "By umpire choice", 
          "By player agreement"]),

        ("What does winning toss allow?", 
         "Choice of side or first strike",
         ["Automatic first strike", 
          "Choice of side or first strike", 
          "Extra turn", 
          "No benefit"]),

        ("If winner chooses side, what happens?", 
         "Loser sits first",
         ["Winner sits first", 
          "Loser sits first", 
          "Both sit together", 
          "No rule"]),

        ("How many trial boards allowed?", 
         "Two",
         ["One", "Two", "Three", "Unlimited"]),
          
         ("Who gets white coins in the board break?", 
         "Player who breaks",
         ["Opponent", 
          "Player who breaks", 
          "Umpire", 
          "Random"]),

        ("What is considered a valid break?", 
         "Striker touching any coin even slightly",
         ["Pocketing a coin", 
          "Striker touching any coin even slightly", 
          "Striker touching queen", 
          "No rule"]),

        ("If striker touches no coin in break, is it valid?", 
         "No, break not considered made",
         ["Yes", 
          "No, break not considered made", 
          "Only if near pocket", 
          "Depends"]),

        ("How many extra chances are allowed if break fails in first attempt?", 
         "Maximum two more chances",
         ["One", 
          "Maximum two more chances", 
          "Three", 
          "No extra chances"]),

        ("If break fails after 3 chances, what happens?", 
         "Right to break is lost and opponent plays",
         ["Player retries", 
          "Right to break is lost and opponent plays", 
          "Game restarts", 
          "No penalty"]),

        ("What coins does opponent get if break is lost?", 
         "Black coins",
         ["White coins", 
          "Black coins", 
          "Random", 
          "No coins"]),

        ("Can coins be rearranged after failed break chances?", 
         "No",
         ["Yes", 
          "No", 
          "Only queen", 
          "Umpire decides"]),

        ("What happens if improper stroke in break pockets striker without touching coins?", 
         "Turn lost but no due/penalty",
         ["Penalty applied", 
          "Turn lost but no due/penalty", 
          "Game ends", 
          "Extra chance"]),

        ("When must break be taken?", 
         "After umpire calls Play",
         ["Before call", 
          "After umpire calls Play", 
          "Anytime", 
          "No rule"]),

        ("How much time to strike after umpire calls Play?", 
         "15 seconds",
         ["10 seconds", 
          "15 seconds", 
          "30 seconds", 
          "No limit"]),

        ("What happens if break before umpire call?", 
         "Foul and all pocketed coins placed back",
         ["Valid break", 
          "Foul and all pocketed coins placed back", 
          "No action", 
          "Extra turn"]),

        ("Does player continue turn if he pockets his own coin OR queen legally?", 
         "Yes",
         ["No", 
          "Yes", 
          "Only queen", 
          "Depends"]),

        ("When does turn pass to opponent?", 
         "If player fails to pocket legally",
         ["Always", 
          "If player fails to pocket legally", 
          "After any shot", 
          "Never"]),

        ("In first game, who breaks first?", 
         "Player who chooses to break",
         ["Opponent", 
          "Player who chooses to break", 
          "Umpire", 
          "Random"]),

        ("How does breaking order alternate in game?", 
         "Turns alternate",
         ["Only first player", 
          "Turns alternate", 
          "No alternation", 
          "Umpire decides"]),

        ("In second game, who breaks first?", 
         "Player who did not break first in previous game",
         ["Same player", 
          "Player who did not break first in previous game", 
          "Random", 
          "Umpire"]),

        ("In doubles, how does turn pass after break?", 
         "To player on right of breaker",
         ["To partner", 
          "To player on right of breaker", 
          "To opponent", 
          "Random"]),

        ("Maximum time allowed for a stroke?", 
         "15 seconds",
         ["10 seconds", 
          "15 seconds", 
          "30 seconds", 
          "No limit"]),

        ("If player plays out of turn and umpire notices before next stroke?", 
         "Player loses board by coins on board",
         ["Game continues", 
          "Player loses board by coins on board", 
          "No penalty", 
          "Extra turn"]),
         
        ("Who wins the board in carrom?", 
		 "Player who pockets all his coins first",
		 ["Player with queen", 
		  "Player who pockets all his coins first", 
		  "Player with most points", 
		  "None"]),

		("How many points is a queen worth?", 
		 "3 points",
		 ["1 point", 
		  "2 points", 
		  "3 points", 
		  "5 points"]),

		("When is queen value credited?", 
		 "Only if player wins the board",
		 ["Always", 
		  "Only if player wins the board", 
		  "Even if board lost", 
		  "Never"]),

		("Is queen value credited if board is lost?", 
		 "No",
		 ["Yes", 
		  "No", 
		  "Sometimes", 
		  "Depends"]),

		("After reaching 22 points, can extra queen points be added?", 
		 "No",
		 ["Yes", 
		  "No", 
		  "Only in doubles", 
		  "Ignored",
		  "Umpire decides"]),

		("Maximum points that can be scored in one board?", 
		 "12",
		 ["10", 
		  "12", 
		  "15", 
		  "25"]),

		("What happens to due/penalty coins in point calculation?", 
		 "They are written off",
		 ["Added to score", 
		  "They are written off",
		  "Carry forwarded to next game",
		  "Substracted from score"]),		  

		("Game is won at how many points?", 
		 "25 points",
		 ["21 points", 
		  "25 points", 
		  "30 points", 
		  "50 points"]),

		("How many boards decide a game?", 
		 "Eight boards",
		 ["Five boards", 
		  "Eight boards", 
		  "Ten boards", 
		  "Unlimited"]),

		("If score is tied after eight boards, what happens?", 
		 "Extra board is played",
		 ["Game ends tie", 
		  "Extra board is played", 
		  "Umpire decides", 
		  "No extra board"]),

		("In singles, how are sides changed after game?", 
		 "Opposite direction",
		 ["No change", 
		  "Opposite direction", 
		  "Both players shift on their Right hand side",
		  "Both players shift on their Left hand side",		
		  "Umpire decides"]),

		("In doubles, how are sides changed?", 
		 "All players shift To next right side",
		 ["No change", 
		  "All players shift To next right side", 
		  "Opposite side", 
		  "Random",
		  "Umpire Decides"]),

		("When is side changed in third game (pre-quarter finals)?", 
		 "After fourth board or when player reaches 13 points",
		 ["After game", 
		  "After fourth board or when player reaches 13 points", 
		  "At umpire discretion", 
		  "No change"]),

		("From quarter-finals onward, when is side change?", 
		 "After 13 points are scored",
		 ["After every board", 
		  "After 13 points are scored", 
		  "No change", 
		  "At end of match"]),

		("If side change is missed and noticed later, when does it happen?", 
		 "After completion of that board",
		 ["Immediately", 
		  "After completion of that board", 
		  "Game restart", 
		  "No change"]),

		("What decides winner in pre-quarter rounds if tie after eight boards?", 
		 "Extra board with toss for break",
		 ["Tie declared & points shared", 
		  "Extra board with toss for break", 
		  "Higher score wins", 
		  "Umpire decides"]),

		("What counts as points for board winner?", 
		 "Opponent’s remaining coins",
		 ["Own coins", 
		  "Opponent’s remaining coins", 
		  "Queen only", 
		  "No points"]),

		("Does covering queen give points if board is lost?", 
		  "No",
		 ["Yes", 
		  "No", 
		  "Sometimes", 
		  "Only queen points"]),     

		("How much time is allowed for players to change sides?", 
		 "Two minutes",
		 ["One minute",
		  "Two minutes",
		  "Three minutes",
		  "Five minutes"]),

		("Taking more than two minutes to change sides results in?",
		 "Violation of rules",
		 ["No issue",
		  "Warning only",
		  "Violation of rules",
		  "Game restart"]),

		("A violation committed before the first stroke of a player's turn is called?",
		 "Technical Foul",
		 ["Ordinary Foul",
		  "Technical Foul",
		  "Minor Error",
		  "Penalty Stroke"]),

		("What happens if a Technical Foul is committed before first stroke?",
		 "One coin is taken out and turn continues",
		 ["Turn cancelled",
		  "Opponent gets queen",
		  "One coin is taken out and turn continues",
		  "Board forfeited"]),

		("Who places the coin taken out after a Technical Foul?",
		 "Opponent",
		 ["Umpire",
		  "Offending player",
		  "Opponent",
		  "Random player"]),

		("If a player commits a violation when it is NOT his turn, it is called?",
		 "Technical Foul",
		 ["No foul",
		  "Technical Foul",
		  "Warning only",
		  "Game stopped"]),

		("If Technical Foul is committed by player not having turn, what happens?",
		 "Penalty is imposed",
		 ["Nothing",
		  "Warning only",
		  "Penalty is imposed",
		  "Turn skipped"]),

		("Does a Technical Foul always involve loss of a coin?",
		 "Yes",
		 ["Yes",
		  "No",
		  "Only in finals",
		  "Depends on umpire"]),

		("After committing Technical Foul before first stroke, does turn continue?",
		 "Yes",
		 ["No",
		  "Yes",
		  "Only after warning",
		  "Only in doubles"]),

		("Technical Foul applies to which situations?",
		 "Violation before stroke or when not having turn",
		 ["Only during strike",
		  "Only after queen",
		  "Violation before stroke or when not having turn",
		  "Only in singles"])	          
					
    ]                  
            
    

    questions = []
    for i in range(500):
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
        setTimeout(() => fireworks.stop(), 400000);
    </script>
    """, height=250)


# ---------- Sound ----------
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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Begin Quiz", use_container_width=True):
            st.session_state.app_stage = "select"
            st.rerun()

    st.stop()


# ==========================================================
# ================== QUESTION COUNT SELECT =================
# ==========================================================
if st.session_state.app_stage == "select":

    st.title("📊 Choose Number of Questions")
    # ---------- TOP RIGHT QUIT BUTTON (SELECT PAGE) ----------
        
    choice = st.radio(
        "How many questions would you like to attempt?",
        [10, 20, 50, 100],
        horizontal=False,
        index=None
        )

    if st.button("▶ Begin Quiz", use_container_width=True):
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
            format_option(q['answer'])
        else:
            st.success("👏 Your Answer is Correct !!")
            format_option(q['answer'])

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

    st.stop()





# ==========================================================
# ===================== THANK YOU PAGE =====================
# ==========================================================
if st.session_state.app_stage == "thankyou":

    st.title("🎉 Thank You for taking this Quiz!")
    st.write(f"### Hope you have enjoyed this journey, If you have any suggestions or feedback feel free to reach out to me.")
    
    st.write(f"### Vishal Ghosalkar")
    
    if st.button("Check yor Final Score"):
        st.session_state.app_stage = "completed"
        st.rerun()
        
# ==========================================================
# ===================== COMPLETED PAGE =====================
# ==========================================================
if st.session_state.app_stage == "completed":

    st.title("🎉 Quiz Completed!")
    
    if st.button("🔄 ReStart Quiz"):
        st.session_state.app_stage = "select"
        st.rerun()

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

    





