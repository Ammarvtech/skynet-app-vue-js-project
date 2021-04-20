<template>
    <vue-highcharts :options="pieOptions" ref="pieChart"></vue-highcharts>
</template>

<script>
    import VueHighcharts from 'vue2-highcharts';

    export default {
        name: "MPieChart",
        components: {VueHighcharts},
        data() {
            return {
                pieOptions: {
                    credits: {
                        enabled: false
                    },
                    chart: {
                        height: 280,
                        //width: 280,
                        type: 'pie',
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
                            innerSize: 50,
                            depth: 70,
                            size: 100,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y} $',
                                distance: 10,
                                rotation: 5,
                            }
                        }
                    },
                    tooltip: {
                        pointFormat: '<b>{series.name}: {point.percentage:.1f}% | {point.y}$</b>'
                    },
                    series: [{
                        name: 'Total',
                        //startAngle: 100,
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

<style scoped>

</style>