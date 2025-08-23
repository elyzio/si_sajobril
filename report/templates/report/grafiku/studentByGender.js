var ctx = document.getElementById("genderByClassChart");

	var classLabels = ['Mane','Feto'];

	var maleData = [1,2,3];
	var femaleData = [1,2,3];

	var genderByClassChart = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: classLabels,
			datasets: [{
				label: 'Mane',
				data: maleData,
				backgroundColor: 'rgb(0, 138, 0)',
				borderColor: 'rgb(16, 187, 0)',
				borderWidth: 1
			}, {
				label: 'Feto',
				data: femaleData,
				backgroundColor: 'rgb(255, 151, 33)',
				borderColor: 'rgb(252, 80, 0)',
				borderWidth: 1
			}]
		},
		options: {
			responsive: false,
			maintainAspectRatio: false,
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});