<template>
    <div id="validation">
        <vue-headful title="Validation"/>
        <v-layout row wrap>
            <v-flex md2>
                <v-menu v-show="tabPosition != 'RTvalidation'" ref="menu" :close-on-content-click="false" v-model="menu" :nudge-right="40"
                        :return-value.sync="date" lazy transition="scale-transition" offset-y full-width
                        min-width="200px">
                    <v-text-field slot="activator" v-model="date" label="Date" prepend-icon="event"
                                  readonly></v-text-field>
                    <v-date-picker v-model="date" :max="yesterday" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                        <v-btn flat color="primary" @click="getRevenueData();getCostData();$refs.menu.save(date)">OK
                        </v-btn>
                    </v-date-picker>
                </v-menu>
            </v-flex>
            <v-spacer></v-spacer>
            <el-radio-group v-model="tabPosition" style="margin-bottom: 30px; margin-right: 150px;">
                <el-radio-button label="Revenue">&nbsp&nbspRevenue&nbsp&nbsp</el-radio-button>
                <el-radio-button label="Cost">&nbsp&nbsp&nbsp&nbsp Cost &nbsp&nbsp&nbsp&nbsp</el-radio-button>
                <el-radio-button v-if="show_rt_validation" label="RTvalidation">RTvalidation</el-radio-button>
            </el-radio-group>
        </v-layout>
        <div class="row" v-show="!loading && tabPosition == 'Revenue'">
            <el-table :data="_tableData" style="width: 100%" highlight-current-row>
                <el-table-column prop="website_name" label="Website" width="400"></el-table-column>
                <el-table-column prop="campaigns_revenue" label="Campaigns Revenue" width="400" :formatter="formatter">
                </el-table-column>
                <el-table-column label="Other" width="400">
                    <template slot-scope="scope">
                        <el-tooltip placement="top">
                            <div slot="content" style="font-size: medium !important">
                                <p>Taboola No Campaign: {{ scope.row.taboola_rt_nc_revenue }}$</p>
                                <p>DFP No Campaign: {{ scope.row.dfp_nc_revenue }}$</p>
                                <p>Other Providers: {{ scope.row.other }}$</p>
                                <p>EOD Ad Sense: {{ scope.row.ad_sense_dfp }}$</p>
                                <p>EOD HB: {{ scope.row.hb_dfp }}$</p>
                            </div>
                            <span>{{ ncFormatter(scope.row) }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column prop="website_revenue" label="Website Revenue" :formatter="formatter"
                                 width="400"></el-table-column>
                <el-table-column prop="diff" label="Difference" width="400">
                    <template slot-scope="scope">
                        <el-tooltip placement="top">
                            <div slot="content" style="font-size: medium !important">
                                <p>Taboola: {{ scope.row.taboola_diff }} out of {{ scope.row.income_taboola }}</p>
                                <p>Outbrain: {{ scope.row.outbrain_diff }} out of {{ scope.row.income_outbrain }}</p>
                                <p>Adx: {{ scope.row.adx_diff }} out of {{ scope.row.income_adx }}</p>
                                <p>HB DFP: {{ scope.row.hb_diff }} out of {{ scope.row.income_h_bid }}</p>
                                <p>Adsense DFP: {{ scope.row.ad_sense_diff }} out of {{ scope.row.income_adsense }}</p>
                                <br>
                                <p>Other: -{{ scope.row.taboola_rt_nc_revenue + scope.row.dfp_nc_revenue}}</p>
                            </div>
                            <span :class="(scope.row.website_revenue > 100) && scope.row.website_revenue * 0.1 < Math.abs(scope.row.diff) ? 'red-label' : ''">{{parseInt(scope.row.diff)}}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="_centered" v-loading="loading" style="width: 100%"></div>
        <template>
            <div id="cost_validation" v-show="!loading2 && tabPosition == 'Cost'">
                <el-table :data="costData" style="width: 100%"
                          :default-sort="{prop: 'difference', order: 'descending'}">
                    <el-table-column prop="website_name" label="Website" width="400"></el-table-column>
                    <el-table-column prop="site_cost" label="Site Cost (Taboola Only)" width="auto">
                        <template slot-scope="scope">
                                <span>{{parseInt(scope.row.s_cost)}} $</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="campaign_cost" label="Campaign Cost (Taboola Only)" width="auto">
                        <template slot-scope="scope">
                                <span>{{parseInt(scope.row.c_cost)}} $</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="difference" label="Difference (Taboola Only)" width="auto">
                        <template slot-scope="scope">
                                <span :class="(scope.row.difference > 100 || scope.row.difference < -100 ) && (scope.row.s_cost * 0.1 < Math.abs(scope.row.difference) || scope.row.c_cost * 0.1 < Math.abs(scope.row.difference)) ? 'red-label' : ''">{{parseInt(scope.row.difference)}} $</span>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div id="rt_validation" v-show="tabPosition == 'RTvalidation'" style="margin-top:-76px">
                <r-tvalidation></r-tvalidation>
            </div>
        </template>
    </div>
</template>

<script>
    import moment from 'moment-timezone';
    export default {
        name: 'validation',
        components: {
            "RTvalidation": require("./RTvalidation.vue").default,
        },
        mounted() {
            this.getRevenueData();
            this.getCostData();
        },
        data() {
            return {
                date: moment().subtract(1, "days").tz("America/New_York").format("YYYY-MM-DD"),
                yesterday: moment().subtract(1, "days").tz("America/New_York").format("YYYY-MM-DD"),
                tabPosition: 'Revenue',
                menu: false,
                modal: false,
                menu2: false,
                picker: new Date().toISOString().substr(0, 10),
                show_rt_validation: this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.rt_validation == 1,
                tableData: [],
                costData: [],
                loading: false,
                loading2: false,
            }
        },
        methods: {
            getCostData() {
                let date = this.date;
                this.loading2 = true;
                this.$http.get("/api/cost_validation", {params: {'date': date}}).then(res => {
                    this.costData = JSON.parse(res.body.data);
                    this.loading2 = false;
                }, res => {
                    this.loading2 = false;
                    this.error = true;
                });
            },
            getRevenueData() {
                let date = this.date;
                this.loading = true;
                this.$http.get("/api/validation", {params: {'date': date}}).then(res => {
                    this.tableData = res.body.data;
                    this.loading = false;
                }, res => {
                    this.error = true;
                    this.loading = false;
                });
            },
            formatter(row, column) {
                return parseInt(row[column.property]);
            },
            ncFormatter(row) {
                return parseInt(row['taboola_rt_nc_revenue'] + row['dfp_nc_revenue'] + row['other'] + row['ad_sense_dfp'] + row['hb_dfp'])
            }
        },
        computed: {
            _tableData() {
                if (!this.tableData) {
                    return [];
                }
                let tableData = this.tableData;
                // Apply Sort
                tableData = tableData.sort(function (a, b) {
                    return b['diff'] - a['diff'];
                });
                return tableData;
            },
        }
    }
</script>

<style scoped>
    .el-tooltip__popper {
        font-size: large !important;
    }

    .red-label {
        color: red;
    }
</style>