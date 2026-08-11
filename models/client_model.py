import sqlite3


class ClientModel:

    def __init__(self):

        self.connection = sqlite3.connect("database/clms.db")
        self.cursor = self.connection.cursor()

    # ==========================
    # Ajouter
    # ==========================

    def ajouter_client(self, nom, telephone, adresse, email, ville):

        self.cursor.execute("""
            INSERT INTO clients
            (
                nom,
                telephone,
                adresse,
                email,
                ville,
                date_creation
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            nom,
            telephone,
            adresse,
            email,
            ville
        ))

        self.connection.commit()

    # ==========================
    # Afficher
    # ==========================

    def get_all_clients(self):

        self.cursor.execute("""
            SELECT *
            FROM clients
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==========================
    # Modifier
    # ==========================

    def modifier_client(
        self,
        id_client,
        nom,
        telephone,
        adresse,
        email,
        ville
    ):

        self.cursor.execute("""
            UPDATE clients
            SET
                nom = ?,
                telephone = ?,
                adresse = ?,
                email = ?,
                ville = ?
            WHERE id = ?
        """, (
            nom,
            telephone,
            adresse,
            email,
            ville,
            id_client
        ))

        self.connection.commit()

    # ==========================
    # Supprimer
    # ==========================

    def supprimer_client(self, id_client):

        self.cursor.execute("""
            DELETE FROM clients
            WHERE id = ?
        """, (
            id_client,
        ))

        self.connection.commit()

    # ==========================
    # Rechercher
    # ==========================

    def rechercher_client(self, mot):

        self.cursor.execute("""
            SELECT *
            FROM clients
            WHERE
                nom LIKE ?
                OR telephone LIKE ?
                OR email LIKE ?
                OR ville LIKE ?
            ORDER BY id DESC
        """, (
            f"%{mot}%",
            f"%{mot}%",
            f"%{mot}%",
            f"%{mot}%"
        ))

        return self.cursor.fetchall()