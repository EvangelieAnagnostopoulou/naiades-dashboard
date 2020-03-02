const getColorBetween = function(fromColor, toColor, ratio) {
    const hex = function(x) {
        x = x.toString(16);
        return (x.length === 1) ? '0' + x : x;
    };
    const hexBetween = function(offset) {
        return Math.ceil(
            parseInt(fromColor.substring(offset, offset + 2), 16) * (1 - ratio) +
            parseInt(toColor.substring(offset, offset + 2), 16) * ratio
        )
    };

    const r = hexBetween(1);
    const g = hexBetween(3);
    const b = hexBetween(5);

    return `#${hex(r)}${hex(g)}${hex(b)}`;
};

const getGreenRedScaleColor = function(ratio) {
    if (ratio < 0.5) {
        return getColorBetween('#04D215', '#ffdb01', ratio * 2)
    } else {
        return getColorBetween('#ffdb01', '#FF0F00', (ratio - 0.5) * 2)
    }
};

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
        const percentage = 10 + (datum.total_consumption - minTotal) / (maxTotal - minTotal) * 80;
        const isMySchool = datum.meter_number === window.USER.meterNumber;

        const $rank = $('<div class="position" />');
        if (idx < 3) {
            $rank
                .addClass('top-three')
                .append($('<img />').attr('src', `${window.STATIC_ROOT}/img/leaderboard/${idx + 1}.png`))
        } else {
            $rank.text(idx + 1);
        }

        $leaderboard.append(
            $('<div />')
                .addClass(isMySchool && 'my-school')
                .append($rank)
                .append($('<div />')
                    .addClass('info')
                    .append($('<div class="name" />').text(`${datum.name}`))
                    .append($('<div class="activity" />').text(datum.activity))
                )
                .append(
                    $('<div />')
                        .addClass('progress-container')
                        .append($('<div class="bar" />')
                            .css('width', `${(percentage + 10).toFixed(1)}%`)
                            .css('background-color', getGreenRedScaleColor(idx / 10))
                        )
                        .append($('<div class="value" />').text(`${parseFloat(datum.total_consumption).toFixed(0)} lt`))
                )
                .append(
                    isMySchool && $('<span />').addClass('my-school').text('My School')
                )
        );
    });

    $container.append($leaderboard);

    function openLeaderBoard(evt, LeaderBoardName) {
      // Declare all variables
      var i, tabcontent, tablinks;

      // Get all elements with class="tabcontent" and hide them
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }

      // Get all elements with class="tablinks" and remove the class "active"
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }

      // Show the current tab, and add an "active" class to the button that opened the tab
      document.getElementById(LeaderBoardName).style.display = "block";
      evt.currentTarget.className += " active";
    }

    // Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();

    };

    function openLeaderBoard(evt, LeaderBoardName) {
      // Declare all variables
      var i, tabcontent, tablinks;

      // Get all elements with class="tabcontent" and hide them
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }

      // Get all elements with class="tablinks" and remove the class "active"
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }

      // Show the current tab, and add an "active" class to the button that opened the tab
      document.getElementById(LeaderBoardName).style.display = "block";
      evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();