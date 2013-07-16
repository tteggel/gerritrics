%rebase page nav=nav, name=name

<div class="jumbotron">

%if defined('name') and name:
<h1>{{!name}}</h1>
%end


</div>

<div id="chart"></div>

<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script type="text/javascript">
var Timeline = Timeline || {}
Timeline.config = {'user': {{!user}}};
</script>
<script src="/static/js/timeline.js"></script>
