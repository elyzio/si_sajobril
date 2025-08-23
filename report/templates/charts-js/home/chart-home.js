var ctx = document.getElementById("genderByClassChart");

	var classLabels = [{% for cls, _ in class_gender_counts.items %}"{{ cls }}"{% if not forloop.last %}, {% endif %}{% endfor %}];

	var maleData = [{% for _, data in class_gender_counts.items %}{{ data.Mane }}{% if not forloop.last %}, {% endif %}{% endfor %}];
	var femaleData = [{% for _, data in class_gender_counts.items %}{{ data.Feto }}{% if not forloop.last %}, {% endif %}{% endfor %}];

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