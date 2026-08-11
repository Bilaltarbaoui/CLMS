from models.entry_model import EntryModel


class EntryController:

    def __init__(self):

        self.model = EntryModel()

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

        # Vérifier quantité

        try:

            quantite = int(quantite)

        except (ValueError, TypeError):

            raise Exception(
                "La quantité doit être un nombre entier."
            )

        # Vérifier quantité positive

        if quantite <= 0:

            raise Exception(
                "La quantité doit être supérieure à 0."
            )

        # Vérifier produit

        if product_id is None:

            raise Exception(
                "Veuillez sélectionner un produit."
            )

        # Ajouter

        self.model.ajouter_entree(
            product_id,
            quantite,
            fournisseur,
            numero_bon,
            commentaire
        )

    # =====================================================
    # AFFICHER TOUTES LES ENTREES
    # =====================================================

    def get_all_entries(self):

        return self.model.get_all_entries()

    # =====================================================
    # COMPATIBILITE DASHBOARD
    # =====================================================

    def get_all(self):

        return self.get_all_entries()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        try:

            self.model.close()

        except Exception:

            pass