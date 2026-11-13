# California DMV Practice Test (EN + PT-BR)

Simulator for the California Class C knowledge test.

- 36 questions per test, 30 correct to pass, 3 choices per question (same as the adult original-license test)
- Every test is a new random draw from a bank of 340 questions, in the DMV's mix of topics; questions you have not seen come first
- English questions and answers, with a smaller Portuguese (PT-BR) translation in parentheses (can be switched off)
- Practice mode (answer and explanation after each question) and Exam mode (results at the end)
- Review of missed questions, saved in your browser

Questions are original, written from the rules in the official
[California Driver's Handbook](https://www.dmv.ca.gov/portal/handbook/california-driver-handbook/).
They are **not** the DMV's actual exam questions. This is an unofficial study tool.

## Run

Open `index.html`, or use the GitHub Pages link of this repository.

## Edit questions

Questions live in `src/q1.js`, `src/q2.js`, `src/q3.js`. Run `python3 build.py` to validate the bank and rebuild `index.html`.
