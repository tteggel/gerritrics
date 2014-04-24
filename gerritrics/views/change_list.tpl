%rebase page nav=nav, name=name
<script type="text/javascript" language="javascript" src="//cdn.datatables.net/1.10-dev/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" language="javascript" src="/static/js/moment.min.js"></script>
<script type="text/javascript" language="javascript" src="/static/js/dataTables.bootstrap.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/dataTables.bootstrap.css">
<script type="text/javascript" charset="utf-8">
    $(document).ready(function() {
        table = $('#changes').dataTable({
            "iDisplayLength": 100,
            "aoColumnDefs": [{
                "aTargets": [6, 7],
                "mRender": function(data, type, full) {
                               if (type === 'display') {
                                 return moment(data * 1000).fromNow()
                               } else {
                                 return data;
                               }
                           }
            },{
                "aTargets": [12, 17, 22, 27],
                "mRender": function(data, type, full) {
                               if (type === 'sort' && data == 0) {
                                   return 9007199254740992;
                               }
                               if (type === 'display' && data > 0) {
                                 return moment.duration(data * 1000).humanize()
                               } else if (type === 'display' && data == 0) {
                                 return 'still waiting';
                               } else if (type === 'display') {
                                 return "-" + moment.duration(Math.abs(data) * 1000).humanize();
                               } else {
                                 return data;
                               }
                           }
                       }]
                   }
        );
        $(window).resize(function () {
            table.fnAdjustColumnSizing();
        });
    });
</script>
<table id="changes" class="table table-hover table-condensed table-bordered">
 <thead>
  <tr>
   <th rowspan="3">Change-Id</th>
   <th rowspan="3">Project</th>
   <th rowspan="3">Subject</th>
   <th rowspan="3">Status</th>
   <th rowspan="3">Owner</th>
   <th rowspan="3">#</th>
   <th rowspan="3" title="Created">C</th>
   <th rowspan="3" title="Updated">U</th>
   <th colspan="10">Current Patch</th>
   <th colspan="10">All Patches</th>
  </tr>
  <tr class="text-center">
    <th colspan="5">All reviews</th>
    <th colspan="5">Core reviews</th>
    <th colspan="5">All reviews</th>
    <th colspan="5">Core reviews</th>
  </tr>
  <tr class="text-right">
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th title="Time To First Review">TTFR</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th title="Time To First Review">TTFR</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th title="Time To First Review">TTFR</th>
    <th>-2</th>
    <th>-1</th>
    <th>+1</th>
    <th>+2</th>
    <th title="Time To First Review">TTFR</th>
  </tr>
 </thead>
 <tbody>
  % if defined('changes') and changes:
  % for change in changes:
  <tr>
    <td><a href="https://review.openstack.org/#/q/{{change['id']}},n,z">{{change['id'][:9]}}</a></td>
    <td>{{change['project']}}</td>
    <td>{{change['subject']}}</td>
    <td>{{change['status'].replace('WORKINPROGRESS', 'WIP')}}</td>
    <td>{{change['owner']['name']}}</td>
    <td>{{len(change['patchSets'])}}</td>
    <td>{{change['createdOn']}}</td>
    <td>{{change['lastUpdated']}}</td>
    % for s in [change['currentPatchSet']['summary'], change['summary']]:
    %     for t in [s['all'], s['cores']]:
    %         for u in ['-2', '-1', '1', '2']:
    %         v=t[u]
    <td class="text-right {{'danger' if int(u) < 0 and v > 0 else 'success' if int(u) > 0 and v > 0 else ''}}">{{v}}</td>
    %         end #for
    <td>{{t['ttfr']}}</td>
    %     end #for
    % end #for
  </tr>
  % end #for
  % end #if
 </tbody>
</table>
