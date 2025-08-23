setInterval(function(){
    $.get('/api/notification/monitoring-implementasaun/',function(data) {
        document.getElementById("notifMonitoringImplementasaun").innerHTML = data.value;
    });
}, 5000);
console.log(data.value)