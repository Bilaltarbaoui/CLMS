import psutil
stopped=[]
for p in psutil.process_iter(['pid','name','cmdline']):
    try:
        cl = p.info['cmdline'] or []
        s = ' '.join(cl).lower()
        if 'web_app.py' in s and 'clms' in s:
            try:
                p.terminate()
            except Exception:
                pass
            stopped.append(p.pid)
    except Exception:
        continue
# escalate
import time
for pid in list(stopped):
    try:
        p = psutil.Process(pid)
        p.wait(3)
    except Exception:
        try:
            psutil.Process(pid).kill()
        except Exception:
            pass
print('FORCE_STOPPED', stopped)
