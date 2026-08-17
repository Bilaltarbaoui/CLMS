import os
import psutil
import pathlib

proj = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print('PROJECT_ROOT', proj)
path = str(pathlib.Path(os.path.join(proj, 'database', 'clms.db')).resolve()).lower()
print('DBPATH', path)
print('--- WEB_APP PROCESSES ---')
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
    try:
        cl = ' '.join(p.info.get('cmdline') or [])
        cwd = p.info.get('cwd') or ''
        if 'web_app.py' in cl and proj.lower() in cl.lower():
            print('WEB', p.pid, p.info.get('name'), cwd, cl)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
print('--- DB HOLDERS ---')
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
    try:
        for f in p.open_files():
            if f.path.lower() == path:
                cl = ' '.join(p.info.get('cmdline') or [])
                print('DB', p.pid, p.info.get('name'), p.info.get('cwd') or '', cl)
                break
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
