from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem
)

from controllers.inventory_controller import InventoryController


class InventoryView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = InventoryController()

        # =====================================================
        # RECHERCHE
        # =====================================================

        self.txtRecherche = self.ui.findChild(
            QLineEdit,
            "txtRecherche"
        )

        # =====================================================
        # BOUTON RECHERCHE
        # =====================================================

        self.btnRechercher = self.ui.findChild(
            QPushButton,
            "btnRechercher"
        )

        # =====================================================
        # BOUTON ACTUALISER
        # =====================================================

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        # =====================================================
        # TABLE INVENTAIRE
        # =====================================================

        self.tableInventaire = self.ui.findChild(
            QTableWidget,
            "tableInventaire"
        )

        # =====================================================
        # VERIFICATION
        # =====================================================

        if self.tableInventaire is None:

            print(
                "ERREUR : tableInventaire introuvable."
            )

            return

        # =====================================================
        # CONFIGURATION TABLEAU
        # =====================================================

        self.tableInventaire.clear()

        self.tableInventaire.setColumnCount(6)

        self.tableInventaire.setHorizontalHeaderLabels([

            "Référence",
            "Produit",
            "Catégorie",
            "Stock Total",
            "Stock Minimum",
            "État"

        ])

        # =====================================================
        # CONNEXIONS
        # =====================================================

        if self.btnRechercher is not None:

            self.btnRechercher.clicked.connect(
                self.rechercher
            )

        if self.btnActualiser is not None:

            self.btnActualiser.clicked.connect(
                self.actualiser
            )

        # =====================================================
        # CHARGEMENT
        # =====================================================

        self.charger_inventaire()

    # =====================================================
    # CONVERTIR STOCK
    # =====================================================

    def convertir_stock(self, valeur):

        try:

            return int(valeur)

        except (ValueError, TypeError):

            return 0

    # =====================================================
    # ETAT STOCK
    # =====================================================

    def determiner_etat(
        self,
        stock,
        stock_min
    ):

        if stock <= 0:

            return "Rupture"

        if stock <= stock_min:

            return "Stock faible"

        return "Disponible"

    # =====================================================
    # AFFICHER INVENTAIRE
    # =====================================================

    def afficher_produits(
        self,
        produits
    ):

        self.tableInventaire.setRowCount(0)

        for ligne, produit in enumerate(produits):

            self.tableInventaire.insertRow(
                ligne
            )

            # =================================================
            # PRODUCTS
            # =================================================
            #
            # 0 = id
            # 1 = reference
            # 2 = nom
            # 3 = categorie
            # 4 = marque
            # 5 = unite
            # 6 = stock
            # 7 = stock_min
            #
            # =================================================

            reference = produit[1]

            nom = produit[2]

            categorie = produit[3]

            stock = self.convertir_stock(
                produit[6]
            )

            stock_min = self.convertir_stock(
                produit[7]
            )

            etat = self.determiner_etat(
                stock,
                stock_min
            )

            # =================================================
            # COLONNE 0
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(reference)
                )
            )

            # =================================================
            # COLONNE 1
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(nom)
                )
            )

            # =================================================
            # COLONNE 2
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    str(categorie)
                )
            )

            # =================================================
            # COLONNE 3
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                3,
                QTableWidgetItem(
                    str(stock)
                )
            )

            # =================================================
            # COLONNE 4
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                4,
                QTableWidgetItem(
                    str(stock_min)
                )
            )

            # =================================================
            # COLONNE 5
            # =================================================

            self.tableInventaire.setItem(
                ligne,
                5,
                QTableWidgetItem(
                    etat
                )
            )

        # =====================================================
        # AJUSTER LES COLONNES
        # =====================================================

        self.tableInventaire.resizeColumnsToContents()

    # =====================================================
    # CHARGER INVENTAIRE
    # =====================================================

    def charger_inventaire(self):

        produits = self.controller.get_inventory()

        self.afficher_produits(
            produits
        )

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self):

        mot = self.txtRecherche.text().strip()

        if mot == "":

            self.charger_inventaire()

            return

        produits = self.controller.rechercher(
            mot
        )

        self.afficher_produits(
            produits
        )

    # =====================================================
    # ACTUALISER
    # =====================================================

    def actualiser(self):

        self.txtRecherche.clear()

        self.charger_inventaire()