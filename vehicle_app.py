import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.vehicle_view import VehicleView


app = QApplication(sys.argv)

print("======================================")
print("VEHICLE APP START")
print("======================================")


# =====================================================
# CHARGER UI
# =====================================================

ui_file = QFile(
    "ui/main_window_vehicule.ui"
)

if not ui_file.open(QFile.ReadOnly):

    print(
        "ERREUR : impossible d'ouvrir l'UI vehicule"
    )

    sys.exit(1)


loader = QUiLoader()

window = loader.load(
    ui_file
)

ui_file.close()


if window is None:

    print(
        "ERREUR : impossible de charger la fenêtre véhicule"
    )

    sys.exit(1)


print(
    "VEHICLE UI LOAD = OK"
)


# =====================================================
# CREER VIEW
# =====================================================

vehicle_view = VehicleView(
    window
)


print(
    "VEHICLE VIEW CREATED = OK"
)


# =====================================================
# AFFICHER
# =====================================================

window.show()

print(
    "VEHICLE WINDOW SHOW = OK"
)


# =====================================================
# APPLICATION
# =====================================================

sys.exit(
    app.exec()
)