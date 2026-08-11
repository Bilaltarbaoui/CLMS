from models.vehicle_model import VehicleModel


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

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_all(self):

        return self.model.get_all()

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

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer(self, id_vehicule):

        self.model.supprimer(
            id_vehicule
        )

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