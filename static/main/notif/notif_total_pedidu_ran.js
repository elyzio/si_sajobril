setInterval(function(){
    $.get('/api/notification/blood/request',function(data) {
        document.getElementById("notifbloodrequest").innerHTML = data.value;
    });
}, 100);
console.log(data.value)