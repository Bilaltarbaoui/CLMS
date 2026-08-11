import sqlite3


class InventoryModel:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/clms.db"
        )

        self.cursor = self.connection.cursor()

    # =====================================================
    # AFFICHER INVENTAIRE
    # =====================================================

    def get_inventory(self):

        self.cursor.execute("""

            SELECT
                id,
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

            FROM products

            ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self, mot):

        self.cursor.execute("""

            SELECT
                id,
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

            FROM products

            WHERE
                reference LIKE ?
                OR nom LIKE ?
                OR categorie LIKE ?

            ORDER BY id DESC

        """, (

            f"%{mot}%",
            f"%{mot}%",
            f"%{mot}%"

        ))

        return self.cursor.fetchall()

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        self.connection.close()