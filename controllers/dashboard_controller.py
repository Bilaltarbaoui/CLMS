from models.dashboard_model import DashboardModel


class DashboardController:

    def __init__(self):

        self.model = DashboardModel()

    # =====================================================
    # NOMBRE DE PRODUITS
    # =====================================================

    def get_nombre_produits(self):

        return self.model.get_nombre_produits()

    # =====================================================
    # TOTAL ENTREES
    # =====================================================

    def get_total_entrees(self):

        return self.model.get_total_entrees()

    # =====================================================
    # TOTAL SORTIES
    # =====================================================

    def get_total_sorties(self):

        return self.model.get_total_sorties()

    # =====================================================
    # ALERTES
    # =====================================================

    def get_nombre_alertes(self):

        return self.model.get_nombre_alertes()

    # =====================================================
    # DERNIERS MOUVEMENTS
    # =====================================================

    def get_derniers_mouvements(self):

        return self.model.get_derniers_mouvements()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        if getattr(self, 'model', None) and hasattr(self.model, 'close'):

            try:
                self.model.close()
            except Exception:
                pass