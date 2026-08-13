import os
import sys
import tempfile
import shutil
import importlib.util
import sqlite3

orig = os.getcwd()
project_root = orig

results = []

def report(name, ok, msg=''):
    status = 'PASS' if ok else 'FAIL'
    print(f"{status}: {name} {msg}")
    results.append((name, ok, msg))


def load_app_in_tempdir(tempdir):
    # ensure tempdir has database dir
    os.makedirs(os.path.join(tempdir, 'database'), exist_ok=True)
    # load web_app.py as module with imports resolving to project
    spec = importlib.util.spec_from_file_location('web_app_test', os.path.join(project_root, 'web_app.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules['web_app_test'] = module
    sys.path.insert(0, project_root)
    try:
        spec.loader.exec_module(module)
    finally:
        try:
            sys.path.pop(0)
        except Exception:
            pass
    return module


def run():
    td = tempfile.mkdtemp()
    try:
        os.chdir(td)
        appmod = load_app_in_tempdir(td)
        app = appmod.app

        # Use controllers to create users
        from controllers.user_controller import UserController
        uc = UserController()
        uc._actor = 'SYSTEM'
        try:
            # create users
            a = uc.create_user('ck_admin', 'Pass123!', role='admin', nom_complet='Admin CK', actif=1)
            r = uc.create_user('ck_resp', 'Pass123!', role='responsable', nom_complet='Resp CK', actif=1)
            m = uc.create_user('ck_mag', 'Pass123!', role='magasinier', nom_complet='Mag CK', actif=1)
            report('create_users', True, '')
        except Exception as e:
            report('create_users', False, str(e))

        client = app.test_client()

        # Helper login
        def login(username, password):
            return client.post('/login', data={'username': username, 'password': password}, follow_redirects=False)

        # A. Unauthenticated access
        r = client.get('/clients')
        report('unauthenticated_clients_redirect', r.status_code in (301,302), f'status={r.status_code}')

        # Admin
        login('ck_admin', 'Pass123!')
        r = client.get('/clients')
        report('admin_clients_get', r.status_code == 200, f'status={r.status_code}')
        r = client.get('/gestion-utilisateurs')
        report('admin_gestion_utilisateurs', r.status_code == 200, f'status={r.status_code}')
        r = client.get('/parametres')
        report('admin_parametres', r.status_code == 200, f'status={r.status_code}')
        client.get('/logout')

        # Responsable
        login('ck_resp', 'Pass123!')
        r = client.get('/clients')
        report('resp_clients_get', r.status_code == 200, f'status={r.status_code}')
        r = client.get('/gestion-utilisateurs')
        report('resp_gestion_utilisateurs_forbidden', r.status_code == 403, f'status={r.status_code}')
        r = client.get('/parametres')
        report('resp_parametres_forbidden', r.status_code == 403, f'status={r.status_code}')
        client.get('/logout')

        # Magasinier
        login('ck_mag', 'Pass123!')
        r = client.get('/produits')
        report('mag_produits_get', r.status_code == 200, f'status={r.status_code}')
        r = client.get('/clients')
        report('mag_clients_forbidden', r.status_code == 403, f'status={r.status_code}')
        r = client.get('/vehicules')
        report('mag_vehicules_forbidden', r.status_code == 403, f'status={r.status_code}')
        client.get('/logout')

        # Products: magasiner add/edit allowed, delete forbidden
        login('ck_mag', 'Pass123!')
        # Add product
        r = client.post('/produits/add', data={'reference':'TREF','nom':'TProd','categorie':'c','marque':'m','unite':'u','stock':'0','stock_min':'0'}, follow_redirects=False)
        added_ok = r.status_code in (302, 303)
        report('mag_add_produit', added_ok, f'status={r.status_code}')
        # Edit product - need id; fetch products page content to find id simplified: query model
        from models.product_model import ProductModel
        pm = ProductModel()
        products = pm.get_all_products()
        pid = products[0][0] if products else None
        if pid:
            r = client.post(f'/produits/edit/{pid}', data={'reference':'TREF','nom':'TProd2','categorie':'c','marque':'m','unite':'u','stock':'0','stock_min':'0'}, follow_redirects=False)
            report('mag_edit_produit', r.status_code in (302,303), f'status={r.status_code}')
            # Delete attempt
            r = client.post(f'/produits/delete/{pid}', follow_redirects=False)
            report('mag_delete_produit_forbidden', r.status_code == 403, f'status={r.status_code}')
        else:
            report('mag_product_not_found', False, 'no product created')
        client.get('/logout')

        # Stock tests using models directly
        from models.product_model import ProductModel
        from models.entry_model import EntryModel
        from models.sortie_model import SortieModel

        pm = ProductModel()
        em = EntryModel()
        sm = SortieModel()
        # create a product
        pid = pm.create_product('REFCK','ProdCK') if hasattr(pm, 'create_product') else None
        # Fallback insert directly
        conn = sqlite3.connect(os.path.join('database','clms.db'))
        cur = conn.cursor()
        if not pid:
            cur.execute("INSERT INTO products (reference, nom, stock, date_creation) VALUES (?, ?, ?, datetime('now'))", ('REFCK','ProdCK',0))
            conn.commit()
            cur.execute('SELECT id FROM products WHERE reference=?', ('REFCK',))
            pid = cur.fetchone()[0]

        # Reset stock operations
        # entries
        try:
            em.ajouter_entree(pid, 20, 'F', 'NB1', 'ok')
            report('entry_positive', True, '')
        except Exception as e:
            report('entry_positive', False, str(e))
        try:
            em.ajouter_entree(pid, 0, 'F', 'NB2', 'zero')
            report('entry_zero', True, '')
        except Exception as e:
            report('entry_zero', False, str(e))
        try:
            em.ajouter_entree(pid, -5, 'F', 'NB3', 'neg')
            report('entry_negative_should_fail', False, 'negative accepted')
        except Exception:
            report('entry_negative_should_fail', True, '')

        # sorties
        try:
            sm.ajouter_sortie(pid, 8, 'C', 'NB4', 'ok')
            report('sortie_positive', True, '')
        except Exception as e:
            report('sortie_positive', False, str(e))
        try:
            sm.ajouter_sortie(pid, 0, 'C', 'NB5', 'zero')
            report('sortie_zero', True, '')
        except Exception as e:
            report('sortie_zero', False, str(e))
        try:
            sm.ajouter_sortie(pid, -3, 'C', 'NB6', 'neg')
            report('sortie_negative_should_fail', False, 'negative accepted')
        except Exception:
            report('sortie_negative_should_fail', True, '')
        try:
            # overdraw
            sm.ajouter_sortie(pid, 9999, 'C', 'NB7', 'over')
            report('sortie_overdraw_should_fail', False, 'overdraw accepted')
        except Exception:
            report('sortie_overdraw_should_fail', True, '')

        # verify stock final = entries - sorties
        cur.execute('SELECT stock FROM products WHERE id=?', (pid,))
        stock = cur.fetchone()[0]
        cur.execute('SELECT SUM(quantite) FROM stock_entries WHERE product_id=?', (pid,))
        sum_ent = cur.fetchone()[0] or 0
        cur.execute('SELECT SUM(quantite) FROM stock_outputs WHERE product_id=?', (pid,))
        sum_sort = cur.fetchone()[0] or 0
        report('stock_consistency', stock == (sum_ent - sum_sort), f'stock={stock} ent={sum_ent} sort={sum_sort}')

        # Historique: check that entries were logged (non-sensitive)
        cur.execute("SELECT COUNT(*) FROM historique")
        hcount = cur.fetchone()[0]
        report('historique_nonempty', hcount > 0, f'count={hcount}')

        # User management: duplicate username
        try:
            uc.create_user('ck_admin', 'X', role='admin')
            report('duplicate_username_should_fail', False, 'duplicate allowed')
        except Exception:
            report('duplicate_username_should_fail', True, '')

        # role invalid
        try:
            uc.create_user('ck_badrole', 'X', role='invalidrole')
            report('invalid_role_rejected', False, 'invalid role allowed')
        except Exception:
            report('invalid_role_rejected', True, '')

        # session invalidation for inactive user
        # create inactive user
        uid = uc.create_user('ck_inactive', 'P', role='magasinier', actif=0)
        r = client.post('/login', data={'username':'ck_inactive','password':'P'}, follow_redirects=False)
        # Login should not authenticate; accessing protected resource should redirect to login
        r2 = client.get('/clients')
        report('inactive_user_cannot_login', r2.status_code in (301,302), f'status={r2.status_code}')

        # cleanup
        try:
            uc.close()
        except Exception:
            pass
        try:
            pm.close()
        except Exception:
            pass
        try:
            em.database.close()
        except Exception:
            pass
        try:
            sm.database.close()
        except Exception:
            pass
        try:
            appmod.database.close()
        except Exception:
            pass
        conn.close()
        # return to original cwd before cleanup
        try:
            os.chdir(orig)
        except Exception:
            pass
    finally:
        # best-effort cleanup; Windows may keep a lock for a short time
        try:
            shutil.rmtree(td)
        except Exception:
            pass

    # summary
    passed = sum(1 for _,ok,_ in results if ok)
    total = len(results)
    print('\nSUMMARY: %d/%d passed' % (passed, total))

if __name__ == '__main__':
    run()
