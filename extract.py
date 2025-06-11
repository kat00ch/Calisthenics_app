# main.py - Chargement des fichiers JSON sous forme de classes

import json
import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Exercice:
    id: str
    nom: str
    description: str
    points_par_repetition: int
    points_par_duree_seconde: int
    niveau_minimum: int
    categorie: str
    special: bool

@dataclass
class Malus:
    id: str
    nom: str
    description: str
    points_perdus: int
    conditions_declenchement: str

@dataclass
class Objectif:
    id: str
    nom: str
    description: str
    points_totaux_requis: int
    exercices_associes: List[str]
    bonus_recompense: str

@dataclass
class Session:
    id: str
    date: str
    utilisateur_id: str
    exercices_realises: List[dict]
    malus: List[str]
    points_totaux_gagnes: int
    points_totaux_perdus: int

@dataclass
class Utilisateur:
    id: str
    nom: str
    date_debut: str
    points_totaux: int
    niveau: int
    progression_objectifs: dict
    historique_sessions: List[str]

@dataclass
class ChallengeCondition:
    exercice_id: Optional[str]
    objectif_id: Optional[str]
    type: str
    valeur_cible: int

@dataclass
class Challenge:
    challenge_id: str
    titre: str
    type: str
    date_debut: str
    date_fin: str
    conditions: List[ChallengeCondition]
    recompense: dict

@dataclass
class Niveau:
    niveau: int
    points_requis: int
    exercices_debloques: List[str]
    exercices_speciaux_debloques: List[str]

@dataclass
class PositionnementQuestion:
    question: str
    type: str
    exercice_id: Optional[str]
    seuils: List[dict]

@dataclass
class TestPositionnement:
    test_id: str
    questions: List[PositionnementQuestion]


def charger_json(path: str):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read().strip()
        if not contenu:
            return []
        try:
            data = json.loads(contenu)
            if isinstance(data, dict):
                return [data]
            return data
        except:
            result = []
            for line in contenu.splitlines():
                line = line.strip()
                if line:
                    result.append(json.loads(line))
            return result

def extraire_infos():
    exercices_data = charger_json("data/exercices.json")
    exercices = [Exercice(**e) for e in exercices_data]

    malus_data = charger_json("data/malus.json")
    malus = [Malus(**m) for m in malus_data]

    objectifs_data = charger_json("data/objectifs.json")
    objectifs = [Objectif(**o) for o in objectifs_data]

    sessions_data = charger_json("data/sessions.json")
    sessions = [Session(**s) for s in sessions_data]

    utilisateurs_data = charger_json("data/utilisateurs.json")
    utilisateurs = [Utilisateur(**u) for u in utilisateurs_data]

    challenges_data = charger_json("data/challenges.json")
    challenges = [Challenge(**c) for c in challenges_data]

    niveaux_data = charger_json("data/niveaux.json")
    niveaux = [Niveau(**n) for n in niveaux_data]

    positionnement_data = charger_json("data/positionnement.json")
    positionnement = [TestPositionnement(**t) for t in positionnement_data]

    return {
        "exercices": exercices,
        "malus": malus,
        "objectifs": objectifs,
        "sessions": sessions,
        "utilisateurs": utilisateurs,
        "challenges": challenges,
        "niveaux": niveaux,
        "positionnement": positionnement
    }

def creer_joueur(nom: str, id: str, date_debut: str):
    utilisateur = Utilisateur(
        id=id,
        nom=nom,
        date_debut=date_debut,
        points_totaux=0,
        niveau=1,
        progression_objectifs={},
        historique_sessions=[]
    )
    return utilisateur