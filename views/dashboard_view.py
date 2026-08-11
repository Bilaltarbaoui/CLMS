from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout
)

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis
)

from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

from controllers.product_controller import ProductController
from controllers.entry_controller import EntryController
from controllers.sortie_controller import SortieController
from controllers.vehicle_controller import VehicleController
from controllers.gasoil_controller import GasoilController


class DashboardView:

    def __init__(self, ui):

        print("DASHBOARD VIEW START")

        self.ui = ui

        # =====================================================
        # MODELS / CONTROLLERS
        # =====================================================

        self.product_controller = ProductController()
        self.entry_controller = EntryController()
        self.sortie_controller = SortieController()
        self.vehicle_controller = VehicleController()
        self.gasoil_controller = GasoilController()

        print("DASHBOARD MODELS = OK")

        # =====================================================
        # LABELS
        # =====================================================

        self.lblProduits = self.ui.findChild(
            QLabel,
            "lblProduits"
        )

        self.lblTotalEntrees = self.ui.findChild(
            QLabel,
            "lblTotalEntrees"
        )

        self.lblTotalSorties = self.ui.findChild(
            QLabel,
            "lblTotalSorties"
        )

        self.lblAlertes = self.ui.findChild(
            QLabel,
            "lblAlertes"
        )

        self.lblVehicules = self.ui.findChild(
            QLabel,
            "lblVehicules"
        )

        self.lblTotalGasoil = self.ui.findChild(
            QLabel,
            "lblTotalGasoil"
        )

        # =====================================================
        # GRAPHIQUE ENTREES / SORTIES
        # =====================================================

        self.chartEntreesSorties = self.ui.findChild(
            QWidget,
            "chartEntreesSorties"
        )

        if self.chartEntreesSorties:

            print(
                "CHART ENTREES SORTIES = OK"
            )

        else:

            print(
                "ERREUR : chartEntreesSorties introuvable"
            )

        # =====================================================
        # GRAPHIQUE GASOIL PAR VEHICULE
        # =====================================================

        self.chartGasoilVehicules = self.ui.findChild(
            QWidget,
            "chartGasoilVehicules"
        )

        if self.chartGasoilVehicules:

            print(
                "CHART GASOIL VEHICULES = OK"
            )

        else:

            print(
                "ERREUR : chartGasoilVehicules introuvable"
            )

        # =====================================================
        # TABLEAU MOUVEMENTS
        # =====================================================

        self.tableMouvements = self.ui.findChild(
            QTableWidget,
            "tableMouvements"
        )

        if self.tableMouvements:

            print(
                "TABLE MOUVEMENTS = OK"
            )

        else:

            print(
                "ERREUR : tableMouvements introuvable"
            )

        # =====================================================
        # TABLEAU VEHICULES GASOIL
        # =====================================================

        self.tableVehicules = self.ui.findChild(
            QTableWidget,
            "tableVehicules"
        )

        if self.tableVehicules:

            print(
                "TABLE VEHICULES = OK"
            )

            self.tableVehicules.setColumnCount(
                3
            )

            self.tableVehicules.setHorizontalHeaderLabels([
                "Véhicule",
                "Nombre opérations",
                "Total Gasoil (L)"
            ])

        else:

            print(
                "ERREUR : tableVehicules introuvable"
            )

        # =====================================================
        # TABLEAU GASOIL PAR VEHICULE
        # =====================================================

        self.tableGasoilVehicules = self.ui.findChild(
            QTableWidget,
            "tableGasoilVehicules"
        )

        if self.tableGasoilVehicules:

            print(
                "TABLE GASOIL VEHICULES = OK"
            )

            self.tableGasoilVehicules.setColumnCount(
                3
            )

            self.tableGasoilVehicules.setHorizontalHeaderLabels([
                "Matricule",
                "Opérations",
                "Total gasoil"
            ])

        else:

            print(
                "ERREUR : tableGasoilVehicules introuvable"
            )

        # =====================================================
        # BOUTON ACTUALISER
        # =====================================================

        self.btnActualiser = self.ui.findChild(
            QPushButton,
            "btnActualiser"
        )

        if self.btnActualiser:

            self.btnActualiser.clicked.connect(
                self.actualiser
            )

            print(
                "BTN DASHBOARD ACTUALISER = OK"
            )

        else:

            print(
                "ERREUR : btnActualiser introuvable"
            )

        # =====================================================
        # ACTUALISATION INITIALE
        # =====================================================

        self.actualiser()

        print(
            "DASHBOARD VIEW = OK"
        )

    # =========================================================
    # ACTUALISER DASHBOARD
    # =========================================================

    def actualiser(self):

        print(
            "DASHBOARD ACTUALISATION = START"
        )

        try:

            # =================================================
            # PRODUITS
            # =================================================

            produits = self.product_controller.get_all()

            nombre_produits = len(
                produits
            )

            print(
                "DASHBOARD PRODUITS =",
                nombre_produits
            )

            if self.lblProduits:

                self.lblProduits.setText(
                    f"Produits : {nombre_produits}"
                )

            # =================================================
            # ENTREES
            # =================================================

            entrees = self.entry_controller.get_all()

            total_entrees = 0

            for entree in entrees:

                if len(entree) > 3:

                    try:

                        total_entrees += float(
                            entree[3]
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

            print(
                "DASHBOARD TOTAL ENTREES =",
                total_entrees
            )

            if self.lblTotalEntrees:

                self.lblTotalEntrees.setText(
                    f"Total Entrées : {total_entrees}"
                )

            # =================================================
            # SORTIES
            # =================================================

            sorties = (
                self.sortie_controller
                .get_all_sorties()
            )

            total_sorties = 0

            for sortie in sorties:

                if len(sortie) > 3:

                    try:

                        total_sorties += float(
                            sortie[3]
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

            print(
                "DASHBOARD TOTAL SORTIES =",
                total_sorties
            )

            if self.lblTotalSorties:

                self.lblTotalSorties.setText(
                    f"Total Sorties : {total_sorties}"
                )

            # =================================================
            # GRAPHIQUE ENTREES / SORTIES
            # =================================================

            self.afficher_graphique_entrees_sorties(
                total_entrees,
                total_sorties
            )

            # =================================================
            # VEHICULES
            # =================================================

            vehicules = (
                self.vehicle_controller
                .get_all()
            )

            nombre_vehicules = len(
                vehicules
            )

            print(
                "DASHBOARD VEHICULES =",
                nombre_vehicules
            )

            if self.lblVehicules:

                self.lblVehicules.setText(
                    f"Véhicules : {nombre_vehicules}"
                )

            # =================================================
            # GASOIL
            # =================================================

            gasoil = (
                self.gasoil_controller
                .get_all()
            )

            total_gasoil = 0

            for operation in gasoil:

                if len(operation) > 5:

                    try:

                        total_gasoil += float(
                            operation[5]
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

            print(
                "DASHBOARD TOTAL GASOIL =",
                total_gasoil,
                "L"
            )

            if self.lblTotalGasoil:

                self.lblTotalGasoil.setText(
                    f"Total Gasoil : {total_gasoil} L"
                )

            # =================================================
            # ALERTES STOCK
            # =================================================

            alertes = 0

            for produit in produits:

                if len(produit) > 7:

                    try:

                        stock = float(
                            produit[6]
                        )

                        stock_min = float(
                            produit[7]
                        )

                        if stock <= stock_min:

                            alertes += 1

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

            print(
                "DASHBOARD ALERTES =",
                alertes
            )

            if self.lblAlertes:

                self.lblAlertes.setText(
                    f"Alertes Stock : {alertes}"
                )

            # =================================================
            # MOUVEMENTS
            # =================================================

            self.afficher_mouvements(
                entrees,
                sorties
            )

            print(
                "DASHBOARD MOUVEMENTS =",
                len(entrees) + len(sorties)
            )

            # =================================================
            # STATISTIQUES GASOIL PAR VEHICULE
            # =================================================

            statistiques = (
                self.gasoil_controller
                .get_statistics_by_vehicle()
            )

            # =================================================
            # GRAPHIQUE GASOIL
            # =================================================

            self.afficher_graphique_gasoil(
                statistiques
            )

            # =================================================
            # TABLEAU VEHICULES
            # =================================================

            donnees_vehicules = []

            for matricule, data in (
                statistiques.items()
            ):

                nombre_operations = data.get(
                    "operations",
                    0
                )

                total_gasoil_vehicule = data.get(
                    "quantite",
                    0
                )

                donnees_vehicules.append([
                    matricule,
                    nombre_operations,
                    total_gasoil_vehicule
                ])

            self.afficher_vehicules_gasoil(
                donnees_vehicules
            )

            # =================================================
            # ANCIEN TABLEAU
            # =================================================

            self.afficher_gasoil_par_vehicule()

            print(
                "DASHBOARD ACTUALISATION = OK"
            )

        except Exception as error:

            print(
                "ERREUR DASHBOARD :",
                error
            )

    # =========================================================
    # GRAPHIQUE ENTREES / SORTIES
    # =========================================================

    def afficher_graphique_entrees_sorties(
        self,
        total_entrees,
        total_sorties
    ):

        if not self.chartEntreesSorties:

            print(
                "ERREUR : chartEntreesSorties introuvable"
            )

            return

        try:

            # -------------------------------------------------
            # LAYOUT
            # -------------------------------------------------

            layout = (
                self.chartEntreesSorties.layout()
            )

            if layout is None:

                layout = QVBoxLayout(
                    self.chartEntreesSorties
                )

                layout.setContentsMargins(
                    5,
                    5,
                    5,
                    5
                )

            else:

                while layout.count():

                    item = layout.takeAt(
                        0
                    )

                    widget = item.widget()

                    if widget:

                        widget.deleteLater()

            # -------------------------------------------------
            # BARRES
            # -------------------------------------------------

            bar_entrees = QBarSet(
                "Entrées"
            )

            bar_sorties = QBarSet(
                "Sorties"
            )

            bar_entrees.append(
                float(total_entrees)
            )

            bar_sorties.append(
                float(total_sorties)
            )

            series = QBarSeries()

            series.append(
                bar_entrees
            )

            series.append(
                bar_sorties
            )

            # -------------------------------------------------
            # CHART
            # -------------------------------------------------

            chart = QChart()

            chart.addSeries(
                series
            )

            chart.setTitle(
                "Entrées / Sorties"
            )

            chart.setAnimationOptions(
                QChart.SeriesAnimations
            )

            chart.legend().setVisible(
                True
            )

            chart.legend().setAlignment(
                Qt.AlignBottom
            )

            # -------------------------------------------------
            # AXE X
            # -------------------------------------------------

            axis_x = QBarCategoryAxis()

            axis_x.append([
                "Mouvements"
            ])

            chart.addAxis(
                axis_x,
                Qt.AlignBottom
            )

            series.attachAxis(
                axis_x
            )

            # -------------------------------------------------
            # AXE Y
            # -------------------------------------------------

            maximum = max(
                float(total_entrees),
                float(total_sorties)
            )

            if maximum <= 0:

                maximum = 100

            axis_y = QValueAxis()

            axis_y.setRange(
                0,
                maximum * 1.2
            )

            axis_y.setLabelFormat(
                "%.0f"
            )

            chart.addAxis(
                axis_y,
                Qt.AlignLeft
            )

            series.attachAxis(
                axis_y
            )

            # -------------------------------------------------
            # CHART VIEW
            # -------------------------------------------------

            chart_view = QChartView(
                chart
            )

            chart_view.setRenderHint(
                QPainter.Antialiasing
            )

            chart_view.setStyleSheet(
                "background: transparent;"
            )

            layout.addWidget(
                chart_view
            )

            print(
                "GRAPHIQUE ENTREES SORTIES = OK"
            )

        except Exception as error:

            print(
                "ERREUR GRAPHIQUE ENTREES SORTIES :",
                error
            )

    # =========================================================
    # GRAPHIQUE GASOIL PAR VEHICULE
    # =========================================================

    def afficher_graphique_gasoil(
        self,
        statistiques
    ):

        if not self.chartGasoilVehicules:

            print(
                "ERREUR : chartGasoilVehicules introuvable"
            )

            return

        try:

            # -------------------------------------------------
            # LAYOUT
            # -------------------------------------------------

            layout = (
                self.chartGasoilVehicules.layout()
            )

            if layout is None:

                layout = QVBoxLayout(
                    self.chartGasoilVehicules
                )

                layout.setContentsMargins(
                    5,
                    5,
                    5,
                    5
                )

            else:

                while layout.count():

                    item = layout.takeAt(
                        0
                    )

                    widget = item.widget()

                    if widget:

                        widget.deleteLater()

            # -------------------------------------------------
            # BAR SET
            # -------------------------------------------------

            bar_set = QBarSet(
                "Gasoil (L)"
            )

            categories = []

            valeurs = []

            for matricule, data in (
                statistiques.items()
            ):

                quantite = data.get(
                    "quantite",
                    0
                )

                try:

                    quantite = float(
                        quantite
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    quantite = 0

                categories.append(
                    str(matricule)
                )

                valeurs.append(
                    quantite
                )

                bar_set.append(
                    quantite
                )

            # -------------------------------------------------
            # SERIES
            # -------------------------------------------------

            series = QBarSeries()

            series.append(
                bar_set
            )

            # -------------------------------------------------
            # CHART
            # -------------------------------------------------

            chart = QChart()

            chart.addSeries(
                series
            )

            chart.setTitle(
                "Consommation Gasoil par véhicule"
            )

            chart.setAnimationOptions(
                QChart.SeriesAnimations
            )

            chart.legend().setVisible(
                False
            )

            # -------------------------------------------------
            # AXE X
            # -------------------------------------------------

            axis_x = QBarCategoryAxis()

            axis_x.append(
                categories
            )

            chart.addAxis(
                axis_x,
                Qt.AlignBottom
            )

            series.attachAxis(
                axis_x
            )

            # -------------------------------------------------
            # AXE Y
            # -------------------------------------------------

            maximum = (
                max(valeurs)
                if valeurs
                else 100
            )

            if maximum <= 0:

                maximum = 100

            axis_y = QValueAxis()

            axis_y.setRange(
                0,
                maximum * 1.2
            )

            axis_y.setLabelFormat(
                "%.0f"
            )

            chart.addAxis(
                axis_y,
                Qt.AlignLeft
            )

            series.attachAxis(
                axis_y
            )

            # -------------------------------------------------
            # CHART VIEW
            # -------------------------------------------------

            chart_view = QChartView(
                chart
            )

            chart_view.setRenderHint(
                QPainter.Antialiasing
            )

            chart_view.setStyleSheet(
                "background: transparent;"
            )

            layout.addWidget(
                chart_view
            )

            print(
                "GRAPHIQUE GASOIL VEHICULES = OK"
            )

        except Exception as error:

            print(
                "ERREUR GRAPHIQUE GASOIL :",
                error
            )

    # =========================================================
    # AFFICHER MOUVEMENTS
    # =========================================================

    def afficher_mouvements(
        self,
        entrees,
        sorties
    ):

        if not self.tableMouvements:

            return

        mouvements = []

        # =====================================================
        # ENTREES
        # =====================================================

        for entree in entrees:

            if len(entree) < 8:

                continue

            reference = entree[1]
            produit = entree[2]
            quantite = entree[3]
            tiers = entree[4]
            date = entree[7]

            mouvements.append([
                "Entrée",
                reference,
                produit,
                quantite,
                tiers,
                date
            ])

        # =====================================================
        # SORTIES
        # =====================================================

        for sortie in sorties:

            if len(sortie) < 7:

                continue

            reference = sortie[1]
            produit = sortie[2]
            quantite = sortie[3]
            tiers = sortie[4]
            date = sortie[6]

            mouvements.append([
                "Sortie",
                reference,
                produit,
                quantite,
                tiers,
                date
            ])

        # =====================================================
        # TABLEAU
        # =====================================================

        self.tableMouvements.setRowCount(
            0
        )

        for ligne, mouvement in enumerate(
            mouvements
        ):

            self.tableMouvements.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(
                mouvement
            ):

                self.tableMouvements.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        self.tableMouvements.resizeColumnsToContents()

    # =========================================================
    # AFFICHER VEHICULES GASOIL
    # =========================================================

    def afficher_vehicules_gasoil(
        self,
        donnees
    ):

        print(
            ">>> AFFICHAGE TABLE VEHICULES GASOIL"
        )

        if not self.tableVehicules:

            print(
                "ERREUR : tableVehicules introuvable"
            )

            return

        # -----------------------------------------------------
        # VIDER
        # -----------------------------------------------------

        self.tableVehicules.clearContents()

        # -----------------------------------------------------
        # COLONNES
        # -----------------------------------------------------

        self.tableVehicules.setColumnCount(
            3
        )

        self.tableVehicules.setHorizontalHeaderLabels([
            "Véhicule",
            "Nombre opérations",
            "Total Gasoil (L)"
        ])

        # -----------------------------------------------------
        # LIGNES
        # -----------------------------------------------------

        self.tableVehicules.setRowCount(
            len(donnees)
        )

        # -----------------------------------------------------
        # REMPLIR
        # -----------------------------------------------------

        for ligne, donnees_vehicule in enumerate(
            donnees
        ):

            vehicule = donnees_vehicule[0]

            nombre_operations = (
                donnees_vehicule[1]
            )

            total_gasoil = (
                donnees_vehicule[2]
            )

            self.tableVehicules.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(vehicule)
                )
            )

            self.tableVehicules.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(nombre_operations)
                )
            )

            try:

                total_gasoil = float(
                    total_gasoil
                )

            except (
                ValueError,
                TypeError
            ):

                total_gasoil = 0

            self.tableVehicules.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    f"{total_gasoil:.1f} L"
                )
            )

        # -----------------------------------------------------
        # AJUSTER
        # -----------------------------------------------------

        self.tableVehicules.resizeColumnsToContents()

        print(
            "TABLE VEHICULES GASOIL AFFICHÉE =",
            len(donnees)
        )

    # =========================================================
    # GASOIL PAR VEHICULE
    # =========================================================

    def afficher_gasoil_par_vehicule(
        self
    ):

        if not self.tableGasoilVehicules:

            return

        try:

            statistiques = (
                self.gasoil_controller
                .get_statistics_by_vehicle()
            )

        except Exception as error:

            print(
                "ERREUR STATISTIQUES GASOIL :",
                error
            )

            return

        # =====================================================
        # VIDER
        # =====================================================

        self.tableGasoilVehicules.setRowCount(
            0
        )

        # =====================================================
        # AJOUTER
        # =====================================================

        for ligne, (
            matricule,
            data
        ) in enumerate(
            statistiques.items()
        ):

            self.tableGasoilVehicules.insertRow(
                ligne
            )

            nombre_operations = data.get(
                "operations",
                0
            )

            quantite_totale = data.get(
                "quantite",
                0
            )

            self.tableGasoilVehicules.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(matricule)
                )
            )

            self.tableGasoilVehicules.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(nombre_operations)
                )
            )

            try:

                quantite_totale = float(
                    quantite_totale
                )

            except (
                ValueError,
                TypeError
            ):

                quantite_totale = 0

            self.tableGasoilVehicules.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    f"{quantite_totale:.1f} L"
                )
            )

            print(
                matricule,
                "=",
                nombre_operations,
                "operations |",
                f"{quantite_totale:.1f}",
                "L"
            )

        self.tableGasoilVehicules.resizeColumnsToContents()

        print(
            "DASHBOARD GASOIL VEHICULES =",
            len(statistiques)
        )

    # =========================================================
    # FERMER
    # =========================================================

    def close(self):

        try:

            self.product_controller.close()

        except Exception:

            pass

        try:

            self.entry_controller.close()

        except Exception:

            pass

        try:

            self.sortie_controller.close()

        except Exception:

            pass

        try:

            self.vehicle_controller.close()

        except Exception:

            pass

        try:

            self.gasoil_controller.close()

        except Exception:

            pass

        print(
            "DASHBOARD VIEW CLOSED"
        )