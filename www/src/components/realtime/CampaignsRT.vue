<template>
    <div id="campaign_data_rt">
        <vue-progress-bar></vue-progress-bar>
        <vue-headful title="Websites Campaigns RT"/>
        <div v-show="!showMediumkey">
            <!--Campaign - Form-->
            <form @submit="submit">
                <div class="row">
                    <div class="col-xs-2">
                        <websites-dropdown @selectWebsite="selectWebsite($event)"></websites-dropdown>
                    </div>
                    <div class="col-xs-2">
                        <sources-dropdown @selectSource="selectSource($event)"></sources-dropdown>
                    </div>
                    <div class="isDisabled col-xs-2" style="width: 16% !important;">
                        <v-menu full-width offset-y :close-on-content-click="false" v-model="dateMenu" bottom>
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
                        <v-btn type="submit" color="info" :disabled="loading">Submit</v-btn>
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
            <el-alert style="font-weight:bold"
                      title="Important! please keep in mind the real-time data is estimated and not final"
                      type="info"
                      :closable="false"
                      center
                      show-icon>
            </el-alert>
            <el-alert style="font-weight:bold"
                      title="Gemini real-time is not functional, please do not use! "
                      type="error"
                      :closable="false"
                      center
                      show-icon>
            </el-alert>

            <cascader ref="cascader" :class="[disabled ? 'tb-hide' : '']" style="padding: 9px 0 9px 0;"></cascader>

            <!--Campaigns-Websites-Table-->
            <table class="table table-striped table-hover" :class="[hide ? 'tb-hide' : '','']">
                <thead>
                <tr>
                    <th v-if="display_bulk_change && items.length > 0">
                        <label class="form-checkbox">
                            <input type="checkbox" v-model="selectAllItems" @change="campaign_selected_init">
                        </label>
                    </th>
                    <th @click="headClick(field,key, true)" class="pointer"
                        :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"
                        v-for="(field, key) in tfields">
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
                        <div v-else-if="key == 'chart' && show_chart">
                            <strong>{{field.label}}&ensp; <span
                                    class="sub_label_title">{{field.sub_label}}</span></strong>
                        </div>
                        <div v-else-if="key != 'chart'">
                            <strong>{{field.label}}&ensp; <span
                                    class="sub_label_title">{{field.sub_label}}</span></strong>
                        </div>
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr v-if="items.length > 0"
                    style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                    <td v-if="display_bulk_change"></td>
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
                    <td class="summary"><span>N/A</span></td>
                    <td class="summary"></td>
                    <td class="summary"><span>N/A</span></td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Number of clicks</div>
                            <span>{{sum_clicks}}</span></el-tooltip>
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
                            <span>{{sum_cost | _format_(0)}}<i style="padding-left: 2px;">$</i></span></el-tooltip>
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
                            <div slot="content">Weighted Avg. of the current bid <br> Separated to USD and BRL</div>
                            <span v-if="!(avg_br == 0 && avg_us == 0)">{{ avg_us | _format_(4)}} <i
                                    style="padding-left: 2px;">$</i> | {{ avg_br | _format_(4)}} <i
                                    style="padding-left: 2px;">R$</i></span></el-tooltip>
                    </td>
                    <td class="summary">
                        <el-tooltip placement="top">
                            <div slot="content">Weighted Avg. of Current ROIs</div>
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
                    <td class="summary"></td>
                </tr>

                <tr v-for="(item, index) in _items" v-if="item!==undefined && item.campaign_id!=null" :ref="++index">
                    <td v-if="display_bulk_change">
                        <label>
                            <input type="checkbox" v-model="selectItem" :value="item" @change="item.index=index">
                        </label>
                    </td>
                    <td>
                        <span class="link" @click="filter_field(item.source, 'source')">{{item.source}}</span>
                    </td>
                    <td>
                        <span>{{ item.acronym }}</span>
                    </td>
                    <td :class="[item.automation == '1' ? 'tdWidth' : '']">
                        <el-tooltip class="item" effect="dark"
                                    :content="campaign_show === 'id' ? item.name : item.campaign_id"
                                    placement="top-start">
                            <el-tooltip :disabled="!isValidId(item.campaign_id)" class="item" effect="dark"
                                        content="Campaign id contain whitespace" placement="top-start">
                                <span>
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
                        <div class="red-label block" v-if="item.enable == '0'"><span>(disabled)</span></div>

                        <el-tooltip v-if="item.automation == '1'" placement="top">
                            <div slot="content">
                                <div>This campaign has automation rules applied to it.</div>
                            </div>
                            <i v-if="item.automation == '1'" class="fas fa-cogs float-icon" aria-hidden="true"
                               style="margin-top:3px;"></i>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{item.creation_date}}</span>
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
                        <span>{{item.rt_creation_date | _humanize_}}</span>
                    </td>
                    <td>
                        <span>{{item.clicks}}</span>
                    </td>
                    <td>
                        <div v-if="item.revenue > 0.01">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    Taboola Revenue: {{item.taboola_revenue | _format_(2)}}<br/>
                                    Outbrain Revenue: {{item.outbrain_revenue | _format_(2)}}<br/>
                                    HB Revenue: {{item.hb_revenue_dfp | _format_(2)}}<br/>
                                    Adsense Revenue: {{item.ad_sense_revenue_dfp | _format_(2)}}<br/>
                                    AdX Revenue: {{item.adx_revenue | _format_(2)}}<br/>
                                    Ex Revenue: {{item.ex_revenue | _format_(2)}}<br/>
                                </div>
                                <span>{{item.revenue | _format_(2) }}<i style="padding-left: 2px;">$</i></span>
                            </el-tooltip>
                            <i v-if="mark_missing(item)" class="fa fa-exclamation red-label" aria-hidden="true"></i>
                        </div>
                        <div v-else-if="item.revenue < 0.01">
                            <el-tooltip placement="top">
                                <div slot="content">
                                    <div>No revenue to display</div>
                                </div>
                                <span>{{item.revenue | _format_(2) }}</span>
                            </el-tooltip>
                            <i v-if="mark_missing(item)" class="fa fa-exclamation red-label" aria-hidden="true"></i>
                        </div>
                    </td>
                    <td v-if="item.source === 'taboola'" style="min-width: 90px">
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
                            <v-spacer v-if="item.br != 0"></v-spacer>
                            <p v-if="item.br != 0" class="campaign_roi_adjust">Campaign new cost: {{budget /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br != 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br != 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br == 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi == 1"
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
                            <v-spacer v-if="item.br != 0"></v-spacer>
                            <p v-if="item.br != 0" class="campaign_roi_adjust">Campaign new cost: {{budget /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br != 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br != 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br == 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi == 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td v-else-if="item.source === 'facebook' || item.source === 'zemanta' || item.source === 'outbrain'" style="min-width: 90px">
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
                            <v-spacer v-if="item.br != 0"></v-spacer>
                            <p v-if="item.br != 0" class="campaign_roi_adjust">Campaign new cost: {{daily_cap /
                                brl_currency | _format_(0) }} $</p>
                            <span v-if="item.cost_currency && item.br != 0" @mouseover="item.cost_currency = false"
                                  slot="reference" class="link">{{parseInt(item.daily_cap / brl_currency)}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <span v-else-if="item.br != 0" @mouseleave="item.cost_currency = true" slot="reference"
                                  class="link">{{item.daily_cap}}<i style="padding-left: 2px;">R$</i></span>
                            <span v-if="item.br == 0" slot="reference" class="link">{{item.daily_cap}}<i
                                    style="padding-left: 2px;">$</i></span>
                            <div class="text-xs-center">
                                <v-btn @click="edit_campaign_budget(item)" round color="success" dark>Save</v-btn>
                            </div>
                        </el-popover>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi == 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>
                    <td v-else>
                        <span>{{item.cost}}<i style="padding-left: 2px;">$</i> / {{item.daily_cap}}</span>
                        <el-tooltip effect="dark" content="This campaign is close to exceeding its budget"
                                    placement="top">
                            <i v-if="item.exhausted_status > 90 && item.exhausted_roi == 1"
                               class="far fa-credit-card exhausted"></i>
                        </el-tooltip>
                    </td>

                    <td :class="[item.smrtbid ? 'smrtbid' : '']">
                        <span>{{item.profit | _format_(2)}}<i style="padding-left: 2px;">$</i></span>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content">
                                Taboola UV: {{item.taboola_uv | _format_(4)}}<br/>
                                Outbrain UV: {{item.outbrain_uv | _format_(4)}}<br/>
                                HB UV: {{item.hb_revenue_dfp / item.clicks | _format_(4)}}<br/>
                                Adsense UV: {{item.ad_sense_revenue_dfp / item.clicks | _format_(4)}}<br/>
                                AdX UV: {{item.adx_revenue / item.clicks | _format_(4)}}<br/>
                                Ex UV: {{item.ex_revenue / item.clicks | _format_(4)}}<br/>
                                Yesterday's UV: {{item.yest_final_uv | _format_(4)}}<br/>
                            </div>
                            <span>{{item.final_uv | _format_(4)}}<i style="padding-left: 2px;">$</i></span>
                        </el-tooltip>
                    </td>
                    <td>
                        <span>{{item.pages_session | _format_(1)}}</span>
                    </td>

                    <td style="min-width: 90px">
                        <!-- Taboola Bidder-->
                        <div v-if="item.source === 'taboola'" @click="reset_bidder_time(item)">
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
                                            <span v-if="item.br != 0" class="currency_convert larger_font">{{taboola_bid / brl_currency | _format_(4)}}$</span>
                                        </el-col>
                                    </el-form-item>
                                </el-form>

                                <div class="text-xs-center pop_over_btns">
                                    <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                               style="color: #2196f3;width: 180px;">APPLY NOW
                                    </el-button>
                                </div>

                                <div v-if="enable_scheduled_bids">
                                    <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">
                                        Campaign scheduled bids
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
                                                            :disabled="bidder.new == 'false'"
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
                                                    <span v-show="!bidder_deleting"><i
                                                            @click="remove_bidder(item, bindex)" class="el-icon-delete"
                                                            style="font-size: large;cursor: pointer"></i></span>
                                                    <el-tooltip content="Please save to apply changes" placement="right"
                                                                effect="dark">
                                                        <span v-if="bidder.new == true" class="new_label"
                                                              @mouseover="animate">new</span>
                                                    </el-tooltip>
                                                </el-col>
                                            </el-form-item>
                                        </el-form>
                                        <p v-if="item.br != 0" class="campaign_roi_adjust"
                                           style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency |
                                            _format_(4)}} $</p>
                                    </div>

                                    <i @click="add_bidder(item)"
                                       :class="[item.bidders && item.bidders.length == 7 ? 'tb-hide' : '','far fa-plus-square']">
                                        Schedule bid</i>

                                    <div v-if="item.bidders && item.bidders.length > 0"
                                         class="text-xs-center pop_over_btns">
                                        <el-button @click="save_bidder(item)" :loading="bidder_saving"
                                                   class="bidder_btn" :class="{'shake animated': animated}" plain round
                                                   small style="color: #2196f3;width: 180px;">SAVE
                                        </el-button>
                                    </div>
                                </div>

                                <span v-if="item.bid_currency && item.br != 0" @mouseover="item.bid_currency = false"
                                      slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                                <span v-else-if="item.br != 0" @mouseleave="item.bid_currency = true" slot="reference"
                                      class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                                <span v-if="item.br == 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-popover>

                            <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                                <span @click="item.pop_visible=true"
                                      v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                        class="far fa-clock pop_over_clock"></i></span>
                            </el-tooltip>
                        </div>
                        <!-- Gemini Bidder-->
                        <div v-else-if="item.source === 'gemini'" @click="reset_bidder_time(item)">
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
                                            <span v-if="item.br != 0" class="currency_convert larger_font">{{gemini_bid / brl_currency | _format_(4)}}$</span>
                                        </el-col>
                                    </el-form-item>
                                </el-form>

                                <div class="text-xs-center pop_over_btns">
                                    <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                               style="color: #2196f3;width: 180px;">APPLY NOW
                                    </el-button>
                                </div>

                                <div v-if="enable_scheduled_bids">
                                    <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">
                                        Campaign scheduled bids
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
                                                            :disabled="bidder.new == 'false'"
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
                                                    <span v-show="!bidder_deleting"><i
                                                            @click="remove_bidder(item, bindex)" class="el-icon-delete"
                                                            style="font-size: large;cursor: pointer"></i></span>
                                                    <el-tooltip content="Please save to apply changes" placement="right"
                                                                effect="dark">
                                                        <span v-if="bidder.new == true" class="new_label"
                                                              @mouseover="animate">new</span>
                                                    </el-tooltip>
                                                </el-col>
                                            </el-form-item>
                                        </el-form>
                                        <p v-if="item.br != 0" class="campaign_roi_adjust"
                                           style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency |
                                            _format_(4)}} $</p>
                                    </div>

                                    <i @click="add_bidder(item)"
                                       :class="[item.bidders && item.bidders.length == 7 ? 'tb-hide' : '','far fa-plus-square']">
                                        Schedule bid</i>

                                    <div v-if="item.bidders && item.bidders.length > 0"
                                         class="text-xs-center pop_over_btns">
                                        <el-button @click="save_bidder(item)" :loading="bidder_saving"
                                                   class="bidder_btn" :class="{'shake animated': animated}" plain round
                                                   small style="color: #2196f3;width: 180px;">SAVE
                                        </el-button>
                                    </div>
                                </div>

                                <span v-if="item.bid_currency && item.br != 0" @mouseover="item.bid_currency = false"
                                      slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                                <span v-else-if="item.br != 0" @mouseleave="item.bid_currency = true" slot="reference"
                                      class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                                <span v-if="item.br == 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-popover>

                            <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                                <span @click="item.pop_visible=true"
                                      v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                        class="far fa-clock pop_over_clock"></i></span>
                            </el-tooltip>
                        </div>
                        <!-- Facebook Bidder-->
                        <div v-else-if="item.source === 'facebook'" @click="reset_bidder_time(item)">
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
                                            <span v-if="item.br != 0" class="currency_convert larger_font">{{facebook_bid / brl_currency | _format_(4)}}$</span>
                                        </el-col>
                                    </el-form-item>
                                </el-form>

                                <div class="text-xs-center pop_over_btns">
                                    <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                               style="color: #2196f3;width: 180px;">APPLY NOW
                                    </el-button>
                                </div>

                                <div v-if="enable_scheduled_bids">
                                    <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">
                                        Campaign scheduled bids
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
                                                            :disabled="bidder.new == 'false'"
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
                                                    <span v-show="!bidder_deleting"><i
                                                            @click="remove_bidder(item, bindex)" class="el-icon-delete"
                                                            style="font-size: large;cursor: pointer"></i></span>
                                                    <el-tooltip content="Please save to apply changes" placement="right"
                                                                effect="dark">
                                                        <span v-if="bidder.new == true" class="new_label"
                                                              @mouseover="animate">new</span>
                                                    </el-tooltip>
                                                </el-col>
                                            </el-form-item>
                                        </el-form>
                                        <p v-if="item.br != 0" class="campaign_roi_adjust"
                                           style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency |
                                            _format_(4)}} $</p>
                                    </div>

                                    <i @click="add_bidder(item)"
                                       :class="[item.bidders && item.bidders.length == 7 ? 'tb-hide' : '','far fa-plus-square']">
                                        Schedule bid</i>

                                    <div v-if="item.bidders && item.bidders.length > 0"
                                         class="text-xs-center pop_over_btns">
                                        <el-button @click="save_bidder(item)" :loading="bidder_saving"
                                                   class="bidder_btn" :class="{'shake animated': animated}" plain round
                                                   small style="color: #2196f3;width: 180px;">SAVE
                                        </el-button>
                                    </div>
                                </div>

                                <span v-if="item.bid_currency && item.br != 0" @mouseover="item.bid_currency = false"
                                      slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                                <span v-else-if="item.br != 0" @mouseleave="item.bid_currency = true" slot="reference"
                                      class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                                <span v-if="item.br == 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-popover>

                            <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                                <span @click="item.pop_visible=true"
                                      v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                        class="far fa-clock pop_over_clock"></i></span>
                            </el-tooltip>
                        </div>
                        <!-- Zemanta Bidder-->
                        <div v-else-if="item.source === 'zemanta'" @click="reset_bidder_time(item)">
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
                                            <span v-if="item.br != 0" class="currency_convert larger_font">{{zemanta_bid / brl_currency | _format_(4)}}$</span>
                                        </el-col>
                                    </el-form-item>
                                </el-form>

                                <div class="text-xs-center pop_over_btns">
                                    <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                               style="color: #2196f3;width: 180px;">APPLY NOW
                                    </el-button>
                                </div>

                                <div v-if="enable_scheduled_bids">
                                    <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">
                                        Campaign scheduled bids
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
                                                            :disabled="bidder.new == 'false'"
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
                                                    <span v-show="!bidder_deleting"><i
                                                            @click="remove_bidder(item, bindex)" class="el-icon-delete"
                                                            style="font-size: large;cursor: pointer"></i></span>
                                                    <el-tooltip content="Please save to apply changes" placement="right"
                                                                effect="dark">
                                                        <span v-if="bidder.new == true" class="new_label"
                                                              @mouseover="animate">new</span>
                                                    </el-tooltip>
                                                </el-col>
                                            </el-form-item>
                                        </el-form>
                                        <p v-if="item.br != 0" class="campaign_roi_adjust"
                                           style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency |
                                            _format_(4)}} $</p>
                                    </div>

                                    <i @click="add_bidder(item)"
                                       :class="[item.bidders && item.bidders.length == 7 ? 'tb-hide' : '','far fa-plus-square']">
                                        Schedule bid</i>

                                    <div v-if="item.bidders && item.bidders.length > 0"
                                         class="text-xs-center pop_over_btns">
                                        <el-button @click="save_bidder(item)" :loading="bidder_saving"
                                                   class="bidder_btn" :class="{'shake animated': animated}" plain round
                                                   small style="color: #2196f3;width: 180px;">SAVE
                                        </el-button>
                                    </div>
                                </div>

                                <span v-if="item.bid_currency && item.br != 0" @mouseover="item.bid_currency = false"
                                      slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                                <span v-else-if="item.br != 0" @mouseleave="item.bid_currency = true" slot="reference"
                                      class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                                <span v-if="item.br == 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-popover>

                            <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                                <span @click="item.pop_visible=true"
                                      v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                        class="far fa-clock pop_over_clock"></i></span>
                            </el-tooltip>
                        </div>
                        <!--Outbrain Bidder-->
                        <div v-else-if="item.source === 'outbrain'" @click="reset_bidder_time(item)">
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
                                            <span v-if="item.br != 0" class="currency_convert larger_font">{{outbrain_bid / brl_currency | _format_(4)}}$</span>
                                        </el-col>
                                    </el-form-item>
                                </el-form>

                                <div class="text-xs-center pop_over_btns">
                                    <el-button @click="edit_bid(item)" class="bidder_btn" plain round small
                                               style="color: #2196f3;width: 180px;">APPLY NOW
                                    </el-button>
                                </div>

                                <div v-if="enable_scheduled_bids">
                                    <v-subheader v-if="item.bidders && item.bidders.length > 0" class="sub_header">
                                        Campaign scheduled bids
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
                                                            :disabled="bidder.new == 'false'"
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
                                                    <span v-show="!bidder_deleting"><i
                                                            @click="remove_bidder(item, bindex)" class="el-icon-delete"
                                                            style="font-size: large;cursor: pointer"></i></span>
                                                    <el-tooltip content="Please save to apply changes" placement="right"
                                                                effect="dark">
                                                        <span v-if="bidder.new == true" class="new_label"
                                                              @mouseover="animate">new</span>
                                                    </el-tooltip>
                                                </el-col>
                                            </el-form-item>
                                        </el-form>
                                        <p v-if="item.br != 0" class="campaign_roi_adjust"
                                           style="margin: -30px 0 5px 115px">{{bidder.new_bid / brl_currency |
                                            _format_(4)}} $</p>
                                    </div>

                                    <i @click="add_bidder(item)"
                                       :class="[item.bidders && item.bidders.length == 7 ? 'tb-hide' : '','far fa-plus-square']">
                                        Schedule bid</i>

                                    <div v-if="item.bidders && item.bidders.length > 0"
                                         class="text-xs-center pop_over_btns">
                                        <el-button @click="save_bidder(item)" :loading="bidder_saving"
                                                   class="bidder_btn" :class="{'shake animated': animated}" plain round
                                                   small style="color: #2196f3;width: 180px;">SAVE
                                        </el-button>
                                    </div>
                                </div>

                                <span v-if="item.bid_currency && item.br != 0" @mouseover="item.bid_currency = false"
                                      slot="reference" class="link">{{item.bid / brl_currency | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                                <span v-else-if="item.br != 0" @mouseleave="item.bid_currency = true" slot="reference"
                                      class="link">{{item.bid | _format_(4)}}<i style="padding-left: 2px;">R$</i></span>
                                <span v-if="item.br == 0" slot="reference" class="link">{{item.bid | _format_(4)}}<i
                                        style="padding-left: 2px;">$</i></span>
                            </el-popover>

                            <el-tooltip effect="dark" content="Bid Scheduled, click to edit" placement="top">
                                <span @click="item.pop_visible=true"
                                      v-if="enable_scheduled_bids && item.bidders && item.bidders.length > 0"><i
                                        class="far fa-clock pop_over_clock"></i></span>
                            </el-tooltip>
                        </div>
                        <div v-else>
                            {{item.bid}}
                        </div>
                    </td>

                    <td>
                        <span v-if="item.br != 0 && item.bid > 0"
                              :class="[color(item, 'roi', item.final_uv / (item.bid / brl_currency)), 'roi_span',item.smrtbid ? 'smrtbid' : '']">{{ item.final_uv / (item.bid / brl_currency) | format_prc}}%</span>
                        <span v-else-if="item.bid > 0"
                              :class="[color(item, 'roi', item.roi_current), 'roi_span',item.smrtbid ? 'smrtbidroi' : '']">{{ item.roi_current | format_prc}}%</span>
                    </td>
                    <td :class="[item.smrtbid ? 'smrtbid' : '']">
                        <span>{{item.avg_bid | _format_(4) }}<i style="padding-left: 2px;">$</i></span>
                    </td>
                    <td>
                        <span :class="[color(item, 'roi', item.roi_final), 'roi_span',item.smrtbid ? 'smrtbid' : '']">{{item.roi_final | format_prc}}%</span>
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
                    <td v-if="item.source != 'custom' && show_chart && item.data && Array.isArray(item.data)"
                        style="width: 420px"
                        @mouseover="item.data.length > 0 ? shown_tool=index : ''">
                        <la-cartesian v-if="item.data.length > 0" autoresize :bound="[0]" :width="250" :height="70"
                                      :data=item.data>
                            <la-line :width="2" dot label="time (est)" prop="time" color="yellow"></la-line>
                            <la-line :width="2" dot label="uv" prop="uv" color="#6be6c1"
                                     :animationDuration="1"></la-line>
                            <la-line :width="2" dot label="avg bid" prop="avg_bid" color="#3fb1e3"
                                     :animationDuration="1"></la-line>
                            <la-line v-show="false" dot label="clicks" prop="_clicks" color="black"></la-line>
                            <la-line v-show="false" dot label="revenue" prop="_revenue" color="black"></la-line>
                            <la-line v-show="false" dot label="cost" prop="_cost" color="black"></la-line>

                            <la-tooltip v-show="item.data.length > 0 && shown_tool==index">
                                <div class="la-tooltip" slot-scope="props">
                                    <div v-if="item.label" class="la-title">{{ props.label }}</div>
                                    <ul class="list" @mouseover="shown_tool=index">
                                        <li v-for="item in props.actived" v-if="item.label"
                                            :style="{ borderTop: '6px solid ' + item.color }">
                                            <div :class="[item.label == 'time (est)' ? 'time':'','la-label']">{{
                                                item.label.toUpperCase() }}
                                            </div>
                                            <div class="la-value">{{ normalize(item,index)}}</div>
                                        </li>
                                    </ul>
                                </div>
                            </la-tooltip>
                        </la-cartesian>
                    </td>
                    <td v-else></td>
                    <td>
                        <div v-if="item.status =='IN_PROCESS' || item.status =='PENDING'" class="hourglass mleft"></div>
                        <i v-if="item.status =='ERROR'" class="fa fa-exclamation red-label"></i>
                        <div v-if="item.status =='DONE'">
                            <i class="fa fa-check-square green-label mleft"></i>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>

            <!--Campaigns-Pagination-->
            <el-row v-show="items.length > 0" :class="[hide ? 'tb-hide' : '','']" type="flex">
                <el-col>
                    <el-tooltip class="item" effect="dark" content="Per Page" placement="top-start"
                                style="height: 31px">
                        <el-input-number size="small" v-model="perPage" controls-position="right" :min="5"
                                         :step="5"></el-input-number>
                    </el-tooltip>
                    <el-tooltip class="item" effect="dark" content="Minimum Clicks" placement="top-start"
                                style="height: 31px">
                        <el-input-number size="small" v-model="minClicks" controls-position="right" :min="0"
                                         :step="100"></el-input-number>
                    </el-tooltip>
                    <div class="col-md-11 text-center" style="top: -52px">
                        <b-pagination size="md" :total-rows="items.length" :per-page="perPage" v-model="currentPage"/>
                    </div>
                </el-col>
            </el-row>

            <div class="_centered" v-loading="loading" style="width: 100%"></div>
        </div>
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
        name: 'campaign_data_rt',
        components: {
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
            if (localStorage.campaign_show) {
                this.campaign_show = localStorage.campaign_show;
            } else {
                this.campaign_show = 'id';
            }
        },
        data() {
            return {
                site_count: new Set(),
                time: '',
                shown_tool: -1,
                budget: 0,
                dateMenu: false,
                dateRangeOptions: {
                    startDate: moment().tz("America/New_York").format("YYYY-MM-DD"),
                    endDate: moment().tz("America/New_York").format("YYYY-MM-DD"),
                    format: 'MM/DD/YYYY',
                    presets: [
                        {
                            label: 'Today',
                            range: [
                                moment().tz("America/New_York").format("YYYY-MM-DD"),
                                moment().tz("America/New_York").format("YYYY-MM-DD"),
                            ],

                        },
                        {
                            label: 'Yestarday',
                            range: [
                                moment().subtract(1, "days").tz("America/New_York").format("YYYY-MM-DD"),
                                moment().subtract(1, "days").tz("America/New_York").format("YYYY-MM-DD"),
                            ],

                        },
                    ],
                },
                items: [],
                items_copy: [],
                campaign_source: [],
                websites: [],
                summary: [],
                colors: [],
                shown_item: '',
                automation_campaigns: 0,
                allow_toggle_auto: 0,
                step: 0.001,
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                sources: ['facebook', 'taboola', 'gemini', 'outbrain', 'revcontent', 'zemanta', 'custom'],
                tfields: {
                    source: {label: 'Source'},
                    name: {label: 'Site', sortable: false},
                    campaign_id: {label: 'Campaign', sortable: true},
                    creation_date: {label: 'CD', sortable: true},
                    landing_page: {label: 'LP', sortable: false, description: 'Landing page'},
                    rt_creation_date: {
                        label: 'Last Modified',
                        sortable: true,
                        description: 'The last time the data was updated'
                    },
                    clicks: {label: 'Clicks', sortable: true, description: 'Reported by the traffic source'},
                    revenue: {label: 'Revenue', sortable: true, description: 'Accumulated from all revenue sources'},
                    cost: {
                        label: 'C / B',
                        sortable: true,
                        description: 'Cost and Budget',
                        _description: 'Reported by the traffic source'
                    },
                    profit: {label: 'Profit', sortable: true, description: '= Revenue - Cost'},
                    final_uv: {label: 'UV', sortable: true, description: '= Revenue / Clicks'},
                    pages_session: {label: 'P/S', sortable: true, description: '= Pages per Session Reported by DFP'},
                    bid: {
                        label: 'Bid',
                        sortable: true,
                        description: 'Reported by the traffic sources',
                        sub_label: 'Current'
                    },
                    roi_current: {
                        label: 'ROI',
                        sortable: true,
                        sub_label: 'Current',
                        description: '= Campaign UV / Mediums Avg Bid'
                    },
                    avg_bid: {label: 'Avg bid', sortable: true, description: 'Reported by the traffic sources'},
                    roi_final: {label: 'ROI', sortable: true, description: '= UV / Avg.Bid'},
                    automation_active: {label: 'Auto', sortable: true, description: 'Enable/disable automation rules'},
                    chart: {label: 'Trend', sub_label: 'UV vs Clicks'},
                    status: {label: ''},
                },
                limit_date: moment.utc().startOf('day').format("YYYY-MM-DD"),
                show_chart: this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.rt_hourly_chart == 1,
                filterMobile: true,
                filter_fields_hide: true,
                sortDesc: true,
                sortFlag: false,
                loading: false,
                refreshLoading: false,
                showMediumkey: false,
                disabled: true,
                hide: true,
                enable_scheduled_bids: false,
                animated: false,
                sort: null,
                filter: null,
                edit_index: null,
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
                selected_campaign_source: "All",
                selected_device: "All",
                currentPage: 1,
                perPage: 20,
                minClicks: 0,
                brl_currency: 1,
                date_range: [
                    moment().tz("America/New_York").format("YYYY-MM-DD"),
                    moment().tz("America/New_York").format("YYYY-MM-DD")
                ],
                site_id: "All",
                inited_summary: {},
                campaign_show: ''
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
                this.checked_items = [];
            },
            onDateRangeChange(range) {
                this.date_range = range;
            },
            submit: function () {
                this.$Progress.start();
                let site_id = this.site_id == 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
                let device = (this.selected_device ? this.selected_device : 'all').toLocaleLowerCase();
                let source = (this.selected_campaign_source ? this.selected_campaign_source : 'all').toLocaleLowerCase();
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");

                let restrict = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.restricted_campaigns ? this.$store.getters.getUser.settings.restricted_campaigns : '0';
                this.enable_scheduled_bids = this.$store.getters.getUser.settings.scheduled_bids == 1;
                this.allow_toggle_auto = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.toggle_automation ? this.$store.getters.getUser.settings.toggle_automation : '0';

                if (site_id === null) {
                    this.alert('website');
                    return;
                }

                this.loading = true;
                this.disabled = true;
                this.hide = true;
                this.inited_summary = {};
                this.site_count = new Set();
                this.brl_currency = this.$store.getters.getCurrency;
                this.items = [];
                this.checked_items = [];

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
                }, 1);

                this.$http.get('/api/website/user_campaigns_rt', {params: params}).then(res => {
                    if (res.body) {
                        this.items = JSON.parse(JSON.parse(JSON.stringify(res.body['data'])));
                        this.items_copy = this.items;

                        if (this.items) {
                            if (this.show_chart) {
                                this.chart_init();
                            }
                            this.init_bidders();
                        }
                        if (this.$refs.cascader.reapply) {
                            this.$refs.cascader.reapply();
                        }

                        if (this.items.length === 0) {
                            this.filterClose();
                        } else {
                            this.headClick(this.tfields.cost, "cost");
                            this.sortDesc = false;
                            this.hide = false;
                            this.disabled = false;
                            this.mediumKeyword_items = this.items;
                        }
                        this.loading = false;
                        this.refreshLoading = false;
                        this.$Progress.finish();

                    } else {
                        this.$Progress.fail();
                        console.log("---------ERROR-----------");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    this.refreshLoading = false;
                    this.loading = false;
                    this.$Progress.fail();
                    this.notice("Error has occurred, Please try again");
                })
            },
            normalize(item, index) {
                if (item.value === undefined || this.shown_tool === undefined || this.shown_tool != index) return;
                if (item.label == 'time (est)') {
                    this.time = item.value;
                    return item.value;
                }
                const time = this.time;
                let values = this._items[index - 1].hash_data[time];
                return values[item.label.replace(' ', '_')];
            },
            chart_init() {
                try {
                    for (let i of this.items) {
                        if (typeof(i.data) == "string") {
                            i.data = JSON.parse(i.data);
                        }
                        if (typeof i.data[Symbol.iterator] === 'function') {
                            let arr = [];

                            for (let j of i.data) {
                                arr[j.time] = j;
                                arr[j.time]._clicks = 0;
                                arr[j.time]._revenue = 0;
                                arr[j.time]._cost = 0;
                            }

                            i.hash_data = arr;
                        }
                    }
                } catch (e) {
                    console.log(e)
                }
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

                this.refresh_campaign_status();
            },
            check_status_campaign(item) {
                if (!item) {
                    return
                }
                let site_id = this.site_id == 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
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

                this.$http.get('/api/website/user_campaigns_rt', {params: params}).then(res => {
                    if (res.body) {
                        this.items = JSON.parse(JSON.parse(JSON.stringify(res.body['data'])));
                        this.items_copy = this.items;
                        this.timer = undefined;
                        if (this.items) {
                            if (this.show_chart) {
                                this.chart_init();
                            }
                            this.init_bidders();
                          if (this.$refs.cascader.reapply) {
                            this.$refs.cascader.reapply();
                        }
                        }
                    } else {
                        console.log("REFRESH ERROR");
                    }
                }).catch(e => {
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
            },
            edit_campaign_budget_key_press(e, item) {
                if (e.keyCode === 13) {
                    this.edit_campaign_budget(item);
                }
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

                    if (current_filters.length == 0) {
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
                        } else if (i.type == 'less') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field == 'budget' && o.source == 'taboola') {
                                    return o['daily_cap'] < i.amount;
                                }
                                return o[i.field] < i.amount;
                            });
                        } else if (i.type == 'greater') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field == 'budget' && o.source == 'taboola') {
                                    return o['daily_cap'] > i.amount;
                                }
                                return o[i.field] > i.amount;
                            });
                        } else if (i.type == 'between') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                if (i.field == 'budget' && o.source == 'taboola') {
                                    return parseFloat(o['daily_cap']) > parseFloat(i.amount) && parseFloat(o['daily_cap']) < parseFloat(i.between);
                                }
                                return o[i.field] > i.amount && o[i.field] < i.between;
                            });
                        } else if (i.type == 'losing') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] == '1';
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
                    if (query.type == 'less') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field == 'budget' && o.source == 'taboola') {
                                return o['daily_cap'] < query.amount;
                            }
                            return o[query.field] < query.amount;
                        });
                    } else if (query.type == 'greater') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field == 'budget' && o.source == 'taboola') {
                                return o['daily_cap'] > query.amount;
                            }
                            return o[query.field] > query.amount;
                        });
                    } else if (query.type == 'equals') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            return o[query.field] > query.amount - 0.01 && o[query.field] < query.amount + 0.01;
                        });
                    } else if (query.type == 'between') {
                        scope.$data.items = _.filter(scope.$data.items, function (o) {
                            if (query.field == 'budget' && o.source == 'taboola') {
                                return parseFloat(o['daily_cap']) > parseFloat(query.amount) && parseFloat(o['daily_cap']) < parseFloat(query.between);
                            }
                            return o[query.field] > query.amount && o[query.field] < query.between;
                        });
                    }
                }

                else if (query) {
                    scope.$data.items = this.cascaderFilterExtend(query, scope.$data.items);
                }

                if (current_filters.length > 0 && !query && scope.$data.items.length == 0 && !remove && !remove_all) {
                    scope.$data.disabled = false;
                }

                scope.$data.checked_items = [];
            },
            cascaderFilterExtend(query, items) {

                if (query.type == 'creation') {
                    return _.filter(items, function (o) {
                        return Date.parse(o[query.field]) >= Date.parse(query.value[0]) && Date.parse(o[query.field]) <= Date.parse(query.value[1]);
                    });
                }
                else if (query.type == 'landing') {
                    return this.regex_filter(query.value, items)
                }
                else if (query.type == 'losing') {
                    return _.filter(items, function (o) {
                        return o[query.field] == '1';
                    });
                }
                else if (query.type == 'exceeded') {
                    return _.filter(items, function (o) {
                        return (o[query.field] > 90 || o[query.field + "_tb"] > 90) && o['exhausted_roi'] == 1;
                    });
                }
                else if (query.type == 'bidder') {
                    return _.filter(items, function (o) {
                        return o[query.field] && o[query.field].length > 0;
                    });
                }
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
            Timer(callback, time) {
                this.setTimeout(callback, time);
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
                if (key == 'device' || key == 'source' || key == 'name') {
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
            isValidId(cid) {
                return cid.trim().indexOf(' ') !== -1;
            },
            sessionsDiff(item) {
                if (item && item.sessions && item.clicks) {
                    return (item.clicks - (item.sessions * 0.1)) > item.sessions;
                }
                return false
            },
            mark_missing(item) {
                if (!item) {
                    return;
                }
                if ((item.hb_revenue_dfp < 0.01) || (item.taboola_revenue + item.outbrain_revenue < 0.01) || ((item.ad_sense_revenue_dfp + item.adx_revenue) < 0.01)) {
                    return true;
                }
            },
            sort_dates(item) {
                return item.sort(function (a, b) {
                    return new Date(a.data_date + ' ' + a.time) - new Date(a.data_date + ' ' + b.time);
                });
            },
            hideInput(index) {
                this.$refs['bid_input_' + index][0].$el.className = this.$refs['bid_input_' + index][0].$el.className.replace("edit-bid", "tb-hide");
                this.$refs['bid_apply_' + index][0].className = this.$refs['bid_apply_' + index][0].className.replace("edit-bid", "tb-hide");
                this.$refs['bid_close_' + index][0].className = this.$refs['bid_close_' + index][0].className.replace("edit-bid", "tb-hide");
            },
            showInput(item, index) {
                if (this.edit_index) {
                    this.hideInput(this.edit_index)
                }
                this.taboola_bid = item.bid;
                this.edit_index = index;
                this.$refs['bid_input_' + index][0].$el.className = this.$refs['bid_input_' + index][0].$el.className.replace("tb-hide", "edit-bid");
                this.$refs['bid_apply_' + index][0].className = this.$refs['bid_apply_' + index][0].className.replace("tb-hide", "edit-bid");
                this.$refs['bid_close_' + index][0].className = this.$refs['bid_close_' + index][0].className.replace("tb-hide", "edit-bid");
            },
            count_values(key, data) {
                return Object.keys(data.reduce((acc, o) => (acc[o[key]] = (acc[o[key]] || 0) + 1, acc), {})).length;
            },
            color(item, key, val) {
                if (!item) {
                    return
                }
                if (key != 'roi') {
                    item.source = item.source.toLowerCase().replace('.com', '');
                    const elem = this.colors.find(color =>
                        color.source == item.source &&
                        color.device == item.device &&
                        color.field == key &&
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
                if (this.inited_summary[key] != undefined) {
                    if (key == 'ctr') {
                        if (this.inited_summary[key] <= 0.8 && this.inited_summary[key] >= 0.5) {
                            return 's_warning'
                        } else if (this.inited_summary[key] > 0.8) {
                            return 's_success'
                        } else if (this.inited_summary[key] < 0.5) {
                            return 's_danger'
                        }
                    } else if (key == 'pages_session') {
                        if (this.inited_summary[key] <= 16 && this.inited_summary[key] >= 10) {
                            return 's_warning'
                        } else if (this.inited_summary[key] > 16) {
                            return 's_success'
                        } else if (this.inited_summary[key] < 10) {
                            return 's_danger'
                        }
                    } else if (key == 'roi_current' && this.inited_summary[key]) {
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
            _sum(key, data) {
                let res = parseFloat(_.sumBy([key], _.partial(_.sumBy, data)));
                if (res != undefined) {
                    this.inited_summary[key] = res;
                    return res;
                }
            },
            _wavg(w, v, taboola) {
                let data = this.filter_summary();

                if (taboola) {
                    data = data.filter(function (el) {
                        return el.source == 'taboola';
                    });
                }
                data = data.filter(function (el) {
                    return el.bid > 0;
                });

                let res = ((_w, _v) => _v / _w)(...data.reduce((r, o) => [r[0] + o[w], r[1] + o[w] * o[v]], [0, 0]));
                if (res != undefined) {
                    this.inited_summary[v] = res;
                    return res;
                }
            },
            _avg(currency) {
                if (typeof(currency) == "object") return;
                if (this.items) {
                    let currency_items = [];
                    if (currency == 'br') {
                        currency_items = this.filter_summary().filter(function (el) {
                            return el.br != 0 && el.bid > 0;
                        });

                    } else {
                        currency_items = this.filter_summary().filter(function (el) {
                            return el.br == 0 && el.bid > 0;
                        });
                    }

                    if (currency_items.length == 0) {
                        return 0
                    }

                    let res = ((_w, _v) => _v / _w)(...currency_items.reduce((r, o) => [r[0] + o['clicks'], r[1] + o['clicks'] * (o['bid'])], [0, 0]));
                    this.inited_summary[currency] = isNaN(res) ? 'N/A' : res;
                    return res;
                }
            },
            _count_sites() {
                if (this.site_id != 'All') {
                    return 1;
                }

                this.site_count.clear();
                let _filter = this.filter == '' || this.filter == null;
                let items = !_filter ? this.filter_summary() : this.items;
                let acr = '';
                for (let i of items) {
                    acr = i.name.split('-');
                    let _acr = acr[0].toLowerCase().replace(/ /g, "") != 'msnsafe' ? acr[0].trim() : this.site_count.add(acr[1].trim());
                    if (!this.sources.includes(_acr) && !this.site_count.has(_acr) && _acr.length <= 3 && _acr != 'msn') {
                        this.site_count.add(_acr);
                    }
                }
                return this.site_count.size;
            },
            formatCurrency(val, item) {
                if (item && val) {
                    return item.br == 1 ? 'R$' + val : '$' + val;
                }
                return val;
            },
            animate: function () {
                let self = this;
                self.animated = true;
                setTimeout(function () {
                    self.animated = false;
                }, 1000);
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
                }

                // Apply Sort
                if (this.sort) {
                    const field = this.sort;
                    let flag = this.sortFlag;
                    items = items.sort(function (a, b) {
                        if (field == 'rt_creation_date' || field == 'creation_date') {
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
                // Apply pagination
                if (this.perPage) {
                    items = items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage);
                }

                return items;
            },
        },
        filters: {
            _format_: function (value, fix) {
                if (!value && value !== 0) {
                    return ''
                }
                return parseFloat(value).toFixed(fix);
            },
            _humanize_: function (value) {
                if (value == 0) {
                    return 'NEW CAMPAIGN'
                }
                let m1 = moment.tz(value, "America/New_York");
                let m2 = moment().tz("America/New_York");
                let forHuman = moment.duration(m1.diff(m2)).humanize();
                return forHuman === 'invalid date' ? forHuman : forHuman + ' ago';
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
                if (val === undefined || val.length == 0) {
                    this.emptySummary = false;
                    return;
                }
                let _filter = this.filter == '' || this.filter == null;
                let data = this.filter_summary();

                let sums = {};
                let keys = ['clicks', 'revenue', 'cost', 'profit', 'taboola_revenue', 'outbrain_revenue', 'adx_revenue', 'hb_revenue_dfp', 'ad_sense_revenue_dfp', 'ex_revenue'];
                const self = this;

                _.each(data, function (item) {
                    item.exhausted_status = item.source == 'taboola' && item.br == 1 ? (item.cost * 100) / (item.daily_cap / self.brl_currency) : item.exhausted_status;
                    item.roi_current = item.source == 'taboola' && item.br == 1 ? item.final_uv / (item.bid / self.brl_currency) : item.roi_current;
                    _.each(keys, function (key) {
                        sums[key] = (parseFloat(sums[key]) || 0) + parseFloat(item[key]);
                    });
                });

                this.sum_clicks = sums.clicks;
                this.sum_revenue = sums.revenue;
                this.sum_cost = sums.cost;
                this.sum_profit = sums.profit;

                this.taboola_revenue_total = sums.taboola_revenue;
                this.outbrain_revenue_total = sums.outbrain_revenue;

                this.adx_revenue_total = sums.adx_revenue;
                this.hb_revenue_total = sums.hb_revenue_dfp;

                this.adsense_dfp_revenue_total = sums.ad_sense_revenue_dfp;
                this.adsense_analytics_revenue_total = sums.ad_sense_mobile_revenue;
                this.ex_revenue_total = sums.ex_revenue;

                this.sum_campaigns = data.length;
                this.sum_device = this.selected_device != 'All' ? 1 : this.count_values('device', !_filter ? data : this.items);
                this.sum_source = this.selected_campaign_source != 'All' ? 1 : this.count_values('source', !_filter ? data : this.items);

                this.count_sites = this._count_sites();
                this.wavg_clicks_ctr = this._wavg('clicks', 'ctr');
                this.wavg_clicks_pages_session = this._wavg('clicks', 'pages_session');
                this.wavg_bounce_rate = this._wavg('clicks', 'bounce_rate');
                this.wavg_clicks_roi_current = this._wavg('clicks', 'roi_current');
                this.avg_us = this._avg('us');
                this.avg_br = this._avg('br');

                this.losing_campaigns_count = _.filter(data, function (o) {
                    if (o.alert == '1') return o
                }).length;

                this.emptySummary = true;

                const est = moment().tz('America/New_York').format("YYYY-MM-DD HH:mm");
                const start = moment(new Date(est));
                this.bidder = moment(new Date(start));
            },
            campaign_show(cfg) {
                localStorage.campaign_show = cfg;
            },
        }
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

<style scoped>
    /deep/ .ant-input-number-handler-wrap {
        opacity: 1 !important;
    }

    .time {
        width: 140px
    }

    .not-visibale {
        visibility: hidden;
    }

    .hourglass {
        -webkit-animation-name: pour, spin;
        -webkit-animation-duration: 4s;
        -webkit-animation-timing-function: ease-in-out;
        -webkit-animation-iteration-count: infinite;
        animation-name: pour, spin;
        animation-duration: 5s;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
        border: rgba(170, 180, 70, 0) 1em solid;
        border-radius: 20%;
        -moz-border-radius: 20%;
        display: inline-block;
        margin-left: 13px;
        font-family: 'Share Tech', sans-serif;
        font-size: 0.5em;
        color: #069;
    }

    .la-tooltip {
        border-radius: 4px;
        background: rgba(0, 0, 0, 0.8);
        top: -60px !important;
    }

    .la-title {
        padding: 10px;
        color: #fafafa;
    }

    .list {
        list-style: none;
        display: flex;
        padding-left: 0 !important;
    }

    .list li {
        padding: 5px 10px;
        flex: 1;
        color: #fff;
        margin: 0;
        min-width: 90px;
    }

    .list li::before {
        content: none;
    }

    .la-label {
        color: #FAFAFA;
    }

    .la-value {
        color: #FAFAFA;
    }

    ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }

    .isDisabled {
        pointer-events: none;
    }

    td {
        vertical-align: middle !important;
        padding: 8px !important;
    }

    .smrtbid {
        /*text-decoration: line-through;*/
    }

    .smrtbidroi {
        text-decoration: line-through;
    }

    .sb {
        color: red;
    }

    p {
        margin-bottom: 0px;
    }

    .tdWidth {
        min-width: 157px;
    }

    .roi_span {
        display: inline-block;
        width: 45px;
        height: 20px;
        line-height: 15px;
    }

    .float_right {
        float: right;
    }

    @import "../../../node_modules/vuetify/dist/vuetify.min.css";
    @import "../../assets/styles/pages/_CampaignData.scss";
</style>
