<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

%if defined('name') and name:
    <title>OpenStack Metrics &mdash; {{!name}}</title>
%else:
    <title>OpenStack Metrics</title>
%end
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/static/css/activity.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="/static/bootstrap/js/html5shiv.js"></script>
    <![endif]-->

    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

  </head>

  <body>

    <div class="container-fluid">
%if defined('nav') and nav:
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <li><a href="/">Home</a></li>
        </ul>
        <h3 class="muted">OpenStack Gerrit Metrics</h3>
      </div>
      <hr>
%end

%include

%if defined('nav') and nav:
      <hr>

      <div class="footer row">
        <p>
          &copy; <a href="http://hp.com">Hewlett-Packard Development Company L.P.</a> 2014
          &mdash; <a href="https://github.com/thom-leggett/gerritrics">Source</a>
          &mdash; <a href="https://hpcloud.com">Hosted on the HP Cloud</a>
        </p>
      </div>
%end

    </div> <!-- /container -->

    <script src="/static/bootstrap/js/bootstrap.min.js"></script>

  </body>
</html>
