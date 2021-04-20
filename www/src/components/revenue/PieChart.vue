<template>
    <vue-highcharts :options="pieOptions" ref="pieChart"></vue-highcharts>
</template>

<script>
    import VueHighcharts from 'vue2-highcharts';

    export default {
        name: "PieChart",
        components: {VueHighcharts},
        data() {
            return {
                pieOptions: {
                    credits: {
                        enabled: false
                    },
                    chart: {
                        height: 300,
                        type:
                            'pie',
                    },
                    title: {
                        text: ''
                    },
                    subtitle: {
                        text: ''
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            showInLegend: true,
                            cursor: 'pointer',
                            innerSize: 80,
                            depth: 100,
                            size: 180,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y} $',
                                rotation: 15,
                            }
                        }
                    },
                    tooltip: {
                        pointFormat: '<b>{series.name}: {point.percentage:.1f}% | {point.y}$</b>'
                    },
                    series: [{
                        name: 'Total',
                        startAngle: 45,
                        data: []
                    }]
                }
            }
        },
        methods: {
            init_chart(data) {
                let pie = this.$refs.pieChart.chart;
                pie.series[0].setData(data);
            },
        }
    }

</script>
