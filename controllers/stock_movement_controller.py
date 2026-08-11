from models.stock_movement_model import StockMovementModel


class StockMovementController:

    def __init__(self):

        print("STOCK MOVEMENT CONTROLLER START")

        self.model = StockMovementModel()

        print("STOCK MOVEMENT MODEL = OK")

    # =====================================================
    # AFFICHER TOUS LES MOUVEMENTS
    # =====================================================

    def get_movements(self):

        return self.model.get_movements()

    # =====================================================
    # RECHERCHER UN MOUVEMENT
    # =====================================================

    def rechercher(self, mot):

        return self.model.rechercher(
            mot
        )

    # =====================================================
    # FILTRER PAR TYPE
    # =====================================================

    def get_movements_filtre(
        self,
        type_mouvement
    ):

        return self.model.get_movements_filtre(
            type_mouvement
        )

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        self.model.close()