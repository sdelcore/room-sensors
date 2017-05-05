var data = {};
var labels = {};

var websocket = new WebSocket("ws://localhost:8000");

websocket.onmessage = function (event) {
  sensor_data = JSON.parse(event.data);
  labels = [];
  data = [];

  for(var sensor in sensor_data)
  {
    for(i = 0; i < sensor_data[sensor].length; i++)
    {
      labels.push(moment(sensor_data[sensor][i]['date']).format('DD-MM-YYYY h:M a'));
      data.push(sensor_data[sensor][i]['value']);
    }
  }

  layout = {
    "yaxis": {
        "range": [
            Math.min.apply(null, data) - 5, 
            Math.max.apply(null, data) + 5
        ],
        "title": sensor_data[sensor][0]['unit']
    }, 
    "xaxis": {
        "range": [
            labels[0], 
            labels[labels.length - 1]
        ]
    }
  };

  plot_data = [
      {
          "y": data, 
          "x": labels
      }
  ];

  Plotly.newPlot(document.getElementById('PlotSpot'), plot_data, layout);
}

websocket.onopen = function (event) {
  websocket.send('sound');
  
}

window.onbeforeunload = function () {
  websocket.close();
}

updatePlot = function(sensor)
{
  websocket.send(sensor);
}

var figure = {
    "frames": [], 
    "layout": {
        "autosize": true, 
        "yaxis": {
            "range": [], 
            "type": "line", 
            "autorange": true, 
            "title": ""
        }, 
        "title": "Sound", 
        "breakpoints": [], 
        "xaxis": {
            "range": [], 
            "type": "date", 
            "autorange": true, 
            "title": " "
        }, 
        "hovermode": "closest"
    }, 
    "data": [
        {
            "autobinx": true, 
            "uid": "dedad9", 
            "ysrc": "sdelcore:2:a84fb3", 
            "xsrc": "sdelcore:2:4de9c6", 
            "name": "Open", 
            "mode": "lines+markers", 
            "y": [], 
            "x": [], 
            "type": "scatter", 
            "autobiny": true,
        }
    ]
}