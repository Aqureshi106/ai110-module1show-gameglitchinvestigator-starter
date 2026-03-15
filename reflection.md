# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I ran the game for the first time, I noticed that there were three difficulty levels, easy, normal, and hard. It displayed the amount of attempts the user has along with the number ranges that the secret number is within. There was also a developer viewer that allowed me to see the secret number and the history of guesses the user entered.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Bug 1: I expected the hints to lead me closer to the secret number, but the hints were not accurate. For example, in a game where the correct number was 99, the hints repeatedly told me to guess lower, even below 1, despite the valid range being 1–100.

Bug 2: I expected to play a new game once it was concluded but whether I guessed the correct number or not and desire to play a new game, the new game option becomes unresponsive, there was also the case if I tried to play the game under a new difficulty.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I utilized Copilot to assist me in the project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

What Copilot suggested to me which was correct was I had asked in regards to the hints being inaccurate and the solution it provided was to swap the direction hints from both blocks as they had been previously inverted which resolved the issue. I verified the result by playing the game and saw that the hints were accurate.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

What Copilot suggested that was incorrect was when I wanted to solve the bug with restarting the game either by changing the difficulty or restarting the game normally, the suggestion provided would work when restarting normally but failed when changing the difficulty, so I needed to further expand for it to provide a better suggestion. I verified the result by testing the game and creating pytest tests.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

By inspecting the code, then playing the game to determine if the bug was truly solved; if the bug had not been solved, I would ask Copilot for a suggestion upon what issue remains or noticed and why the bug still exists to provide a better suggestion.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

Using pytest, a test showed that when the game is over, the app should not keep showing hint messages, even if the hints are enabled. This test helped to confirm that the final guess behavior is correct and that the game-over state takes priority over hint display logic.

- Did AI help you design or understand any tests? How?

Copilot assisted me in designing the tests as I asked for suggestions in providing assurance that the fixes are truly correct rather than solely relying on playing the game and testing it which isn't always sufficient to determine the fix of the bug.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The secret number appeared to keep changing in the original app because Streamlit reruns the entire script whenever the user interacts with the interface. When this occurs, variables that aren't stored in session state get recreated, which can lead to the secret number being regenerated each time the app reruns.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

How I would explain Streamlit reruns and session state to a friend is by stating that Streamlit automatically reruns the app script whenever the user interacts with the interface so that the page can update. Because of this, normal variables reset each time, but session state allows certain values to persist across reruns so the program can maintain consistent behavior.

- What change did you make that finally gave the game a stable secret number?

The change that gave the game a stable secret number was storing the secret number inside Streamlit’s session state so that it would persist across reruns instead of being regenerated each time the app refreshed.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

A strategy from this project I desire to reuse in future labs and projects is a prompting strategy as not every suggestion Copilot provided was correct, leading me to expand upon the problem in order to find a correct suggestion leading to solving the bugs that I discovered.

- What is one thing you would do differently next time you work with AI on a coding task?

What I would do differently next time I work with artificial intelligence on a coding task is to always prioritize testing whether through interacting with the program or writing pytest tests, it is important to check to ensure the bug has been resolved.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project revealed to me that AI-generated code depends heavily on the quality of prompts. When provided with clear details and examples, AI can suggest accurate solutions, but it can also produce misleading or incorrect suggestions that must be verified.
