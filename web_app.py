from flask import Flask, render_template, request, redirect, url_for, flash, session
from controllers.dashboard_controller import DashboardController
from controllers.vehicle_controller import VehicleController
from controllers.gasoil_controller import GasoilController
from controllers.client_controller import ClientController
from controllers.product_controller import ProductController
from controllers.entry_controller import EntryController
from controllers.sortie_controller import SortieController
from controllers.HistoryController import HistoryController
from controllers.user_controller import UserController
import functools
from flask import abort
from database.database import Database
import os
import secrets

app = Flask(__name__)

# Use environment variable for secret key, fallback to a random one for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Disable Jinja2 template caching in development/debug mode
# In production, caching is enabled by default (good for performance)
if os.environ.get('FLASK_ENV') == 'development':
    app.jinja_env.cache = None

APP_NAME = 'CLMS'
APP_VERSION = '1.0.0'

# Ensure database schema exists and is initialized before handling requests.
database = Database()


# ------------------------
# Authentication helpers
# ------------------------
@app.before_request
def require_login():
    # Allow access to static assets, login/logout, a-propos, and auth-debug
    allowed_paths = ('/login', '/logout', '/a-propos', '/auth-debug')
    # Diagnostic print to confirm this guard runs in the real server
    try:
        session_username = session.get('username')
    except Exception:
        session_username = None

    authenticated = bool(session_username)
    print(f"AUTH CHECK: request.path = {request.path} | session_username = {session_username} | authenticated = {authenticated}")

    if request.path.startswith('/static') or request.path in allowed_paths:
        return None

    # If user not authenticated, redirect to login
    if not authenticated:
        return redirect(url_for('login'))


# =====================================================
# Role-based access decorator (defined early so routes can use it)
# =====================================================
def require_role(*allowed_roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            username = session.get('username')
            if not username:
                return redirect(url_for('login'))

            uc = UserController()
            try:
                user = uc.get_user_by_username(username)
                if not user:
                    # user no longer exists
                    session.pop('username', None)
                    return redirect(url_for('login'))
                if not user.get('actif'):
                    # inactive
                    session.pop('username', None)
                    flash('Compte inactif. Contactez l\'administrateur.', 'error')
                    return redirect(url_for('login'))
                if allowed_roles and user.get('role') not in allowed_roles:
                    # Authenticated but insufficient role: return 403 Forbidden
                    return abort(403)
                return f(*args, **kwargs)
            finally:
                uc.close()

        return wrapped
    return decorator


@app.context_processor
def inject_current_role():
    """Expose `current_role` to all templates using session['username']."""
    username = session.get('username')
    if not username:
        return {'current_role': None}

    uc = UserController()
    try:
        user = uc.get_user_by_username(username)
        if not user:
            return {'current_role': None}
        return {'current_role': user.get('role')}
    finally:
        uc.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db = Database()
        try:
            if db.verify_and_migrate_password(username, password):
                session['username'] = username
                flash('Connexion réussie.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Nom d\'utilisateur ou mot de passe invalide.', 'error')
        except Exception as e:
            flash('Erreur lors de la connexion.', 'error')

    return render_template('login.html', title='Connexion')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Déconnecté.', 'success')
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    dashboard_controller = DashboardController()
    vehicle_controller = VehicleController()
    gasoil_controller = GasoilController()

    try:
        data = {
            'produits': dashboard_controller.get_nombre_produits(),
            'total_entrees': dashboard_controller.get_total_entrees(),
            'total_sorties': dashboard_controller.get_total_sorties(),
            'alertes': dashboard_controller.get_nombre_alertes(),
            'mouvements': dashboard_controller.get_derniers_mouvements(),
        }

        vehicle_stats = vehicle_controller.get_statistics()
        data['vehicules'] = vehicle_stats.get('total', 0)
        data['total_gasoil'] = gasoil_controller.get_total_gasoil() or 0

        return render_template('dashboard.html', data=data, title='Dashboard', active='dashboard')
    finally:
        dashboard_controller.close()
        vehicle_controller.close()
        gasoil_controller.close()

@app.route('/clients')
@require_role('admin', 'responsable')
def clients():
    controller = ClientController()
    query = request.args.get('q', '').strip()
    edit_id = request.args.get('edit_id')
    selected_client = None

    try:
        if query:
            clients = controller.rechercher_client(query)
        else:
            clients = controller.get_all_clients()

        if edit_id:
            try:
                selected_id = int(edit_id)
                selected_client = next((c for c in clients if c[0] == selected_id), None)
            except ValueError:
                selected_client = None

        return render_template(
            'clients.html',
            title='Clients',
            active='clients',
            clients=clients,
            selected_client=selected_client,
            query=query
        )
    finally:
        controller.close()

@app.route('/clients/add', methods=['POST'])
@require_role('admin', 'responsable')
def add_client():
    controller = ClientController()

    try:
        nom = request.form.get('nom', '').strip()
        telephone = request.form.get('telephone', '').strip()
        adresse = request.form.get('adresse', '').strip()
        email = request.form.get('email', '').strip()
        ville = request.form.get('ville', '').strip()

        if not nom:
            flash('Le nom du client est requis.', 'error')
            return redirect(url_for('clients'))

        controller.ajouter_client(nom, telephone, adresse, email, ville)
        flash('Client ajouté avec succès.', 'success')
        return redirect(url_for('clients'))
    finally:
        controller.close()

@app.route('/clients/edit/<int:id_client>', methods=['POST'])
@require_role('admin', 'responsable')
def edit_client(id_client):
    controller = ClientController()

    try:
        nom = request.form.get('nom', '').strip()
        telephone = request.form.get('telephone', '').strip()
        adresse = request.form.get('adresse', '').strip()
        email = request.form.get('email', '').strip()
        ville = request.form.get('ville', '').strip()

        if not nom:
            flash('Le nom du client est requis.', 'error')
            return redirect(url_for('clients', edit_id=id_client))

        controller.modifier_client(id_client, nom, telephone, adresse, email, ville)
        flash('Client modifié avec succès.', 'success')
        return redirect(url_for('clients'))
    finally:
        controller.close()

@app.route('/clients/delete/<int:id_client>', methods=['POST'])
@require_role('admin', 'responsable')
def delete_client(id_client):
    controller = ClientController()

    try:
        controller.supprimer_client(id_client)
        flash('Client supprimé avec succès.', 'success')
        return redirect(url_for('clients'))
    finally:
        controller.close()

@app.route('/produits')
@require_role('admin', 'responsable', 'magasinier')
def produits():
    controller = ProductController()
    query = request.args.get('q', '').strip()
    edit_id = request.args.get('edit_id')
    selected_product = None

    try:
        if query:
            produits = controller.rechercher_produit(query)
        else:
            produits = controller.get_all_products()

        if edit_id:
            try:
                selected_id = int(edit_id)
                selected_product = next((p for p in produits if p[0] == selected_id), None)
            except ValueError:
                selected_product = None

        return render_template(
            'produits.html',
            title='Produits',
            active='produits',
            produits=produits,
            selected_product=selected_product,
            query=query
        )
    finally:
        controller.close()

@app.route('/produits/add', methods=['POST'])
@require_role('admin', 'responsable', 'magasinier')
def add_produit():
    controller = ProductController()

    try:
        reference = request.form.get('reference', '').strip()
        nom = request.form.get('nom', '').strip()
        categorie = request.form.get('categorie', '').strip()
        marque = request.form.get('marque', '').strip()
        unite = request.form.get('unite', '').strip()
        stock = request.form.get('stock', '0').strip()
        stock_min = request.form.get('stock_min', '0').strip()
        numero_lot = request.form.get('numero_lot', '').strip()
        dlc = request.form.get('dlc', '').strip()
        fournisseur = request.form.get('fournisseur', '').strip()
        description = request.form.get('description', '').strip()
        date_reception = request.form.get('date_reception', '').strip()
        date_livraison = request.form.get('date_livraison', '').strip()

        if not nom:
            flash('Le nom du produit est requis.', 'error')
            return redirect(url_for('produits'))

        controller.ajouter_produit(
            reference,
            nom,
            categorie,
            marque,
            unite,
            int(stock or 0),
            int(stock_min or 0),
            numero_lot,
            dlc,
            fournisseur,
            description,
            date_reception,
            date_livraison
        )
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('produits'))
    except ValueError:
        flash('Le stock et le stock minimum doivent être des nombres entiers.', 'error')
        return redirect(url_for('produits'))
    finally:
        controller.close()

@app.route('/produits/edit/<int:id_produit>', methods=['POST'])
@require_role('admin', 'responsable', 'magasinier')
def edit_produit(id_produit):
    controller = ProductController()

    try:
        reference = request.form.get('reference', '').strip()
        nom = request.form.get('nom', '').strip()
        categorie = request.form.get('categorie', '').strip()
        marque = request.form.get('marque', '').strip()
        unite = request.form.get('unite', '').strip()
        stock = request.form.get('stock', '0').strip()
        stock_min = request.form.get('stock_min', '0').strip()
        numero_lot = request.form.get('numero_lot', '').strip()
        dlc = request.form.get('dlc', '').strip()
        fournisseur = request.form.get('fournisseur', '').strip()
        description = request.form.get('description', '').strip()
        date_reception = request.form.get('date_reception', '').strip()
        date_livraison = request.form.get('date_livraison', '').strip()

        if not nom:
            flash('Le nom du produit est requis.', 'error')
            return redirect(url_for('produits', edit_id=id_produit))

        controller.modifier_produit(
            id_produit,
            reference,
            nom,
            categorie,
            marque,
            unite,
            int(stock or 0),
            int(stock_min or 0),
            numero_lot,
            dlc,
            fournisseur,
            description,
            date_reception,
            date_livraison
        )
        flash('Produit modifié avec succès.', 'success')
        return redirect(url_for('produits'))
    except ValueError:
        flash('Le stock et le stock minimum doivent être des nombres entiers.', 'error')
        return redirect(url_for('produits', edit_id=id_produit))
    finally:
        controller.close()

@app.route('/produits/delete/<int:id_produit>', methods=['POST'])
@require_role('admin', 'responsable')
def delete_produit(id_produit):
    controller = ProductController()
    try:
        controller.supprimer_produit(id_produit)
        flash('Produit supprimé avec succès.', 'success')
        return redirect(url_for('produits'))
    finally:
        controller.close()

@app.route('/entrees')
@require_role('admin', 'responsable', 'magasinier')
def entrees():
    controller = EntryController()
    product_controller = ProductController()
    query = request.args.get('q', '').strip()

    try:
        produits = product_controller.get_all_products()
        if query:
            entrees = controller.rechercher(query)
        else:
            entrees = controller.get_all_entries()

        return render_template(
            'entrees.html',
            title='Entrées',
            active='entrees',
            entrees=entrees,
            produits=produits,
            query=query
        )
    finally:
        controller.close()
        product_controller.close()

@app.route('/entrees/add', methods=['POST'])
@require_role('admin', 'responsable', 'magasinier')
def add_entree():
    controller = EntryController()
    try:
        product_id = request.form.get('product_id')
        quantite = request.form.get('quantite', '').strip()
        fournisseur = request.form.get('fournisseur', '').strip()
        numero_bon = request.form.get('numero_bon', '').strip()
        commentaire = request.form.get('commentaire', '').strip()

        if not product_id:
            flash('Le produit est requis.', 'error')
            return redirect(url_for('entrees'))

        controller.ajouter_entree(product_id, quantite, fournisseur, numero_bon, commentaire)
        flash('Entrée enregistrée avec succès.', 'success')
        return redirect(url_for('entrees'))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('entrees'))
    finally:
        controller.close()

@app.route('/sorties')
@require_role('admin', 'responsable', 'magasinier')
def sorties():
    controller = SortieController()
    product_controller = ProductController()
    query = request.args.get('q', '').strip()

    try:
        produits = product_controller.get_all_products()
        sorties = controller.get_all_sorties()

        return render_template(
            'sorties.html',
            title='Sorties',
            active='sorties',
            sorties=sorties,
            produits=produits,
            query=query
        )
    finally:
        controller.close()
        product_controller.close()

@app.route('/sorties/add', methods=['POST'])
@require_role('admin', 'responsable', 'magasinier')
def add_sortie():
    controller = SortieController()
    try:
        product_id = request.form.get('product_id')
        quantite = request.form.get('quantite', '').strip()
        client = request.form.get('client', '').strip()
        numero_bon = request.form.get('numero_bon', '').strip()
        commentaire = request.form.get('commentaire', '').strip()

        if not product_id:
            flash('Le produit est requis.', 'error')
            return redirect(url_for('sorties'))

        controller.ajouter_sortie(product_id, quantite, client, numero_bon, commentaire)
        flash('Sortie enregistrée avec succès.', 'success')
        return redirect(url_for('sorties'))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('sorties'))
    finally:
        controller.close()

@app.route('/vehicules')
@require_role('admin', 'responsable')
def vehicules():
    controller = VehicleController()
    query = request.args.get('q', '').strip()
    edit_id = request.args.get('edit_id')
    selected_vehicle = None

    try:
        if query:
            vehicules = controller.rechercher(query)
        else:
            vehicules = controller.get_all()

        if edit_id:
            try:
                selected_id = int(edit_id)
                selected_vehicle = next((v for v in vehicules if v[0] == selected_id), None)
            except ValueError:
                selected_vehicle = None

        return render_template(
            'vehicules.html',
            title='Véhicules',
            active='vehicules',
            vehicules=vehicules,
            selected_vehicle=selected_vehicle,
            query=query
        )
    finally:
        controller.close()

@app.route('/vehicules/add', methods=['POST'])
@require_role('admin', 'responsable')
def add_vehicule():
    controller = VehicleController()
    try:
        matricule = request.form.get('matricule', '').strip()
        type_vehicule = request.form.get('type', '').strip()
        marque = request.form.get('marque', '').strip()
        modele = request.form.get('modele', '').strip()
        kilometrage = request.form.get('kilometrage', '0').strip()
        etat = request.form.get('etat', '').strip()
        observation = request.form.get('observation', '').strip()

        if not matricule:
            flash('La matricule du véhicule est requise.', 'error')
            return redirect(url_for('vehicules'))

        controller.ajouter(matricule, type_vehicule, marque, modele, int(kilometrage or 0), etat, observation)
        flash('Véhicule ajouté avec succès.', 'success')
        return redirect(url_for('vehicules'))
    except ValueError:
        flash('Le kilométrage doit être un nombre.', 'error')
        return redirect(url_for('vehicules'))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('vehicules'))
    finally:
        controller.close()

@app.route('/vehicules/edit/<int:id_vehicule>', methods=['POST'])
@require_role('admin', 'responsable')
def edit_vehicule(id_vehicule):
    controller = VehicleController()
    try:
        matricule = request.form.get('matricule', '').strip()
        type_vehicule = request.form.get('type', '').strip()
        marque = request.form.get('marque', '').strip()
        modele = request.form.get('modele', '').strip()
        kilometrage = request.form.get('kilometrage', '0').strip()
        etat = request.form.get('etat', '').strip()
        observation = request.form.get('observation', '').strip()

        if not matricule:
            flash('La matricule du véhicule est requise.', 'error')
            return redirect(url_for('vehicules', edit_id=id_vehicule))

        controller.modifier(id_vehicule, matricule, type_vehicule, marque, modele, int(kilometrage or 0), etat, observation)
        flash('Véhicule modifié avec succès.', 'success')
        return redirect(url_for('vehicules'))
    except ValueError:
        flash('Le kilométrage doit être un nombre.', 'error')
        return redirect(url_for('vehicules', edit_id=id_vehicule))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('vehicules', edit_id=id_vehicule))
    finally:
        controller.close()

@app.route('/vehicules/delete/<int:id_vehicule>', methods=['POST'])
@require_role('admin', 'responsable')
def delete_vehicule(id_vehicule):
    controller = VehicleController()
    try:
        controller.supprimer(id_vehicule)
        flash('Véhicule supprimé avec succès.', 'success')
        return redirect(url_for('vehicules'))
    finally:
        controller.close()

@app.route('/gasoil')
@require_role('admin', 'responsable')
def gasoil():
    controller = GasoilController()
    query = request.args.get('q', '').strip()
    edit_id = request.args.get('edit_id')
    selected_operation = None

    try:
        vehicules = controller.get_vehicules()
        if query:
            operations = controller.rechercher(query)
        else:
            operations = controller.get_all()

        if edit_id:
            try:
                selected_id = int(edit_id)
                selected_operation = next((op for op in operations if op[0] == selected_id), None)
            except ValueError:
                selected_operation = None

        return render_template(
            'gasoil.html',
            title='Gasoil',
            active='gasoil',
            operations=operations,
            vehicules=vehicules,
            selected_operation=selected_operation,
            query=query
        )
    finally:
        controller.close()

@app.route('/gasoil/add', methods=['POST'])
@require_role('admin', 'responsable')
def add_gasoil():
    controller = GasoilController()
    try:
        vehicule = request.form.get('vehicule', '').strip()
        date_operation = request.form.get('date_operation', '').strip()
        heure_operation = request.form.get('heure_operation', '').strip()
        kilometrage = request.form.get('kilometrage', '0').strip()
        quantite = request.form.get('quantite', '0').strip()
        observation = request.form.get('observation', '').strip()

        if not vehicule:
            flash('Le véhicule est requis.', 'error')
            return redirect(url_for('gasoil'))
        if not date_operation or not heure_operation:
            flash('La date et l’heure sont requises.', 'error')
            return redirect(url_for('gasoil'))

        controller.ajouter(vehicule, date_operation, heure_operation, float(kilometrage or 0), float(quantite or 0), observation)
        flash('Opération gasoil ajoutée avec succès.', 'success')
        return redirect(url_for('gasoil'))
    except ValueError:
        flash('Le kilométrage et la quantité doivent être des nombres.', 'error')
        return redirect(url_for('gasoil'))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('gasoil'))
    finally:
        controller.close()

@app.route('/gasoil/edit/<int:id_operation>', methods=['POST'])
@require_role('admin', 'responsable')
def edit_gasoil(id_operation):
    controller = GasoilController()
    try:
        vehicule = request.form.get('vehicule', '').strip()
        date_operation = request.form.get('date_operation', '').strip()
        heure_operation = request.form.get('heure_operation', '').strip()
        kilometrage = request.form.get('kilometrage', '0').strip()
        quantite = request.form.get('quantite', '0').strip()
        observation = request.form.get('observation', '').strip()

        if not vehicule:
            flash('Le véhicule est requis.', 'error')
            return redirect(url_for('gasoil', edit_id=id_operation))
        if not date_operation or not heure_operation:
            flash('La date et l’heure sont requises.', 'error')
            return redirect(url_for('gasoil', edit_id=id_operation))

        controller.modifier(id_operation, vehicule, date_operation, heure_operation, float(kilometrage or 0), float(quantite or 0), observation)
        flash('Opération gasoil modifiée avec succès.', 'success')
        return redirect(url_for('gasoil'))
    except ValueError:
        flash('Le kilométrage et la quantité doivent être des nombres.', 'error')
        return redirect(url_for('gasoil', edit_id=id_operation))
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('gasoil', edit_id=id_operation))
    finally:
        controller.close()

@app.route('/gasoil/delete/<int:id_operation>', methods=['POST'])
@require_role('admin', 'responsable')
def delete_gasoil(id_operation):
    controller = GasoilController()
    try:
        controller.supprimer(id_operation)
        flash('Opération gasoil supprimée avec succès.', 'success')
        return redirect(url_for('gasoil'))
    finally:
        controller.close()

@app.route('/historique')
@require_role('admin', 'responsable', 'magasinier')
def historique():
    controller = HistoryController()

    query = request.args.get('q', '').strip()
    type_filter = request.args.get('type', 'Tous').strip()
    module_filter = request.args.get('module', '').strip()

    try:
        # Priority: search > module filter > type filter > all
        if query:
            historique = controller.rechercher(query)
        elif module_filter:
            historique = controller.get_history_module(module_filter)
        elif type_filter and type_filter != 'Tous':
            historique = controller.get_history_filtre(type_filter)
        else:
            historique = controller.get_history()

        modules = controller.get_modules_list()

        return render_template(
            'historique.html',
            title='Historique',
            active='historique',
            historique=historique,
            query=query,
            modules=modules,
            selected_module=module_filter
        )
    finally:
        controller.close()

@app.route('/parametres', methods=['GET', 'POST'])
@require_role('admin')
def parametres():
    db = Database()
    current_user = None
    username = session.get('username')

    if username:
        current_user = db.get_user_by_username(username)

    low_stock_threshold = db.get_low_stock_threshold(default=10)

    if request.method == 'POST':
        threshold_value = request.form.get('low_stock_threshold', '').strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        try:
            if threshold_value == '':
                raise ValueError('Le seuil de stock faible est requis.')
            low_stock_threshold = int(threshold_value)
            if low_stock_threshold < 0:
                raise ValueError('Le seuil de stock faible ne peut pas être négatif.')
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template(
                'parametres.html',
                title='Paramètres',
                active='parametres',
                app_name=APP_NAME,
                app_version=APP_VERSION,
                low_stock_threshold=threshold_value,
                current_user=current_user
            )

        password_change_requested = any(value.strip() for value in (current_password, new_password, confirm_password))
        if password_change_requested:
            if not current_password or not new_password or not confirm_password:
                flash('Pour modifier le mot de passe, remplissez le mot de passe actuel, le nouveau mot de passe et la confirmation.', 'error')
                return render_template(
                    'parametres.html',
                    title='Paramètres',
                    active='parametres',
                    app_name=APP_NAME,
                    app_version=APP_VERSION,
                    low_stock_threshold=low_stock_threshold,
                    current_user=current_user
                )
            if new_password != confirm_password:
                flash('La confirmation du nouveau mot de passe ne correspond pas.', 'error')
                return render_template(
                    'parametres.html',
                    title='Paramètres',
                    active='parametres',
                    app_name=APP_NAME,
                    app_version=APP_VERSION,
                    low_stock_threshold=low_stock_threshold,
                    current_user=current_user
                )
            if not db.verify_and_migrate_password(username, current_password):
                flash('Le mot de passe actuel est incorrect.', 'error')
                return render_template(
                    'parametres.html',
                    title='Paramètres',
                    active='parametres',
                    app_name=APP_NAME,
                    app_version=APP_VERSION,
                    low_stock_threshold=low_stock_threshold,
                    current_user=current_user
                )

            uc = UserController()
            try:
                uc.set_user_password(current_user['id'], new_password)
            finally:
                uc.close()
            flash('Mot de passe mis à jour avec succès.', 'success')

        db.set_low_stock_threshold(low_stock_threshold)
        flash('Paramètres enregistrés avec succès.', 'success')
        return redirect(url_for('parametres'))

    return render_template(
        'parametres.html',
        title='Paramètres',
        active='parametres',
        app_name=APP_NAME,
        app_version=APP_VERSION,
        low_stock_threshold=low_stock_threshold,
        current_user=current_user
    )

@app.route('/a-propos')
def a_propos():
    return render_template(
        'a_propos.html',
        title='À propos',
        active='a_propos',
        app_name=APP_NAME,
        app_version=APP_VERSION
    )


@app.route('/auth-debug')
def auth_debug():
    return {
        "session_username": session.get("username"),
        "authenticated": bool(session.get("username"))
    }

@app.context_processor
def inject_current_role():
    """Expose `current_role` to all templates using session['username'].

    Returns {'current_role': role_or_None}
    """
    username = session.get('username')
    if not username:
        return {'current_role': None}

    uc = UserController()
    try:
        user = uc.get_user_by_username(username)
        if not user:
            return {'current_role': None}
        return {'current_role': user.get('role')}
    finally:
        uc.close()


# =====================================================
# User management routes (admin-only)
# =====================================================


@app.route('/gestion-utilisateurs')
@require_role('admin')
def gestion_utilisateurs():
    uc = UserController()
    try:
        users = uc.get_all_users()
        return render_template('users.html', title='Gestion des utilisateurs', active='parametres', users=users)
    finally:
        uc.close()


@app.route('/users/add', methods=['GET', 'POST'])
@require_role('admin')
def users_add():
    uc = UserController()
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            nom_complet = request.form.get('nom_complet', '').strip() or None
            role = request.form.get('role', '').strip()
            password = request.form.get('password', '')
            confirm = request.form.get('confirm', '')
            actif = 1 if request.form.get('actif') == 'on' else 0

            if not username:
                flash('Le nom d\'utilisateur est requis.', 'error')
                return render_template('_user_form.html', title='Ajouter utilisateur', user=None)
            if role not in UserController.VALID_ROLES:
                flash('Rôle invalide.', 'error')
                return render_template('_user_form.html', title='Ajouter utilisateur', user=None)
            if password != confirm:
                flash('Les mots de passe ne correspondent pas.', 'error')
                return render_template('_user_form.html', title='Ajouter utilisateur', user=None)

            try:
                uc._actor = session.get('username')
                uc.create_user(username, password, role=role, nom_complet=nom_complet, actif=actif)
                flash('Utilisateur créé.', 'success')
                return redirect(url_for('gestion_utilisateurs'))
            except Exception as e:
                flash('Erreur lors de la création de l\'utilisateur.', 'error')
                return render_template('_user_form.html', title='Ajouter utilisateur', user=None)

        return render_template('_user_form.html', title='Ajouter utilisateur', user=None)
    finally:
        uc.close()


@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@require_role('admin')
def users_edit(user_id):
    uc = UserController()
    try:
        user = uc.get_user_by_id(user_id)
        if not user:
            flash('Utilisateur introuvable.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        if request.method == 'POST':
            nom_complet = request.form.get('nom_complet', '').strip() or None
            role = request.form.get('role', '').strip()
            actif = 1 if request.form.get('actif') == 'on' else 0

            if role not in UserController.VALID_ROLES:
                flash('Rôle invalide.', 'error')
                return render_template('_user_form.html', title='Modifier utilisateur', user=user)

            uc._actor = session.get('username')
            uc.update_user(user_id, role=role, nom_complet=nom_complet, actif=actif)
            flash('Utilisateur mis à jour.', 'success')
            return redirect(url_for('gestion_utilisateurs'))

        return render_template('_user_form.html', title='Modifier utilisateur', user=user)
    finally:
        uc.close()


@app.route('/users/delete/<int:user_id>', methods=['POST'])
@require_role('admin')
def users_delete(user_id):
    uc = UserController()
    try:
        user = uc.get_user_by_id(user_id)
        if not user:
            flash('Utilisateur introuvable.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        current_username = session.get('username')
        if current_username and user.get('username') == current_username:
            flash('Vous ne pouvez pas supprimer votre propre compte.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        if user.get('role') == 'admin' or user.get('username') == 'admin' or user_id == 1:
            flash('Vous ne pouvez pas supprimer l’administrateur principal.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        uc._actor = session.get('username')
        uc.delete_user(user_id)
        flash('Utilisateur supprimé avec succès.', 'success')
        return redirect(url_for('gestion_utilisateurs'))
    finally:
        uc.close()


@app.route('/users/toggle-active/<int:user_id>', methods=['POST'])
@require_role('admin')
def users_toggle_active(user_id):
    uc = UserController()
    try:
        user = uc.get_user_by_id(user_id)
        if not user:
            flash('Utilisateur introuvable.', 'error')
            return redirect(url_for('gestion_utilisateurs'))
        new_actif = 0 if user.get('actif') else 1

        # Prevent an admin from deactivating their own account
        current_username = session.get('username')
        if current_username and user.get('username') == current_username and new_actif == 0:
            flash('Vous ne pouvez pas désactiver votre propre compte.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        # Prevent deactivating the last active admin
        if new_actif == 0 and user.get('role') == 'admin':
            users = uc.get_all_users()
            active_admins = [u for u in users if u.get('role') == 'admin' and u.get('actif')]
            # Exclude the target user
            active_admins = [a for a in active_admins if a.get('id') != user_id]
            if not active_admins:
                flash('Impossible de désactiver le dernier administrateur actif.', 'error')
                return redirect(url_for('gestion_utilisateurs'))

        uc._actor = session.get('username')
        uc.set_user_active(user_id, new_actif)
        flash('Statut utilisateur modifié.', 'success')
        return redirect(url_for('gestion_utilisateurs'))
    finally:
        uc.close()


@app.route('/users/change-password/<int:user_id>', methods=['GET', 'POST'])
@require_role('admin')
def users_change_password(user_id):
    uc = UserController()
    try:
        user = uc.get_user_by_id(user_id)
        if not user:
            flash('Utilisateur introuvable.', 'error')
            return redirect(url_for('gestion_utilisateurs'))

        if request.method == 'POST':
            password = request.form.get('password', '')
            confirm = request.form.get('confirm', '')
            if not password:
                flash('Le mot de passe est requis.', 'error')
                return render_template('_user_form.html', title='Changer mot de passe', user=user, change_password=True)
            if password != confirm:
                flash('Les mots de passe ne correspondent pas.', 'error')
                return render_template('_user_form.html', title='Changer mot de passe', user=user, change_password=True)

            uc._actor = session.get('username')
            uc.set_user_password(user_id, password)
            flash('Mot de passe mis à jour.', 'success')
            return redirect(url_for('gestion_utilisateurs'))

        return render_template('_user_form.html', title='Changer mot de passe', user=user, change_password=True)
    finally:
        uc.close()


if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5000)))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host=host, port=port, debug=debug)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', title='Accès refusé'), 403