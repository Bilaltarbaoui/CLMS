from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from PySide6.QtGui import QIntValidator

from controllers.entry_controller import EntryController
from controllers.product_controller import ProductController


class EntryView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = EntryController()

        self.product_controller = ProductController()

        # =====================================================
        # CHAMPS
        # =====================================================

        self.cmbProduit = self.ui.findChild(
            QComboBox,
            "cmbProduit"
        )

        self.txtQuantite = self.ui.findChild(
            QLineEdit,
            "txtQuantite"
        )

        self.txtFournisseur = self.ui.findChild(
            QLineEdit,
            "txtFournisseur"
        )

        self.txtNumeroBon = self.ui.findChild(
            QLineEdit,
            "txtNumeroBon"
        )

        self.txtCommentaire = self.ui.findChild(
            QTextEdit,
            "txtCommentaire"
        )

        # =====================================================
        # BOUTONS
        # =====================================================

        self.btnAjouterEntree = self.ui.findChild(
            QPushButton,
            "btnAjouterEntree"
        )

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableEntrees = self.ui.findChild(
            QTableWidget,
            "tableEntrees"
        )

        # =====================================================
        # VALIDATION QUANTITE
        # =====================================================

        self.txtQuantite.setValidator(
            QIntValidator(
                1,
                999999999,
                self.txtQuantite
            )
        )

        # =====================================================
        # CONNEXIONS
        # =====================================================

        self.btnAjouterEntree.clicked.connect(
            self.ajouter_entree
        )

        self.btnActualiser.clicked.connect(
            self.actualiser
        )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_produits()

        self.charger_entrees()

        print("ENTRY VIEW = OK")

    # =====================================================
    # CHARGER PRODUITS
    # =====================================================

    def charger_produits(self):

        print(">>> CHARGEMENT PRODUITS POUR ENTREES")

        produits = self.product_controller.get_all_products()

        self.cmbProduit.clear()

        for produit in produits:

            # Structure products :
            #
            # 0 = id
            # 1 = reference
            # 2 = nom
            # 3 = categorie
            # ...

            product_id = produit[0]
            reference = produit[1]
            nom = produit[2]

            texte = f"{reference} - {nom}"

            self.cmbProduit.addItem(
                texte,
                product_id
            )

        print(
            "PRODUITS DANS COMBO =",
            len(produits)
        )

    # =====================================================
    # AJOUTER ENTREE
    # =====================================================

    def ajouter_entree(self):

        print(">>> AJOUTER ENTREE")

        # =================================================
        # VERIFIER PRODUIT
        # =================================================

        product_id = self.cmbProduit.currentData()

        if product_id is None:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez sélectionner un produit."
            )

            return

        # =================================================
        # VERIFIER QUANTITE
        # =================================================

        quantite = self.txtQuantite.text().strip()

        if quantite == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir une quantité."
            )

            return

        # =================================================
        # FOURNISSEUR
        # =================================================

        fournisseur = self.txtFournisseur.text().strip()

        # =================================================
        # NUMERO BON
        # =================================================

        numero_bon = self.txtNumeroBon.text().strip()

        # =================================================
        # COMMENTAIRE
        # =================================================

        commentaire = self.txtCommentaire.toPlainText().strip()

        # =================================================
        # ENREGISTREMENT
        # =================================================

        try:

            self.controller.ajouter_entree(
                product_id,
                quantite,
                fournisseur,
                numero_bon,
                commentaire
            )

        except Exception as error:

            QMessageBox.warning(
                self.ui,
                "Erreur",
                str(error)
            )

            print(
                "ERREUR AJOUT ENTREE :",
                error
            )

            return

        # =================================================
        # SUCCES
        # =================================================

        QMessageBox.information(
            self.ui,
            "Succès",
            "Entrée enregistrée avec succès."
        )

        # =================================================
        # NETTOYER
        # =================================================

        self.vider_champs()

        # =================================================
        # ACTUALISER TABLEAU
        # =================================================

        self.charger_entrees()

        # =================================================
        # ACTUALISER COMBO PRODUITS
        # =================================================

        self.charger_produits()

    # =====================================================
    # CHARGER ENTREES
    # =====================================================

    def charger_entrees(self):

        print(">>> CHARGEMENT ENTREES")

        entrees = self.controller.get_all_entries()

        self.tableEntrees.setRowCount(0)

        for ligne, entree in enumerate(entrees):

            self.tableEntrees.insertRow(ligne)

            for colonne, valeur in enumerate(entree):

                self.tableEntrees.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        print(
            "ENTREES CHARGEES =",
            len(entrees)
        )

    # =====================================================
    # ACTUALISER
    # =====================================================

    def actualiser(self):

        print(">>> ACTUALISATION ENTREES")

        self.charger_produits()

        self.charger_entrees()

        print("ACTUALISATION ENTREES = OK")

    # =====================================================
    # VIDER CHAMPS
    # =====================================================

    def vider_champs(self):

        self.txtQuantite.clear()

        self.txtFournisseur.clear()

        self.txtNumeroBon.clear()

        self.txtCommentaire.clear()

        # On remet le combo sur le premier produit

        if self.cmbProduit.count() > 0:

            self.cmbProduit.setCurrentIndex(0)

        print("CHAMPS ENTREE VIDES = OK")
