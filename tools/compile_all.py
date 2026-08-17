import py_compile
import glob
import sys

files = glob.glob('**/*.py', recursive=True)
errors = 0
for f in files:
    try:
        py_compile.compile(f, doraise=True)
    except Exception as e:
        print('COMPILE_ERROR', f, e)
        errors += 1

if errors:
    print('COMPILE_FAIL', errors)
    sys.exit(2)

print('COMPILE_OK', len(files), 'files')
