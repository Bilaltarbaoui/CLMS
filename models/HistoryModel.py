import sqlite3
import unicodedata

from database.database import Database


class HistoryModel:

    def __init__(self):

        # =====================================================
        # DATABASE
        # =====================================================

        self.connection = Database.get_safe_connection("database/clms.db")
        self.cursor = self.connection.cursor()

        print("HISTORY MODEL = OK")

        # Canonical module mapping: normalize DB variants to these canonical names
        self._canonical_order = [
            'Produit',
            'Client',
            'Entrée',
            'Sortie',
            'Véhicule',
            'Gasoil'
        ]

        # Map normalized key -> canonical name
        def _norm(s):
            if s is None:
                return ''
            s2 = str(s).strip().lower()
            s2 = unicodedata.normalize('NFKD', s2)
            s2 = ''.join(ch for ch in s2 if not unicodedata.combining(ch))
            return s2

        self._canonical_map = {
            _norm('produit'): 'Produit',
            _norm('produits'): 'Produit',
            _norm('client'): 'Client',
            _norm('clients'): 'Client',
            _norm('entrée'): 'Entrée',
            _norm('entree'): 'Entrée',
            _norm('entrees'): 'Entrée',
            _norm('sortie'): 'Sortie',
            _norm('sorties'): 'Sortie',
            _norm('véhicule'): 'Véhicule',
            _norm('vehicule'): 'Véhicule',
            _norm('véhicules'): 'Véhicule',
            _norm('vehicules'): 'Véhicule',
            _norm('gasoil'): 'Gasoil',
        }

        # Helper to normalize module value to canonical if possible
        def _to_canonical(val):
            k = _norm(val)
            return self._canonical_map.get(k, val)

        self._to_canonical = _to_canonical

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

        rows = self.cursor.fetchall()
        # Normalize module names for display
        normalized = []
        for r in rows:
            user, typ, module, desc, date = r
            module_canon = self._to_canonical(module)
            normalized.append((user, typ, module_canon, desc, date))

        return normalized

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

        rows = self.cursor.fetchall()
        normalized = []
        for r in rows:
            user, typ, module, desc, date = r
            module_canon = self._to_canonical(module)
            normalized.append((user, typ, module_canon, desc, date))

        return normalized

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

        rows = self.cursor.fetchall()
        normalized = []
        for r in rows:
            user, typ, module, desc, date = r
            module_canon = self._to_canonical(module)
            normalized.append((user, typ, module_canon, desc, date))

        return normalized

    # =====================================================
    # FILTRE PAR MODULE
    # =====================================================

    def get_history_module(self, module_name):

        module_name = (module_name or '').strip()

        if module_name == "":
            return self.get_history()

        # Determine normalized key for requested canonical module
        kn = unicodedata.normalize('NFKD', module_name.strip().lower())
        kn = ''.join(ch for ch in kn if not unicodedata.combining(ch))

        # Build a list of DB module variants that map to this canonical
        variants = [k for k, v in self._canonical_map.items() if v == self._canonical_map.get(kn, module_name)]

        # If no variants found, fall back to exact match
        if not variants:
            variants = [module_name]

        # Fetch all and filter in Python for robust matching
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

        rows = self.cursor.fetchall()
        normalized = []
        for r in rows:
            user, typ, module, desc, date = r
            kn_row = unicodedata.normalize('NFKD', (module or '').strip().lower())
            kn_row = ''.join(ch for ch in kn_row if not unicodedata.combining(ch))
            if kn_row in variants or module in variants:
                module_canon = self._to_canonical(module)
                normalized.append((user, typ, module_canon, desc, date))

        return normalized

    # =====================================================
    # LISTER MODULES DISTINCTS
    # =====================================================

    def get_modules_list(self):

        self.cursor.execute("""
            SELECT DISTINCT module FROM historique
        """)

        rows = self.cursor.fetchall()

        seen = set()
        result = []

        # Normalize each found module to canonical and collect unique canonical modules
        for r in rows:
            if not r or r[0] is None:
                continue
            module = r[0]
            canon = self._to_canonical(module)
            if canon not in seen and canon in self._canonical_order:
                seen.add(canon)
                result.append(canon)

        # Preserve canonical order
        ordered = [m for m in self._canonical_order if m in result]

        return ordered

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        if self.connection:

            self.connection.close()

            print(
                "HISTORY DATABASE CLOSED"
            )