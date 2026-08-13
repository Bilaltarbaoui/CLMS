from models.product_model import ProductModel
from database.database import Database


class ProductController:

    def __init__(self):

        self.model = ProductModel()

    # =====================================================
    # AJOUTER PRODUIT
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

        self.model.ajouter_produit(
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
        )
        # Log history
        try:
            db = Database()
            desc = f"Produit {reference} - {nom} créé"
            db.ajouter_historique("SYSTEM", "CREATE", "Produit", desc)
        except Exception:
            pass

    # =====================================================
    # AFFICHER TOUS LES PRODUITS
    # =====================================================

    def get_all_products(self):

        return self.model.get_all_products()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        if getattr(self, 'model', None) and hasattr(self.model, 'close'):

            try:
                self.model.close()
            except Exception:
                pass

    # =====================================================
    # COMPATIBILITE DASHBOARD
    # =====================================================
    # Dashboard utilise get_all()
    # donc on ajoute cette methode.

    def get_all(self):

        return self.model.get_all_products()

    # =====================================================
    # MODIFIER PRODUIT
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

        self.model.modifier_produit(
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
        )
        # Log history
        try:
            db = Database()
            desc = f"Produit {reference} - {nom} modifié (id={id_produit})"
            db.ajouter_historique("SYSTEM", "UPDATE", "Produit", desc)
        except Exception:
            pass

    # =====================================================
    # SUPPRIMER PRODUIT
    # =====================================================

    def supprimer_produit(
        self,
        id_produit
    ):

        # Fetch product info for description
        try:
            # Attempt to read product before deletion for description
            prod = next((p for p in self.get_all_products() if p[0] == id_produit), None)
            reference = prod[1] if prod else ''
            nom = prod[2] if prod else ''
        except Exception:
            reference = ''
            nom = ''

        self.model.supprimer_produit(
            id_produit
        )

        # Log history
        try:
            db = Database()
            desc = f"Produit {reference} - {nom} supprimé (id={id_produit})"
            db.ajouter_historique("SYSTEM", "DELETE", "Produit", desc)
        except Exception:
            pass

    # =====================================================
    # RECHERCHE PRODUIT
    # =====================================================

    def rechercher_produit(
        self,
        mot
    ):

        return self.model.rechercher_produit(
            mot
        )
    # =====================================================
# AFFICHER TOUS LES PRODUITS
# =====================================================

    def get_all_products(self):

        return self.model.get_all_products()


# =====================================================
# COMPATIBILITE DASHBOARD
# =====================================================

    def get_all(self):

        return self.model.get_all_products()