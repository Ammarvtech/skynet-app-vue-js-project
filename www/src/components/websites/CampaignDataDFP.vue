<template>
    <div id="campaign_data_dfp">
        <vue-progress-bar></vue-progress-bar>
        <vue-headful title="Websites DFP"/>
        <v-layout row justify-center>
            <v-dialog v-model="action_loader" hide-overlay persistent width="300">
                <v-card color="primary" dark>
                    <v-card-text>
                        Please stand by ...
                        <v-progress-linear
                                indeterminate
                                color="white"
                                class="mb-0"
                        ></v-progress-linear>
                    </v-card-text>
                </v-card>
            </v-dialog>
        </v-layout>
        <v-layout row justify-center>
            <v-dialog v-model="show_actions" max-width="1500px">
                <v-card>
                    <v-card-title class="headline">Duplicate Campaign</v-card-title>
                    <v-card-text>
                        <div id="duplicate_table">
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                    <th>
                                        <label class="form-checkbox">
                                            <input type="checkbox" v-model="selectAllDup" @click="selectDup">
                                            <i class="form-icon"></i>
                                        </label>
                                    </th>
                                    <th>Duplication_id</th>
                                    <th>Country Targeting</th>
                                    <th>Dynamic CPC</th>
                                    <th>Daily Cap</th>
                                    <th>Custom Audience</th>
                                    <th>Marketplace Audience</th>
                                    <th>OS Targeting</th>
                                    <th>Platform</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="template in this.duplicate_templates">
                                    <td>
                                        <label class="form-checkbox">
                                            <input type="checkbox" :value="template" v-model="selected_duplicates"
                                                   @click="checkboxCheck()">
                                            <i class="form-icon"></i>
                                        </label>
                                    </td>
                                    <td>{{template.medium}}</td>
                                    <td class="duplicate-column">{{template.country_targeting | _get_str('country') }}
                                    </td>
                                    <td>{{selected_campaign.br ? template.br_cpc : template.cpc}}</td>
                                    <td>{{selected_campaign.br ? template.br_daily_cap : template.daily_cap}}</td>
                                    <td class="duplicate-column">{{template.custom_audience | _get_str('audience',
                                        map_audience=mapping_dup)}}
                                    </td>
                                    <td class="duplicate-column">{{template.marketplace_audience |
                                        _get_str('marketplace', map_audience=mapping_dup) }}
                                    </td>
                                    <td>{{template.os_targeting | _get_str('os')}}</td>
                                    <td>{{template.platform_targeting | _get_str('platform') }}</td>
                                </tr>
                                </tbody>
                            </table>
                            <div class="row">
                                <div class="text-bold col-xs-1" style="width:auto">Selected:</div>
                                <div v-for="tmplt in selected_duplicates">
                                    <div class="col-xs-1 text-uppercase" style="width:auto">{{tmplt.medium}}</div>
                                </div>
                            </div>
                        </div>
                    </v-card-text>
                    <v-card-text>
                        <b>Campaign Name :</b> {{selected_campaign.name ? selected_campaign.name.toUpperCase() : ''}}
                    </v-card-text>
                    <v-card-text>
                        <b>Campaign ID :</b> {{selected_campaign.campaign_id}}
                    </v-card-text>
                    <v-card-text>
                        This campaign will be duplicated into {{selected_duplicates.length}} templates.
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-btn color="red darken-1" outline @click="show_actions = false"
                               style="margin-left: 20px;border-radius: 5px;">Cancel
                        </v-btn>

                        <v-btn v-show='selected_duplicates.length !== 0' color="green darken-1" outline
                               @click="send_action()" :disabled="false"
                               style="border-radius: 5px;">Ok
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-layout>
        <div v-show="!showMediumkey">

            <!--Campaign - Form-->
            <form @submit="submit">
                <el-row :gutter="20">
                    <el-col :span="4">
                        <websites-dropdown @selectWebsite="selectWebsite($event)"></websites-dropdown>
                    </el-col>
                    <el-col :span="4">
                        <v-select v-model="selected_device" :items="devices" label="Device"></v-select>
                    </el-col>
                    <el-col :span="4">
                        <sources-dropdown @selectSource="selectSource($event)"></sources-dropdown>
                    </el-col>
                    <el-col :xs="{offset: 0}" :sm="{offset: 0}" :md="{offset: 0}" :lg="{span: 5, offset: 1}" :xl="3"
                            style="padding-top: 8px;">
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
                    </el-col>
                    <el-col :span="1" style="padding-top: 8px;">
                        <v-btn @click="items=[]" type="submit" color="info" :disabled="loading">Submit</v-btn>
                    </el-col>
                </el-row>
            </form>

            <!--Device - Source - Tags-->
            <el-tag ref="filter_field" :class="[filterMobile ? 'filter_hide' : '']" type="success"></el-tag>
            <el-tag :class="[filter_fields_hide ? 'filter_hide' : '','fixed']" type="success" :closable="true"
                    @close="filterClose"></el-tag>

            <!--Filter-->
            <div :class="[disabled ? 'tb-hide' : '','row']">
                <search-box @selectFilter="selectFilter($event)"></search-box>
                <div class="col-xs-2">
                    <div :class="[disabled ? 'tb-hide' : '','row']">
                        <el-radio-group v-model="campaign_show">
                            <el-radio-button label="id">Campaign ID</el-radio-button>
                            <el-radio-button label="name">Campaign Name</el-radio-button>
                        </el-radio-group>
                    </div>
                </div>

                <div v-if="display_bulk_change && checked_items.length > 0" class="col-xs-2">
                    <el-popover placement="right-end" width="210" trigger="click">
                        <el-popover placement="right" width="200" trigger="click" v-model="roiAdjustView">
                            <div class="pop-div">
                                <el-input-number controls-position="right" class="edit_bid" :max="max_bulk_value"
                                                 :min="min_bulk_value" :step="0.1" size="small"
                                                 @change="selectAllRoiChange" v-model="roi_adjust"
                                                 :disabled="stop"></el-input-number>
                                <br>
                                <i @click="adjustNotice(checked_items,'roiAdjust')"
                                   :class="[stop ? 'not-active' : '', 'el-icon-circle-check link mg-l green-label']"
                                   style="margin-left:10px;"><span
                                        style="font-family:sans-serif;">&nbspAccept</span></i>
                            </div>
                            <el-button class="btn-width" type="warning" slot="reference" @click="bidAdjustView=false">
                                ROI ADJUST &nbsp <i class="fas fa-sliders-h" style="float:right;"></i>
                            </el-button>
                        </el-popover>
                        <el-button type="primary" slot="reference" :loading="bulk_adjust_loading">ACTIONS
                        </el-button>
                        <v-divider></v-divider>
                        <span style="font-weight:bold"> &nbsp&nbsp Campaigns Selected: {{this.checked_items.length}}</span>
                    </el-popover>
                </div>

                <!--Refresh Button-->
                <div class="float_right">
                    <el-tooltip placement="top">
                        <div slot="content">Refresh Campaigns Status</div>
                        <v-btn :loading="refreshLoading" @click="refreshScreen()" fab small light color="primary">
                            <v-icon dark>refresh</v-icon>
                        </v-btn>
                    </el-tooltip>
                </div>
            </div>

            <cascader ref="cascader" :class="[disabled ? 'tb-hide' : '']" style="padding-bottom: 9px;"></cascader>

            <el-row v-show="!hide">
                <el-col>
                    <el-alert v-if="last_update_arry.length > 0" v-bind:title="$title(last_update_arry[0].label)"
                              type="warning" :closable="false" show-icon
                              style="background-color:transparent !important;padding:7px 0 0 0;color:#f56c6c"></el-alert>
                </el-col>
            </el-row>

            <!--Campaigns-Websites-Table-->
            <table class="table table-striped table-hover">
                <thead>
                <tr>
                    <th v-if="display_bulk_change && items.length > 0">
                        <label class="form-checkbox">
                            <input type="checkbox" v-model="selectAllItems" @change="campaign_selected_init">
                        </label>
                    </th>
                    <th v-if="items.length > 0" v-for="(field, key) in tfields" @click="headClick(field,key, true)"
                        class="pointer th_width"
                        :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']">
                        <div v-if="field.description">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    <strong>{{field.description}}</strong><br>
                                    <strong v-if="field._description">{{field._description}}</strong>
                                </div>
                                <strong>{{field.label}}&ensp; <span
                                        class="sub_label_title">{{field.sub_label}}</span></strong>
                            </el-tooltip>
                        </div>
                        <div v-else>
                            <strong :class="[field.sub_label === 'final' ? 'th_width': '']">{{field.label}}&ensp; <span
                                    class="sub_label_title">{{field.sub_label}}</span></strong>
                        </div>
                    </th>
                </tr>
                </thead>
                <tbody>

                <!--site summary start-->
                <tr v-show="items.length > 0 && emptySummary"
                    style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                    <td v-if="display_bulk_change"></td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of devices</div>
                            <span>{{sum_device}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of sources</div>
                            <span>{{sum_source}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of sites</div>
                            <span>{{count_sites}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of campaigns</div>
                            <span>{{sum_campaigns}}</span></el-tooltip>
                    </td>
                    <td></td>
                    <td class="summary">
                        <span>N/A</span>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of clicks</div>
                            <span>{{sum_clicks}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of CTR</div>
                            <span :class="[color_summary('ctr')]">{{wavg_clicks_ctr | _format_(3)}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola Revenue: {{taboola_revenue_total | _format_(2)}}<br/>
                                Outbrain Revenue: {{outbrain_revenue_total | _format_(2)}}<br/>
                                HB Revenue: {{hb_revenue_total | _format_(2)}}<br/>
                                Adx Revenue: {{adx_revenue_total | _format_(2)}}<br/>
                                Ex Revenue: {{ex_revenue_total | _format_(2)}}<br/>
                                Adsense DFP: {{adsense_dfp_revenue_total | _format_(2)}}<br/>
                                Adsense Analytics: {{adsense_analytics_revenue_total | _format_(2)}}
                            </div>
                            <span>{{sum_revenue | _format_(0)}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Total cost</div>
                            <span>{{sum_cost | _format_(0)}}</span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Total profit</div>
                            <span>{{sum_profit | _format_(0)}}<i style="padding-left: 2px;">$</i></span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of UV</div>
                            <span>{{sum_revenue / sum_clicks | _format_(4)}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of P/S</div>
                            <span :class="[color_summary('pages_session')]" style="margin-left: 3px;">{{wavg_clicks_pages_session | _format_(2)}}</span>
                        </el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of BR</div>
                            <span>{{wavg_bounce_rate | _format_(2)}}</span></el-tooltip>
                    </td>
                    <td class="summary" style="width: 800px;">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of the current bid <br> Separated to USD and BRL</div>
                            <span v-if="!(avg_br === 0 && avg_us === 0)">{{ avg_us | _format_(4)}} <i
                                    style="padding-left: 2px;">$</i> | {{ avg_br | _format_(4)}} <i
                                    style="padding-left: 2px;">R$</i></span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of Current ROIs Doesn't <br> include BR campaigns</div>
                            <span :class="[color_summary('roi_current')]">{{wavg_clicks_roi_current * 100 | _format_(0) | prc}}</span>
                        </el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of Avg. bids</div>
                            <span>{{sum_cost / sum_clicks | _format_(4)}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Campaigns total ROI</div>
                            <span :class="[color_roi()]">{{((sum_revenue / sum_cost) * 100) | _format_(0) | prc}}</span>
                        </el-tooltip>
                    </td>
                    <td v-if="this.allow_toggle_auto === '1'" class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of campaigns with active automation rules</div>
                            <span>{{automation_campaigns}}</span></el-tooltip>
                    </td>
                    <td class="summary"></td>
                    <td v-if="enable_actions" class="summary"></td>
                </tr>
                <!--site summary end-->

                <tr v-for="(item, index) in _items" v-if="item!==undefined && item.campaign_id!=null" :ref="++index"
                    :key="item.campaign_id" :class="[item.alert === '1' ? 'tr-losing' : '']">
                    <td v-if="display_bulk_change">
                        <label>
                            <input type="checkbox" v-model="selectItem" :value="item" @change="item.index=index">
                        </label>
                    </td>
                    <td>
                        <span class="link" @click="filter_field(item.device, 'device')">{{item.device}}</span>
                    </td>
                    <td>
                        <span class="link" @click="filter_field(item.source, 'source')">{{item.source}}</span>
                    </td>
                    <td>
                        <span>{{item.acronym }}</span>
                    </td>
                    <td :class="[item.automation === '1' ? 'tdWidth' : '']">
                        <div>
                            <el-tooltip class="item" effect="dark"
                                        :content="campaign_show === 'id' ? item.name : item.campaign_id"
                                        placement="top-start">
                                <el-tooltip :disabled="!isValidId(item.campaign_id)" class="item" effect="dark"
                                            content="Campaign id contain whitespace" placement="top-start">
                                    <span class="link" @click="MediumkeyInit(item, index)">
                                        <span v-show="isValidId(item.campaign_id)" style="font-weight: bold;color:red;">!</span>
                                        <p v-if="campaign_show == 'id'">{{item.campaign_id}}
                                            <el-tooltip v-if="item.smrtbid" placement="top">
                                                <div slot="content">
                                                    <div>Smart bid strategy: The actual bid can be 50% higher.</div>
                                                </div>
                                                <i class="sb">SB</i>
                                            </el-tooltip>
                                        </p>
                                        <p v-else>{{item.name}}
                                            <el-tooltip v-if="item.smrtbid" placement="top">
                                                <div slot="content">
                                                <div>Smart bid strategy: The actual bid can be 50% higher.</div>
                                                </div>
                                                <i class="sb">SB</i>
                                            </el-tooltip>
                                        </p>

                                    </span>
                                </el-tooltip>
                            </el-tooltip>
                            <i :class="[item.mark === '1' ? 'el-icon-warning red-label' : '']"></i>
                            <div class="red-label block" v-if="item.enable === '0'">
                                <span>(disabled)</span>
                            </div>

                            <el-tooltip v-if="item.automation === '1'" placement="top">
                                <div slot="content">
                                    <div>This campaign has automation rules applied to it.</div>
                                </div>
                                <i v-if="item.automation === '1'" class="fas fa-cogs float-icon" aria-hidden="true"
                                   style="margin-top:3px;"></i>
                            </el-tooltip>


                        </div>
                    </td>
                    <td>
                        <el-tooltip v-if="item.lp.toString() !== '0'" effect="dark" :content="item.lp"
                                    placement="top-start">
                            <el-tooltip effect="dark" placement="top-start">
                                <a v-if="item.lp.toString() !== '0'" :href="item.lp" target="_blank">
                                    <i class="fas fa-external-link-alt inventory"></i>
                                </a>
                            </el-tooltip>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{item.creation_date}}</span>
                    </td>
                    <td>
                        <span>{{item.clicks}}</span>
                    </td>
                    <td>
                        <span :class="[color(item, 'ctr'), 'roi_span']">{{item.ctr | _format_(3)}}</span>
                    </td>
                    <td>
                        <div v-if="item.revenue > 0.01">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    Taboola Revenue: {{item.taboola_revenue | _format_(2)}}<br/>
                                    Outbrain Revenue: {{item.outbrain_revenue | _format_(2)}}<br/>
                                    HB Revenue: {{item.hb_revenue_dfp | _format_(2)}}<br/>
                                    Adx Revenue: {{item.adx_revenue | _format_(2)}}<br/>
                                    Ex Revenue: {{item.ex_revenue | _format_(2)}}<br/>
                                    Adsense DFP: {{item.ad_sense_revenue_dfp | _format_(2)}}<br/>
                                    Adsense Analytics: {{item.ad_sense_mobile_revenue | _format_(2)}}
                                </div>
                                <span :class="[item.prediction ? 'red-label' : '']">{{parseInt(item.revenue)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-tooltip>
                            <i v-if="mark_missing(item)" class="fa fa-exclamation red-label float-icon"
                               aria-hidden="true"></i>
                        </div>
                        <div v-else-if="item.revenue < 0.01">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    <div>No revenue to display</div>
                                </div>
                                <span :class="[item.prediction ? 'red-label' : '']">{{parseInt(item.revenue)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-tooltip>
                            <i v-if="mark_missing(item)" class="fa fa-exclamation red-label float-icon"
                               aria-hidden="true"></i>
                        </div>
                    </td>
                    <td v-if="item.source === 'taboola'" style="min-width: 90px">
                        <span>{{parseInt(item.cost)}}<i style="padding-left: 2px;">$</i> /</span>
                        <el-popover @show='budget = item.daily_cap' placement="top" width="245" trigger="click">
                            <a-input-number
                                    @keydown="onlyNumber"
                                    v-on:keyup="edit_campaign_budget_key_press($event, item)"
                                    class="budget_input bid_input"
                                    size="large"
                                    step="100"
                                    v-model="budget"
                                    :formatter="value => formatCurrency(value, item)"
                                    :parser="value => value.replace(/[R$]/g, '')"
                            />
                            <v-spacer v-if="item.br !== 0"></v-spacer>
                            <p v-if="item.br !== 0" class="campaign_roi_adjust">Campaign new cost: {{budget /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br !== 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status_tb > 90 && item.exhausted_roi === 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td v-else-if="item.source === 'gemini'" style="min-width: 90px">
                        <span>{{item.cost}}<i style="padding-left: 2px;">$</i> /</span>
                        <el-popover @show='budget = item.daily_cap' placement="top" width="245" trigger="click">
                            <a-input-number
                                    @keydown="onlyNumber"
                                    v-on:keyup="edit_campaign_budget_key_press($event, item)"
                                    class="budget_input bid_input"
                                    size="large"
                                    step="100"
                                    v-model="budget"
                                    :formatter="value => formatCurrency(value, item)"
                                    :parser="value => value.replace(/[R$]/g, '')"
                            />
                            <v-spacer v-if="item.br !== 0"></v-spacer>
                            <p v-if="item.br !== 0" class="campaign_roi_adjust">Campaign new cost: {{budget /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br !== 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi === 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td v-else-if="item.source === 'facebook' || item.source === 'zemanta' || item.source === 'outbrain'" style="min-width: 90px">
                        <span>{{item.cost}}<i style="padding-left: 2px;">$</i> /</span>
                        <el-popover @show='budget = item.daily_cap' placement="top" width="245" trigger="click">
                            <a-input-number
                                    @keydown="onlyNumber"
                                    v-on:keyup="edit_campaign_budget_key_press($event, item)"
                                    class="daily_cap_input bid_input"
                                    size="large"
                                    step="100"
                                    v-model="budget"
                                    :formatter="value => formatCurrency(value, item)"
                                    :parser="value => value.replace(/[R$]/g, '')"
                            />
                            <v-spacer v-if="item.br !== 0"></v-spacer>
                            <p v-if="item.br !== 0" class="campaign_roi_adjust">Campaign new cost: {{daily_cap /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br !== 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi === 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td v-else>
                        <span>{{item.cost}}<i style="padding-left: 2px;">$</i> / {{item.budget ? item.budget : Math.floor(item.daily_cap)}}</span>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi === 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{parseInt(item.profit)}}<i style="padding-left: 2px;">$</i></span>
                        <el-tooltip v-if="item.alert === 1" placement="top">
                            <div slot="content">
                                This campaign has a negative profit for 3 days in a row !
                            </div>
                            <i v-if="item.alert === 1" class="fas fa-angle-double-down red-label float-icon iconSt"
                               aria-hidden="true"></i>
                        </el-tooltip>

                        <el-tooltip v-if="item.profit_diff <= -30" placement="top">
                            <div slot="content">
                                <div>The profit decreased in {{item.profit_diff| _format_(0)}}% comparing to the
                                    previous period.
                                </div>
                            </div>
                            <i v-if="item.profit_diff <= -30"
                               class="fas fa-arrow-alt-circle-down float-icon red-label iconSt" aria-hidden="true"></i>
                        </el-tooltip>

                        <el-tooltip v-if="item.profit_diff >= 30" placement="top">
                            <div slot="content">
                                <div>The profit increased in {{item.profit_diff| _format_(0)}}% comparing to the
                                    previous period.
                                </div>
                            </div>
                            <i v-if="item.profit_diff >= 30"
                               class="fas fa-arrow-alt-circle-up float-icon green-label iconSt" aria-hidden="true"></i>
                        </el-tooltip>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola UV: {{item.taboola_revenue / item.clicks | _format_(4)}}<br/>
                                Outbrain UV: {{item.outbrain_revenue / item.clicks | _format_(4)}}<br/>
                                HB UV: {{item.hb_revenue_dfp / item.clicks | _format_(4)}}<br/>
                                Adx UV: {{item.adx_revenue / item.clicks | _format_(4)}}<br/>
                                Ex UV: {{item.ex_revenue / item.clicks | _format_(4)}}<br/>
                                Adsense DFP UV: {{item.ad_sense_revenue_dfp / item.clicks | _format_(4)}}<br/>
                                Adsense Analytics UV: {{item.ad_sense_mobile_revenue / item.clicks | _format_(4)}}
                            </div>
                            <span>{{item.final_uv | _format_(4)}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                    <td>
                        <span :class="[color(item, 'pages_session'), 'roi_span']">{{item.pages_session | _format_(2)}}</span>
                    </td>
                    <td>
                        <span>{{item.bounce_rate | _format_(1)}}</span>
                    </td>
                    <!--Taboola bidder-->
                    <td v-if="item.source === 'taboola'" style="min-width: 90px" @click="reset_bidder_time(item)">
                        <el-popover v-model="item.pop_visible" @show='taboola_bid = item.bid'
                                    @hide="reset_bidder_time(item)" placement="bottom" width="440"
                                    popperClass="bidder_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change bid to</span>
                                        <a-input-number
                                                @keydown="onlyNumber"
                                                v-on:keyup="edit_bid_key_press($event, item)"
                                                size="large"
                                                :min="0"
                                                :max="3"
                                                step="0.0001"
                                                v-model="taboola_bid"
                                                :formatter="value => formatCurrency(value, item)"
                                                :parser="value => value.replace(/[R$]/g, '')"
                                                class="bid_input"
                                        />
                                        <span v-if="item.br !== 0" class="curreny_convert larger_font">{{taboola_bid / brl_currency | _format_(4)}}$</span>
                                    </el-col>
                                </el-form-item>
                            </el-form>

                            <div class="text-xs-center pop_over_btns">
                                <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                           style="color: #2196f3;width: 180px;">APPLY NOW
                                </el-button>
                            </div>

                            <div v-if="enable_scheduled_bids">
                                <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">Campaign
                                    scheduled bids
                                </v-subheader>
                                <div v-for="(bidder, bindex) in item.bidders" :key="bindex">
                                    <el-form :inline="true">
                                        <el-form-item label="Change bid at">
                                            <el-col class="line" :span="12">
                                                <VueCtkDateTimePicker
                                                        class="form-group"
                                                        minute-interval="15"
                                                        v-model="bidder.execution_time"
                                                        :only-time="true"
                                                        :overlay="true"
                                                        :no-label="true"
                                                        :disabled="bidder.new === 'false'"
                                                        format='HH:mm'
                                                        formatted="HH:mm"
                                                        @validate="refresh_bidder"
                                                />
                                            </el-col>
                                        </el-form-item>
                                        <el-form-item style="margin-left: -50px">
                                            <el-col class="line">
                                                <span><strong>EDT</strong></span>
                                                <span style="padding: 0 5px 0 5px">to</span>
                                                <a-input-number
                                                        @keydown="onlyNumber"
                                                        :min="0"
                                                        :max="3"
                                                        step="0.0001"
                                                        v-model="bidder.new_bid"
                                                        :formatter="value => formatCurrency(value, item)"
                                                        :parser="value => value.replace(/[R$]/g, '')"
                                                        style="width: 115px !important"
                                                        @change="refresh_bidder"
                                                />
                                                <v-progress-circular :width="2" size="20" v-show="bidder_deleting"
                                                                     indeterminate color="#2196f3"
                                                                     style="margin-left: 5px"></v-progress-circular>
                                                <span v-show="!bidder_deleting"><i @click="remove_bidder(item, bindex)"
                                                                                   class="el-icon-delete"
                                                                                   style="font-size: large;cursor: pointer"></i></span>
                                                <el-tooltip content="Please save to apply changes" placement="right"
                                                            effect="dark">
                                                    <span v-if="bidder.new === true" class="new_label"
                                                          @mouseover="animate">new</span>
                                                </el-tooltip>
                                            </el-col>
                                        </el-form-item>
                                    </el-form>
                                    <p v-if="item.br !== 0" class="campaign_roi_adjust"
                                       style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency | _format_(4)}}
                                        $</p>
                                </div>

                                <i @click="add_bidder(item)"
                                   :class="[item.bidders && item.bidders.length === 7 ? 'tb-hide' : '','far fa-plus-square']">
                                    Schedule bid</i>

                                <div v-if="item.bidders && item.bidders.length > 0"
                                     class="text-xs-center pop_over_btns">
                                    <el-button @click="save_bidder(item)" :loading="bidder_saving" class="bidder_btn"
                                               :class="{'shake animated': animated}" plain round small
                                               style="color: #2196f3;width: 180px;">SAVE
                                    </el-button>
                                </div>
                            </div>

                            <span v-if="item.bid_currency && item.br !== 0" @mouseover="item.bid_currency = false"
                                  slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.bid_currency = true" slot="reference"
                                  class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                        </el-popover>

                        <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                            <span @click="item.pop_visible=true"
                                  v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                    class="far fa-clock pop_over_clock"></i></span>
                        </el-tooltip>

                    </td>
                    <!--Gemini bidder-->
                    <td v-else-if="item.source === 'gemini'" style="min-width: 90px" @click="reset_bidder_time(item)">
                        <el-popover v-model="item.pop_visible" @show='gemini_bid = item.bid'
                                    @hide="reset_bidder_time(item)" placement="bottom" width="440"
                                    popperClass="bidder_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change bid to</span>
                                        <a-input-number
                                                @keydown="onlyNumber"
                                                v-on:keyup="edit_bid_key_press($event, item)"
                                                size="large"
                                                :min="0"
                                                :max="3"
                                                step="0.0001"
                                                v-model="gemini_bid"
                                                :formatter="value => formatCurrency(value, item)"
                                                :parser="value => value.replace(/[R$]/g, '')"
                                                class="bid_input"
                                        />
                                        <span v-if="item.br !== 0" class="curreny_convert larger_font">{{gemini_bid | _format_(4)}}$</span>
                                    </el-col>
                                </el-form-item>
                            </el-form>

                            <div class="text-xs-center pop_over_btns">
                                <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                           style="color: #2196f3;width: 180px;">APPLY NOW
                                </el-button>
                            </div>

                            <div v-if="enable_scheduled_bids">
                                <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">Campaign
                                    scheduled bids
                                </v-subheader>
                                <div v-for="(bidder, bindex) in item.bidders" :key="bindex">
                                    <el-form :inline="true">
                                        <el-form-item label="Change bid at">
                                            <el-col class="line" :span="12">
                                                <VueCtkDateTimePicker
                                                        class="form-group"
                                                        minute-interval="15"
                                                        v-model="bidder.execution_time"
                                                        :only-time="true"
                                                        :overlay="true"
                                                        :no-label="true"
                                                        :disabled="bidder.new === 'false'"
                                                        format='HH:mm'
                                                        formatted="HH:mm"
                                                        @validate="refresh_bidder"
                                                />
                                            </el-col>
                                        </el-form-item>
                                        <el-form-item style="margin-left: -50px">
                                            <el-col class="line">
                                                <span><strong>EDT</strong></span>
                                                <span style="padding: 0 5px 0 5px">to</span>
                                                <a-input-number
                                                        @keydown="onlyNumber"
                                                        :min="0"
                                                        :max="3"
                                                        step="0.0001"
                                                        v-model="bidder.new_bid"
                                                        :formatter="value => formatCurrency(value, item)"
                                                        :parser="value => value.replace(/[R$]/g, '')"
                                                        style="width: 115px !important"
                                                        @change="refresh_bidder"
                                                />
                                                <v-progress-circular :width="2" size="20" v-show="bidder_deleting"
                                                                     indeterminate color="#2196f3"
                                                                     style="margin-left: 5px"></v-progress-circular>
                                                <span v-show="!bidder_deleting"><i @click="remove_bidder(item, bindex)"
                                                                                   class="el-icon-delete"
                                                                                   style="font-size: large;cursor: pointer"></i></span>
                                                <el-tooltip content="Please save to apply changes" placement="right"
                                                            effect="dark">
                                                    <span v-if="bidder.new === true" class="new_label"
                                                          @mouseover="animate">new</span>
                                                </el-tooltip>
                                            </el-col>
                                        </el-form-item>
                                    </el-form>
                                    <p v-if="item.br !== 0" class="campaign_roi_adjust"
                                       style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency | _format_(4)}}
                                        $</p>
                                </div>

                                <i @click="add_bidder(item)"
                                   :class="[item.bidders && item.bidders.length === 7 ? 'tb-hide' : '','far fa-plus-square']">
                                    Schedule bid</i>

                                <div v-if="item.bidders && item.bidders.length > 0"
                                     class="text-xs-center pop_over_btns">
                                    <el-button @click="save_bidder(item)" :loading="bidder_saving" class="bidder_btn"
                                               :class="{'shake animated': animated}" plain round small
                                               style="color: #2196f3;width: 180px;">SAVE
                                    </el-button>
                                </div>
                            </div>

                            <span v-if="item.bid_currency && item.br !== 0" @mouseover="item.bid_currency = false"
                                  slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.bid_currency = true" slot="reference"
                                  class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                        </el-popover>

                        <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                            <span @click="item.pop_visible=true"
                                  v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                    class="far fa-clock pop_over_clock"></i></span>
                        </el-tooltip>
                    </td>
                    <!--Facebook bidder-->
                    <td v-else-if="item.source === 'facebook'" style="min-width: 90px" @click="reset_bidder_time(item)">
                        <el-popover v-model="item.pop_visible" @show='facebook_bid = item.bid'
                                    @hide="reset_bidder_time(item)" placement="bottom" width="440"
                                    popperClass="bidder_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change bid to</span>
                                        <a-input-number
                                                @keydown="onlyNumber"
                                                v-on:keyup="edit_bid_key_press($event, item)"
                                                size="large"
                                                :min="0"
                                                :max="3"
                                                step="0.0001"
                                                v-model="facebook_bid"
                                                :formatter="value => formatCurrency(value, item)"
                                                :parser="value => value.replace(/[R$]/g, '')"
                                                class="bid_input"
                                        />
                                        <span v-if="item.br !== 0" class="curreny_convert larger_font">{{facebook_bid | _format_(4)}}$</span>
                                    </el-col>
                                </el-form-item>
                            </el-form>

                            <div class="text-xs-center pop_over_btns">
                                <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                           style="color: #2196f3;width: 180px;">APPLY NOW
                                </el-button>
                            </div>

                            <div v-if="enable_scheduled_bids">
                                <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">Campaign
                                    scheduled bids
                                </v-subheader>
                                <div v-for="(bidder, bindex) in item.bidders" :key="bindex">
                                    <el-form :inline="true">
                                        <el-form-item label="Change bid at">
                                            <el-col class="line" :span="12">
                                                <VueCtkDateTimePicker
                                                        class="form-group"
                                                        minute-interval="15"
                                                        v-model="bidder.execution_time"
                                                        :only-time="true"
                                                        :overlay="true"
                                                        :no-label="true"
                                                        :disabled="bidder.new === 'false'"
                                                        format='HH:mm'
                                                        formatted="HH:mm"
                                                        @validate="refresh_bidder"
                                                />
                                            </el-col>
                                        </el-form-item>
                                        <el-form-item style="margin-left: -50px">
                                            <el-col class="line">
                                                <span><strong>EDT</strong></span>
                                                <span style="padding: 0 5px 0 5px">to</span>
                                                <a-input-number
                                                        @keydown="onlyNumber"
                                                        :min="0"
                                                        :max="3"
                                                        step="0.0001"
                                                        v-model="bidder.new_bid"
                                                        :formatter="value => formatCurrency(value, item)"
                                                        :parser="value => value.replace(/[R$]/g, '')"
                                                        style="width: 115px !important"
                                                        @change="refresh_bidder"
                                                />
                                                <v-progress-circular :width="2" size="20" v-show="bidder_deleting"
                                                                     indeterminate color="#2196f3"
                                                                     style="margin-left: 5px"></v-progress-circular>
                                                <span v-show="!bidder_deleting"><i @click="remove_bidder(item, bindex)"
                                                                                   class="el-icon-delete"
                                                                                   style="font-size: large;cursor: pointer"></i></span>
                                                <el-tooltip content="Please save to apply changes" placement="right"
                                                            effect="dark">
                                                    <span v-if="bidder.new === true" class="new_label"
                                                          @mouseover="animate">new</span>
                                                </el-tooltip>
                                            </el-col>
                                        </el-form-item>
                                    </el-form>
                                    <p v-if="item.br !== 0" class="campaign_roi_adjust"
                                       style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency | _format_(4)}}
                                        $</p>
                                </div>

                                <i @click="add_bidder(item)"
                                   :class="[item.bidders && item.bidders.length === 7 ? 'tb-hide' : '','far fa-plus-square']">
                                    Schedule bid</i>

                                <div v-if="item.bidders && item.bidders.length > 0"
                                     class="text-xs-center pop_over_btns">
                                    <el-button @click="save_bidder(item)" :loading="bidder_saving" class="bidder_btn"
                                               :class="{'shake animated': animated}" plain round small
                                               style="color: #2196f3;width: 180px;">SAVE
                                    </el-button>
                                </div>
                            </div>

                            <span v-if="item.bid_currency && item.br !== 0" @mouseover="item.bid_currency = false"
                                  slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.bid_currency = true" slot="reference"
                                  class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                        </el-popover>

                        <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                            <span @click="item.pop_visible=true"
                                  v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                    class="far fa-clock pop_over_clock"></i></span>
                        </el-tooltip>
                    </td>
                    <!--Zemanta bidder-->
                    <td v-else-if="item.source === 'zemanta'" style="min-width: 90px" @click="reset_bidder_time(item)">
                        <el-popover v-model="item.pop_visible" @show='zemanta_bid = item.bid'
                                    @hide="reset_bidder_time(item)" placement="bottom" width="440"
                                    popperClass="bidder_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change bid to</span>
                                        <a-input-number
                                                @keydown="onlyNumber"
                                                v-on:keyup="edit_bid_key_press($event, item)"
                                                size="large"
                                                :min="0"
                                                :max="3"
                                                step="0.0001"
                                                v-model="zemanta_bid"
                                                :formatter="value => formatCurrency(value, item)"
                                                :parser="value => value.replace(/[R$]/g, '')"
                                                class="bid_input"
                                        />
                                        <span v-if="item.br !== 0" class="curreny_convert larger_font">{{zemanta_bid | _format_(4)}}$</span>
                                    </el-col>
                                </el-form-item>
                            </el-form>

                            <div class="text-xs-center pop_over_btns">
                                <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                           style="color: #2196f3;width: 180px;">APPLY NOW
                                </el-button>
                            </div>

                            <div v-if="enable_scheduled_bids">
                                <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">Campaign
                                    scheduled bids
                                </v-subheader>
                                <div v-for="(bidder, bindex) in item.bidders" :key="bindex">
                                    <el-form :inline="true">
                                        <el-form-item label="Change bid at">
                                            <el-col class="line" :span="12">
                                                <VueCtkDateTimePicker
                                                        class="form-group"
                                                        minute-interval="15"
                                                        v-model="bidder.execution_time"
                                                        :only-time="true"
                                                        :overlay="true"
                                                        :no-label="true"
                                                        :disabled="bidder.new === 'false'"
                                                        format='HH:mm'
                                                        formatted="HH:mm"
                                                        @validate="refresh_bidder"
                                                />
                                            </el-col>
                                        </el-form-item>
                                        <el-form-item style="margin-left: -50px">
                                            <el-col class="line">
                                                <span><strong>EDT</strong></span>
                                                <span style="padding: 0 5px 0 5px">to</span>
                                                <a-input-number
                                                        @keydown="onlyNumber"
                                                        :min="0"
                                                        :max="3"
                                                        step="0.0001"
                                                        v-model="bidder.new_bid"
                                                        :formatter="value => formatCurrency(value, item)"
                                                        :parser="value => value.replace(/[R$]/g, '')"
                                                        style="width: 115px !important"
                                                        @change="refresh_bidder"
                                                />
                                                <v-progress-circular :width="2" size="20" v-show="bidder_deleting"
                                                                     indeterminate color="#2196f3"
                                                                     style="margin-left: 5px"></v-progress-circular>
                                                <span v-show="!bidder_deleting"><i @click="remove_bidder(item, bindex)"
                                                                                   class="el-icon-delete"
                                                                                   style="font-size: large;cursor: pointer"></i></span>
                                                <el-tooltip content="Please save to apply changes" placement="right"
                                                            effect="dark">
                                                    <span v-if="bidder.new === true" class="new_label"
                                                          @mouseover="animate">new</span>
                                                </el-tooltip>
                                            </el-col>
                                        </el-form-item>
                                    </el-form>
                                    <p v-if="item.br !== 0" class="campaign_roi_adjust"
                                       style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency | _format_(4)}}
                                        $</p>
                                </div>

                                <i @click="add_bidder(item)"
                                   :class="[item.bidders && item.bidders.length === 7 ? 'tb-hide' : '','far fa-plus-square']">
                                    Schedule bid</i>

                                <div v-if="item.bidders && item.bidders.length > 0"
                                     class="text-xs-center pop_over_btns">
                                    <el-button @click="save_bidder(item)" :loading="bidder_saving" class="bidder_btn"
                                               :class="{'shake animated': animated}" plain round small
                                               style="color: #2196f3;width: 180px;">SAVE
                                    </el-button>
                                </div>
                            </div>

                            <span v-if="item.bid_currency && item.br !== 0" @mouseover="item.bid_currency = false"
                                  slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.bid_currency = true" slot="reference"
                                  class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                        </el-popover>

                        <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                            <span @click="item.pop_visible=true"
                                  v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                    class="far fa-clock pop_over_clock"></i></span>
                        </el-tooltip>
                    </td>
                    <!--Outbrain bidder-->
                    <td v-else-if="item.source === 'outbrain'" style="min-width: 90px" @click="reset_bidder_time(item)">
                        <el-popover v-model="item.pop_visible" @show='outbrain_bid = item.bid'
                                    @hide="reset_bidder_time(item)" placement="bottom" width="440"
                                    popperClass="bidder_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change bid to</span>
                                        <a-input-number
                                                @keydown="onlyNumber"
                                                v-on:keyup="edit_bid_key_press($event, item)"
                                                size="large"
                                                :min="0"
                                                :max="3"
                                                step="0.0001"
                                                v-model="outbrain_bid"
                                                :formatter="value => formatCurrency(value, item)"
                                                :parser="value => value.replace(/[R$]/g, '')"
                                                class="bid_input"
                                        />
                                        <span v-if="item.br !== 0" class="curreny_convert larger_font">{{outbrain_bid | _format_(4)}}$</span>
                                    </el-col>
                                </el-form-item>
                            </el-form>

                            <div class="text-xs-center pop_over_btns">
                                <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                           style="color: #2196f3;width: 180px;">APPLY NOW
                                </el-button>
                            </div>

                            <div v-if="enable_scheduled_bids">
                                <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">Campaign
                                    scheduled bids
                                </v-subheader>
                                <div v-for="(bidder, bindex) in item.bidders" :key="bindex">
                                    <el-form :inline="true">
                                        <el-form-item label="Change bid at">
                                            <el-col class="line" :span="12">
                                                <VueCtkDateTimePicker
                                                        class="form-group"
                                                        minute-interval="15"
                                                        v-model="bidder.execution_time"
                                                        :only-time="true"
                                                        :overlay="true"
                                                        :no-label="true"
                                                        :disabled="bidder.new === 'false'"
                                                        format='HH:mm'
                                                        formatted="HH:mm"
                                                        @validate="refresh_bidder"
                                                />
                                            </el-col>
                                        </el-form-item>
                                        <el-form-item style="margin-left: -50px">
                                            <el-col class="line">
                                                <span><strong>EDT</strong></span>
                                                <span style="padding: 0 5px 0 5px">to</span>
                                                <a-input-number
                                                        @keydown="onlyNumber"
                                                        :min="0"
                                                        :max="3"
                                                        step="0.0001"
                                                        v-model="bidder.new_bid"
                                                        :formatter="value => formatCurrency(value, item)"
                                                        :parser="value => value.replace(/[R$]/g, '')"
                                                        style="width: 115px !important"
                                                        @change="refresh_bidder"
                                                />
                                                <v-progress-circular :width="2" size="20" v-show="bidder_deleting"
                                                                     indeterminate color="#2196f3"
                                                                     style="margin-left: 5px"></v-progress-circular>
                                                <span v-show="!bidder_deleting"><i @click="remove_bidder(item, bindex)"
                                                                                   class="el-icon-delete"
                                                                                   style="font-size: large;cursor: pointer"></i></span>
                                                <el-tooltip content="Please save to apply changes" placement="right"
                                                            effect="dark">
                                                    <span v-if="bidder.new === true" class="new_label"
                                                          @mouseover="animate">new</span>
                                                </el-tooltip>
                                            </el-col>
                                        </el-form-item>
                                    </el-form>
                                    <p v-if="item.br !== 0" class="campaign_roi_adjust"
                                       style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency | _format_(4)}}
                                        $</p>
                                </div>

                                <i @click="add_bidder(item)"
                                   :class="[item.bidders && item.bidders.length === 7 ? 'tb-hide' : '','far fa-plus-square']">
                                    Schedule bid</i>

                                <div v-if="item.bidders && item.bidders.length > 0"
                                     class="text-xs-center pop_over_btns">
                                    <el-button @click="save_bidder(item)" :loading="bidder_saving" class="bidder_btn"
                                               :class="{'shake animated': animated}" plain round small
                                               style="color: #2196f3;width: 180px;">SAVE
                                    </el-button>
                                </div>
                            </div>

                            <span v-if="item.bid_currency && item.br !== 0" @mouseover="item.bid_currency = false"
                                  slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br !== 0" @mouseleave="item.bid_currency = true" slot="reference"
                                  class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br === 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                    style="padding-left: 2px;">$</i></span>
                        </el-popover>

                        <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                            <span @click="item.pop_visible=true"
                                  v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                    class="far fa-clock pop_over_clock"></i></span>
                        </el-tooltip>
                    </td>
                    <td v-else-if="item.source === 'custom'" style="min-width: 90px">
                        <span slot="reference" class="link">{{item.bid }}<i style="padding-left: 2px;">$</i></span>
                    </td>

                    <td v-else>
                        {{item.bid | _format_(4)}}$
                    </td>
                    <!--Current ROI-->
                    <td>
                        <el-popover v-if="item.roi_current" @show='roi = parseInt(item.roi_current * 100)'
                                    placement="top" width="220" trigger="click">
                            <a-input-number
                                    @keydown="onlyNumber"
                                    v-on:keyup="edit_campaign_roi_key_press($event, item)"
                                    size="large"
                                    :min="100"
                                    :max="200"
                                    step="10"
                                    v-model="roi"
                                    :formatter="value => formatPrc(value)"
                                    class="bid_input"
                                    style="margin-left: 33px;"
                            />
                            <v-spacer></v-spacer>
                            <p class="campaign_roi_adjust">Campaign new bid: {{(item.final_uv / (roi / 100)) |
                                _format_(4)}}</p>
                            <span slot="reference" :class="[color(item, 'roi', item.roi_current), 'link-roi roi_span']">{{item.roi_current | format_prc}}%</span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_roi(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <div v-else-if="item.roi_current_rt">
                            <span :class="[color(item, 'roi', item.roi_current_rt), 'roi_span']">{{item.roi_current_rt | format_prc}}%</span>
                        </div>
                    </td>
                    <td>
                        <span>{{item.avg_bid | _format_(5) }}<i style="padding-left: 2px;">$</i></span>
                    </td>
                    <td style="width: 1px">
                        <span v-if="item.roi_final" :class="[color(item, 'roi', item.roi_final), 'roi_span']">{{item.roi_final | format_prc}}%</span>
                    </td>
                    <td v-if="toggle_auto_providers.indexOf(item.source) > -1 && allow_toggle_auto === '1'">
                        <el-switch
                                v-model="item.automation_active"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                @change="change_automation(item)"
                                :active-value="1"
                                :inactive-value="0">
                        </el-switch>
                    </td>
                    <td v-else-if="allow_toggle_auto === '1'"></td>
                    <td v-if="enable_actions && item.source === 'taboola' ">
                        <el-tooltip placement="top">
                            <div slot="content">Duplicate</div>
                            <span><i class="fw-icon fa-copy" :class="[action_class ? 'dp_block' : 'dp_allow']" title
                                     @click="get_duplicate_templates(item)"></i></span>
                        </el-tooltip>
                    </td>
                    <td v-else></td>
                    <td style="min-width: 50px">
                        <div v-if="item.status === 'IN_PROCESS' || item.status === 'PENDING'"
                             class="hourglass mleft"></div>
                        <div v-if="item.status === 'ERROR'" class="el-icon-warning red-label mleft"></div>
                        <div v-if="item.status === 'DONE'">
                            <i class="fa fa-check-square green-label mleft"></i>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>

            <el-row v-show="items.length > 0" :class="[hide ? 'tb-hide' : '','']" type="flex">
                <el-col>
                    <el-tooltip class="item" effect="dark" content="Per Page" placement="top-start"
                                style="height: 31px">
                        <el-input-number size="small" v-model="perPage" controls-position="right" :min="5"
                                         :step="5"></el-input-number>
                    </el-tooltip>
                    <el-tooltip class="item" effect="dark" content="Minimum Clicks" placement="top-start"
                                style="visibility: hidden">
                        <el-input-number size="small" v-model="minClicks" controls-position="right" :min="0"
                                         :step="100"></el-input-number>
                    </el-tooltip>
                    <div class="col-md-11 text-center" style="top: -53px">
                        <b-pagination size="md" :total-rows="items.length" :per-page="perPage" v-model="currentPage"/>
                    </div>
                    <div class="col-md-1" style="top: -40px">
                        <download-excel style="" class="excel v-btn theme--light info" name="websites_dfp.xls"
                                        :fields="json_fields" :data="filter_summary()">Export excel<i
                                style="padding-left:10px;padding-bottom: 3px;" class="far fa-file-excel"></i>
                        </download-excel>
                    </div>
                </el-col>
            </el-row>
            <div class="_centered" v-loading="loading" style="width: 100%"></div>
        </div>

        <!-- Medium-Keyword-Page -->
        <medium_key ref="mediumKeyword" v-show="showMediumkey" @logout="logout"></medium_key>
        <vue-snotify></vue-snotify>
    </div>
</template>

<script>
    import moment from 'moment-timezone';
    import changeBid from "../mixins/changeBid";
    import changeAutomation from "../mixins/changeAutomation";
    import bulkCampaigns from "../mixins/bulkCampaigns";
    import bidders from "../mixins/bidders";
    import alerts from "../mixins/alerts";

    export default {
        name: 'campaign_data_dfp',
        components: {
            "medium_key": require("./MediumKey.vue").default,
            "cascader": require("../Cascader.vue").default,
        },
        mixins: [
            changeBid,
            changeAutomation,
            bulkCampaigns,
            bidders,
            alerts
        ],
        mounted() {
            this.$emit('validateUser');
            this.brl_currency = this.$store.getters.getCurrency;
            if (localStorage.campaign_show) {
                this.campaign_show = localStorage.campaign_show;
            } else {
                this.campaign_show = 'id';
            }
        },
        data() {
            return {
                json_fields: {
                    'Site id': 'site_id',
                    'Campaign ID': 'campaign_id',
                    'Source': 'source',
                    'Device': 'device',
                    'Name': 'name',
                    'Creation date': 'creation_date',
                    'Clicks': 'clicks',
                    'CTR': 'ctr',
                    'Revenue': 'revenue',
                    'Cost': 'cost',
                    'Daily Cap (Taboola)': 'daily_cap',
                    'Budget': 'budget',
                    'Profit': 'profit',
                    'Final UV': 'final_uv',
                    'Pages Session': 'pages_session',
                    'Bounce rate': 'bounce_rate',
                    'BID': 'bid',
                    'Roi Current': 'roi_current',
                    'Avg Bid': 'avg_bid',
                    'Roi Final': 'roi_final'
                },
                items: [],
                items_copy: [],
                selected_duplicates: [],
                selectAllDup: false,
                campaign_source: [],
                websites: [],
                summary: [],
                colors: [],
                last_update: [],
                last_update_arry: [],
                duplicate_templates: [],
                mapping_dup: [],
                response_tmp: [],
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                date_range: [
                    moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD")
                ],
                tfields: {
                    device: {label: 'Device'},
                    source: {label: 'Source'},
                    name: {label: 'Site', sortable: false},
                    campaign_id: {label: 'Campaign', sortable: true},
                    landing_page: {label: 'LP', sortable: false, description: 'Landing page'},
                    creation_date: {label: 'CD', sortable: true, description: 'Creation date'},
                    clicks: {label: 'Clicks', sortable: true, description: 'Reported by the traffic source'},
                    ctr: {label: 'Ctr', sortable: true, description: 'Reported by the traffic sources'},
                    revenue: {label: 'Revenue', sortable: true, description: 'Accumulated from all revenue sources'},
                    cost: {
                        label: 'C / B',
                        sortable: true,
                        description: 'Cost and Budget',
                        _description: 'Reported by the traffic source'
                    },
                    profit: {label: 'Profit', sortable: true, description: '= Revenue - Cost'},
                    final_uv: {label: 'UV', sortable: true, description: '= Revenue / Clicks'},
                    pages_session: {
                        label: 'P/S',
                        sortable: true,
                        description: 'Pages per Session',
                        _description: 'Reported by Google Analytics'
                    },
                    bounce_rate: {
                        label: 'BR',
                        sortable: true,
                        description: 'Bounce Rate',
                        _description: 'The drop % between p1 and p2'
                    },
                    bid: {
                        label: 'Bid',
                        sortable: true,
                        description: 'Reported by the traffic sources',
                        sub_label: 'Current'
                    },
                    roi_current: {
                        label: 'ROI',
                        sortable: true,
                        description: '= Campaign UV / Mediums Avg Bid',
                        sub_label: 'Current'
                    },
                    avg_bid: {label: 'Avg bid', sortable: true, description: 'Reported by the traffic sources'},
                    roi_final: {label: 'ROI', sortable: true, description: '= UV / Avg.Bid'},
                    automation_active: {label: 'Auto', sortable: true, description: 'Enable/disable automation rules'},
                },
                limit_date: moment.utc().startOf('day').format("YYYY-MM-DD"),
                sources: ['facebook', 'taboola', 'gemini', 'outbrain', 'revcontent', 'custom'],
                site_count: new Set(),
                inited_summary: {},
                selected_campaign: {},
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
                allow_toggle_auto: 0,
                filterMobile: true,
                filter_fields_hide: true,
                sortDesc: true,
                disabled: true,
                hide: true,
                dateMenu: false,
                emptySummary: true,
                sortFlag: false,
                loading: false,
                showMediumkey: false,
                animated: false,
                enable_scheduled_bids: false,
                action_class: false,
                action_loader: false,
                enable_actions: false,
                refreshLoading: false,
                show_actions: false,
                sort: null,
                filter: null,
                edit_index: null,
                selected_campaign_source: "All",
                selected_device: "All",
                site_id: "All",
                shown_item: '',
                minClicks: 0,
                automation_campaigns: 0,
                budget: 0,
                roi: 0,
                step: 0.001,
                currentPage: 1,
                perPage: 20,
                brl_currency: 1,
                sum_device: undefined,
                sum_source: undefined,
                sum_campaigns: undefined,
                sum_clicks: undefined,
                count_sites: undefined,
                wavg_clicks_ctr: undefined,
                wavg_clicks_pages_session: undefined,
                wavg_bounce_rate: undefined,
                wavg_clicks_roi_current: undefined,
                sum_revenue: undefined,
                sum_cost: undefined,
                sum_profit: undefined,
                taboola_revenue_total: undefined,
                outbrain_revenue_total: undefined,
                adx_revenue_total: undefined,
                hb_revenue_total: undefined,
                adsense_dfp_revenue_total: undefined,
                adsense_analytics_revenue_total: undefined,
                ex_revenue_total: undefined,
                avg_us: undefined,
                avg_br: undefined,
                campaign_show: '',
            }
        },
        methods: {
            logout() {
                this.$emit('logout');
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
            selectSource(source) {
                this.selected_campaign_source = source;
            },
            selectFilter(filter) {
                this.filter = filter;
                this.checked_items = [];
            },
            submit: function () {
                this.items = [];
                this.checked_items = [];
                this.duplicate_templates = [];
                this.action_loader = false;
                this.$Progress.start();
                let site_id = this.site_id == 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
                let device = (this.selected_device ? this.selected_device : 'all').toLocaleLowerCase();
                let source = (this.selected_campaign_source ? this.selected_campaign_source : 'all').toLocaleLowerCase();
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");
                let restrict = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.restricted_campaigns ? this.$store.getters.getUser.settings.restricted_campaigns : '0';

                this.allow_toggle_auto = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.toggle_automation ? this.$store.getters.getUser.settings.toggle_automation : '0';
                if (this.allow_toggle_auto !== '1') {
                    delete this.tfields.automation_active;

                }
                this.loading = true;
                this.disabled = true;
                this.hide = true;
                this.inited_summary = {};
                this.site_count = new Set();
                this.items = [];
                this.last_update_arry = [];
                this.brl_currency = this.$store.getters.getCurrency;
                this.enable_scheduled_bids = this.$store.getters.getUser.settings.scheduled_bids === "1";
                this.enable_actions = this.$store.getters.getUser.settings.actions === "1";

                let params = {
                    'site_id': site_id,
                    'device': device,
                    'source': source,
                    'start': start,
                    'end': end,
                    'restrict': restrict,
                    'login_time': this.$store.getters.getUser.loginTime,
                };

                setTimeout(() => {
                    this.get_colors(params);
                    this.get_last_update(params);
                }, 1);

                this.$http.get('/api/website/user_campaigns_dfp', {params: params}).then(res => {
                    if (res.body && res.body['data']) {
                        this.items = JSON.parse(JSON.parse(JSON.stringify(res.body['data'])));
                        this.items_copy = this.items;
                        if (this.items) {
                            this.init_bidders();
                        }
                        if (this.$refs.cascader.reapply) {
                            this.$refs.cascader.reapply();
                        }
                        if (this.items.length === 0) {
                            this.filterClose();
                        } else {
                            this.hide = false;
                            this.disabled = false;
                            this.headClick(this.tfields.cost, "cost");
                            this.sortDesc = false;
                            this.mediumKeyword_items = this.items;
                            setTimeout(() => {
                                this.notify_losing();
                            }, 1000);
                        }
                        this.loading = false;
                        this.refreshLoading = false;
                        this.$Progress.finish();

                    } else {
                        this.filterClose();
                        this.refreshLoading = false;
                        this.loading = false;
                        this.$Progress.fail();
                        this.notice("Error has occurred, Please try again");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    this.refreshLoading = false;
                    this.loading = false;
                    this.$Progress.fail();
                    this.notice("Error has occurred, Please try again");
                });
            },
            selectDup() {
                this.selected_duplicates = [];
                if (!this.selectAllDup) {
                    for (let i in this.duplicate_templates) {
                        this.selected_duplicates.push(this.duplicate_templates[i]);
                    }
                }
            },
            checkboxCheck() {
                console.log('dup selected: ' + this.selected_duplicates.length + 'selectedalldup: ' + this.selectAllDup);
                if (this.selectAllDup === true && this.selected_duplicates.length === this.duplicate_templates.length) {
                    this.selectAllDup = false;
                }
            },
            send_action() {
                this.action_loader = true;
                let item = this.selected_campaign;
                this.show_actions = false;
                item.pop_visible = false;
                item.status = 'IN_PROCESS';
                let dlr_post = (dst_payload) => {
                    return new Promise((resolve, reject) => {
                        this.$http.post("/api/website/taboola/campaign/duplicate", {
                            dst_payload: dst_payload,
                            login_time: this.$store.getters.getUser.loginTime,
                        }).then(res => {
                            if (res.body === "True") {
                                this.$message({message: 'Request Pending...', center: true, type: 'success'});
                                resolve('ok');
                            } else {
                                this.notice("Error has occurred, Please try again");
                                reject('bad');
                            }
                        }).catch(e => {
                            reject('bad');
                            if (e.status === 401) {
                                this.$emit('logout');
                            }
                            else {
                                this.notice("Error has occurred, Please try again");
                            }
                        })
                    })
                };
                let payloads = [];
                for (let index in this.selected_duplicates) {
                    const template = _.cloneDeep(this.selected_duplicates[index]);
                    const payload = _.cloneDeep(item);
                    payload['dst_params'] = template;
                    if (this.selected_campaign.br) {
                        payload['dst_params']['cpc'] = payload['dst_params']['br_cpc'];
                        payload['dst_params']['daily_cap'] = payload['dst_params']['br_daily_cap'];
                    }
                    delete payload['dst_params']['br_cpc'];
                    delete payload['dst_params']['br_daily_cap'];
                    payloads.push(payload);
                }
                Promise.all(payloads.map(dlr_post)).then(result => {
                    console.log(result);
                    this.action_loader = false;
                }).catch(error => {
                    console.log(error);
                    this.action_loader = false;
                });

                this.refresh_campaign_status(item);
            },
            get_duplicate_templates(item) {
                if (!item) {
                    return;
                }
                if (this.duplicate_templates.length > 0) {
                    this.selected_duplicates = this.duplicate_templates;
                    this.selectAllDup = true;
                    this.action_class = false;
                    this.selected_campaign = item;
                    this.show_actions = true;
                    return;
                }

                this.action_loader = true;
                this.action_class = true;

                this.$http.get('/api/website/audience_mapping', {
                    params: {
                        site_id: item.site_id,
                        source: item.source
                    }
                }).then(res => {
                    if (res.body) {
                        this.mapping_dup = res.body['res'];
                    }
                });
                let params = {
                    site_id: item.site_id,
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.get('/api/website/campaign/duplicate_templates', {params: params}).then(res => {
                    if (res.body['res']) {
                        this.response_tmp = res.body['res'];
                        if (this.response_tmp) {
                            this.load_templates(item);
                        }
                    }
                    this.action_loader = false;
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                });
            },
            load_templates(item) {
                this.response_tmp.forEach(t => t['medium'] = 'dup: ' + t['duplicate_id']);

                if (this.response_tmp) {
                    this.duplicate_templates = this.response_tmp;
                    this.selected_duplicates = this.duplicate_templates;
                    this.selectAllDup = true;
                    this.action_class = false;
                    this.selected_campaign = item;
                    this.show_actions = true;
                    return true;
                }
            }
            ,
            MediumkeyInit: function (item, index) {
                this.$refs.mediumKeyword.initializeView(
                    item,
                    this.mediumKeyword_items,
                    this.websites,
                    this.site_id,
                    this.date_range[0],
                    this.date_range[1],
                    this.selected_campaign_source,
                    this.selected_device
                );
                this.showMediumkey = true;
                this.shown_item = index;
            },
            edit_campaign_budget(item) {
                if (this.budget.toString() === item.daily_cap.toString()) {
                    this.notice("You have entered the same value, No changes are made");
                    return;
                }
                item.status = 'IN_PROCESS';
                item.new_budget = this.budget;
                item.login_time = this.$store.getters.getUser.loginTime;

                this.$http.post("api/website/" + item.source + "/campaign/update_budget", item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...', center: true, type: 'success'});
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                this.refresh_campaign_status(item);
            },
            edit_campaign_budget_key_press(e, item) {
                if (e.keyCode === 13) {
                    this.edit_campaign_budget(item);
                }
            },
            edit_campaign_roi(item) {
              item.new_campaign_bid = item.final_uv / (this.roi / 100);
              if (this.roi.toString() === item.roi_current.toString()) {
                  this.notice("You have entered the same value, No changes are made");
                  return;
              }else if (parseFloat(item.new_campaign_bid) === 0) {
                this.notice("Please enter value greater then 0");
                return;
              }else if (item.source !== 'facebook' && parseInt(item.br) === 0 && parseFloat(item.new_campaign_bid) > 0.25 ) {
                this.notice("Please enter value less then 0.25$");
                return;
              }else if (item.source !== 'facebook' && parseInt(item.br) === 1 && parseFloat(item.new_campaign_bid / this.brl_currency) > 0.25) {
                this.notice("Please enter value less then 0.25$");
                return;
              }
                item.status = 'IN_PROCESS';
                item.new_campaign_bid = Math.round(item.new_campaign_bid * 10000) / 10000; // Round 4 digits after decimal point
                item.new_roi = this.roi / 100;
                item.login_time = this.$store.getters.getUser.loginTime;

                this.$http.post("api/website/campaign/roi_adjust", item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...', center: true, type: 'success'});
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                this.refresh_campaign_status(item);
            },
            edit_campaign_roi_key_press(e, item) {
                if (e.keyCode === 13) {
                    this.edit_campaign_roi(item);
                }
            },
            get_last_update(params) {
                if (params.end !== moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD")) {
                    return;
                }
                this.$http.get('/api/website/last_update', {params: params}).then(res => {
                    if (res.body) {
                        this.last_update = Object.keys(res.body).map(key => res.body[key]);
                        if (this.last_update.length > 0) {
                            this.build_title();
                        }
                    }
                });
            },
            check_status_campaign(item) {
                if (!item) {
                    return
                }
                let site_id = this.site_id === 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
                let device = (this.selected_device ? this.selected_device : 'all').toLocaleLowerCase();
                let source = (this.selected_campaign_source ? this.selected_campaign_source : 'all').toLocaleLowerCase();
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");
                let restrict = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.restrict ? this.$store.getters.getUser.settings.restrict : '0';

                let params = {
                    'site_id': site_id,
                    'device': device,
                    'source': source,
                    'start': start,
                    'end': end,
                    'restrict': restrict,
                    'login_time': this.$store.getters.getUser.loginTime,
                };

                this.$http.get('/api/website/user_campaigns_dfp', {params: params}).then(res => {
                    if (res.body) {
                        this.items = JSON.parse(JSON.parse(JSON.stringify(res.body['data'])));
                        this.items_copy = this.items;
                        this.timer = undefined;
                        if (this.items) {
                            this.init_bidders();
                        }
                        if (this.$refs.cascader.reapply) {
                            this.$refs.cascader.reapply();
                        }
                    } else {
                        console.log("REFRESH ERROR");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    this.refreshLoading = false;
                    this.loading = false;
                    this.$Progress.fail();
                    this.notice("Error has occurred, Please try again");
                });
            },
            notify_losing() {
                const that = this;
                const id = this.site_id || this.site_id.website_id;
                if (id !== 'All' && this.losing_campaigns_count > 0 && this.$cookies.get('losing_campaign') !== this.site_id.website_id) {
                    this.$snotify.warning('', this.site_id.website_name + ' has ' + this.losing_campaigns_count + ' campaigns that lost 3 days in a row.', {
                        pauseOnHover: true,
                        showProgressBar: true,
                        preventDuplicates: true,
                        titleMaxLength: 500,
                        timeout: 5000,
                        closeOnClick: true,
                        position: 'rightTop',
                        buttons: [
                            {
                                text: 'Show campaigns', action: (toast) => {
                                    this.$refs.cascader.instant_filter(true);
                                    this.$snotify.remove(toast.id);
                                }, bold: true
                            },
                            {
                                text: 'Remind me later', action: (toast) => {
                                    this.$snotify.remove(toast.id);
                                    that.$cookies.set("losing_campaign", id, 3600);
                                }, bold: true
                            },
                        ]
                    });
                }
            },
            filter_summary() {
                let items = this.items;
                const fix = v => {
                    if (v instanceof Object) {
                        return ['name', 'campaign_id', 'device', 'source'].map(k => fix(v[k])).join(' ');
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
            cascaderFilter(query, scope, remove, remove_all, current_filters = []) {
                if (remove_all) {
                    scope.$data.items = scope.$data.items_copy;
                    scope.$data.hide = scope.$data.items.length <= 0;
                    return;
                }

                let actions = ['losing', 'landing', 'exceeded', 'creation', 'bidder'];

                if (remove || (current_filters && !query && !remove && !remove_all)) {

                    if (remove && scope.$refs.cascader.labels.indexOf(remove.label) > -1) {
                        scope.$refs.cascader.labels = [];
                    }

                    if (current_filters.length === 0) {
                        scope.$data.items = scope.$data.items_copy;
                        return;
                    }

                    let filtered_items = scope.$data.items_copy;
                    for (let i of current_filters) {
                        if (i.type === 'enabled') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field === 'automation_active') {
                                    return o[i.field] == 1;
                                }
                                return o[i.field] == 1;
                            });
                        } else if (i.type === 'disabled') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field === 'automation_active') {
                                    return o[i.field] == 0;
                                }
                                return o[i.field] == 0;
                            });
                        } else if (i.type === 'less') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field === 'budget' && o.source === 'taboola') {
                                    return o['daily_cap'] < i.amount;
                                }
                                return o[i.field] < i.amount;
                            });
                        } else if (i.type === 'greater') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field === 'budget' && o.source === 'taboola') {
                                    return o['daily_cap'] > i.amount;
                                }
                                return o[i.field] > i.amount;
                            });
                        } else if (i.type === 'between') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field === 'budget' && o.source === 'taboola') {
                                    return parseFloat(o['daily_cap']) > parseFloat(i.amount) && parseFloat(o['daily_cap']) < parseFloat(i.between);
                                }
                                return o[i.field] > i.amount && o[i.field] < i.between;
                            });
                        } else if (i.type === 'losing') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] === 1;
                            });
                        } else {
                            filtered_items = this.cascaderFilterExtend(i, filtered_items);
                        }
                    }

                    scope.$data.items = filtered_items;
                    scope.$data.hide = filtered_items.length <= 0;
                }

                else if (!remove && !remove_all && !actions.includes(query.type)) {

                    if (query.type === 'enabled') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field === 'automation_active') {
                                return o['automation_active'] == 1;
                            }
                        });
                    } else if (query.type === 'disabled') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field === 'automation_active') {
                                return o['automation_active'] == 0;
                            }
                        });
                    }

                    query.amount = parseFloat(query.amount);

                    if (query.type === 'less') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field === 'budget' && o.source === 'taboola') {
                                return o['daily_cap'] < query.amount;
                            }
                            return o[query.field] < query.amount;
                        });
                    } else if (query.type === 'greater') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field === 'budget' && o.source === 'taboola') {
                                return o['daily_cap'] > query.amount;
                            }
                            return o[query.field] > query.amount;
                        });
                    } else if (query.type === 'equals') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            return o[query.field] > query.amount - 0.01 && o[query.field] < query.amount + 0.01;
                        });
                    } else if (query.type === 'between') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field === 'budget' && o.source === 'taboola') {
                                return parseFloat(o['daily_cap']) > parseFloat(query.amount) && parseFloat(o['daily_cap']) < parseFloat(query.between);
                            }
                            return o[query.field] > query.amount && o[query.field] < query.between;
                        });
                    }
                }

                else if (query) {
                    scope.$data.items = this.cascaderFilterExtend(query, scope.$data.items);
                }

                if (current_filters.length > 0 && !query && scope.$data.items.length === 0 && !remove && !remove_all) {
                    scope.$data.disabled = false;
                }

                scope.$data.checked_items = [];
            },
            cascaderFilterExtend(query, items) {

                if (query.type === 'creation') {
                    return _.filter(items, function (o) {
                        return Date.parse(o[query.field]) >= Date.parse(query.value[0]) && Date.parse(o[query.field]) <= Date.parse(query.value[1]);
                    });
                }
                else if (query.type === 'landing') {
                    return this.regex_filter(query.value, items)
                }
                else if (query.type === 'losing') {
                    return _.filter(items, function (o) {
                        return o[query.field] === 1;
                    });
                }
                else if (query.type === 'exceeded') {
                    return _.filter(items, function (o) {
                        return (o[query.field] > 90 || o[query.field + "_tb"] > 90) && o['exhausted_roi'] === 1;
                    });
                }
                else if (query.type === 'bidder') {
                    return _.filter(items, function (o) {
                        return o[query.field] && o[query.field].length > 0;
                    });
                }
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
            color_summary(key) {
                if (this.inited_summary[key] !== undefined) {
                    if (key === 'ctr') {
                        if (this.inited_summary[key] <= 0.8 && this.inited_summary[key] >= 0.5) {
                            return 's_warning'
                        } else if (this.inited_summary[key] > 0.8) {
                            return 's_success'
                        } else if (this.inited_summary[key] < 0.5) {
                            return 's_danger'
                        }
                    } else if (key === 'pages_session') {
                        if (this.inited_summary[key] <= 16 && this.inited_summary[key] >= 10) {
                            return 's_warning'
                        } else if (this.inited_summary[key] > 16) {
                            return 's_success'
                        } else if (this.inited_summary[key] < 10) {
                            return 's_danger'
                        }
                    } else if (key === 'roi_current' && this.inited_summary[key]) {
                        let res = this.inited_summary[key] * 100;
                        if (parseInt(res) <= 129) {
                            return 's_danger'
                        } else if (parseInt(res) >= 129 && parseInt(res) <= 149) {
                            return 's_warning'
                        } else if (parseInt(res) >= 150) {
                            return 's_success'
                        }
                    }
                }
            },
            _sum(key, data) {
                let res = parseFloat(_.sumBy([key], _.partial(_.sumBy, data)));
                if (res !== undefined) {
                    this.inited_summary[key] = res;
                    return res;
                }
            },
            _wavg(w, v, taboola_only) {
                let data = this.filter_summary();

                if (taboola_only) {
                    data = data.filter(function (el) {
                        return el.source === 'taboola';
                    });
                }
                data = data.filter(function (el) {
                    return el.bid > 0;
                });

                let res = ((_w, _v) => _v / _w)(...data.reduce((r, o) => [r[0] + o[w], r[1] + o[w] * o[v]], [0, 0]));
                if (res !== undefined) {
                    this.inited_summary[v] = res;
                    return res;
                }
            },
            _avg(currency) {
                if (typeof(currency) == "object") return;
                if (this.items) {
                    let currency_items = [];
                    if (currency === 'br') {
                        currency_items = this.filter_summary().filter(function (el) {
                            return el.br !== 0 && el.bid > 0;
                        });

                    } else {
                        currency_items = this.filter_summary().filter(function (el) {
                            return el.br === 0 && el.bid > 0;
                        });
                    }

                    if (currency_items.length === 0) {
                        return 0
                    }

                    let res = ((_w, _v) => _v / _w)(...currency_items.reduce((r, o) => [r[0] + o['clicks'], r[1] + o['clicks'] * (o['bid'])], [0, 0]));
                    this.inited_summary[currency] = isNaN(res) ? 'N/A' : res;
                    return res;
                }
            },
            _count_sites() {
                if (this.site_id !== 'All') {
                    return 1;
                }

                this.site_count.clear();
                let _filter = this.filter === '' || this.filter == null;
                let items = !_filter ? this.filter_summary() : this.items;
                let acr = '';
                for (let i of items) {
                    acr = i.name.split('-');
                    let _acr = acr[0].toLowerCase().replace(/ /g, "") !== 'msnsafe' ? acr[0].trim() : this.site_count.add(acr[1].trim());
                    if (!this.sources.includes(_acr) && !this.site_count.has(_acr) && _acr.length <= 3 && _acr !== 'msn') {
                        this.site_count.add(_acr);
                    }
                }
                return this.site_count.size;
            },
            build_title() {
                let sites;
                let time = moment(new Date(Date.now())).format("YYYY-MM-DD");
                let endTime = moment(time + ' ' + '03:00');

                if (this.last_update.length === 1) {
                    if (moment(this.last_update[0].last_update).isBefore(endTime)) {
                        sites = '(last update: ' + moment(this.last_update[0].last_update).format('h:mm a') + ' est)';
                    }
                } else if (this.last_update.length > 1) {
                    sites = 'for the following sites: ';
                    for (let i of this.last_update) {
                        if (moment(i.last_update).isBefore(endTime)) {
                            sites += i.acronym + ' ,'
                        }
                    }
                    sites = sites.slice(0, -1)
                }
                let base = 'Please note that taboola campaigns revenue is not final yet ' + sites;
                if (sites) {
                    this.last_update_arry.push({'label': base});
                }
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
            filter_field: function (field) {
                this.filter = field;
                this.filterMobile = false;
                this.$refs.filter_field.$el.innerHTML = field;
                this.filter_fields_hide = false;
            },
            get_colors: function (params) {
                params.page_type = 'campaign';
                this.$http.get('/api/website/colors', {params: params}).then(res => {
                    if (res.body) {
                        this.colors = Object.keys(res.body).map(key => res.body[key]);
                    }
                });
            },
            color_roi() {
                if (this.inited_summary['revenue'] && this.inited_summary['cost']) {
                    let res = (this.inited_summary['revenue'] / this.inited_summary['cost']) * 100;
                    if (parseInt(res) <= 129) {
                        return 's_danger'
                    } else if (parseInt(res) >= 129 && parseInt(res) <= 149) {
                        return 's_warning'
                    } else if (parseInt(res) >= 150) {
                        return 's_success'
                    }
                }
            },
            mark_missing(item) {
                if (!item) {
                    return;
                }
                if (item.device === 'desktop' && (item.hb_revenue_dfp < 0.01 || (item.ad_sense_revenue_dfp + item.adx_revenue) < 0.01) || (item.taboola_revenue < 0.01 && item.revcontent_revenue < 0.01 && item.outbrain_revenue < 0.01)) {
                    return true;
                } else if ((item.taboola_revenue < 0.01 && item.outbrain_revenue < 0.01) || (item.revcontent_revenue < 0.01 && item.source === 'revcontent')) {
                    return true;
                } else if (item.revenue > 0 && ((item.taboola_revenue / item.revenue >= 0.8) || (item.outbrain_revenue / item.revenue >= 0.8))) {
                    return true;
                }
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
            isValidId(cid) {
                return cid.trim().indexOf(' ') !== -1;
            },
            count_values(key, data) {
                return Object.keys(data.reduce((acc, o) => (acc[o[key]] = (acc[o[key]] || 0) + 1, acc), {})).length;
            },
            onDateRangeChange(range) {
                this.date_range = range
            },
            Timer(callback, time) {
                this.setTimeout(callback, time);
            },
            $title(val) {
                return val;
            },
            animate: function () {
                let self = this;
                self.animated = true;
                setTimeout(function () {
                    self.animated = false;
                }, 1000);
            },
            regex_filter(value, items) {
                const fix = v => {
                    if (v instanceof Object) {
                        return ['lp'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };
                const regex = new RegExp('.*' + value + '.*');
                return items.filter(item => regex.test(fix(item)));
            },
            formatPrc(val) {
                return val + '%';
            },
            formatCurrency(val, item) {
                if (item && val) {
                    return item.br === 1 ? 'R$' + val : '$' + val;
                }
                return val;
            },
            onlyNumber($event) {
                let evt = ($event) ? $event : window.event;
                let charCode = (evt.which) ? evt.which : evt.keyCode;

                if ([46, 8, 9, 27, 13, 110, 190].indexOf(charCode) !== -1 ||
                    // Allow: Ctrl+A
                    (charCode === 65 && evt.ctrlKey === true) ||
                    // Allow: Ctrl+C
                    (charCode === 67 && evt.ctrlKey === true) ||
                    // Allow: Ctrl+X
                    (charCode === 88 && evt.ctrlKey === true) ||
                    // Allow: home, end, left, right
                    (charCode >= 35 && charCode <= 39)) {
                    // let it happen, don't do anything
                    return
                }
                // Ensure that it is a number and stop the keypress
                if (($event.shiftKey || (charCode < 48 || charCode > 57)) && (charCode < 96 || charCode > 105)) {
                    $event.preventDefault()
                }
            },
            refreshScreen() {
                this.refreshLoading = true;
                this.submit();

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
                        return ['name', 'campaign_id', 'device', 'source'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.filter && this.filter.length > 0) {
                    const regex = new RegExp('.*' + this.filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                    this.$Progress.finish();
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

                this.automation_campaigns = _.filter(items, function (o) {
                    if (o.automation_active == '1') return o
                }).length;

                if (this.minClicks) {
                    items = items.filter(i => i.clicks > this.minClicks);
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
        },
        filters: {
            _get_str: function (value, key, map_audience = null) {
                if (value === undefined) {
                    return '';
                }

                let value_obj = JSON.parse(value);
                let curr_val = 'None';

                if (key === 'country' || key === 'platform') {
                    if (value_obj.value === [] || value_obj.value === '') {
                        curr_val = 'All';
                    } else {
                        curr_val = value_obj.value;
                    }

                    if (value.indexOf('EXCLUDE') !== -1) {
                        curr_val = 'WW';
                    }
                }
                else if (key === 'os') {
                    curr_val = value_obj.value[0].os_family;
                }
                else if (key === 'audience') {
                    let mapping = {};
                    for (let i of JSON.parse(JSON.stringify(map_audience))) {
                        mapping[i["audience_id"]] = i['display_name']
                    }
                    if (value_obj.collection[0]) {
                        let collection_array = value_obj.collection[0].collection;
                        let map_array = [];
                        for (let i of collection_array) {
                            map_array.push(mapping[i]);
                        }
                        if (map_array.length === 0) {
                            map_array = 'None';
                        }
                        curr_val = map_array;
                    }
                }
                else if (key === 'marketplace') {
                    if (value_obj.collection[0]) {
                        let mapping = {};
                        for (let i of JSON.parse(JSON.stringify(map_audience))) {
                            mapping[i["audience_id"]] = i['display_name']
                        }

                        curr_val = mapping[value_obj.collection[0].collection.join()];
                        if (curr_val === null) {
                            curr_val = 'None';
                        }
                    }
                } else {
                    curr_val = 'None';
                }
                if (value.indexOf('INCLUDE') !== -1) {
                    return 'Inc. ' + curr_val;
                } else if (value.indexOf('EXCLUDE') !== -1 && curr_val !== 'WW') {
                    return 'Excl. ' + curr_val;
                } else {
                    return curr_val;
                }
            },
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
            prc: function (val) {
                if (val) {
                    return val + '%'
                }
            }
        },
        watch: {
            _items: function (val) {
                if (val === undefined || val.length === 0) {
                    this.emptySummary = false;
                    return;
                }
                let _filter = this.filter === '' || this.filter == null;
                let data = this.filter_summary();

                let sums = {};
                let keys = ['clicks', 'revenue', 'cost', 'profit', 'taboola_revenue', 'outbrain_revenue', 'adx_revenue', 'hb_revenue_dfp', 'ad_sense_revenue_dfp', 'ex_revenue'];

                const self = this;
                _.each(data, function (item) {
                    item.exhausted_status_tb = item.br === 1 ? (item.cost * 100) / (item.daily_cap / self.brl_currency) : item.exhausted_status_tb;
                    _.each(keys, function (key) {
                        sums[key] = (parseFloat(sums[key]) || 0) + parseFloat(item[key]);
                    });
                });

                this.sum_campaigns = data.length;
                this.sum_device = this.selected_device !== 'All' ? 1 : this.count_values('device', !_filter ? data : this.items);
                this.sum_source = this.selected_campaign_source !== 'All' ? 1 : this.count_values('source', !_filter ? data : this.items);

                this.sum_clicks = sums.clicks;
                this.sum_revenue = sums.revenue;
                this.sum_cost = sums.cost;
                this.sum_profit = sums.profit;

                this.outbrain_revenue_total = sums.outbrain_revenue;
                this.taboola_revenue_total = sums.taboola_revenue;
                this.adx_revenue_total = sums.adx_revenue;
                this.hb_revenue_total = sums.hb_revenue_dfp;

                this.adsense_dfp_revenue_total = sums.ad_sense_revenue_dfp;
                this.adsense_analytics_revenue_total = sums.ad_sense_mobile_revenue;
                this.ex_revenue_total = sums.ex_revenue;

                this.count_sites = this._count_sites();
                this.wavg_clicks_ctr = this._wavg('clicks', 'ctr');
                this.wavg_clicks_pages_session = this._wavg('clicks', 'pages_session');
                this.wavg_bounce_rate = this._wavg('clicks', 'bounce_rate');
                this.wavg_clicks_roi_current = this._wavg('clicks', 'roi_current');
                this.avg_us = this._avg('us');
                this.avg_br = this._avg('br');

                this.losing_campaigns_count = _.filter(data, function (o) {
                    if (o.alert === 1) return o
                }).length;

                this.emptySummary = true;

                const est = moment().tz('America/New_York').format("YYYY-MM-DD HH:mm");
                const start = moment(new Date(est));
                this.bidder = moment(new Date(start));
            },
            campaign_show(cfg) {
                localStorage.campaign_show = cfg;
            },
        },
    }

    this.a.methods.Timer.prototype.setTimeout = function (callback, time) {
        let self = this;
        if (this.timer) {
            clearTimeout(this.timer);
        }
        this.finished = false;
        this.callback = callback;
        this.time = time;
        this.timer = setTimeout(function () {
            self.finished = true;
            callback();
        }, time);
        this.start = Date.now();
    };
    this.a.methods.Timer.prototype.add = function (time) {
        if (!this.finished) {
            // add time to time left
            time = this.time - (Date.now() - this.start) + time;
            this.setTimeout(this.callback, time);
        }
    }

</script>
<style lang="scss">
    @import "~vue-snotify/styles/material.css";
</style>
<style scoped>
    /deep/ .snotify-rightTop {
        width: 500px !important;
    }

    /deep/ .snotifyToast__title {
        padding-left: 0;
        font-size: 1.6em !important;
    }

    /deep/ .ant-input-number-handler-wrap {
        opacity: 1 !important;
    }

    .tdWidth {
        min-width: 157px;
    }

    .iconSt {
        margin-top: 3px;
        float: none;
        padding: 0px;
    }

    @import "../../../node_modules/vuetify/dist/vuetify.min.css";
    @import "../../assets/styles/pages/_CampaignData.scss";
</style>

<style>
    .before {
        height: unset !important;
    }

    .dp_block {
        cursor: not-allowed;
    }

    .dp_allow {
        cursor: pointer;
    }

    .duplicate-column {
        max-width: 250px;
    }
</style>
