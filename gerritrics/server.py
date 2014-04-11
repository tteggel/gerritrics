from gevent import monkey; monkey.patch_all()
import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient

import argparse
import os

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

@app.route('/timeline/<user:int>')
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

@app.route('/data/timeline/<user:int>')
def timeline_route(user):
    c = changes.find({"approvals": {"$elemMatch":
                                    {"approvals": {"$elemMatch":
                                                   {"$and":
                                                    [{"key.accountId.id":user}]
                                                }}}}})

    account =  [a for a in c[0]['accounts']['accounts']
                if not isinstance(a['id'], int)
                and a['id']['id'] == user][0]

    approvals = []
    for change in c:
        for approval1 in change['approvals']:
            for approval2 in approval1['approvals']:
                if approval2['key']['accountId']['id'] == user:
                    approvals.append(approval2)

    return {'nav': False, 'name': account['fullName'], 'approvals': approvals }


@app.route('/team/<team>')
@view('team')
def team_route(team):

    reviews =  review_count(map(lambda x: x['gerrit'], team_roster[team]))

    for person in team_roster[team]:
        account = person['gerrit']
        person['reviews'] = [0 if account not in reviews or
                                  x not in reviews[account] else
                             reviews[account][x]
                             for x in range(-2, 3)]
        person['name'] = account_name(person['gerrit'],
                                      person['name'])

    return {'nav': True, 'name': 'Team',
            'team': sorted(team_roster[team], key=lambda x: x['name'].lower())}

################################################################################
# Data functions
################################################################################

def review_count(team):

    raw = changes.aggregate([
        {"$match": {"accounts.accounts.id.id": {"$in": team}}},
        {"$unwind": "$approvals"},
        {"$unwind": "$approvals.approvals"},
        {"$match": {"approvals.approvals.key.accountId.id": {"$in": team}}},
        {"$group": {"_id": {"account": "$approvals.approvals.key.accountId.id",
                            "value": "$approvals.approvals.value"},
                    "count": {"$sum": 1}}}
    ])['result']

    result = {}
    for r in raw:
        value = r['_id']['value']
        account = r['_id']['account']
        count = r['count']
        if account not in result: result[account] = {}
        result[account][value] = r['count']

    return result



def account_name(account, name):
    c = changes.find(
        {"approvals":
         {"$elemMatch":
          {"approvals": {"$elemMatch":
                         {"$and":
                          [{"key.accountId.id":account}]}}}}})

    if c.count() == 0:
        return name

    return [a for a in c[0]['accounts']['accounts']
                if not isinstance(a['id'], int)
                and a['id']['id'] == account][0]['fullName']

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
