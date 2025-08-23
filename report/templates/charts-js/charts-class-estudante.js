document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#reportsChart2"), {
    series: [{
      name: 'CT',
      data: ["{% for xx in loopingestudanteClasse %}","{{xx.total_Clase_CT|floatformat:'3'}}","{% endfor %}"]
    }, {
      name: 'CSH',
      data: ["{% for xx in loopingestudanteClasse %}","{{xx.total_Clase_CSH|floatformat:'3'}}","{% endfor %}"]
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
    colors: ['yellow', 'blue','red','green'],
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 0,
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
      categories: ["{% for ii in loopingestudanteClasse %}","{{ii.name}}","{% endfor %}"]
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    }
  }).render();
});
