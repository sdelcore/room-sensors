require.config({
  paths: {
    "jquery": "https://code.jquery.com/jquery-2.2.4.min", 
    "moment": "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.14.1/moment",
    "chartjs": "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.6/Chart.bundle"
  },
  shim: {
		jquery: {
			exports: "$"
    }
  }
});

var websocket = new WebSocket("ws://localhost:8000");

websocket.onmessage = function (event) {
  console.log(JSON.parse(event.data));
}

require(['jquery', 'moment', 'chartjs'], function($ ,moment, Chart) {
  
  function newDate(days) {
		return moment().add(days, 'd').toDate();
	}
  
  var config = {
    type: 'line',
    data: {
      labels: [newDate(-5), newDate(-4), newDate(-3), newDate(-2), newDate(-1), newDate(0)],
      datasets: [{
        data: [2, 5, 3, 4, 7, 3],
        borderColor: "rgba(220,20,20,1)",
        backgroundColor: "rgba(220,20,20,0.5)"
      }]
    },
    options: {
      scales: {
        xAxes: [{
          type: "time",
          time: {
            unit: 'day',
            round: 'day',
            displayFormats: {
              day: 'MMM D'
            }
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  }
  
  var ctx = document.getElementById("canvas").getContext("2d");
	window.myLine = new Chart(ctx, config);
  
});

//HAVE ONCLICK THAT SENDS WEBSOCKET MESSAGE REQUESTING DATA FOR SPECIFIC DATA SETS

window.onbeforeunload = function () {
        websocket.close();
    }