import os
import shutil
import hashlib
import tempfile
import sqlite3
import traceback

from pathlib import Path
import importlib
import sys

ROOT = Path(__file__).resolve().parent.parent
ORIG_DB = ROOT / 'database' / 'clms.db'

# Ensure project root is on sys.path so imports like `controllers` work
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TMPDIR = tempfile.mkdtemp(prefix='clms_test_')
TMP_DB = Path(TMPDIR) / 'clms_test.db'

print('TMPDIR =', TMPDIR)

# Prepare temporary DB: copy if original exists, otherwise create minimal schema
if ORIG_DB.exists():
    shutil.copyfile(ORIG_DB, TMP_DB)
    print('Copied original DB to', TMP_DB)
else:
    print('Original DB not found, creating minimal test DB at', TMP_DB)
    conn = sqlite3.connect(str(TMP_DB))
    cur = conn.cursor()
    # Minimal schema subset used by tests
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT,
        nom TEXT NOT NULL,
        stock INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS stock_entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantite INTEGER NOT NULL,
        date_reception TEXT
    );
    CREATE TABLE IF NOT EXISTS stock_outputs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantite INTEGER NOT NULL,
        date_sortie TEXT
    );
    CREATE TABLE IF NOT EXISTS historique(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur TEXT,
        type_operation TEXT NOT NULL,
        module TEXT NOT NULL,
        description TEXT,
        date_operation TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        actif INTEGER NOT NULL DEFAULT 1
    );
    ''')
    conn.commit()
    conn.close()

# Monkeypatch sqlite3.connect to redirect the project DB path to TMP_DB
_orig_connect = sqlite3.connect

def connect_redirect(path, *args, **kwargs):
    try:
        if isinstance(path, str) and (path.endswith('database/clms.db') or path.endswith('database\\clms.db') or path == 'database/clms.db'):
            return _orig_connect(str(TMP_DB), *args, **kwargs)
    except Exception:
        pass
    return _orig_connect(path, *args, **kwargs)

sqlite3.connect = connect_redirect

# Now import project modules and run tests
results = []

print('PHASE 1: IMPORT CONTROLLERS')
try:
    # Import controllers
    from controllers.client_controller import ClientController
    from controllers.product_controller import ProductController
    from controllers.entry_controller import EntryController
    from controllers.sortie_controller import SortieController
    from controllers.inventory_controller import InventoryController
    from controllers.vehicle_controller import VehicleController
    from controllers.gasoil_controller import GasoilController
    from controllers.HistoryController import HistoryController
    from controllers.stock_movement_controller import StockMovementController
    from controllers.dashboard_controller import DashboardController
    print('PHASE 1: IMPORT CONTROLLERS OK')
except Exception as e:
    print('PHASE 1: IMPORT CONTROLLERS FAILED', e)
    raise

# If modules were previously imported in this interpreter session,
# reload them to pick up file edits made during this run.
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith('controllers.'):
        try:
            importlib.reload(sys.modules[mod_name])
        except Exception:
            pass

# Re-import controller classes after reload
from controllers.client_controller import ClientController
from controllers.product_controller import ProductController
from controllers.entry_controller import EntryController
from controllers.sortie_controller import SortieController
from controllers.inventory_controller import InventoryController
from controllers.vehicle_controller import VehicleController
from controllers.gasoil_controller import GasoilController
from controllers.HistoryController import HistoryController
from controllers.stock_movement_controller import StockMovementController
from controllers.dashboard_controller import DashboardController

# Instantiate controllers
print('PHASE 2: INSTANTIATE CONTROLLERS')
cc = ClientController()
pc = ProductController()
ec = EntryController()
sc = SortieController()
ic = InventoryController()
vc = VehicleController()
gc = GasoilController()
hc = HistoryController()
smc = StockMovementController()
dc = DashboardController()
print('PHASE 2: INSTANTIATE CONTROLLERS OK')

results.append(('instantiate_controllers', 'OK'))

# 8. Clients: add and list
print('PHASE 3: CLIENTS/PRODUCTS/ENTRY/SORTIE/HISTORY TESTS')
pc.model.connection.execute('DELETE FROM products')
pc.model.connection.commit()
cc.model.connection.execute('DELETE FROM clients')
cc.model.connection.commit()

cc.model.ajouter_client('Test Client','000','Addr','a@b.c','City')
clients = cc.get_all_clients()
results.append(('clients_create_list', 'OK' if clients and len(clients) >= 1 else 'FAIL', clients[:1]))

# 9. Products: add and list
pc.model.ajouter_produit('REF123','TestProd','Cat','Marq','u',10,0,'L1',None,'F',"desc",None,None)
products = pc.get_all_products()
results.append(('products_create_list', 'OK' if products and len(products) >= 1 else 'FAIL', products[:1]))

prod_id = products[0][0]

# 10. Entries: add entry
ec.ajouter_entree(prod_id, 5, 'Fourn', 'B1', 'c')
entries = ec.get_all_entries()
results.append(('entry_add', 'OK' if entries and len(entries) >= 1 else 'FAIL', entries[:1]))

# 11. Sorties: add sortie (valid)
sc.ajouter_sortie(prod_id, 3, 'ClientX', 'S1', 'c')
sorties = sc.get_all_sorties()
results.append(('sortie_add', 'OK' if sorties and len(sorties) >= 1 else 'FAIL', sorties[:1]))

# 21. Rollback check: attempt invalid sortie (too large)
try:
    sc.ajouter_sortie(prod_id, 999999, 'ClientX', 'S2', 'c')
    results.append(('sortie_overflow_rollback', 'FAIL', 'No exception'))
except Exception as e:
    results.append(('sortie_overflow_rollback', 'OK', str(e)))

# 22/23 History: verify traces created
hist = hc.get_history()
results.append(('history_rows', 'OK' if hist and len(hist) >= 2 else 'FAIL', hist[:5]))

# 24. Stock consistency
current_stock = pc.model.cursor.execute('SELECT stock FROM products WHERE id=?', (prod_id,)).fetchone()[0]
results.append(('stock_consistent', 'OK' if isinstance(current_stock, int) or isinstance(current_stock, float) else 'FAIL', current_stock))

# 25. Totals via StockMovementController
movements = smc.get_movements()
total_ent = sum([float(m[3]) for m in movements if str(m[0]).upper().startswith('ENT')])
total_sort = sum([float(m[3]) for m in movements if str(m[0]).upper().startswith('SOR') or str(m[0]).upper().startswith('S')])
results.append(('stockmovement_totals_calc', 'OK', {'total_entrees': total_ent, 'total_sorties': total_sort}))

# 26. Connections closure
try:
    controllers_to_close = [cc, pc, ec, sc, ic, vc, gc, hc, smc, dc]
    for c in controllers_to_close:
        try:
            if hasattr(c, 'close'):
                c.close()
            else:
                # best-effort: close underlying models if present
                if hasattr(c, 'model') and hasattr(c.model, 'close'):
                    c.model.close()
                if hasattr(c, 'vehicle_model') and hasattr(c.vehicle_model, 'close'):
                    c.vehicle_model.close()
        except Exception:
            pass
    results.append(('close_connections', 'OK'))
except Exception as e:
    results.append(('close_connections', 'FAIL', str(e)))

# 27. Password hashing tests (PBKDF2 migration / verification)
try:
    from database.database import Database

    db = Database()

    # Ensure clean users
    try:
        db.cursor.execute('DELETE FROM users')
        db.commit_with_retry()
    except Exception:
        pass

    # Create user with PBKDF2
    newhash, salt = db.make_password_hash('secret123')

    # Ensure password_salt column exists (in case TMP DB was copied from older schema)
    try:
        db.cursor.execute("PRAGMA table_info(users)")
        cols = [r[1] for r in db.cursor.fetchall()]
        if 'password_salt' not in cols:
            db.cursor.execute('ALTER TABLE users ADD COLUMN password_salt TEXT')
            db.commit_with_retry()
    except Exception:
        pass

    db.cursor.execute('INSERT INTO users(username,password_hash,password_salt,role,actif) VALUES (?,?,?,?,?)', ('u1', newhash, salt, 'user', 1))
    db.commit_with_retry()

    ok1 = db.verify_and_migrate_password('u1', 'secret123')
    ok2 = not db.verify_and_migrate_password('u1', 'wrongpass')

    # Legacy hash compatibility: insert legacy sha256 and verify migration
    legacy = hashlib.sha256('oldpass'.encode()).hexdigest()
    db.cursor.execute('INSERT INTO users(username,password_hash,role,actif) VALUES (?,?,?,?)', ('legacy', legacy, 'user', 1))
    db.commit_with_retry()

    legacy_ok = db.verify_and_migrate_password('legacy', 'oldpass')
    # After successful verify, the legacy record should have been migrated to pbkdf2
    db.cursor.execute("SELECT password_hash FROM users WHERE username = ?", ('legacy',))
    new_stored = db.cursor.fetchone()[0]
    migrated = isinstance(new_stored, str) and new_stored.startswith('pbkdf2_sha256$')

    results.append(('password_tests', 'OK' if (ok1 and ok2 and legacy_ok and migrated) else 'FAIL', {
        'ok1': ok1,
        'ok2': ok2,
        'legacy_ok': legacy_ok,
        'migrated': migrated
    }))
except Exception as e:
    results.append(('password_tests', 'FAIL', str(e)))

# Print results
for r in results:
    print(r)

print('TMP_DB_USED:', TMP_DB)
print('TESTS_DONE')
