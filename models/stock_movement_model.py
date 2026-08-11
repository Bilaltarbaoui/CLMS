import sqlite3


class StockMovementModel:

    def __init__(self):

        # =====================================================
        # DATABASE
        # =====================================================

        self.connection = sqlite3.connect(
            "database/clms.db"
        )

        self.cursor = self.connection.cursor()

        print("STOCK MOVEMENT MODEL = OK")

    # =====================================================
    # AFFICHER TOUS LES MOUVEMENTS
    # =====================================================

    def get_movements(self):

        self.cursor.execute("""

            SELECT

                'ENTREE' AS type_mouvement,

                products.reference,

                products.nom,

                stock_entries.quantite,

                stock_entries.fournisseur AS tiers,

                stock_entries.numero_bon,

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

                stock_outputs.numero_bon,

                stock_outputs.date_sortie AS date_mouvement

            FROM stock_outputs

            INNER JOIN products

                ON products.id = stock_outputs.product_id


            ORDER BY date_mouvement DESC

        """)

        return self.cursor.fetchall()

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self, mot):

        mot = mot.strip()

        if mot == "":

            return self.get_movements()

        recherche = f"%{mot}%"

        self.cursor.execute("""

            SELECT

                'ENTREE' AS type_mouvement,

                products.reference,

                products.nom,

                stock_entries.quantite,

                stock_entries.fournisseur AS tiers,

                stock_entries.numero_bon,

                stock_entries.date_reception AS date_mouvement

            FROM stock_entries

            INNER JOIN products

                ON products.id = stock_entries.product_id

            WHERE

                products.reference LIKE ?

                OR products.nom LIKE ?

                OR stock_entries.fournisseur LIKE ?

                OR stock_entries.numero_bon LIKE ?


            UNION ALL


            SELECT

                'SORTIE' AS type_mouvement,

                products.reference,

                products.nom,

                stock_outputs.quantite,

                stock_outputs.client AS tiers,

                stock_outputs.numero_bon,

                stock_outputs.date_sortie AS date_mouvement

            FROM stock_outputs

            INNER JOIN products

                ON products.id = stock_outputs.product_id

            WHERE

                products.reference LIKE ?

                OR products.nom LIKE ?

                OR stock_outputs.client LIKE ?

                OR stock_outputs.numero_bon LIKE ?


            ORDER BY date_mouvement DESC

        """, (

            recherche,
            recherche,
            recherche,
            recherche,

            recherche,
            recherche,
            recherche,
            recherche

        ))

        return self.cursor.fetchall()

    # =====================================================
    # FILTRE PAR TYPE
    # =====================================================

    def get_movements_filtre(self, type_mouvement):

        # =================================================
        # TOUS
        # =================================================

        if type_mouvement == "Tous":

            return self.get_movements()

        # =================================================
        # ENTREES
        # =================================================

        if type_mouvement == "Entrées":

            self.cursor.execute("""

                SELECT

                    'ENTREE' AS type_mouvement,

                    products.reference,

                    products.nom,

                    stock_entries.quantite,

                    stock_entries.fournisseur AS tiers,

                    stock_entries.numero_bon,

                    stock_entries.date_reception AS date_mouvement

                FROM stock_entries

                INNER JOIN products

                    ON products.id = stock_entries.product_id

                ORDER BY date_mouvement DESC

            """)

            return self.cursor.fetchall()

        # =================================================
        # SORTIES
        # =================================================

        if type_mouvement == "Sorties":

            self.cursor.execute("""

                SELECT

                    'SORTIE' AS type_mouvement,

                    products.reference,

                    products.nom,

                    stock_outputs.quantite,

                    stock_outputs.client AS tiers,

                    stock_outputs.numero_bon,

                    stock_outputs.date_sortie AS date_mouvement

                FROM stock_outputs

                INNER JOIN products

                    ON products.id = stock_outputs.product_id

                ORDER BY date_mouvement DESC

            """)

            return self.cursor.fetchall()

        # =================================================
        # TYPE INCONNU
        # =================================================

        return []

    # =====================================================
    # FERMER DATABASE
    # =====================================================

    def close(self):

        if self.connection:

            self.connection.close()

            print(
                "STOCK MOVEMENT DATABASE CLOSED"
            )