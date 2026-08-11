from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QComboBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)

from controllers.HistoryController import HistoryController


class HistoryView:

    def __init__(self, ui):

        self.ui = ui

        print("HISTORY VIEW START")

        # =====================================================
        # CONTROLLER
        # =====================================================

        self.controller = HistoryController()

        print("HISTORY CONTROLLER = OK")

        # =====================================================
        # TABLE HISTORIQUE
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
            "TABLE HISTORIQUE = OK"
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
        # FILTRE TYPE OPERATION
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
                self.charger_historique
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
        # RECHERCHE
        # =====================================================

        if self.txtRecherche is not None:

            self.txtRecherche.textChanged.connect(
                self.appliquer_filtres
            )

            print(
                "RECHERCHE = CONNECTEE"
            )

        # =====================================================
        # FILTRE
        # =====================================================

        if self.cmbType is not None:

            self.cmbType.currentTextChanged.connect(
                self.appliquer_filtres
            )

            print(
                "FILTRE = CONNECTE"
            )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_historique()

        print(
            "HISTORY VIEW = OK"
        )

    # =========================================================
    # CHARGER HISTORIQUE COMPLET
    # =========================================================

    def charger_historique(self):

        print(
            ">>> CHARGEMENT HISTORIQUE COMPLET"
        )

        try:

            historique = self.controller.get_history()

            print(
                "HISTORIQUE =",
                historique
            )

            self.afficher_historique(
                historique
            )

        except Exception as e:

            print(
                "ERREUR CHARGEMENT HISTORIQUE :",
                e
            )

    # =========================================================
    # APPLIQUER FILTRES
    # =========================================================

    def appliquer_filtres(self):

        # =====================================================
        # RECHERCHE
        # =====================================================

        mot = ""

        if self.txtRecherche is not None:

            mot = self.txtRecherche.text().strip()

        # =====================================================
        # TYPE OPERATION
        # =====================================================

        type_operation = "Tous"

        if self.cmbType is not None:

            type_operation = (
                self.cmbType.currentText().strip()
            )

        print(
            "TYPE =",
            type_operation,
            "| RECHERCHE =",
            mot
        )

        try:

            # =================================================
            # AVEC RECHERCHE
            # =================================================

            if mot != "":

                historique = (
                    self.controller.rechercher(
                        mot
                    )
                )

            # =================================================
            # SANS RECHERCHE
            # =================================================

            else:

                historique = (
                    self.controller.get_history()
                )

            # =================================================
            # FILTRE TYPE
            # =================================================

            if type_operation.lower() != "tous":

                historique = [
                    operation
                    for operation in historique
                    if self.est_type_operation(
                        operation,
                        type_operation
                    )
                ]

            # =================================================
            # AFFICHAGE
            # =================================================

            self.afficher_historique(
                historique
            )

        except Exception as e:

            print(
                "ERREUR FILTRAGE HISTORIQUE :",
                e
            )

    # =========================================================
    # DETECTER LE TYPE D'OPERATION
    # =========================================================

    def est_type_operation(
        self,
        operation,
        type_recherche
    ):

        type_recherche = (
            str(type_recherche)
            .strip()
            .upper()
        )

        # -----------------------------------------------------
        # Conversion de l'opération en texte
        # -----------------------------------------------------

        valeurs = [
            str(valeur).strip().upper()
            for valeur in operation
            if valeur is not None
        ]

        # -----------------------------------------------------
        # Normalisation
        # -----------------------------------------------------

        if type_recherche in (
            "ENTRÉES",
            "ENTREES",
            "ENTREE"
        ):

            mots_acceptes = (
                "ENTREE",
                "ENTRÉE",
                "ENTREES",
                "ENTRÉES"
            )

        elif type_recherche in (
            "SORTIES",
            "SORTIE"
        ):

            mots_acceptes = (
                "SORTIE",
                "SORTIES"
            )

        else:

            return True

        # -----------------------------------------------------
        # Recherche du type dans la ligne
        # -----------------------------------------------------

        for valeur in valeurs:

            if valeur in mots_acceptes:

                return True

        return False

    # =========================================================
    # AFFICHER HISTORIQUE
    # =========================================================

    def afficher_historique(
        self,
        historique
    ):

        if self.tableStockMovements is None:

            return

        print(
            ">>> AFFICHAGE HISTORIQUE :",
            len(historique),
            "lignes"
        )

        # =====================================================
        # VIDER TABLEAU
        # =====================================================

        self.tableStockMovements.setRowCount(
            0
        )

        # =====================================================
        # AJOUTER LES LIGNES
        # =====================================================

        for ligne, operation in enumerate(
            historique
        ):

            self.tableStockMovements.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(
                operation
            ):

                item = QTableWidgetItem(
                    ""
                    if valeur is None
                    else str(valeur)
                )

                self.tableStockMovements.setItem(
                    ligne,
                    colonne,
                    item
                )

        # =====================================================
        # AJUSTEMENT COLONNES
        # =====================================================

        self.tableStockMovements.resizeColumnsToContents()

        # =====================================================
        # TOTAUX
        # =====================================================

        self.calculer_totaux(
            historique
        )

        print(
            "AFFICHAGE HISTORIQUE = OK"
        )

    # =========================================================
    # CALCULER TOTAUX
    # =========================================================

    def calculer_totaux(
        self,
        historique
    ):

        total_entrees = 0
        total_sorties = 0

        for operation in historique:

            if not operation:

                continue

            # -------------------------------------------------
            # Chercher le type
            # -------------------------------------------------

            type_operation = None

            for valeur in operation:

                if valeur is None:

                    continue

                texte = (
                    str(valeur)
                    .strip()
                    .upper()
                )

                if texte in (
                    "ENTREE",
                    "ENTRÉE",
                    "ENTREES",
                    "ENTRÉES"
                ):

                    type_operation = "ENTREE"

                    break

                if texte in (
                    "SORTIE",
                    "SORTIES"
                ):

                    type_operation = "SORTIE"

                    break

            # -------------------------------------------------
            # Chercher la quantité
            # -------------------------------------------------

            quantite = 0

            for valeur in operation:

                if valeur is None:

                    continue

                try:

                    nombre = float(
                        str(valeur)
                        .replace(",", ".")
                        .strip()
                    )

                    if nombre >= 0:

                        quantite = nombre

                except (
                    ValueError,
                    TypeError
                ):

                    continue

            # -------------------------------------------------
            # Addition
            # -------------------------------------------------

            if type_operation == "ENTREE":

                total_entrees += quantite

            elif type_operation == "SORTIE":

                total_sorties += quantite

        # =====================================================
        # AFFICHAGE TOTAUX
        # =====================================================

        if self.lblTotalEntrees is not None:

            self.lblTotalEntrees.setText(
                f"Total Entrées : {total_entrees:g}"
            )

        if self.lblTotalSorties is not None:

            self.lblTotalSorties.setText(
                f"Total Sorties : {total_sorties:g}"
            )

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
            "FERMETURE HISTORIQUE"
        )

        try:

            self.controller.close()

        except Exception as e:

            print(
                "ERREUR FERMETURE CONTROLLER :",
                e
            )

        self.ui.close()
