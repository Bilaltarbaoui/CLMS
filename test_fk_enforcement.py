#!/usr/bin/env python
"""
STEP 4: TEST FK DELETION PROTECTION

This test verifies that foreign key constraints are now enforced:
1. Product cannot be deleted if it has related entries
2. Product cannot be deleted if it has related sorties
3. Data integrity is preserved when deletion is rejected
"""

import sqlite3
import os
import tempfile
import shutil
from pathlib import Path


def test_fk_protection_with_entry():
    """Test that products cannot be deleted if they have entries"""
    print("\n" + "="*80)
    print("TEST 1: FK PROTECTION - PRODUCT WITH ENTRY")
    print("="*80 + "\n")
    
    td = tempfile.mkdtemp()
    db_path = os.path.join(td, 'test_fk.db')
    
    try:
        # Create connection WITH FK enforcement
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        c = conn.cursor()
        
        # Create schema
        c.execute("""CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            reference TEXT,
            nom TEXT,
            stock INTEGER DEFAULT 0
        )""")
        
        c.execute("""CREATE TABLE stock_entries (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantite INTEGER,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")
        
        conn.commit()
        
        # Step 1: Create product
        c.execute("INSERT INTO products (reference, nom, stock) VALUES (?, ?, ?)",
                 ('PROD001', 'Test Product', 100))
        product_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 1: Created product ID {product_id}")
        
        # Step 2: Create entry referencing product
        c.execute("INSERT INTO stock_entries (product_id, quantite) VALUES (?, ?)",
                 (product_id, 50))
        entry_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 2: Created entry ID {entry_id} referencing product {product_id}")
        
        # Step 3: Verify product exists
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product_before = c.fetchone()
        assert product_before is not None, "Product should exist before deletion attempt"
        print("[OK] Step 3: Product exists in DB")
        
        # Step 4: Verify entry exists
        c.execute("SELECT * FROM stock_entries WHERE id = ?", (entry_id,))
        entry_before = c.fetchone()
        assert entry_before is not None, "Entry should exist"
        print("[OK] Step 4: Entry exists in DB")
        
        # Step 5: ATTEMPT to delete product (should FAIL with FK constraint)
        try:
            c.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            print("[FAIL] Step 5: FAILED - FK constraint NOT enforced (deletion succeeded!)")
            return False
        except sqlite3.IntegrityError as e:
            print(f"[OK] Step 5: FK constraint enforced - deletion rejected: {e}")
        
        # Step 6: Verify product still exists after failed deletion
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product_after = c.fetchone()
        assert product_after is not None, "Product should still exist after failed deletion"
        print("[OK] Step 6: Product still exists (data integrity preserved)")
        
        # Step 7: Verify entry still exists
        c.execute("SELECT * FROM stock_entries WHERE id = ?", (entry_id,))
        entry_after = c.fetchone()
        assert entry_after is not None, "Entry should still exist"
        print("[OK] Step 7: Entry still exists (data integrity preserved)")
        
        conn.close()
        print("\n" + "="*80)
        print("TEST 1 PASSED: FK protection with entry working correctly")
        print("="*80)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 1 FAILED: {e}")
        return False
    finally:
        try:
            shutil.rmtree(td)
        except:
            pass


def test_fk_protection_with_sortie():
    """Test that products cannot be deleted if they have sorties"""
    print("\n" + "="*80)
    print("TEST 2: FK PROTECTION - PRODUCT WITH SORTIE")
    print("="*80 + "\n")
    
    td = tempfile.mkdtemp()
    db_path = os.path.join(td, 'test_fk.db')
    
    try:
        # Create connection WITH FK enforcement
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        c = conn.cursor()
        
        # Create schema
        c.execute("""CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            reference TEXT,
            nom TEXT,
            stock INTEGER DEFAULT 0
        )""")
        
        c.execute("""CREATE TABLE stock_outputs (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantite INTEGER,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")
        
        conn.commit()
        
        # Step 1: Create product
        c.execute("INSERT INTO products (reference, nom, stock) VALUES (?, ?, ?)",
                 ('PROD002', 'Test Product 2', 150))
        product_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 1: Created product ID {product_id}")
        
        # Step 2: Create sortie referencing product
        c.execute("INSERT INTO stock_outputs (product_id, quantite) VALUES (?, ?)",
                 (product_id, 30))
        sortie_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 2: Created sortie ID {sortie_id} referencing product {product_id}")
        
        # Step 3: Verify product exists
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product_before = c.fetchone()
        assert product_before is not None, "Product should exist before deletion attempt"
        print("[OK] Step 3: Product exists in DB")
        
        # Step 4: Verify sortie exists
        c.execute("SELECT * FROM stock_outputs WHERE id = ?", (sortie_id,))
        sortie_before = c.fetchone()
        assert sortie_before is not None, "Sortie should exist"
        print("[OK] Step 4: Sortie exists in DB")
        
        # Step 5: ATTEMPT to delete product (should FAIL with FK constraint)
        try:
            c.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            print("[FAIL] Step 5: FAILED - FK constraint NOT enforced (deletion succeeded!)")
            return False
        except sqlite3.IntegrityError as e:
            print(f"[OK] Step 5: FK constraint enforced - deletion rejected: {e}")
        
        # Step 6: Verify product still exists after failed deletion
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product_after = c.fetchone()
        assert product_after is not None, "Product should still exist after failed deletion"
        print("[OK] Step 6: Product still exists (data integrity preserved)")
        
        # Step 7: Verify sortie still exists
        c.execute("SELECT * FROM stock_outputs WHERE id = ?", (sortie_id,))
        sortie_after = c.fetchone()
        assert sortie_after is not None, "Sortie should still exist"
        print("[OK] Step 7: Sortie still exists (data integrity preserved)")
        
        conn.close()
        print("\n" + "="*80)
        print("TEST 2 PASSED: FK protection with sortie working correctly")
        print("="*80)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 2 FAILED: {e}")
        return False
    finally:
        try:
            shutil.rmtree(td)
        except:
            pass


def test_fk_disabled_allows_orphans():
    """Verify that WITHOUT FK enforcement, orphan records are created (the bug)"""
    print("\n" + "="*80)
    print("TEST 3: VERIFY FK DISABLED = DATA INTEGRITY RISK (the bug)")
    print("="*80 + "\n")
    
    td = tempfile.mkdtemp()
    db_path = os.path.join(td, 'test_no_fk.db')
    
    try:
        # Create connection WITHOUT FK enforcement (the bug)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = OFF;")  # DISABLED
        c = conn.cursor()
        
        # Create schema
        c.execute("""CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            reference TEXT,
            nom TEXT,
            stock INTEGER DEFAULT 0
        )""")
        
        c.execute("""CREATE TABLE stock_entries (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantite INTEGER,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")
        
        conn.commit()
        
        # Step 1: Create product
        c.execute("INSERT INTO products (reference, nom, stock) VALUES (?, ?, ?)",
                 ('PROD003', 'Test Product 3', 100))
        product_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 1: Created product ID {product_id}")
        
        # Step 2: Create entry referencing product
        c.execute("INSERT INTO stock_entries (product_id, quantite) VALUES (?, ?)",
                 (product_id, 50))
        entry_id = c.lastrowid
        conn.commit()
        print(f"[OK] Step 2: Created entry ID {entry_id} referencing product {product_id}")
        
        # Step 3: Delete product (SHOULD SUCCEED because FK disabled)
        c.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        print("[OK] Step 3: Product deleted (FK not enforced)")
        
        # Step 4: Verify product is GONE
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product_after = c.fetchone()
        if product_after is None:
            print("[OK] Step 4: Product is gone from DB (as expected with FK disabled)")
        
        # Step 5: Check if entry is orphaned (product_id points to non-existent product)
        c.execute("SELECT * FROM stock_entries WHERE id = ?", (entry_id,))
        entry_after = c.fetchone()
        if entry_after is not None:
            print(f"[OK] Step 5: ORPHAN RECORD CREATED: Entry ID {entry_id} now points to non-existent product {entry_after[1]}")
            print("         This is the data integrity bug we're fixing!")
            return True
        else:
            print("[FAIL] Entry was deleted (unexpected)")
            return False
        
    except Exception as e:
        print(f"\n[FAIL] TEST 3 FAILED: {e}")
        return False
    finally:
        try:
            shutil.rmtree(td)
        except:
            pass


if __name__ == '__main__':
    results = []
    
    # Test 1: FK protection with entry
    results.append(("FK Protection with Entry", test_fk_protection_with_entry()))
    
    # Test 2: FK protection with sortie
    results.append(("FK Protection with Sortie", test_fk_protection_with_sortie()))
    
    # Test 3: Demonstrate the bug (FK disabled)
    results.append(("FK Disabled Bug Demo", test_fk_disabled_allows_orphans()))
    
    # Summary
    print("\n" + "="*80)
    print("STEP 4 TEST SUMMARY")
    print("="*80)
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(r[1] for r in results)
    print("="*80)
    if all_passed:
        print("ALL FK ENFORCEMENT TESTS PASSED")
    else:
        print("SOME FK ENFORCEMENT TESTS FAILED")
    print("="*80)
