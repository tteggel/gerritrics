var Timeline = Timeline || {};

Timeline.got_data = function(err, data) {
  if(!err && data) Timeline.render(data);
};

d3.json('/data/timeline/' + Timeline.config.user, Timeline.got_data);

var margin = { top: 30, right: 20, bottom: 0, left: 30},
    width = 700 - margin.left - margin.right,
    height = 430 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 24),
    colours = ["#ff0000", "#880000", "#cccc00","#008800","#00ff00"],
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
    times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];


Timeline.render = function (data) {
          $(".jumbotron").html("<h1>" + data.name + "</h1>");

          data = data.approvals.map(
            function (i) {i.grantedOn = new Date(i.grantedOn * 1000); return i});

          var svg = d3.select("#chart").append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          var dayLabels = svg.selectAll(".dayLabel")
              .data(days)
              .enter().append("text")
                .text(function (d) { return d; })
                .attr("x", 0)
                .attr("y", function (d, i) { return i * gridSize; })
                .style("text-anchor", "end")
                .attr("transform", "translate(-6," + gridSize / 1.5 + ")");

          var timeLabels = svg.selectAll(".timeLabel")
              .data(times)
              .enter().append("text")
                .text(function(d) { return d; })
                .attr("x", function(d, i) { return i * gridSize; })
                .attr("y", 0)
                .style("text-anchor", "middle")
                .attr("transform", "translate(" + gridSize / 2 + ", -6)");

          var heatMap = svg.selectAll(".hour")
              .data(data)
              .enter()
              .append("circle")
              .attr("cx", function(d) { return gridSize *
                                        (d.grantedOn.getHours() + (d.grantedOn.getMinutes() / 60)); })
              .attr("cy", function(d) { return (d.grantedOn.getDay()) * gridSize; })
              .attr("transform", "translate(" + gridSize / 2 + ", " + gridSize / 2  + ")")
              .attr("class", "hour bordered")
              .attr("r", (gridSize/2)-6)
              .style("fill", colours[0]);

          heatMap.transition().duration(1000)
              .style("fill", function(d) { return colours[parseInt(d.value) + 2]; });

      };
