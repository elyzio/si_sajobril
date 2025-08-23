setInterval(function(){
    $.get('/api/notification/implementasaun-rejeitadu/',function(data) {
        document.getElementById("notifimplementasaunrejeita").innerHTML = data.value;
    });
}, 5000);
console.log(data.value)