import pytest
from logic_utils import (
    check_guess,
    parse_guess,
    attempts_left,
    is_game_over,
    should_show_hint,
    next_attempt_count,
    is_duplicate_guess,
)


# ---------------------------------------------------------------------------
# Basic (int vs int) cases
# ---------------------------------------------------------------------------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug-targeted: swapped hint messages (int vs int path)
#
# The original bug had the direction hints backwards:
#   guess > secret → "📈 Go HIGHER!" (wrong — should be "📉 Go LOWER!")
#   guess < secret → "📉 Go LOWER!"  (wrong — should be "📈 Go HIGHER!")
# ---------------------------------------------------------------------------

def test_hint_message_when_too_high():
    """When guess is above the secret the hint must say LOWER, not HIGHER."""
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, (
        f"Expected hint to say 'LOWER' when guess > secret, but got: '{message}'. "
        "The direction hints in check_guess were originally swapped."
    )
    assert "HIGHER" not in message, (
        f"Hint should NOT say 'HIGHER' when guess > secret, but got: '{message}'."
    )


def test_hint_message_when_too_low():
    """When guess is below the secret the hint must say HIGHER, not LOWER."""
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, (
        f"Expected hint to say 'HIGHER' when guess < secret, but got: '{message}'. "
        "The direction hints in check_guess were originally swapped."
    )
    assert "LOWER" not in message, (
        f"Hint should NOT say 'LOWER' when guess < secret, but got: '{message}'."
    )


# ---------------------------------------------------------------------------
# Bug-targeted tests: int guess vs string secret (TypeError branch)
#
# In app.py, on even-numbered attempts the secret is cast to a string:
#   if st.session_state.attempts % 2 == 0:
#       secret = str(st.session_state.secret)
#
# This forces a TypeError in check_guess when comparing int > str.
# The 'Too Low' path inside that except block has a commented-out return
# (#FIXME), so the function silently returns None instead of
# ("Too Low", "📉 Go LOWER!").
# ---------------------------------------------------------------------------

def test_check_guess_win_int_vs_str_secret():
    """Correct guess should still be recognised as a Win when secret is a string."""
    outcome, message = check_guess(42, "42")
    assert outcome == "Win", (
        "check_guess should return 'Win' when int guess equals string secret."
    )


def test_check_guess_too_high_int_vs_str_secret():
    """Guess higher than secret (string) should return 'Too High' with a LOWER hint."""
    outcome, message = check_guess(90, "42")
    assert outcome == "Too High", (
        "check_guess should return 'Too High' when int guess > string secret."
    )
    assert "LOWER" in message, (
        f"Expected hint to say 'LOWER' when guess > string secret, but got: '{message}'."
    )


def test_check_guess_too_low_int_vs_str_secret():
    """
    BUG: When an int guess is LOWER than a stringified secret, the TypeError
    branch in check_guess falls through without returning because the
    'return "Too Low"' line is commented out (#FIXME).
    Also checks the hint message says HIGHER (not LOWER).
    """
    result = check_guess(10, "42")
    assert result is not None, (
        "check_guess returned None for a 'too low' guess against a string secret. "
        "The '#FIXME return \"Too Low\"' line in logic_utils.py must be uncommented."
    )
    outcome, message = result
    assert outcome == "Too Low", (
        f"Expected outcome 'Too Low' but got '{outcome}'. "
        "Uncomment the '#FIXME return \"Too Low\"' line in check_guess."
    )
    assert "HIGHER" in message, (
        f"Expected hint to say 'HIGHER' when guess < string secret, but got: '{message}'. "
        "The direction hints in the TypeError branch were also swapped."
    )


# ---------------------------------------------------------------------------
# Bug-targeted tests: attempts countdown and final-guess behavior
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "attempt_limit, attempts_used, expected_left",
    [
        (8, 0, 8),
        (8, 1, 7),
        (8, 7, 1),
        (8, 8, 0),
    ],
)
def test_attempts_left_counts_down_to_zero(
    attempt_limit, attempts_used, expected_left
):
    """Attempts left should decrement each guess and reach 0 on the final used attempt."""
    assert attempts_left(attempt_limit, attempts_used) == expected_left


def test_is_game_over_on_last_used_attempt():
    """Game should be over exactly when used attempts reaches the limit."""
    assert is_game_over(8, 7) is False
    assert is_game_over(8, 8) is True


def test_should_not_show_hint_when_game_is_over_even_if_enabled():
    """On the final wrong guess, the game-over message should take precedence over hints."""
    assert should_show_hint(True, False) is True
    assert should_show_hint(True, True) is False
    assert should_show_hint(False, False) is False


# ---------------------------------------------------------------------------
# Bug-targeted tests: invalid input should not be accepted or consume attempts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw", ["hello", "abc123", "4.2", "42.0"])
def test_parse_guess_rejects_strings_and_floats(raw):
    """Only whole-number input should be accepted as a guess."""
    ok, guess_int, err = parse_guess(raw)
    assert ok is False
    assert guess_int is None
    assert err == "Enter a whole number."


def test_parse_guess_accepts_integer_input_with_whitespace():
    """Whole-number input should still parse after trimming user whitespace."""
    ok, guess_int, err = parse_guess(" 42 ")
    assert ok is True
    assert guess_int == 42
    assert err is None


def test_invalid_input_does_not_consume_attempt():
    """Submitting invalid input should leave the attempt count unchanged."""
    assert next_attempt_count(0, guess_is_valid=False) == 0
    assert next_attempt_count(3, guess_is_valid=False) == 3


def test_valid_input_consumes_attempt():
    """Submitting a valid integer guess should consume exactly one attempt."""
    assert next_attempt_count(0, guess_is_valid=True) == 1
    assert next_attempt_count(3, guess_is_valid=True) == 4


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_parse_guess_rejects_blank_input(raw):
    """Blank input should be rejected without producing a guess value."""
    ok, guess_int, err = parse_guess(raw)
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."


@pytest.mark.parametrize("raw, expected", [("+7", 7), ("-3", -3), ("0", 0)])
def test_parse_guess_accepts_signed_integer_input(raw, expected):
    """Valid integer strings, including signed values, should still parse as ints."""
    ok, guess_int, err = parse_guess(raw)
    assert ok is True
    assert guess_int == expected
    assert err is None


def test_parse_guess_rejects_negative_decimal_input():
    """Decimal input should be rejected even when it looks close to an integer."""
    ok, guess_int, err = parse_guess("-3.14")
    assert ok is False
    assert guess_int is None
    assert err == "Enter a whole number."


# ---------------------------------------------------------------------------
# Bug-targeted tests: duplicate guesses should not consume attempts
# ---------------------------------------------------------------------------

def test_is_duplicate_guess_detects_repeated_number():
    """A repeated integer guess should be identified as duplicate."""
    history = [12, 50, 7]
    assert is_duplicate_guess(history, 50) is True


def test_is_duplicate_guess_allows_new_number():
    """A new integer guess should not be flagged as duplicate."""
    history = [12, 50, 7]
    assert is_duplicate_guess(history, 13) is False


def test_duplicate_guess_does_not_consume_attempt():
    """When a guess is duplicate, attempts should remain unchanged."""
    attempts_before = 3
    guess_is_new = not is_duplicate_guess([10, 22, 30], 22)
    attempts_after = next_attempt_count(attempts_before, guess_is_valid=guess_is_new)
    assert attempts_after == attempts_before
