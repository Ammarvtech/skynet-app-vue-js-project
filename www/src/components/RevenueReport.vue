<template>
    <div id="revenue-report">
        <vue-headful title="Revenue Report"/>
        <div class="container-fluid date-range-controls">
            <div id="report-controls" class="row">
                <div class="col-xs-6">
                    <el-date-picker v-model="date_range" type="daterange"></el-date-picker>
                    <el-select v-model="device" placeholder="Device" v-on:change="getReport">
                        <el-option
                                v-for="device,idx in devices"
                                :key="idx"
                                :label="device.label"
                                :value="device.value">
                        </el-option>
                    </el-select>
                    <el-input v-model="search" style="max-width: 180px;" placeholder="Search"></el-input>
                </div>
                <div class="col-xs-1">
                    <button v-on:click="getReport" type="submit" class="btn btn-primary">Refresh</button>
                </div>
                <div class="block" style="max-width: 200px; float: right">
                    <span class="">Table Height</span>
                    <el-slider v-model="tableHeight" :step="10" :min="400" :max="2000"></el-slider>
                </div>
            </div>
        </div>
        <div id="report-items" class="container-fluid" v-show="!loading">
            <div class="row">
                <div class="col">
                    <div v-show="show_report" class="alert alert-warning" role="alert">
                        <strong>Ooops:</strong> No data found, please select different date range...
                    </div>
                    <el-table :data="computed_report" show-summary :summary-method="customSummary"
                              :default-sort="sortKey" :max-height="_tableHeight"
                              @cell-dblclick="setCustom" :cell-class-name="statColor" class="appeltable">

                        <!--Devices Sub Row-->
                        <el-table-column type="expand">
                            <template slot-scope="props">
                                <table class="subtable">
                                    <tbody>
                                    <tr v-for="device in ['mobile','tablet','desktop','unknown']">
                                        <td style="width: 197px;padding-left: 59px;">{{device}}</td>
                                        <td class="subtd" v-for="col in rfields"
                                            v-if="isIncome(col)">
                                            {{getSubReport(device, props.row.site_id,col)}}
                                        </td>
                                        <td class="subtd">
                                            {{getTotal(device,props.row.site_id,'income')}}
                                        </td>
                                        <td class="subtd" v-for="col in rfields"
                                            v-if="isSpent(col)">
                                            {{getSubReport(device, props.row.site_id,col)}}
                                        </td>
                                        <td class="subtd">
                                            {{getTotal(device,props.row.site_id,'spent')}}
                                        </td>
                                        <td class="subtd">
                                            {{getSubProfit(device, props.row.site_id)}}
                                        </td>
                                        <td class="subtd">
                                            {{getRoi(device, props.row.site_id)}}
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </template>
                        </el-table-column>
                        <!--End Devices Sub Row-->

                        <el-table-column label="Income">
                            <el-table-column prop="website_name" label="Website Name" sortable width="150">
                            </el-table-column>

                            <el-table-column
                                    v-for="col in rfields"
                                    v-if="isIncome(col)"
                                    :prop="col"
                                    :key="col"
                                    :label="beautifyName(col)"
                                    sortable
                                    width="80"
                            >
                            </el-table-column>

                            <el-table-column prop="total_income" label="Total Income" sortable width="80">
                            </el-table-column>

                        </el-table-column>
                        <el-table-column label="Spent" class="category">
                            <el-table-column
                                    v-for="col in rfields"
                                    v-if="isSpent(col)"
                                    :prop="col"
                                    :key="col"
                                    :label="beautifyName(col)"
                                    sortable
                                    :width="col === 'website_name' ? 150 : 80"
                            >
                            </el-table-column>

                            <el-table-column prop="total_spent" label="Total Spent" sortable width="80">
                            </el-table-column>

                            <el-table-column prop="profit" label="Profit" sortable width="80">
                            </el-table-column>

                            <el-table-column prop="roi" label="ROI" sortable width="80">
                            </el-table-column>

                        </el-table-column>
                    </el-table>
                    <button id="show-summary" @click="showSummary = !showSummary"><i class="el-icon-arrow-right"></i>
                    </button>

                    <!--SUMMARY ROW-->
                    <table id="summary-breakdown" v-show="showSummary">
                        <tr v-for="device in ['mobile','tablet','desktop','unknown']">
                            <td class="summarydevice">{{device}}</td>
                            <td class="summarytd" v-for="field in rfields" v-if="isIncome(field)">
                                {{_summary[device][field].toFixed(2)}}
                            </td>
                            <td class="summarytd">{{isNaN(_summary[device]) ? 0 :
                                _summary[device]['totalIncome'].toFixed(2)}}
                            </td>
                            <td class="summarytd" v-for="field in rfields" v-if="isSpent(field)">
                                {{_summary[device][field].toFixed(2)}}
                            </td>
                            <td class="summarytd">{{isNaN(_summary[device]) ? 0 :
                                _summary[device]['totalSpent'].toFixed(2)}}
                            </td>
                            <td class="summarytd">{{isNaN(_summary[device]) ? 0 :
                                _summary[device]['profit'].toFixed(2)}}
                            </td>
                            <td class="summarytd">{{isNaN(_summary[device]) ? 0 : _summary[device]['roi'].toFixed(2)}}
                            </td>
                        </tr>
                    </table>
                    <!--END SUMMARY ROW-->
                </div>
            </div>
        </div>

        <div v-if="report.length > 0" class="col-md-1">
            <download-excel style="" class="excel v-btn theme--light info" name="revenue_report.xls" :fields="json_fields" :data="report">Export excel<i style="padding-left:10px;padding-bottom: 3px;" class="far fa-file-excel"></i></download-excel>
        </div>

        <div class="_centered" v-loading="loading" style="width: 100%"></div>
    </div>
</template>

<script>
    import Datepicker from "vuejs-datepicker";
    import moment from 'moment-timezone';

    export default {
        name: "revenue-report",
        components: {
            Datepicker,
        },
        mounted() {
            this.$emit('validateUser');
            this.getReport();
        },
        data() {
            return {
                /* Default initializers */
                json_fields: {
                    'Website name': 'website_name',
                    'Site id': 'site_id',
                    'Income adsense': 'income_adsense',
                    'Income adx': 'income_adx',
                    'Income exchange': 'income_exchange',
                    'Income h bid': 'income_h_bid',
                    'Income other': 'income_other',
                    'Income outbrain': 'income_outbrain',
                    'Income revcontent': 'income_revcontent',
                    'Income taboola': 'income_taboola',
                    // 'Income_teads': 'income_teads',
                    // 'Income underdog': 'income_underdog',
                    // 'Income viewdeos': 'income_viewdeos',
                    'Total income': 'total_income',
                    'Spent facebook': 'spent_facebook',
                    'Spent gemini': 'spent_gemini',
                    'Spent outbrain': 'spent_outbrain',
                    'Spent revcontent': 'spent_revcontent',
                    'Spent taboola': 'spent_taboola',
                    'Spent taboola brl': 'spent_taboola_brl',
                    'Spent zemanta': 'spent_zemanta',
                    'Total spent': 'total_spent',
                    'Profit': 'profit',
                    'ROI': 'roi'
                },
                loading: false,
                show_report: false,
                showSummary: false,
                report: [],
                device_report: [],
                yesterday_report: [],
                summary: [],
                device: null,
                search: '',
                tableHeight: 1000,
                devices: [
                    {label: 'mobile', value: 'mobile'},
                    {label: 'tablet', value: 'tablet'},
                    {label: 'desktop', value: 'desktop'},
                    {label: 'unknown', value: 'unknown'},
                    {label: 'All', value: 'null'}
                ],
                date_range: [new Date(Date.now() - 8.64e7), new Date(Date.now() - 8.64e7)],
                rfields: [],
                sortKey: {prop: 'profit', order: 'descending'}
            }
        },
        methods: {
            getReport() {
                this.loading = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");
                let yesterday = moment(this.date_range[0]).subtract(1, 'day').format("YYYY-MM-DD");
                let endpoint = `/api/revenue?date_start=${start}&date_end=${end}&date_yesterday=${yesterday}&device=${this.device}`;
                let params = {
                    'date_start': start,
                    'date_end': end,
                    'date_yesterday': yesterday,
                    'device': this.device,
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.get(endpoint, {params: params}).then(res => {
                    this.report = res.body.report;
                    Object.keys(this.report[0]).forEach((i) => {
                        if (i.indexOf("income_") > -1 || i.indexOf("spent_") > -1 && i.indexOf("source") === -1) {
                            this.rfields.indexOf(i.toString()) === -1 ? this.rfields.push(i.toString()) : '';
                        }
                    });
                    this.rfields = this.rfields.sort();
                    this.yesterday_report = res.body.yesterday_report;
                    this.device_report = res.body.device_report;
                    this.loading = false;
                    if (this.report.length === 0) {
                        this.show_report = true;
                    }
                    this.getSummary(res.body.device_report);
                }).catch(e => {
                    this.loading = false;
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                });
            },
            customSummary(param) {

                const {columns, data} = param;
                const sums = [];
                let ti;
                let ts;

                columns.forEach((column, idx) => {
                    if (column.label === 'Total Income') ti = idx;
                    if (column.label === 'Total Spent') ts = idx;

                    if (idx === 0) {
                        sums[idx] = '_';
                        return;
                    }
                    const values = data.map(item => Number(item[column.property]));
                    if (!values.every(value => isNaN(value))) {
                        sums[idx] = values.reduce((prev, curr) => {
                            const value = Number(curr);
                            if (!isNaN(value)) {
                                return prev + curr;
                            } else {
                                return prev;
                            }
                        }, 0);
                    } else {
                        sums[idx] = 'All';
                    }

                });

                sums[this.rfields.length + 5] = (sums[ti] - sums[ts]) / sums[ts];
                return Object.values(sums).map(i => !isNaN(i) ? parseFloat(i).toFixed(2) : i);
            },
            statColor(item) {
                let row = item.row;
                let col = item.column.ptopertyl
                if (item.column.property === 'income_other' && item.row[item.column.property] > 0) {
                    return 'green-label';
                }
                return (item.row[item.column.property] === -1) ? 'red' : this.usereal(item);
            },
            usereal(item) {
                let row = item.row;
                let key = item.column.property || '';
                if (item.row !== 'undefined') {
                    if (key.match(/^(website_name|total_income|total_spent|profit|roi)$/)) {
                        return false;
                    } else {
                        let type = key.split("_")[0];
                        let provider = key.replace(type + '_', '');
                        let source = type === 'income' ? '_source' : '_spent_source';
                        return row[provider + source] === 'USER' ? 'green-label' : false;
                    }
                }
            },
            getSubReport(device, siteId, col) {
                let row = this.device_report.filter(i => (i.site_id === siteId && i.device === device));
                try {
                    return row[0][col].toFixed(2);
                }
                catch (err) {
                    return 0;
                }
            },
            beautifyName(name) {
                return name.replace('income_', '').replace('spent_', '').replace('_', ' ');
            },
            isIncome(col) {
                col = col.toLowerCase();
                return col.indexOf('income') > -1 && col.indexOf('total') === -1;
            },
            isSpent(col) {
                col = col.toLowerCase();
                return col.indexOf('spent') > -1 && col.indexOf('total') === -1;
            },
            setCustom(item, column) {
                let c1 = moment(this.date_range[0]).isSame(this.date_range[1]);
                let c2 = column.label;
                let c3 = this.device === null;
                if (c1 && c2 && c3) {
                    let key = column.property;
                    let new_value = prompt("Enter updated value:");
                    this.$http.post("/api/revenue", {
                        "date": moment(this.date_range[0]).format("YYYY-MM-DD"),
                        "site_id": item.site_id.toString(),
                        "key": key + "_u",
                        "val": new_value,
                        "login_time": this.$store.getters.getUser.loginTime,
                    }).then(res => {
                        for (let row of this.report) {
                            if (row.site_id === item.site_id) {
                                row[usereal] = 'USER';
                                row[key] = new_value;
                            }
                        }
                    }).catch(e => {
                        if(e.status === 401) {
                            this.$emit('logout');
                        }
                    });
                } else if (!c1) {
                    alert("Custom values not available when date range is selected.");
                }
            },
            getSummary(report) {
                let sum = [];
                let rfields = this.rfields;
                for (let device of ['mobile', 'tablet', 'desktop', 'unknown']) {
                    sum[device] = [];
                    sum[device]['totalIncome'] = sum[device]['totalSpent'] = 0;
                    for (var field of rfields) {
                        sum[device][field] = report.map(i => { // array of the values
                            return i["device"] === device ? i[field] || 0 : 0;
                        }).reduce(function (x, y) { // sum of array
                            return x + y;
                        });
                        if (this.isIncome(field)) {
                            sum[device]['totalIncome'] += sum[device][field];
                        } else if (this.isSpent(field)) {
                            sum[device]['totalSpent'] += sum[device][field];
                        }
                    }
                    sum[device]["profit"] = sum[device]['totalIncome'] - sum[device]['totalSpent'];
                    sum[device]["roi"] = sum[device]["profit"] / sum[device]['totalSpent'];
                }
                this.summary = sum;
            },
            getTotal(device, siteId, type) {
                const that = this;
                let total = 0;
                let row = this.device_report.filter(i => (i.site_id === siteId && i.device === device));
                this.rfields.forEach(idx => {
                    if (row[0]) {
                        if (type === 'income') {
                            if (that.isIncome(idx) && idx in row[0]) {
                                total += row[0][idx];
                            }
                        } else {
                            if (that.isSpent(idx) && idx in row[0]) {
                                total += row[0][idx];
                            }
                        }
                    }
                });
                return parseFloat(total).toFixed(2);
            },
            getSubProfit(device, siteId) {
                let income = this.getTotal(device, siteId, 'income');
                let spent = this.getTotal(device, siteId, 'spent');
                return parseFloat(income - spent).toFixed(2);
            },
            getRoi(device, siteId) {
                let profit = this.getSubProfit(device, siteId);
                let spent = this.getTotal(device, siteId, 'spent');
                return spent > 0 ? parseFloat(profit / spent).toFixed(2) : 'NA';
            }
        },
        computed: {
            computed_report() {
                let validator = (n, field) => {
                    return yesterday_report[n] ? yesterday_report[n][field] : 0;
                };

                let currency = (n) => {
                    let amount = parseFloat(n).toFixed(2);
                    return isNaN(amount) ? 0 : +amount;
                };

                let currency_cmpr = (n, yesterday) => {
                    if (n == null && yesterday > 0 && this.device === null) {
                        return -1;
                    }
                    let amount = parseFloat(n).toFixed(2);
                    return isNaN(amount) ? 0 : +amount;
                };

                let yesterday_report = this.yesterday_report.map((yesterday_item) => {
                    this.rfields.forEach(i => {
                        yesterday_item[i] = currency(yesterday_item[i])
                    });
                    return yesterday_item;
                });

                const clone = (this.device !== null && this.device !== 'null') ? this.device_report : this.report;
                let report = clone.map((item, i) => {
                    this.rfields.forEach(idx => {
                        item[idx] = currency_cmpr(item[idx], validator(i, idx.toString()));
                    });
                    let incomes = 0;
                    let spent = 0;
                    this.rfields.forEach(idx => {
                        if (this.isIncome(idx)) {
                            incomes += item[idx];
                        } else if (this.isSpent(idx)) {
                            spent += item[idx];
                        }
                    });

                    item.total_income = parseFloat(incomes).toFixed(2);
                    item.total_spent = parseFloat(spent).toFixed(2);
                    item.profit = currency(item.total_income - item.total_spent);
                    item.roi = (item.total_spent > 0) ? currency(item.profit / item.total_spent) : 0;

                    return item;
                });
                if (this.device !== null && this.device !== 'null') {
                    report = report.filter(i => i.device === this.device);
                }

                if (this.search) {
                    report = report.filter(i =>
                        i.website_name.toLocaleLowerCase().indexOf(this.search.toLocaleLowerCase()) !== -1
                    );
                }
                return report;
            },
            _summary() {
                return this.summary;
            },
            _tableHeight() {
                return this.tableHeight
            }
        }
    }
</script>

<style>
    #report-items table {
        width: 99.2% !important;
    }

    #report-items th {
        text-transform: capitalize;
    }

    #report-items {
        margin-top: 15px;
    }

    #report-items table th.sortable:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    #report-items table th:nth-child(2),
    #report-items table th:nth-child(3) {
        text-align: center;
    }

    #report-items th .cell, #report-items table tr td:nth-child(2) {
        font-weight: bold;
    }

    #report-items table td {
        padding: 5px 0;
        text-align: left;
    }

    #report-items .has-gutter tr:last-child td {
        font-weight: bold;
        background-color: #ddd !important;
    }

    #report-items table td:hover {
        cursor: pointer;
    }

    #report-items .cell {
        word-break: inherit;
        padding: 0 5px !important;
    }

    #report-items .green-label {
        color: #08d208;
        font-weight: bold;
    }

    #report-items .red {
        color: red;
        font-weight: bold;
    }

    #report-items ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }

    #report-items span.caret-wrapper {
        display: none !important;
    }

    #report-items .subtable {
        width: 100% !important;
        background-color: #ddd;
    }

    #report-items .subtable tr {
        background-color: transparent;
    }

    #report-items .subtable tr:last-child {
        background-color: #ffa8a8;
    }

    #report-items .subtable:hover {
        background-color: #ddd;
    }

    #report-items .subtd {
        padding: 5px 9px !important;
        width: 80px;
    }

    .summarytd {
        width: 80px;
        overflow: hidden;
        white-space: nowrap;
    }

    .summarydevice {
        width: 197px !important;
    }

    #show-summary {
        position: relative;
        left: 15px;
        bottom: 25px;
        background: #ddd;
    }

    #summary-breakdown td {
        border: 1px solid #ddd;
    }

    .col-xs-6 {
        width: auto;
    }

    @media screen and (max-width: 1600px) {
        #summary-breakdown {
            display: none;
        }
    }

    @media screen and (min-width: 1601px) and (max-width: 2000px) {
        .appeltable {
            width: 94vw;
        }
    }

    @media screen and (min-width: 1400px) and (max-width: 1600px) {
        .appeltable {
            width: 90vw;
        }
    }

    @media screen and (min-width: 800px) and (max-width: 1399px) {
        .appeltable {
            width: 86vw;
        }
    }

    @media screen and (min-width: 300px) and (max-width: 799px) {
        .appeltable {
            width: 80vw;
        }
    }

    @media screen and (min-width: 300px) and (max-width: 400px) {
        .appeltable {
            width: 72vw;
        }
    }

    .el-date-editor--daterange.el-input, .el-date-editor--daterange.el-input__inner, .el-date-editor--timerange.el-input, .el-date-editor--timerange.el-input__inner {
        width: auto;
    }
</style>

