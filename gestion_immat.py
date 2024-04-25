import pandas as pd
import streamlit as st


# Définition de la classe VerificateurImmatriculation
class VerificateurImmatriculation:
    def __init__(self, df, colone_immatriculation):
        self.df = df
        self.colonne_immatriculation = colone_immatriculation

    def verifier_immatriculation(self, numero):
        # Initialiser le statut à 'OUI'
        statut = "OUI"

        # Déterminer le nombre de caractères dans l’immatriculation
        numero = str(numero)
        nb_caracteres = len(numero)

        # Si le nombre de caractères est égal à 9
        if nb_caracteres == 9:
            for position, caractere in enumerate(numero, start=1):
                if caractere.isalpha():  # Si le caractère est une lettre
                    if position not in (1, 2, 8, 9):
                        statut = "NON"
                        break
                elif caractere.isdigit():  # Si le caractère est un chiffre
                    if position not in (4, 5, 6):
                        statut = "NON"
                        break
                elif caractere == '-':  # Si le caractère est un tiret
                    if position not in (3, 7):
                        statut = "NON"
                        break

        # Si le nombre de caractères est égal à 8
        elif nb_caracteres == 8:
            nb_chiffres = sum(c.isdigit() for c in numero)
            nb_lettres = sum(c.isalpha() for c in numero)
            if nb_chiffres == 6 and nb_lettres == 2:
                for position, caractere in enumerate(numero, start=1):
                    if caractere.isalpha():
                        if position not in (5, 6):
                            statut = "NON"
                            break
                    elif caractere.isdigit():
                        if position not in (1, 2, 3, 4, 7, 8):
                            statut = "NON"
                            break
                    elif caractere == '-':
                        if position not in (2, 6):
                            statut = "NON"
                            break
            elif nb_chiffres == 5 and nb_lettres == 3:
                if numero[3] != '-':
                    statut = "NON"
            elif nb_chiffres == 3 and nb_lettres == 3:
                for position, caractere in enumerate(numero, start=1):
                    if position not in (1, 7, 8):
                        statut = "NON"
                        break
            else:
                statut = "NON"

        # Si le nombre de caractères est égal à 7
        elif nb_caracteres == 7:
            nb_chiffres = sum(c.isdigit() for c in numero)
            nb_lettres = sum(c.isalpha() for c in numero)
            if nb_chiffres == 5 and nb_lettres == 2:
                if numero[3] != '-':
                    statut = "NON"
            elif nb_chiffres == 4 and nb_lettres == 3:
                for position, caractere in enumerate(numero, start=1):
                    if position not in (3, 4, 5):
                        statut = "NON"
                        break
            else:
                statut = "NON"

        # Si le nombre de caractères est égal à 6
        elif nb_caracteres == 6:
            nb_chiffres = sum(c.isdigit() for c in numero)
            nb_lettres = sum(c.isalpha() for c in numero)
            if nb_chiffres == 4 and nb_lettres == 2:
                for position, caractere in enumerate(numero, start=1):
                    if position not in (3, 4):
                        statut = "NON"
                        break
            elif nb_chiffres == 3 and nb_lettres == 3:
                for position, caractere in enumerate(numero, start=1):
                    if position not in (1, 2, 6):
                        statut = "NON"
                        break
            elif '0' in numero[1:]:
                statut = "NON"
            else:
                statut = "NON"

        # Si le nombre de caractères est inférieur à 6 ou supérieur à 9
        elif nb_caracteres < 6 or nb_caracteres > 9:
            statut = "NON"

        return statut

    def verifier_et_ajouter_statut(self):
        # Initialiser à 'OUI' le paramètre de retour (Statut_SIV/FNI)
        self.df['Statut_SIV/FNI'] = 'OUI'

        # Appliquer la fonction à chaque élément de la colonne 'Numero_Immatriculation'
        self.df['Statut_SIV/FNI'] = self.df['Immatriculation'].apply(self.verifier_immatriculation)

        return self.df


def main():
    st.title("Vérification d'immatriculation")

    chemin_fichier = st.file_uploader("Sélectionnez un fichier Excel ou CSV", type=["xlsx", "xls", "csv"])
    premiere_ligne_non_vide = st.number_input("Numéro de la première ligne non vide :", min_value=1, value=1)

    if chemin_fichier is not None:
        extension = chemin_fichier.name.split('.')[-1]
        if extension.lower() == 'csv':
            df = pd.read_csv(chemin_fichier, skiprows=premiere_ligne_non_vide - 1)
        else:
            df = pd.read_excel(chemin_fichier, skiprows=premiere_ligne_non_vide - 1)

        colonne_immatriculation = st.selectbox("Sélectionnez la colonne à traiter :", df.columns)

        if st.button("Traiter le fichier"):
            if colonne_immatriculation == "":
                st.error("Veuillez saisir le nom de la colonne à traiter.")
            else:
                try:
                    verifier = VerificateurImmatriculation(df, colonne_immatriculation)
                    df_resultat = verifier.verifier_et_ajouter_statut()
                    st.write(df_resultat)
                    df_resultat.to_excel("resultats.xlsx")
                except Exception as e:
                    st.error(f"Une erreur s'est produite : {e}")
        

if __name__ == "__main__":
    main()
