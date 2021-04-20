<template>
    <div>
        <vue-highcharts v-show="chart_ready" :options="options" ref="highcharts"></vue-highcharts>
        <el-checkbox-group v-show="chart_ready" v-model="checkedChartOptions" :min="1" @change="edit_series">
            <el-checkbox v-for="chart in charts" :label="chart" :key="chart">{{chart}}</el-checkbox>
        </el-checkbox-group>
        <br>
    </div>
</template>

<script>
    import VueHighcharts from 'vue2-highcharts';
    import moment from 'moment-timezone';

    const chartOptions = ['Profit', 'Sessions', 'Revenue', 'Avg bid', 'UV', 'ROI', 'Pages/sessions'];

    export default {
        components: {VueHighcharts},
        data() {
            return {
                chart_ready: false,
                series: [],
                current_series: [],
                checkedChartOptions: ['Profit'],
                charts: chartOptions,
                options: {
                    credits: {
                        enabled: false
                    },
                    chart: {
                        zoomType: 'xy'
                    },
                    title: {
                        text: this.$parent.$parent.$options.name  == 'campaigndata' ? 'Website Performance' : 'Campaign Performance'
                    },
                    subtitle: {
                        text: moment(new Date()).add(-15, 'days').format("YYYY/MM/DD") + '  -  ' + moment(new Date()).add(-1, 'days').format("YYYY/MM/DD")
                    },
                    tooltip: {
                        shared: true,
                        style: {fontSize: '18px'}
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'left',
                        x: 80,
                        verticalAlign: 'top',
                        y: 55,
                        floating: true,
                    },
                    xAxis: [{
                        categories: [],
                        crosshair: true
                    }],
                    yAxis: [],
                }
            }
        },
        methods: {
            load(series) {
                let highcharts = this.$refs.highcharts;
                highcharts.delegateMethod('showLoading', 'Loading...');
                highcharts.addSeries(series);
                highcharts.hideLoading();
            },
            get_chart_data(params ,campaign) {

                let end_point = campaign ? '/api/website/chart_data/campaign' : '/api/website/chart_data';
                let query = {
                    'start': moment(new Date()).add(-15, 'days').format("YYYY-MM-DD"),
                    'end': moment(new Date()).add(-1, 'days').format("YYYY-MM-DD"),
                    'campaign_id': params.campaign_id,
                    'site_id': params.site_id,
                    'device': params.device,
                    'source': params.source,
                };

                this.$http.get(end_point, {params: query}).then(res => {
                    if (res.body) {
                        this.series = Object.keys(res.body).map(key => res.body[key]);
                        if (this.series && this.$data.options.yAxis.length == 0) {
                            this.chart_init();
                        } else if (this.$data.options.yAxis.length > 0) {
                            this.clear_chart();
                        }
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            clear_chart() {
                if (this.$data.options.yAxis.length > 0 && this.$refs.highcharts.chart.series) {
                    const that = this;
                    for (let key of that.checkedChartOptions) {
                        let index = that.$refs.highcharts.chart.series.find(ser => ser.name === key).index;
                        that.$refs.highcharts.chart.series[index].remove();
                        that.$refs.highcharts.chart.yAxis[index].remove();
                    }
                    that.init_again();
                }
                // this.chart_init();
            },
            init_again() {
                if (this.checkedChartOptions.length > 0) {
                    const that = this;
                    for (let key of that.checkedChartOptions) {
                        let series_data = [{
                            name: key,
                            type: 'spline',
                            data: that.series.map(a => parseFloat((a[key.replace(/([/]|[\' \'])/, "_").toLowerCase()]).toFixed(3))),
                            tooltip: {valueSuffix: key === 'Profit' ? ' $' : ' '}
                        }];

                        that.$refs.highcharts.chart.addAxis({
                            labels: {format: '{value}'},
                            title: {text: key},
                            opposite: key !== 'Profit',
                        }, false, true);

                        series_data[0].yAxis = that.$data.options.yAxis.find(y => y.title.text === key).index;
                        that.load(series_data[0]);
                    }
                }
            },
            chart_init() {
                let series_data = [{name: 'Profit', type: 'spline', data: [], tooltip: {valueSuffix: ' $'}}];

                // Init profit yAxis
                this.$refs.highcharts.chart.addAxis({
                    labels: {format: '{value}$'},
                    title: {text: 'Profit'},
                    opposite: false
                }, false);

                for (let item of this.series) {
                    // Init X with dates
                    this.$data.options.xAxis[0].categories.push(item['data_date']);
                    series_data[0].data.push(parseFloat(item['profit'].toFixed(3) || 0));
                }

                this.chart_ready = true;
                this.current_series.push('profit');
                this.load(series_data[0]);
            },
            edit_series(keys) {
                if (keys) {
                    const that = this;
                    let update = false;
                    let series_data = [];
                    for (const key of chartOptions) {

                        if (!(that.current_series.includes(key.toLowerCase())) && that.checkedChartOptions.includes(key)) {

                            that.$refs.highcharts.chart.addAxis({
                                labels: {format: '{value}'},
                                title: {text: key},
                                opposite: key !== 'Profit',
                            }, false, true);

                            series_data.push({
                                name: key,
                                type: 'spline',
                                data: that.series.map(a => parseFloat((a[key.replace(/([/]|[\' \'])/, "_").toLowerCase()]).toFixed(3))),
                            });

                            that.current_series.push(key.toLowerCase());
                            series_data[0].yAxis = that.$data.options.yAxis.find(y => y.title.text === key).index;
                            update = true;
                            break;
                        }
                        else if (that.current_series.includes(key.toLowerCase()) && !that.checkedChartOptions.includes(key)) {
                            let index = that.$refs.highcharts.chart.series.find(ser => ser.name === key).index;
                            that.current_series.splice(that.current_series.indexOf(key.toLowerCase()), 1);
                            that.$refs.highcharts.chart.series[index].remove();
                            that.$refs.highcharts.chart.yAxis[index].remove();
                            break;
                        }
                    }
                    if (update) {
                        that.load(series_data[0]);
                    }
                }
            }
        }
    }
</script>

