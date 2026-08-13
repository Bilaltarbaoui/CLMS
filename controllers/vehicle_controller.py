from models.vehicle_model import VehicleModel
from database.database import Database


class VehicleController:

    def __init__(self):

        self.model = VehicleModel()

    # =====================================================
    # AJOUTER
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

        self.model.ajouter(
            matricule,
            type_vehicule,
            marque,
            modele,
            kilometrage,
            etat,
            observation
        )
        try:
            db = Database()
            desc = f"Véhicule {matricule} - {marque} {modele} ajouté"
            db.ajouter_historique("SYSTEM", "CREATE", "Véhicule", desc)
        except Exception:
            pass

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_all(self):

        return self.model.get_all()

    # =====================================================
    # RECHERCHER (minimal, uses get_all())
    # =====================================================

    def rechercher(self, mot):
        if mot is None:
            return self.get_all()

        m = str(mot).lower()
        results = []
        for v in self.model.get_all():
            # v: (id, matricule, type, marque, modele, kilometrage, etat, observation)
            hay = ' '.join([str(v[1] or ''), str(v[3] or ''), str(v[4] or '')]).lower()
            if m in hay:
                results.append(v)

        return results

    # =====================================================
    # MODIFIER
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

        self.model.modifier(
            id_vehicule,
            matricule,
            type_vehicule,
            marque,
            modele,
            kilometrage,
            etat,
            observation
        )
        try:
            db = Database()
            desc = f"Véhicule {matricule} modifié (id={id_vehicule})"
            db.ajouter_historique("SYSTEM", "UPDATE", "Véhicule", desc)
        except Exception:
            pass

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer(self, id_vehicule):
        try:
            veh = next((v for v in self.get_all() if v[0] == id_vehicule), None)
            matricule = veh[1] if veh else ''
        except Exception:
            matricule = ''

        self.model.supprimer(
            id_vehicule
        )

        try:
            db = Database()
            desc = f"Véhicule {matricule} supprimé (id={id_vehicule})"
            db.ajouter_historique("SYSTEM", "DELETE", "Véhicule", desc)
        except Exception:
            pass

    # =====================================================
    # STATISTIQUES
    # =====================================================

    def get_statistics(self):

        return self.model.get_statistics()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        self.model.close()