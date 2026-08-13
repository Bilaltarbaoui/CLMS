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
        try:
            from database.database import Database as _DB
            db = _DB()
            desc = f"Opération gasoil {quantite}L pour véhicule {vehicule}"
            db.ajouter_historique("SYSTEM", "CREATE", "Gasoil", desc)
        except Exception:
            pass

    # =====================================================
    # AFFICHER OPERATIONS GASOIL
    # =====================================================

    def get_all(self):

        return self.model.get_all()

    # =====================================================
    # RECHERCHER DANS LES OPERATIONS GASOIL
    # =====================================================

    def rechercher(self, mot):
        """Search gasoil operations by vehicule, date, or observation"""
        if mot is None:
            return self.get_all()

        m = str(mot).lower()
        results = []
        for op in self.model.get_all():
            # op: (id, vehicule, date_operation, heure_operation, kilometrage, quantite, observation)
            hay = ' '.join([
                str(op[1] or ''),  # vehicule
                str(op[2] or ''),  # date_operation
                str(op[6] or '')   # observation
            ]).lower()
            if m in hay:
                results.append(op)

        return results

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

            if len(operation) < 6:
                continue

            vehicule = str(operation[1]).strip()

            try:
                quantite = float(operation[5])
            except (ValueError, TypeError):
                quantite = 0

            if vehicule not in statistiques:

                statistiques[vehicule] = {
                    "operations": 0,
                    "quantite": 0
                }

            statistiques[vehicule]["operations"] += 1

            statistiques[vehicule]["quantite"] += quantite

        return statistiques

    def get_total_gasoil(self):
        statistics = self.model.get_statistics_by_vehicle()
        return sum((row[2] or 0) for row in statistics)

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
        try:
            from database.database import Database as _DB
            db = _DB()
            desc = f"Opération gasoil modifiée id={id_operation} véhicule={vehicule} qty={quantite}"
            db.ajouter_historique("SYSTEM", "UPDATE", "Gasoil", desc)
        except Exception:
            pass

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer(
        self,
        id_operation
    ):

        # Attempt to fetch operation info before deletion
        try:
            op = next((o for o in self.get_all() if o[0] == id_operation), None)
            vehicule = op[1] if op else ''
            quantite = op[5] if op else ''
        except Exception:
            vehicule = ''
            quantite = ''

        self.model.supprimer(
            id_operation
        )

        try:
            from database.database import Database as _DB
            db = _DB()
            desc = f"Opération gasoil supprimée id={id_operation} véhicule={vehicule} qty={quantite}"
            db.ajouter_historique("SYSTEM", "DELETE", "Gasoil", desc)
        except Exception:
            pass

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        try:
            if getattr(self, 'model', None) and hasattr(self.model, 'close'):
                self.model.close()
        except Exception:
            pass

        try:
            if getattr(self, 'vehicle_model', None) and hasattr(self.vehicle_model, 'close'):
                self.vehicle_model.close()
        except Exception:
            pass
    