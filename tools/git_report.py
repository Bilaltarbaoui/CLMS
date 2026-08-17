import subprocess
import sys

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, cwd='.', stderr=subprocess.STDOUT, text=True)
        return out
    except subprocess.CalledProcessError as e:
        return e.output

print('=== git status ===')
print(run('git status --porcelain'))

print('=== git diff --stat ===')
print(run('git diff --stat'))

print('=== git diff --check ===')
print(run('git diff --check'))

print('=== git log --oneline -5 ===')
print(run('git log --oneline -5'))
