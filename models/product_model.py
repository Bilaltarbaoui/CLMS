import sqlite3
from datetime import datetime

from database.database import Database


class ProductModel:

    def __init__(self):

        self.connection = Database.get_safe_connection("database/clms.db")
        self.cursor = self.connection.cursor()

    # =====================================================
    # AJOUTER
    # =====================================================

    def ajouter_produit(
        self,
        reference,
        nom,
        categorie,
        marque,
        unite,
        stock,
        stock_min,
        numero_lot,
        dlc,
        fournisseur,
        description,
        date_reception,
        date_livraison
    ):

        date_creation = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(
            """
            INSERT INTO products (
                reference,
                nom,
                categorie,
                marque,
                unite,
                stock,
                stock_min,
                numero_lot,
                dlc,
                fournisseur,
                description,
                date_creation,
                date_reception,
                date_livraison
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reference,
                nom,
                categorie,
                marque,
                unite,
                stock,
                stock_min,
                numero_lot,
                dlc,
                fournisseur,
                description,
                date_creation,
                date_reception,
                date_livraison
            )
        )

        self.connection.commit()

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_all_products(self):

        self.cursor.execute(
            """
            SELECT *
            FROM products
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    # =====================================================
    # MODIFIER
    # =====================================================

    
    def modifier_produit(
        self,
        id_produit,
        reference,
        nom,
        categorie,
        marque,
        unite,
        stock,
        stock_min,
        numero_lot,
        dlc,
        fournisseur,
        description,
        date_reception,
        date_livraison
):

        self.cursor.execute(
            """
            UPDATE products
            SET
            reference = ?,
            nom = ?,
            categorie = ?,
            marque = ?,
            unite = ?,
            stock = ?,
            stock_min = ?,
            numero_lot = ?,
            dlc = ?,
            fournisseur = ?,
            description = ?,
            date_reception = ?,
            date_livraison = ?
        WHERE id = ?
        """,
        (
            reference,
            nom,
            categorie,
            marque,
            unite,
            stock,
            stock_min,
            numero_lot,
            dlc,
            fournisseur,
            description,
            date_reception,
            date_livraison,
            id_produit
        )
    )

        self.connection.commit()



    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer_produit(self, id_produit):

        self.cursor.execute(
            """
            DELETE FROM products
            WHERE id = ?
            """,
            (id_produit,)
        )

        self.connection.commit()

    # =====================================================
    # RECHERCHER
    # =====================================================

    def rechercher_produit(self, mot):

        self.cursor.execute(
            """
            SELECT *
            FROM products
            WHERE
                reference LIKE ?
                OR nom LIKE ?
                OR categorie LIKE ?
                OR marque LIKE ?
                OR unite LIKE ?
                OR numero_lot LIKE ?
                OR fournisseur LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{mot}%",
                f"%{mot}%",
                f"%{mot}%",
                f"%{mot}%",
                f"%{mot}%",
                f"%{mot}%",
                f"%{mot}%"
            )
        )

        return self.cursor.fetchall()

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        if getattr(self, 'connection', None):

            try:
                self.connection.close()
            except Exception:
                pass