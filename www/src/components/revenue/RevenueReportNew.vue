<template>
    <div id="revenue-new">
        <div class="row">
            <div :class="[(wXS || wSM || wMD) ? 'input-m col-xs-2' : 'col-xs-2']">
                <el-date-picker v-model="date_range" type="daterange" align="center"></el-date-picker>
            </div>
            <div :class="[(wXS || wSM || wMD) ? 'float-non input-m sub' : 'input_desk', 'col-xs-2']">
                <el-select v-model="selected_device" placeholder="Device" filterable>
                    <el-option v-for="device in devices" :label="device.label" :value="device.value" :key="device.value"></el-option>
                </el-select>
            </div>
            <div :class="[(wXS || wSM || wMD) ? 'float-non input-m sub' : '', 'col-xs-2']">
                <el-select v-model="selected_campaign_source" placeholder="Source" filterable>
                    <el-option v-for="source in sources" :label="source" :value="source" :key="source"></el-option>
                </el-select>
            </div>
            <div :class="[(wXS || wSM || wMD) ? 'float-non sub' : '', 'col-xs-1']">
                <el-button @click="init_data" type="primary" size="medium">SUBMIT</el-button>
            </div>
        </div>
        <div class="break"></div>
        <div v-loading="load">
            <el-table :data="data" style="width: 100%" @expand-change="expend" :default-sort="sortKey" :border="true" :summary-method="summary" show-summary>
                <el-table-column type="expand">
                    <template slot-scope="slot">
                        <el-row v-if="(wLG || wXL)" type="flex" class="row-bg" justify="space-around" style="height: 600px;">
                            <el-col :span="6">
                                <div :class="['hr-sect']">INCOME</div>
                                <div><p :class="['t_total']">TOTAL INCOME: {{slot.row.revenue}} $</p></div>
                                <div class="block">
                                    <pie_chart :ref="'income_source_' + slot.row.site_id"></pie_chart>
                                    <pie_chart :ref="'income_device_' + slot.row.site_id"></pie_chart>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div :class="['hr-sect']">SPENT</div>
                                <div><p :class="['t_total']">TOTAL SPENT: {{slot.row.spent}} $</p></div>
                                <pie_chart :ref="'spent_source' + '_' + slot.row.site_id"></pie_chart>
                                <pie_chart :ref="'spent_device' + '_' + slot.row.site_id"></pie_chart>
                            </el-col>
                        </el-row>
                        <div v-else>
                            <div :class="['income_span_m']">
                                <div :class="['hr-sect']">INCOME</div>
                                <div class="block">
                                    <el-carousel :autoplay=false arrow="always">
                                        <el-carousel-item>
                                            <m_pie_chart :ref="'income_source' + '_' + slot.row.site_id"></m_pie_chart>
                                        </el-carousel-item>
                                        <el-carousel-item>
                                            <m_pie_chart :ref="'income_device' + '_' + slot.row.site_id"></m_pie_chart>
                                        </el-carousel-item>
                                    </el-carousel>
                                </div>
                            </div>
                            <p :class="['total']">TOTAL INCOME: {{slot.row.revenue}} $</p>
                            <div :class="['spent_span_m']">
                                <div :class="['hr-sect']">SPENT</div>
                                <div class="block">
                                    <el-carousel :autoplay=false arrow="always">
                                        <el-carousel-item>
                                            <m_pie_chart :ref="'spent_source' + '_' + slot.row.site_id"></m_pie_chart>
                                        </el-carousel-item>
                                        <el-carousel-item>
                                            <m_pie_chart :ref="'spent_device' + '_' + slot.row.site_id"></m_pie_chart>
                                        </el-carousel-item>
                                    </el-carousel>
                                </div>
                            </div>
                            <p :class="['total']">TOTAL SPENT: {{slot.row.spent}} $</p>
                            <p :class="['hr-sect']">SUMMERY</p>
                            <p :class="['_total']">PROFIT: {{slot.row.profit}} $</p>
                            <p :class="['_total']">ROI: {{slot.row.roi}}</p>
                        </div>
                        <div v-if="(wLG || wXL)" class="divider"></div>
                        <el-row v-if="(wLG || wXL)" type="flex" class="row-bg" justify="space-around">
                            <el-col :span="6">
                            </el-col>
                            <el-col :span="6" style="padding-left: 7px;">
                                <div :class="['hr-sect']">SUMMERY</div>
                                <p :class="['_total']">PROFIT: {{slot.row.profit}} $</p>
                                <p :class="['_total']">ROI: {{slot.row.roi}}</p>
                            </el-col>
                            <el-col :span="6">
                            </el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <el-table-column v-for="field in ((wLG || wXL) ? d_fields : m_fields)" :prop="field" :key="field" :label="field.toUpperCase()" sortable></el-table-column>
            </el-table>
        </div>
    </div>
</template>


<script>
    import moment from 'moment-timezone';

    export default {
        name: "RevenueReportNew",
        components: {
            "pie_chart": require("./PieChart.vue").default,
            "m_pie_chart": require("./MPieChart.vue").default,
        },
        mounted() {
            this.get_source();
            this.init_data();
        },
        data() {
            return {
                load: true,
                devices: [
                    {label: 'Mobile', value: 'mobile'},
                    {label: 'Tablet', value: 'tablet'},
                    {label: 'Desktop', value: 'desktop'},
                    {label: 'All', value: 'all'}
                ],
                sources: [],
                inited: [],
                selected_device: 'All',
                selected_campaign_source: 'All',
                sortKey: {prop: 'profit', order: 'descending'},
                date_range: [new Date(Date.now() - 8.64e7), new Date(Date.now() - 8.64e7)],
                d_fields: ['name', 'revenue', 'spent', 'profit', 'roi'],
                m_fields: ['name', 'profit', 'roi'],
                data: [],
                device_data: [],
                getColor: {
                    'income_taboola': '#ffbc21',
                    'income_facebook': '#424248',
                    'income_gemini': '#f75d5a',
                    'income_revcontnet': '#f7a35c',
                    'spent_taboola': '#ffbc21',
                    'spent_facebook': '#424248',
                    'spent_gemini': '#f75d5a',
                    'spent_revcontnet': '#f7a35c',
                },
            };
        },
        methods: {
            init_data() {
                this.load = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");
                let device = this.selected_device && this.selected_device.toLowerCase() != 'all' ? this.selected_device.toLowerCase() : 'all';
                let source = this.selected_campaign_source && this.selected_campaign_source.toLowerCase() != 'all' ? this.selected_campaign_source.toLowerCase() : 'all';

                let params = {'device': device, 'source': source, 'start': start, 'end': end};

                this.$http.get('/api/init_revenue', {params: params}).then(res => {
                    if (res.body) {
                        this.tmp_data = Object.keys(res.body).map(key => res.body[key]);
                        this.data = this.tmp_data[0];
                        this.provider_data = this.tmp_data[1];
                        this.device_data = this.tmp_data[2];
                        this.load = false;
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            get_source: function () {
                this.$http.get("/api/website/source").then(res => {
                    if (res.body) {
                        this.sources = Object.values(res.body).map(i => i.provider_name);
                        this.sources.unshift("All");
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            expend(row, expandedRows) {
                let _row = document.getElementsByClassName('el-table__expand-icon el-table__expand-icon--expanded').length;
                if (_row > 0 && expandedRows.length > 0) {
                    document.getElementsByClassName('el-table__expand-icon el-table__expand-icon--expanded')[0].getElementsByClassName('el-icon el-icon-arrow-right')[0].click();
                }
                if (row && !(this.inited.includes(row.site_id))) {
                    this.inited.push(row.site_id)
                } else {
                    this.inited = this.inited.filter(item => item != row.site_id);
                    if (expandedRows.length > 0) {
                        this.inited.push(expandedRows[0].site_id)
                    }
                }
                const site_id = this.inited[0];
                setTimeout(() => {
                    let el = this.$el.querySelector(".el-table__expanded-cell");
                    if(el){
                        el.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
                    }
                    this.init_providers_charts(site_id);
                    this.init_devices_charts(site_id);
                }, 1);
            },
            init_providers_charts(site_id) {
                const p_id = this.provider_data.findIndex(function (element) {
                    return element.site_id === site_id;
                });
                let data = this.provider_data[p_id];
                if (data) {
                    this.$refs['income_source_' + this.inited[0]].init_chart(this.sum_data('income', _(data).toPairs().sortBy(0).fromPairs().value()));
                    this.$refs['spent_source_' + this.inited[0]].init_chart(this.sum_data('spent', _(data).toPairs().sortBy(0).fromPairs().value()));
                }
            },
            init_devices_charts(site_id) {
                const d_id = this.device_data.findIndex(function (element) {
                    return element.site_id === site_id;
                });
                let item = this.device_data[d_id];
                if (item) {
                    this.$refs['income_device_' + this.inited[0]].init_chart(this.sum_data('income', _(item).toPairs().sortBy(0).fromPairs().value()));
                    this.$refs['spent_device_' + this.inited[0]].init_chart(this.sum_data('spent', _(item).toPairs().sortBy(0).fromPairs().value()));
                }
            },
            sum_data(type, data) {
                let arr = [];
                let action = type.toString();
                const that = this;
                return Object.keys(data).filter(function (k) {
                    return k.indexOf(type) == 0;
                }).reduce(function (newData, k) {
                    if (data[k] > 0 && k != 'spent') {
                        arr.push({
                            'name': k.replace(action + "_", "").charAt(0).toUpperCase() + k.replace(action + "_", "").slice(1),
                            "y": parseFloat(data[k]),
                            "color": that.getColor[k]
                        })
                    }
                    return arr
                }, {});
            },
            summary(param) {
                const {columns, data} = param;
                const sums = [];

                columns.forEach((column, index) => {

                    if (index === 0 || index === 5) {
                        sums[index] = '';
                        return;
                    }
                    const values = data.map(item => Number(item[column.property]));
                    if (!values.every(value => isNaN(value))) {
                        sums[index] = values.reduce((prev, curr) => {
                            const value = Number(curr);
                            if (!isNaN(value)) {
                                return parseFloat((prev + curr).toFixed(1));
                            } else {
                                return parseFloat((prev).toFixed(1));
                            }
                        }, 0);
                    } else {
                        sums[index] = 'ALL';
                    }
                });

                return sums;
            },
        },
    }
</script>

<style scoped>
    @import "../../assets/styles/pages/_Revenue.scss";
</style>
