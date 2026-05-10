% Murder Mystery Solver knowledge base.
% Facts describe five separate cases; rules infer innocence, suspicion,
% stronger suspicion, likely murderer status, and evidence scores.

:- dynamic case_title/2.
:- dynamic victim/2.
:- dynamic crime_location/2.
:- dynamic crime_weapon/2.
:- dynamic case_description/2.
:- dynamic suspect/2.
:- dynamic has_motive/2.
:- dynamic has_weapon_access/2.
:- dynamic was_at_scene/2.
:- dynamic has_alibi/2.
:- dynamic fingerprints_found/2.
:- dynamic witness_identified/2.
:- dynamic had_conflict/2.
:- dynamic acted_suspiciously/2.

:- discontiguous case_title/2.
:- discontiguous victim/2.
:- discontiguous crime_location/2.
:- discontiguous crime_weapon/2.
:- discontiguous case_description/2.
:- discontiguous suspect/2.
:- discontiguous has_motive/2.
:- discontiguous has_weapon_access/2.
:- discontiguous was_at_scene/2.
:- discontiguous has_alibi/2.
:- discontiguous fingerprints_found/2.
:- discontiguous witness_identified/2.
:- discontiguous had_conflict/2.
:- discontiguous acted_suspiciously/2.

case_id(office_murder).
case_id(mansion_murder).
case_id(library_murder).
case_id(hotel_murder).
case_id(garden_murder).
case_id(custom_case).

% Case 1: The Office Murder
case_title(office_murder, 'The Office Murder').
victim(office_murder, omar).
crime_location(office_murder, office).
crime_weapon(office_murder, knife).
case_description(office_murder, 'Omar was found dead late at night inside his private office after a tense board meeting. The door was unlocked, several contract files were scattered across the desk, and a knife was found near the body. Multiple employees had recently argued with Omar about money, promotions, and missing records. The detective must compare motives, alibis, and physical evidence to identify who most likely killed him.').

suspect(office_murder, john).
suspect(office_murder, sara).
suspect(office_murder, lina).
suspect(office_murder, kareem).
suspect(office_murder, nadia).

has_motive(office_murder, john).
has_motive(office_murder, sara).
has_motive(office_murder, lina).
has_weapon_access(office_murder, john).
has_weapon_access(office_murder, kareem).
was_at_scene(office_murder, john).
was_at_scene(office_murder, sara).
was_at_scene(office_murder, kareem).
has_alibi(office_murder, lina).
has_alibi(office_murder, nadia).
fingerprints_found(office_murder, john).
witness_identified(office_murder, john).
had_conflict(office_murder, john).
had_conflict(office_murder, sara).
acted_suspiciously(office_murder, john).
acted_suspiciously(office_murder, kareem).

% Case 2: The Mansion Murder
case_title(mansion_murder, 'The Mansion Murder').
victim(mansion_murder, laila).
crime_location(mansion_murder, mansion).
crime_weapon(mansion_murder, poison).
case_description(mansion_murder, 'Laila collapsed during a private dinner at her family mansion, and the doctor later confirmed she had been poisoned. The kitchen staff reported that several guests moved freely between the dining room and the serving area before dessert was served. Laila had recently changed her will, angering more than one person in the house. The case needs careful investigation because almost everyone had opportunity, but only one suspect fits the strongest evidence.').

suspect(mansion_murder, adam).
suspect(mansion_murder, mona).
suspect(mansion_murder, rami).
suspect(mansion_murder, dina).
suspect(mansion_murder, youssef).

has_motive(mansion_murder, mona).
has_motive(mansion_murder, rami).
has_motive(mansion_murder, adam).
has_weapon_access(mansion_murder, mona).
has_weapon_access(mansion_murder, dina).
was_at_scene(mansion_murder, mona).
was_at_scene(mansion_murder, rami).
was_at_scene(mansion_murder, dina).
has_alibi(mansion_murder, adam).
has_alibi(mansion_murder, youssef).
fingerprints_found(mansion_murder, mona).
witness_identified(mansion_murder, rami).
had_conflict(mansion_murder, mona).
had_conflict(mansion_murder, rami).
acted_suspiciously(mansion_murder, mona).
acted_suspiciously(mansion_murder, dina).

% Case 3: The Library Murder
case_title(library_murder, 'The Library Murder').
victim(library_murder, hazem).
crime_location(library_murder, library).
crime_weapon(library_murder, candlestick).
case_description(library_murder, 'Hazem was discovered between the history shelves after the city library closed for the evening. A heavy brass candlestick was missing from the reading table and later found hidden behind a return cart. Earlier that week, Hazem had accused several visitors and staff members of stealing rare manuscripts. The detective must decide which suspect had the motive, access, and evidence linking them to the scene.').

suspect(library_murder, farah).
suspect(library_murder, basel).
suspect(library_murder, salma).
suspect(library_murder, tarek).
suspect(library_murder, nour).

has_motive(library_murder, basel).
has_motive(library_murder, salma).
has_motive(library_murder, farah).
has_weapon_access(library_murder, basel).
has_weapon_access(library_murder, nour).
was_at_scene(library_murder, basel).
was_at_scene(library_murder, salma).
was_at_scene(library_murder, nour).
has_alibi(library_murder, farah).
has_alibi(library_murder, tarek).
fingerprints_found(library_murder, basel).
witness_identified(library_murder, basel).
had_conflict(library_murder, basel).
had_conflict(library_murder, salma).
acted_suspiciously(library_murder, basel).
acted_suspiciously(library_murder, nour).

% Case 4: The Hotel Murder
case_title(hotel_murder, 'The Hotel Murder').
victim(hotel_murder, maya).
crime_location(hotel_murder, hotel).
crime_weapon(hotel_murder, scarf).
case_description(hotel_murder, 'Maya was found dead in a quiet hotel corridor shortly after a charity reception. A scarf from the cloakroom was identified as the murder weapon, and witnesses reported raised voices near the service elevator. The victim had been preparing to expose a financial scheme connected to several guests. The investigation must separate nervous witnesses from the person whose evidence points to murder.').

suspect(hotel_murder, hassan).
suspect(hotel_murder, mariam).
suspect(hotel_murder, sami).
suspect(hotel_murder, yara).
suspect(hotel_murder, omnia).

has_motive(hotel_murder, yara).
has_motive(hotel_murder, hassan).
has_motive(hotel_murder, sami).
has_weapon_access(hotel_murder, yara).
has_weapon_access(hotel_murder, mariam).
was_at_scene(hotel_murder, yara).
was_at_scene(hotel_murder, hassan).
was_at_scene(hotel_murder, mariam).
has_alibi(hotel_murder, sami).
has_alibi(hotel_murder, omnia).
fingerprints_found(hotel_murder, yara).
witness_identified(hotel_murder, yara).
had_conflict(hotel_murder, yara).
had_conflict(hotel_murder, hassan).
acted_suspiciously(hotel_murder, yara).
acted_suspiciously(hotel_murder, mariam).

% Case 5: The Garden Murder
case_title(garden_murder, 'The Garden Murder').
victim(garden_murder, fady).
crime_location(garden_murder, garden).
crime_weapon(garden_murder, shovel).
case_description(garden_murder, 'Fady was found beside the greenhouse before sunrise, with a muddy shovel lying nearby. The garden gate had been forced open, but the tool shed showed signs that someone used a key. Fady had been involved in a bitter dispute over the property and several suspects were seen near the garden path. The detective must use the clues to determine whose story fails under Prolog reasoning.').

suspect(garden_murder, ali).
suspect(garden_murder, dina).
suspect(garden_murder, george).
suspect(garden_murder, hana).
suspect(garden_murder, selim).

has_motive(garden_murder, george).
has_motive(garden_murder, hana).
has_motive(garden_murder, ali).
has_weapon_access(garden_murder, george).
has_weapon_access(garden_murder, selim).
was_at_scene(garden_murder, george).
was_at_scene(garden_murder, hana).
was_at_scene(garden_murder, selim).
has_alibi(garden_murder, ali).
has_alibi(garden_murder, dina).
fingerprints_found(garden_murder, george).
witness_identified(garden_murder, george).
had_conflict(garden_murder, george).
had_conflict(garden_murder, hana).
acted_suspiciously(garden_murder, george).
acted_suspiciously(garden_murder, selim).

% Placeholder facts for the user-created case. The GUI replaces these facts
% with user input before investigating custom_case.
case_title(custom_case, 'Create Your Own Mystery').
victim(custom_case, unknown_victim).
crime_location(custom_case, unknown_location).
crime_weapon(custom_case, unknown_weapon).
case_description(custom_case, 'Build a custom case by entering suspects and evidence manually. Prolog will use the same rules to infer suspicious suspects, innocent suspects, evidence scores, and likely murderer candidates.').

% Reasoning rules
innocent(Case, Person) :-
    suspect(Case, Person),
    has_alibi(Case, Person).

suspicious(Case, Person) :-
    suspect(Case, Person),
    \+ has_alibi(Case, Person),
    once((
        has_motive(Case, Person);
        has_weapon_access(Case, Person);
        was_at_scene(Case, Person);
        fingerprints_found(Case, Person);
        witness_identified(Case, Person);
        had_conflict(Case, Person);
        acted_suspiciously(Case, Person)
    )).

strongly_suspicious(Case, Person) :-
    suspect(Case, Person),
    has_motive(Case, Person),
    was_at_scene(Case, Person),
    \+ has_alibi(Case, Person).

likely_murderer(Case, Person) :-
    suspect(Case, Person),
    has_motive(Case, Person),
    has_weapon_access(Case, Person),
    was_at_scene(Case, Person),
    \+ has_alibi(Case, Person),
    once((
        fingerprints_found(Case, Person);
        witness_identified(Case, Person);
        acted_suspiciously(Case, Person)
    )).

evidence_point(Case, Person, motive) :-
    has_motive(Case, Person).

evidence_point(Case, Person, weapon_access) :-
    has_weapon_access(Case, Person).

evidence_point(Case, Person, scene_presence) :-
    was_at_scene(Case, Person).

evidence_point(Case, Person, fingerprints) :-
    fingerprints_found(Case, Person).

evidence_point(Case, Person, witness) :-
    witness_identified(Case, Person).

evidence_point(Case, Person, conflict) :-
    had_conflict(Case, Person).

evidence_point(Case, Person, suspicious_behavior) :-
    acted_suspiciously(Case, Person).

evidence_list(Case, Person, EvidenceList) :-
    suspect(Case, Person),
    findall(Evidence, evidence_point(Case, Person, Evidence), EvidenceList).

evidence_score(Case, Person, Score) :-
    evidence_list(Case, Person, EvidenceList),
    length(EvidenceList, Score).

reason(Case, Person, motive) :-
    has_motive(Case, Person).

reason(Case, Person, weapon_access) :-
    has_weapon_access(Case, Person).

reason(Case, Person, scene_presence) :-
    was_at_scene(Case, Person).

reason(Case, Person, no_alibi) :-
    suspect(Case, Person),
    \+ has_alibi(Case, Person).

reason(Case, Person, fingerprints) :-
    fingerprints_found(Case, Person).

reason(Case, Person, witness) :-
    witness_identified(Case, Person).

reason(Case, Person, conflict) :-
    had_conflict(Case, Person).

reason(Case, Person, suspicious_behavior) :-
    acted_suspiciously(Case, Person).

clear_custom_case :-
    retractall(case_title(custom_case, _)),
    retractall(victim(custom_case, _)),
    retractall(crime_location(custom_case, _)),
    retractall(crime_weapon(custom_case, _)),
    retractall(case_description(custom_case, _)),
    retractall(suspect(custom_case, _)),
    retractall(has_motive(custom_case, _)),
    retractall(has_weapon_access(custom_case, _)),
    retractall(was_at_scene(custom_case, _)),
    retractall(has_alibi(custom_case, _)),
    retractall(fingerprints_found(custom_case, _)),
    retractall(witness_identified(custom_case, _)),
    retractall(had_conflict(custom_case, _)),
    retractall(acted_suspiciously(custom_case, _)).
