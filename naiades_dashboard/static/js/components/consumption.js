<!-- Chart code -->
//Clustered Bar chart
var chart = AmCharts.makeChart("chartdiv2", {
  "type": "serial",
     "theme": "dark",
  "categoryField": "school",
  "rotate": true,
  "startDuration": 1,
  "categoryAxis": {
    "gridPosition": "start",
    "position": "left"
  },
  "trendLines": [],
  "graphs": [
    {
      "balloonText": "This week consumption:[[value]]",
      "fillAlphas": 0.8,
      "id": "AmGraph-1",
      "lineAlpha": 0.2,
      "title": "This week",
      "type": "column",
      "valueField": "this week"
    },
    {
      "balloonText": "Last week:[[value]]",
      "fillAlphas": 0.8,
      "id": "AmGraph-2",
      "lineAlpha": 0.2,
      "title": "Last week",
      "type": "column",
      "valueField": "last week"
    }
  ],
  "guides": [],
  "valueAxes": [
    {
      "id": "ValueAxis-1",
      "position": "top",
      "axisAlpha": 0
    }
  ],
  "allLabels": [],
  "balloon": {},
  "titles": [{
          "text":"This week vs last week consumption"
      }],
  "dataProvider": [
    {
      "school": 'school5',
      "this week": 23.5,
      "last week": 18.1
    },
    {
      "school": 'school21',
      "this week": 30.5,
      "last week": 23.1
    },
    {
      "school": 'school45',
      "this week": 23.5,
      "last week": 18.1
    },
    {
      "school": 'school1',
      "this week": 23.5,
      "last week": 29.1
    },
    {
      "school": 'school2',
      "this week": 18.5,
      "last week": 25.1
    }
  ],
    "export": {
    	"enabled": true
     }

});

var chart = AmCharts.makeChart("chartdiv3", {
    "type": "serial",
    "theme": "dark",
    "handDrawn":true,
    "handDrawScatter":3,
    "legend": {
        "useGraphSettings": true,
        "markerSize":12,
        "valueWidth":0,
        "verticalGap":0
    },
    "dataProvider": [
    {
      "school": 'school5',
      "this week": 23.5,
      "last week": 18.1
    },
        {
      "school": 'school45',
      "this week": 20,
      "last week": 19
    },
    {
      "school": 'school21',
      "this week": 30.5,
      "last week": 23.1
    },
    {
      "school": 'school1',
      "this week": 23.5,
      "last week": 25.1
    },
    {
      "school": 'school2',
      "this week": 18.5,
      "last week": 29.1
    }
    ],
    "valueAxes": [{
        "minorGridAlpha": 0.08,
        "minorGridEnabled": true,
        "position": "top",
        "axisAlpha":0
    }],
    "startDuration": 1,
    "graphs": [{
        "balloonText": "<span style='font-size:13px;'>[[title]] consumption at [[category]]:<b>[[value]]</b></span>",
        "title": "This week",
        "type": "column",
        "fillAlphas": 0.8,

        "valueField": "this week"
    }, {
        "balloonText": "<span style='font-size:13px;'>[[title]] consumption at [[category]]:<b>[[value]]</b></span>",
        "bullet": "round",
        "bulletBorderAlpha": 1,
        "bulletColor": "#FFFFFF",
        "useLineColorForBulletBorder": true,
        "fillAlphas": 0,
        "lineThickness": 2,
        "lineAlpha": 1,
        "bulletSize": 7,
        "title": "Last week",
        "valueField": "last week"
    }],
    "rotate": true,
    "categoryField": "school",
    "categoryAxis": {
        "gridPosition": "start"
    },
    "export": {
    	"enabled": true
     }

});

//Chart 3

var chart = AmCharts.makeChart("chartdiv4", {
    "theme": "dark",
    "type": "serial",
    "dataProvider": [{
      "school": 'school5',
      "this week": 23.5,
      "last week": 18.1
    },
        {
      "school": 'school45',
      "this week": 20,
      "last week": 19
    },
    {
      "school": 'school21',
      "this week": 30.5,
      "last week": 23.1
    },
    {
      "school": 'school1',
      "this week": 23.5,
      "last week": 25.1
    },
    {
      "school": 'school2',
      "this week": 18.5,
      "last week": 29.1
    }],
    "valueAxes": [{
        "unit": "lt",
        "position": "left",
        "title": "Water consumption",
    }],
    "startDuration": 1,
    "graphs": [{
        "balloonText": " This week consumption at [[category]] : <b>[[value]]</b>",
        "fillAlphas": 0.9,
        "lineAlpha": 0.2,
        "title": "this week",
        "type": "column",
        "valueField": "this week"
    }, {
        "balloonText": "Last week consumption at [[category]] : <b>[[value]]</b>",
        "fillAlphas": 0.9,
        "lineAlpha": 0.2,
        "title": "last week",
        "type": "column",
        "clustered":false,
        "columnWidth":0.5,
        "valueField": "last week"
    }],
    "plotAreaFillAlphas": 0.1,
    "categoryField": "school",
    "categoryAxis": {
        "gridPosition": "start"
    },
    "export": {
    	"enabled": true
     }

});