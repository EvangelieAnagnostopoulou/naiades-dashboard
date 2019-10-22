$(function () {
    const CHART_CONFIGS = {
        total_hourly_consumption: {
            categoryField: "hour",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]:[[value]]",
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
        total_daily_consumption: {
            categoryField: "day",
            graphs: [
                {
                    "balloonText": "[[title]] of [[category]]:[[value]]",
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
        }
    };

    $.each($('.amchart'), function(idx, amchart) {
        const $amchart = $(amchart);
        const chartId = $amchart.attr('id');
        const metric = chartId.split('-')[1];
        const config = CHART_CONFIGS[metric];

        // set as loading
        $amchart
            .empty()
            .addClass('loading')
            .append($('<i>').addClass('fa fa-spinner fa-spin'));

        // request data from backend
        $.ajax({
            url: `/api/measurements/data?metric=${metric}`,
            success: function({data}) {
                AmCharts.makeChart(chartId,
                    {
                        "type": "serial",
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
                        "dataProvider": data,
                        ...(config.extra || {})
                    }
                );
            },
            error: function(error) {
                $amchart
                    .empty()
                    .removeClass('loading')
                    .addClass('error')
                    .text(`An error occurred when loading data for ${metric}`)
            }
        });
    })
});