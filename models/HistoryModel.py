import sqlite3


class HistoryModel:

    def __init__(self):

        # =====================================================
        # DATABASE
        # =====================================================

        self.connection = sqlite3.connect(
            "database/clms.db"
        )

        self.cursor = self.connection.cursor()

        print("HISTORY MODEL = OK")

    # =====================================================
    # AFFICHER HISTORIQUE COMPLET
    # =====================================================

    def get_history(self):

        self.cursor.execute("""

            SELECT

                utilisateur,

                type_operation,

                module,

                description,

                date_operation

            FROM historique

            ORDER BY date_operation DESC

        """)

        return self.cursor.fetchall()

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self, mot):

        mot = mot.strip()

        if mot == "":

            return self.get_history()

        recherche = f"%{mot}%"

        self.cursor.execute("""

            SELECT

                utilisateur,

                type_operation,

                module,

                description,

                date_operation

            FROM historique

            WHERE

                utilisateur LIKE ?

                OR type_operation LIKE ?

                OR module LIKE ?

                OR description LIKE ?

                OR date_operation LIKE ?

            ORDER BY date_operation DESC

        """, (

            recherche,
            recherche,
            recherche,
            recherche,
            recherche

        ))

        return self.cursor.fetchall()

    # =====================================================
    # FILTRE PAR TYPE D'OPERATION
    # =====================================================

    def get_history_filtre(self, type_operation):

        # =================================================
        # TOUS
        # =================================================

        if type_operation == "Tous":

            return self.get_history()

        # =================================================
        # FILTRE
        # =================================================

        self.cursor.execute("""

            SELECT

                utilisateur,

                type_operation,

                module,

                description,

                date_operation

            FROM historique

            WHERE type_operation = ?

            ORDER BY date_operation DESC

        """, (
            type_operation,
        ))

        return self.cursor.fetchall()

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        if self.connection:

            self.connection.close()

            print(
                "HISTORY DATABASE CLOSED"
            )