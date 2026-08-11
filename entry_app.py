import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from database.database import Database
from views.entry_view import EntryView

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

ui_file = QFile("ui/main_window_entries.ui")

ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)

ui_file.close()

# ==========================
# View
# ==========================

entry_view = EntryView(window)

window.show()

sys.exit(app.exec())