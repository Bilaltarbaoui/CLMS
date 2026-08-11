from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from PySide6.QtCore import Qt

from controllers.vehicle_controller import VehicleController


class VehicleView:

    def __init__(self, ui):

        print("VEHICLE VIEW START")

        self.ui = ui

        # =====================================================
        # CONTROLLER
        # =====================================================

        self.controller = VehicleController()

        print("VEHICLE CONTROLLER = OK")

        # =====================================================
        # CHAMPS
        # =====================================================

        self.txtMatricule = self.ui.findChild(
            QLineEdit,
            "txtMatricule"
        )

        self.cmbType = self.ui.findChild(
            QComboBox,
            "cmbType"
        )

        self.txtMarque = self.ui.findChild(
            QLineEdit,
            "txtMarque"
        )

        self.txtModele = self.ui.findChild(
            QLineEdit,
            "txtModele"
        )

        self.txtKilometrage = self.ui.findChild(
            QLineEdit,
            "txtKilometrage"
        )

        self.cmbEtat = self.ui.findChild(
            QComboBox,
            "cmbEtat"
        )

        self.txtObservation = self.ui.findChild(
            QLineEdit,
            "txtObservation"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableVehicules = self.ui.findChild(
            QTableWidget,
            "tableVehicules"
        )

        if self.tableVehicules is None:

            print("ERREUR : tableVehicules introuvable")

            return

        print("TABLE VEHICULES = OK")

        # =====================================================
        # CONFIGURATION TABLEAU
        # =====================================================

        self.tableVehicules.setColumnCount(8)

        self.tableVehicules.setHorizontalHeaderLabels([
            "ID",
            "Matricule",
            "Type",
            "Marque",
            "Modèle",
            "Kilométrage",
            "État",
            "Observation"
        ])

        self.tableVehicules.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tableVehicules.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.tableVehicules.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.tableVehicules.setAlternatingRowColors(
            True
        )

        # =====================================================
        # BOUTONS
        # =====================================================

        self.btnAjouter = self.ui.findChild(
            QPushButton,
            "btnAjouter"
        )

        self.btnModifier = self.ui.findChild(
            QPushButton,
            "btnModifier"
        )

        self.btnSupprimer = self.ui.findChild(
            QPushButton,
            "btnSupprimer"
        )

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        # =====================================================
        # VERIFICATION BOUTONS
        # =====================================================

        print(
            "BTN AJOUTER =",
            "OK" if self.btnAjouter else "ERREUR"
        )

        print(
            "BTN MODIFIER =",
            "OK" if self.btnModifier else "ERREUR"
        )

        print(
            "BTN SUPPRIMER =",
            "OK" if self.btnSupprimer else "ERREUR"
        )

        print(
            "BTN ACTUALISER =",
            "OK" if self.btnActualiser else "ERREUR"
        )

        # =====================================================
        # CONNEXIONS
        # =====================================================

        if self.btnAjouter:

            self.btnAjouter.clicked.connect(
                self.ajouter
            )

        if self.btnModifier:

            self.btnModifier.clicked.connect(
                self.modifier
            )

        if self.btnSupprimer:

            self.btnSupprimer.clicked.connect(
                self.supprimer
            )

        if self.btnActualiser:

            self.btnActualiser.clicked.connect(
                self.charger_vehicules
            )

        self.tableVehicules.itemSelectionChanged.connect(
            self.selectionner_vehicule
        )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_vehicules()

        print("VEHICLE VIEW = OK")

    # =========================================================
    # CHARGER VEHICULES
    # =========================================================

    def charger_vehicules(self):

        print(">>> CHARGEMENT VEHICULES")

        try:

            vehicules = self.controller.get_all()

            print(
                ">>> VEHICULES CHARGES =",
                len(vehicules)
            )

            # Afficher chaque véhicule dans le terminal
            for vehicule in vehicules:

                print(
                    "VEHICULE :",
                    vehicule
                )

            self.afficher_vehicules(
                vehicules
            )

        except Exception as error:

            print(
                "ERREUR CHARGEMENT VEHICULES :",
                error
            )

            QMessageBox.critical(
                self.ui,
                "Erreur",
                str(error)
            )

    # =========================================================
    # AFFICHER VEHICULES
    # =========================================================

    def afficher_vehicules(
        self,
        vehicules
    ):

        print(
            ">>> AFFICHAGE TABLE VEHICULES"
        )

        # -----------------------------------------------------
        # Vérifier tableau
        # -----------------------------------------------------

        if self.tableVehicules is None:

            print(
                "ERREUR : tableau véhicules introuvable"
            )

            return

        # -----------------------------------------------------
        # Configuration
        # -----------------------------------------------------

        self.tableVehicules.setColumnCount(8)

        self.tableVehicules.setRowCount(0)

        # -----------------------------------------------------
        # Ajouter les lignes
        # -----------------------------------------------------

        for ligne, vehicule in enumerate(
            vehicules
        ):

            print(
                ">>> LIGNE =",
                ligne,
                "|",
                vehicule
            )

            self.tableVehicules.insertRow(
                ligne
            )

            # -------------------------------------------------
            # Vérifier structure
            # -------------------------------------------------

            if len(vehicule) < 8:

                print(
                    "ERREUR : véhicule incomplet =",
                    vehicule
                )

                continue

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(vehicule[0])
                )
            )

            # -------------------------------------------------
            # MATRICULE
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(vehicule[1])
                )
            )

            # -------------------------------------------------
            # TYPE
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    str(vehicule[2])
                )
            )

            # -------------------------------------------------
            # MARQUE
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                3,
                QTableWidgetItem(
                    str(vehicule[3])
                )
            )

            # -------------------------------------------------
            # MODELE
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                4,
                QTableWidgetItem(
                    str(vehicule[4])
                )
            )

            # -------------------------------------------------
            # KILOMETRAGE
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                5,
                QTableWidgetItem(
                    str(vehicule[5])
                )
            )

            # -------------------------------------------------
            # ETAT
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                6,
                QTableWidgetItem(
                    str(vehicule[6])
                )
            )

            # -------------------------------------------------
            # OBSERVATION
            # -------------------------------------------------

            self.tableVehicules.setItem(
                ligne,
                7,
                QTableWidgetItem(
                    str(vehicule[7])
                )
            )

        # -----------------------------------------------------
        # Ajuster colonnes
        # -----------------------------------------------------

        self.tableVehicules.resizeColumnsToContents()

        # Garder une largeur minimum
        for colonne in range(8):

            if self.tableVehicules.columnWidth(
                colonne
            ) < 80:

                self.tableVehicules.setColumnWidth(
                    colonne,
                    80
                )

        print(
            ">>> TABLEAU REMPLI =",
            self.tableVehicules.rowCount(),
            "lignes"
        )

    # =========================================================
    # AJOUTER VEHICULE
    # =========================================================

    def ajouter(self):

        print(">>> AJOUTER VEHICULE")

        matricule = (
            self.txtMatricule.text()
            .strip()
        )

        type_vehicule = (
            self.cmbType.currentText()
            .strip()
        )

        marque = (
            self.txtMarque.text()
            .strip()
        )

        modele = (
            self.txtModele.text()
            .strip()
        )

        kilometrage_text = (
            self.txtKilometrage.text()
            .strip()
        )

        etat = (
            self.cmbEtat.currentText()
            .strip()
        )

        observation = (
            self.txtObservation.text()
            .strip()
        )

        # -----------------------------------------------------
        # MATRICULE
        # -----------------------------------------------------

        if matricule == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir la matricule."
            )

            return

        # -----------------------------------------------------
        # KILOMETRAGE
        # -----------------------------------------------------

        if kilometrage_text == "":

            kilometrage = 0

        else:

            try:

                kilometrage = float(
                    kilometrage_text
                )

            except ValueError:

                QMessageBox.warning(
                    self.ui,
                    "Attention",
                    "Le kilométrage doit être un nombre."
                )

                return

        if kilometrage < 0:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Le kilométrage ne peut pas être négatif."
            )

            return

        # -----------------------------------------------------
        # AJOUT
        # -----------------------------------------------------

        try:

            self.controller.ajouter(

                matricule,
                type_vehicule,
                marque,
                modele,
                kilometrage,
                etat,
                observation

            )

            print(
                ">>> VEHICULE AJOUTE =",
                matricule
            )

            QMessageBox.information(
                self.ui,
                "Succès",
                "Véhicule ajouté avec succès."
            )

            self.charger_vehicules()

            self.vider_formulaire()

        except Exception as error:

            print(
                "ERREUR AJOUT VEHICULE :",
                error
            )

            QMessageBox.critical(
                self.ui,
                "Erreur",
                str(error)
            )

    # =========================================================
    # SELECTIONNER VEHICULE
    # =========================================================

    def selectionner_vehicule(self):

        ligne = (
            self.tableVehicules.currentRow()
        )

        if ligne < 0:

            return

        print(
            ">>> VEHICULE SELECTIONNE :",
            ligne
        )

        # ID
        item = self.tableVehicules.item(
            ligne,
            0
        )

        # MATRICULE
        item = self.tableVehicules.item(
            ligne,
            1
        )

        if item:

            self.txtMatricule.setText(
                item.text()
            )

        # TYPE
        item = self.tableVehicules.item(
            ligne,
            2
        )

        if item:

            self.cmbType.setCurrentText(
                item.text()
            )

        # MARQUE
        item = self.tableVehicules.item(
            ligne,
            3
        )

        if item:

            self.txtMarque.setText(
                item.text()
            )

        # MODELE
        item = self.tableVehicules.item(
            ligne,
            4
        )

        if item:

            self.txtModele.setText(
                item.text()
            )

        # KILOMETRAGE
        item = self.tableVehicules.item(
            ligne,
            5
        )

        if item:

            self.txtKilometrage.setText(
                item.text()
            )

        # ETAT
        item = self.tableVehicules.item(
            ligne,
            6
        )

        if item:

            self.cmbEtat.setCurrentText(
                item.text()
            )

        # OBSERVATION
        item = self.tableVehicules.item(
            ligne,
            7
        )

        if item:

            self.txtObservation.setText(
                item.text()
            )

    # =========================================================
    # MODIFIER
    # =========================================================

    def modifier(self):

        ligne = (
            self.tableVehicules.currentRow()
        )

        if ligne < 0:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez sélectionner un véhicule."
            )

            return

        item_id = self.tableVehicules.item(
            ligne,
            0
        )

        if item_id is None:

            return

        try:

            id_vehicule = int(
                item_id.text()
            )

        except ValueError:

            return

        matricule = (
            self.txtMatricule.text()
            .strip()
        )

        type_vehicule = (
            self.cmbType.currentText()
            .strip()
        )

        marque = (
            self.txtMarque.text()
            .strip()
        )

        modele = (
            self.txtModele.text()
            .strip()
        )

        kilometrage_text = (
            self.txtKilometrage.text()
            .strip()
        )

        etat = (
            self.cmbEtat.currentText()
            .strip()
        )

        observation = (
            self.txtObservation.text()
            .strip()
        )

        if matricule == "":

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez saisir la matricule."
            )

            return

        if kilometrage_text == "":

            kilometrage = 0

        else:

            try:

                kilometrage = float(
                    kilometrage_text
                )

            except ValueError:

                QMessageBox.warning(
                    self.ui,
                    "Attention",
                    "Kilométrage invalide."
                )

                return

        if kilometrage < 0:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Kilométrage invalide."
            )

            return

        try:

            self.controller.modifier(

                id_vehicule,
                matricule,
                type_vehicule,
                marque,
                modele,
                kilometrage,
                etat,
                observation

            )

            print(
                ">>> VEHICULE MODIFIE =",
                id_vehicule
            )

            QMessageBox.information(
                self.ui,
                "Succès",
                "Véhicule modifié avec succès."
            )

            self.charger_vehicules()

            self.vider_formulaire()

        except Exception as error:

            print(
                "ERREUR MODIFICATION :",
                error
            )

            QMessageBox.critical(
                self.ui,
                "Erreur",
                str(error)
            )

    # =========================================================
    # SUPPRIMER
    # =========================================================

    def supprimer(self):

        ligne = (
            self.tableVehicules.currentRow()
        )

        if ligne < 0:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Veuillez sélectionner un véhicule."
            )

            return

        item_id = self.tableVehicules.item(
            ligne,
            0
        )

        if item_id is None:

            return

        try:

            id_vehicule = int(
                item_id.text()
            )

        except ValueError:

            return

        confirmation = QMessageBox.question(

            self.ui,

            "Confirmation",

            "Voulez-vous vraiment supprimer ce véhicule ?",

            QMessageBox.Yes |
            QMessageBox.No

        )

        if confirmation != QMessageBox.Yes:

            return

        try:

            self.controller.supprimer(
                id_vehicule
            )

            print(
                ">>> VEHICULE SUPPRIME =",
                id_vehicule
            )

            QMessageBox.information(
                self.ui,
                "Succès",
                "Véhicule supprimé avec succès."
            )

            self.charger_vehicules()

            self.vider_formulaire()

        except Exception as error:

            print(
                "ERREUR SUPPRESSION :",
                error
            )

            QMessageBox.critical(
                self.ui,
                "Erreur",
                str(error)
            )

    # =========================================================
    # VIDER FORMULAIRE
    # =========================================================

    def vider_formulaire(self):

        self.txtMatricule.clear()

        self.txtMarque.clear()

        self.txtModele.clear()

        self.txtKilometrage.clear()

        self.txtObservation.clear()

        if self.cmbType.count() > 0:

            self.cmbType.setCurrentIndex(0)

        if self.cmbEtat.count() > 0:

            self.cmbEtat.setCurrentIndex(0)

        self.tableVehicules.clearSelection()

        print(
            "FORMULAIRE VEHICULE VIDE = OK"
        )

    # =========================================================
    # FERMER
    # =========================================================

    def close(self):

        try:

            self.controller.close()

        except Exception as error:

            print(
                "ERREUR FERMETURE VEHICULE :",
                error
            )

        print(
            "VEHICLE VIEW CLOSED"
        )
