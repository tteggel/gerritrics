%rebase page nav=nav, name=name

<table class="table table-striped">
 <thead>
  <tr>
   <th>Name</th>
   <th>all</th>
   <th>-2</th>
   <th>-1</th>
   <th>0</th>
   <th>+1</th>
   <th>+2</th>
  </tr>
 </thead>
 <tbody>
  % if defined('team') and team:
  % for person in team:
  <tr>
    <td>{{person['name']}}</td>
    <td>{{sum(person['reviews'])}}</td>
    <td>{{person['reviews'][0]}}</td>
    <td>{{person['reviews'][1]}}</td>
    <td>{{person['reviews'][2]}}</td>
    <td>{{person['reviews'][3]}}</td>
    <td>{{person['reviews'][4]}}</td>
  </tr>
  % end #for
  % end #if
 </tbody>
</table>
