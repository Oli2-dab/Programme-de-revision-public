#Olivier Moreau
#
#2025
#
#CQFA : Exam 1 : théorie du vol

import streamlit as st
import random
import re

# Fonctions de génération aléatoire
def ISA_alt_1():
    return random.randrange(0, 50001, 500)

def ISA_temp_2():
    return random.randint(-90, 30)

def ISA_ISA_3():
    return random.randint(-20, 20)

# Nettoyage de la réponse utilisateur
def nettoyage_ISA(réponse):
    match = re.search(r"-?\d+", réponse)
    return int(match.group()) if match else None

# Génération d'une nouvelle question
def générer_question():
    type_q = random.randint(1, 3)
    st.session_state.type_question = type_q

    if type_q == 1:
        ISA_altitude = -1
        while ISA_altitude < 0:
            ISA_température = ISA_temp_2()
            ISA_ISA = ISA_ISA_3()
            dif_temp = (ISA_ISA - ISA_température) * -1
            ISA_altitude = (dif_temp - 15) / -2 * 1000
        st.session_state.données = {
            "ISA_ISA": ISA_ISA,
            "ISA_température": ISA_température,
            "réponse_correcte": round(ISA_altitude)
        }

    elif type_q == 2:
        ISA_altitude = ISA_alt_1()
        ISA_ISA = ISA_ISA_3()
        ISA_théorique = 15 - 2 * (ISA_altitude / 1000)
        ISA_température = ISA_ISA + ISA_théorique
        st.session_state.données = {
            "ISA_altitude": ISA_altitude,
            "ISA_ISA": ISA_ISA,
            "réponse_correcte": round(ISA_température)
        }

    elif type_q == 3:
        ISA_altitude = ISA_alt_1()
        ISA_température = ISA_temp_2()
        ISA_théorique = 15 - ISA_altitude / 1000 * 2
        ISA_ISA = ISA_température - ISA_théorique
        st.session_state.données = {
            "ISA_altitude": ISA_altitude,
            "ISA_température": ISA_température,
            "réponse_correcte": round(ISA_ISA)
        }

# Initialisation des états
if "étape" not in st.session_state:
    st.session_state.étape = "question"
if "type_question" not in st.session_state or "données" not in st.session_state:
    générer_question()

st.title("Quiz ISA ✈️🌡️")

# Étape 1 : Affichage de la question
if st.session_state.étape == "question":
    type_q = st.session_state.type_question
    données = st.session_state.données

    if type_q == 1:
        ISA_ISA = données["ISA_ISA"]
        ISA_température = données["ISA_température"]
        st.write(f"Vous volez dans des conditions d'ISA **{ISA_ISA}**.")
        st.write(f"La température extérieure est de **{ISA_température}°C**.")
        st.write("À quelle altitude, en pieds, volez-vous ?")

    elif type_q == 2:
        ISA_altitude = données["ISA_altitude"]
        ISA_ISA = données["ISA_ISA"]
        st.write(f"Vous volez à une altitude de **{ISA_altitude} pi**.")
        st.write(f"Les conditions d'ISA sont de **{ISA_ISA}**.")
        st.write("Quelle est la température extérieure en °C ?")

    elif type_q == 3:
        ISA_altitude = données["ISA_altitude"]
        ISA_température = données["ISA_température"]
        st.write(f"Vous volez à une altitude de **{ISA_altitude} pi**.")
        st.write(f"La température extérieure est de **{ISA_température}°C**.")
        st.write("Quel est l'ISA ?")

    réponse = st.text_input("Votre réponse :")
    if st.button("Valider ma réponse"):
        valeur = nettoyage_ISA(réponse)
        st.session_state.réponse_utilisateur = valeur
        st.session_state.étape = "correction"

# Étape 2 : Affichage de la correction
elif st.session_state.étape == "correction":
    valeur = st.session_state.réponse_utilisateur
    bonne = st.session_state.données["réponse_correcte"]

    if valeur is None:
        st.warning("Vous n'avez pas entré de chiffre.")
    elif round(valeur) == round(bonne):
        st.success("Bonne réponse ! 🎉")
    else:
        st.error(f"Mauvaise réponse. La bonne réponse était **{bonne}**.")

    if st.button("Question suivante"):
        st.session_state.étape = "question"
        st.session_state.réponse_utilisateur = None
        générer_question()