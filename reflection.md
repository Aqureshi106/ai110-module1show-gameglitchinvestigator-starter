# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I ran the game for the first time, I noticed that there are three difficulties, being easy, normal and hard. It displayed the amount of attempts the user has along with the number ranges that the secret number is within. Also there was a developer viewer which allows seeing the secret number and history of choices the user inputted.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Bug 1: I expected the hints to lead me closer to the correct number but the hints are not accurate (Example being a game where the correct number is suppose to be 99 but each hint after a given input is to go lower, even below 1 despite the range of guesses being 1-100 inclusively)

Bug 2: I expected to play a new game once it was concluded but whether I guess the correct number or not and desire to play a new game, the new game option becomes unresponsive, this would even be the case if I desire to play the game under a new difficulty.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I utilized copilot to assist me in the project

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

What copilot suggested to me which was correct was I had asked in regards to the hints being inaccurate and the solution it provided was to swap the direction hints from both blocks as they had been previously inverted which resolved the issue. I verified the result through playing the game and saw that the guesses were accurate.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

What copilot suggested that was incorrect was when I wanted to solve the bug with restarting the game whether it was through changing the difficulty or out of interest, the suggestion provided would work out of interest but fail to work out in terms of changing the difficulty, so I needed to further expand for it to provide a better suggestion. I verified the result as I had tested the game also creating pytests to determine any issues.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

By inspecting the code, then playing the game to determine if the bug was truly solved; if the bug had not been solved, I would ask copilot for a suggestion upon what issue remains or noticed and why the bug still exists to provide a better suggestion.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
With the utilization of pytest, a test showed that when the game is over, the app should not keep showing hint messages, even if the hints are enabled. With this test, it helped to confirm that the final guess behavior is correct and that the game-over state takes priority over hint display logic.

- Did AI help you design or understand any tests? How?
Copilot assisted me in designing the tests as I asked for suggestions in providing assurance that the fixes are truly correct rather than solely relying on playing the game and testing it which cannot be feasible in determining if it was an overall fix.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
