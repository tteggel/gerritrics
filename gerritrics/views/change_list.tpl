%rebase page nav=nav, name=name
<table class="table table-hover table-condensed table-bordered">
 <thead>
  <tr>
   <th rowspan="3">Change-Id</th>
   <th rowspan="3">Project</th>
   <th rowspan="3">Subject</th>
   <th rowspan="3">Status</th>
   <th rowspan="3">Owner</th>
   <th rowspan="3">#</th>
   <th rowspan="3">O</th>
   <th rowspan="3">U</th>
   <th colspan="8">Current Patch</th>
   <th colspan="8">All Patches</th>
  </tr>
  <tr class="text-center">
    <th colspan="4">All reviews</th>
    <th colspan="4">Core reviews</th>
    <th colspan="4">All reviews</th>
    <th colspan="4">Core reviews</th>
  </tr>
  <tr class="text-right">
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
  </tr>
 </thead>
 <tbody>
  % import datetime
  % from ago import human
  % def agoe(e):
  %    d = datetime.datetime.fromtimestamp(e)
  %    return human(d, precision=1, past_tense="{}")
  % end #dev
  % if defined('changes') and changes:
  % for change in changes:
  <tr>
    <td><a href="https://review.openstack.org/#/q/{{change['id']}},n,z}}">{{change['id'][:9]}}</a></td>
    <td>{{change['project']}}</td>
    <td>{{change['subject']}}</td>
    <td>{{change['status'].replace('WORKINPROGRESS', 'WIP')}}</td>
    <td>{{change['owner']['name']}}</td>
    <td>{{len(change['patchSets'])}}</td>
    <td>{{agoe(change['createdOn'])}}</td>
    <td>{{agoe(change['lastUpdated'])}}</td>
    % for s in [change['currentPatchSet']['summary'], change['summary']]:
    %     for t in [s['all'], s['cores']]:
    %         for u in ['-2', '-1', '1', '2']:
    %         v=t[u]
    <td class="text-right {{'danger' if int(u) < 0 and v > 0 else 'success' if int(u) > 0 and v > 0 else ''}}">{{v}}</td>
    %         end #for
    %     end #for
    % end #for
  </tr>
  % end #for
  % end #if
 </tbody>
</table>
