import psutil, os
proj = os.path.abspath('.')
stopped=[]
for p in psutil.process_iter(['pid','name','cmdline']):
    try:
        cl = ' '.join(p.info.get('cmdline') or [])
        if 'web_app.py' in cl and proj.lower() in cl.lower():
            try:
                p.terminate()
            except Exception:
                pass
            stopped.append(p.pid)
    except Exception:
        pass
print('STOPPED', stopped)
