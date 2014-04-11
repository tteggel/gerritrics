%rebase page nav=nav, name=name
%import urllib
<script type="text/javascript" language="javascript" src="//cdn.datatables.net/1.10-dev/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" language="javascript" src="/static/js/dataTables.bootstrap.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/dataTables.bootstrap.css">
<script type="text/javascript" charset="utf-8">
        $(document).ready(function() {
                $('#team').dataTable();
        } );
</script>
<table id="team" class="table table-hover table-condensed table-bordered">
 <thead>
  <tr>
   <th>Name</th>
   <th>all</th>
   <th>-2</th>
   <th>-1</th>
   <th>+1</th>
   <th>+2</th>
   <th>niceness ratio</th>
  </tr>
 </thead>
 <tbody>
  % if defined('team') and team:
  % for person in team:
  % email_escaped=urllib.quote(person['email'])
  <tr>
    <td><a href="/timeline/{{email_escaped}}">{{person['name']}}</a></td>
    <td>{{sum(person['reviews'])}}</td>
    <td>{{person['reviews'][0]}}</td>
    <td>{{person['reviews'][1]}}</td>
    <td>{{person['reviews'][3]}}</td>
    <td>{{person['reviews'][4]}}</td>
    <td>{{0 if sum(person['reviews']) == 0 else '{0:.2f}'.format(float((person['reviews'][3]+person['reviews'][4]) - (person['reviews'][0] + person['reviews'][1]))/sum(person['reviews']))}}</td>
  </tr>
  % end #for
  % end #if
 </tbody>
</table>
