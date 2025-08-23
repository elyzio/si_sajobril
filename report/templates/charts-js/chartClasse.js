document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#chartClasse"), {
    series: [{
      name: '10 aNO',
      data: ["{% for xx in loopingturm %}","{{xx.tot|floatformat:'3'}} ","{% endfor %}"]
    }, {
      name: '11 ANO',
      data: ["{% for xx in loopingturm %}","{{xx.tot1|floatformat:'3'}}","{% endfor %}"]
    }, {
      name: '12 ANO',
      data: ["{% for xx in loopingturm %}","{{xx.tot2|floatformat:'3'}}","{% endfor %}"]
    
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
    colors: ['#909497', '#82e0aa'],
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
      categories: ["{% for ii in loopingturm %}","{{ii.Turma}}","{% endfor %}"]
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    }
  }).render();
});
