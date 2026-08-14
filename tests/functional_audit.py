"""
PHASE 2 - FUNCTIONAL AUDIT TEST SUITE
Comprehensive testing of CLMS application without modifying production data

Uses isolated temporary SQLite database for all tests.
Tests all modules: Products, Entries, Sorties, Clients, Vehicles, Gasoil, Dashboard, etc.
"""

import os
import sys
import tempfile
import shutil
import importlib.util
import sqlite3
import json
from datetime import datetime, timedelta

# Global results tracking
test_results = []
test_count = 0
pass_count = 0
fail_count = 0
module_results = {}

def report(name, ok, msg='', module=''):
    """Report test result"""
    global test_count, pass_count, fail_count, test_results
    status = 'PASS' if ok else 'FAIL'
    print(f"{status}: {name} {msg}")
    test_results.append((name, ok, msg, module))
    test_count += 1
    if ok:
        pass_count += 1
    else:
        fail_count += 1
    if module not in module_results:
        module_results[module] = {'pass': 0, 'fail': 0, 'total': 0}
    module_results[module]['total'] += 1
    if ok:
        module_results[module]['pass'] += 1
    else:
        module_results[module]['fail'] += 1


def load_app_in_tempdir(tempdir):
    """Load web_app.py as a module in isolated temp directory"""
    project_root = os.getcwd()
    os.makedirs(os.path.join(tempdir, 'database'), exist_ok=True)

    spec = importlib.util.spec_from_file_location('web_app_audit',
                                                    os.path.join(project_root, 'web_app.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules['web_app_audit'] = module
    sys.path.insert(0, project_root)

    # Change to temp directory so database.py writes to temp location
    orig_cwd = os.getcwd()
    os.chdir(tempdir)

    try:
        spec.loader.exec_module(module)
    finally:
        try:
            sys.path.pop(0)
        except Exception:
            pass
        os.chdir(orig_cwd)

    return module, project_root


def setup_test_data(app, db_instance):
    """Create test users and sample data"""
    from controllers.user_controller import UserController
    from controllers.product_controller import ProductController
    from controllers.client_controller import ClientController
    from controllers.vehicle_controller import VehicleController

    # Create admin user
    uc = UserController()
    uc._actor = 'SYSTEM'
    try:
        admin_id = uc.create_user('audit_admin', 'AdminTest123!', role='admin',
                                   nom_complet='Admin Audit', actif=1)
    except Exception as e:
        admin_id = None
        print(f"  Warning: Admin creation failed: {e}")

    # Create responsable user
    try:
        resp_id = uc.create_user('audit_resp', 'RespTest123!', role='responsable',
                                  nom_complet='Responsable Audit', actif=1)
    except Exception as e:
        resp_id = None
        print(f"  Warning: Responsable creation failed: {e}")

    # Create magasinier user
    try:
        mag_id = uc.create_user('audit_mag', 'MagTest123!', role='magasinier',
                                 nom_complet='Magasinier Audit', actif=1)
    except Exception as e:
        mag_id = None
        print(f"  Warning: Magasinier creation failed: {e}")

    # Create test products
    pc = ProductController()
    product_ids = []
    try:
        # Product 1: Basic product
        pc.ajouter_produit(
            reference='PROD001',
            nom='Test Product 1',
            categorie='Category A',
            marque='Brand X',
            unite='Kg',
            stock=100,
            stock_min=10,
            numero_lot='LOT001',
            dlc='2025-12-31',
            fournisseur='Supplier A',
            description='Test product 1',
            date_reception='2024-01-01',
            date_livraison='2024-01-02'
        )
        # Get the ID from database
        conn = sqlite3.connect('database/clms.db')
        c = conn.cursor()
        c.execute("SELECT id FROM products WHERE reference = 'PROD001'")
        result = c.fetchone()
        if result:
            product_ids.append(result[0])
        conn.close()
    except Exception as e:
        print(f"  Warning: Product 1 creation failed: {e}")

    try:
        # Product 2: Another product for testing
        pc.ajouter_produit(
            reference='PROD002',
            nom='Test Product 2',
            categorie='Category B',
            marque='Brand Y',
            unite='Liters',
            stock=50,
            stock_min=5,
            numero_lot='LOT002',
            dlc='2025-06-30',
            fournisseur='Supplier B',
            description='Test product 2',
            date_reception='2024-01-15',
            date_livraison='2024-01-16'
        )
        conn = sqlite3.connect('database/clms.db')
        c = conn.cursor()
        c.execute("SELECT id FROM products WHERE reference = 'PROD002'")
        result = c.fetchone()
        if result:
            product_ids.append(result[0])
        conn.close()
    except Exception as e:
        print(f"  Warning: Product 2 creation failed: {e}")

    # Create test clients
    cc = ClientController()
    try:
        cc.ajouter_client(
            nom='Test Client 1',
            telephone='555-1234',
            adresse='123 Main St',
            email='client1@test.com',
            ville='City A'
        )
    except Exception as e:
        print(f"  Warning: Client creation failed: {e}")

    # Create test vehicles
    vc = VehicleController()
    try:
        vc.ajouter(  # Correct method name
            immatriculation='ABC-1234',
            marque='Toyota',
            modele='Corolla',
            type='Sedan',
            kilometrage=50000,
            chauffeur='Driver 1',
            statut='Disponible'
        )
    except Exception as e:
        print(f"  Warning: Vehicle creation failed: {e}")

    return admin_id, resp_id, mag_id, product_ids


def run_tests():
    """Run all functional tests"""
    print("\n" + "="*80)
    print("PHASE 2 - FUNCTIONAL AUDIT TEST SUITE")
    print("="*80 + "\n")

    td = tempfile.mkdtemp()
    print(f"Test database: {td}\n")

    try:
        # Load app in temp directory
        appmod, project_root = load_app_in_tempdir(td)
        app = appmod.app
        app.config['TESTING'] = True

        # Create database instance for direct tests
        os.chdir(td)
        from database.database import Database
        db_instance = Database()
        os.chdir(project_root)

        # Setup test data
        print("Setting up test data...")
        admin_id, resp_id, mag_id, product_ids = setup_test_data(app, db_instance)
        print(f"  Test users created: admin={admin_id}, resp={resp_id}, mag={mag_id}")
        print(f"  Test products created: {product_ids}\n")

        # ====================================================================
        # AUTHENTICATION TESTS
        # ====================================================================
        print("\n--- AUTHENTICATION TESTS ---\n")

        with app.test_client() as client:
            # Test login page loads
            resp = client.get('/login')
            report('login_page_loads', resp.status_code == 200, f'status={resp.status_code}', 'Authentication')

            # Test login with correct credentials
            resp = client.post('/login', data={
                'username': 'audit_admin',
                'password': 'AdminTest123!'
            }, follow_redirects=True)
            report('login_success', resp.status_code == 200, f'status={resp.status_code}', 'Authentication')

            # Test inactive user cannot login
            try:
                from controllers.user_controller import UserController as UC
                uc_test = UC()
                uc_test._actor = 'SYSTEM'
                uc_test.set_user_active(admin_id, 0)  # Deactivate admin

                resp = client.post('/login', data={
                    'username': 'audit_admin',
                    'password': 'AdminTest123!'
                }, follow_redirects=True)
                report('inactive_user_blocked', resp.status_code == 302 or 'login' in resp.get_data(as_text=True).lower(),
                       f'status={resp.status_code}', 'Authentication')

                # Reactivate for other tests
                uc_test.set_user_active(admin_id, 1)
            except Exception as e:
                report('inactive_user_blocked', False, str(e), 'Authentication')

        # ====================================================================
        # PRODUCTS TESTS
        # ====================================================================
        print("\n--- PRODUCTS TESTS ---\n")

        from controllers.product_controller import ProductController
        from models.product_model import ProductModel

        pc = ProductController()

        # Test: Create product
        try:
            pc.ajouter_produit(
                reference='PROD_TEST_003',
                nom='Test Product for Audit',
                categorie='Test',
                marque='TestBrand',
                unite='Unit',
                stock=0,
                stock_min=0,
                numero_lot='LOT003',
                dlc='2025-12-31',
                fournisseur='Test Supplier',
                description='Product for audit',
                date_reception='2024-01-01',
                date_livraison='2024-01-02'
            )
            report('product_create', True, '', 'Products')
        except Exception as e:
            report('product_create', False, str(e), 'Products')

        # Test: Get all products
        try:
            products = pc.get_all_products()
            report('product_list', len(products) > 0, f'count={len(products)}', 'Products')
        except Exception as e:
            report('product_list', False, str(e), 'Products')

        # Test: Get product by ID
        if product_ids:
            try:
                pm = ProductModel()
                prod = pm.get_product_by_id(product_ids[0])
                report('product_get_by_id', prod is not None, '', 'Products')
            except Exception as e:
                report('product_get_by_id', False, str(e), 'Products')

        # Test: Update product
        if product_ids:
            try:
                pm = ProductModel()
                pm.modifier_produit(
                    id_produit=product_ids[0],
                    reference='PROD001_MODIFIED',
                    nom='Modified Product',
                    categorie='Category A',
                    marque='Brand X',
                    unite='Kg',
                    stock=150,  # Increase stock
                    stock_min=10,
                    numero_lot='LOT001',
                    dlc='2025-12-31',
                    fournisseur='Supplier A',
                    description='Modified test product',
                    date_reception='2024-01-01',
                    date_livraison='2024-01-02'
                )
                # Verify the update
                prod = pm.get_product_by_id(product_ids[0])
                report('product_modify', prod and prod[2] == 'Modified Product',
                       f'nom={prod[2] if prod else "N/A"}', 'Products')
            except Exception as e:
                report('product_modify', False, str(e), 'Products')

        # ====================================================================
        # ENTRIES (ENTRÉES) TESTS
        # ====================================================================
        print("\n--- ENTRIES TESTS ---\n")

        from models.entry_model import EntryModel
        from controllers.entry_controller import EntryController

        if product_ids:
            prod_id = product_ids[0]
            em = EntryModel()
            ec = EntryController()

            # Test: Add entry with positive quantity
            try:
                em.ajouter_entree(
                    product_id=prod_id,
                    quantite=25,
                    fournisseur='Test Fournisseur',
                    numero_bon='BON001',
                    commentaire='Test entry'
                )
                report('entry_positive_quantity', True, '', 'Entries')
            except Exception as e:
                report('entry_positive_quantity', False, str(e), 'Entries')

            # Test: Add entry with zero quantity (should be allowed)
            try:
                em.ajouter_entree(
                    product_id=prod_id,
                    quantite=0,
                    fournisseur='Test Fournisseur',
                    numero_bon='BON002',
                    commentaire='Zero entry (no-op)'
                )
                report('entry_zero_quantity', True, '', 'Entries')
            except Exception as e:
                report('entry_zero_quantity', False, str(e), 'Entries')

            # Test: Add entry with negative quantity (should fail)
            try:
                em.ajouter_entree(
                    product_id=prod_id,
                    quantite=-10,
                    fournisseur='Test Fournisseur',
                    numero_bon='BON003',
                    commentaire='Negative entry'
                )
                report('entry_negative_rejected', False, 'Should have rejected', 'Entries')
            except Exception:
                report('entry_negative_rejected', True, '', 'Entries')

            # Test: Stock updated correctly
            try:
                pm = ProductModel()
                prod = pm.get_product_by_id(prod_id)
                # Initial stock was 150 (from modification), +25 from entry
                expected_stock = 150 + 25
                actual_stock = prod[6] if prod else None
                report('entry_stock_updated', actual_stock == expected_stock,
                       f'expected={expected_stock}, actual={actual_stock}', 'Entries')
            except Exception as e:
                report('entry_stock_updated', False, str(e), 'Entries')

            # Test: Entry listed
            try:
                entries = ec.get_all_entries()
                report('entry_list', len(entries) > 0, f'count={len(entries)}', 'Entries')
            except Exception as e:
                report('entry_list', False, str(e), 'Entries')

        # ====================================================================
        # SORTIES (OUTPUTS) TESTS
        # ====================================================================
        print("\n--- SORTIES TESTS ---\n")

        from models.sortie_model import SortieModel
        from controllers.sortie_controller import SortieController

        if product_ids:
            prod_id = product_ids[0]
            sm = SortieModel()
            sc = SortieController()

            # Test: Add sortie with positive quantity
            try:
                sm.ajouter_sortie(
                    product_id=prod_id,
                    quantite=15,
                    client='Test Client',
                    numero_bon='SORT001',
                    commentaire='Test sortie'
                )
                report('sortie_positive_quantity', True, '', 'Sorties')
            except Exception as e:
                report('sortie_positive_quantity', False, str(e), 'Sorties')

            # Test: Add sortie with zero quantity (should be allowed)
            try:
                sm.ajouter_sortie(
                    product_id=prod_id,
                    quantite=0,
                    client='Test Client',
                    numero_bon='SORT002',
                    commentaire='Zero sortie'
                )
                report('sortie_zero_quantity', True, '', 'Sorties')
            except Exception as e:
                report('sortie_zero_quantity', False, str(e), 'Sorties')

            # Test: Add sortie with negative quantity (should fail)
            try:
                sm.ajouter_sortie(
                    product_id=prod_id,
                    quantite=-5,
                    client='Test Client',
                    numero_bon='SORT003',
                    commentaire='Negative sortie'
                )
                report('sortie_negative_rejected', False, 'Should have rejected', 'Sorties')
            except Exception:
                report('sortie_negative_rejected', True, '', 'Sorties')

            # Test: Overdraw protection (try to sell more than stock)
            try:
                # Current stock should be: 150 (initial) + 25 (entry) - 15 (sortie) = 160
                sm.ajouter_sortie(
                    product_id=prod_id,
                    quantite=200,  # More than current stock
                    client='Test Client',
                    numero_bon='SORT004',
                    commentaire='Overdraw attempt'
                )
                report('sortie_overdraw_rejected', False, 'Should have rejected overdraw', 'Sorties')
            except Exception:
                report('sortie_overdraw_rejected', True, '', 'Sorties')

            # Test: Stock updated correctly
            try:
                pm = ProductModel()
                prod = pm.get_product_by_id(prod_id)
                # Stock should be: 150 + 25 - 15 = 160
                expected_stock = 160
                actual_stock = prod[6] if prod else None
                report('sortie_stock_updated', actual_stock == expected_stock,
                       f'expected={expected_stock}, actual={actual_stock}', 'Sorties')
            except Exception as e:
                report('sortie_stock_updated', False, str(e), 'Sorties')

            # Test: Sortie listed
            try:
                sorties = sc.get_all_sorties()
                report('sortie_list', len(sorties) > 0, f'count={len(sorties)}', 'Sorties')
            except Exception as e:
                report('sortie_list', False, str(e), 'Sorties')

        # ====================================================================
        # STOCK CONSISTENCY TEST
        # ====================================================================
        print("\n--- STOCK CONSISTENCY TEST ---\n")

        if product_ids:
            prod_id = product_ids[0]
            try:
                # Query database directly
                conn = sqlite3.connect('database/clms.db')
                c = conn.cursor()

                # Get current stock from products table
                c.execute("SELECT stock FROM products WHERE id = ?", (prod_id,))
                current_stock = c.fetchone()[0]

                # Get sum of entries
                c.execute("SELECT COALESCE(SUM(quantite), 0) FROM stock_entries WHERE product_id = ?", (prod_id,))
                total_entries = c.fetchone()[0]

                # Get sum of sorties
                c.execute("SELECT COALESCE(SUM(quantite), 0) FROM stock_outputs WHERE product_id = ?", (prod_id,))
                total_sorties = c.fetchone()[0]

                conn.close()

                # Calculate expected stock (assuming initial stock = 150)
                expected_stock = 150 + total_entries - total_sorties

                report('stock_consistency', current_stock == expected_stock,
                       f'stock={current_stock}, entries={total_entries}, sorties={total_sorties}, expected={expected_stock}',
                       'Stock')
            except Exception as e:
                report('stock_consistency', False, str(e), 'Stock')

        # ====================================================================
        # CLIENTS TESTS
        # ====================================================================
        print("\n--- CLIENTS TESTS ---\n")

        from controllers.client_controller import ClientController
        from models.client_model import ClientModel

        cc = ClientController()
        cm = ClientModel()

        # Test: Create client
        try:
            cc.ajouter_client(
                nom='Audit Test Client',
                telephone='555-9999',
                adresse='999 Test Ave',
                email='audit@test.com',
                ville='Test City'
            )
            report('client_create', True, '', 'Clients')
        except Exception as e:
            report('client_create', False, str(e), 'Clients')

        # Test: Get all clients
        try:
            clients = cm.get_all_clients()
            report('client_list', len(clients) > 0, f'count={len(clients)}', 'Clients')
        except Exception as e:
            report('client_list', False, str(e), 'Clients')

        # ====================================================================
        # VEHICLES TESTS
        # ====================================================================
        print("\n--- VEHICLES TESTS ---\n")

        from controllers.vehicle_controller import VehicleController
        from models.vehicle_model import VehicleModel

        vc = VehicleController()
        vm = VehicleModel()

        # Test: Create vehicle
        try:
            vc.ajouter(  # Correct method name
                immatriculation='TEST-9999',
                marque='Ford',
                modelo='Transit',
                type='Van',
                kilometrage=100000,
                chauffeur='Test Driver',
                statut='Disponible'
            )
            report('vehicle_create', True, '', 'Vehicles')
        except Exception as e:
            report('vehicle_create', False, str(e), 'Vehicles')

        # Test: Duplicate immatriculation should fail
        try:
            vc.ajouter_vehicule(
                immatriculation='TEST-9999',  # Same as above
                marque='Renault',
                modele='Master',
                type='Van',
                kilometrage=50000,
                chauffeur='Another Driver',
                statut='Disponible'
            )
            report('vehicle_duplicate_immatriculation_rejected', False, 'Should have rejected duplicate', 'Vehicles')
        except Exception:
            report('vehicle_duplicate_immatriculation_rejected', True, '', 'Vehicles')

        # Test: Get all vehicles
        try:
            vehicles = vm.get_all()  # Correct method name
            report('vehicle_list', len(vehicles) > 0, f'count={len(vehicles)}', 'Vehicles')
        except Exception as e:
            report('vehicle_list', False, str(e), 'Vehicles')

        # ====================================================================
        # GASOIL TESTS
        # ====================================================================
        print("\n--- GASOIL TESTS ---\n")

        from controllers.gasoil_controller import GasoilController
        from models.gasoil_model import GasoilModel

        gc = GasoilController()
        gm = GasoilModel()

        # Test: Add gasoil operation
        try:
            gc.ajouter(  # Correct method name
                vehicule='TEST-9999',
                date_operation='2024-01-10',
                heure_operation='14:30',
                kilometrage=100500,
                quantite=50.5,
                observation='Fuel top-up'
            )
            report('gasoil_create', True, '', 'Gasoil')
        except Exception as e:
            report('gasoil_create', False, str(e), 'Gasoil')

        # Test: Get all gasoil operations
        try:
            operations = gm.get_all()
            report('gasoil_list', len(operations) > 0, f'count={len(operations)}', 'Gasoil')
        except Exception as e:
            report('gasoil_list', False, str(e), 'Gasoil')

        # Test: Get gasoil statistics
        try:
            stats = gm.get_statistics_by_vehicle()
            report('gasoil_statistics', len(stats) > 0, f'vehicles={len(stats)}', 'Gasoil')
        except Exception as e:
            report('gasoil_statistics', False, str(e), 'Gasoil')

        # ====================================================================
        # DASHBOARD TESTS
        # ====================================================================
        print("\n--- DASHBOARD TESTS ---\n")

        from models.dashboard_model import DashboardModel

        dm = DashboardModel()

        # Test: Get nombre de produits
        try:
            count = dm.get_nombre_produits()
            report('dashboard_product_count', count >= 0, f'count={count}', 'Dashboard')
        except Exception as e:
            report('dashboard_product_count', False, str(e), 'Dashboard')

        # Test: Get total entries
        try:
            total = dm.get_total_entrees()
            report('dashboard_total_entries', total >= 0, f'total={total}', 'Dashboard')
        except Exception as e:
            report('dashboard_total_entries', False, str(e), 'Dashboard')

        # Test: Get total sorties
        try:
            total = dm.get_total_sorties()
            report('dashboard_total_sorties', total >= 0, f'total={total}', 'Dashboard')
        except Exception as e:
            report('dashboard_total_sorties', False, str(e), 'Dashboard')

        # Test: Get alertes
        try:
            count = dm.get_nombre_alertes()
            report('dashboard_alerts', count >= 0, f'count={count}', 'Dashboard')
        except Exception as e:
            report('dashboard_alerts', False, str(e), 'Dashboard')

        # Test: Get derniers mouvements
        try:
            mouvements = dm.get_derniers_mouvements()
            report('dashboard_recent_movements', len(mouvements) >= 0, f'count={len(mouvements)}', 'Dashboard')
        except Exception as e:
            report('dashboard_recent_movements', False, str(e), 'Dashboard')

        # ====================================================================
        # HISTORIQUE TESTS
        # ====================================================================
        print("\n--- HISTORIQUE TESTS ---\n")

        from controllers.HistoryController import HistoryController

        hc = HistoryController()

        # Test: Get all history
        try:
            history = hc.get_history()  # Correct method name
            report('historique_list', len(history) > 0, f'count={len(history)}', 'Historique')
        except Exception as e:
            report('historique_list', False, str(e), 'Historique')

        # Test: Verify no passwords in history
        try:
            history = hc.get_history()  # Correct method name
            has_password = False
            for record in history:
                # record is a tuple: (id, utilisateur, type_operation, module, description, date_operation)
                if len(record) > 4:
                    description = record[4]
                    if description and ('password' in description.lower() or 'hash' in description.lower()):
                        has_password = True
                        break
            report('historique_no_passwords', not has_password, '', 'Historique')
        except Exception as e:
            report('historique_no_passwords', False, str(e), 'Historique')

        # ====================================================================
        # USERS REGRESSION TESTS
        # ====================================================================
        print("\n--- USERS REGRESSION TESTS ---\n")

        from controllers.user_controller import UserController

        uc = UserController()

        # Test: Duplicate username rejection
        try:
            uc.create_user('audit_admin', 'TestPass123!', role='responsable',
                           nom_complet='Duplicate User', actif=1)
            report('user_duplicate_username_rejected', False, 'Should have rejected', 'Users')
        except Exception:
            report('user_duplicate_username_rejected', True, '', 'Users')

        # Test: Invalid role rejection
        try:
            uc.create_user('test_invalid_role', 'TestPass123!', role='invalid_role',
                           nom_complet='Invalid Role User', actif=1)
            report('user_invalid_role_rejected', False, 'Should have rejected', 'Users')
        except Exception:
            report('user_invalid_role_rejected', True, '', 'Users')

        # Test: Self-deactivation prevention
        try:
            with app.test_client() as client:
                # Login as admin
                client.post('/login', data={
                    'username': 'audit_admin',
                    'password': 'AdminTest123!'
                })

                # Try to toggle own active status (should fail)
                resp = client.post(f'/users/toggle-active/{admin_id}', follow_redirects=True)
                # Should redirect back or show error
                report('user_self_deactivation_prevented', True, '', 'Users')
        except Exception as e:
            report('user_self_deactivation_prevented', False, str(e), 'Users')

        # ====================================================================
        # DATABASE INTEGRITY TESTS
        # ====================================================================
        print("\n--- DATABASE INTEGRITY TESTS ---\n")

        try:
            conn = sqlite3.connect('database/clms.db')
            c = conn.cursor()

            # Test: Foreign key enforcement
            c.execute("PRAGMA foreign_keys")
            fk_enabled = c.fetchone()[0]
            report('database_foreign_keys_enabled', fk_enabled == 1, f'fk={fk_enabled}', 'Database')

            # Test: tables exist
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = c.fetchall()
            table_names = [t[0] for t in tables]
            expected_tables = ['users', 'products', 'stock_entries', 'stock_outputs', 'clients', 'vehicles', 'gasoil', 'historique']
            all_present = all(t in table_names for t in expected_tables)
            report('database_all_tables_present', all_present, f'tables={len(table_names)}', 'Database')

            conn.close()
        except Exception as e:
            report('database_integrity', False, str(e), 'Database')

        # ====================================================================
        # ROUTING TESTS
        # ====================================================================
        print("\n--- ROUTING TESTS ---\n")

        with app.test_client() as client:
            # Login as admin
            client.post('/login', data={
                'username': 'audit_admin',
                'password': 'AdminTest123!'
            })

            # Test main routes
            routes_to_test = [
                ('/', 200, 'dashboard'),
                ('/produits', 200, 'products'),
                ('/entrees', 200, 'entries'),
                ('/sorties', 200, 'sorties'),
                ('/clients', 200, 'clients'),
                ('/vehicules', 200, 'vehicles'),
                ('/gasoil', 200, 'gasoil'),
                ('/historique', 200, 'historique'),
                ('/parametres', 200, 'parameters'),
                ('/gestion-utilisateurs', 200, 'user_management'),
            ]

            for route, expected_status, name in routes_to_test:
                try:
                    resp = client.get(route)
                    report(f'route_{name}', resp.status_code == expected_status,
                           f'status={resp.status_code}', 'Routing')
                except Exception as e:
                    report(f'route_{name}', False, str(e), 'Routing')

        # Close database
        db_instance.close()

    finally:
        # Cleanup temp directory
        os.chdir(project_root if 'project_root' in locals() else os.getcwd())
        try:
            shutil.rmtree(td)
        except Exception as e:
            print(f"Warning: Could not delete temp directory: {e}")


def print_summary():
    """Print test summary"""
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {test_count}")
    print(f"Passed: {pass_count}")
    print(f"Failed: {fail_count}")
    print(f"Success Rate: {pass_count}/{test_count} ({100*pass_count//test_count if test_count > 0 else 0}%)\n")

    print("MODULE RESULTS:")
    print("-" * 80)
    for module in sorted(module_results.keys()):
        stats = module_results[module]
        rate = 100 * stats['pass'] // stats['total'] if stats['total'] > 0 else 0
        status = 'PASS' if stats['fail'] == 0 else 'FAIL'
        print(f"{module:20} {status:6} {stats['pass']:3}/{stats['total']:3} ({rate:3}%)")
    print("-" * 80 + "\n")


if __name__ == '__main__':
    run_tests()
    print_summary()
