<template>
    <div id="RTValidation">
        <vue-headful title="Websites Campaigns"/>
        <!--<div v-show="!showMediumkey">-->
        <div>
            <!--Campaign - Form-->
            <form @submit="submit">
                <div class="row">
                    <div class="col-xs-2">
                        <websites-dropdown @selectWebsite="selectWebsite($event)"></websites-dropdown>
                    </div>
                    <div class="col-xs-2">
                        <v-select v-model="selected_device" :items="devices" label="Device"></v-select>
                    </div>
                    <div class="col-xs-2">
                        <sources-dropdown @selectSource="selectSource($event)"></sources-dropdown>
                    </div>
                    <div class="col-xs-2" style="width: 16% !important;">
                        <v-menu full-width offset-y :close-on-content-click="false" bottom v-model="dateMenu">
                            <v-btn color="primary" outline slot="activator">{{ date_range[0] }} &mdash; {{ date_range[1]
                                }}
                            </v-btn>
                            <v-card>
                                <v-card-text>
                                    <v-daterange highlight-colors="blue-grey" :options="dateRangeOptions"
                                                 @input="onDateRangeChange"/>
                                </v-card-text>
                            </v-card>
                        </v-menu>
                    </div>
                    <div>
                        <v-btn @click="items=[]" type="submit" color="info" :disabled="loading">Submit</v-btn>
                    </div>
                </div>
            </form>

            <!--Device - Source - Tags-->
            <el-tag ref="filter_field" :class="[filterMobile ? 'filter_hide' : '']" type="success"></el-tag>
            <el-tag :class="[filter_fields_hide ? 'filter_hide' : '','fixed']" type="success" :closable="true"
                    @close="filterClose"></el-tag>

            <!--Filter & perPage-->
            <div :class="[disabled ? 'tb-hide' : '','row']">
              <search-box @selectFilter="selectFilter($event)"></search-box>
                <div class="top col-xs-2" style="padding-top: 32px">
                    <el-tooltip class="item" effect="dark" content="Per Page" placement="top-start">
                        <el-input-number size="small" v-model="perPage" controls-position="right" :min="5"
                                         :step="5"></el-input-number>
                    </el-tooltip>
                    <el-tooltip class="item" effect="dark" content="Minimum Clicks" placement="top-start">
                        <el-input-number size="small" v-model="minClicks" controls-position="right" :min="0"
                                         :step="100"></el-input-number>
                    </el-tooltip>
                </div>
            </div>

            <!--Campaigns-Websites-Table-->
            <table class="table table-striped table-hover" :class="[hide ? 'tb-hide' : '','']">
                <thead>
                <tr>
                    <th v-for="(field, key) in tfields" @click="headClick(field,key, true)" class="pointer th_width"
                        :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']">
                        <div v-if="field.description">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    <strong>{{field.description}}</strong><br>
                                    <strong v-if="field._description">{{field._description}}</strong>
                                </div>
                                <strong>{{field.label}}&ensp; <span
                                        class="sub_label">{{field.sub_label}}</span></strong>
                            </el-tooltip>
                        </div>
                        <div v-else>
                            <strong :class="[field.sub_label === 'final' ? 'th_width': '']">{{field.label}}&ensp; <span
                                    class="sub_label">{{field.sub_label}}</span></strong>
                        </div>
                    </th>
                </tr>
                </thead>
                <tbody>
                <!--site summary start-->
                <tr v-if="items.length > 0" style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of devices</div><span>{{_summary('device')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of sources</div><span>{{_summary('source')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of sites</div><span>{{_count_sites()}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of campaigns</div><span>{{_summary('campaigns')}}</span></el-tooltip></td>

                <td class="summary"><span>N/A</span></td>

                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of clicks</div><span>{{_summary('clicks_x')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of clicks</div><span>{{_summary('clicks_y')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Number of clicks</div><span>{{_summary('clicks_x') - _summary('clicks_y')}}</span></el-tooltip></td>

                  <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola Revenue: {{tb_revenue_sum_final | _format_(2)}}<br/>
                                Outbrain Revenue: {{ob_revenue_sum_final | _format_(2)}}<br/>
                                HB Revenue: {{hb_revenue_sum_final | _format_(2)}}<br/>
                                Adx Revenue: {{adx_revenue_sum_final | _format_(2)}}<br/>
                                Ex Revenue: {{ex_revenue_sum_final| _format_(2)}}<br/>
                                Adsense DFP: {{ad_sense_revenue_sum_final | _format_(2)}}<br/>
                                Adsense Analytics: {{ad_sense_mobile_revenue_sum_final | _format_(2)}}
                            </div>
                            <span>{{_summary('revenue_x')}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                  <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola Revenue: {{tb_revenue_sum_rt | _format_(2)}}<br/>
                                Outbrain Revenue: {{ob_revenue_sum_rt | _format_(2)}}<br/>
                                HB Revenue: {{hb_revenue_sum_rt | _format_(2)}}<br/>
                                Adx Revenue: {{adx_revenue_sum_rt | _format_(2)}}<br/>
                                Ex Revenue: {{ex_revenue_sum_rt| _format_(2)}}<br/>
                                Adsense DFP: {{ad_sense_revenue_sum_rt | _format_(2)}}<br/>
                                Adsense Analytics: {{ad_sense_mobile_revenue_sum_rt | _format_(2)}}
                            </div>
                            <span>{{_summary('revenue_y')}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                  <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola Revenue diff: {{tb_revenue_sum_final - tb_revenue_sum_rt | _format_(2)}}<br/>
                                Outbrain Revenue diff: {{ob_revenue_sum_final - ob_revenue_sum_rt | _format_(2)}}<br/>
                                HB Revenue diff: {{hb_revenue_sum_final - hb_revenue_sum_rt | _format_(2)}}<br/>
                                Adx Revenue diff: {{adx_revenue_sum_final - adx_revenue_sum_rt | _format_(2)}}<br/>
                                Ex Revenue diff : {{ex_revenue_sum_final - ex_revenue_sum_rt| _format_(2)}}<br/>
                                Adsense DFP diff: {{ad_sense_revenue_sum_final - ad_sense_revenue_sum_rt | _format_(2)}}<br/>
                                Adsense Analytics diff: {{ad_sense_mobile_revenue_sum_final - ad_sense_mobile_revenue_sum_rt | _format_(2)}}
                            </div>
                            <span>{{_summary('revenue_x') - _summary('revenue_y')}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Total cost</div><span>{{_summary('cost_x')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Total cost</div><span>{{_summary('cost_y')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Total cost</div><span>{{_summary('cost_x') - _summary('cost_y')}}</span></el-tooltip></td>

                <td class="summary"><el-tooltip placement="top"><div slot="content">Total profit</div><span>{{_summary('profit_x')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Total profit</div><span>{{_summary('profit_y')}}</span></el-tooltip></td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Total profit</div><span>{{_summary('profit_x') - _summary('profit_y')}}</span></el-tooltip></td>

                                        <!--<PHASE 2 !!!!!!>-->

                <td class="summary"><el-tooltip placement="top"><div slot="content">Weighted Avg. of UV</div>
                <span>{{_summary('revenue_x') / _summary('clicks_x') | _format_(4)}}</span></el-tooltip>
                </td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Weighted Avg. of UV</div>
                <span>{{_summary('revenue_x') / _summary('clicks_y') | _format_(4)}}</span></el-tooltip>
                </td>
                <td class="summary"><el-tooltip placement="top"><div slot="content">Weighted Avg. of UV</div>
                <span> {{ Math.abs((1-((_summary('revenue_x') / _summary('clicks_x')) / (_summary('revenue_y') / _summary('clicks_y') )))*100) | _format_(2) }}%</span></el-tooltip>
                </td>
                <!--<td class="summary">-->
                <!--<el-tooltip placement="top"><div slot="content">Weighted Avg. of Avg. bids</div>-->
                <!--<span>{{_summary('cost_x') / _summary('clicks_x') | _format_(3)}}</span>-->
                <!--</el-tooltip>-->
                <!--</td>-->
                <!--<td class="summary">-->
                <!--<el-tooltip placement="top"><div slot="content">Weighted Avg. of Avg. bids</div>-->
                <!--<span>{{_summary('cost_y') / _summary('clicks_y') | _format_(3)}}</span>-->
                <!--</el-tooltip>-->
                <!--</td>                <td class="summary">-->
                <!--<el-tooltip placement="top"><div slot="content">Weighted Avg. of Avg. bids</div>-->
                <!--<span>{{_summary('cost_diff') / _summary('clicks_diff') | _format_(3)}}</span>-->
                <!--</el-tooltip>-->
                <!--</td>-->
                <td class="summary"></td>
                </tr>
                <!--site summary end-->

                <tr v-for="(item, index) in _items" v-if="item!==undefined && item.campaign_id!=null" :ref="++index"
                    :key="item.campaign_id">
                    <td>
                        <span class="link" @click="filter_field(item.device, 'device')">{{item.device}}</span>
                    </td>
                    <td>
                        <span class="link" @click="filter_field(item.source, 'source')">{{item.source}}</span>
                    </td>
                    <td>
                        <span>{{item.website_name.toUpperCase() | acronym }}</span>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">{{item.name}}</div>
                            <span>{{item.campaign_id}}</span>
                        </el-tooltip>
                    </td>

                    <td>
                        <span>{{item.creation_date}}</span>
                    </td>

                    <td>
                        <span>{{item.clicks_x}}</span>
                    </td>
                    <td>
                        <span>{{item.clicks_y}}</span>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                DFP Clicks: {{item.clicks_x| _format_(2)}}<br/>
                                RT Clicks: {{item.clicks_y| _format_(2)}}<br/>
                            </div>
                            <span>{{parseInt(item.clicks_diff)}}%</span>
                        </el-tooltip>
                    </td>
                  <td>
                    <el-tooltip placement="top">
                              <div slot="content">
                                  Taboola Revenue: {{item.taboola_revenue_x | _format_(2)}}<br/>
                                  Outbrain Revenue: {{item.outbrain_revenue_x | _format_(2)}}<br/>
                                  HB Revenue: {{item.hb_revenue_dfp_x | _format_(2)}}<br/>
                                  Adx Revenue: {{item.adx_revenue_x | _format_(2)}}<br/>
                                  Ex Revenue: {{item.ex_revenue_x | _format_(2)}}<br/>
                                  Adsense DFP: {{item.ad_sense_revenue_dfp_x | _format_(2)}}<br/>
                                  Adsense Analytics: {{item.ad_sense_mobile_revenue_x | _format_(2)}}
                              </div>
                            <span>{{item.revenue_x| _format_(2)}}</span>
                          </el-tooltip>
                    </td>
                  <td>
                  <el-tooltip placement="top">
                              <div slot="content">
                                  Taboola Revenue: {{item.taboola_revenue_y | _format_(2)}}<br/>
                                  Outbrain Revenue: {{item.outbrain_revenue_y | _format_(2)}}<br/>
                                  HB Revenue: {{item.hb_revenue_dfp_y | _format_(2)}}<br/>
                                  Adx Revenue: {{item.adx_revenue_y | _format_(2)}}<br/>
                                  Ex Revenue: {{item.ex_revenue_y | _format_(2)}}<br/>
                                  Adsense DFP: {{item.ad_sense_revenue_dfp_y | _format_(2)}}<br/>
                                  Adsense Analytics: {{item.ad_sense_mobile_revenue_y | _format_(2)}}
                              </div>
                            <span>{{item.revenue_y| _format_(2)}}</span>
                          </el-tooltip>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                  Taboola Revenue: {{ Math.abs((1-(item.taboola_revenue_x / item.taboola_revenue_y))*100) | _format_(2)}}%<br/>
                                  Outbrain Revenue: {{ Math.abs((1-(item.outbrain_revenue_x / item.outbrain_revenue_y))*100)  | _format_(2)}}%<br/>
                                  HB Revenue: {{Math.abs((1-(item.hb_revenue_dfp_x / item.hb_revenue_dfp_y))*100)  | _format_(2)}}%<br/>
                                  Adx Revenue: {{Math.abs((1-(item.adx_revenue_x / item.adx_revenue_y))*100)   | _format_(2)}}%<br/>
                                  Ex Revenue: {{Math.abs((1-(item.ex_revenue_x / item.ex_revenue_y))*100) | _format_(2)}}%<br/>
                                  Adsense DFP: {{Math.abs((1-(item.ad_sense_revenue_dfp_x / item.ad_sense_revenue_dfp_y))*100) | _format_(2)}}%<br/>
                                  Adsense Analytics: {{Math.abs((1-(item.ad_sense_mobile_revenue_x / item.ad_sense_mobile_revenue_y))*100)  | _format_(2)}}%
                            </div>
                            <span>{{Math.abs(parseInt(item.revenue_diff))}}%</span>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{item.cost_x| _format_(2)}}</span>
                    </td>
                    <td>
                        <span>{{item.cost_y| _format_(2)}}</span>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                DFP Cost: {{item.cost_x| _format_(2)}}<br/>
                                RT Cost: {{item.cost_y| _format_(2)}}<br/>
                            </div>
                            <span>{{parseInt(item.cost_diff)}}%</span>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{item.profit_x| _format_(2)}}</span>
                    </td>
                    <td>
                        <span>{{item.profit_y| _format_(2)}}</span>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                DFP Profit: {{item.profit_x| _format_(2)}}<br/>
                                RT Profit: {{item.profit_y| _format_(2)}}<br/>
                            </div>
                            <span>{{(item.profit_x - item.profit_y)| _format_(2)}}</span>
                        </el-tooltip>
                    </td>

                                    <!--<PHASE 2 !!!!!!>-->
                  <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola UV: {{item.taboola_revenue_x / item.clicks_x | _format_(4)}}<br/>
                                Outbrain UV: {{item.outbrain_revenue_x / item.clicks_x | _format_(4)}}<br/>
                                HB UV: {{item.hb_revenue_dfp_x / item.clicks_x | _format_(4)}}<br/>
                                Adx UV: {{item.adx_revenue_x / item.clicks_x | _format_(4)}}<br/>
                                Ex UV: {{item.ex_revenue_x / item.clicks_x | _format_(4)}}<br/>
                                Adsense DFP UV: {{item.ad_sense_revenue_dfp_X / item.clicks_x | _format_(4)}}<br/>
                                Adsense Analytics UV: {{item.ad_sense_mobile_revenue_x / item.clicks_x | _format_(4)}}
                            </div>
                        <span>{{item.final_uv_x| _format_(4)}}</span>
                        </el-tooltip>
                    </td>
                  <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola UV: {{item.taboola_revenue_y / item.clicks_y | _format_(4)}}<br/>
                                Outbrain UV: {{item.outbrain_revenue_y / item.clicks_y | _format_(4)}}<br/>
                                HB UV: {{item.hb_revenue_dfp_y / item.clicks_y | _format_(4)}}<br/>
                                Adx UV: {{item.adx_revenue_y / item.clicks_y | _format_(4)}}<br/>
                                Ex UV: {{item.ex_revenue_y / item.clicks_y | _format_(4)}}<br/>
                                Adsense DFP UV: {{item.ad_sense_revenue_dfp_X / item.clicks_y | _format_(4)}}<br/>
                                Adsense Analytics UV: {{item.ad_sense_mobile_revenue_y / item.clicks_y | _format_(4)}}
                            </div>
                        <span>{{item.final_uv_y| _format_(4)}}</span>
                        </el-tooltip>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                DFP Final_UV: {{item.final_uv_x| _format_(4)}}<br/>
                                RT Final_UV: {{item.final_uv_y| _format_(4)}}<br/>
                            </div>
                            <span>{{item.final_uv_diff| _format_(0)}}%</span>

<!--                            <span v-if="">{{Math.abs((1-item.final_uv_x/item.final_uv_y))*100 | _format_(2)}}%</span>-->
                        </el-tooltip>
                    </td>
                    <!--<td>-->
                        <!--<span>{{item.avg_bid_x| _format_(2)}}</span>-->
                    <!--</td>-->
                    <!--<td>-->
                        <!--<span>{{item.avg_bid_y| _format_(2)}}</span>-->
                    <!--</td>-->
                    <!--<td>-->
                        <!--<el-tooltip placement="top">-->
                            <!--<div slot="content">-->
                                <!--DFP avg_bid: {{item.avg_bid_x| _format_(2)}}<br/>-->
                                <!--RT avg_bid: {{item.avg_bid_y| _format_(2)}}<br/>-->
                            <!--</div>-->
                            <!--<span>{{item.avg_bid_diff| _format_(2)}}</span>-->
                        <!--</el-tooltip>-->
                    <!--</td>-->
                </tr>
                </tbody>
            </table>

            <div :class="[hide ? 'tb-hide' : '','']" class="col-md-11 text-center">
                <b-pagination size="md" :total-rows="items.length" :per-page="perPage" v-model="currentPage"/>
            </div>
            <div class="_centered" v-loading="loading" style="width: 100%"></div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment-timezone';
    import alerts from "./mixins/alerts";

    export default {
        name: 'RTvalidation',
        mixins: [alerts],
        components: {
            // "medium_key": require("./websites/MediumKey.vue").default,
        },
        mounted() {
            this.$emit('validateUser');
        },
        data() {
            return {
                site_count: new Set(),
                dateMenu: false,
                dateRangeOptions: {
                    startDate: moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    endDate: moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    format: 'MM/DD/YYYY',
                    presets: [
                        {
                            label: 'Today',
                            range: [
                                moment(new Date(Date.now())).format("YYYY-MM-DD"),
                                moment(new Date(Date.now())).format("YYYY-MM-DD"),
                            ],

                        },
                        {
                            label: 'Yesterday',
                            range: [
                                moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                                moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                            ],
                        },
                    ],
                },
                items: [],
                campaign_source: [],
                // websites: [],
                // summary: [],
                colors: [],
                shown_item: '',
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                sources: ['All', 'Taboola','Facebook', 'Gemini', 'Outbrain', 'Revcontent'],
                tfields: {
                    device: {label: 'Device'},
                    source: {label: 'Source'},
                    name: {label: 'Site', sortable: false},
                    campaign_id: {label: 'Campaign ID', sortable: true},
                    creation_date: {label: 'CD', sortable: true, description: 'Creation date'},
                    clicks_x: {label: 'Clicks_Final', sortable: true},
                    clicks_y: {label: 'Clicks_RT', sortable: true},
                    clicks_diff: {label: 'Clicks_Diff', sortable: true},
                    revenue_x: {label: 'Revenue_Final', sortable: true},
                    revenue_y: {label: 'Revenue_RT', sortable: true},
                    revenue_diff: {label: 'Revenue_Diff', sortable: true},
                    cost_x: {label: 'Cost_Final', sortable: true},
                    cost_y: {label: 'Cost_RT', sortable: true},
                    cost_diff: {label: 'Cost_Diff', sortable: true},
                    profit_x: {label: 'Profit_Final', sortable: true, description: '= Revenue - Cost'},
                    profit_y: {label: 'Profit_RT', sortable: true, description: '= Revenue - Cost'},
                    profit_diff: {label: 'Profit_Diff', sortable: true, description: '= Revenue - Cost'},
                    //Phase 2 !!!!!
                    final_uv_x: {label: 'UV_DFP', sortable: true, description: '= Revenue / Clicks'},
                    final_uv_y: {label: 'UV_RT', sortable: true, description: '= Revenue / Clicks'},
                    final_uv_diff: {label: 'UV_Diff', sortable: true, description: '= Revenue / Clicks'},
                    // avg_bid_x: {label: 'Avg_bid_DFP', sortable: true},
                    // avg_bid_y: {label: 'Avg_bid_RT', sortable: true},
                    // avg_bid_diff: {label: 'Avg_bid_Diff', sortable: true},
                },
                filterMobile: true,
                filter_fields_hide: true,
                sortDesc: true,
                sortFlag: false,
                loading: false,
                disabled: true,
                hide: true,
                sort: null,
                filter: null,
                selected_campaign_source: "Taboola",
                selected_device: "All",
                currentPage: 1,
                perPage: 20,
                minClicks: 0,
                date_range: [
                     moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                     moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD")
                ],
                site_id: "All",
                inited_summary: {},
                tb_revenue_sum_final : undefined,
                tb_revenue_sum_rt : undefined,
                ob_revenue_sum_final : undefined,
                ob_revenue_sum_rt : undefined,
                hb_revenue_sum_final : undefined,
                hb_revenue_sum_rt : undefined,
                adx_revenue_sum_final : undefined,
                adx_revenue_sum_rt : undefined,
                ad_sense_revenue_sum_final : undefined,
                ad_sense_revenue_sum_rt : undefined,
                ad_sense_mobile_revenue_sum_final : undefined,
                ad_sense_mobile_revenue_sum_rt : undefined,
                ex_revenue_sum_final : undefined,
                ex_revenue_sum_rt : undefined,
            }
        },
        methods: {
            selectSource(source) {
                this.selected_campaign_source = source;
            },
            selectWebsite(sites) {
                this.site_id = {'website_id': '', 'website_name': ''};
                sites.forEach(site => {
                    this.site_id['website_id'] += site['website_id'] + ',';
                    this.site_id['website_name'] += site['website_name'] + ',';
                });
                this.site_id['website_id'] = this.site_id['website_id'].slice(0, -1);
                this.site_id['website_name'] = this.site_id['website_name'].slice(0, -1);
                this.submit();
            },
            selectFilter(filter) {
                this.filter = filter;
            },
            onDateRangeChange(range) {
                this.date_range = range
            },
            submit: function () {
                this.items = [];

                let site_id = this.site_id === 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
                let device = (this.selected_device ? this.selected_device : 'all').toLocaleLowerCase();
                let source = (this.selected_campaign_source ? this.selected_campaign_source : 'all').toLocaleLowerCase();
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");

                if (site_id === null) {
                    this.alert('website');
                    return;
                }

                this.loading = true;
                this.disabled = true;
                this.hide = true;
                this.inited_summary = {};
                this.site_count = new Set();

                let params = {
                    'site_id': site_id,
                    'device': device,
                    'source': source,
                    'start': start,
                    'end': end,
                    'login_time': this.$store.getters.getUser.loginTime,
                };

                setTimeout(() => {
                    this.get_colors(params);
                }, 1);

                this.$http.get('/api/website/campaigns_rt_validation', {params: params}).then(res => {
                    if (res.body) {
                        this.items = Object.keys(res.body).map(key => res.body[key]);
                        if (this.items.length === 0) {
                            this.filterClose();
                        } else {
                            this.headClick(this.tfields.clicks_x, "clicks_x");
                            this.sortDesc = false;
                            this.hide = false;
                            this.disabled = false;
                            this.mediumKeyword_items = this.items;
                        }
                        this.loading = false;
                    } else {
                        console.log("---------ERROR-----------");
                    }
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
            },
            get_colors: function (params) {
                params.page_type = 'campaign';
                this.$http.get('/api/website/colors', {params: params}).then(res => {
                    if (res.body) {
                        this.colors = Object.keys(res.body).map(key => res.body[key]);
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            filter_field: function (field) {
                this.filter = field;
                this.filterMobile = false;
                this.$refs.filter_field.$el.innerHTML = field;
                this.filter_fields_hide = false;
            },
            filterClose: function () {
                this.filter = "";
                this.filterMobile = true;
                this.filter_fields_hide = true;
            },
            highlight() {
                let obj = this.shown_item === 0 ? this.$refs[1][0] : this.$refs[this.shown_item][0];
                let orig = obj.style.color;
                obj.style.background = '#7ed1ff';
                setTimeout(function () {
                    obj.style.background = orig;
                }, 3000);
            },
            headClick(field, key, flag = false) {
                if (key === 'device' || key === 'source' || key === 'name') {
                    return;
                }
                if (flag) this.sortFlag = !this.sortFlag;
                if (!field.sortable) {
                    return;
                }
                if (key === this.sort) {
                    this.sortDesc = !this.sortDesc;
                }

                this.sort = key;
            },
            color(item, key, val) {
                if (!item) {
                    return
                }
                if (key !== 'roi') {
                    item.source = item.source.toLowerCase().replace('.com', '');
                    const elem = this.colors.find(color =>
                        color.source === item.source &&
                        color.device === item.device &&
                        color.field === key &&
                        color.from <= item[key] && item[key] <= color.to
                    );

                    if (elem) {
                        return elem.color + ' label'
                    } else {
                        return ''
                    }
                } else {
                    if (parseInt(val * 100) <= 129) {
                        return 'label-danger label'
                    } else if (parseInt(val * 100) >= 129 && parseInt(val * 100) <= 149) {
                        return 'label-warning label'
                    } else if (parseInt(val * 100) >= 150) {
                        return 'label-success label'
                    }
                }

            },
            filter_summary() {
                let items = this.items;
                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };
                if (this.filter && this.filter.length > 0) {
                    this.filter = this.filter.trim().toLowerCase();
                    const regex = new RegExp('.*' + this.filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                }
                return items;
            },
            count_values(key, data) {
                return Object.keys(data.reduce((acc, o) => (acc[o[key]] = (acc[o[key]] || 0) + 1, acc), {})).length;
            },
            _summary(key) {
                let _filter = this.filter === '' || this.filter == null;
                if (key === 'campaigns') {
                    return this.filter_summary().length;

                } else if (key === 'device') {
                    return this.selected_device !== 'All' ? 1 : this.count_values('device', !_filter ? this.filter_summary() : this.items);

                } else if (key === 'source') {
                    return this.selected_campaign_source !== 'All' ? 1 : this.count_values('source', !_filter ? this.filter_summary() : this.items);
                }

                let res = parseInt(_.sumBy([key], _.partial(_.sumBy, this.filter_summary())));
                if (res !== undefined) {
                    this.inited_summary[key] = res;
                    return res;
                }
            },
            _count_sites() {
                if (this.site_id !== 'All') {
                    return 1;
                }
                let _filter = this.filter === '' || this.filter == null;
                if (this.inited_summary['sites'] && _filter) {
                    return this.inited_summary['sites'];
                }
                if (!_filter || !this.inited_summary['sites']) {
                    let items = !_filter ? this.filter_summary() : this.items;
                    let acr = '';
                    for (let i of items) {
                        acr = i.name.split('-');
                        let _acr = acr[0].toLowerCase().replace(/ /g, "") !== 'msnsafe' ? acr[0].trim() : this.site_count.add(acr[1].trim());
                        if (!this.sources.includes(_acr) && !this.site_count.has(_acr) && _acr.length <= 3 && _acr !== 'msn') {
                            this.site_count.add(_acr);
                        }
                    }
                    this.inited_summary['sites'] = this.site_count.size;
                    return this.inited_summary['sites'];
                }
            },
        },
        computed: {
            _items() {
                if (!this.items) {
                    return [];
                }

                let items = this.items;

                const fix = v => {
                    if (v instanceof Object) {
                        return ['campaign_id', 'name'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };
                let data = this.filter_summary();

                let sums = {};
                let keys = ['taboola_revenue_x', 'taboola_revenue_y', 'outbrain_revenue_x', 'outbrain_revenue_y',
                  'hb_revenue_dfp_x', 'hb_revenue_dfp_y', 'adx_revenue_x', 'adx_revenue_y', 'ad_sense_revenue_dfp_x',
                  'ad_sense_revenue_dfp_y', 'ad_sense_mobile_revenue_x', 'ad_sense_mobile_revenue_y','ex_revenue_x','ex_revenue_y' ];

                //const self = this;
                _.each(data, function (item) {
                    _.each(keys, function (key) {
                        sums[key] = (parseFloat(sums[key]) || 0) + parseFloat(item[key]);
                    });
                });

                this.tb_revenue_sum_final = sums.taboola_revenue_x;
                this.tb_revenue_sum_rt = sums.taboola_revenue_y;
                this.ob_revenue_sum_final = sums.outbrain_revenue_x;
                this.ob_revenue_sum_rt = sums.outbrain_revenue_y;
                this.hb_revenue_sum_final = sums.hb_revenue_dfp_x;
                this.hb_revenue_sum_rt = sums.hb_revenue_dfp_y;
                this.adx_revenue_sum_final = sums.adx_revenue_x;
                this.adx_revenue_sum_rt = sums.adx_revenue_y;
                this.ad_sense_revenue_sum_final = sums.ad_sense_revenue_dfp_x;
                this.ad_sense_revenue_sum_rt = sums.ad_sense_revenue_dfp_y;
                this.ad_sense_mobile_revenue_sum_final = sums.ad_sense_mobile_revenue_x;
                this.ad_sense_mobile_revenue_sum_rt = sums.ad_sense_mobile_revenue_y;
                this.ex_revenue_sum_final = sums.ex_revenue_x;
                this.ex_revenue_sum_rt = sums.ex_revenue_y;
                // Apply filter
                if (this.filter && this.filter.length > 0) {
                    const regex = new RegExp('.*' + this.filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    const field = this.sort;
                    let flag = this.sortFlag;
                    items = items.sort(function (a, b) {
                        if (field === 'creation_date') {
                            return flag ? new Date(a[field]) - new Date(b[field]) : new Date(b[field]) - new Date(a[field]);
                        } else {
                            return flag ? a[field] - b[field] : b[field] - a[field];
                        }
                    });
                }

                if (this.minClicks) {
                    items = items.filter(i => i.clicks_x > this.minClicks);
                }

                if (items.length < this.perPage) {
                    this.currentPage = 1;
                }

                // Apply pagination
                if (this.perPage) {
                    items = items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage);
                }

                return items;
            },
            _isAll() {
                return this.site_id === 'All';
            }
        },
        filters: {
            _format_: function (value, fix) {
                if (value === 0) {
                    return value;
                }
                if (!value && value !== 0) {
                    return ''
                }
                return parseFloat(value).toFixed(fix);
            },
            format_prc: function (value) {
                if (!value && value !== 0) {
                    return '';
                }
                if (value === '0') {
                    return 0;
                }
                return parseInt(value * 100);
            },
            acronym: function (item) {
                if (!item) {
                    return;
                }
                let acr = item.split(' ');
                if (acr[0].toLowerCase().replace(/ /g, "") !== 'msnsafe') {
                    return acr.map(function (item) {
                        return item[0]
                    }).join('');
                }
                else {
                    return acr[1]
                }
            },
            prc: function (val) {
                if (val) {
                    return val + '%'
                }
            }
        }
    }
</script>

<style>
    ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }
</style>
<style scoped>
    @import "../../node_modules/vuetify/dist/vuetify.min.css";
    @import "../assets/styles/pages/_CampaignData.scss";
</style>
