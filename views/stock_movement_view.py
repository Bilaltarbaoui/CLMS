from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QComboBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

from controllers.stock_movement_controller import StockMovementController


class StockMovementView:

    def __init__(self, ui):

        self.ui = ui

        print("STOCK MOVEMENT VIEW START")

        # =====================================================
        # CONTROLLER
        # =====================================================

        self.controller = StockMovementController()

        print("STOCK MOVEMENT CONTROLLER = OK")

        # =====================================================
        # TABLE MOUVEMENTS STOCK
        # =====================================================

        self.tableStockMovements = self.ui.findChild(
            QTableWidget,
            "tableStockMovements"
        )

        if self.tableStockMovements is None:

            print(
                "ERREUR : tableStockMovements introuvable"
            )

            return

        print(
            "TABLE STOCK MOVEMENTS = OK"
        )

        # =====================================================
        # CHAMP RECHERCHE
        # =====================================================

        self.txtRecherche = self.ui.findChild(
            QLineEdit,
            "txtRecherche"
        )

        if self.txtRecherche is None:

            print(
                "ERREUR : txtRecherche introuvable"
            )

        else:

            print(
                "TXT RECHERCHE = OK"
            )

        # =====================================================
        # FILTRE TYPE
        # =====================================================

        self.cmbType = self.ui.findChild(
            QComboBox,
            "cmbType"
        )

        if self.cmbType is None:

            print(
                "ERREUR : cmbType introuvable"
            )

        else:

            print(
                "CMB TYPE = OK"
            )

        # =====================================================
        # TOTAL ENTREES
        # =====================================================

        self.lblTotalEntrees = self.ui.findChild(
            QLabel,
            "lblTotalEntrees"
        )

        if self.lblTotalEntrees is None:

            print(
                "ERREUR : lblTotalEntrees introuvable"
            )

        else:

            print(
                "LBL TOTAL ENTREES = OK"
            )

        # =====================================================
        # TOTAL SORTIES
        # =====================================================

        self.lblTotalSorties = self.ui.findChild(
            QLabel,
            "lblTotalSorties"
        )

        if self.lblTotalSorties is None:

            print(
                "ERREUR : lblTotalSorties introuvable"
            )

        else:

            print(
                "LBL TOTAL SORTIES = OK"
            )

        # =====================================================
        # BOUTON ACTUALISER
        # =====================================================

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        if self.btnActualiser is None:

            print(
                "ERREUR : btnActualiser introuvable"
            )

        else:

            self.btnActualiser.clicked.connect(
                self.charger_mouvements
            )

            print(
                "BTN ACTUALISER = OK"
            )

        # =====================================================
        # BOUTON FERMER
        # =====================================================

        self.btnFermer = self.ui.findChild(
            QPushButton,
            "btnFermer"
        )

        if self.btnFermer is None:

            print(
                "ERREUR : btnFermer introuvable"
            )

        else:

            self.btnFermer.clicked.connect(
                self.fermer
            )

            print(
                "BTN FERMER = OK"
            )

        # =====================================================
        # CONNEXION RECHERCHE
        # =====================================================

        if self.txtRecherche is not None:

            self.txtRecherche.textChanged.connect(
                self.appliquer_filtres
            )

        # =====================================================
        # CONNEXION FILTRE TYPE
        # =====================================================

        if self.cmbType is not None:

            self.cmbType.currentTextChanged.connect(
                self.appliquer_filtres
            )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_mouvements()

        print(
            "STOCK MOVEMENT VIEW = OK"
        )

    # =========================================================
    # CHARGER MOUVEMENTS
    # =========================================================

    def charger_mouvements(self):

        print(
            ">>> CHARGEMENT MOUVEMENTS STOCK"
        )

        mouvements = self.controller.get_movements()

        print(
            "MOUVEMENTS =",
            mouvements
        )

        self.afficher_mouvements(
            mouvements
        )

    # =========================================================
    # APPLIQUER FILTRES
    # =========================================================

    def appliquer_filtres(self):

        # -----------------------------------------------------
        # RECHERCHE
        # -----------------------------------------------------

        mot = ""

        if self.txtRecherche is not None:

            mot = self.txtRecherche.text().strip()

        # -----------------------------------------------------
        # TYPE
        # -----------------------------------------------------

        type_mouvement = "Tous"

        if self.cmbType is not None:

            type_mouvement = (
                self.cmbType.currentText()
            )

        print(
            "FILTRE =",
            type_mouvement,
            "| RECHERCHE =",
            mot
        )

        # =====================================================
        # CAS 1 : RECHERCHE
        # =====================================================

        if mot != "":

            mouvements = (
                self.controller.rechercher(
                    mot
                )
            )

            # -------------------------------------------------
            # FILTRE ENTREES
            # -------------------------------------------------

            if type_mouvement == "Entrées":

                mouvements = [

                    mouvement

                    for mouvement in mouvements

                    if str(
                        mouvement[0]
                    ).strip().upper()
                    in (
                        "ENTREE",
                        "ENTRÉE"
                    )
                ]

            # -------------------------------------------------
            # FILTRE SORTIES
            # -------------------------------------------------

            elif type_mouvement == "Sorties":

                mouvements = [

                    mouvement

                    for mouvement in mouvements

                    if str(
                        mouvement[0]
                    ).strip().upper()
                    == "SORTIE"
                ]

        # =====================================================
        # CAS 2 : PAS DE RECHERCHE
        # =====================================================

        else:

            mouvements = (
                self.controller.get_movements_filtre(
                    type_mouvement
                )
            )

        # =====================================================
        # AFFICHAGE
        # =====================================================

        self.afficher_mouvements(
            mouvements
        )

    # =========================================================
    # AFFICHER MOUVEMENTS
    # =========================================================

    def afficher_mouvements(
        self,
        mouvements
    ):

        if self.tableStockMovements is None:

            return

        print(
            ">>> AFFICHAGE MOUVEMENTS :",
            len(mouvements),
            "lignes"
        )

        # -----------------------------------------------------
        # VIDER TABLEAU
        # -----------------------------------------------------

        self.tableStockMovements.setRowCount(
            0
        )

        # -----------------------------------------------------
        # AJOUTER LES LIGNES
        # -----------------------------------------------------

        for ligne, mouvement in enumerate(
            mouvements
        ):

            self.tableStockMovements.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(
                mouvement
            ):

                item = QTableWidgetItem(
                    "" if valeur is None
                    else str(valeur)
                )

                self.tableStockMovements.setItem(
                    ligne,
                    colonne,
                    item
                )

        # -----------------------------------------------------
        # AJUSTER COLONNES
        # -----------------------------------------------------

        self.tableStockMovements.resizeColumnsToContents()

        # =====================================================
        # CALCUL TOTAUX
        # =====================================================

        self.calculer_totaux(
            mouvements
        )

        print(
            "AFFICHAGE MOUVEMENTS = OK"
        )

    # =========================================================
    # CALCULER TOTAUX
    # =========================================================

    def calculer_totaux(
        self,
        mouvements
    ):

        total_entrees = 0
        total_sorties = 0

        # -----------------------------------------------------
        # PARCOURIR MOUVEMENTS
        # -----------------------------------------------------

        for mouvement in mouvements:

            if len(mouvement) < 4:

                continue

            # -------------------------------------------------
            # TYPE
            # -------------------------------------------------

            type_mouvement = str(
                mouvement[0]
            ).strip().upper()

            # -------------------------------------------------
            # QUANTITE
            # -------------------------------------------------

            try:

                quantite = float(
                    mouvement[3]
                )

            except (
                ValueError,
                TypeError
            ):

                quantite = 0

            # -------------------------------------------------
            # ENTREE
            # -------------------------------------------------

            if type_mouvement in (
                "ENTREE",
                "ENTRÉE"
            ):

                total_entrees += quantite

            # -------------------------------------------------
            # SORTIE
            # -------------------------------------------------

            elif type_mouvement == "SORTIE":

                total_sorties += quantite

        # =====================================================
        # AFFICHAGE TOTAL ENTREES
        # =====================================================

        if self.lblTotalEntrees is not None:

            self.lblTotalEntrees.setText(
                f"Total Entrées : {total_entrees:g}"
            )

        # =====================================================
        # AFFICHAGE TOTAL SORTIES
        # =====================================================

        if self.lblTotalSorties is not None:

            self.lblTotalSorties.setText(
                f"Total Sorties : {total_sorties:g}"
            )

        # =====================================================
        # DEBUG
        # =====================================================

        print(
            "TOTAL ENTREES =",
            total_entrees
        )

        print(
            "TOTAL SORTIES =",
            total_sorties
        )

    # =========================================================
    # FERMER
    # =========================================================

    def fermer(self):

        print(
            "FERMETURE MOUVEMENTS STOCK"
        )

        self.ui.close()