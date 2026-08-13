import sqlite3
import os
import hashlib
import hmac
import binascii
import threading
import time


class Database:

    # =====================================================
    # CLASS-LEVEL HELPER: SAFE CONNECTION FACTORY
    # =====================================================
    @staticmethod
    def get_safe_connection(db_path: str = "database/clms.db"):
        """
        Create a SQLite connection with proper PRAGMA settings.
        MUST use this for all connections to ensure FK enforcement.
        
        Usage:
            conn = Database.get_safe_connection()
            cursor = conn.cursor()
            ...
            conn.close()
        """
        conn = sqlite3.connect(db_path, timeout=30)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
        except Exception:
            pass
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
        except Exception:
            pass
        try:
            conn.execute("PRAGMA busy_timeout = 30000;")
        except Exception:
            pass
        return conn

    def __init__(self):

        # =====================================================
        # CHEMIN DE LA BASE DE DONNÉES
        # =====================================================

        self.database_path = "database/clms.db"

        # Créer le dossier database s'il n'existe pas
        os.makedirs("database", exist_ok=True)

        # Connexion SQLite (timeout réduit les échecs immédiats en cas de contention)
        # On active WAL et foreign_keys pour diminuer les verrous et respecter les FK
        self.connection = sqlite3.connect(
            self.database_path,
            timeout=30
        )

        # Curseur
        self.cursor = self.connection.cursor()
        # Create PRAGMAs and schema under write lock to avoid concurrent DDL/PRAGMA writes
        try:
            with Database._write_lock:
                # PRAGMA: journal_mode=WAL pour réduire la contention lecture/écriture
                try:
                    self.cursor.execute("PRAGMA journal_mode=WAL;")
                except Exception:
                    pass

                # Activer les foreign keys
                try:
                    self.cursor.execute("PRAGMA foreign_keys = ON;")
                except Exception:
                    pass

                # Set a sensible busy timeout to reduce transient locked errors
                try:
                    self.cursor.execute("PRAGMA busy_timeout = 30000;")
                except Exception:
                    pass

                print("DATABASE = OK")

                # Créer les tables and default admin under a process-wide write lock
                try:
                    self.create_tables()
                except Exception:
                    pass
                try:
                    self.create_default_admin()
                except Exception:
                    pass
        except Exception:
            # Fall back: best-effort without lock
            try:
                self.cursor.execute("PRAGMA journal_mode=WAL;")
            except Exception:
                pass
            try:
                self.cursor.execute("PRAGMA foreign_keys = ON;")
            except Exception:
                pass
            try:
                print("DATABASE = OK")
                self.create_tables()
            except Exception:
                pass
            try:
                self.create_default_admin()
            except Exception:
                pass

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
                password_salt TEXT,

                role TEXT NOT NULL DEFAULT 'user',

                nom_complet TEXT,

                actif INTEGER NOT NULL DEFAULT 1,

                date_creation TEXT

            )
        """)

        # Ensure legacy schemas gain the password_salt column if missing
        try:
            self.cursor.execute("PRAGMA table_info(users)")
            cols = [row[1] for row in self.cursor.fetchall()]
            if 'password_salt' not in cols:
                self.cursor.execute("ALTER TABLE users ADD COLUMN password_salt TEXT")
        except Exception:
            pass

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

    # =====================================================
    # COMMIT WITH RETRY (reduce transient SQLITE_LOCKED)
    # =====================================================

    # Use a reentrant lock because some write operations already hold the lock
    # while calling Database.commit_with_retry(). A regular Lock would deadlock.
    _write_lock = threading.RLock()

    def commit_with_retry(self, retries: int = 5, backoff: float = 0.05):

        attempt = 0

        while True:

            try:

                # Serialize commits within this process to reduce contention
                with Database._write_lock:
                    self.connection.commit()

                return True

            except sqlite3.OperationalError as e:

                if attempt >= retries:
                    raise

                time.sleep(backoff * (2 ** attempt))

                attempt += 1

    # =====================================================
    # PASSWORD HASHING (PBKDF2-based, per-user salt)
    # =====================================================

    def generate_salt(self, length: int = 16) -> str:

        return binascii.hexlify(os.urandom(length)).decode()

    def hash_password_pbkdf2(self, password: str, salt: str, iterations: int = 200000) -> str:

        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)

        return binascii.hexlify(dk).decode()

    def make_password_hash(self, password: str, iterations: int = 200000) -> (str, str):

        salt = self.generate_salt()

        h = self.hash_password_pbkdf2(password, salt, iterations)

        # Stored format: pbkdf2_sha256$<iterations>$<salt>$<hex>
        return f"pbkdf2_sha256${iterations}${salt}${h}", salt

    def verify_and_migrate_password(self, username: str, password: str) -> bool:

        # Return True if password correct. If legacy SHA-256 detected, rehash and update.
        # Also fetch `actif` to prevent authentication for inactive users
        self.cursor.execute("SELECT password_hash, actif FROM users WHERE username = ?", (username,))

        row = self.cursor.fetchone()

        if not row:
            return False

        stored = row[0] or ''
        try:
            actif = int(row[1])
        except Exception:
            actif = 1

        if actif == 0:
            # user explicitly inactive — do not authenticate
            return False

        if stored.startswith('pbkdf2_sha256$'):
            try:
                parts = stored.split('$')
                iterations = int(parts[1])
                salt = parts[2]
                hexhash = parts[3]
                candidate = self.hash_password_pbkdf2(password, salt, iterations)
                return hmac.compare_digest(candidate, hexhash)
            except Exception:
                return False

        # Legacy SHA-256 (hex only)
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()

        if hmac.compare_digest(legacy_hash, stored):

            # Migrate to pbkdf2
            newhash, salt = self.make_password_hash(password)
            try:
                self.cursor.execute("UPDATE users SET password_hash = ?, password_salt = ? WHERE username = ?", (newhash, salt, username))
                self.commit_with_retry()
            except Exception:
                pass

            return True

        return False

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

        # create an admin user with inactive flag and a PBKDF2-hashed password
        newhash, salt = self.make_password_hash("Admin123")

        self.cursor.execute("""
        INSERT INTO users(
            username,
            password_hash,
            password_salt,
            role,
            actif
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
            "admin",
            newhash,
            salt,
            "admin",
            0
        ))

        try:
            self.commit_with_retry()
        except Exception:
            # best-effort
            try:
                self.connection.commit()
            except Exception:
                pass

        print("DEFAULT ADMIN = CREATED (inactive)")
        print("WARNING: Default admin 'admin' created but marked inactive. Enable/rehash on first-run if needed.")

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
            try:
                self.commit_with_retry()
            except Exception:
                self.connection.commit()

        print("HISTORIQUE = AJOUTÉ")

        return True

    # =====================================================
    # USER MANAGEMENT HELPERS (no schema changes)
    # =====================================================

    def get_all_users(self):
        """Return a list of users with non-sensitive fields only.

        Each item is a dict: id, username, role, nom_complet, actif, date_creation
        """
        self.cursor.execute("SELECT id, username, role, nom_complet, actif, date_creation FROM users ORDER BY username COLLATE NOCASE")
        rows = self.cursor.fetchall()
        users = []
        for r in rows:
            users.append({
                'id': r[0],
                'username': r[1],
                'role': r[2],
                'nom_complet': r[3],
                'actif': int(r[4]) if r[4] is not None else None,
                'date_creation': r[5]
            })
        return users

    def get_user_by_id(self, user_id):
        """Return non-sensitive user info by id or None."""
        self.cursor.execute("SELECT id, username, role, nom_complet, actif, date_creation FROM users WHERE id = ?", (user_id,))
        r = self.cursor.fetchone()
        if not r:
            return None
        return {
            'id': r[0],
            'username': r[1],
            'role': r[2],
            'nom_complet': r[3],
            'actif': int(r[4]) if r[4] is not None else None,
            'date_creation': r[5]
        }

    def get_user_by_username(self, username):
        """Return non-sensitive user info by username or None."""
        self.cursor.execute("SELECT id, username, role, nom_complet, actif, date_creation FROM users WHERE username = ?", (username,))
        r = self.cursor.fetchone()
        if not r:
            return None
        return {
            'id': r[0],
            'username': r[1],
            'role': r[2],
            'nom_complet': r[3],
            'actif': int(r[4]) if r[4] is not None else None,
            'date_creation': r[5]
        }

    def username_exists(self, username) -> bool:
        self.cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone() is not None

    def create_user(self, username, password, role='magasinier', nom_complet=None, actif=1):
        """Create a new user with PBKDF2-hashed password. Returns new user id.

        Raises sqlite3.IntegrityError on duplicate username.
        """
        if not username:
            raise ValueError('username required')
        newhash, salt = self.make_password_hash(password)
        now = None
        try:
            self.cursor.execute("INSERT INTO users (username, password_hash, password_salt, role, nom_complet, actif, date_creation) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))", (username, newhash, salt, role, nom_complet, int(actif)))
            self.commit_with_retry()
            return self.cursor.lastrowid
        except Exception:
            # propagate integrity error upstream
            raise

    def update_user(self, user_id, role=None, nom_complet=None, actif=None):
        """Update non-sensitive fields for a user."""
        fields = []
        params = []
        if role is not None:
            fields.append('role = ?')
            params.append(role)
        if nom_complet is not None:
            fields.append('nom_complet = ?')
            params.append(nom_complet)
        if actif is not None:
            fields.append('actif = ?')
            params.append(int(actif))
        if not fields:
            return False
        params.append(user_id)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(sql, tuple(params))
        self.commit_with_retry()
        return True

    def set_user_active(self, user_id, actif: int):
        self.cursor.execute("UPDATE users SET actif = ? WHERE id = ?", (int(actif), user_id))
        self.commit_with_retry()
        return True

    def set_user_password(self, user_id, new_password):
        """Securely set a user's password using PBKDF2. Does not return the hash."""
        newhash, salt = self.make_password_hash(new_password)
        self.cursor.execute("UPDATE users SET password_hash = ?, password_salt = ? WHERE id = ?", (newhash, salt, user_id))
        self.commit_with_retry()
        return True