from database.database import Database
from models.HistoryModel import HistoryModel


class HistoryController:

    def __init__(self):

        print("HISTORY CONTROLLER START")

        # =====================================================
        # DATABASE INITIALIZATION
        # =====================================================

        self.database = Database()
        self.database.create_tables()

        # =====================================================
        # MODEL
        # =====================================================

        self.model = HistoryModel()

        print("HISTORY CONTROLLER = OK")

    # =====================================================
    # AFFICHER HISTORIQUE COMPLET
    # =====================================================

    def get_history(self):

        print(
            ">>> CONTROLLER : GET HISTORY"
        )

        return self.model.get_history()

    # =====================================================
    # RECHERCHER DANS HISTORIQUE
    # =====================================================

    def rechercher(self, mot):

        print(
            ">>> CONTROLLER : RECHERCHE =",
            mot
        )

        return self.model.rechercher(
            mot
        )

    # =====================================================
    # FILTRER PAR TYPE
    # =====================================================

    def get_history_filtre(
        self,
        type_mouvement
    ):

        print(
            ">>> CONTROLLER : FILTRE =",
            type_mouvement
        )

        return self.model.get_history_filtre(
            type_mouvement
        )

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        print(
            ">>> FERMETURE HISTORY CONTROLLER"
        )

        self.model.close()

        print(
            "HISTORY CONTROLLER CLOSED"
        )
