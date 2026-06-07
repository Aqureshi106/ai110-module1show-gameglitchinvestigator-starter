def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: You flagged invalid-input behavior; Copilot and I tightened this to integer-only parsing.
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()

    if raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw)
    except Exception:
        return False, None, "Enter a whole number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    guess_value = int(guess)
    secret_value = int(secret)

    if guess_value == secret_value:
        return "Win", "🎉 Correct!"

    # FIX: We corrected swapped hint directions together during bug triage.
    if guess_value > secret_value:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Updates the player's score based on the game outcome and attempt number.
    This function implements a scoring system for a guessing game where:
    - A "Win" grants 100 points minus 10 per attempt (minimum 10 points)
    - A "Too High" guess grants or deducts 5 points based on attempt parity
    - A "Too Low" guess deducts 5 points
    - Any other outcome leaves the score unchanged
    Args:
        current_score (int): The player's current score before the update.
        outcome (str): The result of the player's guess. Expected values are:
            - "Win": Player guessed correctly
            - "Too High": Player's guess was higher than the target
            - "Too Low": Player's guess was lower than the target
        attempt_number (int): The current attempt number (0-indexed), used to
            calculate win points and determine odd/even for "Too High" outcomes.
    Returns:
        int: The updated score after applying the outcome logic.
    Examples:
        >>> update_score(0, "Win", 0)
        90
        >>> update_score(0, "Win", 9)
        10
        >>> update_score(50, "Too High", 2)
        55
        >>> update_score(50, "Too High", 1)
        45
        >>> update_score(50, "Too Low", 0)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def attempts_left(attempt_limit: int, attempts_used: int) -> int:
    # FIX: Added with Copilot to make attempts countdown testable and consistent in the UI.
    """Return remaining attempts after the number already used."""
    return attempt_limit - attempts_used


def guess_closeness_percent(guess: int, secret: int, low: int, high: int) -> int:
    """Return 0-100 closeness where 100 means the guess is exactly correct."""
    range_size = max(high - low, 1)
    distance = abs(int(guess) - int(secret))
    closeness = 100 - round((distance / range_size) * 100)
    return max(0, min(100, closeness))


def guess_temperature_label(closeness: int) -> tuple[str, str, str]:
    """Return a friendly Hot/Cold label, emoji, and Streamlit message style."""
    if closeness >= 85:
        return "Hot", "🔥", "error"
    if closeness >= 60:
        return "Warm", "🌤️", "warning"
    if closeness >= 30:
        return "Cool", "💧", "info"
    return "Cold", "🧊", "info"


def build_guess_summary(history: list[int], secret: int, low: int, high: int):
    """Build table-ready rows summarizing each guess in the current round."""
    rows = []
    for attempt_number, guess in enumerate(history, start=1):
        closeness = guess_closeness_percent(guess, secret, low, high)
        label, emoji, _style = guess_temperature_label(closeness)
        rows.append(
            {
                "Attempt": attempt_number,
                "Guess": guess,
                "Closeness": f"{closeness}%",
                "State": f"{emoji} {label}",
            }
        )
    return rows


def is_game_over(attempt_limit: int, attempts_used: int) -> bool:
    """Return True when no attempts remain."""
    return attempts_used >= attempt_limit


def should_show_hint(show_hint_enabled: bool, game_over: bool) -> bool:
    # FIX: Added after your game-over report so hints are hidden once attempts run out.
    """Hints are shown only when enabled and the game is still active."""
    return show_hint_enabled and not game_over


def next_attempt_count(current_attempts: int, guess_is_valid: bool) -> int:
    # FIX: Added with Copilot so invalid entries no longer consume attempts.
    """Only valid guesses should consume an attempt."""
    if guess_is_valid:
        return current_attempts + 1
    return current_attempts


def is_duplicate_guess(guess_history: list[int], guess: int) -> bool:
    # FIX: Added after your duplicate-guess feedback so repeats do not cost attempts.
    """Return True if the player has already submitted this guess."""
    return guess in guess_history
