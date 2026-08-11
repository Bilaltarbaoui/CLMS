import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from database.database import Database
from views.product_view import ProductView

app = QApplication(sys.argv)

# Base de données
db = Database()
db.create_tables()

# Chargement de l'interface Produits
loader = QUiLoader()

ui_file = QFile("ui/main_window_product.ui")
ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)

ui_file.close()

# Création de la vue
product_view = ProductView(window)

# Affichage
window.show()

sys.exit(app.exec())