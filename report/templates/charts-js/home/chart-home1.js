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
				backgroundColor: 'rgba(54, 162, 235, 0.5)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1
			}, {
				label: 'Feto',
				data: femaleData,
				backgroundColor: 'rgba(255, 99, 132, 0.5)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});