from models.product_model import ProductModel


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

    # =====================================================
    # AFFICHER TOUS LES PRODUITS
    # =====================================================

    def get_all_products(self):

        return self.model.get_all_products()

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

    # =====================================================
    # SUPPRIMER PRODUIT
    # =====================================================

    def supprimer_produit(
        self,
        id_produit
    ):

        self.model.supprimer_produit(
            id_produit
        )

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