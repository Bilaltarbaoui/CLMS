from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDateEdit,
    QTimeEdit
)

from PySide6.QtCore import QDate, QTime

from controllers.gasoil_controller import GasoilController


class GasoilView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = GasoilController()

        # =====================================================
        # VEHICULE
        # =====================================================

        self.cmbVehicule = self.ui.findChild(
            QComboBox,
            "cmbVehicule"
        )

        # =====================================================
        # DATE
        # =====================================================

        self.dateOperation = self.ui.findChild(
            QDateEdit,
            "dateOperation"
        )

        # =====================================================
        # HEURE
        # =====================================================

        self.heureOperation = self.ui.findChild(
            QTimeEdit,
            "heureOperation"
        )

        # =====================================================
        # KILOMETRAGE
        # =====================================================

        self.txtKilometrage = self.ui.findChild(
            QLineEdit,
            "txtKilometrage"
        )

        # =====================================================
        # QUANTITE
        # =====================================================

        self.txtQuantite = self.ui.findChild(
            QLineEdit,
            "txtQuantite"
        )

        # =====================================================
        # OBSERVATION
        # =====================================================

        self.txtObservation = self.ui.findChild(
            QLineEdit,
            "Observation"
        )

        # =====================================================
        # RECHERCHE
        # =====================================================

        self.txtRecherche = self.ui.findChild(
            QLineEdit,
            "txtRecherche"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableGasoil = self.ui.findChild(
            QTableWidget,
            "tableGasoil"
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
        # DATE / HEURE PAR DEFAUT
        # =====================================================

        if self.dateOperation:
            self.dateOperation.setDate(
                QDate.currentDate()
            )

        if self.heureOperation:
            self.heureOperation.setTime(
                QTime.currentTime()
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
                self.actualiser
            )

        if self.txtRecherche:
            self.txtRecherche.textChanged.connect(
                self.rechercher
            )

        if self.tableGasoil:
            self.tableGasoil.itemSelectionChanged.connect(
                self.selectionner_gasoil
            )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_vehicules()
        self.charger_gasoil()

    # =====================================================
    # CHARGER VEHICULES
    # =====================================================

    def charger_vehicules(self):

        if not self.cmbVehicule:
            return

        try:
            vehicules = self.controller.get_vehicules()

        except Exception as e:

            print(
                "ERREUR CHARGEMENT VEHICULES :",
                e
            )

            return

        self.cmbVehicule.clear()

        for vehicule in vehicules:

            if len(vehicule) < 7:
                continue

            matricule = str(
                vehicule[1]
            ).strip()

            etat = str(
                vehicule[6]
            ).strip()

            if etat in (
                "Disponible",
                "En circulation"
            ):

                self.cmbVehicule.addItem(
                    matricule
                )

        print(
            "VEHICULES GASOIL =",
            self.cmbVehicule.count()
        )

    # =====================================================
    # AJOUTER
    # =====================================================

    def ajouter(self):

        if not self.cmbVehicule:
            return

        vehicule = (
            self.cmbVehicule
            .currentText()
            .strip()
        )

        if vehicule == "":

            print(
                "ERREUR : aucun véhicule sélectionné"
            )

            return

        date_operation = (
            self.dateOperation
            .date()
            .toString("yyyy-MM-dd")
        )

        heure_operation = (
            self.heureOperation
            .time()
            .toString("HH:mm:ss")
        )

        kilometrage_text = (
            self.txtKilometrage
            .text()
            .strip()
        )

        if kilometrage_text == "":
            kilometrage = 0

        else:

            try:
                kilometrage = float(
                    kilometrage_text
                )

            except ValueError:

                print(
                    "ERREUR : kilométrage invalide"
                )

                return

        quantite_text = (
            self.txtQuantite
            .text()
            .strip()
        )

        if quantite_text == "":

            print(
                "ERREUR : quantité vide"
            )

            return

        try:

            quantite = float(
                quantite_text
            )

        except ValueError:

            print(
                "ERREUR : quantité invalide"
            )

            return

        if quantite <= 0:

            print(
                "ERREUR : quantité doit être supérieure à 0"
            )

            return

        observation = (
            self.txtObservation
            .text()
            .strip()
        )

        try:

            self.controller.ajouter(
                vehicule,
                date_operation,
                heure_operation,
                kilometrage,
                quantite,
                observation
            )

        except Exception as e:

            print(
                "ERREUR AJOUT GASOIL :",
                e
            )

            return

        print(
            "GASOIL AJOUTE :",
            vehicule,
            "|",
            quantite,
            "L"
        )

        self.charger_gasoil()
        self.vider_formulaire()

    # =====================================================
    # CHARGER GASOIL
    # =====================================================

    def charger_gasoil(self):

        if not self.tableGasoil:
            return

        try:

            gasoil = self.controller.get_all()

        except Exception as e:

            print(
                "ERREUR CHARGEMENT GASOIL :",
                e
            )

            return

        self.afficher_gasoil(
            gasoil
        )

    # =====================================================
    # AFFICHER GASOIL
    # =====================================================

    def afficher_gasoil(
        self,
        gasoil
    ):

        self.tableGasoil.setRowCount(0)

        for ligne, operation in enumerate(
            gasoil
        ):

            self.tableGasoil.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(
                operation
            ):

                self.tableGasoil.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        self.tableGasoil.resizeColumnsToContents()

    # =====================================================
    # RECHERCHER
    # =====================================================

    def rechercher(self):

        if not self.txtRecherche:
            return

        recherche = (
            self.txtRecherche
            .text()
            .strip()
            .lower()
        )

        try:

            gasoil = self.controller.get_all()

        except Exception as e:

            print(
                "ERREUR RECHERCHE :",
                e
            )

            return

        if recherche == "":

            self.afficher_gasoil(
                gasoil
            )

            return

        resultats = []

        for operation in gasoil:

            texte = " ".join(
                str(valeur).lower()
                for valeur in operation
            )

            if recherche in texte:

                resultats.append(
                    operation
                )

        self.afficher_gasoil(
            resultats
        )

    # =====================================================
    # SELECTIONNER
    # =====================================================

    def selectionner_gasoil(self):

        if not self.tableGasoil:
            return

        ligne = self.tableGasoil.currentRow()

        if ligne < 0:
            return

        item = self.tableGasoil.item(
            ligne,
            1
        )

        if item:
            self.cmbVehicule.setCurrentText(
                item.text()
            )

        item = self.tableGasoil.item(
            ligne,
            2
        )

        if item:

            date = QDate.fromString(
                item.text(),
                "yyyy-MM-dd"
            )

            if date.isValid():
                self.dateOperation.setDate(
                    date
                )

        item = self.tableGasoil.item(
            ligne,
            3
        )

        if item:

            heure = QTime.fromString(
                item.text(),
                "HH:mm:ss"
            )

            if heure.isValid():
                self.heureOperation.setTime(
                    heure
                )

        item = self.tableGasoil.item(
            ligne,
            4
        )

        if item:
            self.txtKilometrage.setText(
                item.text()
            )

        item = self.tableGasoil.item(
            ligne,
            5
        )

        if item:
            self.txtQuantite.setText(
                item.text()
            )

        item = self.tableGasoil.item(
            ligne,
            6
        )

        if item:
            self.txtObservation.setText(
                item.text()
            )

    # =====================================================
    # MODIFIER
    # =====================================================

    def modifier(self):

        ligne = self.tableGasoil.currentRow()

        if ligne < 0:

            print(
                "Aucune opération sélectionnée"
            )

            return

        item = self.tableGasoil.item(
            ligne,
            0
        )

        if not item:
            return

        try:

            id_operation = int(
                item.text()
            )

        except ValueError:

            print(
                "ERREUR : ID invalide"
            )

            return

        vehicule = (
            self.cmbVehicule
            .currentText()
            .strip()
        )

        date_operation = (
            self.dateOperation
            .date()
            .toString("yyyy-MM-dd")
        )

        heure_operation = (
            self.heureOperation
            .time()
            .toString("HH:mm:ss")
        )

        kilometrage_text = (
            self.txtKilometrage
            .text()
            .strip()
        )

        if kilometrage_text == "":
            kilometrage = 0

        else:

            try:

                kilometrage = float(
                    kilometrage_text
                )

            except ValueError:

                print(
                    "ERREUR : kilométrage invalide"
                )

                return

        try:

            quantite = float(
                self.txtQuantite
                .text()
                .strip()
            )

        except ValueError:

            print(
                "ERREUR : quantité invalide"
            )

            return

        if quantite <= 0:

            print(
                "ERREUR : quantité invalide"
            )

            return

        observation = (
            self.txtObservation
            .text()
            .strip()
        )

        try:

            self.controller.modifier(
                id_operation,
                vehicule,
                date_operation,
                heure_operation,
                kilometrage,
                quantite,
                observation
            )

        except Exception as e:

            print(
                "ERREUR MODIFICATION GASOIL :",
                e
            )

            return

        print(
            "GASOIL MODIFIE =",
            id_operation
        )

        self.charger_gasoil()
        self.vider_formulaire()

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer(self):

        ligne = self.tableGasoil.currentRow()

        if ligne < 0:

            print(
                "Aucune opération sélectionnée"
            )

            return

        item = self.tableGasoil.item(
            ligne,
            0
        )

        if not item:
            return

        try:

            id_operation = int(
                item.text()
            )

        except ValueError:

            print(
                "ERREUR : ID invalide"
            )

            return

        try:

            self.controller.supprimer(
                id_operation
            )

        except Exception as e:

            print(
                "ERREUR SUPPRESSION GASOIL :",
                e
            )

            return

        print(
            "GASOIL SUPPRIME =",
            id_operation
        )

        self.charger_gasoil()
        self.vider_formulaire()

    # =====================================================
    # ACTUALISER
    # =====================================================

    def actualiser(self):

        self.charger_vehicules()
        self.charger_gasoil()

        print(
            "GASOIL ACTUALISE = OK"
        )

    # =====================================================
    # VIDER FORMULAIRE
    # =====================================================

    def vider_formulaire(self):

        if self.dateOperation:

            self.dateOperation.setDate(
                QDate.currentDate()
            )

        if self.heureOperation:

            self.heureOperation.setTime(
                QTime.currentTime()
            )

        if self.txtKilometrage:
            self.txtKilometrage.clear()

        if self.txtQuantite:
            self.txtQuantite.clear()

        if self.txtObservation:
            self.txtObservation.clear()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        try:

            self.controller.close()

        except Exception as e:

            print(
                "ERREUR FERMETURE GASOIL :",
                e
            )