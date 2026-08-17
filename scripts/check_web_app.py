import psutil
import sys
for p in psutil.process_iter(['pid','name','cmdline']):
    try:
        cl = p.info['cmdline'] or []
        s = ' '.join(cl)
        if 'web_app.py' in s or ('flask' in s and 'web_app' in s):
            print('RUNNING', p.pid, s)
    except Exception:
        continue
