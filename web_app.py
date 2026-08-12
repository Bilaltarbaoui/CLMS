from flask import Flask, render_template
from controllers.dashboard_controller import DashboardController
from controllers.vehicle_controller import VehicleController
from controllers.gasoil_controller import GasoilController

app = Flask(__name__)

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
def clients():
    return render_template('base.html', title='Clients', active='clients')

@app.route('/produits')
def produits():
    return render_template('base.html', title='Produits', active='produits')

@app.route('/entrees')
def entrees():
    return render_template('base.html', title='Entrées', active='entrees')

@app.route('/sorties')
def sorties():
    return render_template('base.html', title='Sorties', active='sorties')

@app.route('/vehicules')
def vehicules():
    return render_template('base.html', title='Véhicules', active='vehicules')

@app.route('/gasoil')
def gasoil():
    return render_template('base.html', title='Gasoil', active='gasoil')

@app.route('/historique')
def historique():
    return render_template('base.html', title='Historique', active='historique')

@app.route('/parametres')
def parametres():
    return render_template('base.html', title='Paramètres', active='parametres')

@app.route('/a-propos')
def a_propos():
    return render_template('base.html', title='À propos', active='a_propos')

if __name__ == '__main__':
    app.run(debug=True)