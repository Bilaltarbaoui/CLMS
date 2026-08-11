import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.gasoil_view import GasoilView


# =====================================================
# APPLICATION
# =====================================================

app = QApplication(sys.argv)

print("APP START = OK")


# =====================================================
# CHARGER UI
# =====================================================

loader = QUiLoader()

ui_file = QFile(
    "ui/main_window_gasoil.ui"
)

if not ui_file.open(QFile.ReadOnly):

    print("ERREUR : impossible d'ouvrir UI Gasoil")

    sys.exit(1)


window = loader.load(
    ui_file
)

ui_file.close()


if window is None:

    print("ERREUR : window = None")

    sys.exit(1)


print("UI LOAD = OK")


# =====================================================
# CREER VIEW
# =====================================================

gasoil_view = GasoilView(
    window
)

print("GASOIL VIEW = OK")


# =====================================================
# AFFICHER
# =====================================================

window.show()
window.raise_()
window.activateWindow()

print("WINDOW SHOW = OK")
# =====================================================
# LANCER APPLICATION
# =====================================================

sys.exit(
    app.exec()
)