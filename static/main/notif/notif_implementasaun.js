setInterval(function(){
    $.get('/api/notification/implementasaun/',function(data) {
        document.getElementById("notifimplementasaun").innerHTML = data.value;
    });
}, 5000);
console.log(data.value)