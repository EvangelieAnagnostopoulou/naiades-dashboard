$(function () {
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
                    "type": "column",
                }
            ],
            titles: [
                {
                    "id": "Title-1",
                    "size": 28,
                    "text": "You vs. Others"
                }
            ],
            valueAxes: [
                {
                    "id": "ValueAxis-1",
                    "title": "Consumption (lt)",
                    "minimum": 0,
                }
            ],
            extra: {
                rotate: true,
            }
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
            extra: {
                colors: ["#3498db"]
            }
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
        }
    };

    const showChart = function(chartId, metric, data) {
        const config = CHART_CONFIGS[metric];

        AmCharts.makeChart(chartId,
            {
                "type": "serial",
                "theme": "chalk",
                "categoryField": config.categoryField,
                "startDuration": 1,
                "categoryAxis": {
                    "gridPosition": "start"
                },
                "trendLines": [],
                "graphs": config.graphs,
                "guides": [],
                "valueAxes": config.valueAxes,
                "allLabels": [],
                "balloon": {},
                "legend": {
                    "enabled": true,
                    "useGraphSettings": true
                },
                "titles": config.titles,
                "numberFormatter": {
                    "precision": 2,
                    "decimalSeparator": ".",
                    "thousandsSeparator": ","
                },
                "dataProvider": data,
                ...(config.extra || {})
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