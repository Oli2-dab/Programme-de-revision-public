import streamlit as st
import random
import re

# ------------------ UTILITAIRES ------------------

def nettoyage_ISA(réponse):
    match = re.search(r"-?\d+", réponse)
    return int(match.group()) if match else None

def nettoyer_mot(mot):
    mot = re.sub(r"^(l'|le|la|les|un|une|des|d')\s*", "", mot)
    mot = mot.replace("'", "")
    return mot.lower()

# ------------------ INITIALISATION ------------------

if "page" not in st.session_state:
    st.session_state.page = "menu"

# ------------------ MENU PRINCIPAL ------------------

if st.session_state.page == "menu":
    st.title("🛫 Bienvenue dans l'application d'examen")
    st.write("Choisissez une activité :")

    if st.button("📘 Répondre à des questions"):
        st.session_state.page = "quiz"
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.feedback = ""
        st.session_state.correction = ""

    if st.button("🌡️ Faire des problèmes ISA"):
        st.session_state.page = "isa"
        st.session_state.étape = "question"
        st.session_state.réponse_utilisateur = None
        st.session_state.type_question = random.randint(1, 3)
        st.session_state.données = {}

    if st.button("🧮 Autres types de problèmes (à venir)"):
        st.session_state.page = "autre"

# ------------------ BOUTON RETOUR ------------------

if st.session_state.page != "menu":
    st.sidebar.button("🏠 Retour au menu", on_click=lambda: st.session_state.update({"page": "menu"}))

# ------------------ PAGE QUIZ ------------------

if st.session_state.page == "quiz":
    st.title("✈️ Quiz de théorie du vol")

    liste_question = [

        #Définitions

        {"question": "Quel est la compostant où nous sommes assis dans l'avion?", "réponses": ["fuselage"], "mode": "tous"},
        {"question": "Quel est la partie porteuse d'un avion?", "réponses": ["aile"], "mode": "tous"},
        {"question": "Comment se nomme le bout de l'aile?", "réponses": ["saumon"], "mode": "tous"},
        {"question": "Comment se nomme la jonction entre l'aile et le fuselage?", "réponses": ["emplanture"], "mode": "tous"},
        {"question": "Comment se nomme l'avant de l'aile?", "réponses": ["bord", "attaque"], "mode": "tous"},
        {"question": "Comment se nomme l'arrière de l'aile?", "réponses": ["bord", "fuite"], "mode": "tous"},
        {"question": "Comment appelons-nous les catégories l'aile?", "réponses": ["profil", "profils"], "mode": "au_moins_un"},
        {"question": "Comment se nomme la partie qui assure la propultion?", "réponses": ["moteur", "moteurs"], "mode": "au_moins_un"},
        {"question": "Comment se nomme la partie à l'arrière de l'avion?", "réponses": ["empennage"], "mode": "tous"},
        {"question": "Comment se nomme le mouvement d'avant en arrière?", "réponses": ["tangage"], "mode": "tous"},
        {"question": "Selon quel axe le tengage se produit-il?", "réponses": ["latéral", "transversal"], "mode": "au_moins_un"},
        {"question": "Quels surfaces de contrôle est responsable du tengage?", "réponses": ["gouverne", "profondeur"], "mode": "tous"},
        {"question": "Comment se nomme le mouvement de droite à gauche en panchant?", "réponses": ["roulis"], "mode": "tous"},
        {"question": "Selon quel axe le roulis se produit-il?", "réponses": ["longitudinal"], "mode": "tous"},
        {"question": "Quels surfaces de contrôle est responsable du roulis?", "réponses": ["ailerons", "aileron"], "mode": "au_moins_un"},
        {"question": "Comment se nomme le mouvement de droite à gauche sans pancher?", "réponses": ["lacet"], "mode": "tous"},
        {"question": "Selon quel axe le lacet se produit-il?", "réponses": ["vertical"], "mode": "au_moins_un"},
        {"question": "Quels surfaces de contrôle est responsable du lacet?", "réponses": ["gouverne", "direction"], "mode": "tous"},
        {"question": "Comment se nomme la distance entre les deux saumons des ailes?", "réponses": ["envergure"], "mode": "tous"},
        {"question": "Comment se nomme la composante où se trouve les roues?", "réponses": ["train", "atterrissage"], "mode": "tous"},
        {"question": "Quels sont les quatres forces qui agissent sur un avion? (gravité n'est pas la bonne réponse)", "réponses": ["poids", "traction", "portance", "trainée"], "mode": "tous"},

        #Assiette
        {"question": "Comment se nomme l'assiette de référence?", "réponses": ["croisière"], "mode": "tous"},
        {"question": "Comment se nomme l'assiette où le nez est au dessus de l'horizon?", "réponses": ["cabrée"], "mode": "tous"},
        {"question": "Comment se nomme l'assiette où le nez est au dessous de l'horizon?", "réponses": ["piquée"], "mode": "tous"},
        {"question": "Comment se nomme l'assiette où l'on amorce un virage?", "réponses": ["inclinée"], "mode": "tous"},

        #Gouverne de vol
        {"question": "Quel est la définition d'une gouverne de vol?", "réponses": ["surface", "mobile", "varier", "assiette", "configuration", "avion"], "mode": "tous"},
        {"question": "Quels sont les deux types de surface de contrôle?", "réponses": ["primaire", "secondaire"], "mode": "tous"},
        {"question": "Quel est la définitions d'une surface de contrôle primaire?", "réponses": ["essentielles", "maneuvrer", "avion", "perte", "blocage", "risques", "majeurs"], "mode": "tous"},
        {"question": "Quel est la définitions d'une surface de contrôle secondaire?", "réponses": ["pas", "essentielles", "réduisent", "facilitent", "travail", "perte", "augmente", "travail", "pas", "danger"], "mode": "tous"},
        {"question": "Nomme une surface de contrôle secondaire?", "réponses": ["compensateurs", "volets", "déporteurs", "aérofreins"], "mode": "au_moins_un"},
        {"question": "Quel est le rôle des compensateurs?", "réponses": ["réduire", "effort", "manoeuvrer", "gouvernes"], "mode": "tous"},
        {"question": "Quel est le rôle des volets?", "réponses": ["augmenter", "portance", "basse", "vitesse"], "mode": "tous"},
        {"question": "Quel est le défaut des volets?", "réponses": ["augmenter", "traînée"], "mode": "tous"},
        {"question": "Quel est le rôle des déporteurs?", "réponses": ["augmentation", "traînée", "diminution", "portance"], "mode": "tous"},
        {"question": "Où sont situés les déporteurs?", "réponses": ["extrados"], "mode": "tous"},
        {"question": "Quel est le rôle des aérofreins?", "réponses": ["augmentation", "traînée"], "mode": "tous"},

        #Profils
        {"question": "Comment se nomme la partie du dessus de l'aile?", "réponses": ["extrados"], "mode": "tous"},
        {"question": "Comment se nomme la partie du dessous de l'aile?", "réponses": ["intrados"], "mode": "tous"},
        {"question": "Quel est la définition de la corde?", "réponses": ["ligne", "bord", "attaque", "bord", "fuite"], "mode": "tous"},
        {"question": "Comment se nomme la distance entre l'intrados et l'extrados?", "réponses": ["épaisseur"], "mode": "tous"},
        {"question": "Comment se nomme la ligne à la moitié entre l'intrados et l'extrados?", "réponses": ["moyenne"], "mode": "tous"},
        {"question": "Comment se nomme la superficie totale de la voilure, en incluant la partie qui traverse le fuselage?", "réponses": ["surface", "alaire"], "mode": "tous"},
        {"question": "Comment se nomme le  rapport du poids total à la superficie alaire?", "réponses": ["charge", "alaire"], "mode": "tous"},
        {"question": "Comment se nomme le poids apparent d'un avion en fonction de la masse et force d'inertie qu'il subit?", "réponses": ["facteur", "charge"], "mode": "tous"},
        {"question": "Comment se nomme l'angle entre un plan horizontal à la hauteur de l'emplanture de l'aile et l'aile?", "réponses": ["dièdre"], "mode": "tous"},
        {"question": "Quels sont les 3 types de dièdre?", "réponses": ["positif", "négatif", "poly"], "mode": "tous"},
        {"question": "Comment se nomme l'angle entre un plan transversal et le bord d'attaque des ailes?", "réponses": ["flèche"], "mode": "tous"},
        {"question": "Que veut dire MTOW? (En français)", "réponses": ["masse", "maximale", "décollage"], "mode": "tous"},
        {"question": "Que veut dire MRW? (En français)", "réponses": ["masse", "maximale", "aire", "trafic"], "mode": "tous"},
        {"question": "Que veut dire MLW? (En français)", "réponses": ["masse", "maximale", "atterrissage"], "mode": "tous"},
        {"question": "Que veut dire MZW? (En français)", "réponses": ["masse", "maximale", "sans", "carburant"], "mode": "tous"},
        {"question": "Quel est la partie du circuit juste après le décollage?", "réponses": ["vent", "debout"], "mode": "tous"},
        {"question": "Quel est la partie du circuit juste après le vent debout?", "réponses": ["vent", "travers"], "mode": "tous"},
        {"question": "Quel est la partie du circuit juste après le vent de travers?", "réponses": ["vent", "arrière"], "mode": "tous"},
        {"question": "Quel est la partie du circuit juste après le vent arrière?", "réponses": ["base"], "mode": "tous"},
        {"question": "Quel est la partie du circuit juste après la base?", "réponses": ["finale"], "mode": "tous"},

        #L'air

        {"question": "À quel altitude s'arrête la troposphère?", "réponses": ["360", "36000", "11000"], "mode": "au_moins_un"},
        {"question": "Quel est la couche juste au dessus de la troposhère?", "réponses": ["tropopause"], "mode": "tous"},
        {"question": "Quel est la couche juste au dessus de la tropopause?", "réponses": ["stratosphère"], "mode": "tous"},
        {"question": "À quel endroit la tropopause est-elle plus haute?", "réponses": ["équateur"], "mode": "tous"},
        {"question": "De combien de degrès la température diminue-t-elle par 1000pi?", "réponses": ["2", "deux"], "mode": "au_moins_un"},
        {"question": "Quelle est la définitions de la pression atmosphérique?", "réponses": ["poids", "colonne", "air"], "mode": "tous"},
        {"question": "Comment se nomme l'effet du manque d'oxigène du à l'atitude?", "réponses": ["hypoxie"], "mode": "tous"},
        {"question": "Quelle est la pression de référence en Hg?", "réponses": ["29", "92"], "mode": "tous"},
        {"question": "Quelle est la pression de référence en kPa? (1 chiffre après la ,)", "réponses": ["101", "3"], "mode": "tous"},
        {"question": "Quelle est la température de référence en C?", "réponses": ["15"], "mode": "tous"},
        {"question": "De combien la pession diminue-t-elle par 1000pi? (en Hg)", "réponses": ["1", "pouce"], "mode": "au_moins_un"},
        {"question": "De combien la pession diminue-t-elle par 30pi? (en mmbar)", "réponses": ["1"], "mode": "tous"},
        {"question": "Comment se nomme l'altitude entre le point de référence sur un aérodrome et le niveau moyen de la mer?", "réponses": ["élévation", "aérodrome"], "mode": "tous"},
        {"question": "Quel est l'accronyme de l'altitude au-dessus de l'aérodrome?", "réponses": ["aae"], "mode": "tous"},
        {"question": "Quel est l'accronyme de la distance verticale exacte entre l'avion et le sol ou la mer?", "réponses": ["hauteur"], "mode": "tous"},
        {"question": "Avec quel instrument la hauteur est-elle mesurer?", "réponses": ["radioaltimètre"], "mode": "tous"},
        {"question": "Que veut dire ASL?", "réponses": ["altitude", "niveau", "mer"], "mode": "tous"},
        {"question": "Que veut dire AGL?", "réponses": ["altitude", "niveau", "sol"], "mode": "tous"},
        {"question": "Quel est l'acronyme de niveau de vol?", "réponses": ["fl"], "mode": "tous"},
        {"question": "Quel est l'acronyme de calage altimétrique?", "réponses": ["qnh"], "mode": "tous"},
        {"question": "Quel est l'acronyme de la pression standard?", "réponses": ["qne"], "mode": "tous"},
        {"question": "Quel est l'acronyme de la pression pour une hauteur 0?", "réponses": ["qfe"], "mode": "tous"},
        {"question": "Comment se nomme l'altitude lue sur l'altimètre à la pression locale?", "réponses": ["indiqué", "indiquée"], "mode": "au_moins_un"},
        {"question": "Comment se nomme l'altitude au-dessus du niveau de la mer?", "réponses": ["vrai", "vraie"], "mode": "au_moins_un"},
        {"question": "Comment se nomme l'altitude indiquée quand l'altimètre affiche le QNE?", "réponses": ["pression"], "mode": "tous"},
        {"question": "Comment se nomme l'altitude pression corrigée pour la température?", "réponses": ["densité"], "mode": "tous"},
        {"question": "Quel est la masse volumique standard en kg/m3?", "réponses": ["1", "225"], "mode": "tous"},
        {"question": "Quel chiffre, arondit à l'unité, faut-il additionner au C pour former des K?", "réponses": ["273"], "mode": "tous"},
        {"question": "À parir de quel vitesse prenons-nous en compte la compressibilité? (en kts)", "réponses": ["300"], "mode": "tous"},
        {"question": "Avec quel appareil mesurons-nous la vitesse?", "réponses": ["anémomètre"], "mode": "tous"},
        {"question": "Quel vitesse est plus important : a)la vitesse par rapport au sol ou b)la vitesse par rapport à l'air", "réponses": ["b"], "mode": "tous"},
        {"question": "La vitesse par rapport à l'air est-elle l'IAS (indiquée) ou le TAS (vraie)?", "réponses": ["tas"], "mode": "tous"},
        {"question": "Avec quel appareil mesurons-nous la vitesse?", "réponses": ["anémomètre"], "mode": "tous"},
        {"question": "Quel est la vitesse affiché à l'anémomètre? (abréviation)", "réponses": ["ias"], "mode": "tous"},
        {"question": "Quel est la vitesse corrigée pour les erreurs de position et d'instrument? (abréviation)", "réponses": ["cas"], "mode": "tous"},
        {"question": "Quel est la vitesse corrigée pour les effets de la compressibilité à l'altitude donnée? (abréviation)", "réponses": ["eas"], "mode": "tous"},
        {"question": "Quel est le coefficient pour trouver la vitesse du son à une altitude donnée (a) en m/s?", "réponses": ["20", "1"], "mode": "tous"},
        {"question": "Quel est le coefficient pour trouver la vitesse du son à une altitude donnée (a) en kts?", "réponses": ["38", "94"], "mode": "tous"},
        {"question": "Comment se nomme la région à l'avant de l'aéronef qui fait l'objet d'un changement brusque de pression et de densité et qui se déplace comme un front d'onde à une vitesse égale ou supérieure à celle du son?", "réponses": ["onde", "choc"], "mode": "tous"},
        {"question": "Comment se nomme les vitesses où tous les écoulement sont subsoniques?", "réponses": ["subsonique", "subsoniques"], "mode": "au_moins_un"},
        {"question": "Comment se nomme les vitesses où les écoulement sont subsoniques, mais où il y a des écoulements supersoniques?", "réponses": ["transsonique", "transsoniques"], "mode": "au_moins_un"},
        {"question": "Comment se nomme les vitesses où tous les écoulement sont supersoniques?", "réponses": ["supersonique", "supersoniques"], "mode": "au_moins_un"},
        {"question": "Comment se nomme les vitesses où supérieur à mach 5?", "réponses": ["hypersonique", "hypersoniques"], "mode": "au_moins_un"},
        {"question": "Comment se nomme le concept qui s'opposent au glissement des couches fluides les unes sur les autres?", "réponses": ["viscosité"], "mode": "tous"},
        {"question": "Qu'est-ce que le nombre de Reynolds?", "réponses": ["nombre", "sans", "dimension", "rapport", "forces", "pression", "dynamique", "viscosité", "écoulement"], "mode": "tous"},
        
        #Air en mouvement
        
        {"question": "Quels sont les deux types de soufflerie? (veine ___ et veine ____)", "réponses": ["guidée", "libre"], "mode": "tous"},
        {"question": "Quels sont les deux critères qui doivent être identique entre les tests en soufflerie et les tests en vol?", "réponses": ["nombre", "mach", "reynolds"], "mode": "tous"},
        {"question": "Quels sont d'autres méthodes pour faire des tests? (réponses au singulier)", "réponses": ["tunnel", "eau", "sous", "voilure", "crash", "pilote", "essai"], "mode": "tous"},
        {"question": "Quels sont d'autres méthodes pour faire des tests? (réponses au singulier)", "réponses": ["tunnel", "eau", "sous", "voilure", "crash", "pilote", "essai"], "mode": "tous"},
        {"question": "Est-ce que la nature aime le vide? (v = vraie et f= faux)", "réponses": ["f"], "mode": "tous"},
        {"question": "Quels sont les quatres critères que l'on pose lorsqu'on étudie un fluide?", "réponses": ["conservation", "masse", "incompressible", "vitesse", "mach", "0", "5", "écoulement", "permanent"], "mode": "tous"},
        {"question": "Comment se nomme l'angle entre entre le vent relatif et la corde de l'aile?", "réponses": ["angle", "attaque"], "mode": "tous"},
        {"question": "Quel est la troisième loi de newton, qui nous aide à avoir de la portance?", "réponses": ["action", "réaction"], "mode": "tous"},
        {"question": "Comment se nomme l'effet où un flux de fluide en mouvement en contact avec une surface courbe aura tendance à suivre la courbure de la surface plutôt que de continuer à se déplacer en ligne droite?", "réponses": ["coanda"], "mode": "tous"},
        {"question": "Comment se nomme le point appartenant à un objet, submergé dans un écoulement, où se termine une ligne de courant?", "réponses": ["point", "arrêt"], "mode": "tous"},
        {"question": "Qu'est-ce que le tube pitot mesure?", "réponses": ["pression", "totale"], "mode": "tous"},
        {"question": "Qu'est-ce que la prise de pression statique mesure?", "réponses": ["pression", "statique"], "mode": "tous"},

        #Portance et trainée

        {"question": "Quel est la variable qui représente le coefficient de portance?", "réponses": ["cz"], "mode": "tous"},
        {"question": "Quel est la variable qui représente le coefficient de trainée?", "réponses": ["cx"], "mode": "tous"},
        {"question": "Quel est la définition de l'angle d'incidence?", "réponses": ["angle","entre","corde","aile","axe","longitudinal"], "mode": "tous"},
        {"question": "Quel est la définition du centre de poussée?", "réponses": ["point","application","résultante","forces","aérodynamique"], "mode": "tous"},
        {"question": "Quels sont les forces qui composent la résultante aérodynamique?", "réponses": ["surpression", "intrados", "dépression", "extrados", "frottement"], "mode": "tous"},
        {"question": "Quel est la composante de la résultante aérodynamique perpendiculaire à la direction de l'écoulement?", "réponses": ["portance"], "mode": "tous"},
        {"question": "Le centre de poussé, avance-t-il ou recule-t-il avec l'augmentationde l'angle d'attaque?", "réponses": ["avance"], "mode": "tous"},
        {"question": "Qu'arrive-t-il avec le profil si le centre de poussé avance trop (l'angle d'attaque est trop haut)?", "réponses": ["décrochage"], "mode": "tous"},
        {"question": "Quel est la composante de la résultante aérodynamique parallèle à la direction de l'écoulement?", "réponses": ["trainée"], "mode": "tous"},
        {"question": "Quels sont les éléments responsable de la trainée?", "réponses": ["viscosité", "couche", "limite", "design", "général"], "mode": "tous"},
        {"question": "Quel est la définitions de la couche limite?", "réponses": ["couche", "fluide", "vitesse", "inférieure", "égale", "99", "vitesse", "écoulement"], "mode": "tous"},
        {"question": "Quels sont les deux régimes de la couche limite?", "réponses": ["laminaire", "turbulent"], "mode": "tous"},
        {"question": "Quels sont les trois trainée qui composent la trainée totale?", "réponses": ["induite", "parasite", "onde"], "mode": "tous"},
        {"question": "Qu'est-ce que la trainée induite?", "réponses": ["force", "résistance", "avancement", "portance"], "mode": "tous"},
        {"question": "Qu'est-ce que la trainée d'onde?", "réponses": ["vitesse", "écoulement", "variation", "densité", "fluide"], "mode": "tous"},
        {"question": "Qu'est-ce que la trainée parasite?", "réponses": ["forme", "avion", "interférence", "frottement", "air"], "mode": "tous"},
        {"question": "Quels sont les trois trainée qui composent la trainée parasite?", "réponses": ["forme", "frottement", "interférence"], "mode": "tous"},
        {"question": "Quels sont les deux types trainées les plus importante? (qui créer le plus de trainée)", "réponses": ["frottement", "induite"], "mode": "tous"},
        {"question": "Quel est la définition de la finesse?", "réponses": ["rapport", "coefficients", "portance", "traînée", "aérodyne", "mesurant", "aptitude", "planer", "induite"], "mode": "tous"},
        {"question": "Quel est la définition des polaires?", "réponses": ["courbes", "déterminer", "caractéristiques", "profil"], "mode": "tous"},



    ]

    if st.session_state.index < len(liste_question):
        q = liste_question[st.session_state.index]
        st.subheader(f"Question {st.session_state.index + 1}")
        st.write(q["question"])
        réponse = st.text_input("Votre réponse", key=f"réponse_{st.session_state.index}")

        if st.button("Soumettre"):
            mots_utilisateur = [nettoyer_mot(m) for m in réponse.strip().lower().split()]
            mots_clés = [mot.lower() for mot in q["réponses"]]
            mode = q.get("mode", "au_moins_un")

            bonne = all(mot in mots_utilisateur for mot in mots_clés) if mode == "tous" else any(mot in mots_utilisateur for mot in mots_clés)

            if bonne:
                st.session_state.feedback = "✅ Bonne réponse !"
                st.session_state.correction = ""
                st.session_state.score += 1
            else:
                st.session_state.feedback = "❌ Mauvaise réponse."
                st.session_state.correction = f"✔️ Correction : {', '.join(q['réponses'])}"

        st.markdown(f"**{st.session_state.feedback}**")
        if st.session_state.correction:
            st.markdown(f"{st.session_state.correction}")

        if st.session_state.feedback:
            if st.button("Question suivante"):
                st.session_state.index += 1
                st.session_state.feedback = ""
                st.session_state.correction = ""
    else:
        st.success(f"🎯 Score final : {st.session_state.score} / {len(liste_question)}")
        if st.button("Rejouer le quiz"):
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.feedback = ""
            st.session_state.correction = ""

# ------------------ PAGE ISA ------------------

def générer_question_isa():
    type_q = random.randint(1, 3)
    st.session_state.type_question = type_q

    if type_q == 1:
        ISA_altitude = -1
        while ISA_altitude < 0:
            ISA_température = random.randint(-90, 30)
            ISA_ISA = random.randint(-20, 20)
            dif_temp = (ISA_ISA - ISA_température) * -1
            ISA_altitude = (dif_temp - 15) / -2 * 1000
        st.session_state.données = {
            "ISA_ISA": ISA_ISA,
            "ISA_température": ISA_température,
            "réponse_correcte": round(ISA_altitude)
        }

    elif type_q == 2:
        ISA_altitude = random.randrange(0, 50001, 500)
        ISA_ISA = random.randint(-20, 20)
        ISA_théorique = 15 - 2 * (ISA_altitude / 1000)
        ISA_température = ISA_ISA + ISA_théorique
        st.session_state.données = {
            "ISA_altitude": ISA_altitude,
            "ISA_ISA": ISA_ISA,
            "réponse_correcte": round(ISA_température)
        }

    elif type_q == 3:
        ISA_altitude = random.randrange(0, 50001, 500)
        ISA_température = random.randint(-90, 30)
        ISA_théorique = 15 - ISA_altitude / 1000 * 2
        ISA_ISA = ISA_température - ISA_théorique
        st.session_state.données = {
            "ISA_altitude": ISA_altitude,
            "ISA_température": ISA_température,
            "réponse_correcte": round(ISA_ISA)
        }

if st.session_state.page == "isa":
    st.title("🌡️ Problèmes ISA")

    if "données" not in st.session_state or not st.session_state.données:
        générer_question_isa()

    if st.session_state.étape == "question":
        type_q = st.session_state.type_question
        données = st.session_state.données

        if type_q == 1:
            st.write(f"ISA : **{données['ISA_ISA']}**, Température : **{données['ISA_température']}°C**")
            st.write("À quelle altitude volez-vous ?")

        elif type_q == 2:
            st.write(f"Altitude : **{données['ISA_altitude']} pi**, ISA : **{données['ISA_ISA']}**")
            st.write("Quelle est la température extérieure ?")

        elif type_q == 3:
            st.write(f"Altitude : **{données['ISA_altitude']} pi**, Température : **{données['ISA_température']}°C**")
            st.write("Quel est l'ISA ?")

        réponse = st.text_input("Votre réponse :")
        if st.button("Valider ma réponse"):
            valeur = nettoyage_ISA(réponse)
            st.session_state.réponse_utilisateur = valeur
            st.session_state.étape = "correction"

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
            générer_question_isa()

# ------------------ PAGE AUTRE ------------------

if st.session_state.page == "autre":
    st.title("🧮 Autres types de problèmes")
    st.info("Cette section sera développée prochainement. Revenez bientôt !")