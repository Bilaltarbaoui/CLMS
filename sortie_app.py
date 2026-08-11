import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from database.database import Database
from views.sortie_view import SortieView

app = QApplication(sys.argv)

# ==========================
# Base de données
# ==========================

db = Database()
db.create_tables()

# ==========================
# Interface
# ==========================

loader = QUiLoader()

ui_file = QFile("ui/main_window_sorties.ui")

ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)

ui_file.close()

# ==========================
# View
# ==========================

sortie_view = SortieView(window)

window.show()

sys.exit(app.exec())