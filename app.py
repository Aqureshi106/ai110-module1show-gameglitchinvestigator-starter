import random
import streamlit as st
# FIX: Refactored core game logic into logic_utils.py with Copilot Agent mode to keep app.py focused on UI/state.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    attempts_left,
    is_game_over,
    should_show_hint,
    next_attempt_count,
    is_duplicate_guess,
    guess_closeness_percent,
    guess_temperature_label,
    build_guess_summary,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# FIX: You reported mode-switch inconsistency; Copilot and I reset round state on difficulty change.
# Changing difficulty should start a fresh round in the new range.
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []


def render_guess_history_sidebar():
    st.sidebar.subheader("Guess History")
    if st.session_state.history:
        for attempt_number, previous_guess in enumerate(
            st.session_state.history,
            start=1,
        ):
            closeness = guess_closeness_percent(
                previous_guess,
                st.session_state.secret,
                low,
                high,
            )
            label, emoji, _style = guess_temperature_label(closeness)
            st.sidebar.caption(
                f"{attempt_number}. Guess {previous_guess} - "
                f"{emoji} {label}, {closeness}% close"
            )
            st.sidebar.progress(closeness)
    else:
        st.sidebar.caption("No guesses yet.")


def render_session_summary():
    st.subheader("Session Summary")
    if st.session_state.history:
        st.table(
            build_guess_summary(
                st.session_state.history,
                st.session_state.secret,
                low,
                high,
            )
        )
    else:
        st.caption("No submitted guesses yet.")


st.subheader("Make a guess")

# FIX: We replaced hardcoded range text with dynamic {low}/{high} and shared attempts logic.
attempts_display = st.empty()
attempts_display.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left(attempt_limit, st.session_state.attempts)}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: You reproduced the post-game restart bug; Copilot and I reset status/history so a finished round can start fresh.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    render_guess_history_sidebar()
    render_session_summary()
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

attempts_display.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left(attempt_limit, st.session_state.attempts)}"
)

if submit:
    # FIX: Validation now runs before attempt updates so bad inputs do not consume tries.
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    # FIX: Duplicate guesses are blocked based on your gameplay feedback.
    elif is_duplicate_guess(st.session_state.history, guess_int):
        st.warning("You already guessed that number. Try a different integer.")
    else:
        st.session_state.attempts = next_attempt_count(
            st.session_state.attempts,
            guess_is_valid=True,
        )
        attempts_display.info(
            f"Guess a number between {low} and {high}. "
            f"Attempts left: {attempts_left(attempt_limit, st.session_state.attempts)}"
        )
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        game_over = is_game_over(attempt_limit, st.session_state.attempts)

        # FIX: We suppress hints on final failed guess so game-over messaging is clear.
        if should_show_hint(show_hint, game_over):
            closeness = guess_closeness_percent(
                guess_int,
                st.session_state.secret,
                low,
                high,
            )
            label, emoji, style = guess_temperature_label(closeness)
            structured_hint = (
                f"{emoji} {label}: {message} "
                f"Your guess is {closeness}% close."
            )
            if style == "error":
                st.error(structured_hint)
            elif style == "warning":
                st.warning(structured_hint)
            else:
                st.info(structured_hint)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if game_over:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_guess_history_sidebar()
render_session_summary()

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
