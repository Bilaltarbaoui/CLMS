import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from database.database import Database
from views.inventory_view import InventoryView


app = QApplication(sys.argv)

# ==========================
# Base de données
# ==========================

db = Database()
db.create_tables()

# ==========================
# Chargement de l'interface
# ==========================

loader = QUiLoader()

ui_file = QFile("ui/main_window_inventory.ui")
ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)

ui_file.close()

# ==========================
# Création de la vue
# ==========================

inventory_view = InventoryView(window)

# ==========================
# Affichage
# ==========================

window.show()

sys.exit(app.exec())