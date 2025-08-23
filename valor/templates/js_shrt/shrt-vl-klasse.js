document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#reportsChart18"), {
    series: [{
      name: '10 Ano',
      data: ["{% for xx in loopingestudanteVl %}","{{xx.total_Vl_klass|floatformat:'3'}}","{% endfor %}"]
    }, {
      name: '11 Ano',
      data: ["{% for xx in loopingestudanteVl %}","{{xx.total_Vl_klass1|floatformat:'3'}}","{% endfor %}"]
    },{
      name: '12 Ano',
      data: ["{% for xx in loopingestudanteVl %}","{{xx.total_Vl_klass2|floatformat:'3'}}","{% endfor %}"]
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
    colors: ['yellow','red','#000080'],
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
      categories: ["{% for ii in loopingestudanteVl %}","{{ii.nome_periode}}","{% endfor %}"]
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    }
  }).render();
});
