<template>
    <div id="campaigns_main">
        <h1>Taboola Real Time Alpha</h1>
        <el-row slot="custom-tool-bar" :gutter="20" style="margin-bottom: 15px">
         <el-col :span="2">
            <el-button v-if="campaign === 'back'" type="primary" @click="actionsDef.def[0].handler()" icon="el-icon-arrow-left" disabled plain >Back</el-button>
            <el-button v-else="" type="primary" @click="actionsDef.def[0].handler()" icon="el-icon-arrow-left" plain >Back</el-button>
          </el-col>
            <el-col :span="2">
                <el-button type="success" @click="actionsDef.def[1].handler()" icon="el-icon-search" plain >Go</el-button>
            </el-col>
            <el-col :span="5">
                <el-select v-model="site_id" filterable placeholder="Websites">
                    <el-option v-for="website in websites" :label="website.website_name"
                               :value="website.website_id" :key="website.website_id">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span="9">
                <el-date-picker v-model="date_range" type="datetimerange"
                                start-placeholder="Start Date"
                                range-separator="|"
                                end-placeholder="End Date"
                                size="large"
                                :default-time="['00:00:00','23:59:59']">
                </el-date-picker>
            </el-col>
        </el-row>

        <el-card header="Domains Totals" style="padding-bottom: 7px">
            <data-tables v-if="campaignsSummary" :data="campaignsSummary" :pagination-def="{show:false}"
                         :search-def="{show:false}" :table-props="{rowClassName:tableRowClassName, stripe: false}">


                <el-table-column label="Domain" width="75">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>{{ scope.row.website_name }}</p>
                        <div class="domain-col" :style="{'background': stringToColour(scope.row.website_name)}" slot="reference">{{ scope.row.acronym }}</div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="Date" key="max_date" prop="max_date" width="155" sortable="custom">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>Max Date: {{ lastDateCol(scope.row, "max_date") }}</p>
                        <p>Min Date: {{ lastDateCol(scope.row, "min_date") }}</p>
                        <div class="date-col" slot="reference">{{ lastDateCol(scope.row, "max_date") }}</div>
                    </el-popover>
                </template>
            </el-table-column>
            <!--<el-table-column label="Date" key="max_date" prop="max_date" width="155" sortable="custom">-->
                <!--<template slot-scope="scope">-->
                    <!--{{ lastDateCol(scope.row, "max_date") }}-->
                <!--</template>-->
            <!--</el-table-column>-->
            <el-table-column label="Clicks" key="clicks" prop="clicks" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "clicks") }}
                </template>
            </el-table-column>
            <el-table-column label="CPC" key="cpc" prop="cpc" width="80" sortable="custom">
                <template slot-scope="scope">
                    {{ fixedThreeFloatCol(scope.row, "cpc") }}
                </template>
            </el-table-column>

            <el-table-column label="UV" width="75" sortable="custom">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <table style="width:100%">
                          <tr>
                            <th>Provider</th>
                            <th>UV</th>
                          </tr>
                          <tr >
                            <td class="tbUV">Taboola</td>
                            <td> ${{ floatCol(scope.row, "p_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="adsUV">Adsense</td>
                            <td> ${{ floatCol(scope.row, "ads_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="hbUV">Header Bidder</td>
                            <td> ${{ floatCol(scope.row, "hb_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="dUV">Estimated Delta</td>
                            <td> ${{ floatCol(scope.row, "d_uv") }}</td>
                          </tr>
                        </table>
                        <div slot="reference">
                            {{ uvFloatFormatter(scope.row) }}
                        </div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="Revenue" key="final_revenue" prop="final_revenue" width="110" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "final_revenue") }}
                </template>
            </el-table-column>
            <el-table-column label="Spent" key="spent" pop="spent" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "spent") }}
                </template>
            </el-table-column>
            <el-table-column label="Profit" key="profit" prop="profit" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "profit") }}
                </template>
            </el-table-column>
            <el-table-column label="ROI" key="roi" prop="roi" width="80" sortable="custom">
                <template slot-scope="scope">
                    {{ fixedThreeFloatCol(scope.row, "roi") }}
                </template>
            </el-table-column>

            </data-tables>
        </el-card>
        <el-row style="padding-bottom: 20px">
            <data-tables v-if="selectedCampaign" :data="[selectedCampaign]" :pagination-def="{show:false}"
                         :search-def="{show:false}">
                <el-table-column v-for="col in colsDrillDownWidget" :key="col.prop" :prop="col.prop" :label="col.label"
                                 :formatter="col.formatter">
                </el-table-column>
            </data-tables>
        </el-row>
        <el-card header="Campaigns Totals" shadow="hover"><div class="centered" v-loading="loading"></div><data-tables v-if="!loading" :data="campaignsData" :search-def="searchDef"
                     border style="width: 100%" :table-props="{rowClassName:tableRowClassName,stripe: false}">
            <el-table-column label="Domain" width="75">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>{{ scope.row.website_name }}</p>
                        <div class="domain-col" :style="{'background': stringToColour(scope.row.website_name)}" slot="reference">{{ scope.row.acronym }}</div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="Campaign ID" key="campaign" prop="campaign" width="105">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>Last Date: {{ scope.row.last_date }}</p>
                        <p>Creation Date: {{ scope.row.creation_date }}</p>
                        <div class="campaign-col" slot="reference">{{ scope.row.campaign }}</div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="Date" key="last_date" prop="last_date" width="155" sortable="custom">
                <template slot-scope="scope">
                    {{ lastDateCol(scope.row, "last_date") }}
                </template>
            </el-table-column>
            <el-table-column label="Clicks" key="clicks" prop="clicks" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "clicks") }}
                </template>
            </el-table-column>
            <el-table-column label="CPC" key="cpc" prop="cpc" width="80" sortable="custom">
                <template slot-scope="scope">
                    {{ fixedThreeFloatCol(scope.row, "cpc") }}
                </template>
            </el-table-column>

            <el-table-column label="UV" width="75" sortable="custom">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <table style="width:100%">
                          <tr>
                            <th>Provider</th>
                            <th>UV</th>
                          </tr>
                          <tr >
                            <td class="tbUV">Taboola</td>
                            <td> ${{ floatCol(scope.row, "p_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="adsUV">Adsense</td>
                            <td> ${{ floatCol(scope.row, "ads_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="hbUV">Header Bidder</td>
                            <td> ${{ floatCol(scope.row, "hb_uv") }}</td>
                          </tr>
                          <tr>
                            <td class="dUV">Estimated Delta</td>
                            <td> ${{ floatCol(scope.row, "d_uv") }}</td>
                          </tr>
                        </table>
                        <div slot="reference">
                            {{ uvFloatFormatter(scope.row) }}
                        </div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="Revenue" key="final_revenue" prop="final_revenue" width="110" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "final_revenue") }}
                </template>
            </el-table-column>
            <el-table-column label="Spent" key="spent" pop="spent" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "spent") }}
                </template>
            </el-table-column>
            <el-table-column label="Profit" key="profit" prop="profit" width="100" sortable="custom">
                <template slot-scope="scope">
                    {{ intCol(scope.row, "profit") }}
                </template>
            </el-table-column>
            <el-table-column label="ROI" key="roi" prop="roi" width="80" sortable="custom">
                <template slot-scope="scope">
                    {{ fixedThreeFloatCol(scope.row, "roi") }}
                </template>
            </el-table-column>
            <el-table-column label="">
                <template slot-scope="scope">
                    <el-dropdown size="medium" trigger="click">
                                  <span class="el-dropdown-link">
                                      <el-button type="success" icon="el-icon-more" size="mini" plain circle></el-button>
                                  </span>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item @click.native="actionColDef.def[0].handler(scope.row)">More</el-dropdown-item>
                            <el-dropdown-item @click.native="actionColDef.def[1].handler(scope.row)">Delta</el-dropdown-item>
                            <el-dropdown-item @click.native="actionColDef.def[3].handler(scope.row)">Debug</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </template>
            </el-table-column>
        </data-tables></el-card>






    </div>
</template>

<script>
    import Switch from '../partials/Switch.vue';
    import Datepicker from "vuejs-datepicker";
    import moment from 'moment-timezone';
    import ElRow from "element-ui/packages/row/src/row";
    import ElCard from "../../../node_modules/element-ui/packages/card/src/main.vue";

    export default {
        components: {
            ElCard,
            ElRow,
            appSwitch: Switch,
            datePicker: Datepicker
        },
        mounted() {
            this.getDefaults();
        },
        data() {
            return {
                websites: [],
                campaignsData: [],
                mediumsData: [],
                loading: false,
                visible1: false,
                cols: [
                    {
                        prop: "last_date",
                        label: "Last Update",
                        formatter: this.dateFormatter
                    },
                    {
                        prop: "last_date",
                        label: "Hour",
                        formatter: this.timeFormatter
                    },
                    {
                        prop: "campaign",
                        label: "Campaign ID",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "clicks",
                        label: "Clicks",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "cpc",
                        label: "CPC",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "p_uv",
                        label: "Taboola UV",
                        formatter: this.fixedFourFloatFormatter
                    },
                    {
                        prop: "hb_uv",
                        label: "HB UV",
                        formatter: this.fixedFourFloatFormatter
                    },
                    {
                        prop: "hb_factor_uv",
                        label: "HB Factor UV",
                        formatter: this.fixedFourFloatFormatter
                    },
                    {
                        prop: "hb_factor",
                        label: "HB Factor",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "spent",
                        label: "Spent",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "final_revenue",
                        label: "Revenue",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "profit",
                        label: "Profit",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.fixedFloatFormatter
                    }
                ],
                colsDrillDownWidget: [
                    {
                        prop: "last_date",
                        label: "Last Update",
                        formatter: this.dateFormatter
                    },
                    {
                        prop: "last_date",
                        label: "Hour",
                        formatter: this.timeFormatter
                    },
                    {
                        prop: "campaign",
                        label: "Campaign ID",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "clicks",
                        label: "Clicks",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "cpc",
                        label: "CPC",
                        formatter: this.intFormatter
                    },
                    {
                        label: "UV",
                        formatter: this.uvFloatFormatter
                    },
                    {
                        prop: "final_revenue",
                        label: "Revenue",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "spent",
                        label: "Spent",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "profit",
                        label: "Profit",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.fixedFloatFormatter
                    }
                ],
                colsSummaryWidget: [
                    {
                        prop: "website_name",
                        label: "Domain",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "clicks",
                        label: "Clicks",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "cpc",
                        label: "CPC",
                        formatter: this.intFormatter
                    },
                    {
                        label: "UV",
                        formatter: this.uvFloatFormatter
                    },
                    {
                        prop: "final_revenue",
                        label: "Revenue",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "spent",
                        label: "Spent",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "profit",
                        label: "Profit",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.fixedFloatFormatter
                    }
                ],
                colsSummary: [
                    {
                        prop: "last_date",
                        label: "Last Update",
                        formatter: this.datetimeFormatter
                    },
                    {
                        prop: "website_name",
                        label: "Domain",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "campaign",
                        label: "Campaign ID",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "clicks",
                        label: "Clicks",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "cpc",
                        label: "CPC",
                        formatter: this.intFormatter
                    },
                    {
                        label: "UV",
                        formatter: this.uvFloatFormatter
                    },
                    {
                        prop: "final_revenue",
                        label: "Revenue",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "spent",
                        label: "Spent",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "profit",
                        label: "Profit",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.fixedFloatFormatter
                    }
                ],
                colsMedium: [
                    {
                        prop: "last_date",
                        label: "Last Update",
                        formatter: this.datetimeFormatter
                    },
                    {
                        prop: "website_name",
                        label: "Domain",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "campaign",
                        label: "Campaign ID",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "medium",
                        label: "Medium",
                        formatter: this.defaultFormatter
                    },
                    {
                        prop: "clicks",
                        label: "Clicks",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "visits",
                        label: "Visits",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "cpc",
                        label: "CPC",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "p_uv",
                        label: "Taboola UV",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "final_revenue",
                        label: "Revenue",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "spent",
                        label: "Spent",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "profit",
                        label: "Profit",
                        formatter: this.fixedFloatFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.fixedFloatFormatter
                    }
                ],
                filter: null,
                prv_filter: null,
                site_filter: null,
                date_range: [new Date(Date.now()).setHours(0,0,0,0), new Date(Date.now()).setHours(23,59,59,0)],
                account_filter: null,
                campaign: 'back',
                medium: false,
                campaignsSummary: null,
                selectedCampaign: null,
                user_id: '',
                provider_id: '',
                perPage: 20,
                currentPage: 1,
                hide: false,
                filterAccounts: [],
                site_id: '',
                searchDef: {
                    show: true
                },
                actionsDef: {
                    colProps: {
                        span: 3
                    },
                    def: [
                        {
                            name: 'Back',
                            handler: () => {
                                // to-do a good practice is to cache last result
                                if (this.campaign !== 'back') {
                                    this.$message(`Back Up`);
                                    this.selectedCampaign = null;
                                    this.getCampaigns();
                                    this.getCampaignsSummary();
                                }
                                else {
                                    this.$message(`Please select campaign`);

                                }
                            },
                            icon: 'el-icon-arrow-left',
                            buttonProps: {
                                type: 'primary',
                                plain: true
                            }
                        },
                        {
                            name: 'Go',
                            handler: () => {
                                this.getCampaigns();
                                this.getCampaignsSummary();
                            },
                            icon: 'el-icon-search',
                            buttonProps: {
                                type: 'success',
                                plain: true
                            }
                        }]
                },
                actionColDef: {
                    label: 'Actions',
                    tableColProps: {
                        align: 'center'
                    },
                    def: [{
                        handler: row => {
                            if (this.campaign === row.campaign) {
                                this.$message(`Back Up`);
                                this.selectedCampaign = null;
                                this.medium = false;
                                this.getCampaigns();
                            }
                            else {
                                this.campaign = row.campaign;
                                this.$message(`${row.campaign} Drill Down`);
                                this.selectedCampaign = row;
                                this.getCampaign(row.website_id);
                            }
                        },

                        buttonProps: {
                            type: 'success',
                            plain: true,
                            icon: 'el-icon-more'
                        }

                    },
                        {
                            handler: row => {
                                if (this.campaign === row.campaign) {
                                    this.$message(`Back Up`);
                                    this.selectedCampaign = null;
                                    this.medium = false;
                                    this.getCampaigns();
                                }
                                else {
                                    this.campaign = row.campaign;
                                    this.$message(`${row.campaign} Delta Drill Down`);
                                    this.selectedCampaign = row;
                                    this.getCampaignDelta(row.website_id);
                                }
                            },
                            buttonProps: {
                                type: 'info',
                                plain: true,
                                icon: 'el-icon-tickets'
                            },
                        },
                        {
                            handler: row => {
                                if (this.campaign === row.campaign) {
                                    this.$message(`Back Up`);
                                    this.selectedCampaign = null;
                                    this.medium = false;
                                    this.getCampaigns();
                                }
                                else {
                                    this.campaign = row.campaign;
                                    this.$message(`${row.campaign} Medium Drill Down`);
                                    this.selectedCampaign = row;
                                    this.medium = true;
                                    this.getCampaignMediums(row.website_id);
                                }
                            },
                            buttonProps: {
                                type: 'blue',
                                plain: true,
                                icon: 'el-icon-news'
                            },
                        },
                        {
                            handler: row => {
                                this.openBox(row)
                            },
                            buttonProps: {
                                type: 'blue',
                                plain: true,
                                icon: 'el-icon-question'
                            },
                        }

                    ]
                },
                pPercent: 0,
                pStatus: ''
            }
        },
        methods: {
            getDefaults() {
                this.$http.get("/api/website/user_websites").then(res => {
                    //Fast all sites workaround
                    //to-do show all sites only if admin or dan
                    this.websites = res.body;
                    let allSitesID = [];
                    for (let web in this.websites) {
                        allSitesID.push(this.websites[web]['website_id'])
                    }
                    let allSite = {};
                    allSite['url'] = "http://omgstudios.com/";
                    allSite['website_id'] = allSitesID.toString();
                    allSite['website_name'] = "All";

                    this.websites[Object.keys(this.websites).length+1] = this.websites[0];
                    this.websites[0] = allSite;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            getCampaigns() {
                this.loading = true;
                this.medium = false;
                this.mediumsData = [];
                this.campaign = 'back';
                let start = moment(this.date_range[0]).format("YYYY-MM-DD") + " 00:00:00";
                let end = moment(this.date_range[1]).format("YYYY-MM-DD") + " 23:59:59";
                this.$http.get("/api/realtime/campaigns?site_id=" + this.site_id + "&start=" + start + "&end=" + end).then(res => {
                    this.campaignsData = res.body.campaigns;
                    this.loading = false;

                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            getCampaign(siteID) {
                this.loading = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD HH:mm:ss");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD HH:mm:ss");
                this.$http.get("/api/realtime/campaigns/" + this.campaign + "?site_id=" + siteID + "&start=" + start + "&end=" + end).then(res => {
                    this.campaignsData = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            getCampaignMediums(siteID) {
                this.loading = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD") + " 00:00:00";
                let end = moment(this.date_range[1]).format("YYYY-MM-DD") + " 23:59:59";
                this.$http.get("/api/realtime/campaigns/mediums/" + this.campaign + "?site_id=" + siteID + "&start=" + start + "&end=" + end).then(res => {
                    this.mediumsData = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            getCampaignDelta(siteID) {
                this.loading = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD") + " 00:00:00";
                let end = moment(this.date_range[1]).format("YYYY-MM-DD") + " 23:59:59";
                this.$http.get("/api/realtime/campaigns/delta/" + this.campaign + "?site_id=" + siteID + "&start=" + start + "&end=" + end).then(res => {
                    this.campaignsData = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            getCampaignsSummary() {
                this.loading = true;
                this.medium = false;
                this.mediumsData = [];
                this.campaignData = 'back';
                let start = moment(this.date_range[0]).format("YYYY-MM-DD") + " 00:00:00";
                let end = moment(this.date_range[1]).format("YYYY-MM-DD") + " 23:59:59";
                this.$http.get("/api/realtime/campaigns/summary?site_id=" + this.site_id + "&start=" + start + "&end=" + end).then(res => {
                    this.campaignsSummary = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            defaultFormatter(row, column) {
                return row[column.property];
            },
            lastDateCol(row, column) {
                return row[column].replace('T',' ')
            },
            datetimeFormatter(row, column) {
                return row[column.property].replace('T',' ')
            },
            dateFormatter(row, column) {
                return row[column.property].split('T')[0]
            },
            timeFormatter(row, column) {
                return row[column.property].split('T')[1].substr(0, 2)
            },
            intFormatter(row, column) {
                return parseFloat(row[column.property])
            },
            fixedFloatFormatter(row, column) {
                return parseFloat(row[column.property]).toFixed(2)
            },
            fixedFourFloatFormatter(row, column) {
                return parseFloat(row[column.property]).toFixed(4)
            },
            fixedThreeFloatCol(row, column) {
                return parseFloat(row[column]).toFixed(3)
            },
            intCol(row, column) {
                return parseInt(row[column])
            },
            floatCol(row, column) {
                return parseFloat(row[column]).toFixed(3)
            },
            uvFloatFormatter(row) {
                return parseFloat(row['p_uv']+row['hb_uv']+row['ads_uv']+row['d_uv']).toFixed(4)
            },
            handleRowClick(row, event, column) {
                //to-do modal on specific column click for more campaign options
                if (column.property !== 'campaign') {
                    if (this.campaign === row.campaign) {
                        this.$message(`Back Up`);
                        this.getCampaigns();
                    }
                    else {
                        this.campaign = row.campaign;
                        this.$message(`${row.campaign} Drill Down`);
                        this.getCampaign();
                    }

                    console.log(row, event, column);
                }
            },
            openBox(row) {
                this.$confirm(row, 'Debug: Raw Data', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'info'
                }).then(() => {
                    this.$message({
                        type: 'success',
                        message: 'Debug completed'
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: 'Debug canceled'
                    });
                });
            },
            stringToColour(str) {
              let hash = 0;
              for (let i = 0; i < str.length; i++) {
                hash = str.charCodeAt(i) + ((hash << 5) - hash);
              }
              let colour = '#';
              for (let i = 0; i < 3; i++) {
                let value = (hash >> (i * 8)) & 0xFF;
                colour += ('00' + value.toString(16)).substr(-2);
              }
              return colour;
            },
            tableRowClassName({row, rowIndex}) {
             if ( (parseFloat(row.roi) < -0.5 && parseInt(row.clicks) > 500|| parseFloat(row.roi) > 1.5 && parseInt(row.clicks) > 500)) {
                  return 'warning-row';
                } else {
                  return '';
                }
              }
        },
        watch: {},
        computed: {
            progressPercent: function () {
                return this.pPercent
            },
            progressStatus: function () {
                return this.pStatus
            }
        },
    }
</script>

<style>
    ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }

    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }
    .el-message-box {
	    width: 80%!important;
    }
    .tbUV{
        color: dodgerblue;
        font-weight: bold;
        padding-top: 2px ;
    }
    .hbUV{
        color: green;
        font-weight: bold;
        padding-top: 2px ;
    }
    .adsUV{
        color: orange;
        font-weight: bold;
        padding-top: 2px ;
    }
    .dUV{
        color: purple;
        font-weight: bold;
        padding-top: 2px ;
    }
    .line-separator{
        height:1px;
        background:black;
        border-bottom:1px solid black;
    }
    .campaign-col{
        color: black;
        font-weight: bolder;
    }
    .domain-col{
      width: 30px;
      height: 30px;
      border-radius: 50%;
      font-size: 10px;
      color: #fff;
      text-align: center;
      line-height: 30px;
      margin: 5px 0;
      font-weight: 900;
    }
    .search{
        width: 100%;
    }
    .el-table{
    border-collapse:separate;
    border:solid lightgrey 1px;
    border-radius:6px;
    -moz-border-radius:6px;
    text-align:center;
    margin-left:auto;
    margin-right:auto;
    }
    .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
    .table-header {
        padding-top: 8px;
        font-weight: 900;
        font-size: large;
    }
</style>
