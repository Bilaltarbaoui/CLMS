import psutil, time
proj = r'C:\Users\HP\Documents\CLMS\06_Prototype'
stopped = []
for p in psutil.process_iter(['pid','name','cmdline']):
    try:
        cl = p.info['cmdline'] or []
        s = ' '.join(cl)
        if 'web_app.py' in s and proj in s:
            pid = p.pid
            try:
                p.terminate()
            except Exception:
                pass
            stopped.append(pid)
    except Exception:
        continue
# wait
for pid in stopped:
    try:
        p = psutil.Process(pid)
        p.wait(5)
    except Exception:
        try:
            psutil.Process(pid).kill()
        except Exception:
            pass
print('STOPPED', stopped)
