
const ctx = document.getElementById('umalisan_postu').getContext('2d');
var graphData = {
    type: 'line',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            borderWidth: 1
        }]
    },
    options: {}
}

const umalisan_postu = new Chart(ctx, graphData);


var socket = new WebSocket('ws://localhost:8000/ws/graph/');

socket.onmessage = function(e) {
	var djangoData = JSON.parse(e.data);
	console.log(djangoData);

	var newGraphData = graphData.data.datasets[0].data;
	console.log(newGraphData);
	newGraphData.shift();
	newGraphData.push(djangoData.value);

	graphData.data.datasets[0].data = newGraphData;
	umalisan_postu.update();

}