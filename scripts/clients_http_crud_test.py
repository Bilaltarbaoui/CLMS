import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

import psutil

BASE = 'http://127.0.0.1:5000'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def start_server():
    cmd = [
        os.path.join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe'),
        os.path.join(PROJECT_ROOT, 'scripts', 'start_web_single.py')
    ]
    proc = subprocess.Popen(cmd, cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc


def stop_server(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def wait_for_server(timeout=15):
    end = time.time() + timeout
    while time.time() < end:
        for c in psutil.net_connections(kind='inet'):
            if c.laddr.port == 5000 and c.status == 'LISTEN':
                return True
        time.sleep(0.2)
    return False


def request(opener, path, data=None):
    url = BASE + path
    body = urllib.parse.urlencode(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    with opener.open(req, timeout=20) as r:
        return r.getcode(), r.geturl(), r.read().decode('utf-8', errors='replace')


def row_has_name(html, name):
    return bool(re.search(r'<tr>.*?<td>\d+</td>.*?<td>' + re.escape(name) + r'</td>.*?</tr>', html, re.S))


def cleanup_db_holders():
    db_path = str(Path(PROJECT_ROOT, 'database', 'clms.db').resolve()).lower()
    holders = []
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for f in p.open_files():
                if str(f.path).lower() == db_path:
                    holders.append((p.pid, p.name(), p.cmdline()))
                    break
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return holders


def main():
    existing_server = None
    for c in psutil.net_connections(kind='inet'):
        if c.laddr.port == 5000 and c.status == 'LISTEN':
            try:
                p = psutil.Process(c.pid)
                cmdline = ' '.join(p.cmdline() or [])
                if 'start_web_single.py' in cmdline or 'flask' in cmdline.lower():
                    existing_server = p
                    break
            except Exception:
                pass

    if existing_server:
        print('Stopping existing server process', existing_server.pid)
        existing_server.kill()
        existing_server.wait(timeout=5)

    proc = start_server()
    try:
        if not wait_for_server(15):
            out, err = proc.communicate(timeout=5)
            print('Server failed to start')
            print(out)
            print(err)
            sys.exit(1)

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(),
            urllib.request.HTTPRedirectHandler()
        )

        print('STEP1 GET /clients')
        status, url, body = request(opener, '/clients')
        print('  status', status)
        assert status == 200
        assert 'Clients' in body

        unique = f'httpcrud_{int(time.time())}'
        temp_name = f'TEST_CLIENT_{unique}'
        temp_tel = '000111222'
        temp_addr = 'Temp Address'
        temp_email = f'{unique}@example.com'
        temp_city = 'TestVille'

        print('STEP2 ADD client', temp_name)
        status, url, body = request(opener, '/clients/add', data={
            'nom': temp_name,
            'telephone': temp_tel,
            'adresse': temp_addr,
            'email': temp_email,
            'ville': temp_city
        })
        print('  status', status, 'url', url)
        assert status == 200
        assert url.endswith('/clients')
        assert row_has_name(body, temp_name)

        print('STEP3 SEARCH new client')
        status, url, body = request(opener, f'/clients?q={urllib.parse.quote(temp_name)}')
        print('  status', status)
        assert status == 200
        assert row_has_name(body, temp_name)
        ids = re.findall(r'<td>(\d+)</td>\s*<td>' + re.escape(temp_name), body)
        assert ids
        client_id = ids[0]
        print('  found client_id', client_id)

        new_name = temp_name + '_EDITED'
        print('STEP4 EDIT client', client_id)
        status, url, body = request(opener, f'/clients/edit/{client_id}', data={
            'nom': new_name,
            'telephone': temp_tel,
            'adresse': temp_addr,
            'email': temp_email,
            'ville': temp_city
        })
        print('  status', status, 'url', url)
        assert status == 200
        assert url.endswith('/clients')
        assert row_has_name(body, new_name)

        status, url, body = request(opener, f'/clients?q={urllib.parse.quote(new_name)}')
        print('  verify edit', status)
        assert status == 200
        assert row_has_name(body, new_name)

        print('STEP5 DELETE client', client_id)
        status, url, body = request(opener, f'/clients/delete/{client_id}', data={})
        print('  status', status, 'url', url)
        assert status == 200
        assert url.endswith('/clients')
        assert not row_has_name(body, new_name)

        status, url, body = request(opener, f'/clients?q={urllib.parse.quote(new_name)}')
        print('  verify deletion', status)
        assert status == 200
        assert not row_has_name(body, new_name)

        print('STEP6 REFRESH /clients')
        status, url, body = request(opener, '/clients')
        print('  status', status)
        assert status == 200
        assert not row_has_name(body, new_name)

        print('STEP7 DB cleanup check')
        conn = sqlite3.connect(Path(PROJECT_ROOT, 'database', 'clms.db'), timeout=10, check_same_thread=False)
        try:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM clients WHERE nom IN (?, ?)', (temp_name, new_name))
            count = cur.fetchone()[0]
            print('  count', count)
            assert count == 0
        finally:
            conn.close()

        print('STEP8 STOP SERVER')
        stop_server(proc)
        proc = None

        holders = cleanup_db_holders()
        print('  db holders after stop', holders)
        assert not holders

        print('FULL CLIENTS CRUD TEST PASSED')
    except Exception:
        raise
    finally:
        if proc is not None:
            stop_server(proc)


if __name__ == '__main__':
    main()
