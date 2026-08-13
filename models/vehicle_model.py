import sqlite3

from database.database import Database


class VehicleModel:

    def __init__(self):

        self.connection = Database.get_safe_connection("database/clms.db")
        self.cursor = self.connection.cursor()

        self.create_table()

    # =====================================================
    # CREER TABLE VEHICULES
    # =====================================================

    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                matricule TEXT NOT NULL UNIQUE,

                type TEXT,

                marque TEXT,

                modele TEXT,

                kilometrage REAL DEFAULT 0,

                etat TEXT,

                observation TEXT

            )
        """)

        self.connection.commit()

    # =====================================================
    # AJOUTER VEHICULE
    # =====================================================

    def ajouter(
        self,
        matricule,
        type_vehicule,
        marque,
        modele,
        kilometrage,
        etat,
        observation
    ):

        self.cursor.execute("""
            INSERT INTO vehicles (
                matricule,
                type,
                marque,
                modele,
                kilometrage,
                etat,
                observation
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            matricule,
            type_vehicule,
            marque,
            modele,
            kilometrage,
            etat,
            observation
        ))

        self.connection.commit()

    # =====================================================
    # AFFICHER VEHICULES
    # =====================================================

    def get_all(self):

        self.cursor.execute("""
            SELECT
                id,
                matricule,
                type,
                marque,
                modele,
                kilometrage,
                etat,
                observation

            FROM vehicles

            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # =====================================================
    # MODIFIER VEHICULE
    # =====================================================

    def modifier(
        self,
        id_vehicule,
        matricule,
        type_vehicule,
        marque,
        modele,
        kilometrage,
        etat,
        observation
    ):

        self.cursor.execute("""
            UPDATE vehicles

            SET
                matricule = ?,
                type = ?,
                marque = ?,
                modele = ?,
                kilometrage = ?,
                etat = ?,
                observation = ?

            WHERE id = ?
        """, (
            matricule,
            type_vehicule,
            marque,
            modele,
            kilometrage,
            etat,
            observation,
            id_vehicule
        ))

        self.connection.commit()

    # =====================================================
    # SUPPRIMER VEHICULE
    # =====================================================

    def supprimer(self, id_vehicule):

        self.cursor.execute("""
            DELETE FROM vehicles

            WHERE id = ?
        """, (
            id_vehicule,
        ))

        self.connection.commit()

    # =====================================================
    # STATISTIQUES
    # =====================================================

    def get_statistics(self):

        # Total véhicules
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles
        """)

        total = self.cursor.fetchone()[0]

        # Véhicules actifs
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles
            WHERE LOWER(etat) = 'actif'
        """)

        actifs = self.cursor.fetchone()[0]

        # Véhicules en maintenance
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles
            WHERE LOWER(etat) = 'maintenance'
        """)

        maintenance = self.cursor.fetchone()[0]

        # Véhicules hors service
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles
            WHERE LOWER(etat) = 'hors service'
        """)

        hors_service = self.cursor.fetchone()[0]

        # Kilométrage total
        self.cursor.execute("""
            SELECT COALESCE(SUM(kilometrage), 0)
            FROM vehicles
        """)

        kilometrage_total = self.cursor.fetchone()[0]

        return {
            "total": total,
            "actifs": actifs,
            "maintenance": maintenance,
            "hors_service": hors_service,
            "kilometrage_total": kilometrage_total
        }

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None