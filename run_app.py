import os
from statistics.main import app

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('IP', '0.0.0.0')
    app.run(host=host, port=port)