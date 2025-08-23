document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#reportsChart14"), {
    series: [{
      name: '$',
      data: ["{% for xx in looping_total_estudante_propinas_tin %}","{{xx.total_propinas_per_ano}}","{% endfor %}"]
   
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
    colors: ['RoyalBlue', 'red','black'],
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
      categories: ["{% for ii in looping_total_estudante_propinas_tin %}","{{ii.ano}}","{% endfor %}"]
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    }
  }).render();
});
