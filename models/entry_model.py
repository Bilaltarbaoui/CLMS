import sqlite3
from datetime import datetime

from database.database import Database


class EntryModel:

    def __init__(self):

        self.database = Database()
        self.connection = self.database.connection
        self.cursor = self.database.cursor

    # =====================================================
    # AJOUTER UNE ENTREE
    # =====================================================

    def ajouter_entree(

        self,
        product_id,
        quantite,
        fournisseur,
        numero_bon,
        commentaire

    ):

        date_reception = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:

            # Enregistrer l'entrée

            self.cursor.execute("""

            INSERT INTO stock_entries(

                product_id,
                quantite,
                fournisseur,
                numero_bon,
                commentaire,
                date_reception

            )

            VALUES(?,?,?,?,?,?)

            """, (

                product_id,
                quantite,
                fournisseur,
                numero_bon,
                commentaire,
                date_reception

            ))

            # Mise à jour du stock

            self.cursor.execute("""

            UPDATE products

            SET stock = stock + ?

            WHERE id = ?

            """, (

                quantite,
                product_id

            ))

            produit = self.cursor.execute(
                "SELECT reference, nom FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()

            if produit is None:
                reference = ""
                nom = ""
            else:
                reference = produit[0] or ""
                nom = produit[1] or ""

            if reference and nom:
                description = f"Entrée de {quantite} pour le produit {reference} - {nom}"
            elif reference:
                description = f"Entrée de {quantite} pour le produit {reference}"
            elif nom:
                description = f"Entrée de {quantite} pour le produit {nom}"
            else:
                description = f"Entrée de {quantite} pour le produit {product_id}"

            self.database.ajouter_historique(
                "SYSTEM",
                "ENTREE",
                "Entrees",
                description,
                commit=False
            )

            self.connection.commit()

        except Exception:

            self.connection.rollback()
            raise

    # =====================================================
    # AFFICHER LES ENTREES
    # =====================================================

    def get_all_entries(self):

        self.cursor.execute("""

        SELECT

            stock_entries.id,

            products.reference,

            products.nom,

            stock_entries.quantite,

            stock_entries.fournisseur,

            stock_entries.numero_bon,

            stock_entries.commentaire,

            stock_entries.date_reception

        FROM stock_entries

        INNER JOIN products

        ON products.id = stock_entries.product_id

        ORDER BY stock_entries.id DESC

        """)

        return self.cursor.fetchall()