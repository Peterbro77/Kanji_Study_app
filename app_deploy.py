import streamlit as st
import pandas as pd
import random

kanji_data = {
    "N2": pd.read_csv("Data/N2_Kanji.csv"),
    "N3": pd.read_csv("Data/N3_Kanji.csv"),
    "N4": pd.read_csv("Data/N4_Kanji.csv"),
    "N5": pd.read_csv("Data/N5_Kanji.csv")
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gluten:wght@700&display=swap');

    html, body {
      font-family: 'Ariel';
    }

    .css-title {
      --rotate: 70deg;
      --transition: 400ms cubic-bezier(0.25, 1, 0.5, 1);
      display: flex;
      position: relative;
      top: 0.25em;
      color: white;
      user-select: none;
      perspective: 2em;
      transform: scale(0.9);
      transform-style: preserve-3d;
      transition: var(--transition);
      transition-property: perspective, transform;
      cursor: pointer;
      justify-content: center;
      font-size: 7rem;
    }

    .css-title span {
      display: flex;
      flex-direction: column;
      line-height: 0.475;
      transition: var(--transition);
      transition-property: color, transform;
      transform-style: preserve-3d;
    }

    .css-title:hover {
      transform: scale(1.25);
    }

    .css-title:hover span {
      color: #fffb;
      transform: translateZ(6vmin);
    }
    </style>
""", unsafe_allow_html=True)


# Define your quiz function here
def run_quiz(level):
    df = kanji_data.get(level)
    if df is None or df.empty:
        st.error("No data found for this level.")
        return

    # Let user define range for quizzing (1-based for UI)
    st.markdown("#### Select Range of Kanji:")
    max_index = len(df)  # 1-based max for user
    start_idx_1b = st.number_input("Start Index (1-based)", min_value=1, max_value=max_index, value=1, key="start_idx")
    end_idx_1b = st.number_input("End Index (1-based)", min_value=1, max_value=max_index, value=max_index, key="end_idx")

    # Convert 1-based input to 0-based
    start_idx = start_idx_1b - 1
    end_idx = end_idx_1b - 1

    # Validate range
    if start_idx > end_idx:
        st.error("❌ Start index cannot be greater than end index.")
        return

    # Initialize quiz state
    if (
        "quiz_index" not in st.session_state or
        "quiz_range" not in st.session_state or
        st.session_state.quiz_range != (start_idx, end_idx)
    ):
        st.session_state.quiz_index = random.randint(start_idx, end_idx)
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.quiz_range = (start_idx, end_idx)

    # Get current Kanji row
    kanji_row = df.iloc[st.session_state.quiz_index]

    st.markdown("### What is the meaning of this Kanji?")
    st.markdown(f"## {kanji_row['Kanji']}")

    user_answer = st.text_input("Your answer:")

    if st.button("Submit"):
        correct = str(kanji_row["Meaning"]).strip().lower()
        user = user_answer.strip().lower()
        st.session_state.total += 1

        if user == correct:
            st.success("Correct! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer: **{correct}**")

    if st.button("Next"):
        st.session_state.quiz_index = random.randint(start_idx, end_idx)

    st.info(f"Score: {st.session_state.score} / {st.session_state.total}")






#--------------------------------------------MODES----------------------------------------------------#



from quiz_logic import load_kanji_data, get_quiz_data
# Load data
csv_path = "Data/N3_Kanji.csv"
df = load_kanji_data(csv_path)
total_kanji = len(df)

st.markdown("""
    <style>
    /* Target buttons inside the sidebar */
    section[data-testid="stSidebar"] button {
        width: 100% !important;
        display: block;
        margin: 0.2rem 0;
        text-align: center;
        white-space: nowrap;
    }
    </style>
""", unsafe_allow_html=True)



# Sidebar for mode
# mode = st.sidebar("Select Mode", ["ようこそう","N2","N3","N4","N5", "🧪 Quiz"])
if "mode" not in st.session_state:
    st.session_state.mode = "ようこそう"

def set_mode(selected_mode):
    st.session_state.mode = selected_mode


# Sidebar
# -------------------- Sidebar --------------------
# --- Sidebar ---
with st.sidebar:
    st.sidebar.image(
    "Images/Kanji_icon.png",
    use_container_width=True
)
    st.markdown("### ")

    # Welcome button
    if st.button("ようこそう", type="primary"):
        set_mode("ようこそう")
        st.session_state["quiz_dropdown"] = "None"
        st.session_state["flashcard_dropdown"] = "Select"

    # Flashcard dropdown (with on_change)
    def on_flashcard_change():
        if st.session_state.flashcard_dropdown != "Select":
            set_mode(st.session_state.flashcard_dropdown)
            st.session_state["quiz_dropdown"] = "None"

    st.selectbox(
        "Choose Flashcard Level",
        ["Select", "N2", "N3", "N4", "N5"],
        key="flashcard_dropdown",
        on_change=on_flashcard_change
    )

    # Quiz dropdown (with on_change)
    def on_quiz_change():
        if st.session_state.quiz_dropdown != "None":
            set_mode(st.session_state.quiz_dropdown)
            st.session_state["flashcard_dropdown"] = "Select"

    st.selectbox(
        "Choose Quiz Level",
        ["None", "N2 Quiz", "N3 Quiz", "N4 Quiz", "N5 Quiz"],
        key="quiz_dropdown",
        on_change=on_quiz_change
    )

# --- END: Dropdown Logic ---


# # Use the mode for routing
# mode = st.session_state.mode

# index_key = f"flashcard_index_{mode}"

# if index_key not in st.session_state:
#     st.session_state[index_key] = 0

mode = st.session_state["mode"]
if mode == "ようこそう":
    def welcome():
        
        # st.markdown(
        #     f"<h1 style='text-align: center; font-size: 100px; color: white'>Kanji Study App</h1>",
        #     unsafe_allow_html=True
        # )

        st.markdown("""
    <div class="css-title">
        <span>K</span><span>a</span><span>n</span><span>j</span><span>i</span>
        <span>&nbsp;</span>
        <span>S</span><span>t</span><span>u</span><span>d</span><span>y</span>
        &nbsp;</span>
        <span>A</span><span>p</span><span>p</span>
    </div>
""", unsafe_allow_html=True)

        # st.markdown(
        #     f"<h1 style='text-align: center; font-size: 1px;'></h1>",
        #     unsafe_allow_html=True
        # )
        

        

        st.markdown("""
        <style>
        .shimmer-text {
            display: inline-block;
            background: linear-gradient(90deg, #00f, #0ff, #00f) -100% / 200%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 900;
            font-family: 'Exo', sans-serif;
            font-size: 35px !important;
            animation: shimmer 2s linear infinite;
            text-align: center;
            width: 100%;
        }

        @keyframes shimmer {
            to { background-position: 100% }
        }

        .center-container {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Use the class in your HTML content
        st.markdown(
            """
            <div class = "center-container">
                <p class='shimmer-text'>Your Personal 漢字 Learner</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # st.image(
        # "C:/Users/peter/Desktop/Peter/study stuff/DS/Kanji_Study_app/Kanji_icon.png",
        # width=650)

        st.markdown(
            f"<h1 style='text-align: center; font-size: 1px;'></h1>",
            unsafe_allow_html=True
        )

        from PIL import Image
        import base64
        from io import BytesIO

        # Load and encode image
        img = Image.open("Images/Kanji_icon.png")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()

        # Render it centered in main app
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                <img src="data:image/png;base64,{img_b64}" width="350">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h1 style='text-align: center; font-size: 200px;'></h1>",
            unsafe_allow_html=True
        )


        
        # About Section
        st.markdown('<h2 class="section-title">📚 About</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p class="section-text">
        Kanji Study App is your personalized companion for learning and reviewing Kanji characters for the All JLPT levels. Whether you're prepping for exams or building daily reading fluency, this app makes mastering over Kanji engaging and effective.
        </p>
        """, unsafe_allow_html=True)

        # Features Section
        st.markdown('<h2 class="section-title">✨ Features</h2>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="section-text">
            <li>🧠 Learn Kanji meanings, readings (onyomi & kunyomi), and examples</li>
            <li>📝 Quiz mode to reinforce your memory</li>
            <li>🎯 Built for JLPT-level proficiency</li>
        </ul>
        """, unsafe_allow_html=True)





elif mode == "N3":
    def render_flashcards(mode):

        index_key = f"index_N3"

        
        # Load kanji data
        df = pd.read_csv("Data/N3_Kanji.csv")

        kanji_data = df.to_dict(orient="records")


        # Initialize session state variables
        if "kanji_list" not in st.session_state:
            st.session_state.kanji_list = kanji_data  # kanji_data should be your list of kanji dicts

        if "bookmarked_kanji" not in st.session_state:
            st.session_state.bookmarked_kanji = set()

        if "filtered_mode" not in st.session_state:
            st.session_state.filtered_mode = False
        if "filtered_indices" not in st.session_state:
            st.session_state.filtered_indices = []
        if "filtered_index" not in st.session_state:
            st.session_state.filtered_index = 0


        # App title
        st.title("JLPT N3 Kanji Study 🎌")

        # Search functionality
        search_query = st.text_input("🔍 Search for a Kanji / Onyomi / Kunyomi / Meaning: ").strip()



        # ------------------ SESSION STATE INITIALIZATION ------------------ #
        if index_key not in st.session_state:
            st.session_state[index_key] = 0

        if "show_details" not in st.session_state:
            st.session_state.show_details = False

        if "go_next" not in st.session_state:
            st.session_state.go_next = False

        if "go_prev" not in st.session_state:
            st.session_state.go_prev = False

        shuffle_key = f"shuffled_indices_N3"
        shuffle_flag_key = f"is_shuffled_N3"

        if shuffle_key not in st.session_state:
            st.session_state[shuffle_key] = list(range(len(df)))

        if shuffle_flag_key not in st.session_state:
            st.session_state[shuffle_flag_key] = False


        #-------------------------SEARCH LOGIC--------------------------------#
        if search_query:
            # Case-insensitive match in any of the four columns
            mask = df.apply(lambda row: search_query.lower() in str(row['Kanji']).lower() 
                                            or search_query.lower() in str(row['Onyomi']).lower()
                                            or search_query.lower() in str(row['Kunyomi']).lower()
                                            or search_query.lower() in str(row['Meaning']).lower(), axis=1)
            search_results = df[mask]

            if not search_results.empty:
                st.markdown(f"### 🔎 Search Results ({len(search_results)} found):")
                for idx, row in search_results.iterrows():
                    st.markdown(f"---")
                    st.markdown(f"## Kanji: {row['Kanji']}")
                    st.markdown(f"**Onyomi**: {row['Onyomi']}")
                    st.markdown(f"**Kunyomi**: {row['Kunyomi']}")
                    st.markdown(f"**Meaning**: {row['Meaning']}")
            else:
                st.markdown("❌ No matching kanji found.")
            st.stop()





        # Detect toggle state change manually
        prev_mode = st.session_state.get("filtered_mode", False)

        # Bookmark toggle
        #from streamlit_toggle import st_toggle_switch
        #new_mode = st_toggle_switch(
         #   label = "🔖 View bookmarked Kanji",
          #  key = "Bookmarked",
           # default_value = False,
            #label_after = False,
            #inactive_color = "#8D0909",
            #active_color = "White",
            #track_color = "Green",

        #)
         new_mode = st.checkbox("🔖 View Bookmarked Only", value=prev_mode)

        #If the toggle changed, update state and rerun
        if new_mode != prev_mode:
            st.session_state.filtered_mode = new_mode
            st.session_state.filtered_index = 0
            st.rerun()  # ✅ Use st.rerun() instead of experimental version

        # Proceed based on current mode
        if st.session_state.get("filtered_mode", False):
            # Filter the DataFrame
            filtered_df = df[df["Kanji"].isin(st.session_state.bookmarked_kanji)]

            if filtered_df.empty:
                st.warning("You have no bookmarked kanji.")
                st.stop()

            st.session_state.filtered_indices = list(filtered_df.index)

            if st.session_state.filtered_index >= len(st.session_state.filtered_indices):
                st.session_state.filtered_index = 0

            actual_index = st.session_state.filtered_indices[st.session_state.filtered_index]
        else:
            actual_index = st.session_state[shuffle_key][st.session_state[index_key]]


        kanji_row = df.iloc[actual_index]



        # -------- INITIALIZE BOOKMARK STATE -------- #
        if "bookmarked" not in st.session_state:
            st.session_state.bookmarked = set()
        if "toggle_bookmark" not in st.session_state:
            st.session_state.toggle_bookmark = False

        # Get actual index of the current kanji
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]

        # -------- BOOKMARK BUTTON -------- #
        # Get actual index of the current kanji from shuffled list
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]
        current_kanji = df.iloc[actual_index]

        kanji_char = current_kanji["Kanji"]
        bookmarked = kanji_char in st.session_state.bookmarked_kanji

        bookmark_icon = "💚" if bookmarked else "🤍"
        bookmark_label = f"{bookmark_icon} Bookmark"

        if st.button(bookmark_label, key="bookmark"):
            if bookmarked:
                st.session_state.bookmarked_kanji.remove(kanji_char)
            else:
                st.session_state.bookmarked_kanji.add(kanji_char)
            st.rerun()




        # ------------------ DISPLAY KANJI AND PROGRESS ------------------ #
        total_kanji = len(df)
        current = st.session_state[index_key] + 1  # human-friendly
        # kanji_row = df.iloc[st.session_state.index]

        st.markdown(f"### 📖 Kanji {current} of {total_kanji}")
        # st.markdown(f"## Kanji: {kanji_row['Kanji']}")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 200px;'>{kanji_row['Kanji']}</h1>",
            unsafe_allow_html=True
        )




        # ------------------ TOGGLE DETAILS ------------------ #
        if st.button("Show / Hide Onyomi, Kunyomi, Meaning"):
            st.session_state.show_details = not st.session_state.show_details

        if st.session_state.show_details:
            st.markdown(
                f"<p><strong style = 'color:green'>Onyomi:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{kanji_row['Onyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Kunyomi:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Kunyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Meaning:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Meaning']}</p>",
                unsafe_allow_html=True
            )



        # Shuffle button
        def shuffle_kanji():
            random.shuffle(st.session_state[shuffle_key])
            st.session_state[index_key] = 0  # Reset to first shuffled kanji
            st.session_state[shuffle_flag_key] = True

        st.button("🔀 Shuffle", on_click=shuffle_kanji)

        # Reset button
        def reset_kanji_order():
            st.session_state[shuffle_key] = list(range(len(df)))
            st.session_state[index_key] = 0
            st.session_state[shuffle_flag_key] = False

        st.button("🔁 Reset", on_click=reset_kanji_order)

        # ------------------ NAVIGATION CALLBACKS ------------------ #
        # def go_previous():
        #     st.session_state.go_prev = True
        #     st.session_state.go_next = False

        # def go_next():
        #     st.session_state.go_next = True
        #     st.session_state.go_prev = False

        # ------------------ NAVIGATION BUTTONS ------------------ #
        st.markdown("<br><br>", unsafe_allow_html=True)

        col_prev, col_spacer, col_next = st.columns([1, 0.2, 1])

        with col_prev:
            if st.button("⬅️ Previous", use_container_width=True, key="prev_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index - 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] - 1) % len(st.session_state[shuffle_key])
                st.rerun()  # <-- clears button state after updating. so, navigation callback are not needed anymore

        with col_next:
            if st.button("Next ➡️", use_container_width=True, key="next_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index + 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] + 1) % len(st.session_state[shuffle_key])
                st.rerun()
            # st.title("Learn Kanji")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 67px; color: orange'>漢字を勉強しましょう</h1>",
                unsafe_allow_html=True
        )
            # st.write(df)  # Can enhance later


elif mode == "N4":
    def render_flashcards(mode):
        index_key = f"index_N4"
        
        # Load kanji data
        df = pd.read_csv("Data/N4_Kanji.csv")

        kanji_data = df.to_dict(orient="records")


        # Initialize session state variables
        if "kanji_list" not in st.session_state:
            st.session_state.kanji_list = kanji_data  # kanji_data should be your list of kanji dicts

        if "bookmarked_kanji" not in st.session_state:
            st.session_state.bookmarked_kanji = set()

        if "filtered_mode" not in st.session_state:
            st.session_state.filtered_mode = False
        if "filtered_indices" not in st.session_state:
            st.session_state.filtered_indices = []
        if "filtered_index" not in st.session_state:
            st.session_state.filtered_index = 0


        # App title
        st.title("JLPT N4 Kanji Study 🎌")

        # Search functionality
        search_query = st.text_input("🔍 Search for a Kanji / Onyomi / Kunyomi / Meaning: ").strip()



        # ------------------ SESSION STATE INITIALIZATION ------------------ #
        if index_key not in st.session_state:
            st.session_state[index_key] = 0

        if "show_details" not in st.session_state:
            st.session_state.show_details = False

        if "go_next" not in st.session_state:
            st.session_state.go_next = False

        if "go_prev" not in st.session_state:
            st.session_state.go_prev = False

        shuffle_key = f"shuffled_indices_N4"
        shuffle_flag_key = f"is_shuffled_N4"

        if shuffle_key not in st.session_state:
            st.session_state[shuffle_key] = list(range(len(df)))

        if shuffle_flag_key not in st.session_state:
            st.session_state[shuffle_flag_key] = False


        #-------------------------SEARCH LOGIC--------------------------------#
        if search_query:
            # Case-insensitive match in any of the four columns
            mask = df.apply(lambda row: search_query.lower() in str(row['Kanji']).lower() 
                                            or search_query.lower() in str(row['Onyomi']).lower()
                                            or search_query.lower() in str(row['Kunyomi']).lower()
                                            or search_query.lower() in str(row['Meaning']).lower(), axis=1)
            search_results = df[mask]

            if not search_results.empty:
                st.markdown(f"### 🔎 Search Results ({len(search_results)} found):")
                for idx, row in search_results.iterrows():
                    st.markdown(f"---")
                    st.markdown(f"## Kanji: {row['Kanji']}")
                    st.markdown(f"**Onyomi**: {row['Onyomi']}")
                    st.markdown(f"**Kunyomi**: {row['Kunyomi']}")
                    st.markdown(f"**Meaning**: {row['Meaning']}")
            else:
                st.markdown("❌ No matching kanji found.")
            st.stop()





        # Detect toggle state change manually
        prev_mode = st.session_state.get("filtered_mode", False)

        # Bookmark toggle
        #from streamlit_toggle import st_toggle_switch
        #new_mode = st_toggle_switch(
         #   label = "🔖 View bookmarked Kanji",
         #   key = "Bookmarked",
         #  default_value = False,
         #   label_after = False,
         #   inactive_color = "#8D0909",
         #   active_color = "White",
         #   track_color = "Green",

        #)

        # Render the checkbox
         new_mode = st.checkbox("🔖 View Bookmarked Only", value=prev_mode)

        # If the toggle changed, update state and rerun
        if new_mode != prev_mode:
            st.session_state.filtered_mode = new_mode
            st.session_state.filtered_index = 0
            st.rerun()  # ✅ Use st.rerun() instead of experimental version

        # Proceed based on current mode
        if st.session_state.get("filtered_mode", False):
            # Filter the DataFrame
            filtered_df = df[df["Kanji"].isin(st.session_state.bookmarked_kanji)]

            if filtered_df.empty:
                st.warning("You have no bookmarked kanji.")
                st.stop()

            st.session_state.filtered_indices = list(filtered_df.index)

            if st.session_state.filtered_index >= len(st.session_state.filtered_indices):
                st.session_state.filtered_index = 0

            actual_index = st.session_state.filtered_indices[st.session_state.filtered_index]
        else:
            actual_index = st.session_state[shuffle_key][st.session_state[index_key]]


        kanji_row = df.iloc[actual_index]



        # -------- INITIALIZE BOOKMARK STATE -------- #
        if "bookmarked" not in st.session_state:
            st.session_state.bookmarked = set()
        if "toggle_bookmark" not in st.session_state:
            st.session_state.toggle_bookmark = False

        # Get actual index of the current kanji
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]

        # -------- BOOKMARK BUTTON -------- #
        # Get actual index of the current kanji from shuffled list
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]
        current_kanji = df.iloc[actual_index]

        kanji_char = current_kanji["Kanji"]
        bookmarked = kanji_char in st.session_state.bookmarked_kanji

        bookmark_icon = "💚" if bookmarked else "🤍"
        bookmark_label = f"{bookmark_icon} Bookmark"

        if st.button(bookmark_label, key="bookmark"):
            if bookmarked:
                st.session_state.bookmarked_kanji.remove(kanji_char)
            else:
                st.session_state.bookmarked_kanji.add(kanji_char)
            st.rerun()




        # ------------------ DISPLAY KANJI AND PROGRESS ------------------ #
        total_kanji = len(df)
        current = st.session_state[index_key] + 1  # human-friendly
        # kanji_row = df.iloc[st.session_state.index]

        st.markdown(f"### 📖 Kanji {current} of {total_kanji}")
        # st.markdown(f"## Kanji: {kanji_row['Kanji']}")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 200px;'>{kanji_row['Kanji']}</h1>",
            unsafe_allow_html=True
        )




        # ------------------ TOGGLE DETAILS ------------------ #
        if st.button("Show / Hide Onyomi, Kunyomi, Meaning"):
            st.session_state.show_details = not st.session_state.show_details

        if st.session_state.show_details:
            st.markdown(
                f"<p><strong style = 'color:green'>Onyomi:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{kanji_row['Onyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Kunyomi:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Kunyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Meaning:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Meaning']}</p>",
                unsafe_allow_html=True
            )



        # Shuffle button
        def shuffle_kanji():
            random.shuffle(st.session_state[shuffle_key])
            st.session_state[index_key] = 0  # Reset to first shuffled kanji
            st.session_state[shuffle_flag_key] = True

        st.button("🔀 Shuffle", on_click=shuffle_kanji)

        # Reset button
        def reset_kanji_order():
            st.session_state[shuffle_key] = list(range(len(df)))
            st.session_state[index_key] = 0
            st.session_state[shuffle_flag_key] = False

        st.button("🔁 Reset", on_click=reset_kanji_order)

        # ------------------ NAVIGATION CALLBACKS ------------------ #
        # def go_previous():
        #     st.session_state.go_prev = True
        #     st.session_state.go_next = False

        # def go_next():
        #     st.session_state.go_next = True
        #     st.session_state.go_prev = False

        # ------------------ NAVIGATION BUTTONS ------------------ #
        st.markdown("<br><br>", unsafe_allow_html=True)

        col_prev, col_spacer, col_next = st.columns([1, 0.2, 1])

        with col_prev:
            if st.button("⬅️ Previous", use_container_width=True, key="prev_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index - 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] - 1) % len(st.session_state[shuffle_key])
                st.rerun()  # <-- clears button state after updating. so, navigation callback are not needed anymore

        with col_next:
            if st.button("Next ➡️", use_container_width=True, key="next_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index + 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] + 1) % len(st.session_state[shuffle_key])
                st.rerun()
            # st.title("Learn Kanji")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 67px; color: orange'>漢字を勉強しましょう</h1>",
                unsafe_allow_html=True
        )
            # st.write(df)  # Can enhance later


if mode == "N5":
    def render_flashcards(mode):

        index_key = f"index_N5"

        # Load kanji data
        df = pd.read_csv("Data/N5_Kanji.csv")

        kanji_data = df.to_dict(orient="records")


        # Initialize session state variables
        if "kanji_list" not in st.session_state:
            st.session_state.kanji_list = kanji_data  # kanji_data should be your list of kanji dicts

        if "bookmarked_kanji" not in st.session_state:
            st.session_state.bookmarked_kanji = set()

        if "filtered_mode" not in st.session_state:
            st.session_state.filtered_mode = False
        if "filtered_indices" not in st.session_state:
            st.session_state.filtered_indices = []
        if "filtered_index" not in st.session_state:
            st.session_state.filtered_index = 0


        # App title
        st.title("JLPT N5 Kanji Study 🎌")

        # Search functionality
        search_query = st.text_input("🔍 Search for a Kanji / Onyomi / Kunyomi / Meaning: ").strip()



        # ------------------ SESSION STATE INITIALIZATION ------------------ #
        if index_key not in st.session_state:
            st.session_state[index_key] = 0

        if "show_details" not in st.session_state:
            st.session_state.show_details = False

        if "go_next" not in st.session_state:
            st.session_state.go_next = False

        if "go_prev" not in st.session_state:
            st.session_state.go_prev = False

        shuffle_key = f"shuffled_indices_N5"
        shuffle_flag_key = f"is_shuffled_N5"

        if shuffle_key not in st.session_state:
            st.session_state[shuffle_key] = list(range(len(df)))

        if shuffle_flag_key not in st.session_state:
            st.session_state[shuffle_flag_key] = False


        #-------------------------SEARCH LOGIC--------------------------------#
        if search_query:
            # Case-insensitive match in any of the four columns
            mask = df.apply(lambda row: search_query.lower() in str(row['Kanji']).lower() 
                                            or search_query.lower() in str(row['Onyomi']).lower()
                                            or search_query.lower() in str(row['Kunyomi']).lower()
                                            or search_query.lower() in str(row['Meaning']).lower(), axis=1)
            search_results = df[mask]

            if not search_results.empty:
                st.markdown(f"### 🔎 Search Results ({len(search_results)} found):")
                for idx, row in search_results.iterrows():
                    st.markdown(f"---")
                    st.markdown(f"## Kanji: {row['Kanji']}")
                    st.markdown(f"**Onyomi**: {row['Onyomi']}")
                    st.markdown(f"**Kunyomi**: {row['Kunyomi']}")
                    st.markdown(f"**Meaning**: {row['Meaning']}")
            else:
                st.markdown("❌ No matching kanji found.")
            st.stop()





        # Detect toggle state change manually
        prev_mode = st.session_state.get("filtered_mode", False)

        # Bookmark toggle
        #from streamlit_toggle import st_toggle_switch
        #new_mode = st_toggle_switch(
         #   label = "🔖 View bookmarked Kanji",
         #   key = "Bookmarked",
         #   default_value = False,
         #   label_after = False,
         #   inactive_color = "#8D0909",
         #   active_color = "White",
         #   track_color = "Green",

        #)

        # Render the checkbox
         new_mode = st.checkbox("🔖 View Bookmarked Only", value=prev_mode)

        # If the toggle changed, update state and rerun
        if new_mode != prev_mode:
            st.session_state.filtered_mode = new_mode
            st.session_state.filtered_index = 0
            st.rerun()  # ✅ Use st.rerun() instead of experimental version

        # Proceed based on current mode
        if st.session_state.get("filtered_mode", False):
            # Filter the DataFrame
            filtered_df = df[df["Kanji"].isin(st.session_state.bookmarked_kanji)]

            if filtered_df.empty:
                st.warning("You have no bookmarked kanji.")
                st.stop()

            st.session_state.filtered_indices = list(filtered_df.index)

            if st.session_state.filtered_index >= len(st.session_state.filtered_indices):
                st.session_state.filtered_index = 0

            actual_index = st.session_state.filtered_indices[st.session_state.filtered_index]
        else:
            actual_index = st.session_state[shuffle_key][st.session_state[index_key]]


        kanji_row = df.iloc[actual_index]



        # -------- INITIALIZE BOOKMARK STATE -------- #
        if "bookmarked" not in st.session_state:
            st.session_state.bookmarked = set()
        if "toggle_bookmark" not in st.session_state:
            st.session_state.toggle_bookmark = False

        # Get actual index of the current kanji
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]

        # -------- BOOKMARK BUTTON -------- #
        # Get actual index of the current kanji from shuffled list
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]
        current_kanji = df.iloc[actual_index]

        kanji_char = current_kanji["Kanji"]
        bookmarked = kanji_char in st.session_state.bookmarked_kanji

        bookmark_icon = "💚" if bookmarked else "🤍"
        bookmark_label = f"{bookmark_icon} Bookmark"

        if st.button(bookmark_label, key="bookmark"):
            if bookmarked:
                st.session_state.bookmarked_kanji.remove(kanji_char)
            else:
                st.session_state.bookmarked_kanji.add(kanji_char)
            st.rerun()




        # ------------------ DISPLAY KANJI AND PROGRESS ------------------ #
        total_kanji = len(df)
        current = st.session_state[index_key] + 1  # human-friendly
        # kanji_row = df.iloc[st.session_state.index]

        st.markdown(f"### 📖 Kanji {current} of {total_kanji}")
        # st.markdown(f"## Kanji: {kanji_row['Kanji']}")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 200px;'>{kanji_row['Kanji']}</h1>",
            unsafe_allow_html=True
        )




        # ------------------ TOGGLE DETAILS ------------------ #
        if st.button("Show / Hide Onyomi, Kunyomi, Meaning"):
            st.session_state.show_details = not st.session_state.show_details

        if st.session_state.show_details:
            st.markdown(
                f"<p><strong style = 'color:green'>Onyomi:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{kanji_row['Onyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Kunyomi:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Kunyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Meaning:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Meaning']}</p>",
                unsafe_allow_html=True
            )



        # Shuffle button
        def shuffle_kanji():
            random.shuffle(st.session_state[shuffle_key])
            st.session_state[index_key] = 0  # Reset to first shuffled kanji
            st.session_state[shuffle_flag_key] = True

        st.button("🔀 Shuffle", on_click=shuffle_kanji)

        # Reset button
        def reset_kanji_order():
            st.session_state[shuffle_key] = list(range(len(df)))
            st.session_state[index_key] = 0
            st.session_state[shuffle_flag_key] = False

        st.button("🔁 Reset", on_click=reset_kanji_order)

        # ------------------ NAVIGATION CALLBACKS ------------------ #
        # def go_previous():
        #     st.session_state.go_prev = True
        #     st.session_state.go_next = False

        # def go_next():
        #     st.session_state.go_next = True
        #     st.session_state.go_prev = False

        # ------------------ NAVIGATION BUTTONS ------------------ #
        st.markdown("<br><br>", unsafe_allow_html=True)

        col_prev, col_spacer, col_next = st.columns([1, 0.2, 1])

        with col_prev:
            if st.button("⬅️ Previous", use_container_width=True, key="prev_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index - 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] - 1) % len(st.session_state[shuffle_key])
                st.rerun()  # <-- clears button state after updating. so, navigation callback are not needed anymore

        with col_next:
            if st.button("Next ➡️", use_container_width=True, key="next_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index + 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] + 1) % len(st.session_state[shuffle_key])
                st.rerun()
            # st.title("Learn Kanji")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 67px; color: orange'>漢字を勉強しましょう</h1>",
                unsafe_allow_html=True
        )
            # st.write(df)  # Can enhance later



elif mode == "N2":
    def render_flashcards(mode):
        index_key = f"index_N2"

        # Load kanji data
        df = pd.read_csv("Data/N2_Kanji.csv")

        kanji_data = df.to_dict(orient="records")


        # Initialize session state variables
        if "kanji_list" not in st.session_state:
            st.session_state.kanji_list = kanji_data  # kanji_data should be your list of kanji dicts

        if "bookmarked_kanji" not in st.session_state:
            st.session_state.bookmarked_kanji = set()

        if "filtered_mode" not in st.session_state:
            st.session_state.filtered_mode = False
        if "filtered_indices" not in st.session_state:
            st.session_state.filtered_indices = []
        if "filtered_index" not in st.session_state:
            st.session_state.filtered_index = 0


        # App title
        st.title("JLPT N2 Kanji Study 🎌")

        # Search functionality
        search_query = st.text_input("🔍 Search for a Kanji / Onyomi / Kunyomi / Meaning: ").strip()



        # ------------------ SESSION STATE INITIALIZATION ------------------ #
        if index_key not in st.session_state:
            st.session_state[index_key] = 0

        if "show_details" not in st.session_state:
            st.session_state.show_details = False

        if "go_next" not in st.session_state:
            st.session_state.go_next = False

        if "go_prev" not in st.session_state:
            st.session_state.go_prev = False

        shuffle_key = f"shuffled_indices_N2"
        shuffle_flag_key = f"is_shuffled_N2"

        if shuffle_key not in st.session_state:
            st.session_state[shuffle_key] = list(range(len(df)))

        if shuffle_flag_key not in st.session_state:
            st.session_state[shuffle_flag_key] = False


        #-------------------------SEARCH LOGIC--------------------------------#
        if search_query:
            # Case-insensitive match in any of the four columns
            mask = df.apply(lambda row: search_query.lower() in str(row['Kanji']).lower() 
                                            or search_query.lower() in str(row['Onyomi']).lower()
                                            or search_query.lower() in str(row['Kunyomi']).lower()
                                            or search_query.lower() in str(row['Meaning']).lower(), axis=1)
            search_results = df[mask]

            if not search_results.empty:
                st.markdown(f"### 🔎 Search Results ({len(search_results)} found):")
                for idx, row in search_results.iterrows():
                    st.markdown(f"---")
                    st.markdown(f"## Kanji: {row['Kanji']}")
                    st.markdown(f"**Onyomi**: {row['Onyomi']}")
                    st.markdown(f"**Kunyomi**: {row['Kunyomi']}")
                    st.markdown(f"**Meaning**: {row['Meaning']}")
            else:
                st.markdown("❌ No matching kanji found.")
            st.stop()





        # Detect toggle state change manually
        prev_mode = st.session_state.get("filtered_mode", False)

        # Bookmark toggle
        #from streamlit_toggle import st_toggle_switch
        #new_mode = st_toggle_switch(
        #    label = "🔖 View bookmarked Kanji",
        #    key = "Bookmarked",
        #    default_value = False,
        #    label_after = False,
        #    inactive_color = "#8D0909",
        #    active_color = "White",
        #    track_color = "Green",

        #)

        # Render the checkbox
         new_mode = st.checkbox("🔖 View Bookmarked Only", value=prev_mode)

        # If the toggle changed, update state and rerun
        if new_mode != prev_mode:
            st.session_state.filtered_mode = new_mode
            st.session_state.filtered_index = 0
            st.rerun()  # ✅ Use st.rerun() instead of experimental version

        # Proceed based on current mode
        if st.session_state.get("filtered_mode", False):
            # Filter the DataFrame
            filtered_df = df[df["Kanji"].isin(st.session_state.bookmarked_kanji)]

            if filtered_df.empty:
                st.warning("You have no bookmarked kanji.")
                st.stop()

            st.session_state.filtered_indices = list(filtered_df.index)

            if st.session_state.filtered_index >= len(st.session_state.filtered_indices):
                st.session_state.filtered_index = 0

            actual_index = st.session_state.filtered_indices[st.session_state.filtered_index]
        else:
            actual_index = st.session_state[shuffle_key][st.session_state[index_key]]

        kanji_row = df.iloc[actual_index]



        # -------- INITIALIZE BOOKMARK STATE -------- #
        if "bookmarked" not in st.session_state:
            st.session_state.bookmarked = set()
        if "toggle_bookmark" not in st.session_state:
            st.session_state.toggle_bookmark = False

        # Get actual index of the current kanji
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]

        # -------- BOOKMARK BUTTON -------- #
        # Get actual index of the current kanji from shuffled list
        # actual_index = st.session_state.shuffled_indices[st.session_state.index]
        current_kanji = df.iloc[actual_index]

        kanji_char = current_kanji["Kanji"]
        bookmarked = kanji_char in st.session_state.bookmarked_kanji

        bookmark_icon = "💚" if bookmarked else "🤍"
        bookmark_label = f"{bookmark_icon} Bookmark"

        if st.button(bookmark_label, key="bookmark"):
            if bookmarked:
                st.session_state.bookmarked_kanji.remove(kanji_char)
            else:
                st.session_state.bookmarked_kanji.add(kanji_char)
            st.rerun()




        # ------------------ DISPLAY KANJI AND PROGRESS ------------------ #
        total_kanji = len(df)
        current = st.session_state[index_key] + 1  # human-friendly
        # kanji_row = df.iloc[st.session_state.index]

        st.markdown(f"### 📖 Kanji {current} of {total_kanji}")
        # st.markdown(f"## Kanji: {kanji_row['Kanji']}")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 200px;'>{kanji_row['Kanji']}</h1>",
            unsafe_allow_html=True
        )




        # ------------------ TOGGLE DETAILS ------------------ #
        if st.button("Show / Hide Onyomi, Kunyomi, Meaning"):
            st.session_state.show_details = not st.session_state.show_details

        if st.session_state.show_details:
            st.markdown(
                f"<p><strong style = 'color:green'>Onyomi:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{kanji_row['Onyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Kunyomi:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Kunyomi']}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p><strong style = 'color:green'>Meaning:</strong>&nbsp;&nbsp;&nbsp;{kanji_row['Meaning']}</p>",
                unsafe_allow_html=True
            )



        # Shuffle button
        def shuffle_kanji():
            random.shuffle(st.session_state[shuffle_key])
            st.session_state[index_key] = 0  # Reset to first shuffled kanji
            st.session_state[shuffle_flag_key] = True

        st.button("🔀 Shuffle", on_click=shuffle_kanji)

        # Reset button
        def reset_kanji_order():
            st.session_state[shuffle_key] = list(range(len(df)))
            st.session_state[index_key] = 0
            st.session_state[shuffle_flag_key] = False

        st.button("🔁 Reset", on_click=reset_kanji_order)

        # ------------------ NAVIGATION CALLBACKS ------------------ #
        # def go_previous():
        #     st.session_state.go_prev = True
        #     st.session_state.go_next = False

        # def go_next():
        #     st.session_state.go_next = True
        #     st.session_state.go_prev = False

        # ------------------ NAVIGATION BUTTONS ------------------ #
        st.markdown("<br><br>", unsafe_allow_html=True)

        col_prev, col_spacer, col_next = st.columns([1, 0.2, 1])

        with col_prev:
            if st.button("⬅️ Previous", use_container_width=True, key="prev_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index - 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] - 1) % len(st.session_state[shuffle_key])
                st.rerun()  # <-- clears button state after updating. so, navigation callback are not needed anymore

        with col_next:
            if st.button("Next ➡️", use_container_width=True, key="next_btn"):
                if st.session_state.filtered_mode:
                    st.session_state.filtered_index = (st.session_state.filtered_index + 1) % len(st.session_state.filtered_indices)
                else:
                    st.session_state[index_key] = (st.session_state[index_key] + 1) % len(st.session_state[shuffle_key])
                st.rerun()
            # st.title("Learn Kanji")

        st.markdown(
            f"<h1 style='text-align: center; font-size: 67px; color: orange'>漢字を勉強しましょう</h1>",
                unsafe_allow_html=True
        )
            # st.write(df)  # Can enhance later





# -------------------- Main Area --------------------
mode = st.session_state.get("mode", "ようこそう")

if "Quiz" in mode:
    level = mode.replace(" Quiz", "")  # Get level: N2, N3, etc.

    valid_levels = ["N2", "N3", "N4", "N5"]

    if level in valid_levels:
        run_quiz(level)  # ✅ Just call with level string
    else:
        st.error("⚠️ No quiz available for this level.")

elif mode in ["N2", "N3", "N4", "N5"]:
    render_flashcards(mode)
elif mode == "ようこそう":
    welcome()


#------------------------------------------------------------------------------------Quiz-Mode---------------------------------------------------------------------------------------#

# elif mode == "🧪 Quiz":
#     st.markdown(
#         f"<h1 style='text-align: center; font-size: 67px; color: red'>クイズの時間です</h1>",
#             unsafe_allow_html=True
#     )
#     # st.title("クイズの時間です")

#     st.write(f"Total Kanji Available: {total_kanji}")
#     start = st.number_input("Start index (1-based)", min_value=1, max_value=total_kanji, value=1)
#     end = st.number_input("End index (1-based)", min_value=1, max_value=total_kanji, value=min(10, total_kanji))

#     if start > end:
#         st.warning("⚠️ Start index should be less than or equal to end index.")
#     else:
#         if st.button("Start Quiz"):
#             quiz_data = get_quiz_data(df, start, end)

#             score = 0
#             st.session_state["quiz"] = quiz_data.to_dict("records")
#             st.session_state["index"] = 0
#             st.session_state["score"] = 0

#     # Run Quiz if initialized
#     if "quiz" in st.session_state and st.session_state["index"] < len(st.session_state["quiz"]):
#         current = st.session_state["quiz"][st.session_state["index"]]
#         st.subheader(f"Q{st.session_state['index']+1}: What is the meaning of '{current['Kanji']}'?")
#         user_answer = st.text_input("Your answer:")

#         if st.button("Submit"):
#             correct = current["Meaning"].strip().lower()
#             if user_answer.strip().lower() == correct:
#                 st.success("✅ Correct!")
#                 st.session_state["score"] += 1
#             else:
#                 st.error(f"❌ Incorrect. Correct answer: {correct}")

#             st.session_state["index"] += 1

#     elif "quiz" in st.session_state and st.session_state["index"] >= len(st.session_state["quiz"]):
#         st.success(f"🎉 Quiz complete! You scored {st.session_state['score']}/{len(st.session_state['quiz'])}")
#         if st.button("Restart Quiz"):
#             del st.session_state["quiz"]
#             del st.session_state["index"]
#             del st.session_state["score"]






