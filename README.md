# Murder Mystery Solver

A simple academic expert system that solves murder mystery cases using a Prolog knowledge base and a Python Tkinter GUI. Users select a predefined case or create a custom mystery, run investigation queries, and see suspects, evidence scores, innocent suspects, and likely murderer explanations inferred by Prolog rules.

## Technologies Used

- Prolog for facts and reasoning rules
- Python for the application
- Tkinter for the GUI
- PySwip to connect Python with SWI-Prolog

## Requirements

Install the Python dependency:

```bash
pip install -r requirements.txt
```

SWI-Prolog must also be installed. PySwip uses SWI-Prolog underneath, so the GUI cannot run Prolog queries without it. On Windows, the app also checks the common install path `C:\Program Files\swipl\bin`.

## Run

```bash
python app.py
```

## What the GUI Queries

The buttons in the investigation screen run Prolog queries such as:

```prolog
suspect(Case, X).
suspicious(Case, X).
strongly_suspicious(Case, X).
likely_murderer(Case, X).
innocent(Case, X).
evidence_score(Case, X, Score).
reason(Case, X, Reason).
```

## GUI Flows

The project has two investigation flows:

- Predefined case investigation: choose one of 5 built-in cases, read the case description, and run query buttons.
- Custom case creation: enter a title, victim, location, weapon, description, and up to 8 suspects with evidence checkboxes. Every visible suspect row must have a valid name; delete all suspect rows if you intentionally want a case with no suspects. A custom case can also have no likely murderer. The app asserts those facts into Prolog as `custom_case`, then uses the same rules as the predefined cases.

## Knowledge Base

`knowledge_base.pl` contains five predefined crime cases plus a custom case placeholder. Each predefined case has a victim, location, weapon, story description, suspects, and clues such as motive, weapon access, scene presence, alibi, fingerprints, witness evidence, conflict, and suspicious behavior.

The custom case builder calls the Prolog rule `clear_custom_case/0`, then uses `assertz/1` to add the user's new facts. The final answers are not hardcoded in Python; Prolog rules still infer the results.

Custom case validation checks that required case fields are filled and visible suspect names normalize into valid, unique Prolog atoms.

The Prolog rules infer:

- innocent suspects from confirmed alibis
- suspicious suspects from no alibi plus at least one clue
- strongly suspicious suspects from motive, scene presence, and lack of alibi
- likely murderer candidates from motive, weapon access, scene presence, no alibi, and strong evidence
- evidence scores by counting matching evidence points
