<template>
    <div id="medium_key" ref="medium_key">
        <div class="row">
            <div class="col-xs-1" style=" padding-left: 7px;width:auto">
               
                <el-tooltip placement="right" effect="light">
                 <div slot="content">
                        <span style="color: black">{{item_selected.name}}</span>
                   </div>
                    <v-btn @click="showCampaigns()" color="info" dark>
                        <v-icon dark left>arrow_back</v-icon>
                        Campaigns ({{this.item_selected.campaign_id}})
                    </v-btn>
                </el-tooltip>
            </div>
            <div class="col-xs-1" style=" padding-left: 7px;width:auto">
            <el-col :xl="2" style="margin-left: 6px;float:unset !important;">
             
                <v-menu full-width offset-y :close-on-content-click="false" bottom v-model="dateMenu">
                    <v-btn color="primary" outline slot="activator">{{ date_filter[0] }} &mdash; {{ date_filter[1] }}
                    </v-btn>
                    <v-card>
                        <v-card-text>
                            <v-daterange highlight-colors="blue-grey" :options="dateRangeOptions"
                                         @input="onDateRangeChange"/>
                            <v-btn text color="info" @click="submitDateRangeChange">OK</v-btn>
                        </v-card-text>
                    </v-card>
                </v-menu>
            </el-col>
            </div>
                                                                                                                                                           
            <!-- v-show="!roiviews_hide" -->
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
  
        <div  class="col-xs-1" style=" padding-left: 7px;width:auto;margin-top: 0px;"> 
                    <v-btn color="info" dark style="pointer-events: none;">
                        <strong>{{this.item_selected.device}}</strong>
                    </v-btn>
            </div>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    
            <div  class="col-xs-1" style=" padding-left: 7px;width:auto;margin-top: 0px;"> 
                    <v-btn color="info" dark style="pointer-events: none;">
                        <strong>{{this.country_name}}</strong> 
                     </v-btn>  
            </div>

       
            <div class="col-xs-1" style="float: right !important;margin-right: 100px;display: flex;">
                <div v-if="item_selected.status =='IN_PROCESS'" style="padding-top: 15px;">
                    <i class="hourglass mleft"></i>
                </div>
                <div v-if="(item_selected.source === 'revcontent' || item_selected.source === 'taboola' || item_selected.source === 'gemini' || item_selected.source === 'facebook' || item_selected.source === 'zemanta' || item_selected.source === 'outbrain') && item_selected.enable != '0'">
                    <v-btn @click="deleteNotice" :disabled="stop_campaign" color="error" style="line-height: normal">
                        Stop Campaign
                        <v-icon dark right>block</v-icon>
                    </v-btn>
                </div>
                <div v-else-if="(item_selected.source == 'revcontent' || item_selected.source == 'taboola' || item_selected.source == 'zemanta' || item_selected.source == 'outbrain')">
                    <v-btn @click="enableNotice" :disabled="stop_campaign" color="success" style="line-height: normal">
                        Enable Campaign
                        <v-icon dark right>redo</v-icon>
                    </v-btn>
                </div>
            </div>
        </div>

        <br>
        <el-tabs type="card" class="tab" v-model="activeName" @tab-click="tabClick">
            <el-tab-pane label="Mediums" name="medium"></el-tab-pane>
            <el-tab-pane label="Increase Pageviews" name="page_views"></el-tab-pane>
            <el-tab-pane v-if="show_hourly_tab" label="Hourly Roi" name="hourly_roi"></el-tab-pane>
        </el-tabs>

        <div>
            <div v-show="!medium_hide">
                <div v-loading="medium_load">
                    <search-box @selectFilter="selectMediumFilter($event)"></search-box>

                    <div v-if="losing_campaigns_count > 0 && item_selected.source == 'taboola'"
                         :class="[$vuetify.breakpoint.lgAndDown ? 'col-xs-2' : 'col-xs-1', 'top']"
                         style="padding-top:7px">

                    </div>

                    <!--ACTIONS BUTTON-->
                    <div v-if="item_selected.source == 'taboola' && checked_mediums.length > 0" class="col-xs-1"
                         style="padding-top:12px;padding-left:0px;">
                        <el-popover placement="right-end" width="210" trigger="click">

                            <!--BID ADJUST -->
                            <el-popover placement="right" width="200" trigger="click" v-model="bidAdjustView">
                                <div class="pop-div">
                                    <el-input-number controls-position="right" class="edit_bid" :max="100" :min="-98"
                                                     :step="10" size="small" v-model="bulk_bid_mod_change"
                                                     :disabled="stop"></el-input-number>
                                    <el-tag class="percent" type="gray" color="transparent"><i
                                            class="fa fa-percent"></i></el-tag>
                                    <br>
                                    <i @click="adjustNotice(checked_mediums,'bidAdjust' , 'mod',bulk_bid_mod_change)"
                                       :class="[stop ? 'not-active' : '', 'el-icon-circle-check link mg-l green-label']"
                                       style="margin-left:-5px;"><span
                                            style="font-family:sans-serif;">&nbspAccept</span></i>
                                    <span @click="adjustNotice(checked_mediums,'bidAdjust' , 'default')"
                                          class="link default">|  Default</span>
                                </div>
                                <el-button class="btn-width" type="primary" slot="reference"
                                           @click="roiAdjustView=false">BID ADJUST<i class="fas fa-dice"
                                                                                     style="float:right;"></i>
                                </el-button>
                            </el-popover>


                            <!--ADJUST ROI-->
                            <el-popover placement="right" width="200" trigger="click" v-model="roiAdjustView">
                                <div class="pop-div">
                                    <el-input-number controls-position="right" class="edit_bid" :max="2" :min="0"
                                                     :step="0.1" size="small" @change="selectAllRoiChange"
                                                     v-model="roi_adjust" :disabled="stop"></el-input-number>
                                    <br>
                                    <i @click="adjustNotice(checked_mediums,'roiAdjust')"
                                       :class="[stop ? 'not-active' : '', 'el-icon-circle-check link mg-l green-label']"
                                       style="margin-left:10px;"><span
                                            style="font-family:sans-serif;">&nbspAccept</span></i>
                                </div>
                                <el-button class="btn-width" type="warning" slot="reference"
                                           @click="bidAdjustView=false">ROI ADJUST<i class="fas fa-sliders-h"
                                                                                     style="float:right;"></i>
                                </el-button>
                            </el-popover>

                            <!--TOGGLE MEDIUMS -->
                            <el-button class="btn-width" @click="adjustNotice(checked_mediums,'toggle')" type="danger">
                                PAUSE / PLAY<i class="fas fa-ban" style="float:right;"></i></el-button>
                            <el-button type="primary" slot="reference" :loading="bulk_adjust_loading">ACTIONS
                            </el-button>
                            <v-divider></v-divider>
                            <span style="font-weight:bold"> &nbsp&nbsp&nbsp&nbsp Mediums Selected: {{this.checked_mediums.length}}</span>
                        </el-popover>
                    </div>

                    <div class="float_right">
                        <el-tooltip placement="top">
                            <div slot="content">Refresh Mediums Status</div>
                            <v-btn :loading="refreshLoading" @click="refreshScreen()" fab small light color="primary">
                                <v-icon dark>refresh</v-icon>
                            </v-btn>
                        </el-tooltip>
                    </div>
                    <div class="col-lg-12">
                        <cascader ref="cascader" style="padding-bottom: 9px;"></cascader>
                    </div>

                    <table class="table table-striped table-hover">
                        <thead>
                        <tr>
                            <th v-if="item_selected.source == 'taboola'"
                                :class="[taboola_campaign ? 'no-visibility' : '']">
                                <input type="checkbox" v-model="selectAllAction" @change="mediums_index_init">
                            </th>
                            <th v-if="item_selected.source == 'taboola'" @click="headClick(field,key, true)"
                                v-for="field,key in medium_headers_taboola" class="pointer">
                                <strong>{{field.label}}</strong>
                            </th>
                            <th v-if="item_selected.source != 'taboola'" @click="headClick(field,key, true)"
                                v-for="field,key in medium_headers" class="pointer">
                                <strong>{{field.label}}</strong>
                            </th>

                            <th v-if="item_selected.source == 'taboola'">
                                <strong></strong>
                            </th>
                            <th @click="headClick(null,'roi_final', true)" v-if="item_selected.source == 'taboola'"
                                class="pointer">
                                <strong>ROI</strong>
                            </th>
                            <th v-if="item_selected.source == 'taboola'"></th>
                        </tr>
                        </thead>
                        <tbody>

                        <!--site summary start-->
                        <tr v-show="medium_items.length > 0"
                            style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                            <td v-if="item_selected.source == 'taboola'"></td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Number of mediums</div>
                                    <span>{{sum_mediums}}</span></el-tooltip>
                            </td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Weighted Avg. of CTR</div>
                                    <span>{{summary_ctr | _format(3)}}</span>
                                </el-tooltip>
                            </td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Number of clicks</div>
                                    <span>{{summary_clicks}}</span></el-tooltip>
                            </td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Weighted Average UV</div>
                                    <span>{{summary_revenue / summary_clicks | _format(4)}}</span></el-tooltip>
                            </td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Weighted Avg. of P/S</div>
                                    <span :class="[color_summary('pages_session')]">{{summary_ps | _format(2)}}</span>
                                </el-tooltip>
                            </td>
                            <td class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">
                                        Taboola Revenue: {{summary_provider_revenue | _format(2) }}<br/>
                                        Calculated DFP Revenue: {{summary_cdr | _format(2) }}<br/>
                                    </div>
                                    <span>{{summary_revenue | _format(1) }}$</span>
                                </el-tooltip>
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Sum of Cost</div>
                                    <span>{{summary_cost | _format(1)}}</span></el-tooltip>
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Sum of Profit</div>
                                    <span>{{summary_revenue - summary_cost | _format(1)}}</span></el-tooltip>
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                                <el-tooltip placement="top">
                                    <div slot="content">Weighted Avg. of ROI</div>
                                    <span :class="[color_summary('roi')]">{{summary_roi * 100 | _format(1) | prc}}</span>
                                </el-tooltip>
                            </td>
                            <td v-if="item_selected.source == 'taboola'" class="summary">
                            </td>
                        </tr>
                        <!--site summary end-->

                        <tr v-for="(item, index) in _medium_items" v-if="item!==undefined && item.campaign_id!=null"
                            :ref="'m_tr_'+index"
                            :class="[(item.status == 'IN_PROCESS' || item.status == 'PENDING') ? 'event_block':'' , item.alert == 1 && item_selected.source == 'taboola' ? 'tr-losing' : '' ]">
                            <td v-if="item_selected.source == 'taboola'">
                                <input type="checkbox" v-model="selectItems" :value="item" @change="item.index=index"
                                       :disabled="roi_adjust[index] == 0"
                                       :class="[taboola_campaign ? 'no-visibility' : '']">
                            </td>
                            <td>
                                <span>{{item.medium}}</span>
                                <div class="red-label block" v-if="item.source == 'taboola' && item.block == '1'">
                                    <span>(blocked)</span>
                                </div>
                                <!--<i :class="[item.rule_mark == '-1' ? 'el-icon-warning red float_right' : '']"></i>-->
                            </td>
                            <td><span>{{item.ctr | _format(3)}}</span></td>
                            <td>
                                <el-tooltip placement="top">
                                    <div slot="content">
                                        Sessions: {{item.sessions}}
                                    </div>
                                    <span>{{item.clicks}}</span>
                                </el-tooltip>
                            </td>
                            <td>
                                <el-tooltip placement="top">
                                    <div slot="content">
                                        Taboola UV: {{item.taboola_uv | _format(4)}}<br/>
                                        DFP UV: {{item.calculated_dfp_revenue / item.clicks | _format(4) }}<br/>
                                    </div>
                                    <span>{{item.final_uv | _format(4) }}</span>
                                </el-tooltip>
                            </td>
                            <td>
                                <span :class="[color(item, 'pages_session'), 'roi_span']">{{item.pages_session | _format(2) }}</span>
                            </td>
                            <td>
                                <el-tooltip placement="top">
                                    <div slot="content">
                                        Taboola Revenue: {{item.provider_revenue | _format(2) }}<br/>
                                        Calculated DFP Revenue: {{item.calculated_dfp_revenue | _format(2) }}<br/>
                                    </div>
                                    <span>{{item.revenue | _format(2) }}$</span>
                                </el-tooltip>
                            </td>
                            <td v-if="item_selected.source == 'taboola'">
                                <span>{{item.cost | _format(1)}}$</span>
                            </td>
                            <td v-if="item_selected.source == 'taboola'">
                                <span>{{item.profit | _format(2) }}$</span>
                                <span v-if="item.alert == 1"></span>
                                <el-tooltip v-if="item.alert == 1" placement="right">
                                    <div slot="content">This medium has a negetive profit for 3 days in a row !</div>
                                    <i v-if="item.alert == 1" class="fas fa-angle-double-down red-label "
                                       aria-hidden="true"></i>
                                </el-tooltip>
                            </td>
                            <td :class="[expend ? 'diff_bid_expend': 'diff_bid']" v-if="item.source === 'taboola'"
                                style="min-width: 315px">
                                <div class="block" v-if="item.bid && item.bid != 1">
                                    <div :ref="'taboola-'+index">
                                        <el-popover @show="bid_mod_change=calc_percentage_diff(item.bid)"
                                                    placement="top" width="245" trigger="click">
                                            <a-input-number class="budget_input bid_input" size="large"
                                                            @keydown="onlyNumber"
                                                            v-on:keyup="bulk_update_medium_bid_taboola_key_press($event, item, 'mod', bid_mod_change, index)"
                                                            v-model="bid_mod_change"
                                                            :max="100" :min="-98" :step="10"
                                                            :disable="stop"
                                                            :formatter="value => formatCurrency(value)"
                                                            :parser="value => value.replace(/[%]/g, '')"
                                            />
                                            <p v-if="item.bid != '1'"
                                               @click="bulk_update_medium_bid_taboola(item,'default',0,index)"
                                               class="link campaign_roi_adjust">Set Default</p>

                                            <div slot="reference">
                                                <div v-if="item.bid_currency && item_selected.br != 0"
                                                     @mouseover="item.bid_currency = false">
                                                    <span class="link">{{calc_percentage_diff(item.bid)}}%</span>
                                                    <span class="link">(${{calc_percentage(item.bid / brl_currency) | _format(3) }})</span>
                                                </div>

                                                <div v-else-if="item_selected.br != 0"
                                                     @mouseleave="item.bid_currency = true">
                                                    <span class="link">{{calc_percentage_diff(item.bid)}}%</span>
                                                    <span class="link">(R${{calc_percentage(item.bid) | _format(3) }})</span>
                                                </div>

                                                <div v-if="item_selected.br == 0"
                                                     @mouseleave="item.bid_currency = true">
                                                    <span class="link">{{calc_percentage_diff(item.bid)}}%</span>
                                                    <span class="link">(${{calc_percentage(item.bid) | _format(3) }})</span>
                                                </div>
                                            </div>

                                            <div class="text-xs-center">
                                                <v-btn @click="bulk_update_medium_bid_taboola(item, 'mod', bid_mod_change, index)"
                                                       round color="success" dark>Save
                                                </v-btn>
                                            </div>
                                        </el-popover>
                                    </div>
                                </div>
                                <div class="block" v-else>
                                    <div :ref="'taboola-'+index">
                                        <el-popover placement="top" width="245" trigger="click">
                                            <a-input-number class="budget_input bid_input" size="large"
                                                            @keydown="onlyNumber"
                                                            v-on:keyup="bulk_update_medium_bid_taboola_key_press($event, item, 'mod', bid_mod_change2, index)"
                                                            v-model="bid_mod_change2"
                                                            :max="100" :min="-98" :step="10"
                                                            :disable="stop"
                                                            :formatter="value => formatCurrency(value)"
                                                            :parser="value => value.replace(/[%]/g, '')"/>

                                            <p v-if="item.bid != '1'"
                                               @click="bulk_update_medium_bid_taboola(item,'default',0,index)"
                                               class="link campaign_roi_adjust">Set Default</p>

                                            <div slot="reference">
                                                <span v-if="item.bid_currency && item_selected.br != 0"
                                                      @mouseover="item.bid_currency = false" class="link"
                                                      v-model="cpc_modification">default (${{item_selected.bid / brl_currency | _format(3) }})</span>
                                                <span v-else-if="item_selected.br != 0"
                                                      @mouseleave="item.bid_currency = true" class="link"
                                                      v-model="cpc_modification">default (R${{item_selected.bid ? item_selected.bid : item_selected.avg_cpc | _format(3) }})</span>
                                                <span v-if="item_selected.br == 0" class="link"
                                                      v-model="cpc_modification">default (${{item_selected.bid ? item_selected.bid : item_selected.avg_cpc | _format(3) }})</span>
                                            </div>

                                            <div class="text-xs-center">
                                                <v-btn @click="bulk_update_medium_bid_taboola(item,'mod',bid_mod_change2,index)"
                                                       round color="success" dark>Save
                                                </v-btn>
                                            </div>
                                        </el-popover>
                                    </div>
                                </div>
                                <div style="float: right;">
                                    <el-button size="small"
                                               @click="bulk_update_medium_bid_taboola(item,'down',0, index)"
                                               :disabled="stop">-10%
                                    </el-button>
                                    <el-button size="small" @click="bulk_update_medium_bid_taboola(item,'up',0, index)"
                                               :disabled="stop">+10%
                                    </el-button>
                                </div>
                            </td>
                            <td v-if="(item.source === 'taboola' || item.source === 'revcontent')">
                                <el-button size="small" @click="bulk_update_medium_status(item,index)" :disabled="stop">
                                    <i :class="[item.block == '0' || item.block == '-1' ? 'fa fa-ban red-label' : item.block == '1' ? 'fa fa-undo green-label auto check-small' : '']"></i>
                                </el-button>
                            </td>
                            <td style="width: 1px" v-if="item.source === 'taboola'">
                                <span :class="[color(item, 'roi', item.roi_final),'roi_span']">{{item.roi_final | format_prc}}%</span>
                            </td>
                            <td v-if="item_selected.source == 'taboola'">
                                <div v-if="item.status =='DONE'">
                                    <i class="fa fa-check-square green-label mleft"></i>
                                </div>
                                <div v-else-if="item.status =='IN_PROCESS' || item.status =='PENDING'">
                                    <div class="hourglass mleft"></div>
                                </div>
                                <div v-else-if="item.status =='ERROR'">
                                    <i class="fa fa-exclamation red-label mleft"></i>
                                </div>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    <div v-show="!stop" class="col-md-11 text-center">
                        <b-pagination size="md" :total-rows="this.medium_items.length" :per-page="perPage"
                                      v-model="medium_currentPage"/>
                    </div>
                </div>
                <div :class="[$vuetify.breakpoint.lgAndDown ? 'col-xs-2' : 'col-xs-1', 'top']">
                    <el-input-number :options="options" size="small" v-model="mperPage" controls-position="right"
                                     :step="5"></el-input-number>
                </div>
            </div>
            <div v-loading="inpage_load">
                <div v-show="!ipageviews_hide">

                <search-box @selectFilter="selectInpageFilter($event)"></search-box>
                <div class="top col-xs-2" style="padding-top: 32px">
                    <el-tooltip class="item" effect="dark" content="Per Page" placement="top-start">
                        <el-input-number size="small" v-model="perPage" controls-position="right" :min="5"
                                         :step="5"></el-input-number>
                    </el-tooltip>
                </div>



                    <table class="table table-striped table-hover">
                        <thead>
                        <tr>
                            <th
                                    @click="headClick(field,key, true)"
                                    :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"
                                    v-for="field,key in ipageviews_headers">
                                <strong>{{field.label}}</strong>
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(item, index) in _ipageviews_items" v-if="item!==undefined">
                            <td>
                            <span>{{item.page_title}}</span>
                            </td>
                            <td>
                                <a :href="item.page | get_link(saved_site_id)" target="_blank">
                                    <span>{{item.page}}</span>
                                </a>
                            </td>
                            <td>
                                <span>{{item.avg_time| _time_format()}} </span>
                            </td>
                            <td>
                                <span>{{item.exit_rate | _format(3)}}</span>
                            </td>
                            <td>
                                <span>{{item.pageviews}}</span>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    <div v-show="!ipageviews_hide" class="col-md-11 text-center">
                        <b-pagination size="md" :total-rows="ipageviews_items.length" :per-page="perPage"
                                      v-model="ipageviews_currentPage"/>
                    </div>
                </div>
            </div>
            <div v-loading="roi_load">
                <div v-show="!roiviews_hide">
                    <table class="table table-striped table-hover">
                        <thead>
                        <tr>
                            <th
                                    @click="headClick(field,key, true)"
                                    :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"
                                    v-for="field,key in roiviews_headers">
                                <strong>{{field.label}}</strong>
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                              <tr v-if="_roi_items.length > 0"
                                style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                          <td style="width: 92px;">            
                                
                            </td> 
                              <td style="width: 92px;">            
                                <span>Total</span>
                            </td> 
                              <td style="width: 92px;">            
                                <!-- <span>N/A</span> -->
                              </td> 
                            <td style="width: 92px;">
                             
                                <span v-if="!(sum_of_revenue / sum_of_cost)">N/A</span>
                                <span v-else>{{sum_of_revenue / sum_of_cost | _format(2)}}</span>
                            </td>
                        
                            <td style="width: 92px;">            
                                <span  v-if="!sum_of_clicks">N/A</span>
                                <span  v-else>{{ sum_of_clicks | _format_n()}}</span>
                            </td>  
                            <td style="width: 92px;">            
                                <span  v-if="!sum_of_revenue">N/A</span>
                               
                                <span v-else>{{sum_of_revenue | _format(2)}}</span>

                            </td>  
                            <td style="width: 92px;">            
                                <span  v-if="!sum_of_cost">N/A</span>
                                <span  v-else>{{ sum_of_cost | _format(2)}}</span>
                            </td>  
                            <td style="width: 92px;">            
                                <span  v-if="!sum_of_profit">N/A</span>
                                <span  v-else>{{ sum_of_profit | _format(2)}}</span>
                            </td>  
                          
                          
                            <td style="width: 92px;">
                                <span v-if="!sum_of_clicks">N/A</span>
                                <span v-else-if="!(sum_of_revenue / sum_of_clicks)">N/A</span>
                                <span v-else>{{sum_of_revenue / sum_of_clicks | _format(4)}}</span>
                            </td>
                             <td style="width: 92px;">
                                <span v-if="!sum_of_clicks">N/A</span>
                                <span v-else-if="!(sum_of_cost / sum_of_clicks)">N/A</span>
                                <span v-else>{{sum_of_cost / sum_of_clicks | _format(4)}}</span>
                               
                            </td>                  

                        </tr>
                         <tr v-for="(item, index) in _roi_items" v-if="item!==undefined">
                            <td style="width: 92px;">
                            <span>{{ item.data_date | formatDate }}</span>
                            </td>
                            <td style="width: 92px;">
                                <span>NA</span>
                            </td>
                            <td style="width: 92px;">
                                <span>NA</span>                            
                            </td>
                            <td style="width: 92px;">
                                <span v-if="!item.cost">N/A</span>
                                <span v-else-if="!(item.revenue / item.cost)">N/A</span>
                                <span v-else>{{item.revenue / item.cost | _format(2)}}</span>
                                                     
                            </td>
                            <td style="width: 92px;">
                                <span>{{item.clicks | _format_n()}}</span>                        
                            </td>
                            <td style="width: 92px;">
                                <span>{{item.revenue | _format(2)}}</span>
                            </td> 
                            <td style="width: 92px;">
                                <span>{{item.cost | _format(2)}}</span>
                            </td> 
                            <td style="width: 92px;">
                                <span>{{item.profit | _format(2)}}</span>
                            </td>
                            <td style="width: 92px;">
                                <span v-if="!item.clicks">N/A</span>
                                <span v-else-if="!(item.revenue / item.clicks)">N/A</span>
                                <span v-else>{{item.revenue / item.clicks | _format(4)}}</span>
                            </td>
                             <td style="width: 92px;">
                                <span v-if="!item.clicks">N/A</span>
                                <span v-else-if="!(item.cost / item.clicks)">N/A</span>
                                <span v-else>{{item.cost / item.clicks | _format(4)}}</span>
                               
                            </td>
                        </tr>
                   
                        <tr v-if="_roi_items.length == 0"
                                style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                         
                              <td style="width: 92px;text-align: center;" colspan="10" >            
                                <span>No Records Found</span>
                            </td> 
                        </tr>
                        </tbody>
                    </table>
                     <div v-if="_roi_items.length > 0" class="col-md-11 text-center">
                        <b-pagination size="md" :total-rows="roi_items.length" :per-page="perPage"
                                      v-model="roi_currentPage"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment-timezone';
    import alerts from "../mixins/alerts";

    export default {
        name: 'medium_key',
        mixins: [alerts],
        components: {
            "charts": require("./Charts.vue").default,
            "cascader": require("../Cascader.vue").default
        },
        data() {
            return {
                sum_of_final_roi: [],
                sum_of_clicks: [],
                sum_of_revenue: [],
                sum_of_cost: [],
                sum_of_profit: [],
                items: [],
                colors: [],
                checked_mediums: [],
                _items: [],
                inited_summary: {},
                medium_items_copy: [],
                losing_campaigns_count: 0,
                websites: [],
                medium_items: [],
                roi_items: [],
                ipageviews_items: [],
                inpage_filter: '',
                medium_block_items: [],
                campaigns_items: [],
                date_filter: [],
                tab_init: [],
                options: [{text: 5, value: 5}, {text: 10, value: 10},
                    {text: 15, value: 15},
                    {text: 20, value: 20},
                    {text: 25, value: 25},
                    {text: 30, value: 30}],
                medium_headers_taboola: {
                    medium: {label: 'Medium', sortable: true},
                    ctr: {label: 'creative CTR', sortable: true},
                    clicks: {label: 'Clicks', sortable: true},
                    final_uv: {label: 'UV', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    revenue: {label: 'Revenue', sortable: true},
                    cost: {label: 'Cost', sortable: true},
                    profit: {label: 'Profit', sortable: true},
                    bid: {label: 'CPC Bid', sortable: true}
                },
                medium_headers: {
                    medium: {label: 'Medium', sortable: true},
                    ctr: {label: 'creative CTR', sortable: true},
                    clicks: {label: 'Clicks', sortable: true},
                    final_uv: {label: 'UV', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    revenue: {label: 'Revenue', sortable: true}
                },
                ipageviews_headers: {
                    page_title: {label: 'Page title', sortable: true},
                    page: {label: 'Page URL', sortable: true},
                    avg_time: {label: 'Avg time', sortable: true},
                    exit_rate: {label: '% Exit', sortable: true},
                    pageviews: {label: 'Page views', sortable: true},
                },
                roiviews_headers: {
                        data_date: {label: 'Hour', sortable: true},
                        target_roi: {label: 'Target roi', sortable: true},
                        target: {label: 'Target', sortable: true},
                        final_roi: {label: 'Final roi', sortable: true},
                        clicks: {label: 'Clicks', sortable: true},
                        revenue: {label: 'Revenue', sortable: true},
                        cost: {label: 'Cost', sortable: true},
                        profit: {label: 'Profit', sortable: true},
                        uv: {label: 'UV', sortable: true},
                        avg_uc: {label: 'Avg Cpc', sortable: true},
                },
                dateRangeOptions: {
                    startDate: moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    endDate: moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    format: 'MM/DD/YYYY',
                },
                perPage: 20,
                mperPage: 30,
                rperPage: 20,
                medium_currentPage: 1,
                ipageviews_currentPage: 1,
                roi_currentPage: 1,
                brl_currency: 1,
                medium_star_count: 0,
                step: 0.01,
                roi_adjust: 1.3,
                sort: null,
                taboola_campaign: false,
                dateMenu: false,
                hide: false,
                sortFlag: false,
                medium_filter: null,
                medium_hide: true,
                ipageviews_hide: true,
                roiviews_hide: true,
                sortDesc: true,
                stop: false,
                sync: false,
                editable: false,
                index_edit: false,
                bid_mod_index: false,
                budget: false,
                expend: false,
                medium_load: true,
                inpage_load:false,
                roi_load:false,
                stop_campaign: false,
                disable_reload: false,
                bulk_update: false,
                roi_adjust_update: false,
                roi_apply: false,
                bulk_adjust_loading: false,
                refreshLoading: false,
                bidAdjustView: false,
                roiAdjustView: false,
                loadingbtn: false,
                activeName: 'medium',
                device_selected: '',
                source_selected: '',
                item_selected: '',
                site_id: '',
                saved_site_id: '',
                campaign_id: '',
                campaign_id_value: '',
                date_start: '',
                date_end: '',
                avg_cpc: '',
                bid_mod_change: 0,
                bid_mod_change2: 0,
                summary_ctr: 0,
                sum_mediums: 0,
                summary_clicks: 0,
                summary_ps: 0,
                summary_cdr: 0,
                summary_provider_revenue: 0,
                summary_roi: 0,
                summary_revenue: 0,
                summary_cost: 0,
                page_summary_avg_time: 0,
                bulk_bid_mod_change: '',
                cpc_modification: '',
                country_name: '',
                req_action: '',
                roi_adjust_input_length: null,
                show_hourly_tab: this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.hourly_roi == 1
            }
        },
        methods: {
            selectInpageFilter(filter) {
                this.inpage_filter = filter;
            },
            selectMediumFilter(filter) {
                this.medium_filter = filter;
            },
            initializeView(item, items, websites, site_id, date_start, date_end, source, device) {
                this.items = items;
                this.item_selected = item;
                this.websites = websites;
                this.date_start = date_start;
                this.date_end = date_end;
                this.date_filter = [date_start, date_end];
                this.campaign_id = item.campaign_id + ' - ' + item.name;
                this.campaign_id_value = item.campaign_id;
                this.site_id = item.site_id;
                this.saved_site_id = site_id;
                this.avg_cpc = item.bid;
                this.budget = item.budget;
                this.bid_mod_change = 0;
                this.bid_mod_change2 = 0;
                this.bulk_bid_mod_change = '';
                this.device_selected = device;
                this.source_selected = source;
                this.medium_hide = false;
                this.ipageviews_hide = true;
                this.roiviews_hide = true;
                this.factor = item.factor;
                this.brl_currency = this.$store.getters.getCurrency;
                this.inpage_filter = '';
                this.taboola_campaign = (this.item_selected.source != 'taboola') || (this.item_selected.source == 'taboola' && this.item_selected.clicks <= 0);

                setTimeout(() => {
                    this.get_colors({'device': 'all', 'source': item.source, 'page_type': 'medium'});
                }, 1);
                this.initializeData(item, date_start, date_end);
                if (this.item_selected.country) {
                  const country = JSON.parse(this.item_selected.country);
                  if (this.item_selected.source === 'taboola') {
                    if (country.type.includes('exclude')) {
                      this.country_name = 'Worldwide';
                    } else {
                      this.country_name = country.value.join('/');
                    }
                  }else if (this.item_selected.source === 'zemanta'){
                    if (country['excluded']['countries'].length > 0) {
                      this.country_name = 'Worldwide';
                    } else {
                      this.country_name = country['included']['countries'].join('/');
                    }
                  }else if (this.item_selected.source === 'outbrain'){
                    if (country.length === 0 ) {
                      this.country_name = 'Worldwide';
                    } else {
                       this.country_name = country.map(element => element.code).join('/');
                    }
                  }
                }else{
                  this.country_name = 'N/A';
                }
            },
            initializeRoiData() {
                let item = this.items;
                let date_start = this.date_start;
                let date_end = this.date_end;
                let site = this.site_id ? this.site_id : null;
                let campaign_id = this.campaign_id_value;
                let start = moment(Array.isArray(date_start) ? date_start[0] : date_start).format("YYYY-MM-DD");
                let end = moment(Array.isArray(date_end) ? date_end[1] : date_end).format("YYYY-MM-DD");

                 let params = {
                    'site': site,
                    'campaign_id': campaign_id,
                    'start_date': start,
                    'end_date' : end,
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.get('/api/reports/get_hourly_roi_data', {params: params}).then(res => {

                    // if (this.datas) {
                        if (res.body.data) {
                        this.sort = false;
                        this._items = Object.keys(res.body.data).map(key => res.body.data[key]);
                        if (this._items.length === 0) {
                            this.warning(req_action.replace("_", " ") + ' data not found');
                            this.hide_load(req_action);
                        }                  
                        this.roi_items = this._items;
                        this.roi_items_copy = this._items;
                        // this.refreshLoading = false;
                        this.roi_load = false;       
                     }  
                });

             
              
            },
            initializeData(item, date_start, date_end, switch_dates, action = 'mediums') {

                if (!item || !date_start || !date_end) {
                    return;
                }

                this.roi_adjust = 1.3;
                this.medium_star_count = 0;
                this.checked_mediums = [];

                if (switch_dates && date_start.length === 0) {
                    return false;
                } else if (switch_dates) {
                    this.date_start = this.date_filter[0];
                    this.date_end = this.date_filter[1];
                }

                let campaign_id = item.campaign_id !== '' ? item.campaign_id : null;
                let device = item.device ? item.device : null;
                let source = item.source ? item.source : null;
                let site_id = this.site_id ? this.site_id : null;
                let start = moment(Array.isArray(date_start) ? date_start[0] : date_start).format("YYYY-MM-DD");
                let end = moment(Array.isArray(date_end) ? date_end[1] : date_end).format("YYYY-MM-DD");

                this.activeName = 'medium';

                this.medium_block_hide = true;
                if (action == 'mediums') {
                    this.medium_load = true;
                }else{
                    this.inpage_load = true;
                }

                let params = {
                    'campaign_id': campaign_id,
                    'device': device,
                    'source': source,
                    'site_id': site_id,
                    'start': start,
                    'end': end
                };

                // let actions = ['mediums', 'inpage'];
                // for (let act of actions) {
                let endpoint = '/api/website/' + action;
                this.get_data(action, endpoint, params);
                // }
            },
            get_data(req_action, endpoint, params, skip) {
                this.$http.get(endpoint, {params: params}).then(res => {
                    if (res.body) {
                        this._items = Object.keys(res.body).map(key => res.body[key]);
                        if (this._items.length === 0) {
                            this.warning(req_action.replace("_", " ") + ' data not found');
                            this.hide_load(req_action);
                        } else if (skip && this.disable_reload) {
                            return;
                        } else if (req_action === 'mediums') {
                            this.medium_items = this._items;
                            this.medium_items_copy = this._items;
                            if (this.item_selected.source == 'taboola') {
                                this.selectAllRoiChange(true)
                            }
                            if (this.$refs.cascader.reapply) {
                                this.$refs.cascader.reapply();
                            }
                            if (!skip) {
                                this.headClick(null, "clicks");
                                this.sortDesc = false;
                                this.medium_load = false;
                                this.inpage_load = false;
                                this.medium_hide = false;
                            }

                        } else if (req_action == 'inpage') {
                            this.inpage_load = false;
                            this.ipageviews_items = this._items
                        }
                        this.refreshLoading = false;
                        if (req_action === 'campaigns') {
                            this.campaigns_items = this._items;
                            if (!skip) {
                                this.campaigns_load = false;
                            }
                        }
                        this.stop = false;

                    } else {
                        this.hide_load(req_action);
                        console.log("---------ERROR-----------");
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
            showCampaigns() {
                window.stop();
                this.$parent.showMediumkey = false;
                this.activeName = '';
                this.medium_items = [];
                this.medium_block_items = [];
                this.checked_mediums = [];
                this.keyword_items = [];
                this.device_items = [];
                this.item_selected = '';
                this.items = [];
                this.index_edit = false;
                this.sync = false;
                this.firstInit = false;
                this.date_filter = [];
                this.device_selected = '';
                this.source_selected = false;
                this.ipageviews_star_count = 0;
                this.country_star_count = 0;
                this.block_medium_star_count = 0;
                this.medium_star_count = 0;
                this.keyword_star_count = 0;
                this.stop_campaign = false;
                this.editable = false;
                this.disable_reload = true;
                this.bulk_adjust_loading = false;
                this.refreshLoading = false;
                this.roi_adjust_update = false;
                this.ad_content_items = [];
                this.ipageviews_items = [];
                this.country_items = [];
                this.tab_init = [];
                this.$parent.highlight();
            },
            stopCampaign() {

                this.stop_campaign = true;
                this.item_selected.status = 'IN_PROCESS';

                let campaign_id = this.item_selected.campaign_id ? this.item_selected.campaign_id : null;
                let site_id = this.site_id ? this.site_id : null;
                let source = this.item_selected.source ? this.item_selected.source : null;

                let params = {
                    'site_id': site_id,
                    'source': source,
                    'campaign_id': campaign_id,
                    'login_time': this.$store.getters.getUser.loginTime,
                };

                this.$http.post('/api/website/stop_campaign', {params: params}).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...', center: true, type: 'success'});
                    } else {
                        this.$alert('Sorry, Error has occurred while trying stop the campaign', ' ', {
                            confirmButtonText: 'OK',
                            type: 'warning'
                        });
                    }
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.$alert('Sorry, Error has occurred while trying stop the campaign', ' ', {
                            confirmButtonText: 'OK',
                            type: 'warning'
                        });
                    }
                });
                const that = this;
                setTimeout(function () {
                    that.check_status_campaign();
                    that.stop_campaign = false;
                }, 10000);
            },
            bulk_update_medium_status(items, index = '') {

                let validKeys = ['action', 'bid', 'medium'];
                this.bulk_adjust_loading = true;

                //Handle single medium
                if (items.length == undefined) {
                    items.index = index;
                    let arr = [];
                    arr.push(items);
                    items = arr;
                }
                let newItems = _.cloneDeep(items);
                this.disable_reload = false;

                // Prepare status per medium
                items.forEach((item) => {
                    item.status = 'IN_PROCESS';

                    if (this.$refs['m_tr_' + item.index]) {
                        this.$refs['m_tr_' + item.index][0].className = "event_block";
                    }
                });

                newItems.forEach((item) => {
                    item.action = 'toggle';
                    item.site_id = this.site_id;
                    item.status = 'IN_PROCESS';
                    item.login_time = this.$store.getters.getUser.loginTime;

                    if (item != newItems[0]) {
                        Object.keys(item).forEach((key) => validKeys.includes(key) || delete item[key]);
                    }
                });

                let endpoint = '';
                if (newItems[0].source === 'taboola') {
                    endpoint = '/api/website/mediums/taboola/bulk';
                } else if (newItems[0].source === 'revcontent') {
                    endpoint = '/api/website/mediums/taboola/bulk';
                }

                this.$http.post(endpoint, newItems).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...', center: true, type: 'success'});
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                    this.bulk_adjust_loading = false;

                    this.checked_mediums = [];
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function () {
                    items.forEach((item) => {
                        that.check_status(item, 'mediums');
                        if (!that.disable_reload) {
                            if (that.$refs['m_tr_' + item.index] != undefined) {
                                if (item.status == 'DONE') {
                                    that.$refs['m_tr_' + item.index][0].className = "";
                                }
                            }
                        }
                    });
                }, 10000);
            },
            bulk_update_medium_bid_taboola(items, action, prcnt = 0.0, index = '') {

                this.bulk_adjust_loading = true;
                let validKeys = ['action', 'bid', 'medium'];

                //Handle single medium
                if (items.length == undefined) {
                    items.index = index;
                    let arr = [];
                    arr.push(items);
                    items = arr;
                }
                let newItems = _.cloneDeep(items);
                this.disable_reload = false;

                // Prepare status per medium
                items.forEach((item) => {
                    item.status = 'IN_PROCESS';
                    if (this.$refs['m_tr_' + item.index]) {
                        this.$refs['m_tr_' + item.index][0].className = "event_block";
                    }
                });

                newItems.forEach((item) => {
                    item.action = 'bid';
                    item.login_time = this.$store.getters.getUser.loginTime;
                    let current_bid = item.bid ? item.bid : 1;
                    let new_bid = current_bid;
                    let _step = 0.1;
                    if (action === "up") {
                        new_bid = Math.round((parseFloat(current_bid) + _step) * 1000) / 1000;
                    } else if (action === "down") {
                        new_bid = Math.round((parseFloat(current_bid) - _step) * 1000) / 1000;
                    } else if (action === "default") {
                        new_bid = 1.0;
                    } else if (action === "mod") {
                        new_bid = (100.0 + parseFloat(prcnt)) / 100.0
                    }

                    if (new_bid > 2.0 || new_bid < 0.02) {
                        this.notice("Bid range is between +100% and -98% , check medium : " + item.medium);
                    }

                    if(new_bid > 2.0){
                        new_bid = 2;
                    }else if(new_bid < 0.02){
                        new_bid = 0.02;
                    }

                    item.bid = new_bid;
                    this.bid = item.bid;
                    item.site_id = this.site_id;
                    item.status = 'IN_PROCESS';

                    if (item != newItems[0]) {
                        Object.keys(item).forEach((key) => validKeys.includes(key) || delete item[key]);
                    }
                });

                this.$http.post('/api/website/mediums/taboola/bulk', newItems).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...', center: true, type: 'success'});
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                    this.bulk_adjust_loading = false;
                    this.checked_mediums = [];
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                this.bid_mod_change = 0;
                this.bid_mod_change2 = 0;
                this.$el.click();

                const that = this;
                setTimeout(function () {
                    items.forEach((item) => {
                        that.check_status(item, 'mediums');
                        if (!that.disable_reload) {
                            if (that.$refs['m_tr_' + item.index] != undefined) {
                                if (item.status == 'DONE') {
                                    that.$refs['m_tr_' + item.index][0].className = "";
                                }
                            }
                        }
                    });
                }, 10000);
            },
            bulk_update_medium_bid_taboola_key_press(e, item, action, bid_mod_change, index) {
                if (e.keyCode === 13) {
                    this.bulk_update_medium_bid_taboola(item, action, bid_mod_change,index);
                }
            },
            applyRoiAdjust() {
                let items = this.checked_mediums;
                this.bulk_adjust_loading = true;
                this.disable_reload = false;

                // Prepare status per medium
                items.forEach((item) => {
                    item.status = 'IN_PROCESS';
                    if (this.$refs['m_tr_' + item.index]) {
                        this.$refs['m_tr_' + item.index][0].className = "event_block";
                    }
                });
                for (let item of items) {
                    // let val = this.checked_mediums[item.index];
                    let val = this.roi_adjust;
                    let cpc_bid = 0;
                    let bid = item.source == 'taboola' ? this.item_selected.bid : this.item_selected.avg_cpc;
                    // Check if BRL
                    if (this.item_selected.br != 0 && item.bid_currency == true) {
                        cpc_bid = (item.final_uv / val) * this.brl_currency;
                    } else {
                        cpc_bid = (item.final_uv / val);
                    }
                    let bid_adjust = (cpc_bid / bid) - 1;
                    if (item.source == 'taboola') {
                        bid_adjust = 1 + bid_adjust;
                        if (bid_adjust > 2) {
                            item.bid_adjust = 2;
                        } else if (bid_adjust < 0.02) {
                            item.bid_adjust = 0.02;
                        } else {
                            item.bid_adjust = bid_adjust;
                        }

                    } else if (item.source == 'revcontent') {
                        item.bid_adjust = Math.floor(target_bid * 100) / 100;
                    }
                    console.log("New bid: " + item.bid_adjust);
                }

                if (this.item_selected.source === 'taboola') {
                    this.AdjustMediumsBulk();
                } else if (this.item_selected.source === 'revcontent') {
                    this.AdjustKeywordsBulk();
                }
            },
            AdjustMediumsBulk() {
                let mediums = this.checked_mediums;
                let newItems = _.cloneDeep(mediums);
                let endpoint = '/api/website/mediums/taboola/bulk';
                let validKeys = ['action', 'bid', 'bid_adjust', 'medium'];

                newItems.forEach((medium) => {
                    medium.status = 'IN_PROCESS';
                    medium.action = 'roi';
                    medium.login_time = this.$store.getters.getUser.loginTime;
                    if (medium != newItems[0]) {
                        Object.keys(medium).forEach((key) => validKeys.includes(key) || delete medium[key]);
                    }
                });

                this.$http.post(endpoint, newItems).then(res => {
                    if (res.body === "True") {
                        this.bulk_adjust_loading = false;
                        this.checked_mediums = [];
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                    this.checked_mediums = [];
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
                const that = this;
                setTimeout(function () {
                    mediums.forEach((medium) => {
                        that.check_status(medium, 'mediums');
                        if (!that.disable_reload) {
                            if (that.$refs['m_tr_' + medium.index] != undefined) {
                                if (medium.status == 'DONE') {
                                    that.$refs['m_tr_' + medium.index][0].className = "";
                                }
                            }
                        }
                    });
                }, 10000);
            },
            AdjustKeywordsBulk() {
                let keywords = this.checked_mediums;
                let newItems = _.cloneDeep(keywords);
                let endpoint = '/api/website/keywords/taboola/bulk';
                let validKeys = ['action', 'bid', 'bid_adjust', 'medium'];

                newItems.forEach((keyword) => {
                    keyword.status = 'IN_PROCESS';
                    if (keyword != newItems[0]) {
                        Object.keys(keyword).forEach((key) => validKeys.includes(key) || delete keyword[key]);
                    }
                });

                this.$http.post(endpoint, newItems).then(res => {
                    if (res.body === "True") {
                        this.bulk_adjust_loading = false;
                        this.checked_mediums = [];
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                    this.checked_mediums = [];
                });
                const that = this;
                setTimeout(function () {
                    keywords.forEach((keyword) => {
                        that.check_status(keyword, 'mediums');
                        if (!that.disable_reload) {
                            if (that.$refs['m_tr_' + keyword.index] != undefined) {
                                if (keyword.status == 'DONE') {
                                    that.$refs['m_tr_' + keyword.index][0].className = "";
                                }
                            }
                        }
                    });
                }, 10000);
            },
            selectAllRoiChange(fast) {
                this.roi_apply = true;
                const that = this;
                setTimeout(function () {
                    for (let i of that.checked_mediums) {
                        i.roi_adjust = that.roi_adjust;
                    }
                    that.roi_apply = false;
                }, fast ? 0 : 500);
            },
            check_status(item, action) {
                let params = {
                    'campaign_id': item.campaign_id,
                    'device': item.device,
                    'source': item.source,
                    'site_id': item.site_id,
                    'start': moment(this.date_start).format("YYYY-MM-DD"),
                 'end': moment(this.date_end).format("YYYY-MM-DD")
                };
                this.get_data(action, '/api/website/' + action, params, true);
            },
            check_status_campaign() {
                let params = this.item_selected;
                this.$http.get('/api/website/check_status', {params}).then(res => {
                    if (res.body) {
                        this.item_selected = Object.keys(res.body).map(key => res.body[key])[0];
                        const campaign_id = this.item_selected.campaign_id;
                        let index = this.items.findIndex(function (element) {
                            return element.campaign_id === campaign_id
                        });
                        this.items[index].status = this.item_selected.status;
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            // losingFilter(toggle) {
            //     if (toggle) {
            //         this.medium_items = _.filter(this.medium_items, function (o) {
            //             return o.alert == 1
            //         });
            //     } else {
            //         this.medium_items = this.medium_items_copy;
            //         return this.medium_items;
            //     }
            // },
            tabClick(tab) {
                if (tab.label.toLowerCase() === "mediums") {
                    this.ipageviews_hide = true;
                    this.medium_hide = false;
                    this.roiviews_hide = true;
                    this.sort = false;
                }
                else if (tab.label.toLowerCase().replace(" ", "_") === "increase_pageviews") {
                    this.inpage_load = true;
                    this.initializeData(this.item_selected, this.date_start, this.date_end, false, 'inpage');
                    this.ipageviews_hide = false;
                    this.medium_hide = true;
                    this.roiviews_hide = true;
                }else if (tab.label.toLowerCase().replace(" ", "_") === "hourly_roi") {


                    this.roi_load = true;
                    // this.refreshLoading = true;
                    this.ipageviews_hide = true;
                    this.medium_hide = true;
                    this.roiviews_hide = false;
                    this.initializeRoiData();
                
                }

            },
            onDateRangeChange(range) {
                this.date_filter = range
            },
            submitDateRangeChange() {
                this.dateMenu = false;
                this.initializeData(this.item_selected, this.date_filter[0], this.date_filter[1], true)
            },
            mediums_index_init() {
                for (let index in this.medium_items) {
                    this.roi_items[index]['index'] = index;
                }
            },
            roi_index_init() {
                for (let index in this.roi_items) {
                    this.medium_items[index]['index'] = index;
                }
            },
        
            headClick(field, key, flag = false) {

                if (flag) this.sortFlag = !this.sortFlag;

                if (key === this.sort) {
                    this.sortDesc = !this.sortDesc;
                }

                this.sort = key;
            },
            open_bid_mod(index) {
                this.expend = true;
                if (this.bid_mod_index >= 0 && this.bid_mod_index !== false) {
                    this.close_bid_mod(this.bid_mod_index, true);
                }
                this.bid_mod_index = index;
                this.bid_mod_change = '';
                this.$refs['taboola-' + index][0].className = this.$refs['taboola-' + index][0].className.replace("tb-hide", "edit_bid");
            },
            close_bid_mod(index, skip) {
                this.expend = !!skip;
                this.bid_mod_index = index;
                this.bid_mod_change = '';
                this.$refs['taboola-' + index][0].className = this.$refs['taboola-' + index][0].className.replace("edit_bid", "tb-hide");
            },
            calc_percentage(bid) {
                let cbid = this.item_selected.bid ? this.item_selected.bid : this.item_selected.avg_cpc;
                let round_cpc = Math.round(cbid * 1000) / 1000;
                let res = round_cpc * bid;
                return Math.round(res * 1000) / 1000;
            },
            calc_percentage_diff(item) {
                let prcnt = item * 100;
                return parseFloat(item) < 1 ?
                    "-" + (Math.round((100 - prcnt) * 1000) / 1000).toString() :
                    "+" + (Math.round((prcnt - 100) * 1000) / 1000).toString();
            },
            deleteNotice() {
                this.$confirm('This action will stop the campaign. Continue?', 'Warning', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    this.stopCampaign();
                })
            },
            adjustNotice(items, action = 'roiAdjust', mode = '', bid = 0) {
                let msg = '';
                let msgEnd = ", Continue ? Please note, maximum bid changes will be between +100% and -98%, we advise you to check the new bid after applying";
                let type = this.item_selected.source == 'taboola' ? 'mediums' : 'keywords';
                let item = this.checked_mediums[0];
                if (action == 'roiAdjust') {
                    if (items.length == 1) {
                        let val = this.roi_adjust;
                        msg = "You are about to adjust ROI on medium " + item.medium + " from " + parseInt(item.roi * 100) + "% to " + parseInt(val * 100) + "%"
                    }
                    if (items.length > 1) {
                        msg = "You are about to adjust ROI " + items.length + " " + type + " to " + parseInt(this.roi_adjust * 100) + "%"
                    }
                } else if (action == 'bidAdjust') {
                    if (mode == 'default') {
                        if (items.length == 1) {
                            msg = "You are to adjust bid on medium " + item.medium + " with default value 1.0"
                        }
                        else {
                            msg = "You are about to adjust bid for " + items.length + " " + type + " with default value 1.0"
                        }
                    } else {
                        if (items.length == 1) {
                            msg = "You are about to adjust bid on medium " + item.medium + " to " + parseInt(bid) + "% bid"
                        }
                        else {
                            msg = "You are about to adjust bid for " + items.length + " " + type + " to " + parseInt(bid) + "%"
                        }
                    }
                } else if (action == 'toggle') {
                    if (items.length == 1) {
                        msg = "You are about to toggle medium " + item.medium + " Continue ? "
                    }
                    else {
                        msg = "You are about to toggle " + items.length + " " + type + ", Continue ? "
                    }
                }
                if (action != 'toggle') {
                    msg = msg + msgEnd;
                }
                this.$confirm(msg, 'Warning', {
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                    center: true,
                    customClass: 'roi_notice_msg'
                }).then(() => {
                    this.$message({
                        type: 'success',
                        message: 'Action in process',
                        center: true
                    });
                    if (action == 'roiAdjust') {
                        this.applyRoiAdjust();
                    } else if (action == 'bidAdjust') {
                        this.bulk_update_medium_bid_taboola(items, 'mod', bid);
                    } else if (action == 'toggle') {
                        this.bulk_update_medium_status(items)
                    }
                }).catch(() => {
                    this.$message({
                        type: 'warning',
                        message: 'Action canceled',
                        center: true
                    });
                });
            },
            formatCurrency(val) {
                return val == '' ? val : val + '%';
            },
            enableNotice() {
                this.$confirm('This action will enable the campaign. Continue?', 'Warning', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    this.stopCampaign();
                }).catch(() => {

                });
            },
            hide_load(typ) {
            
                if (typ === 'mediums') {
                    this.medium_load = false;
                    this.medium_hide = true;
                }else{
                    this.inpage_load = false;
                    this.ipageviews_hide = true;

                }
            },
            success(msg) {
                this.$notify({
                    title: 'Sync',
                    message: msg,
                    type: 'success'
                });
            },
            warning(msg) {
                this.$notify({
                    title: 'Warning',
                    message: msg,
                    type: 'warning'
                });
            },
            cascaderFilter(query, scope, remove, remove_all, current_filters = []) {
                if (remove_all) {
                    scope.$data.medium_items = scope.$data.medium_items_copy;
                    scope.$data.hide = scope.$data.medium_items.length > 0 ? false : true;
                    return;
                }

                let actions = ['losing', 'landing', 'exceeded', 'creation', 'automation'];

                if (remove || (current_filters && !query && !remove && !remove_all)) {

                    if (remove && scope.$refs.cascader.labels.indexOf(remove.label) > -1) {
                        scope.$refs.cascader.labels = [];
                    }

                    if (current_filters.length == 0) {
                        scope.$data.medium_items = scope.$data.medium_items_copy;
                        return;
                    }

                    let filtered_items = scope.$data.medium_items_copy;
                    for (let i of current_filters) {
                        if (i.type == 'less') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] < i.amount;
                            });
                        } else if (i.type == 'greater') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] > i.amount;
                            });
                        } else if (i.type == 'between') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] > i.amount && o[i.field] < i.between;
                            });
                        } else if (i.type == 'losing') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] == '1';
                            });
                        } else if (i.type == 'automation') {
                            filtered_items = _.filter(filtered_items, function (o) {
                                return o[i.field] == '1';
                            });
                        } else {
                            filtered_items = this.cascaderFilterExtend(i, filtered_items);
                        }
                    }

                    scope.$data.medium_items = filtered_items;
                    scope.$data.hide = filtered_items.length > 0 ? false : true;
                }

                else if (!remove && !remove_all && !actions.includes(query.type)) {
                    query.amount = parseFloat(query.amount);
                    if (query.type == 'less') {
                        scope.$data.medium_items = _.filter(scope.$data.medium_items, function (o) {
                            return o[query.field] < query.amount;
                        });
                    } else if (query.type == 'greater') {
                        scope.$data.medium_items = _.filter(scope.$data.medium_items, function (o) {
                            return o[query.field] > query.amount;
                        });
                    } else if (query.type == 'equals') {
                        scope.$data.medium_items = _.filter(scope.$data.medium_items, function (o) {
                            return o[query.field] > query.amount - 0.01 && o[query.field] < query.amount + 0.01;
                        });
                    } else if (query.type == 'between') {
                        scope.$data.medium_items = _.filter(scope.$data.medium_items, function (o) {
                            return o[query.field] > query.amount && o[query.field] < query.between;
                        });
                    }
                }

                else if (query) {
                    scope.$data.medium_items = this.cascaderFilterExtend(query, scope.$data.medium_items);
                }

                if (current_filters.length > 0 && !query && scope.$data.medium_items.length == 0 && !remove && !remove_all) {
                    scope.$data.disabled = false;
                }
            },
            cascaderFilterExtend(query, items) {
                if (query.type == 'losing') {
                    return _.filter(items, function (o) {
                        return o[query.field] == '1';
                    });
                }

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
            refreshScreen() {
                this.refreshLoading = true;
                this.submitDateRangeChange();

            },
            filter_summary() {
                let items = this.medium_items;
                const fix = v => {
                    if (v instanceof Object) {
                        return ['medium'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                if (this.medium_filter && this.medium_filter.length > 0) {
                    this.medium_filter = this.medium_filter.trim().toLowerCase();
                    const regex = new RegExp('.*' + this.medium_filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                }
                return items;
            },
            _wavg(w, v) {
                let data = this.filter_summary();
                let res = ((_w, _v) => _v / _w)(...data.reduce((r, o) => [r[0] + o[w], r[1] + o[w] * o[v]], [0, 0]));
                if (res != undefined) {
                    this.inited_summary[v] = res;
                    return res;
                }
            },
            count_values(key, data) {
                return Object.keys(data.reduce((acc, o) => (acc[o[key]] = (acc[o[key]] || 0) + 1, acc), {})).length;
            },
           
            color_summary(key) {
                if (this.inited_summary[key] != undefined) {
                    if (key == 'color_summary') {
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
                    } else if (key == 'roi' && this.inited_summary[key]) {
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
            onlyNumber($event) {
                let evt = ($event) ? $event : window.event;
                let charCode = (evt.which) ? evt.which : evt.keyCode;

                if ([8, 9, 13, 27, 45, 46, 109, 110, 173, 189, 190].indexOf(charCode) !== -1 ||
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
        },
        computed: {
        _roi_items() {
                if (!this.roi_items) {
                    return [];
                }

                let roi_items = this.roi_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return ['roi'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.medium_filter && this.medium_filter.length > 0) {
                    this.medium_filter = this.medium_filter.trim().toLowerCase();
                    const regex = new RegExp('.*' + this.medium_filter + '.*', 'ig');
                    roi_items = roi_items.filter(item => regex.test(fix(item)));
                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                if (this.sort != false && this.roiviews_hide == false) {
                    const field = this.sort;
                    let flag = this.sortFlag;   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                    if (field === 'uv') {   
                        const field = 'revenue';
                        const field2 = 'clicks';
                        roi_items = roi_items.sort(function (a, b) { 
                            if(flag == true){                             
                                return a[field]/a[field2] - b[field]/b[field2];
                            }else{
                                return b[field]/b[field2] - a[field]/a[field2];
                            }
                        });
                    }else if(field === 'avg_uc'){

                        const field = 'cost';
                        const field2 = 'clicks';
                        roi_items = roi_items.sort(function (a, b) { 
                            if(flag == true){                             
                                return a[field]/a[field2] - b[field]/b[field2];
                            }else{
                                return b[field]/b[field2] - a[field]/a[field2];
                            }
                        });
                    }
                    else if(field === 'data_date'){
                        roi_items = roi_items.sort(function (a, b) {
                        return flag ? moment(String(a[field])).format('H') - moment(String(b[field])).format('H') : moment(String(b[field])).format('H') - moment(String(a[field])).format('H');
                        });
                    }else{
                        roi_items = roi_items.sort(function (a, b) {
                      
                        if(flag == true){
                                return a[field] - b[field];
                            }else{
                                return b[field] - a[field];
                            }
                        });
                    }
                }

                return roi_items;
            },
            _medium_items() {
                if (!this.medium_items) {
                    return [];
                }

                let medium_items = this.medium_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return ['medium'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.medium_filter && this.medium_filter.length > 0) {
                    this.medium_filter = this.medium_filter.trim().toLowerCase();
                    const regex = new RegExp('.*' + this.medium_filter + '.*', 'ig');
                    medium_items = medium_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                
                if (this.sort != false && this.medium_hide == false) {
                    const field = this.sort;
                    let flag = this.sortFlag;
                    medium_items = medium_items.sort(function (a, b) {
                        return flag ? a[field] - b[field] : b[field] - a[field];
                    });
                }

                // Apply pagination
                if (this.mperPage) {
                    medium_items = medium_items.slice((this.medium_currentPage - 1) * this.mperPage, this.medium_currentPage * this.mperPage);
                }

                return medium_items;
            },
            _ipageviews_items() {
                if (!this.ipageviews_items) {
                    return [];
                }

                let ipageviews_items = this.ipageviews_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return ['page_title','page'].map(k => fix(v[k])).join(' ').toLowerCase();;
                    }
                    return String(v);
                };

                // Apply Sort
                if (this.sort) {
                    const field = this.sort;
                    let flag = this.sortFlag;
                    if (field == 'page_title') {
                        ipageviews_items = ipageviews_items.sort((a, b) => flag ? a[field].localeCompare(b[field]) : b[field].localeCompare(a[field]))
                    } else {
                        ipageviews_items = ipageviews_items.sort(function (a, b) {
                            return flag ? a[field] - b[field] : b[field] - a[field];
                        });
                    }
                }

                // Apply filter
                if (this.inpage_filter && this.inpage_filter.length > 0) {
                    const regex = new RegExp('.*' + this.inpage_filter + '.*');
                    ipageviews_items = ipageviews_items.filter(item => regex.test(fix(item)));
                }

                // Apply pagination
                if (this.perPage) {
                    ipageviews_items = ipageviews_items.slice((this.ipageviews_currentPage - 1) * this.perPage, this.ipageviews_currentPage * this.perPage);
                }

                return ipageviews_items;
            },
            selectItems: {
                get: function () {
                    return this.checked_mediums;
                },
                set: function (items) {
                    this.checked_mediums = items;
                    this.roi_adjust_input_length = this.checked_mediums.length;

                }
            },
            selectAllAction: {
                get: function () {
                    return this.roi_adjust_input_length ? this.checked_mediums.length == this.roi_adjust_input_length : false;
                },
                set: function (value) {
                    let selected = [];
                    if (value) {
                        this.medium_items.forEach(function (medium) {
                            //  if (medium.clicks >= 10) {
                            selected.push(medium);
                            // }
                        });
                    }
                    this.checked_mediums = selected;
                    this.roi_adjust_input_length = this.checked_mediums.length
                }
            },
            selectAllRoiRev: {
                get: function () {
                    return this.roi_adjust_input_length ? this.checked_mediums.length == this.roi_adjust_input_length : false;
                },
                set: function (value) {
                    let selected = [];
                    if (value) {
                        this.keyword_items.forEach(function (keyword) {
                            if (keyword.sessions >= 10) {
                                selected.push(keyword);
                            }
                        });
                    }
                    this.checked_mediums = selected;
                    this.roi_adjust_input_length = this.checked_mediums.length

                }
            },
        },
        filters: {
            divide: function (val, device, factor) {
                if (device == 'mobile') {
                    return val / 1000;
                } else if (!factor) {
                    return val / 100;
                } else {
                    return val;
                }
            },
            formatDate(value){
                  if (value) {
                    return moment(String(value)).format('H');
                  }
            },
             _format_n(value, fix) {
                if ((!value && value !== 0)) {
                    return '';
                }
                return parseFloat(value).toFixed(fix);
            },
            _format(value, fix) {
                if ((!value && value !== 0) || !fix) {
                    return '';
                }
                return parseFloat(value).toFixed(fix);
            },
            _time_format(value) {
                if (!value) {
                    return '';
                }
                return value.replace(".", ":");
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
            get_link: function (value, obj) {
                if (!value) {
                    return '';
                }
                try {
                    let str = obj.website_name.replace(/\s/g, '');
                    return '//'+str +'.com'+ value;
                }catch(e){
                    console.log(e);
                    return '';
                }
            },
            prc: function (val) {
                if (val) {
                    return val + '%'
                }
            }
        },
        watch: {

             _roi_items: function () {
        
                let _filter = this.filter == '' || this.filter == null;
                let data = this.filter_summary();

                let sums = {};
                let keys = ['clicks', 'revenue', 'cost', 'profit'];

                _.each(data, function (item) {
                    _.each(keys, function (key) {
                        sums[key] = (sums[key] || 0) + item[key];
                    });
                });
                this.sum_of_final_roi =this.count_values('final_roi',this.roi_items);
                this.sum_of_clicks =sums.clicks;
                this.sum_of_revenue =sums.revenue;
                this.sum_of_cost =sums.cost;
                this.sum_of_profit =sums.profit;
            },

            _medium_items: function () {
                this.losing_campaigns_count = _.filter(this.medium_items, function (o) {
                    if (o.alert == '1') return o
                }).length;

                let _filter = this.medium_filter == '' || this.medium_filter == null;
                let data = this.filter_summary();

                let sums = {};
                let keys = ['clicks', 'revenue', 'cost', 'provider_revenue', 'calculated_dfp_revenue'];

                _.each(data, function (item) {
                    _.each(keys, function (key) {
                        sums[key] = (sums[key] || 0) + item[key];
                    });
                });

                this.sum_mediums = this.count_values('medium', !_filter ? data : this.medium_items);
                this.summary_ctr = this._wavg('clicks', 'ctr');
                this.summary_ps = this._wavg('clicks', 'pages_session');
                this.summary_roi = this._wavg('clicks', 'roi_final');
                this.summary_clicks = sums.clicks;
                this.summary_revenue = sums.revenue;
                this.summary_provider_revenue = sums.provider_revenue;
                this.summary_cdr = sums.calculated_dfp_revenue;
                this.summary_cost = sums.cost;
            },
        }
    }
</script>

<style lang="scss">
    .roi_notice_msg {
        width: 800px !important;
    }

</style>
<style>
    .not-visibale {
        visibility: hidden;
    }

    .roi_span {
        display: inline-block;
        width: 45px;
        height: 20px;
        line-height: 15px;
    }

    @import "../../assets/styles/pages/_MediumKey.scss";

</style>
<style scoped>
    /deep/ .date-range__presets {
        display: none;
    }

    /deep/ .ant-input-number-handler-wrap {
        opacity: 1 !important;
    }

    .btn-width {
        width: 185px;
        margin: 4px 0px;
    }

    .pop-div {
        align-content: center;
        margin-left: 25px;
        padding-top: 0px;
    }
</style>
