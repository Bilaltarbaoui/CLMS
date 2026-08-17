import os
import shutil
import tempfile
import sqlite3
import importlib
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG_DB = ROOT / 'database' / 'clms.db'
TMPDIR = tempfile.mkdtemp(prefix='clms_conc_')
TMP_DB = Path(TMPDIR) / 'clms_conc.db'
print('TMPDIR =', TMPDIR)

# Prepare tmp DB
if ORIG_DB.exists():
    shutil.copyfile(ORIG_DB, TMP_DB)
    print('Copied original DB to', TMP_DB)
else:
    print('Original DB not found; creating minimal DB')
    conn = sqlite3.connect(str(TMP_DB))
    cur = conn.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, reference TEXT, nom TEXT, stock INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS stock_entries(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, quantite INTEGER NOT NULL, date_reception TEXT);
    CREATE TABLE IF NOT EXISTS stock_outputs(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, quantite INTEGER NOT NULL, date_sortie TEXT);
    CREATE TABLE IF NOT EXISTS historique(id INTEGER PRIMARY KEY AUTOINCREMENT, utilisateur TEXT, type_operation TEXT NOT NULL, module TEXT NOT NULL, description TEXT, date_operation TEXT NOT NULL);
    ''')
    conn.commit()
    conn.close()

# Seed product
conn = sqlite3.connect(str(TMP_DB))
cur = conn.cursor()
cur.execute('INSERT OR IGNORE INTO products(id, reference, nom, stock) VALUES (1, "P1", "Prod1", 100)')
conn.commit()
conn.close()

# Worker functions

def do_entry(args):
    # Use EntryController to ensure Database PRAGMAs are applied per connection
    _, prod_id, qty = args
    try:
        from controllers.entry_controller import EntryController
        ec = EntryController()
        ec.ajouter_entree(prod_id, qty, 'CONC', 'CNUM', 'concurrency test')
        try:
            ec.close()
        except Exception:
            pass
        return ('entry', 'ok')
    except sqlite3.OperationalError as e:
        return ('entry', 'operational', str(e))
    except Exception as e:
        return ('entry', 'error', str(e))


def do_output(args):
    _, prod_id, qty = args
    try:
        from controllers.sortie_controller import SortieController
        sc = SortieController()
        sc.ajouter_sortie(prod_id, qty, 'CONC', 'CNUM', 'concurrency test')
        try:
            sc.close()
        except Exception:
            pass
        return ('output', 'ok')
    except sqlite3.OperationalError as e:
        return ('output', 'operational', str(e))
    except Exception as e:
        return ('output', 'error', str(e))


if __name__ == '__main__':
    dbpath = str(TMP_DB)
    # Parameters
    num_workers = 2
    ops_per_worker = 10
    args = []
    for _ in range(num_workers * ops_per_worker):
        if random.random() < 0.6:
            # entry
            qty = random.randint(1,5)
            args.append((dbpath, 1, qty))
        else:
            qty = random.randint(1,4)
            args.append((dbpath, 1, qty))

    # Mix operations: half entries half outputs
    tasks = []
    for i, a in enumerate(args):
        if i % 2 == 0:
            tasks.append(('entry', a))
        else:
            tasks.append(('output', a))

    max_workers = 8
    summary = {
        'entry_ok':0,'entry_operational':0,'entry_error':0,
        'output_ok':0,'output_operational':0,'output_error':0,'output_insufficient':0
    }
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {}
        for i, t in enumerate(tasks):
            func = do_entry if t[0] == 'entry' else do_output
            future = executor.submit(func, t[1])
            future_to_task[future] = t

        for future in as_completed(future_to_task):
            t = future_to_task[future]
            try:
                res = future.result()
            except Exception as e:
                res = ('unknown','error', str(e))
            if res[0] == 'entry':
                if res[1] == 'ok':
                    summary['entry_ok'] += 1
                elif res[1] == 'operational':
                    summary['entry_operational'] += 1
                else:
                    summary['entry_error'] += 1
            elif res[0] == 'output':
                if res[1] == 'ok':
                    summary['output_ok'] += 1
                elif res[1] == 'operational':
                    summary['output_operational'] += 1
                elif res[1] == 'insufficient':
                    summary['output_insufficient'] += 1
                else:
                    summary['output_error'] += 1
            else:
                summary['entry_error'] += 1

            # collect error samples
            try:
                if res[1] != 'ok' and len(res) > 2:
                    errors.append(res[2])
            except Exception:
                pass

    print('SUMMARY', summary)
    if errors:
        print('ERROR SAMPLES:', list(set(errors))[:10])
    # validate stock consistency
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute('SELECT stock FROM products WHERE id=?',(1,))
    final_stock = cur.fetchone()[0]
    conn.close()
    print('FINAL_STOCK', final_stock)
    # count history rows
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM historique')
    count_hist = cur.fetchone()[0]
    conn.close()
    print('HISTORY_COUNT', count_hist)
    print('TMP_DB_USED:', dbpath)
