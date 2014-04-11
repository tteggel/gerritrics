from gevent import monkey; monkey.patch_all()
import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient

import argparse
import os
import urllib

import version
from team import team_roster

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
parser.add_argument('-m', '--mongohost', default='127.0.0.1',
                    help='the hostname of the mongodb server.',
                    type=str)
parser.add_argument('-n', '--mongoport', default=27017,
                    help='the port number of the mongodb server.',
                    type=int)
args = parser.parse_args()

################################################################################
# App setup
################################################################################

app = Bottle()
changes = MongoClient(args.mongohost, args.mongoport).openstack_gerrit.changes
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

@app.route('/timeline/<user>')
@view('timeline')
def timeline_page_route(user):
    return {'nav': True, 'name': 'Timeline', 'user': user}

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

## Dynamic routes ##############################################################

@app.route('/data/timeline/<user>')
def timeline_route(user):
    user = urllib.unquote(user)
    c = changes.find({"patchSets.approvals.by.email": user})
    approvals = []
    for change in c:
        for patchset in change['patchSets']:
	    if 'approvals' not in patchset: continue
            for approval in patchset['approvals']:
                if 'email' in approval['by'] and approval['by']['email'] == user:
                    approvals.append(approval)

    return {'nav': False, 'name': user, 'approvals': approvals }

@app.route('/team/<team>')
@view('team')
def team_route(team):

    reviews =  review_count(map(lambda x: x['email'], team_roster[team]))

    for person in team_roster[team]:
        account = person['email']
        person['reviews'] = [0 if account not in reviews or
                                  x not in reviews[account] else
                             reviews[account][x]
                             for x in range(-2, 3)]

    return {'nav': True, 'name': 'Team',
            'team': sorted(team_roster[team], key=lambda x: x['name'].lower())}

################################################################################
# Data functions
################################################################################

def review_count(team):

    raw = changes.aggregate([
        {"$match": {"patchSets.approvals.by.email": {"$in": team}}},
        {"$unwind": "$patchSets"},
        {"$unwind": "$patchSets.approvals"},
        {"$match": {"patchSets.approvals.by.email": {"$in": team}}},
        {"$group": {"_id": {"account": "$patchSets.approvals.by.email",
                            "value": "$patchSets.approvals.value"},
                    "count": {"$sum": 1}}}
    ])['result']

    result = {}
    for r in raw:
        value = int(r['_id']['value'])
        account = r['_id']['account']
        count = r['count']
        if account not in result: result[account] = {}
        result[account][value] = r['count']

    return result

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
