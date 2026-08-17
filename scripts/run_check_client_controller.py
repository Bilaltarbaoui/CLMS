import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print('ROOT', root)
sys.path.insert(0, root)
print('SYPATH0', sys.path[0])
print('CWD', os.getcwd())
print('FILES', os.listdir(root)[:10])
from controllers.client_controller import ClientController

c=ClientController()
clients=c.get_all_clients()
print('COUNT', len(clients))
c.close()
