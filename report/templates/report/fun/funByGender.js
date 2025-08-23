var ctx = document.getElementById("funByGender").getContext('2d');
        var sexoChart = new Chart(ctx, {
            type: 'doughnut',  // Change to 'pie' if you prefer pie chart
            data: {
                labels: [{% for item in count_by_gender_fun%}"{{item.Sexo}}",{% endfor %}],
                datasets: [{
                    data: [{% for item in count_by_gender_fun%}{{item.total}},{% endfor %}],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',  // Blue
                        'rgba(255, 99, 132, 0.7)'   // Red
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                legend: {
                    position: 'bottom'
                }
                // title: {
                //     display: true,
                //     text: 'Grafiku funsionariu tuir sexo'
                // }
            }
        });