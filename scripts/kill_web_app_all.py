import psutil, os
proj = os.path.abspath('.')
stopped = []
for p in psutil.process_iter(['pid','name','cmdline','cwd']):
    try:
        cl = ' '.join(p.info.get('cmdline') or [])
        cwd = p.info.get('cwd') or ''
        if 'web_app.py' in cl and (proj.lower() in cl.lower() or proj.lower() in (cwd or '').lower()):
            try:
                p.kill()
            except Exception:
                try:
                    p.terminate()
                except Exception:
                    pass
            stopped.append(p.pid)
    except Exception:
        pass
print('KILLED', stopped)
