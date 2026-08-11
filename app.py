import sys

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QMessageBox,
)

from views.dashboard_view import DashboardView
from views.client_view import ClientView
from views.product_view import ProductView
from views.entry_view import EntryView
from views.sortie_view import SortieView
from views.vehicle_view import VehicleView
from views.gasoil_view import GasoilView
from views.history_view import HistoryView


# ============================================================
# APPLICATION
# ============================================================

print("CLMS APP START = OK")

app = QApplication(sys.argv)

loader = QUiLoader()


# ============================================================
# CHARGER UI PRINCIPALE
# ============================================================

ui_file = QFile("ui/main_app.ui")

print("MAIN UI FILE = ui/main_app.ui")

if not ui_file.exists():
    print("ERREUR : ui/main_app.ui N'EXISTE PAS")
    sys.exit(1)

if not ui_file.open(QFile.ReadOnly):
    print("ERREUR : impossible d'ouvrir ui/main_app.ui")
    sys.exit(1)

window = loader.load(ui_file)

ui_file.close()

if window is None:
    print("ERREUR : MAIN UI LOAD = FAILED")
    sys.exit(1)

print("MAIN UI LOAD = OK")


# ============================================================
# VARIABLES
# ============================================================

dashboard_window = None
dashboard_view = None

client_window = None
client_view = None

product_window = None
product_view = None

entry_window = None
entry_view = None

sortie_window = None
sortie_view = None

vehicle_window = None
vehicle_view = None

gasoil_window = None
gasoil_view = None

history_window = None
history_view = None


# ============================================================
# OUVRIR DASHBOARD
# ============================================================

def ouvrir_dashboard():

    global dashboard_window
    global dashboard_view

    print("OUVERTURE DASHBOARD = OK")

    dashboard_file = QFile(
        "ui/main_window_dashboard.ui"
    )

    if not dashboard_file.exists():
        print(
            "ERREUR : "
            "ui/main_window_dashboard.ui N'EXISTE PAS"
        )
        return

    if not dashboard_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/main_window_dashboard.ui"
        )
        return

    dashboard_window = loader.load(
        dashboard_file
    )

    dashboard_file.close()

    if dashboard_window is None:
        print(
            "ERREUR : "
            "DASHBOARD UI LOAD = FAILED"
        )
        return

    print("DASHBOARD UI LOAD = OK")

    try:

        dashboard_view = DashboardView(
            dashboard_window
        )

    except Exception as error:

        print(
            "ERREUR : "
            "DASHBOARD VIEW = FAILED"
        )

        print("DETAIL :", error)

        return

    print("DASHBOARD VIEW = OK")

    dashboard_window.show()

    print("DASHBOARD SHOW = OK")


# ============================================================
# OUVRIR CLIENTS
# ============================================================

def ouvrir_clients():

    global client_window
    global client_view

    print("OUVERTURE CLIENTS = OK")

    client_file = QFile("ui/client.ui")

    if not client_file.exists():
        print("ERREUR : ui/client.ui N'EXISTE PAS")
        return

    if not client_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/client.ui"
        )
        return

    client_window = loader.load(
        client_file
    )

    client_file.close()

    if client_window is None:
        print("ERREUR : CLIENT UI LOAD = FAILED")
        return

    print("CLIENT UI LOAD = OK")

    try:

        client_view = ClientView(
            client_window
        )

    except Exception as error:

        print("ERREUR : CLIENT VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("CLIENT VIEW = OK")

    client_window.show()

    print("CLIENT WINDOW SHOW = OK")


# ============================================================
# OUVRIR PRODUITS
# ============================================================

def ouvrir_produits():

    global product_window
    global product_view

    print("OUVERTURE PRODUITS = OK")

    product_file = QFile("ui/product.ui")

    if not product_file.exists():
        print("ERREUR : ui/product.ui N'EXISTE PAS")
        return

    if not product_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/product.ui"
        )
        return

    product_window = loader.load(
        product_file
    )

    product_file.close()

    if product_window is None:
        print("ERREUR : PRODUCT UI LOAD = FAILED")
        return

    print("PRODUCT UI LOAD = OK")

    try:

        product_view = ProductView(
            product_window
        )

    except Exception as error:

        print("ERREUR : PRODUCT VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("PRODUCT VIEW = OK")

    product_window.show()

    print("PRODUCT WINDOW SHOW = OK")


# ============================================================
# OUVRIR ENTREES
# ============================================================

def ouvrir_entrees():

    global entry_window
    global entry_view

    print("OUVERTURE ENTREES = OK")

    entry_file = QFile("ui/entry.ui")

    if not entry_file.exists():
        print("ERREUR : ui/entry.ui N'EXISTE PAS")
        return

    if not entry_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/entry.ui"
        )
        return

    entry_window = loader.load(
        entry_file
    )

    entry_file.close()

    if entry_window is None:
        print("ERREUR : ENTRY UI LOAD = FAILED")
        return

    print("ENTRY UI LOAD = OK")

    try:

        entry_view = EntryView(
            entry_window
        )

    except Exception as error:

        print("ERREUR : ENTRY VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("ENTRY VIEW = OK")

    entry_window.show()

    print("ENTRY WINDOW SHOW = OK")


# ============================================================
# OUVRIR SORTIES
# ============================================================

def ouvrir_sorties():

    global sortie_window
    global sortie_view

    print("OUVERTURE SORTIES = OK")

    sortie_file = QFile("ui/sortie.ui")

    if not sortie_file.exists():
        print("ERREUR : ui/sortie.ui N'EXISTE PAS")
        return

    if not sortie_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/sortie.ui"
        )
        return

    sortie_window = loader.load(
        sortie_file
    )

    sortie_file.close()

    if sortie_window is None:
        print("ERREUR : SORTIE UI LOAD = FAILED")
        return

    print("SORTIE UI LOAD = OK")

    try:

        sortie_view = SortieView(
            sortie_window
        )

    except Exception as error:

        print("ERREUR : SORTIE VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("SORTIE VIEW = OK")

    sortie_window.show()

    print("SORTIE WINDOW SHOW = OK")


# ============================================================
# OUVRIR VEHICULES
# ============================================================

def ouvrir_vehicules():

    global vehicle_window
    global vehicle_view

    print("OUVERTURE VEHICULES = OK")

    vehicle_file = QFile("ui/vehicle.ui")

    if not vehicle_file.exists():
        print("ERREUR : ui/vehicle.ui N'EXISTE PAS")
        return

    if not vehicle_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/vehicle.ui"
        )
        return

    vehicle_window = loader.load(
        vehicle_file
    )

    vehicle_file.close()

    if vehicle_window is None:
        print("ERREUR : VEHICLE UI LOAD = FAILED")
        return

    print("VEHICLE UI LOAD = OK")

    try:

        vehicle_view = VehicleView(
            vehicle_window
        )

    except Exception as error:

        print("ERREUR : VEHICLE VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("VEHICLE VIEW = OK")

    vehicle_window.show()

    print("VEHICLE WINDOW SHOW = OK")


# ============================================================
# OUVRIR GASOIL
# ============================================================

def ouvrir_gasoil():

    global gasoil_window
    global gasoil_view

    print("OUVERTURE GASOIL = OK")

    gasoil_file = QFile("ui/gasoil.ui")

    if not gasoil_file.exists():
        print("ERREUR : ui/gasoil.ui N'EXISTE PAS")
        return

    if not gasoil_file.open(QFile.ReadOnly):
        print(
            "ERREUR : impossible d'ouvrir "
            "ui/gasoil.ui"
        )
        return

    gasoil_window = loader.load(
        gasoil_file
    )

    gasoil_file.close()

    if gasoil_window is None:
        print("ERREUR : GASOIL UI LOAD = FAILED")
        return

    print("GASOIL UI LOAD = OK")

    try:

        gasoil_view = GasoilView(
            gasoil_window
        )

    except Exception as error:

        print("ERREUR : GASOIL VIEW = FAILED")
        print("DETAIL :", error)

        return

    print("GASOIL VIEW = OK")

    gasoil_window.show()

    print("GASOIL WINDOW SHOW = OK")


# ============================================================
# OUVRIR HISTORIQUE
# ============================================================

def ouvrir_historique():

    global history_window
    global history_view

    print("OUVERTURE HISTORIQUE = OK")

    history_file = QFile(
        "ui/stock_movement.ui"
    )

    if not history_file.exists():

        print(
            "ERREUR : "
            "ui/stock_movement.ui N'EXISTE PAS"
        )

        return

    if not history_file.open(
        QFile.ReadOnly
    ):

        print(
            "ERREUR : impossible d'ouvrir "
            "ui/stock_movement.ui"
        )

        return

    history_window = loader.load(
        history_file
    )

    history_file.close()

    if history_window is None:

        print(
            "ERREUR : "
            "HISTORIQUE UI LOAD = FAILED"
        )

        return

    print("HISTORIQUE UI LOAD = OK")

    try:

        history_view = HistoryView(
            history_window
        )

    except Exception as error:

        print(
            "ERREUR : "
            "HISTORY VIEW = FAILED"
        )

        print("DETAIL :", error)

        return

    print("HISTORY VIEW = OK")

    history_window.show()

    print("HISTORIQUE WINDOW SHOW = OK")


# ============================================================
# PARAMETRES
# ============================================================

def ouvrir_parametres():

    print("OUVERTURE PARAMETRES = OK")

    QMessageBox.information(
        window,
        "Paramètres",
        "Module Paramètres\n\n"
        "Cette fonctionnalité sera développée "
        "dans la prochaine étape."
    )

    print("PARAMETRES = OK")


# ============================================================
# A PROPOS
# ============================================================

def ouvrir_a_propos():

    print("OUVERTURE A PROPOS = OK")

    QMessageBox.about(
        window,
        "À propos",
        "CLMS - Gestion Logistique\n\n"
        "Application de gestion logistique.\n"
        "Transport - Stock - Véhicules - Gasoil"
    )

    print("A PROPOS = OK")


# ============================================================
# FONCTION UTILITAIRE
# ============================================================

def connecter_bouton(
    nom_bouton,
    fonction
):

    bouton = window.findChild(
        QPushButton,
        nom_bouton
    )

    if bouton is None:

        print(
            "ERREUR :",
            nom_bouton,
            "introuvable"
        )

        return False

    bouton.clicked.connect(
        fonction
    )

    print(
        "BTN",
        nom_bouton,
        "= OK"
    )

    return True


# ============================================================
# BOUTONS PRINCIPAUX
# ============================================================

connecter_bouton(
    "btnDashboard",
    ouvrir_dashboard
)

connecter_bouton(
    "btnClients",
    ouvrir_clients
)

connecter_bouton(
    "btnProduits",
    ouvrir_produits
)

connecter_bouton(
    "btnEntrees",
    ouvrir_entrees
)

connecter_bouton(
    "btnSorties",
    ouvrir_sorties
)

connecter_bouton(
    "btnVehicules",
    ouvrir_vehicules
)

connecter_bouton(
    "btnGasoil",
    ouvrir_gasoil
)


# ============================================================
# BOUTONS HISTORIQUE / PARAMETRES / A PROPOS
# ============================================================

connecter_bouton(
    "btnHistorique",
    ouvrir_historique
)

connecter_bouton(
    "btnParametres",
    ouvrir_parametres
)

connecter_bouton(
    "btnAPropos",
    ouvrir_a_propos
)


# ============================================================
# AFFICHER FENETRE PRINCIPALE
# ============================================================

window.show()

print("MAIN WINDOW SHOW = OK")


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

sys.exit(
    app.exec()
)