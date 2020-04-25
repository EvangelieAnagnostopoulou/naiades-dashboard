$(function () {
    const weeklyChange = {
        "type": "serial",

          "rotate": true,
          "marginBottom": 50,
            "startDuration": 1,
            colors: ["#04D215", "#FF0F00"],
            // titles: [
            //     {
            //         "id": "Title-1",
            //         "size": 28,
            //         "text": "Consumption change since last week"
            //     }
            // ],
            "graphs": [{
                "fillAlphas": 0.8,
                "lineAlpha": 0.2,
                "type": "column",
                "valueField": "decrease",
                "title": "Decrease",
                "labelText": "- [[value]]%",
                "clustered": false,
                "fillColorsField": "color",
                "labelFunction": function(item) {
                  return Math.abs(item.values.value);
                },
                "balloonFunction": function(item) {
                  return item.category + ": " + Math.abs(item.values.value) + "%";
                }
              }, {
                "fillAlphas": 0.8,
                "lineAlpha": 0.2,
                "type": "column",
                "valueField": "increase",
                "title": "Increase",
                "labelText": "+ [[value]]%",
                "clustered": false,
                "fillColorsField": "color",
                "labelFunction": function(item) {
                  return Math.abs(item.values.value);
                },
                "balloonFunction": function(item) {
                  return item.category + ": " + Math.abs(item.values.value) + "%";
                }
              }],
              "categoryField": "school",
              "categoryAxis": {
                "gridPosition": "start",
                "gridAlpha": 0.2,
                "axisAlpha": 0,
              },
              "valueAxes": [{
                "gridAlpha": 0,
                "ignoreAxisWidth": true,
                "labelFunction": function(value) {
                  return Math.abs(value) + '%';
                },
                "guides": [{
                  "value": 0,
                  "lineAlpha": 0.2
                }]
              }],
              "balloon": {
                "fixedPosition": true
              },
              "chartCursor": {
                "valueBalloonsEnabled": false,
                "cursorAlpha": 0.05,
                "fullWidth": true
              },
              "allLabels": [{
                "text": "Decrease",
                "x": "28%",
                "y": "97%",
                "bold": true,
                "align": "middle"
              }, {
                "text": "Increase",
                "x": "75%",
                "y": "97%",
                "bold": true,
                "align": "middle"
              }],
    };

    const CHART_CONFIGS = {
        total_hourly_consumption: {
            categoryField: "hour",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": "Total consumption per hour",
                    "bullet": "round",
                    "valueField": "total_consumption"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": "Total consumption per hour"
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": "Consumption (lt)"
                }
            ]
        },
        you_vs_others: {
            categoryField: "entity",
            graphs: [
                {
                    "balloonText": "[[category]] [[title]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": "Total weekly consumption",
                    "valueField": "weekly_total",
                    // "cornerRadiusTop": 8,
                    "type": "column",
                    "fillColorsField": "color",
                    "fillAlphas": 1,
                    "lineAlpha": 0.1,
                }
            ],
             "legend": {
                    "enabled": false
             },
            titles: [
                {
                    "id": "Title-1",
                    "size": 28,
                    "text": "My School vs. Others"
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": "Consumption (lt)",
                    "minimum": 0,
                }
            ],
            rotate: true,
        },
        total_daily_consumption: {
            categoryField: "day",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": "Total consumption per day",
                    "bullet": "round",
                    "valueField": "total_consumption"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": "Total consumption per day"
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": "Consumption (lt)"
                }
            ],
            colors: ["#3498db"]
        },
        weekly_consumption_by_meter: {
            categoryField: "meter_number",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": "Total weekly consumption",
                    "fillAlphas": 1,
                    "valueField": "total_consumption",
                    "type": "column"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": "Total weekly consumption"
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": "Consumption (lt)"
                }
            ],
            extra: {
                colors: ["#59ad59"],
                rotate: true
            }
        },
        weekly_change: weeklyChange,
        you_vs_others_weekly_change: JSON.parse(JSON.stringify(weeklyChange)),
        monthly_consumption:{
            "type": "serial",
            "theme": "dark",
            "marginRight": 70,
            "valueAxes": [{
            "axisAlpha": 0,
            "position": "left",
            "title": "Monthly consumption"
          }],
            "legend": {"enabled": false},
          "startDuration": 1,
          "graphs": [{
            "balloonText": "<b>[[category]]: [[value]]</b>",
            "fillColorsField": "color",
            "fillAlphas": 0.9,
            "lineAlpha": 0.2,
            "type": "column",
            "valueField": "consumption"
          }],
          "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
          },
          "categoryField": "month",
          "categoryAxis": {
            "gridPosition": "start",
            "labelRotation": 45
          },
          "export": {
            "enabled": true
          }
        }
    };

    const showChart = function(chartId, metric, data) {
        const config = CHART_CONFIGS[metric];

        AmCharts.makeChart(chartId,
            {
                "fontFamily":  "'Open Sans', sans-serif",
                "theme": CHART_THEME,
                "type": "serial",
                "startDuration": 1,
                "categoryAxis": {
                    "gridPosition": "start"
                },
                "trendLines": [],
                "guides": [],
                "allLabels": [],
                "balloon": {},
                "legend": {
                    "enabled": true,
                    "useGraphSettings": true
                },
                "numberFormatter": {
                    "precision": 2,
                    "decimalSeparator": ".",
                    "thousandsSeparator": ","
                },
                "dataProvider": data,
                "export": {
                    "enabled": true,
                    "menu":[],
                     "beforeCapture": function() {
                      var chart = this.setup.chart;
                      chart.theme = "none";
                      chart.validateNow();
                    },
                    "afterCapture": function() {
                      var chart = this.setup.chart;
                      setTimeout(function() {
                        chart.theme = "dark";
                        chart.validateNow();
                      }, 10);
                    }
                },
                ...(config || {})
            }
        );
    };

    $.each($('.data-item'), function(idx, container) {
        const $container = $(container);
        const chartId = $container.attr('id');
        const metric = chartId.split('-')[1];
        const isChart = $container.hasClass('data-chart');

        // set as loading
        $container
            .empty()
            .addClass('loading')
            .append($('<i>').addClass('fa fa-spinner fa-spin'));

        // request data from backend
        $.ajax({
            url: `/api/measurements/data?metric=${metric}`,
            success: function({data}) {
                if (isChart) {
                    showChart(chartId, metric, data);
                } else {
                    // remove loading
                    $container
                        .empty()
                        .removeClass('loading');

                    window.COMPONENT_CALLBACKS[metric]($container, metric, data);
                }
            },
            error: function(error) {
                $container
                    .empty()
                    .removeClass('loading')
                    .addClass('error')
                    .text(`An error occurred when loading data for ${metric}`)
            }
        });
    });

    // request map data
    // $.ajax({
    //     url: `/api/measurements/data?metric=all&idx=0`,
    //     success: function({data}) {
    //         updateMap(data);
    //     },
    //     error: function(error) {
    //         console.error(`An error occurred when loading data for map data.`)
    //     }
    // });
});