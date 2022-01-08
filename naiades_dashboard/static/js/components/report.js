/**
 * Define export function
 */

function exportReport() {

  // So that we know export was started
  console.log(`${window.MESSAGES.report.startingExport}...`);

  // Define IDs of the charts we want to include in the report
  var ids = ["chart-you_vs_others", "chart-total_hourly_consumption", "chart-total_daily_consumption", "chart-you_vs_others_weekly_change", "chart-weekly_change"];
  //var ids = ["chartdiv1", "chartdiv2", "chartdiv3", "chartdiv4"];

  // Collect actual chart objects out of the AmCharts.charts array
  var charts = {}
  var charts_remaining = ids.length;
  for (var i = 0; i < ids.length; i++) {
    for (var x = 0; x < AmCharts.charts.length; x++) {
      // charts[ids[i]] = AmCharts.charts[x];
      if (AmCharts.charts[x].div && AmCharts.charts[x].div.id == ids[i])
        charts[ids[i]] = AmCharts.charts[x];
    }
  }

  // Trigger export of each chart
  for (var x in charts) {
    if (charts.hasOwnProperty(x)) {
      var chart = charts[x];
      chart["export"].capture({}, function() {
        this.toPNG({}, function(data) {

          // Save chart data into chart object itself
          this.setup.chart.exportedImage = data;

          // Reduce the remaining counter
          charts_remaining--;

          // Check if we got all of the charts
          if (charts_remaining == 0) {
            // Yup, we got all of them
            // Let's proceed to putting PDF together
            generatePDF();
          }

        });
      });
    }
  }

  function generatePDF() {

    // Log
    console.log(`${window.MESSAGES.report.generatingPDF}...`);
    console.log(charts);
    // Initiliaze a PDF layout
    var layout = {
      "content": []
    };

    // Let's add a custom title
    layout.content.push({
      "text": window.MESSAGES.report.weeklyTitle,
      "fontSize": 15,
      "alignment": "center",
    });

    // Now let's grab actual content from our <p> intro tag
    layout.content.push({
      "text": document.getElementById("intro").innerHTML
    });

    // Put two next charts side by side in columns
    layout.content.push({
      "columns": [{
        "width": "50%",
        "image": charts["chart-you_vs_others"].exportedImage,
        "fit": [250, 300]
      }, {
        "width": "*",
        "image": charts["chart-you_vs_others_weekly_change"].exportedImage,
        "fit": [250, 300]
      }],
      "columnGap": 10
    });

    // Add bigger chart
    layout.content.push({
      "image": charts["chart-total_hourly_consumption"].exportedImage,
      "fit": [523, 300]
    });

    // Add bigger chart
    layout.content.push({
      "image": charts["chart-total_daily_consumption"].exportedImage,
      "fit": [523, 300]
    });

    // Add bigger chart
    layout.content.push({
      "image": charts["chart-weekly_change"].exportedImage,
      "fit": [523, 300]
    });

    // Add chart and text next to each other
    /*layout.content.push({
      "columns": [{
        "width": "25%",
        "image": charts["chartdiv4"].exportedImage,
        "fit": [125, 300]
      }, {
        "width": "*",
        "stack": [
          document.getElementById("note1").innerHTML,
          "\n\n",
          document.getElementById("note2").innerHTML
        ]
      }],
      "columnGap": 10
    });*/

    // Trigger the generation and download of the PDF
    // We will use the first chart as a base to execute Export on
    chart["export"].toPDF(layout, function(data) {
      this.download(data, "application/pdf", "amCharts.pdf");
    });

  }

}