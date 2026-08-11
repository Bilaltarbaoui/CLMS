import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.dashboard_view import DashboardView


# =====================================================
# APPLICATION
# =====================================================

app = QApplication(sys.argv)


# =====================================================
# CHARGEMENT DE L'INTERFACE
# =====================================================

loader = QUiLoader()

ui_file = QFile(
    "ui/main_window_dashboard.ui"
)

ui_file.open(
    QFile.ReadOnly
)

window = loader.load(
    ui_file
)

ui_file.close()


# =====================================================
# CREATION DE LA VUE
# =====================================================

dashboard_view = DashboardView(
    window
)


# =====================================================
# AFFICHAGE
# =====================================================

window.show()


# =====================================================
# LANCER APPLICATION
# =====================================================

sys.exit(
    app.exec()
)