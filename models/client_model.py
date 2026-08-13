import sqlite3
import time
from typing import List, Tuple, Any

from database.database import Database


class ClientModel:

    DB_PATH = "database/clms.db"

    def __init__(self):
        # Keep init lightweight: do not hold a persistent connection.
        pass

    def _connect(self):
        return Database.get_safe_connection(self.DB_PATH)

    def _commit_with_retry(self, conn: sqlite3.Connection, retries: int = 5, backoff: float = 0.05):
        attempt = 0
        while True:
            try:
                conn.commit()
                return True
            except sqlite3.OperationalError as e:
                if attempt >= retries or 'locked' not in str(e).lower():
                    raise
                time.sleep(backoff * (2 ** attempt))
                attempt += 1

    # ==========================
    # Ajouter
    # ==========================

    def ajouter_client(self, nom: str, telephone: str, adresse: str, email: str, ville: str):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
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
            """, (nom, telephone, adresse, email, ville))
            self._commit_with_retry(conn)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # ==========================
    # Afficher
    # ==========================

    def get_all_clients(self) -> List[Tuple[Any, ...]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT *
                FROM clients
                ORDER BY id DESC
            """)
            return cur.fetchall()
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # ==========================
    # Modifier
    # ==========================

    def modifier_client(self, id_client: int, nom: str, telephone: str, adresse: str, email: str, ville: str):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE clients
                SET
                    nom = ?,
                    telephone = ?,
                    adresse = ?,
                    email = ?,
                    ville = ?
                WHERE id = ?
            """, (nom, telephone, adresse, email, ville, id_client))
            self._commit_with_retry(conn)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # ==========================
    # Supprimer
    # ==========================

    def supprimer_client(self, id_client: int):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM clients
                WHERE id = ?
            """, (id_client,))
            self._commit_with_retry(conn)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # ==========================
    # Rechercher
    # ==========================

    def rechercher_client(self, mot: str) -> List[Tuple[Any, ...]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT *
                FROM clients
                WHERE
                    nom LIKE ?
                    OR telephone LIKE ?
                    OR email LIKE ?
                    OR ville LIKE ?
                ORDER BY id DESC
            """, (f"%{mot}%", f"%{mot}%", f"%{mot}%", f"%{mot}%"))
            return cur.fetchall()
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # =====================================================
    # FERMER DATABASE (no-op for compatibility)
    # =====================================================

    def close(self):
        return