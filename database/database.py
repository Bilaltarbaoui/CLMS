import sqlite3
import os
import hashlib


class Database:

    def __init__(self):

        # =====================================================
        # CHEMIN DE LA BASE DE DONNÉES
        # =====================================================

        self.database_path = "database/clms.db"

        # Créer le dossier database s'il n'existe pas
        os.makedirs("database", exist_ok=True)

        # Connexion SQLite
        self.connection = sqlite3.connect(
            self.database_path
        )

        # Curseur
        self.cursor = self.connection.cursor()

        print("DATABASE = OK")

        # Créer les tables
        self.create_tables()

        # Créer le compte administrateur par défaut
        self.create_default_admin()

    # =====================================================
    # CREATION DES TABLES
    # =====================================================

    def create_tables(self):

        print(">>> CREATION DES TABLES")

        # =================================================
        # TABLE CLIENTS
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nom TEXT NOT NULL,

                telephone TEXT,

                adresse TEXT,

                email TEXT,

                ville TEXT,

                date_creation TEXT

            )
        """)

        # =================================================
        # TABLE PRODUCTS
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                reference TEXT,

                nom TEXT NOT NULL,

                categorie TEXT,

                marque TEXT,

                unite TEXT,

                stock INTEGER DEFAULT 0,

                stock_min INTEGER DEFAULT 0,

                numero_lot TEXT,

                dlc TEXT,

                fournisseur TEXT,

                description TEXT,

                date_creation TEXT,

                date_reception TEXT,

                date_livraison TEXT

            )
        """)

        # =================================================
        # TABLE STOCK ENTRIES
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_entries(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_id INTEGER NOT NULL,

                quantite INTEGER NOT NULL,

                fournisseur TEXT,

                numero_bon TEXT,

                commentaire TEXT,

                date_reception TEXT,

                FOREIGN KEY(product_id)
                REFERENCES products(id)

            )
        """)

        # =================================================
        # TABLE STOCK OUTPUTS
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_outputs(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_id INTEGER NOT NULL,

                quantite INTEGER NOT NULL,

                client TEXT,

                numero_bon TEXT,

                commentaire TEXT,

                date_sortie TEXT,

                FOREIGN KEY(product_id)
                REFERENCES products(id)

            )
        """)

        # =================================================
        # TABLE VEHICLES
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                immatriculation TEXT NOT NULL UNIQUE,

                marque TEXT,

                modele TEXT,

                type TEXT,

                kilometrage INTEGER DEFAULT 0,

                chauffeur TEXT,

                statut TEXT DEFAULT 'Disponible',

                date_creation TEXT

            )
        """)

        # =================================================
        # TABLE GASOIL
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS gasoil(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                vehicule TEXT NOT NULL,

                date_operation TEXT,

                heure_operation TEXT,

                kilometrage INTEGER DEFAULT 0,

                quantite REAL DEFAULT 0,

                observation TEXT

            )
        """)

        # =================================================
        # TABLE USERS
        # =================================================

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'user',

                nom_complet TEXT,

                actif INTEGER NOT NULL DEFAULT 1,

                date_creation TEXT

            )
        """)
            # =================================================
    # TABLE HISTORIQUE
    # =================================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS historique(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            utilisateur TEXT,

            type_operation TEXT NOT NULL,

            module TEXT NOT NULL,

            description TEXT,

            date_operation TEXT NOT NULL

        )
    """)

        # =================================================
        # VALIDATION
        # =================================================

        self.connection.commit()

        print("TABLES = OK")

    # =====================================================
    # FERMER LA BASE DE DONNÉES
    # =====================================================

    def close(self):

        if self.connection:

            self.connection.close()

            print("DATABASE CLOSED")

    def hash_password(self, password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    def create_default_admin(self):

        self.cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            ("admin",)
        )

        admin = self.cursor.fetchone()

        if admin is not None:
            return

        password_hash = self.hash_password(
            "Admin123"
        )

        self.cursor.execute("""
        INSERT INTO users(
            username,
            password_hash,
            role
        )
        VALUES (?, ?, ?)
    """, (
            "admin",
            password_hash,
            "admin"
        ))

        self.connection.commit()

        print("DEFAULT ADMIN = CREATED")

    def ajouter_historique(
        self,
        utilisateur,
        type_operation,
        module,
        description,
        commit=True
    ):

        from datetime import datetime

        date_operation = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute("""
            INSERT INTO historique(
                utilisateur,
                type_operation,
                module,
                description,
                date_operation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            utilisateur,
            type_operation,
            module,
            description,
            date_operation
        ))

        if commit:
            self.connection.commit()

        print("HISTORIQUE = AJOUTÉ")

        return True