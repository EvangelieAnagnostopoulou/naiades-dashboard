window.COMPONENT_CALLBACKS.weekly_consumption_by_meter = function($container, metric, data) {
    const $leaderboard = $('<div />')
        .addClass('leaderboard');

    // parse & find min/max
    const totals = [];
    $.each(data, function(idx, datum) {
        datum.total_consumption = parseFloat(datum.total_consumption);
        totals.push(datum.total_consumption);
    });

    const minTotal = Math.min.apply(Math, totals);
    const maxTotal = Math.max.apply(Math, totals);

    $.each(data, function(idx, datum) {
        const percentage = (datum.total_consumption - minTotal) / (maxTotal - minTotal) * 90;

        $leaderboard.append(
            $('<div />')
                .append($('<div class="position" />').text(idx + 1))
                .append($('<div />')
                    .addClass('info')
                    .append($('<div class="name" />').text(`Meter #${datum.meter_number}`))
                    .append($('<div class="activity" />').text(datum.activity))
                )
                .append(
                    $('<div />')
                        .addClass('progress-container')
                        .append($('<div class="bar" />').css('width', `${(percentage + 10).toFixed(1)}%`))
                        .append($('<div class="value" />').text(`${parseFloat(datum.total_consumption).toFixed(2)} lt`))
                )
        );
    });

    $container.append($leaderboard);
};