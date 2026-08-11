import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.history_view import HistoryView


# =====================================================
# APPLICATION
# =====================================================

app = QApplication(sys.argv)


# =====================================================
# CHARGEMENT DE L'INTERFACE
# =====================================================

loader = QUiLoader()

ui_file = QFile(
    "ui/stock_movement.ui"
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

history_view = HistoryView(
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

