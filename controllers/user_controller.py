from database.database import Database


class UserController:

    VALID_ROLES = ('admin', 'responsable', 'magasinier')

    def __init__(self):

        self.db = Database()

    # =====================================================
    # LIST
    # =====================================================

    def get_all_users(self):
        return self.db.get_all_users()

    # =====================================================
    # GET
    # =====================================================

    def get_user_by_id(self, user_id):
        return self.db.get_user_by_id(user_id)

    def get_user_by_username(self, username):
        return self.db.get_user_by_username(username)

    # =====================================================
    # AVAILABILITY
    # =====================================================

    def username_exists(self, username):
        return self.db.username_exists(username)

    # =====================================================
    # CREATE
    # =====================================================

    def create_user(self, username, password, role='magasinier', nom_complet=None, actif=1):
        if role not in UserController.VALID_ROLES:
            raise ValueError('invalid role')
        # delegate to Database.create_user (will hash password)
        new_id = self.db.create_user(username, password, role=role, nom_complet=nom_complet, actif=actif)
        try:
            actor = getattr(self, '_actor', None) or 'SYSTEM'
            # Log creation without sensitive data
            desc = f"Utilisateur {username} créé (role={role})"
            self.db.ajouter_historique(actor, 'CREATE', 'Utilisateur', desc)
        except Exception:
            pass
        return new_id

    # =====================================================
    # UPDATE
    # =====================================================

    def update_user(self, user_id, role=None, nom_complet=None, actif=None):
        if role is not None and role not in UserController.VALID_ROLES:
            raise ValueError('invalid role')
        # Read previous state for logging
        try:
            prev = self.get_user_by_id(user_id)
        except Exception:
            prev = None

        res = self.db.update_user(user_id, role=role, nom_complet=nom_complet, actif=actif)

        try:
            actor = getattr(self, '_actor', None) or 'SYSTEM'
            parts = []
            if prev:
                if role is not None and prev.get('role') != role:
                    parts.append(f"rôle: {prev.get('role')} -> {role}")
                if nom_complet is not None and prev.get('nom_complet') != nom_complet:
                    parts.append("nom_complet modifié")
                if actif is not None and prev.get('actif') != int(bool(actif)):
                    parts.append(f"actif: {prev.get('actif')} -> {int(bool(actif))}")
            else:
                parts.append('utilisateur mis à jour')

            desc = f"Utilisateur id={user_id} mis à jour ({'; '.join(parts)})"
            self.db.ajouter_historique(actor, 'UPDATE', 'Utilisateur', desc)
        except Exception:
            pass

        return res

    # =====================================================
    # ACTIVATE / DEACTIVATE
    # =====================================================

    def set_user_active(self, user_id, actif: int):
        # Log activation/deactivation
        try:
            prev = self.get_user_by_id(user_id)
        except Exception:
            prev = None

        res = self.db.set_user_active(user_id, int(bool(actif)))

        try:
            actor = getattr(self, '_actor', None) or 'SYSTEM'
            username = prev.get('username') if prev else f'id={user_id}'
            action = 'ACTIVATE' if int(bool(actif)) else 'DEACTIVATE'
            desc = f"Utilisateur {username} { 'activé' if action=='ACTIVATE' else 'désactivé' }"
            self.db.ajouter_historique(actor, action, 'Utilisateur', desc)
        except Exception:
            pass

        return res

    # =====================================================
    # PASSWORD
    # =====================================================

    def set_user_password(self, user_id, new_password):
        # new_password must be provided; password hashing handled by Database
        # Do not log passwords; only a non-sensitive event
        try:
            prev = self.get_user_by_id(user_id)
        except Exception:
            prev = None

        res = self.db.set_user_password(user_id, new_password)

        try:
            actor = getattr(self, '_actor', None) or 'SYSTEM'
            username = prev.get('username') if prev else f'id={user_id}'
            desc = f"Mot de passe modifié pour utilisateur {username}"
            self.db.ajouter_historique(actor, 'UPDATE', 'Utilisateur', desc)
        except Exception:
            pass

        return res

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):
        try:
            if getattr(self, 'db', None):
                self.db.close()
        except Exception:
            pass
