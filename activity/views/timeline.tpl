%rebase page nav=nav, name=name

<div class="jumbotron">

%if defined('name') and name:
<h1>{{!name}}</h1>
%end

%if defined('desc') and desc:
<p>{{!desc}}</p>
%end

</div>
