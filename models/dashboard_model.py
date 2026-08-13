import sqlite3

from database.database import Database


class DashboardModel:

    def __init__(self):

        self.connection = Database.get_safe_connection("database/clms.db")
        self.cursor = self.connection.cursor()

    # =====================================================
    # NOMBRE DE PRODUITS
    # =====================================================

    def get_nombre_produits(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)

        resultat = self.cursor.fetchone()

        return resultat[0]

    # =====================================================
    # TOTAL ENTREES
    # =====================================================

    def get_total_entrees(self):

        self.cursor.execute("""
            SELECT COALESCE(SUM(quantite), 0)
            FROM stock_entries
        """)

        resultat = self.cursor.fetchone()

        return resultat[0]

    # =====================================================
    # TOTAL SORTIES
    # =====================================================

    def get_total_sorties(self):

        self.cursor.execute("""
            SELECT COALESCE(SUM(quantite), 0)
            FROM stock_outputs
        """)

        resultat = self.cursor.fetchone()

        return resultat[0]

    # =====================================================
    # ALERTES STOCK MINIMUM
    # =====================================================

    def get_nombre_alertes(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE stock <= stock_min
        """)

        resultat = self.cursor.fetchone()

        return resultat[0]

    # =====================================================
    # DERNIERS MOUVEMENTS
    # =====================================================

    def get_derniers_mouvements(self):

        self.cursor.execute("""

            SELECT

                'ENTREE' AS type_mouvement,

                products.reference,

                products.nom,

                stock_entries.quantite,

                stock_entries.fournisseur AS tiers,

                stock_entries.date_reception AS date_mouvement

            FROM stock_entries

            INNER JOIN products

                ON products.id = stock_entries.product_id


            UNION ALL


            SELECT

                'SORTIE' AS type_mouvement,

                products.reference,

                products.nom,

                stock_outputs.quantite,

                stock_outputs.client AS tiers,

                stock_outputs.date_sortie AS date_mouvement

            FROM stock_outputs

            INNER JOIN products

                ON products.id = stock_outputs.product_id


            ORDER BY date_mouvement DESC

            LIMIT 10

        """)

        return self.cursor.fetchall()

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        self.connection.close()