from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from controllers.client_controller import ClientController


class ClientView:

    def __init__(self, ui):

        self.ui = ui

        self.controller = ClientController()

        self.id_client = None

        # =====================================================
        # CHAMPS
        # =====================================================

        self.txtNom = self.ui.findChild(
            QLineEdit,
            "txtNom"
        )

        self.txtTelephone = self.ui.findChild(
            QLineEdit,
            "txtTelephone"
        )

        self.txtAdresse = self.ui.findChild(
            QLineEdit,
            "txtAdresse"
        )

        self.txtEmail = self.ui.findChild(
            QLineEdit,
            "txtEmail"
        )

        self.txtVille = self.ui.findChild(
            QLineEdit,
            "txtVille"
        )

        self.txtRecherche = self.ui.findChild(
            QLineEdit,
            "txtRecherche"
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

        self.btnRechercher = self.ui.findChild(
            QPushButton,
            "btnRechercher"
        )

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableWidget = self.ui.findChild(
            QTableWidget,
            "tableWidget"
        )

        # =====================================================
        # CONNEXIONS
        # =====================================================

        self.btnAjouter.clicked.connect(
            self.ajouter_client
        )

        self.btnModifier.clicked.connect(
            self.modifier_client
        )

        self.btnSupprimer.clicked.connect(
            self.supprimer_client
        )

        self.btnRechercher.clicked.connect(
            self.rechercher_client
        )

        self.tableWidget.cellClicked.connect(
            self.selectionner_client
        )

        # =====================================================
        # CHARGEMENT INITIAL
        # =====================================================

        self.charger_clients()

    # =========================================================
    # VIDER LES CHAMPS
    # =========================================================

    def vider_champs(self):

        self.id_client = None

        self.txtNom.clear()
        self.txtTelephone.clear()
        self.txtAdresse.clear()
        self.txtEmail.clear()
        self.txtVille.clear()

    # =========================================================
    # AJOUTER CLIENT
    # =========================================================

    def ajouter_client(self):

        self.controller.ajouter_client(
            self.txtNom.text(),
            self.txtTelephone.text(),
            self.txtAdresse.text(),
            self.txtEmail.text(),
            self.txtVille.text()
        )

        self.vider_champs()

        self.charger_clients()

    # =========================================================
    # CHARGER CLIENTS
    # =========================================================

    def charger_clients(self):

        clients = self.controller.get_all_clients()

        self.tableWidget.setRowCount(0)

        for ligne, client in enumerate(clients):

            self.tableWidget.insertRow(ligne)

            for colonne, valeur in enumerate(client):

                self.tableWidget.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

    # =========================================================
    # SELECTIONNER CLIENT
    # =========================================================

    def selectionner_client(
        self,
        row,
        column
    ):

        self.id_client = int(
            self.tableWidget.item(
                row,
                0
            ).text()
        )

        self.txtNom.setText(
            self.tableWidget.item(
                row,
                1
            ).text()
        )

        self.txtTelephone.setText(
            self.tableWidget.item(
                row,
                2
            ).text()
        )

        self.txtAdresse.setText(
            self.tableWidget.item(
                row,
                3
            ).text()
        )

        self.txtEmail.setText(
            self.tableWidget.item(
                row,
                4
            ).text()
        )

        self.txtVille.setText(
            self.tableWidget.item(
                row,
                5
            ).text()
        )

    # =========================================================
    # MODIFIER CLIENT
    # =========================================================

    def modifier_client(self):

        if self.id_client is None:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Sélectionnez un client."
            )

            return

        self.controller.modifier_client(
            self.id_client,
            self.txtNom.text(),
            self.txtTelephone.text(),
            self.txtAdresse.text(),
            self.txtEmail.text(),
            self.txtVille.text()
        )

        self.vider_champs()

        self.charger_clients()

    # =========================================================
    # SUPPRIMER CLIENT
    # =========================================================

    def supprimer_client(self):

        if self.id_client is None:

            QMessageBox.warning(
                self.ui,
                "Attention",
                "Sélectionnez un client."
            )

            return

        confirmation = QMessageBox.question(
            self.ui,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce client ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.No:

            return

        self.controller.supprimer_client(
            self.id_client
        )

        self.vider_champs()

        self.charger_clients()

    # =========================================================
    # RECHERCHER CLIENT
    # =========================================================

    def rechercher_client(self):

        print("RECHERCHE = OK")

        mot = self.txtRecherche.text().strip()

        print(
            "MOT RECHERCHE :",
            mot
        )

        if mot == "":

            print("RECHERCHE VIDE")

            self.charger_clients()

            return

        clients = self.controller.rechercher_client(
            mot
        )

        print(
            "RESULTAT RECHERCHE :",
            clients
        )

        self.tableWidget.setRowCount(0)

        for ligne, client in enumerate(clients):

            self.tableWidget.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(client):

                self.tableWidget.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        print("RECHERCHE TERMINEE")