{% load babel %}{% load bolibana %}PERCENT = {% if graph.options.only_percent %}'%'{% else %}''{% endif %};
{{ id}} = new Highcharts.Chart(
        {chart: {renderTo: '{{ id }}', defaultSeriesType: '{{ graph.graph_type }}', backgroundColor: '#ebebeb', },
        legend: {}, title: {text: null},
        xAxis: {categories: [{% for p in graph.periods %}'{{ p.middle|datefmt:"MMMM YYYY" }}',{% endfor %}]},
        yAxis: {title: {text: null},{% if graph.options.only_percent %} max:105{% endif %}},
        series: [{%for key, line in graph.data %}{name: '{{ line.label }}', data: [{% for pid, lvalue in line.values.items|sorted %}{% if graph.options.only_percent %}{{ lvalue.percent|default:"0"|percentraw }}{% else %}{{ lvalue.value|default_if_none:"-0" }}{% endif %},{% endfor %}]},{% endfor %}],
        tooltip: {formatter: function() { return ''+ this.series.name +': '+ this.y +PERCENT;} },
        plotOptions: {line: {animation: false, dataLabels: {enabled: true}, enableMouseTracking: false },
                      column: {animation: false, enableMouseTracking: false, dataLabels: {enabled: true, formatter: function() {if (this.y == '-0') { return "n/a" } else { return '' + this.y.toString().replace('.', ',') + PERCENT;} }} }},
        exporting: {enabled: true}, credits: {enabled: true, text: "© PNLP – {{ eperiod.middle|datefmt:"MMMM yyyy" }}", href: null},
      });
