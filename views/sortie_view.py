from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from controllers.sortie_controller import SortieController
from controllers.product_controller import ProductController


class SortieView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = SortieController()
        self.product_controller = ProductController()

        self.id_sortie = None

        # =====================================================
        # PRODUIT
        # =====================================================

        self.cmbProduit = self.ui.findChild(
            QComboBox,
            "cmbProduit"
        )

        # =====================================================
        # QUANTITE
        # =====================================================

        self.txtQuantite = self.ui.findChild(
            QLineEdit,
            "txtQuantite"
        )

        # =====================================================
        # CLIENT
        # =====================================================

        self.txtClient = self.ui.findChild(
            QLineEdit,
            "txtClient"
        )

        # =====================================================
        # NUMERO BON
        # =====================================================

        self.txtNumeroBon = self.ui.findChild(
            QLineEdit,
            "txtNumeroBon"
        )

        # =====================================================
        # COMMENTAIRE
        # =====================================================

        self.txtCommentaire = self.ui.findChild(
            QTextEdit,
            "txtCommentaire"
        )

        # =====================================================
        # BOUTON AJOUTER
        # =====================================================

        self.btnAjouterSortie = self.ui.findChild(
            QPushButton,
            "btnAjouterSortie"
        )

        # =====================================================
        # BOUTON ACTUALISER
        # =====================================================

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableSorties = self.ui.findChild(
            QTableWidget,
            "tableSorties"
        )

        # =====================================================
        # VERIFICATION DES WIDGETS
        # =====================================================

        if self.cmbProduit is None:
            print("ERREUR : cmbProduit introuvable")

        if self.txtQuantite is None:
            print("ERREUR : txtQuantite introuvable")

        if self.txtClient is None:
            print("ERREUR : txtClient introuvable")

        if self.txtNumeroBon is None:
            print("ERREUR : txtNumeroBon introuvable")

        if self.txtCommentaire is None:
            print("ERREUR : txtCommentaire introuvable")

        if self.btnAjouterSortie is None:
            print("ERREUR : btnAjouterSortie introuvable")

        if self.btnActualiser is None:
            print("ERREUR : btnActualiser introuvable")

        if self.tableSorties is None:
            print("ERREUR : tableSorties introuvable")

        # =====================================================
        # CONNEXIONS
        # =====================================================

        if self.btnAjouterSortie is not None:

            self.btnAjouterSortie.clicked.connect(
                self.ajouter_sortie
            )

        if self.btnActualiser is not None:

            self.btnActualiser.clicked.connect(
                self.charger_sorties
            )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_produits()
        self.charger_sorties()

        print("SORTIE VIEW = OK")

    # =====================================================
    # CHARGER PRODUITS
    # =====================================================

    def charger_produits(self):

        if self.cmbProduit is None:
            return

        self.cmbProduit.clear()

        produits = self.product_controller.get_all_products()

        for produit in produits:

            product_id = produit[0]
            reference = produit[1]
            nom = produit[2]

            self.cmbProduit.addItem(
                f"{reference} - {nom}",
                product_id
            )

        print("SORTIE PRODUITS = OK")

    # =====================================================
    # CHARGER LES SORTIES
    # =====================================================

    def charger_sorties(self):

        if self.tableSorties is None:
            return

        try:

            sorties = self.controller.get_all_sorties()

            self.tableSorties.setRowCount(0)

            for ligne, sortie in enumerate(sorties):

                self.tableSorties.insertRow(ligne)

                for colonne, valeur in enumerate(sortie):

                    self.tableSorties.setItem(
                        ligne,
                        colonne,
                        QTableWidgetItem(
                            str(valeur)
                        )
                    )

            self.tableSorties.resizeColumnsToContents()

            print("SORTIES TABLE = OK")

        except Exception as error:

            print("ERREUR : CHARGEMENT SORTIES")
            print("DETAIL :", error)

    # =====================================================
    # AJOUTER UNE SORTIE
    # =====================================================

    def ajouter_sortie(self):

        # =================================================
        # VERIFIER PRODUIT
        # =================================================

        if self.cmbProduit.currentIndex() == -1:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez sélectionner un produit."
            )

            return

        # =================================================
        # RECUPERER QUANTITE
        # =================================================

        texte_quantite = (
            self.txtQuantite
            .text()
            .strip()
        )

        # =================================================
        # QUANTITE VIDE
        # =================================================

        if texte_quantite == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir une quantité."
            )

            return

        # =================================================
        # VERIFIER QUANTITE
        # =================================================

        try:

            quantite = int(texte_quantite)

        except ValueError:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "La quantité doit être un nombre entier."
            )

            return

        # =================================================
        # QUANTITE POSITIVE
        # =================================================

        if quantite <= 0:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "La quantité doit être supérieure à 0."
            )

            return

        # =================================================
        # RECUPERER LES DONNEES
        # =================================================

        try:

            product_id = self.cmbProduit.currentData()

            client = (
                self.txtClient
                .text()
                .strip()
            )

            numero_bon = (
                self.txtNumeroBon
                .text()
                .strip()
            )

            commentaire = (
                self.txtCommentaire
                .toPlainText()
                .strip()
            )

            # =================================================
            # ENREGISTRER
            # =================================================

            self.controller.ajouter_sortie(
                product_id,
                quantite,
                client,
                numero_bon,
                commentaire
            )

            # =================================================
            # SUCCES
            # =================================================

            QMessageBox.information(
                self.ui,
                "Succès",
                "Sortie enregistrée avec succès."
            )

            # =================================================
            # NETTOYER
            # =================================================

            self.vider_champs()

            # =================================================
            # ACTUALISER
            # =================================================

            self.charger_sorties()

            # Recharger les produits permet aussi
            # de garder le ComboBox synchronisé.

            self.charger_produits()

        except Exception as error:

            QMessageBox.critical(
                self.ui,
                "Erreur",
                str(error)
            )

    # =====================================================
    # VIDER LES CHAMPS
    # =====================================================

    def vider_champs(self):

        if self.cmbProduit.count() > 0:

            self.cmbProduit.setCurrentIndex(0)

        self.txtQuantite.clear()

        self.txtClient.clear()

        self.txtNumeroBon.clear()

        self.txtCommentaire.clear()
