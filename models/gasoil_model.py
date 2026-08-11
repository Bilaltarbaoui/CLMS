import sqlite3


class GasoilModel:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/clms.db"
        )

        self.cursor = self.connection.cursor()

    # =====================================================
    # CREER TABLE GASOIL
    # =====================================================

    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS gasoil (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                vehicule TEXT NOT NULL,

                date_operation TEXT NOT NULL,

                heure_operation TEXT NOT NULL,

                kilometrage REAL,

                quantite REAL NOT NULL,

                observation TEXT

            )
        """)

        self.connection.commit()

    # =====================================================
    # AJOUTER OPERATION GASOIL
    # =====================================================

    def ajouter(
        self,
        vehicule,
        date_operation,
        heure_operation,
        kilometrage,
        quantite,
        observation
    ):

        self.cursor.execute("""
            INSERT INTO gasoil (

                vehicule,
                date_operation,
                heure_operation,
                kilometrage,
                quantite,
                observation

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            vehicule,
            date_operation,
            heure_operation,
            kilometrage,
            quantite,
            observation

        ))

        self.connection.commit()

    # =====================================================
    # AFFICHER TOUTES LES OPERATIONS GASOIL
    # =====================================================

    def get_all(self):

        self.cursor.execute("""
            SELECT

                id,
                vehicule,
                date_operation,
                heure_operation,
                kilometrage,
                quantite,
                observation

            FROM gasoil

            ORDER BY

                date_operation DESC,
                heure_operation DESC

        """)

        return self.cursor.fetchall()

    # =====================================================
    # STATISTIQUES GASOIL PAR VEHICULE
    # =====================================================

    def get_statistics_by_vehicle(self):

        self.cursor.execute("""
            SELECT

                vehicule,

                COUNT(*) AS nombre_operations,

                SUM(quantite) AS total_gasoil

            FROM gasoil

            GROUP BY vehicule

            ORDER BY total_gasoil DESC

        """)

        return self.cursor.fetchall()

    # =====================================================
    # MODIFIER OPERATION GASOIL
    # =====================================================

    def modifier(
        self,
        id_operation,
        vehicule,
        date_operation,
        heure_operation,
        kilometrage,
        quantite,
        observation
    ):

        self.cursor.execute("""
            UPDATE gasoil

            SET

                vehicule = ?,

                date_operation = ?,

                heure_operation = ?,

                kilometrage = ?,

                quantite = ?,

                observation = ?

            WHERE id = ?

        """, (

            vehicule,
            date_operation,
            heure_operation,
            kilometrage,
            quantite,
            observation,
            id_operation

        ))

        self.connection.commit()

    # =====================================================
    # SUPPRIMER OPERATION GASOIL
    # =====================================================

    def supprimer(self, id_operation):

        self.cursor.execute("""
            DELETE FROM gasoil

            WHERE id = ?

        """, (
            id_operation,
        ))

        self.connection.commit()

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        self.connection.close()