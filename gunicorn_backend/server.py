import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn --workers 3 --timeout 1000 --bind 0.0.0.0:5151 app:app".split()
    sys.exit(run())