from models.gasoil_model import GasoilModel
from models.vehicle_model import VehicleModel


class GasoilController:

    def __init__(self):

        # =====================================================
        # MODELS
        # =====================================================

        self.model = GasoilModel()

        self.vehicle_model = VehicleModel()

        # =====================================================
        # CREER TABLES
        # =====================================================

        self.model.create_table()

        self.vehicle_model.create_table()

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

        self.model.ajouter(
            vehicule,
            date_operation,
            heure_operation,
            kilometrage,
            quantite,
            observation
        )

    # =====================================================
    # AFFICHER OPERATIONS GASOIL
    # =====================================================

    def get_all(self):

        return self.model.get_all()

    # =====================================================
    # VEHICULES
    # =====================================================

    def get_vehicules(self):

        return self.vehicle_model.get_all()

    # =====================================================
    # STATISTIQUES GASOIL PAR VEHICULE
    # =====================================================

    def get_statistics_by_vehicle(self):

        operations = self.model.get_all()

        statistiques = {}

        for operation in operations:

            vehicule = operation[1]
            quantite = operation[5]

            if vehicule not in statistiques:

                statistiques[vehicule] = {
                    "operations": 0,
                    "quantite": 0
                }

            statistiques[vehicule]["operations"] += 1

            statistiques[vehicule]["quantite"] += float(
                quantite
            )

        return statistiques

    # =====================================================
    # MODIFIER
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

        self.model.modifier(
            id_operation,
            vehicule,
            date_operation,
            heure_operation,
            kilometrage,
            quantite,
            observation
        )

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer(
        self,
        id_operation
    ):

        self.model.supprimer(
            id_operation
        )
        
# =====================================================
# STATISTIQUES GASOIL PAR VEHICULE
# =====================================================

def get_statistics_by_vehicle(self):

    operations = self.model.get_all()

    statistiques = {}

    for operation in operations:

        if len(operation) < 6:
            continue

        vehicule = str(
            operation[1]
        ).strip()

        try:
            quantite = float(
                operation[5]
            )

        except (ValueError, TypeError):
            quantite = 0

        # ---------------------------------------------
        # PREMIERE OPERATION DU VEHICULE
        # ---------------------------------------------

        if vehicule not in statistiques:

            statistiques[vehicule] = {
                "operations": 0,
                "quantite": 0
            }

        # ---------------------------------------------
        # CALCUL
        # ---------------------------------------------

        statistiques[vehicule]["operations"] += 1

        statistiques[vehicule]["quantite"] += quantite

    return statistiques


    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        self.model.close()

        self.vehicle_model.close()
    