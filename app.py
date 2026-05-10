from pathlib import Path
import os
import re
import sys
import tkinter as tk
from tkinter import messagebox, ttk


def prepare_swi_prolog_path():
    """Help PySwip find SWI-Prolog on Windows when PATH was not updated."""
    if os.name != "nt":
        return

    for root in (Path("C:/Program Files/swipl"), Path("C:/Program Files (x86)/swipl")):
        bin_dir = root / "bin"
        if bin_dir.exists():
            os.environ.setdefault("SWI_HOME_DIR", str(root))
            current_path = os.environ.get("PATH", "")
            if str(bin_dir) not in current_path:
                os.environ["PATH"] = f"{bin_dir}{os.pathsep}{current_path}"
            break


prepare_swi_prolog_path()

try:
    from pyswip import Prolog
except Exception as exc:
    Prolog = None
    PYSWIP_IMPORT_ERROR = exc
else:
    PYSWIP_IMPORT_ERROR = None


BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.pl"
CUSTOM_CASE = "custom_case"
DEFAULT_CUSTOM_SUSPECTS = 3
MAX_CUSTOM_SUSPECTS = 8

THEME = {
    "bg": "#171717",
    "panel": "#242424",
    "card": "#2d2d2d",
    "card_selected": "#3a241f",
    "border": "#4b3b2f",
    "accent": "#b22222",
    "gold": "#c8a45d",
    "error_bg": "#3b1f1f",
    "error_text": "#ffd6d6",
    "text": "#f4efe7",
    "muted": "#c9bfb1",
    "output": "#101010",
}

EVIDENCE_FIELDS = [
    ("has_motive", "Has motive"),
    ("has_weapon_access", "Weapon access"),
    ("was_at_scene", "At scene"),
    ("has_alibi", "Has alibi"),
    ("fingerprints_found", "Fingerprints"),
    ("witness_identified", "Witness"),
    ("had_conflict", "Conflict"),
    ("acted_suspiciously", "Suspicious act"),
]

REASON_TEXT = {
    "motive": "had a motive",
    "weapon_access": "had access to the weapon",
    "scene_presence": "was seen at the crime scene",
    "no_alibi": "has no confirmed alibi",
    "fingerprints": "has fingerprint evidence connected to the crime",
    "witness": "was identified by a witness",
    "conflict": "had a conflict with the victim",
    "suspicious_behavior": "acted suspiciously after the crime",
}


class MurderMysteryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Murder Mystery Solver")
        self.geometry("1100x760")
        self.minsize(960, 680)
        self.configure(bg=THEME["bg"])

        self.prolog = None
        self.cases = []
        self.selected_case = tk.StringVar()
        self.case_cards = {}
        self.output = None

        self._setup_styles()
        self._load_prolog()
        self._build_case_screen()

    def _setup_styles(self):
        self.option_add("*Font", ("Segoe UI", 10))
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=THEME["bg"])
        style.configure("Panel.TFrame", background=THEME["panel"])
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["text"])
        style.configure("Muted.TLabel", background=THEME["bg"], foreground=THEME["muted"])
        style.configure("Panel.TLabel", background=THEME["panel"], foreground=THEME["text"])
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), background=THEME["bg"], foreground=THEME["text"])
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12), background=THEME["bg"], foreground=THEME["muted"])
        style.configure("Section.TLabel", font=("Segoe UI", 14, "bold"), background=THEME["panel"], foreground=THEME["gold"])
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8), background=THEME["accent"], foreground="#ffffff")
        style.map("TButton", background=[("active", "#8b0000")])
        style.configure("TEntry", fieldbackground="#f7f0e6")
        style.configure("TCheckbutton", background=THEME["panel"], foreground=THEME["text"])

    def _load_prolog(self):
        if Prolog is None:
            self._show_startup_error(
                "PySwip could not be imported.\n\n"
                "Install requirements with:\n"
                "pip install -r requirements.txt\n\n"
                f"Details: {PYSWIP_IMPORT_ERROR}"
            )
            return
        if not KB_PATH.exists():
            self._show_startup_error(f"Knowledge base not found:\n{KB_PATH}")
            return
        try:
            self.prolog = Prolog()
            self.prolog.consult(str(KB_PATH))
            self.cases = self._load_cases()
        except Exception as exc:
            self.prolog = None
            self._show_startup_error(
                "Could not start SWI-Prolog through PySwip.\n\n"
                "Make sure SWI-Prolog is installed and available on PATH.\n\n"
                f"Details: {exc}"
            )

    def _show_startup_error(self, message):
        print(message, file=sys.stderr)
        self.after(200, lambda: messagebox.showerror("Setup Error", message))

    def _query(self, query):
        if self.prolog is None:
            return []
        try:
            return list(self.prolog.query(query))
        except Exception as exc:
            messagebox.showerror("Query Error", f"Prolog query failed:\n{query}\n\n{exc}")
            return []

    def _one_value(self, query, variable):
        rows = self._query(query)
        return clean_value(rows[0].get(variable, "")) if rows else ""

    def _load_cases(self):
        cases = []
        for row in self._query("case_id(Case)"):
            case_id = clean_value(row["Case"])
            cases.append(self._case_data(case_id))
        return cases

    def _case_data(self, case_id):
        return {
            "id": case_id,
            "title": self._one_value(f"case_title({case_id}, Title)", "Title"),
            "victim": self._one_value(f"victim({case_id}, Victim)", "Victim"),
            "location": self._one_value(f"crime_location({case_id}, Location)", "Location"),
            "weapon": self._one_value(f"crime_weapon({case_id}, Weapon)", "Weapon"),
            "description": self._one_value(f"case_description({case_id}, Description)", "Description"),
        }

    def _refresh_cases(self):
        self.cases = self._load_cases()

    def _clear_window(self):
        for child in self.winfo_children():
            child.destroy()

    def _build_case_screen(self):
        self._refresh_cases()
        self.case_cards = {}
        self._clear_window()

        root = ttk.Frame(self, padding=28)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Murder Mystery Solver", style="Title.TLabel").pack(anchor="center")
        ttk.Label(root, text="Select a crime case to investigate", style="Subtitle.TLabel").pack(anchor="center", pady=(4, 22))

        if not self.cases:
            ttk.Label(root, text="No cases could be loaded. Check PySwip and SWI-Prolog.", style="Subtitle.TLabel").pack(pady=30)
            return

        grid = ttk.Frame(root)
        grid.pack(fill="both", expand=True)

        for index, case in enumerate(self.cases):
            row = index // 3
            col = index % 3
            self._create_case_card(grid, case, row, col)

        for col in range(3):
            grid.columnconfigure(col, weight=1, uniform="cases")
        for row in range(2):
            grid.rowconfigure(row, weight=1)

        ttk.Button(root, text="Start Investigation", command=self._start_investigation).pack(pady=(18, 0), ipadx=18)

    def _create_case_card(self, parent, case, row, col):
        card = tk.Frame(parent, bg=THEME["card"], highlightbackground=THEME["border"], highlightthickness=1, padx=16, pady=14)
        card.grid(row=row, column=col, sticky="nsew", padx=9, pady=9)
        self.case_cards[case["id"]] = card

        title = "Create Your Own Mystery" if case["id"] == CUSTOM_CASE else case["title"]
        desc = (
            "Build a custom case by entering suspects and evidence manually."
            if case["id"] == CUSTOM_CASE
            else preview_text(case["description"], 170)
        )

        tk.Radiobutton(
            card,
            text=title,
            value=case["id"],
            variable=self.selected_case,
            command=self._refresh_selected_card_styles,
            bg=THEME["card"],
            activebackground=THEME["card"],
            fg=THEME["text"],
            activeforeground=THEME["text"],
            selectcolor=THEME["accent"],
            font=("Segoe UI", 12, "bold"),
            wraplength=280,
            justify="left",
        ).pack(anchor="w")

        if case["id"] != CUSTOM_CASE:
            details = f"Victim: {display_name(case['victim'])}\nLocation: {display_name(case['location'])}\nWeapon: {display_name(case['weapon'])}"
            tk.Label(card, text=details, bg=THEME["card"], fg=THEME["gold"], justify="left", anchor="w").pack(anchor="w", pady=(10, 8), fill="x")

        tk.Label(card, text=desc, bg=THEME["card"], fg=THEME["muted"], justify="left", anchor="nw", wraplength=300).pack(anchor="w", fill="both", expand=True)

        def select_card(_event=None, case_id=case["id"]):
            self.selected_case.set(case_id)
            self._refresh_selected_card_styles()

        card.bind("<Button-1>", select_card)
        for child in card.winfo_children():
            child.bind("<Button-1>", select_card)

    def _refresh_selected_card_styles(self):
        selected = self.selected_case.get()
        for case_id, card in self.case_cards.items():
            color = THEME["card_selected"] if case_id == selected else THEME["card"]
            card.configure(bg=color, highlightbackground=THEME["accent"] if case_id == selected else THEME["border"], highlightthickness=2 if case_id == selected else 1)
            for child in card.winfo_children():
                try:
                    child.configure(bg=color, activebackground=color)
                except tk.TclError:
                    child.configure(bg=color)

    def _start_investigation(self):
        case_id = self.selected_case.get()
        if not case_id:
            messagebox.showinfo("Select a Case", "Please select a crime case before starting the investigation.")
            return
        if case_id == CUSTOM_CASE:
            self._build_custom_case_screen()
            return
        self._build_investigation_screen()

    def _build_custom_case_screen(self):
        self._clear_window()
        self.custom_vars = {}
        self.suspect_rows = []
        self.add_suspect_button = None

        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Create Your Own Mystery", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            container,
            text="Enter case facts, then add up to 8 suspects. Every visible suspect row needs a valid name; delete rows you do not want.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        self.validation_slot = ttk.Frame(container)
        self.validation_slot.pack(fill="x")
        self.validation_var = tk.StringVar()
        self.validation_label = tk.Label(
            self.validation_slot,
            textvariable=self.validation_var,
            bg=THEME["error_bg"],
            fg=THEME["error_text"],
            justify="left",
            anchor="w",
            wraplength=1000,
            padx=12,
            pady=10,
        )
        self.validation_label.pack(fill="x", pady=(0, 14))
        self.validation_label.pack_forget()

        details = ttk.Frame(container, style="Panel.TFrame", padding=16)
        details.pack(fill="x", pady=(0, 14))
        ttk.Label(details, text="Case Details", style="Section.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        fields = [
            ("title", "Case title", "The Custom Mystery"),
            ("victim", "Victim", "Victim Name"),
            ("location", "Location", "Study Room"),
            ("weapon", "Weapon", "Letter Opener"),
        ]
        for index, (key, label, default) in enumerate(fields, start=1):
            ttk.Label(details, text=label, style="Panel.TLabel").grid(row=index, column=0, sticky="w", padx=(0, 8), pady=4)
            var = tk.StringVar(value=default)
            self.custom_vars[key] = var
            ttk.Entry(details, textvariable=var, width=32).grid(row=index, column=1, sticky="ew", padx=(0, 18), pady=4)

        ttk.Label(details, text="Description", style="Panel.TLabel").grid(row=1, column=2, sticky="nw", padx=(0, 8), pady=4)
        description = tk.Text(details, height=5, width=42, wrap="word", bg="#f7f0e6", fg="#1a1a1a", relief="flat", padx=8, pady=6)
        description.insert("1.0", "A victim was found under suspicious circumstances. Several suspects had different motives and opportunities. The detective must inspect each clue and let Prolog decide which suspects match the rules.")
        description.grid(row=1, column=3, rowspan=4, sticky="nsew", pady=4)
        self.custom_vars["description"] = description
        details.columnconfigure(1, weight=1)
        details.columnconfigure(3, weight=1)

        suspects = ttk.Frame(container, style="Panel.TFrame", padding=16)
        suspects.pack(fill="both", expand=True)
        header = ttk.Frame(suspects, style="Panel.TFrame")
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Suspects and Evidence", style="Section.TLabel").pack(side="left")
        self.suspect_counter_var = tk.StringVar()
        ttk.Label(header, textvariable=self.suspect_counter_var, style="Panel.TLabel").pack(side="right")

        table_shell = ttk.Frame(suspects, style="Panel.TFrame")
        table_shell.pack(fill="both", expand=True)
        self.suspect_canvas = tk.Canvas(table_shell, bg=THEME["panel"], highlightthickness=0, height=230)
        scrollbar = ttk.Scrollbar(table_shell, orient="vertical", command=self.suspect_canvas.yview)
        self.suspect_rows_frame = ttk.Frame(self.suspect_canvas, style="Panel.TFrame")
        self.suspect_canvas_window = self.suspect_canvas.create_window((0, 0), window=self.suspect_rows_frame, anchor="nw")
        self.suspect_canvas.configure(yscrollcommand=scrollbar.set)
        self.suspect_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.suspect_rows_frame.bind(
            "<Configure>",
            lambda _event: self.suspect_canvas.configure(scrollregion=self.suspect_canvas.bbox("all")),
        )
        self.suspect_canvas.bind(
            "<Configure>",
            lambda event: self.suspect_canvas.itemconfigure(self.suspect_canvas_window, width=event.width),
        )

        self._draw_suspect_header()
        for default_name in ("Ali", "Mona", "Karim"):
            self._add_suspect_row(default_name)

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text="Create Case and Start Investigation", command=self._create_custom_case).pack(side="left", padx=(0, 10))
        self.add_suspect_button = ttk.Button(actions, text="Add Suspect", command=self._add_suspect_row)
        self.add_suspect_button.pack(side="left", padx=(0, 10))
        ttk.Button(actions, text="Back to Cases", command=self._build_case_screen).pack(side="left")

        self._update_suspect_counter()

    def _draw_suspect_header(self):
        ttk.Label(self.suspect_rows_frame, text="Suspect", style="Panel.TLabel").grid(row=0, column=0, sticky="w", padx=4, pady=(0, 6))
        for col, (_predicate, label) in enumerate(EVIDENCE_FIELDS, start=1):
            ttk.Label(self.suspect_rows_frame, text=label, style="Panel.TLabel").grid(row=0, column=col, padx=4, pady=(0, 6))
        ttk.Label(self.suspect_rows_frame, text="Remove", style="Panel.TLabel").grid(row=0, column=len(EVIDENCE_FIELDS) + 1, padx=4, pady=(0, 6))
        self.suspect_rows_frame.columnconfigure(0, weight=1)

    def _add_suspect_row(self, default_name=""):
        if len(self.suspect_rows) >= MAX_CUSTOM_SUSPECTS:
            self._show_custom_validation(f"You can add at most {MAX_CUSTOM_SUSPECTS} suspect rows.")
            return
        self._clear_custom_validation()

        row_data = {"name": tk.StringVar(value=default_name), "widgets": []}
        for predicate, _label in EVIDENCE_FIELDS:
            var = tk.BooleanVar(value=False)
            row_data[predicate] = var
        self._restore_suspect_row(row_data)
        self._update_suspect_counter()

    def _remove_suspect_row(self, row_data):
        self._clear_custom_validation()
        self.suspect_rows.remove(row_data)
        self._rebuild_suspect_rows()

    def _rebuild_suspect_rows(self):
        for child in self.suspect_rows_frame.winfo_children():
            child.destroy()
        self._draw_suspect_header()
        rows = list(self.suspect_rows)
        self.suspect_rows = []
        for row_data in rows:
            self._restore_suspect_row(row_data)
        self._update_suspect_counter()

    def _restore_suspect_row(self, row_data):
        row_data["widgets"] = []
        self.suspect_rows.append(row_data)
        row_index = len(self.suspect_rows)

        entry = ttk.Entry(self.suspect_rows_frame, textvariable=row_data["name"], width=22)
        entry.grid(row=row_index, column=0, sticky="ew", padx=4, pady=5)
        row_data["widgets"].append(entry)
        for col, (predicate, _label) in enumerate(EVIDENCE_FIELDS, start=1):
            checkbox = ttk.Checkbutton(self.suspect_rows_frame, variable=row_data[predicate])
            checkbox.grid(row=row_index, column=col, padx=4, pady=5)
            row_data["widgets"].append(checkbox)
        remove_button = ttk.Button(
            self.suspect_rows_frame,
            text="Delete",
            command=lambda data=row_data: self._remove_suspect_row(data),
        )
        remove_button.grid(row=row_index, column=len(EVIDENCE_FIELDS) + 1, padx=4, pady=5)
        row_data["widgets"].append(remove_button)

    def _update_suspect_counter(self):
        count = len(self.suspect_rows)
        self.suspect_counter_var.set(f"Suspects: {count} / {MAX_CUSTOM_SUSPECTS}")
        if self.add_suspect_button is not None and self.add_suspect_button.winfo_exists():
            state = "disabled" if count >= MAX_CUSTOM_SUSPECTS else "normal"
            self.add_suspect_button.configure(state=state)

    def _create_custom_case(self):
        self._clear_custom_validation()
        try:
            title = require_text(self.custom_vars["title"].get(), "Case title")
            victim = required_atom(self.custom_vars["victim"].get(), "Victim")
            location = required_atom(self.custom_vars["location"].get(), "Location")
            weapon = required_atom(self.custom_vars["weapon"].get(), "Weapon")
            description = require_text(self.custom_vars["description"].get("1.0", "end"), "Description")
            suspects = self._validated_custom_suspects()
        except ValueError as exc:
            self._show_custom_validation(str(exc))
            return

        self._clear_custom_case_facts()

        self._assert_fact(f"case_title({CUSTOM_CASE}, {quote_prolog_atom(title)})")
        self._assert_fact(f"victim({CUSTOM_CASE}, {victim})")
        self._assert_fact(f"crime_location({CUSTOM_CASE}, {location})")
        self._assert_fact(f"crime_weapon({CUSTOM_CASE}, {weapon})")
        self._assert_fact(f"case_description({CUSTOM_CASE}, {quote_prolog_atom(description)})")

        for suspect_atom, row in suspects:
            self._assert_fact(f"suspect({CUSTOM_CASE}, {suspect_atom})")
            for predicate, _label in EVIDENCE_FIELDS:
                if row[predicate].get():
                    self._assert_fact(f"{predicate}({CUSTOM_CASE}, {suspect_atom})")

        saved_suspects = self._people_from_query(f"suspect({CUSTOM_CASE}, X)")
        if len(saved_suspects) != len(suspects):
            self._show_custom_validation("The custom suspects were not saved correctly in Prolog. Please try again.")
            return

        self.selected_case.set(CUSTOM_CASE)
        self._refresh_cases()
        self._build_investigation_screen()

    def _show_custom_validation(self, message):
        self.validation_var.set(f"Please fix this before creating the case:\n{message}")
        if not self.validation_label.winfo_ismapped():
            self.validation_label.pack(fill="x", pady=(0, 14))

    def _clear_custom_validation(self):
        if hasattr(self, "validation_var"):
            self.validation_var.set("")
        if hasattr(self, "validation_label") and self.validation_label.winfo_ismapped():
            self.validation_label.pack_forget()

    def _validated_custom_suspects(self):
        suspects = []
        seen_atoms = {}

        for index, row in enumerate(self.suspect_rows, start=1):
            raw_name = row["name"].get().strip()
            if not raw_name:
                raise ValueError(f"Suspect row {index} has no name. Enter a real name or delete the row.")
            try:
                atom = to_prolog_atom(raw_name)
            except ValueError:
                raise ValueError(
                    f"Suspect row {index} has an invalid name. "
                    "Use a real name with at least one letter, not only numbers or symbols."
                )

            if atom in seen_atoms:
                raise ValueError(
                    f"Duplicate suspect name after normalization: '{raw_name}' matches '{seen_atoms[atom]}'."
                )
            seen_atoms[atom] = raw_name
            suspects.append((atom, row))

        if len(suspects) > MAX_CUSTOM_SUSPECTS:
            raise ValueError(f"Please enter no more than {MAX_CUSTOM_SUSPECTS} suspects.")
        return suspects

    def _clear_custom_case_facts(self):
        self._query("clear_custom_case")

    def _assert_fact(self, fact):
        self._query(f"assertz(({fact}))")

    def _build_investigation_screen(self):
        self._refresh_cases()
        self._clear_window()
        case = self._current_case()

        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        summary = ttk.Frame(container, style="Panel.TFrame", padding=18)
        summary.pack(fill="x", pady=(0, 18))
        ttk.Label(summary, text=f"Case: {case['title']}", style="Section.TLabel").pack(anchor="w")
        facts = f"Victim: {display_name(case['victim'])}    Location: {display_name(case['location'])}    Weapon: {display_name(case['weapon'])}"
        ttk.Label(summary, text=facts, style="Panel.TLabel").pack(anchor="w", pady=(6, 10))
        tk.Label(
            summary,
            text=f"Description:\n{case['description']}",
            bg=THEME["panel"],
            fg=THEME["muted"],
            justify="left",
            anchor="w",
            wraplength=980,
        ).pack(anchor="w", fill="x")

        body = ttk.Frame(container)
        body.pack(fill="both", expand=True)

        button_panel = ttk.Frame(body, style="Panel.TFrame", padding=14)
        button_panel.pack(side="left", fill="y", padx=(0, 18))
        ttk.Label(button_panel, text="Investigation Queries", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        buttons = [
            ("Show All Suspects", self.show_all_suspects),
            ("Find Suspicious Suspects", self.show_suspicious),
            ("Find Strongly Suspicious Suspects", self.show_strongly_suspicious),
            ("Find Likely Murderer", self.show_likely_murderer),
            ("Show Innocent Suspects", self.show_innocent),
            ("Show Evidence Scores", self.show_evidence_scores),
            ("Back to Cases", self._build_case_screen),
        ]
        for label, command in buttons:
            ttk.Button(button_panel, text=label, command=command).pack(fill="x", pady=5)

        output_frame = ttk.Frame(body)
        output_frame.pack(side="left", fill="both", expand=True)
        self.output = tk.Text(
            output_frame,
            wrap="word",
            font=("Consolas", 11),
            bg=THEME["output"],
            fg=THEME["text"],
            insertbackground=THEME["text"],
            relief="solid",
            borderwidth=1,
            padx=14,
            pady=14,
        )
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        scrollbar.pack(side="right", fill="y")
        self.output.configure(yscrollcommand=scrollbar.set)
        self._write_output("CASE FILE READY\n\nChoose an investigation query from the left.")

    def _current_case(self):
        case_id = self.selected_case.get()
        return next(case for case in self.cases if case["id"] == case_id)

    def _write_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def _people_from_query(self, query):
        return [clean_value(row["X"]) for row in self._query(query)]

    def _show_people(self, title, query):
        people = self._people_from_query(query)
        descriptions = {
            "Suspicious Suspects": "These suspects have no confirmed alibi and at least one suspicious clue.",
            "Strongly Suspicious Suspects": "These suspects had motive, were at the scene, and have no confirmed alibi.",
        }
        if not people:
            context = f"\n{descriptions[title]}\n" if title in descriptions else ""
            self._write_output(f"{title.upper()}\n{'=' * len(title)}{context}\nNo results found for this query.")
            return
        lines = [title.upper(), "=" * len(title)]
        if title in descriptions:
            lines.extend(["", descriptions[title]])
        lines.append("")
        lines.extend(f"- {display_name(person)}" for person in people)
        self._write_output("\n".join(lines))

    def show_all_suspects(self):
        case_id = self.selected_case.get()
        self._show_people("All Suspects", f"suspect({case_id}, X)")

    def show_suspicious(self):
        case_id = self.selected_case.get()
        self._show_people("Suspicious Suspects", f"suspicious({case_id}, X)")

    def show_strongly_suspicious(self):
        case_id = self.selected_case.get()
        self._show_people("Strongly Suspicious Suspects", f"strongly_suspicious({case_id}, X)")

    def show_innocent(self):
        case_id = self.selected_case.get()
        self._show_people("Innocent Suspects", f"innocent({case_id}, X)")

    def show_likely_murderer(self):
        case_id = self.selected_case.get()
        murderers = self._people_from_query(f"likely_murderer({case_id}, X)")
        if not murderers:
            self._write_output(
                "LIKELY MURDERER\n===============\n\n"
                "These suspects match the strongest rule: motive, weapon access, scene presence, no alibi, and strong evidence.\n\n"
                "No likely murderer found.\n\n"
                "No suspect matched all required Prolog conditions: motive, weapon access, scene presence, no alibi, "
                "and at least one strong connecting clue."
            )
            return

        blocks = [
            "LIKELY MURDERER",
            "===============",
            "",
            "These suspects match the strongest rule: motive, weapon access, scene presence, no alibi, and strong evidence.",
        ]
        for person in murderers:
            blocks.extend(["", display_name(person), "", "Reason:"])
            blocks.extend(self._explanation_lines(case_id, person))
        self._write_output("\n".join(blocks))

    def _explanation_lines(self, case_id, person):
        rows = self._query(f"reason({case_id}, {person}, Reason)")
        reasons = [clean_value(row["Reason"]) for row in rows]
        lines = [f"- {display_name(person)} {REASON_TEXT[reason]}." for reason in reasons if reason in REASON_TEXT]
        if self._query(f"suspect({case_id}, {person})"):
            lines.insert(0, f"- {display_name(person)} is a suspect in this case.")
        return lines

    def show_evidence_scores(self):
        case_id = self.selected_case.get()
        rows = self._query(f"evidence_score({case_id}, X, Score)")
        if not rows:
            self._write_output("EVIDENCE SCORES\n===============\n\nNo results found for this query.")
            return

        scored = [(clean_value(row["X"]), int(row["Score"])) for row in rows]
        scored.sort(key=lambda item: (-item[1], item[0]))
        lines = ["EVIDENCE SCORES", "===============", ""]
        for person, score in scored:
            evidence = self._evidence_points(case_id, person)
            evidence_text = ", ".join(format_evidence(item) for item in evidence) or "no evidence points"
            lines.append(f"- {display_name(person)}: {score} ({evidence_text})")
        self._write_output("\n".join(lines))

    def _evidence_points(self, case_id, person):
        return [clean_value(row["Evidence"]) for row in self._query(f"evidence_point({case_id}, {person}, Evidence)")]


def clean_value(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def display_name(value):
    return clean_value(value).replace("_", " ").title()


def format_evidence(value):
    return clean_value(value).replace("_", " ")


def preview_text(text, max_length):
    text = " ".join(clean_value(text).split())
    return text if len(text) <= max_length else text[: max_length - 3].rstrip() + "..."


def require_text(value, label):
    text = clean_value(value).strip()
    if not text:
        raise ValueError(f"{label} cannot be empty.")
    return text


def required_atom(value, label):
    text = require_text(value, label)
    try:
        return to_prolog_atom(text)
    except ValueError:
        raise ValueError(f"{label} must contain at least one letter and be usable as a Prolog atom.")


def to_prolog_atom(value):
    atom = clean_value(value).strip().lower().replace(" ", "_")
    atom = re.sub(r"[^a-z0-9_]", "", atom)
    atom = re.sub(r"_+", "_", atom).strip("_")
    if not atom or not re.search(r"[a-z]", atom):
        raise ValueError("Invalid Prolog atom")
    if atom[0].isdigit():
        atom = f"p_{atom}"
    return atom


def quote_prolog_atom(value):
    escaped = clean_value(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


if __name__ == "__main__":
    app = MurderMysteryApp()
    app.mainloop()
