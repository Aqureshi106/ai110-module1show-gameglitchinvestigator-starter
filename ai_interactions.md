## Agent Workflow

### What I Asked the Agent to Do

Plan and implement a meaningful new feature for the guessing game, such as a high score tracker or a guess history sidebar, and document the workflow in this file.

### What the Agent Completed

- Added a Guess History sidebar to `app.py` that lists previous guesses and displays a progress bar showing how close each guess was to the secret number.
- Added `guess_closeness_percent` to `logic_utils.py` so the closeness calculation is testable outside the Streamlit UI.
- Added unit tests in `tests/test_game_logic.py` for exact, far, and out-of-range guess closeness behavior.
- Kept the feature separate from scoring and attempt-count logic so viewing history does not change gameplay state.

### Files Modified

- `app.py`
- `logic_utils.py`
- `tests/test_game_logic.py`
- `ai_interactions.md`

### Manual Corrections Made

- Chose the Guess History sidebar instead of file-based high score persistence to avoid adding save-file complexity while still improving the game experience.
- Reviewed the diff after edits and kept the feature scoped to a small utility function plus sidebar rendering.

## Model Comparison: Phase 1 Logic Bug

### Bug Selected

The Phase 1 bug I compared was in `check_guess()`. The app sometimes passed the secret number as a string, which caused the original integer comparison to fail or behave incorrectly. A partial fix used a `try`/`except TypeError` branch, but that still compared values as strings in one path. For example, `90` and `"100"` could be ordered incorrectly if treated as text instead of numbers.

### Model 1: GitHub Copilot

Most of the code before this session was generated or edited with GitHub Copilot. Copilot helped move logic into `logic_utils.py` and produced a working-looking fix by catching `TypeError` inside `check_guess()`. Its approach was:

- Keep the original `guess > secret` comparison.
- Catch `TypeError` when an integer guess was compared to a string secret.
- Convert the guess to a string and compare against the string secret.
- Add the missing return for the too-low string-secret case.

This fixed the immediate crash/fall-through bug, but it was less Pythonic because it handled the symptom after the comparison failed. It also left a hidden edge case because string comparisons are lexicographic, not numeric.

### Model 2: ChatGPT / Codex

In this session, ChatGPT/Codex changed `check_guess()` so both inputs are converted to integers before any comparison:

- `guess_value = int(guess)`
- `secret_value = int(secret)`
- Compare `guess_value` and `secret_value` for win, too high, and too low outcomes.

This was more readable and more Pythonic because the function normalizes its inputs once at the top, then uses straightforward numeric comparisons. It also removed the extra `try`/`except TypeError` branch, which made the control flow shorter and easier to reason about.

### Which Fix Was More Readable / Pythonic?

ChatGPT/Codex gave the more readable and Pythonic fix. Converting both values to integers once is clearer than keeping two separate comparison paths. It also matches the game domain better because guesses and secrets are numbers, even if Streamlit or session state temporarily stores one value as a string.

### Which Explained the Why More Clearly?

ChatGPT/Codex explained the underlying cause more clearly: the issue was not only that `int > str` can raise a `TypeError`, but also that converting the guess to a string creates lexicographic comparisons. The important lesson is that game logic should compare numbers as numbers, not as text.

### Manual Correction / Final Choice

I kept the ChatGPT/Codex version because it fixed both the visible TypeError bug and the quieter high/low ordering bug. I also added a regression test for `check_guess(90, "100")` so the game confirms that string secrets are still compared numerically.
