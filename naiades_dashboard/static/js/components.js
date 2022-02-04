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
                "title": window.MESSAGES.components.decrease,
                "labelText": "[[value]]%",
                "clustered": false,
                "fillColorsField": "color",
                "labelFunction": function(item) {
                  return Math.abs(item.values.value);
                },
                "balloonFunction": function(item) {
                  return `${item.category}: ${Math.abs(item.values.value)}%`;
                }
              }, {
                "fillAlphas": 0.8,
                "lineAlpha": 0.2,
                "type": "column",
                "valueField": "increase",
                "title": window.MESSAGES.components.increase,
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
                "text": window.MESSAGES.components.decrease,
                "x": "28%",
                "y": "97%",
                "bold": true,
                "align": "middle"
              }, {
                "text": window.MESSAGES.components.increase,
                "x": "75%",
                "y": "97%",
                "bold": true,
                "align": "middle"
              }],
    };

    const CHART_CONFIGS = {
        avg_hourly_consumption: {
            categoryField: "hour",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": window.MESSAGES.components.avgConsumptionPerHour,
                    "bullet": "round",
                    "valueField": "avg_consumption"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": window.MESSAGES.components.avgConsumptionPerHour
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": window.MESSAGES.components.consumptionLt
                }
            ]
        },
        you_vs_others: {
            categoryField: "entity",
            graphs: [
                {
                    "balloonText": "[[category]] [[title]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": window.MESSAGES.components.totalWeeklyConsumption,
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
                /*{
                    "id": "Title-1",
                    "size": 28,
                    "text": window.MESSAGES.components.mySchoolVsOthers
                }*/
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": window.MESSAGES.components.consumptionLtPerUser,
                    "minimum": 0,
                }
            ],
            rotate: true,
        },
        avg_day_consumption: {
            categoryField: "day",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]: [[value]] lt.",
                    "id": "AmGraph-1",
                    "title": window.MESSAGES.components.avgConsumptionPerDay,
                    "bullet": "round",
                    "valueField": "avg_consumption"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": window.MESSAGES.components.avgConsumptionPerDay
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": window.MESSAGES.components.consumptionLt
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
                    "title": window.MESSAGES.components.totalWeeklyConsumption,
                    "fillAlphas": 1,
                    "valueField": "total_consumption",
                    "type": "column"
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": window.MESSAGES.components.totalWeeklyConsumption
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": window.MESSAGES.components.consumptionLt
                }
            ],
            extra: {
                colors: ["#59ad59"],
                rotate: true
            }
        },
        weekly_change: weeklyChange,
        you_vs_others_weekly_change: JSON.parse(JSON.stringify(weeklyChange)),
        overall_change: JSON.parse(JSON.stringify(weeklyChange)),
        monthly_consumption: {
            type: "serial",
            marginRight: 70,
            valueAxes: [
                {
                    axisAlpha: 0,
                    position: "left",
                    minimum: 0,
                    title: window.MESSAGES.components.monthlyConsumption
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": window.MESSAGES.components.monthlyConsumption
                }
            ],
            legend: {
                enabled: false,
            },
            startDuration: 1,
            graphs: [
                {
                    balloonText: "<b>[[category]]: [[value]]</b>",
                    fillColorsField: "color",
                    fillAlphas: 0.9,
                    lineAlpha: 0.2,
                    type: "column",
                    valueField: "consumption"
                }
            ],
            chartCursor: {
                categoryBalloonEnabled: false,
                cursorAlpha: 0,
                zoomable: false
            },
            categoryField: "month",
            categoryAxis: {
                gridPosition: "start",
                labelRotation: 45
            },
            export: {
                enabled: true
            }
        }
    };

    AmCharts.checkEmptyData = function(chart) {
        if (chart.dataProvider.length !== 0) {
            return
        }

        // set min/max on the value axis
        chart.valueAxes[0].minimum = 0;
        chart.valueAxes[0].maximum = 100;

        // add dummy data point
        const dataPoint = {
            dummyValue: 0
        };
        dataPoint[chart.categoryField] = '';
        chart.dataProvider = [dataPoint];

        // add label
        chart.addLabel(0, '50%', window.MESSAGES.components.noData, 'center');

        // set opacity of the chart div
        chart.chartDiv.style.opacity = 0.5;

        // redraw it
        chart.validateNow();
    };

    const showChart = function(chartId, metric, data) {
        const config = CHART_CONFIGS[metric];

        // format day, hour
        $.each(data, function(idx, datum) {
            if (datum.hasOwnProperty("hour") && datum.hour >= 0 && datum.hour < 24) {
                datum.hour = `${datum.hour.toLocaleString('en', {minimumIntegerDigits: 2})}:00`;
            }

            if (datum.hasOwnProperty("day") && datum.day >= 0 && datum.day < 7) {
                datum.day = window.MESSAGES.days[datum.day]
            }
        });

        const charts = AmCharts.makeChart(chartId,
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
        AmCharts.checkEmptyData(charts);
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
                    .text(`${window.MESSAGES.components.error} ${metric}`)
            }
        });
        /*const $cont = $(container);
        const chartIdent = $cont.attr('id');
        if (chartIdent === "chart-overall_change"){
            for (var i = 0; i< chart.dataProvider.length; ++i) {
                if (chart.dataProvider[i].school === "school198") {
                    item.dataContext.selected = "#8198b4"
                }

            }
        }*/
    });
});
