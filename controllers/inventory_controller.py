from models.inventory_model import InventoryModel


class InventoryController:

    def __init__(self):

        self.model = InventoryModel()

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_inventory(self):

        return self.model.get_inventory()

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self, mot):

        return self.model.rechercher(mot)

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        if getattr(self, 'model', None) and hasattr(self.model, 'close'):

            try:
                self.model.close()
            except Exception:
                pass