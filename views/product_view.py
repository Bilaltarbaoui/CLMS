from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from PySide6.QtGui import QIntValidator

from controllers.product_controller import ProductController


class ProductView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = ProductController()

        self.id_produit = None

        # =====================================================
        # CHAMPS PRODUIT
        # =====================================================

        self.txtReference = self.ui.findChild(
            QLineEdit,
            "txtReference"
        )

        self.txtNomProduit = self.ui.findChild(
            QLineEdit,
            "txtNomProduit"
        )

        self.txtCategorie = self.ui.findChild(
            QLineEdit,
            "txtCategorie"
        )

        self.txtMarque = self.ui.findChild(
            QLineEdit,
            "txtMarque"
        )

        self.txtUnite = self.ui.findChild(
            QLineEdit,
            "txtUnite"
        )

        self.txtStock = self.ui.findChild(
            QLineEdit,
            "txtStock"
        )

        self.txtStockMin = self.ui.findChild(
            QLineEdit,
            "txtStockMin"
        )

        self.txtNumeroLot = self.ui.findChild(
            QLineEdit,
            "txtNumeroLot"
        )

        self.txtDLC = self.ui.findChild(
            QLineEdit,
            "txtDLC"
        )

        self.txtFournisseur = self.ui.findChild(
            QLineEdit,
            "txtFournisseur"
        )

        self.txtDescription = self.ui.findChild(
            QLineEdit,
            "txtDescription"
        )

        self.txtDateReception = self.ui.findChild(
            QLineEdit,
            "txtDateReception"
        )

        self.txtDateLivraison = self.ui.findChild(
            QLineEdit,
            "txtDateLivraison"
        )

        # =====================================================
        # CHAMP RECHERCHE
        # =====================================================

        self.txtRechercheProduit = self.ui.findChild(
            QLineEdit,
            "txtRechercheProduit"
        )

        # =====================================================
        # BOUTONS
        # =====================================================

        self.btnAjouterProduit = self.ui.findChild(
            QPushButton,
            "btnAjouterProduit"
        )

        self.btnModifierProduit = self.ui.findChild(
            QPushButton,
            "btnModifierProduit"
        )

        self.btnSupprimerProduit = self.ui.findChild(
            QPushButton,
            "btnSupprimerProduit"
        )

        self.btnRechercherProduit = self.ui.findChild(
            QPushButton,
            "btnRechercherProduit"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableProduit = self.ui.findChild(
            QTableWidget,
            "tableProduit"
        )

        # =====================================================
        # VERIFICATION DES WIDGETS
        # =====================================================

        widgets = {
            "txtReference": self.txtReference,
            "txtNomProduit": self.txtNomProduit,
            "txtCategorie": self.txtCategorie,
            "txtMarque": self.txtMarque,
            "txtUnite": self.txtUnite,
            "txtStock": self.txtStock,
            "txtStockMin": self.txtStockMin,
            "txtNumeroLot": self.txtNumeroLot,
            "txtDLC": self.txtDLC,
            "txtFournisseur": self.txtFournisseur,
            "txtDescription": self.txtDescription,
            "txtDateReception": self.txtDateReception,
            "txtDateLivraison": self.txtDateLivraison,
            "txtRechercheProduit": self.txtRechercheProduit,
            "btnAjouterProduit": self.btnAjouterProduit,
            "btnModifierProduit": self.btnModifierProduit,
            "btnSupprimerProduit": self.btnSupprimerProduit,
            "btnRechercherProduit": self.btnRechercherProduit,
            "tableProduit": self.tableProduit
        }

        for nom, widget in widgets.items():

            if widget is None:

                print(
                    f"ERREUR : widget introuvable -> {nom}"
                )

        # =====================================================
        # VALIDATION DES STOCKS
        # =====================================================

        if self.txtStock:

            self.txtStock.setValidator(
                QIntValidator(
                    0,
                    999999999,
                    self.txtStock
                )
            )

        if self.txtStockMin:

            self.txtStockMin.setValidator(
                QIntValidator(
                    0,
                    999999999,
                    self.txtStockMin
                )
            )

        # =====================================================
        # CONFIGURATION TABLEAU
        # =====================================================

        if self.tableProduit:

            self.tableProduit.setColumnCount(15)

            self.tableProduit.setHorizontalHeaderLabels([
                "ID",
                "Référence",
                "Produit",
                "Catégorie",
                "Marque",
                "Unité",
                "Stock",
                "Stock minimum",
                "N° Lot",
                "DLC",
                "Fournisseur",
                "Description",
                "État",
                "Date réception",
                "Date livraison"
            ])

        # =====================================================
        # CONNEXIONS DES BOUTONS
        # =====================================================

        if self.btnAjouterProduit:

            self.btnAjouterProduit.clicked.connect(
                self.ajouter_produit
            )

        if self.btnModifierProduit:

            self.btnModifierProduit.clicked.connect(
                self.modifier_produit
            )

        if self.btnSupprimerProduit:

            self.btnSupprimerProduit.clicked.connect(
                self.supprimer_produit
            )

        if self.btnRechercherProduit:

            self.btnRechercherProduit.clicked.connect(
                self.rechercher_produit
            )

        # =====================================================
        # CONNEXION TABLEAU
        # =====================================================

        if self.tableProduit:

            self.tableProduit.cellClicked.connect(
                self.selectionner_produit
            )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_produits()

        print("PRODUCT VIEW = OK")

    # =====================================================
    # AJOUTER PRODUIT
    # =====================================================

    def ajouter_produit(self):

        print(">>> AJOUTER PRODUIT")

        # =================================================
        # VERIFICATION DU NOM
        # =================================================

        nom = self.txtNomProduit.text().strip()

        if nom == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir le nom du produit."
            )

            return

        # =================================================
        # RECUPERATION DU STOCK
        # =================================================

        stock = self.txtStock.text().strip()

        stock_min = self.txtStockMin.text().strip()

        if stock == "":
            stock = "0"

        if stock_min == "":
            stock_min = "0"

        # =================================================
        # AJOUT DANS LA BASE
        # =================================================

        try:

            self.controller.ajouter_produit(

                self.txtReference.text().strip(),

                nom,

                self.txtCategorie.text().strip(),

                self.txtMarque.text().strip(),

                self.txtUnite.text().strip(),

                stock,

                stock_min,

                self.txtNumeroLot.text().strip(),

                self.txtDLC.text().strip(),

                self.txtFournisseur.text().strip(),

                self.txtDescription.text().strip(),

                self.txtDateReception.text().strip(),

                self.txtDateLivraison.text().strip()
            )

        except Exception as e:

            QMessageBox.critical(
                self.ui,
                "Erreur",
                f"Impossible d'ajouter le produit.\n\n{e}"
            )

            print(
                "ERREUR AJOUT PRODUIT =",
                e
            )

            return

        # =================================================
        # MESSAGE SUCCES
        # =================================================

        QMessageBox.information(
            self.ui,
            "Succès",
            "Produit ajouté avec succès."
        )

        # =================================================
        # NETTOYAGE
        # =================================================

        self.vider_champs()

        # =================================================
        # ACTUALISATION
        # =================================================

        self.charger_produits()

    # =====================================================
    # CHARGER PRODUITS
    # =====================================================

    def charger_produits(self):

        print(">>> CHARGEMENT PRODUITS")

        try:

            produits = self.controller.get_all_products()

        except Exception as e:

            print(
                "ERREUR CHARGEMENT PRODUITS =",
                e
            )

            QMessageBox.critical(
                self.ui,
                "Erreur",
                f"Impossible de charger les produits.\n\n{e}"
            )

            return

        self.tableProduit.setRowCount(0)

        # =================================================
        # PARCOURIR LES PRODUITS
        # =================================================

        for ligne, produit in enumerate(produits):

            self.tableProduit.insertRow(ligne)

            # =============================================
            # STRUCTURE PRODUIT
            # =============================================

            id_produit = produit[0]
            reference = produit[1]
            nom = produit[2]
            categorie = produit[3]
            marque = produit[4]
            unite = produit[5]
            stock = produit[6]
            stock_min = produit[7]
            numero_lot = produit[8]
            dlc = produit[9]
            fournisseur = produit[10]
            description = produit[11]
            date_reception = produit[12]
            date_livraison = produit[13]

            # =============================================
            # ETAT DU STOCK
            # =============================================

            try:

                stock_int = int(stock)

            except (ValueError, TypeError):

                stock_int = 0

            try:

                stock_min_int = int(stock_min)

            except (ValueError, TypeError):

                stock_min_int = 0

            if stock_int == 0:

                etat = "🔴 Rupture"

            elif stock_int <= stock_min_int:

                etat = "🟠 Stock faible"

            else:

                etat = "🟢 Normal"

            # =============================================
            # DONNEES A AFFICHER
            # =============================================

            valeurs = [

                id_produit,

                reference,

                nom,

                categorie,

                marque,

                unite,

                stock,

                stock_min,

                numero_lot,

                dlc,

                fournisseur,

                description,

                etat,

                date_reception,

                date_livraison
            ]

            # =============================================
            # AFFICHAGE
            # =============================================

            for colonne, valeur in enumerate(valeurs):

                self.tableProduit.setItem(

                    ligne,

                    colonne,

                    QTableWidgetItem(
                        str(valeur if valeur is not None else "")
                    )
                )

        print(
            "PRODUITS CHARGES =",
            len(produits)
        )

    # =====================================================
    # SELECTIONNER PRODUIT
    # =====================================================

    def selectionner_produit(
        self,
        row,
        column
    ):

        print(
            ">>> PRODUIT SELECTIONNE :",
            row
        )

        # =================================================
        # RECUPERATION ID
        # =================================================

        item_id = self.tableProduit.item(
            row,
            0
        )

        if item_id is None:

            return

        try:

            self.id_produit = int(
                item_id.text()
            )

        except ValueError:

            QMessageBox.warning(
                self.ui,
                "Erreur",
                "ID du produit invalide."
            )

            return

        # =================================================
        # FONCTION POUR RECUPERER UNE CELLULE
        # =================================================

        def valeur(colonne):

            item = self.tableProduit.item(
                row,
                colonne
            )

            if item is None:

                return ""

            return item.text()

        # =================================================
        # REMPLISSAGE DES CHAMPS
        # =================================================

        self.txtReference.setText(
            valeur(1)
        )

        self.txtNomProduit.setText(
            valeur(2)
        )

        self.txtCategorie.setText(
            valeur(3)
        )

        self.txtMarque.setText(
            valeur(4)
        )

        self.txtUnite.setText(
            valeur(5)
        )

        self.txtStock.setText(
            valeur(6)
        )

        self.txtStockMin.setText(
            valeur(7)
        )

        self.txtNumeroLot.setText(
            valeur(8)
        )

        self.txtDLC.setText(
            valeur(9)
        )

        self.txtFournisseur.setText(
            valeur(10)
        )

        self.txtDescription.setText(
            valeur(11)
        )

        self.txtDateReception.setText(
            valeur(13)
        )

        self.txtDateLivraison.setText(
            valeur(14)
        )

        print(
            "PRODUIT ID SELECTIONNE =",
            self.id_produit
        )

    # =====================================================
    # MODIFIER PRODUIT
    # =====================================================

    def modifier_produit(self):

        print(">>> MODIFIER PRODUIT")

        # =================================================
        # VERIFICATION SELECTION
        # =================================================

        if self.id_produit is None:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Sélectionnez un produit à modifier."
            )

            return

        # =================================================
        # VERIFICATION NOM
        # =================================================

        nom = self.txtNomProduit.text().strip()

        if nom == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir le nom du produit."
            )

            return

        # =================================================
        # STOCK
        # =================================================

        stock = self.txtStock.text().strip()

        stock_min = self.txtStockMin.text().strip()

        if stock == "":
            stock = "0"

        if stock_min == "":
            stock_min = "0"

        # =================================================
        # MODIFICATION
        # =================================================

        try:

            self.controller.modifier_produit(

                self.id_produit,

                self.txtReference.text().strip(),

                nom,

                self.txtCategorie.text().strip(),

                self.txtMarque.text().strip(),

                self.txtUnite.text().strip(),

                stock,

                stock_min,

                self.txtNumeroLot.text().strip(),

                self.txtDLC.text().strip(),

                self.txtFournisseur.text().strip(),

                self.txtDescription.text().strip(),

                self.txtDateReception.text().strip(),

                self.txtDateLivraison.text().strip()
            )

        except Exception as e:

            QMessageBox.critical(
                self.ui,
                "Erreur",
                f"Impossible de modifier le produit.\n\n{e}"
            )

            print(
                "ERREUR MODIFICATION =",
                e
            )

            return

        # =================================================
        # MESSAGE
        # =================================================

        QMessageBox.information(
            self.ui,
            "Succès",
            "Produit modifié avec succès."
        )

        # =================================================
        # NETTOYAGE
        # =================================================

        self.vider_champs()

        # =================================================
        # ACTUALISATION
        # =================================================

        self.charger_produits()

    # =====================================================
    # SUPPRIMER PRODUIT
    # =====================================================

    def supprimer_produit(self):

        print(">>> SUPPRIMER PRODUIT")

        # =================================================
        # VERIFICATION SELECTION
        # =================================================

        if self.id_produit is None:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Sélectionnez un produit."
            )

            return

        # =================================================
        # CONFIRMATION
        # =================================================

        confirmation = QMessageBox.question(

            self.ui,

            "Confirmation",

            "Voulez-vous vraiment supprimer ce produit ?",

            QMessageBox.Yes |
            QMessageBox.No,

            QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:

            print(
                "SUPPRESSION ANNULEE"
            )

            return

        # =================================================
        # SUPPRESSION
        # =================================================

        try:

            self.controller.supprimer_produit(
                self.id_produit
            )

        except Exception as e:

            QMessageBox.critical(
                self.ui,
                "Erreur",
                f"Impossible de supprimer le produit.\n\n{e}"
            )

            print(
                "ERREUR SUPPRESSION =",
                e
            )

            return

        # =================================================
        # MESSAGE SUCCES
        # =================================================

        QMessageBox.information(
            self.ui,
            "Succès",
            "Produit supprimé avec succès."
        )

        # =================================================
        # NETTOYAGE
        # =================================================

        self.vider_champs()

        # =================================================
        # ACTUALISATION
        # =================================================

        self.charger_produits()

    # =====================================================
    # RECHERCHER PRODUIT
    # =====================================================

    def rechercher_produit(self):

        print(">>> RECHERCHE PRODUIT")

        mot = self.txtRechercheProduit.text().strip()

        print(
            "MOT RECHERCHE :",
            mot
        )

        # =================================================
        # RECHERCHE VIDE
        # =================================================

        if mot == "":

            print(
                "RECHERCHE VIDE"
            )

            self.charger_produits()

            return

        # =================================================
        # RECHERCHE DATABASE
        # =================================================

        try:

            produits = self.controller.rechercher_produit(
                mot
            )

        except Exception as e:

            QMessageBox.critical(
                self.ui,
                "Erreur",
                f"Erreur pendant la recherche.\n\n{e}"
            )

            print(
                "ERREUR RECHERCHE =",
                e
            )

            return

        print(
            "RESULTATS :",
            len(produits)
        )

        # =================================================
        # VIDER TABLEAU
        # =================================================

        self.tableProduit.setRowCount(0)

        # =================================================
        # AFFICHER RESULTATS
        # =================================================

        for ligne, produit in enumerate(produits):

            self.tableProduit.insertRow(
                ligne
            )

            # =============================================
            # STRUCTURE PRODUIT
            # =============================================

            id_produit = produit[0]
            reference = produit[1]
            nom = produit[2]
            categorie = produit[3]
            marque = produit[4]
            unite = produit[5]
            stock = produit[6]
            stock_min = produit[7]
            numero_lot = produit[8]
            dlc = produit[9]
            fournisseur = produit[10]
            description = produit[11]
            date_reception = produit[12]
            date_livraison = produit[13]

            # =============================================
            # ETAT
            # =============================================

            try:

                stock_int = int(stock)

            except (ValueError, TypeError):

                stock_int = 0

            try:

                stock_min_int = int(stock_min)

            except (ValueError, TypeError):

                stock_min_int = 0

            if stock_int == 0:

                etat = "🔴 Rupture"

            elif stock_int <= stock_min_int:

                etat = "🟠 Stock faible"

            else:

                etat = "🟢 Normal"

            # =============================================
            # VALEURS
            # =============================================

            valeurs = [

                id_produit,

                reference,

                nom,

                categorie,

                marque,

                unite,

                stock,

                stock_min,

                numero_lot,

                dlc,

                fournisseur,

                description,

                etat,

                date_reception,

                date_livraison
            ]

            # =============================================
            # AFFICHAGE
            # =============================================

            for colonne, valeur in enumerate(valeurs):

                self.tableProduit.setItem(

                    ligne,

                    colonne,

                    QTableWidgetItem(
                        str(
                            valeur
                            if valeur is not None
                            else ""
                        )
                    )
                )

        print(
            "RECHERCHE TERMINEE"
        )

    # =====================================================
    # VIDER LES CHAMPS
    # =====================================================

    def vider_champs(self):

        print(">>> VIDER CHAMPS")

        self.id_produit = None

        # =================================================
        # CHAMPS PRODUIT
        # =================================================

        self.txtReference.clear()

        self.txtNomProduit.clear()

        self.txtCategorie.clear()

        self.txtMarque.clear()

        self.txtUnite.clear()

        self.txtStock.clear()

        self.txtStockMin.clear()

        self.txtNumeroLot.clear()

        self.txtDLC.clear()

        self.txtFournisseur.clear()

        self.txtDescription.clear()

        self.txtDateReception.clear()

        self.txtDateLivraison.clear()

        print(
            "CHAMPS VIDES = OK"
        )