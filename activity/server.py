import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer

import argparse
import os

import version

################################################################################
# Command line config
################################################################################
script_path = os.path.dirname(__file__)
parser = argparse.ArgumentParser(
    description="""OpenStack Activity server (v{0}).""".format(version.get_version()))
parser.add_argument('-a', '--address', default='0.0.0.0',
                    help='the ip address to bind to.',
                    type=str)
parser.add_argument('-p', '--port', default=8080,
                    help='the port number to bind to.',
                    type=int)
args = parser.parse_args()

################################################################################
# App setup
################################################################################
app = Bottle()
bottle.TEMPLATE_PATH.append('{0}/views'.format(script_path))


################################################################################
# Routes
################################################################################

## Satic routes ################################################################

static_root = '{0}/static'.format(script_path)

@app.route('/')
@view('index')
def index_route():
    return {'nav': True}

@app.route('/static/<filepath:path>')
def static_route(filepath):
    return static_file(filepath, root=static_root)

@app.route('<filepath:path>/')
def slash_route(filepath):
    """
    Redirect routes with trailing slash to one without.
    """
    return redirect(filepath)

@app.route('/favicon.ico')
def favicon():
    return static_route('favicon.ico')

################################################################################
# Main
################################################################################
def main():
    """
    Run the server.
    """
    server = WSGIServer((args.address, args.port), app)
    server.serve_forever()

if __name__ == "__main__":
    main()
