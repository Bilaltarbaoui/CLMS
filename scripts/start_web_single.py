import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
os.chdir(project_root)

from web_app import app

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
