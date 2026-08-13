import sqlite3
from datetime import datetime

from database.database import Database


class SortieModel:

    def __init__(self):

        self.database = Database()
        self.connection = self.database.connection
        self.cursor = self.database.cursor

    # =====================================================
    # AJOUTER UNE SORTIE
    # =====================================================

    def ajouter_sortie(

        self,
        product_id,
        quantite,
        client,
        numero_bon,
        commentaire

    ):

        # Validate quantity: must be a positive integer
        try:
            quantite = int(quantite)
        except Exception:
            raise Exception("La quantité doit être un nombre entier.")

        # Allow zero (no-op) but reject negative quantities
        if quantite < 0:
            raise Exception("La quantité doit être supérieure ou égale à 0.")

        # Serialize write-heavy operations to avoid SQLite write contention in-process
        from database.database import Database as _DatabaseClass

        with _DatabaseClass._write_lock:

            try:

                # Vérifier le stock actuel
                self.cursor.execute(
                    "SELECT stock FROM products WHERE id=?",
                    (product_id,)
                )

                resultat = self.cursor.fetchone()

                if resultat is None:
                    raise Exception("Produit introuvable.")

                stock_actuel = int(resultat[0])

                if quantite > stock_actuel:
                    raise Exception("Stock insuffisant.")

                date_sortie = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Enregistrer la sortie
                self.cursor.execute("""
                INSERT INTO stock_outputs(
                    product_id,
                    quantite,
                    client,
                    numero_bon,
                    commentaire,
                    date_sortie
                ) VALUES(?,?,?,?,?,?)
                """, (
                    product_id,
                    quantite,
                    client,
                    numero_bon,
                    commentaire,
                    date_sortie
                ))

                # Diminuer le stock
                self.cursor.execute("""
                UPDATE products
                SET stock = stock - ?
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
                    description = f"Sortie de {quantite} pour le produit {reference} - {nom}"
                elif reference:
                    description = f"Sortie de {quantite} pour le produit {reference}"
                elif nom:
                    description = f"Sortie de {quantite} pour le produit {nom}"
                else:
                    description = f"Sortie de {quantite} pour le produit {product_id}"

                self.database.ajouter_historique(
                    "SYSTEM",
                    "SORTIE",
                    "Sortie",
                    description,
                    commit=False
                )

                try:
                    self.database.commit_with_retry()
                except Exception:
                    # fallback
                    self.connection.commit()

            except Exception:
                self.connection.rollback()
                raise

    # =====================================================
    # AFFICHER LES SORTIES
    # =====================================================

    def get_all_sorties(self):

        self.cursor.execute("""

        SELECT

            stock_outputs.id,

            products.reference,

            products.nom,

            stock_outputs.quantite,

            stock_outputs.client,

            stock_outputs.numero_bon,

            stock_outputs.date_sortie

        FROM stock_outputs

        INNER JOIN products

        ON products.id = stock_outputs.product_id

        ORDER BY stock_outputs.id DESC

        """)

        return self.cursor.fetchall()