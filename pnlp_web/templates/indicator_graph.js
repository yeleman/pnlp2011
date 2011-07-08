{% load babel %}
{% load pnlp %}
{{ id}} = new Highcharts.Chart(
        {chart: {renderTo: '{{ id }}', defaultSeriesType: 'column', backgroundColor: 'transparent', },
        legend: {},
        title: {text: null},
        xAxis: {categories: [{% for p in graph.periods %}'{{ p.middle|datefmt:"MMMM YYYY" }}',{% endfor %}]},
        yAxis: {title: {text: null}, max:100},
        series: [{%for key, line in graph.data %}{name: '{{ line.label }}', data: [{% for pid, lvalue in line.values.items %}{{ lvalue.percent|default:"0"|percentraw }},{% endfor %}]},{% endfor %}],
        tooltip: {formatter: function() { return ''+ this.series.name +': '+ this.y +'%';} },
        plotOptions: {line: {animation: false, dataLabels: {enabled: true}, enableMouseTracking: false },
                      column: {animation: false, enableMouseTracking: false, dataLabels: {enabled: true, formatter: function() {return '' + this.y.toString().replace('.', ',') + '%';}} }},
        exporting: {enabled: true},
        credits: {enabled: true, text: "© PNLP – {{ eperiod.middle|datefmt:"MMMM yyyy" }}", href: null},
      });
