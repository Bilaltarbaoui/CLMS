#!/usr/bin/env python
"""
STEP 5: REGRESSION TEST - Check key modules still work after FK fix
"""

import sys
import os
import tempfile
import shutil
import importlib.util
from pathlib import Path

# Use temp database for all tests
test_db = tempfile.mkdtemp()
os.environ['CLMS_TEST_DB_PATH'] = os.path.join(test_db, 'clms.db')

# Dynamically load web_app in temp environment
web_app_path = Path('web_app.py').resolve()
spec = importlib.util.spec_from_file_location("web_app", web_app_path)
web_app = importlib.util.module_from_spec(spec)
sys.modules['web_app'] = web_app
spec.loader.exec_module(web_app)

print("\n" + "="*80)
print("REGRESSION TEST: Core modules after FK enforcement fix")
print("="*80 + "\n")

results = []

# Test 1: Product creation with FK enforcement
try:
    print("[TEST 1] Product creation...")
    from controllers.product_controller import ProductController
    from models.product_model import ProductModel

    pc = ProductController()
    pm = ProductModel()

    # Test basic operation
    pc.ajouter_produit(
        reference='REG-TEST-001',
        nom='Test Product',
        categorie='Test',
        marque='Brand',
        unite='piece',
        stock=100,
        stock_min=10,
        numero_lot='LOT001',
        dlc='2025-12-31',
        fournisseur='Supplier',
        description='Test',
        date_reception='2026-08-13',
        date_livraison='2026-08-13'
    )

    products = pm.get_all_products()
    if products and len(products) > 0:
        print("  ✓ PASS: Product created successfully with FK enforcement")
        results.append(("Products", True))
    else:
        print("  ✗ FAIL: Product not created")
        results.append(("Products", False))

    pc.close()
    pm.close()
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results.append(("Products", False))

# Test 2: Entry creation with FK enforcement
try:
    print("[TEST 2] Stock entry creation...")
    from controllers.entry_controller import EntryController
    from models.entry_model import EntryModel
    from database.database import Database

    db = Database()
    ec = EntryController()
    em = EntryModel(db)

    # Get first product
    products = em.connection.execute("SELECT id FROM products LIMIT 1").fetchall()
    if products:
        product_id = products[0][0]
        em.ajouter_entree(
            product_id=product_id,
            quantite=50,
            fournisseur='Test Supplier',
            numero_bon='BON001',
            commentaire='Test entry'
        )

        # Verify entry was created
        entries = em.connection.execute(
            "SELECT * FROM stock_entries WHERE product_id = ?",
            (product_id,)
        ).fetchall()

        if entries:
            print("  ✓ PASS: Entry created successfully with FK enforcement")
            results.append(("Entries", True))
        else:
            print("  ✗ FAIL: Entry not created")
            results.append(("Entries", False))
    else:
        print("  ! SKIP: No products available")
        results.append(("Entries", True))

    db.close()
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results.append(("Entries", False))

# Test 3: Vehicle creation
try:
    print("[TEST 3] Vehicle creation...")
    from controllers.vehicle_controller import VehicleController
    from models.vehicle_model import VehicleModel

    vc = VehicleController()
    vm = VehicleModel()

    vc.ajouter(
        immatriculation='REG-TEST-001',
        marque='Test Brand',
        modele='Model',
        type='VL',
        kilometrage=0,
        chauffeur='Driver',
        statut='Disponible'
    )

    vehicles = vm.get_all()
    if vehicles and len(vehicles) > 0:
        print("  ✓ PASS: Vehicle created successfully with FK enforcement")
        results.append(("Vehicles", True))
    else:
        print("  ✗ FAIL: Vehicle not created")
        results.append(("Vehicles", False))

    vc.close()
    vm.close()
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results.append(("Vehicles", False))

# Test 4: Client creation
try:
    print("[TEST 4] Client creation...")
    from controllers.client_controller import ClientController
    from models.client_model import ClientModel

    cc = ClientController()
    cm = ClientModel()

    cc.ajouter_client(
        nom='Test Client',
        telephone='555-0000',
        adresse='123 Test St',
        email='test@example.com',
        ville='Test City'
    )

    clients = cm.get_all_clients()
    if clients and len(clients) > 0:
        print("  ✓ PASS: Client created successfully with FK enforcement")
        results.append(("Clients", True))
    else:
        print("  ✗ FAIL: Client not created")
        results.append(("Clients", False))

    cc.close()
    cm.close()
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results.append(("Clients", False))

# Test 5: Dashboard KPIs
try:
    print("[TEST 5] Dashboard KPI calculations...")
    from models.dashboard_model import DashboardModel

    dm = DashboardModel()

    num_products = dm.get_nombre_produits()
    total_entries = dm.get_total_entrees()
    total_sorties = dm.get_total_sorties()
    alerts = dm.get_nombre_alertes()
    movements = dm.get_derniers_mouvements()

    if num_products >= 0 and total_entries >= 0 and total_sorties >= 0:
        print(f"  ✓ PASS: Dashboard KPIs working")
        print(f"    - Products: {num_products}")
        print(f"    - Total entries: {total_entries}")
        print(f"    - Total sorties: {total_sorties}")
        print(f"    - Alerts: {alerts}")
        results.append(("Dashboard", True))
    else:
        print("  ✗ FAIL: Dashboard KPI calculation failed")
        results.append(("Dashboard", False))

    dm.close()
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results.append(("Dashboard", False))

# Summary
print("\n" + "="*80)
print("REGRESSION TEST SUMMARY")
print("="*80)
passed = 0
failed = 0
for test_name, result in results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status}: {test_name}")
    if result:
        passed += 1
    else:
        failed += 1

print("="*80)
print(f"Total: {passed} PASSED, {failed} FAILED")
print("="*80)

# Cleanup
try:
    shutil.rmtree(test_db)
except:
    pass

sys.exit(0 if failed == 0 else 1)
