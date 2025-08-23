setInterval(function(){
    $.get('/api/notification/survey-rejeitadu/',function(data) {
        document.getElementById("notifsurveyrejeita").innerHTML = data.value;
    });
}, 5000);
console.log(data.value)