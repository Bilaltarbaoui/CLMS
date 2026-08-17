import psutil, pathlib, os
path = str(pathlib.Path('database/clms.db').resolve()).lower()
print('DBPATH', path)
holders = []
for p in psutil.process_iter(['pid','name','exe','cmdline','cwd']):
    try:
        for f in p.open_files():
            if f.path.lower() == path:
                holders.append((p.pid, p.info.get('name'), p.info.get('cmdline'), p.info.get('cwd')))
                break
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        continue
if not holders:
    print('HOLDERS_NONE')
else:
    for pid,name,cmd,cwd in holders:
        print('HOLDER', pid, name, cmd, cwd)
