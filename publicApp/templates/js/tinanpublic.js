document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#publictinan"), {
    series: [{
      name: 'estudante',
      data: ["{% for xx in looping_total_estudante_tin %}","{{xx.total_estudante_kada_tinan|floatformat:'3'}}","{% endfor %}"]
     
    }],
    chart: {
      height: 400,
      type: 'bar',
      toolbar: {
        show: false
      },
    },
    markers: {
      size: 12
    },
    colors: ['#B3B6B7', 'blue','#4E342E',],
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 90, 100]
      }
    },
    dataLabels: {
      enabled: true,
    },
    stroke: {
      curve: 'smooth',
      width: 1
    },
    xaxis: {
      type: 'text',
      categories: ["{% for ii in looping_total_estudante_tin %}","{{ii.ano}}","{% endfor %}"]
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    }
  }).render();
});
