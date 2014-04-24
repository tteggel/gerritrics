import sys
from gevent import monkey; monkey.patch_all()
import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
import re
import requests

import argparse
import os
import urllib

import version
from team import team_roster
from change_list import change_lists

#################################################################################
# Command line config
#################################################################################

script_path = os.path.dirname(__file__)
parser = argparse.ArgumentParser(
    description="""OpenStack Activity server (v{0}).""".format(
        version.get_version()))
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

#################################################################################
# App setup
#################################################################################

app = Bottle()
changes = MongoClient(args.mongohost, args.mongoport).openstack_gerrit.changes
bottle.TEMPLATE_PATH.append('{0}/views'.format(script_path))

## Project lists ################################################################

def get_projects():
    host = 'https://git.openstack.org'
    result = {}
    sys.stdout.write('Loading openstack project list')
    project_list = requests.get(
        '{0}/cgit/openstack-infra/reviewstats/plain/projects'.format(host)).text
    for project_url in re.findall(""".*href='([^']*json)""", project_list):
        project = requests.get(''.join([host, project_url])).json()
        sys.stdout.write('.'); sys.stdout.flush()
        for repo in project['subprojects']:
            result[repo] = project['core-team']
    print('done.')
    return result

projects = get_projects()

#################################################################################
# Routes
#################################################################################

## Root routes ##################################################################

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

## Timeline routes ##############################################################

@app.route('/timeline/<user>')
@view('timeline')
def timeline_page_route(user):
    return {'nav': True, 'name': 'Timeline', 'user': user}

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

## Team routes ##################################################################

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

## Changelist routes #############################################################

@app.route('/changes/<listname>')
@view('change_list')
def change_list(listname):
    r = []
    team = team_roster[listname]
    for person in team:
        if 'closed' in request.query:
            c = changes.find({'owner.email': person['email']})
        else:
            c = changes.find({'owner.email': person['email'],
                              'status': {'$in': ['NEW', 'WORKINPROGRESS']}})
        for d in c: r.append(d)

    r = map(summarise_change, r)

    return {'nav': True, 'name': 'Changes', 'changes': r}

def summarise_change(change):
    def summarise_patchset(patchset):

        def value_is(n):
            return (lambda x: x['value'] == n)

        def is_core(project):
            return (lambda x: 'by' in x
                    and 'username' in x['by']
                    and project in projects
                    and x['by']['username'] in projects[project])

        def summarise_approvals(a):
            result = { k: len(filter(value_is(k), a))
                         for k in ['-2', '-1', '1', '2'] }
            first_review = sorted(a, key=lambda x: x['grantedOn'])[0]
            result['ttfr'] = first_review['grantedOn'] - change['createdOn']
            return result

        def not_jenkins(a):
            return a['by']['username'] != 'jenkins'

        def empty_summary():
            return { k: 0 for k in ['-2', '-1', '1', '2', 'ttfr'] }

        s = {}
        if 'approvals' in patchset:
            approvals = filter(not_jenkins, patchset['approvals'])
            if len(approvals) > 0:
                s['all'] = summarise_approvals(approvals)

            core_approvals = filter(is_core(change['project']), approvals)
            if len(core_approvals) > 0:
                s['cores'] = summarise_approvals(core_approvals)

        if 'all' not in s:
            s['all'] = empty_summary()

        if 'cores' not in s:
            s['cores'] = empty_summary()

        patchset['summary'] = s

        return patchset

    def summarise_summary(l, f):
        r = {}
        for p in l:
            for (t, v) in p['summary'].items():
                if t not in r: r[t] = {}
                for (n, c) in v.items():
                    if n not in r[t]: r[t][n] = []
                    r[t][n].append(c)

        for (t, v) in r.items():
            for (n, c) in v.items():
                r[t][n] = f[n](c)
        return r

    def avg(l):
        return float(sum(l)) / len(l) if len(l) > 0 else float('nan')

    change['currentPatchSet'] = summarise_patchset(change['currentPatchSet'])
    change['patchSets'] = map(summarise_patchset, change['patchSets'])
    change['summary'] = summarise_summary(change['patchSets'], {'-2': sum,
                                                                '-1': sum,
                                                                '1': sum,
                                                                '2': sum,
                                                                'ttfr': avg})
    return change


#################################################################################
# Main
#################################################################################

def main():
    """
    Run the server.
    """
    server = WSGIServer((args.address, args.port), app)
    server.serve_forever()

if __name__ == "__main__":
    main()
