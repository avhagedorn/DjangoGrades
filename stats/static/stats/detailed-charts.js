Chart.defaults.global.animation.duration = 1600;
Chart.defaults.scale.gridLines.drawOnChartArea = false;

var avgOptions = {
        responsive: true,
        maintainAspectRatio: false,
        beginAtZero:false,
        elements: {
            point:{
                backgroundColor: "#f2f2f2"
            }
        },
        legend: {
            display: false,
        },
        title: {
              display: true,
              text: 'Average Grades',
            fontColor: "#f2f2f2"
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "#f2f2f2",
                    stepSize: 5,
                },
                gridLines: {
                      display: false
                },
            }],
            xAxes: [{
                ticks: {
                    display: false
                },
                gridLines: {
                    display: false
                },
            }]
        },
   }


var studentOptions = {
    responsive: true,
    maintainAspectRatio: false,
    beginAtZero:false,
    elements: {
        point:{
            backgroundColor: "#f2f2f2"
        }
    },
    legend: {
        display: false,
    },
    title: {
          display: true,
          text: 'Assignment Grades',
        fontColor: "#f2f2f2"
    },
    scales: {
        yAxes: [{
            ticks: {
                fontColor: "#f2f2f2",
                stepSize: 10,
            },
            gridLines: {
                  display: false
            },
        }],
        xAxes: [{
            ticks: {
                display: false
            },
            gridLines: {
                display: false
            },
        }]
    },
}

var distOptions = {
        responsive: true,
        maintainAspectRatio: false,
        beginAtZero:false,
        elements: {
            point:{
                backgroundColor: "#f2f2f2"
            }
        },
        legend: {
            display: false,
        },
        title: {
              display: true,
              text: 'Grade Distribution',
            fontColor: "#f2f2f2"
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "#f2f2f2",
                    stepSize: 20,
                },
                gridLines: {
                      display: false
                },
            }],
            xAxes: [{
                ticks: {
                    min: 0,
                    stepSize: 1,
                    fontColor: "#f2f2f2"
                },
                gridLines: {
                    display: false
                },
            }]
        }, 
    }

var letterDistOptions = {
        responsive: true,
        maintainAspectRatio: false,

        legend: {
            display: false,
        },
        title: {
            display: false
        },
        
    }

var avgTitle = {
    display: true,
    text: 'Average Grades',
    fontColor: "#f2f2f2"
    }