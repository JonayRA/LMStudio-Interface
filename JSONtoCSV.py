# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:03:35 2024

@author: jonay
"""
import os
import json
import pandas as pd

def aplatis_json(y, prefix=''):
    """
    Aplatisse un JSON, y compris les JSONs imbriqués.
    """
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y, prefix)
    return out

# Demander à l'utilisateur le chemin du dossier dans la console
dossier = input("Veuillez entrer le chemin du dossier contenant les fichiers JSON. Si vous aviez ouvert le fichier 'output' il doit être fermé avant de continuer. : ")

if not dossier:
    print("Aucun dossier sélectionné. Terminaison du programme.")
else:
    # Listes pour stocker les données de chaque participant
    liste_donnees = []

    # Itérer sur les fichiers dans le dossier
    for nom_fichier in os.listdir(dossier):
        print(nom_fichier)
        if nom_fichier.endswith('.json'):
            participant_id = nom_fichier.split('_')[0]  # Obtenir l'ID du participant
            type_fichier = nom_fichier.split('_')[1].split('.')[0]  # Obtenir le type de fichier

            chemin_fichier = os.path.join(dossier, nom_fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                json_donnees = json.load(fichier)

            # Rechercher s'il existe déjà un enregistrement pour ce participant
            donnees_participant = next((item for item in liste_donnees if item['IDParticipant'] == participant_id), None)

            if donnees_participant is None:
                donnees_participant = {'IDParticipant': participant_id}
                liste_donnees.append(donnees_participant)

            # Aplatir les données JSON et les ajouter à l'enregistrement du participant
            donnees_aplaties = aplatis_json(json_donnees, f'{type_fichier}_')
            for cle, valeur in donnees_aplaties.items():
                # S'assurer que les noms de champs ne se répètent pas
                cle_unique = cle
                compteur = 1
                while cle_unique in donnees_participant:
                    cle_unique = f"{cle}_{compteur}"
                    compteur += 1
                donnees_participant[cle_unique] = valeur

    # Convertir la liste de dictionnaires en DataFrame
    df = pd.DataFrame(liste_donnees)

    # Enregistrer le DataFrame dans un fichier CSV dans le même dossier
    csv_sortie = os.path.join(dossier, 'output.csv')
    df.to_csv(csv_sortie, index=False, encoding='utf-8-sig')

    print(f'Données sauvegardées dans {csv_sortie}')
