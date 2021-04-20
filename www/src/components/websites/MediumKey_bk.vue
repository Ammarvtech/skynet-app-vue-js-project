<template>
    <div id="medium_key">
        <div class="row">
            <div class="col-xs-1">
                <div>&nbsp</div>
                <el-button-group>
                    <el-button icon="el-icon-arrow-left" class="radius" @click="showCampaigns()" type="primary" :disabled="stop">Campaigns</el-button>
                </el-button-group>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-2">
                <div>&nbsp</div>
                <el-date-picker v-model="date_filter" @change="conflict=true;initializeData(item_selected,date_filter,date_filter,true)" type="daterange" placeholder="Select different dates" :disabled="stop"></el-date-picker>
            </div>
            <div class="col-xs-3">
                <div>&nbsp</div>
                <el-select class="space" v-model="site_id" v-on:change="submit_onchange(item_selected)" :disabled="stop">
                    <el-option v-for="website in websites" :label="website.website_name" :value="website.website_id" :key="website.website_id"></el-option>
                </el-select>
            </div>
            <div class="col-xs-6 input-pull-left">
                <div>&nbsp</div>
                <el-select v-on:change="navigate('select')" v-on:visible-change="conflict=false" class="large" v-model="campaign_id" :disabled="stop">
                    <el-option class="card" v-for="(item, index) in items" :value="++index + ' - ' + item.campaign_id + ' - ' + item.name" :key="item.campaign_id">
                        <span>Campaign: {{ item.campaign_id }}</span><br>
                        <span>Name: {{ item.name }}</span><br>
                        <span>Device: {{ item.device }}</span>
                    </el-option>
                </el-select>
                <i @click="navigate('backward')" :class="[stop ? 'waiting el-icon-arrow-left click' : 'el-icon-arrow-left click']"></i>&nbsp
                <i @click="navigate('forward')" :class="[stop ? 'waiting el-icon-arrow-right click' : 'el-icon-arrow-right click']"></i>
            </div>
            <div class="col-xs-1">&nbsp
                <div v-if="(item_selected.source == 'revcontent' || item_selected.source == 'taboola') && item_selected.enable != '0'">
                    <button :class="['btn btn-danger']" @click="deleteNotice" :disabled="stop_campaign">Stop Campaign</button>
                </div>
                <div v-else-if="(item_selected.source == 'revcontent' || item_selected.source == 'taboola')">
                    <button :class="['btn btn-success']" @click="enableNotice" :disabled="stop_campaign">Enable Campaign</button>
                </div>
            </div>
            <div class="col-xs-1 process">
                <div v-if="item_selected.status =='IN_PROCESS'">
                    <i class="el-icon-loading blue"></i>
                </div>
            </div>
        </div>
        <div>&nbsp</div>
        <div>&nbsp</div>
        <!--<el-row class="col-lg-12 card-pull-left">-->
            <!--<el-col class="card-width" :class="[item_selected.device !== 'desktop' ? 'mobile-card' : '']">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Device</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<div v-if="item_selected.device === 'desktop'">-->
                                <!--<img src="src/assets/desktop.png"/>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.device === 'mobile'">-->
                                <!--<img src="src/assets/mobile.png"/>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.device === 'tablet'">-->
                                <!--<img src="src/assets/tablet.png"/>-->
                            <!--</div>-->
                            <!--<div v-else>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width" :class="[item_selected.device !== 'desktop' ? 'source-card' : '']">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Source</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<div v-if="item_selected.source == 'revcontent'">-->
                                <!--<img src="src/assets/rev.png"/>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.source === 'taboola'">-->
                                <!--<img src="src/assets/taboola.png"/>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.source === 'contentad'">-->
                                <!--<img src="src/assets/cadd.png"/>-->
                            <!--</div>-->
                            <!--<div v-else>-->
                                <!--<span>{{item_selected.source}}</span>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Sessions</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span>{{item_selected.sessions}}</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Pages/Sessions</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span :class="[color(item_selected, 'pages_session')]">{{item_selected.pages_session | _format(3) }}</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Bounce Rate</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span>{{item_selected.bounce_rate | _format(3)}}%</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Cost/Budget</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix budget_margin">-->
                            <!--<div v-if="item_selected.source === 'revcontent'">-->
                                <!--<el-popover ref="revbudget" placement="top" width="170" v-model="budget_visible">-->
                                    <!--<p>Enter New Budget:</p>-->
                                    <!--<div class="budget_container">-->
                                        <!--<div>&nbsp</div>-->
                                        <!--<el-input-number :step="bstep" size="small" v-model="budget" :disabled="stop"></el-input-number>-->
                                        <!--<div class="budget_action">-->
                                            <!--<el-button type="text" size="mini"  @click="budget_visible = false" :disabled="stop">cancel</el-button>-->
                                            <!--<el-button type="primary" size="mini" @click="set_revcontent_budget(item_selected)" :disabled="stop">confirm</el-button>-->
                                        <!--</div>-->
                                    <!--</div>-->
                                <!--</el-popover>-->
                                <!--<el-button class="budget_btn" size="mini" v-popover:revbudget :disabled="stop">{{item_selected.cost | _format(2)}} / {{item_selected.budget | _format(2)}}$</el-button>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.source === 'taboola'">-->
                                <!--<span>{{item_selected.cost | _format(2)}} / {{item_selected.daily_cap | _format(2)}}$</span>-->
                            <!--</div>-->
                            <!--<div v-else>-->
                                <!--<span>{{item_selected.cost | _format(2)}} / {{item_selected.budget | _format(2)}}$</span>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<div v-if="item_selected.device !== 'desktop'">-->
                <!--<el-col class="card-width">-->
                    <!--<el-card class="data-card">-->
                        <!--<div>-->
                            <!--<span class="black">CPC</span>-->
                            <!--<hr class="style-one">-->
                            <!--<div class="bottom clearfix">-->
                                <!--<span>{{item_selected.adsense_cpc | _format(3) }}</span>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</el-card>-->
                <!--</el-col>-->
                <!--<el-col class="card-width">-->
                    <!--<el-card class="data-card">-->
                        <!--<div>-->
                            <!--<span class="black">CTR</span>-->
                            <!--<hr class="style-one">-->
                            <!--<div class="bottom clearfix">-->
                                <!--<span>{{item_selected.ctr | _format(3) }}</span>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</el-card>-->
                <!--</el-col>-->
            <!--</div>-->
            <!--<div v-else></div>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Revenue</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span>{{item_selected.revenue | _format(3)}}$</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">UV</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix left-side">-->
                            <!--<div>-->
                                <!--<el-tooltip placement="top">-->
                                    <!--<div slot="content">-->
                                        <!--<div v-if="item_selected.source === 'revcontent' && item_selected.revcontent_uv > 0">-->
                                            <!--<span>P UV: {{item_selected.revcontent_uv | _format(3)}}</span><br>-->
                                        <!--</div>-->
                                        <!--<div v-if="item_selected.source === 'taboola' && item_selected.taboola_uv > 0">-->
                                            <!--<span>P UV: {{item_selected.taboola_uv | _format(3)}}</span><br>-->
                                        <!--</div>-->
                                        <!--<span>UV: {{item_selected.user_value | _format(3) }}</span><br>-->
                                        <!--<div v-if="item_selected.device === 'desktop' && item_selected.hb_user_value > 0">-->
                                            <!--<span>HB UV: {{item_selected.hb_user_value | _format(3)}}</span><br>-->
                                        <!--</div>-->
                                        <!--<div v-if="item_selected.ad_sense_uv > 0">-->
                                            <!--AdSense UV: {{item_selected.ad_sense_uv | _format(3)}}-->
                                        <!--</div>-->
                                        <!--<div v-if="item_selected.delta_uv > 0">-->
                                            <!--Delta UV: {{item_selected.delta_uv | _format(3)}}-->
                                        <!--</div>-->
                                    <!--</div>-->
                                    <!--<span>{{item_selected.final_uv | _format(3)}}</span>-->
                                <!--</el-tooltip>-->
                            <!--</div>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">Real Bid</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span>{{item_selected.cost / item_selected.sessions | _format(3) }}</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card :class="[editable ? 'data-card-editable' : 'data-card']">-->
                    <!--<div>-->
                        <!--<span class="black">Bid</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<div v-if="item_selected.source === 'taboola' && item_selected.bid">-->
                                <!--<el-badge value="Edit" class="item">-->
                                    <!--<el-button @click="make_editable('taboola',null,item_selected.bid)" size="small">{{item_selected.bid | _format(3)}}</el-button>-->
                                <!--</el-badge>-->
                            <!--</div>-->
                            <!--<div v-else-if="item_selected.source === 'taboola' && item_selected.avg_cpc">-->
                                <!--<el-badge value="Edit" class="item">-->
                                    <!--<el-button @click="make_editable('taboola',null,item_selected.avg_cpc)" size="small">{{item_selected.avg_cpc | _format(3)}}</el-button>-->
                                <!--</el-badge>-->
                            <!--</div>-->
                            <!--<div v-else>-->
                                <!--<span>{{item_selected.avg_cpc | _format(3)}}</span>-->
                            <!--</div>-->
                            <!--<el-input-number :class="[editable ? 'edit' : 'tb-hide']" :step="step" size="small" v-model="avg_cpc"></el-input-number>-->
                            <!--<i :class="[editable ? '' : 'tb-hide']" @click="update_campaign_cpc_taboola(item_selected,avg_cpc,'update')" class="el-icon-circle-check link mg-l green"></i>-->
                            <!--<i :class="[editable ? '' : 'tb-hide']" @click="update_campaign_cpc_taboola(item_selected,null,'cancel')" class="el-icon-circle-close link mg-r red"></i>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--<el-col class="card-width">-->
                <!--<el-card class="data-card">-->
                    <!--<div>-->
                        <!--<span class="black">ROI</span>-->
                        <!--<hr class="style-one">-->
                        <!--<div class="bottom clearfix">-->
                            <!--<span>-->
                                <!--<span :class="[color(item_selected, 'roi')]">{{item_selected.roi | _format(3)}}</span>-->
                            <!--</span>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
        <!--</el-row>-->
        <div>&nbsp</div>

        <!--<b-btn :class="[hide ? 'tb-hide' : '','btn-primary']" v-b-toggle.chart size="sm">-->
            <!--<span class="when-opened">Close</span>-->
            <!--<span class="when-closed">Open</span>-->
            <!--Chart-->
        <!--</b-btn>-->
        <!--<b-collapse visible id="chart">-->
            <!--<charts ref="chart"></charts>-->
        <!--</b-collapse>-->

        <div>
            <el-badge v-show="medium_star_count > 0" :value="medium_star_count" :max="99" class="item medium_star"></el-badge>
            <!--<el-badge v-show="keyword_star_count > 0" :value="keyword_star_count" :max="99" class="item keyword_star"></el-badge>-->
            <!--<el-badge v-show="ipageviews_star_count > 0" :value="ipageviews_star_count" :max="99" class="item ipageviews_star"></el-badge>-->
            <!--<el-badge v-show="country_star_count > 0" :value="country_star_count" :max="99" class="item country_star"></el-badge>-->
            <!--<el-badge v-show="block_medium_star_count > 0" :value="block_medium_star_count" :max="99" class="item block_medium_star"></el-badge>-->

            <el-tabs type="card" class="tab" v-model="activeName" @tab-click="tabClick">
                <el-tab-pane label="Mediums" name="medium"></el-tab-pane>
                <!--<el-tab-pane label="Keywords" name="keyword"></el-tab-pane>-->
                <!--<el-tab-pane label="Increase Pageviews" name="page_views"></el-tab-pane>-->
                <!--<el-tab-pane label="Countries" name="country"></el-tab-pane>-->
                <!--<el-tab-pane label="Mobile Devices" name="mobile_device"></el-tab-pane>-->
                <!--<el-tab-pane label="Campaigns" name="campaigns"></el-tab-pane>-->
                <!--<el-tab-pane v-if="item_selected.source == 'taboola'" label="Bulk Medium Block" name="bulk_medium_block"></el-tab-pane>-->
            </el-tabs>

            <!--Medium - Table-->
            <div v-show="!medium_hide">
                <div v-loading="medium_load">
                    <div class="top col-xs-2">
                        <b-form-input ref="medium_filter" v-model="medium_filter" placeholder="Type to Search"></b-form-input>
                    </div>
                    <div class="top col-sm-1">
                        <b-form-select :options="options" v-model="mperPage"></b-form-select>
                    </div>
                    <div v-if="item_selected.source == 'taboola' && roi_adjust_input.length > 0" class="top col-xs-4">
                        <el-button type="primary" @click="roiAdjustNotice" size="medium" :disabled="this.checked_roi_adjustment.length == 0 || roi_adjust_update" :loading="roi_adjust_loading">Adjust ROI</el-button>
                    </div>
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th @click="headClick(field,key)" v-for="field,key in medium_headers" class="pointer">
                                    <strong>{{field.label}}</strong>
                                </th>
                                <th v-if="item_selected.source == 'taboola'">
                                    <strong>Cost</strong>
                                </th>
                                <th v-if="item_selected.source == 'taboola'">
                                    <strong>CPC Bid</strong>
                                </th>
                                <th></th>
                                <th v-if="item_selected.source == 'taboola' && roi_adjust_input.length > 0">
                                    <input type="checkbox" v-model="selectAllRoi" @change="mediums_index_init">
                                </th>
                                <th v-if="item_selected.source == 'taboola' && roi_adjust_input.length > 0" style="width: 130px">
                                    <el-input-number class="adjust" controls-position="right" @change="selectAllRoiChange" :max="1" :min="0.1" :step="0.1" size="mini" v-model="roi_adjust" :disabled="stop"></el-input-number>
                                    <i :class="[roi_apply ? 'el-icon-loading blue' : 'tb-hide']"></i>
                                </th>
                                <th @click="headClick(null,'roi')" v-if="item_selected.source == 'taboola'" class="pointer">
                                    <strong>ROI</strong>
                                </th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in _medium_items" v-if="item!==undefined && item.campaign_id!=null"
                                :ref="'m_tr_'+index" :class="[item.status == 'IN_PROCESS' ? 'event_block':'']">
                                <td>
                                    <span>{{item.medium}}</span>&nbsp;
                                    <div class="red block" v-if="item.source == 'taboola' && item.block == '1'">
                                        <span>(blocked)</span>
                                    </div>
                                    <i :class="[item.rule_mark == '-1' ? 'el-icon-warning red float_right' : '']"></i>
                                </td>
                                <td>
                                    <el-tooltip placement="top">
                                        <div v-if="item.device =='desktop'" slot="content">
                                            HB UV: {{item.hb_user_value | _format(4) }}<br/>
                                            P UV: {{item.provider_uv | divide(item.device, true) | _format(4) }}
                                            <div v-if="item.ad_sense_uv > 0">
                                                AdSense UV: {{item.ad_sense_uv | format_fixed}}
                                            </div>
                                            <div v-if="item.delta_uv > 0">
                                                Delta UV: {{item.delta_uv | format_fixed}}
                                            </div>
                                        </div>
                                        <div v-else slot="content">
                                            UV: {{item.user_value | divide(item.device) | _format(4) }}<br/>
                                            P UV: {{item.provider_uv | divide(item.device) | _format(4) }}
                                        </div>
                                        <span>
                                            {{item.final_uv | divide(item.device, true) | _format(4) }}
                                        </span>
                                    </el-tooltip>
                                </td>
                                <td>
                                    <span>{{item.sessions}}</span>
                                </td>
                                <td>
                                    <span>{{item.bounce_rate | _format(3) }}%</span>
                                </td>
                                <td>
                                    <span :class="[color(item, 'pages_session')]">{{item.pages_session | _format(3) }}</span>
                                </td>
                                <td>
                                    <span>{{item.publisher_ctr | _format(3) }}</span>
                                </td>
                                <td>
                                    <span>{{item.adsense_cpc | _format(3) }}</span>
                                </td>
                                <td>
                                    <span>
                                        {{item.publisher_revenue | _format(3) }}$
                                    </span>
                                </td>
                                <td v-if="item_selected.source == 'taboola'">
                                    <span>{{item.cost | _format(3) }}$</span>
                                </td>
                                <td :class="[expend ? 'diff_bid_expend': 'diff_bid']" v-if="item.source === 'taboola'">
                                    <div class="block" v-if="item.bid && item.bid != item_selected.avg_cpc && item.bid != 1">
                                        <span class="link" @click="open_bid_mod(index)">{{calc_percentage_diff(item.bid)}}%</span>
                                        <span class="link" @click="open_bid_mod(index)">(${{calc_percentage(item.bid) | _format(3) }})</span>
                                        <div class="tb-hide" :ref="'taboola-'+index">
                                            <el-input-number class="edit_bid" :max="50" :min="-50" :step="1" size="small" v-model="bid_mod_change" :disabled="stop"></el-input-number>
                                            <el-tag class="percent" type="gray" color="transparent"><i class="fa fa-percent"></i></el-tag><br>
                                            <i @click="active_update_medium_bid_taboola(item,'mod', index, bid_mod_change)" :class="[stop ? 'not-active' : '', 'el-icon-circle-check link mg-l green']"></i>
                                            <i @click="close_bid_mod(index)" :class="[stop ? 'not-active' : '', 'el-icon-circle-close link mg-bid red']"></i>
                                            <span @click="active_update_medium_bid_taboola(item,'default', index)" class="link default">|  Default</span>
                                        </div>
                                    </div>
                                    <div class="block" v-else>
                                        <span class="link" v-model="cpc_modification" @click="open_bid_mod(index)">default (${{item_selected.bid ? item_selected.bid : item_selected.avg_cpc | _format(3) }})</span>
                                        <div class="tb-hide" :ref="'taboola-'+index">
                                            <el-input-number class="edit_bid" :max="50" :min="-50" :step="1" size="small" v-model="bid_mod_change" :disabled="stop"></el-input-number>
                                            <el-tag class="percent" type="gray" color="transparent"><i class="fa fa-percent"></i></el-tag><br>
                                            <i @click="active_update_medium_bid_taboola(item,'mod', index, bid_mod_change)" :class="[stop ? 'not-active' : '', 'el-icon-circle-check link mg-l green']"></i>
                                            <i @click="close_bid_mod(index)" :class="[stop ? 'not-active' : '', 'el-icon-circle-close link mg-bid red']"></i>
                                            <span @click="active_update_medium_bid_taboola(item,'default', index)" class="link default">|  Default</span>
                                        </div>
                                    </div>
                                    <div style="float: right;">
                                        <el-button class="" size="small" @click="active_update_medium_bid_taboola(item,'down', index)" :disabled="stop">-10%</el-button>
                                        <el-button class="" size="small" @click="active_update_medium_bid_taboola(item,'up', index)" :disabled="stop">+10%</el-button>
                                    </div>
                                </td>
                                <td v-if="(item.source === 'taboola' || item.source === 'revcontent')">
                                    <el-button size="small" @click="update_medium_status(item,index)" :disabled="stop"><i :class="[item.block == '0' || item.block == '-1' ? 'fa fa-ban red' : item.block == '1' ? 'fa fa-undo green auto check-small' : '']"></i></el-button>
                                </td>
                                <td v-if="item.source === 'taboola' && item.sessions >= 50">
                                    <input type="checkbox" v-model="checked_roi_adjustment" :value="item" @change="item.index=index" :disabled="roi_adjust_input[index] == 0">
                                </td>
                                <td v-else-if="item.source === 'taboola' && item.sessions <= 50"></td>
                                <td v-if="item.source === 'taboola' && item.sessions >= 50">
                                    <el-input-number class="adjust" controls-position="right" :max="1" :min="0" :step="0.1" size="mini" v-model="roi_adjust_input[index]" @change="item.index=index"></el-input-number>
                                </td>
                                <td v-else-if="item.source === 'taboola' && item.sessions <= 50"></td>
                                <td v-if="item.source === 'taboola'">
                                    <span :class="[color(item, 'roi')]">{{item.roi | _format(3)}}</span>
                                </td>
                                <td>
                                    <div v-if="item.status =='DONE'">
                                        <i class="fa fa-check-square green mleft"></i>
                                    </div>
                                    <div v-else-if="item.status =='IN_PROCESS' || item.status =='PENDING'">
                                        <div class="hourglass mleft"></div>
                                    </div>
                                    <div v-else-if="item.status =='ERROR'">
                                        <i class="fa fa-exclamation red mleft"></i>
                                    </div>
                                </td>
                                <td v-if="item.source !== 'taboola' && item.source !=='revcontent'"></td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-show="!stop" class="col-md-11 text-center">
                        <b-pagination size="md" :total-rows="this.medium_items.length" :per-page="perPage" v-model="medium_currentPage"/>
                    </div>
                </div>
            </div>

            <!--Keywords - Table-->
            <!--<div v-show="!keyword_hide">-->
                <!--<div v-loading="keyword_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="keyword_filter" v-model="keyword_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<div v-if="item_selected.source == 'revcontent' && roi_adjust_input.length > 0" class="top col-xs-4">-->
                        <!--<el-button type="primary" @click="roiAdjustNotice" size="medium" :disabled="this.checked_roi_adjustment.length == 0 || roi_adjust_update" :loading="roi_adjust_loading">Adjust ROI</el-button>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick(field,key)" v-for="field,key in keyword_headers" class="pointer">-->
                                    <!--<div v-if="item_selected.source != 'revcontent' && field.label == 'CPC Bid'"></div>-->
                                    <!--<div v-else-if="field.description">-->
                                        <!--<el-tooltip placement="top">-->
                                            <!--<div slot="content">-->
                                                <!--<strong>{{field.description}}</strong>-->
                                            <!--</div>-->
                                            <!--<strong>{{field.label}}</strong>-->
                                        <!--</el-tooltip>-->
                                    <!--</div>-->
                                    <!--<div v-else>-->
                                        <!--<strong>{{field.label}}</strong>-->
                                    <!--</div>-->
                                <!--</th>-->
                                <!--<th v-if="item_selected.source == 'revcontent'"><strong>Cost</strong></th>-->
                                <!--<th v-if="item_selected.source == 'revcontent' && roi_adjust_input.length > 0">-->
                                    <!--<input type="checkbox" v-model="selectAllRoiRev" @change="keywords_index_init">-->
                                <!--</th>-->
                                <!--<th v-if="item_selected.source == 'revcontent' && roi_adjust_input.length > 0" style="width: 130px">-->
                                    <!--<el-input-number class="adjust" controls-position="right" @change="selectAllRoiChange" :max="1" :min="0.1" :step="0.1" size="mini" v-model="roi_adjust" :disabled="stop"></el-input-number>-->
                                    <!--<i :class="[roi_apply ? 'el-icon-loading blue' : 'tb-hide']"></i>-->
                                <!--</th>-->
                                <!--<th @click="headClick(null,'roi')" v-if="item_selected.source == 'revcontent'" :class="['sorting','sorting_'+(sortDesc?'desc':'asc')]">-->
                                    <!--<strong>ROI</strong>-->
                                <!--</th>-->
                                <!--<th v-if="item_selected.source == 'revcontent'"></th>-->
                                <!--<th><strong>Status</strong></th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _keywords_items" v-if="item!==undefined && item.campaign_id!=null"-->
                                <!--:ref="'k_tr_'+index" :class="[item.status == 'IN_PROCESS' ? 'event_block':'']">-->
                                <!--<td>-->
                                    <!--<span>{{item.keyword}}</span>-->
                                    <!--<i :class="[item.rule_mark == '-1' ? 'el-icon-warning red float_right' : '']"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<div v-if="item_selected.source === 'revcontent'">-->
                                        <!--<span @click="make_editable('revcontent', index, item.bid)">{{item.bid | _format(3) }}</span>-->
                                        <!--<el-input-number :ref="'rev-'+index" class="tb-hide" size="small" :step="step" v-model="rev_avg_cpc"></el-input-number>-->
                                        <!--<i :ref="'rev-check-'+index" @click="set_revcontent_cpc(item,rev_avg_cpc,'update', index)" class="el-icon-circle-check link tb-hide green"></i>-->
                                        <!--<i :ref="'rev-close-'+index" @click="set_revcontent_cpc(item,null,'cancel', index)" class="el-icon-circle-close link tb-hide red"></i>-->
                                    <!--</div>-->
                                    <!--<div v-else>-->
                                        <!--<span>{{item.avg_cpc | _format(3) }}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<el-tooltip placement="top">-->
                                        <!--<div v-if="item.device =='desktop'" slot="content">-->
                                            <!--HB UV: {{item.hb_user_value | _format(4) }}<br/>-->
                                            <!--P UV: {{item.provider_uv | divide(item.device, true) | _format(4) }}-->
                                            <!--<div v-if="item.ad_sense_uv > 0">-->
                                                <!--AdSense UV: {{item.ad_sense_uv | format_fixed}}-->
                                            <!--</div>-->
                                            <!--<div v-if="item.delta_uv > 0">-->
                                                <!--Delta UV: {{item.delta_uv | format_fixed}}-->
                                            <!--</div>-->
                                        <!--</div>-->
                                        <!--<div v-else slot="content">-->
                                            <!--UV: {{item.user_value | divide(item.device) | _format(4) }}<br/>-->
                                            <!--P UV: {{item.provider_uv | divide(item.device) | _format(4) }}-->
                                        <!--</div>-->
                                        <!--<span>-->
                                            <!--{{item.final_uv | divide(item.device, true) | _format(4) }}-->
                                        <!--</span>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.sessions}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.bounce_rate | _format(3)}}%</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'pages_session')]">{{item.pages_session | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.publisher_ctr | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>-->
                                        <!--{{item.publisher_revenue | _format(3)}}$-->
                                    <!--</span>-->
                                <!--</td>-->
                                <!--<td v-if="item_selected.source == 'revcontent'">-->
                                    <!--<span>{{item.cost | _format(3) }}$</span>-->
                                <!--</td>-->
                                <!--<td v-if="item.source === 'revcontent' && item.sessions >= 50">-->
                                    <!--<input type="checkbox" v-model="checked_roi_adjustment" :value="item" @change="item.index=index" :disabled="roi_adjust_input[index] == 0">-->
                                <!--</td>-->
                                <!--<td v-else></td>-->
                                <!--<td v-if="item.source === 'revcontent' && item.sessions >= 50">-->
                                    <!--<el-input-number class="adjust" controls-position="right" :max="1" :min="0" :step="0.1" size="mini" v-model="roi_adjust_input[index]" @change="item.index=index"></el-input-number>-->
                                <!--</td>-->
                                <!--<td v-else></td>-->
                                <!--<td v-if="item.source === 'revcontent'">-->
                                    <!--<span :class="[color(item, 'roi')]">{{item.roi | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td v-if="item.source === 'revcontent' && item.enabled == '1'">-->
                                    <!--<el-tooltip class="item" effect="dark" content="Block Keyword" placement="top-start">-->
                                        <!--<el-button size="small" class="red" @click="update_keyword_status_revcontent(item,index)" :disabled="stop"><i class="fa fa-ban red"></i></el-button>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td v-else-if="item.source === 'revcontent' && item.enabled == '0'">-->
                                    <!--<el-tooltip class="item" effect="dark" content="Activate Keyword" placement="top-start">-->
                                        <!--<el-button class="check-small" size="small" @click="update_keyword_status_revcontent(item,index)" :disabled="stop"><i class="fa fa-undo green auto"></i></el-button>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td v-else-if="item.source === 'revcontent' && !item.enabled">-->
                                    <!--<i class="fa fa-exclamation-circle exclamation"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<div v-if="item.status =='DONE'">-->
                                        <!--<i class="fa fa-check-square green mleft"></i>-->
                                    <!--</div>-->
                                    <!--<div v-else-if="item.status =='IN_PROCESS' || item.status =='PENDING'">-->
                                        <!--<div class="hourglass mleft"></div>-->
                                    <!--</div>-->
                                    <!--<div v-else-if="item.status =='ERROR'">-->
                                        <!--<i class="fa fa-exclamation red mleft"></i>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td v-if="item.source !== 'taboola' && item.source !=='revcontent'"></td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.keyword_items.length" :per-page="perPage" v-model="keyword_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Increase Pageviews - Table-->
            <!--<div v-show="!ipageviews_hide">-->
                <!--<div v-loading="ipageviews_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="inpage_filter" v-model="inpage_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick_pageviews(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in ipageviews_headers">-->
                                    <!--<strong>{{field.label}}</strong>-->
                                <!--</th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _ipageviews_items" v-if="item!==undefined">-->
                                <!--<td>-->
                                    <!--<span>{{item.page}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<i :class="[item.mark === '-1' ? 'el-icon-warning red' : '']"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.pageviews}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.exit_rate | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_ctr | _format(4)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(4)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.clicks}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.revenue | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.hb_user_value | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{ (item.revenue / item.pageviews) * 1000 | _format(6) }}</span>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.ipageviews_items.length" :per-page="perPage" v-model="ipageviews_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Countrys - Table-->
            <!--<div v-show="!country_hide">-->
                <!--<div v-loading="country_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="country_filter" v-model="country_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in country_headers">-->
                                    <!--<strong>{{field.label}}</strong>-->
                                <!--</th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _country_items" v-if="item!==undefined">-->
                                <!--<td>-->
                                    <!--<span>{{item.country}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<i :class="[item.rule_mark === '-1' ? 'el-icon-warning red' : '']"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<el-tooltip placement="top">-->
                                        <!--<div slot="content">-->
                                            <!--UV: {{item.user_value | _format(3) }}<br/>-->
                                            <!--HB UV: {{item.hb_user_value | _format(3) }}</div>-->
                                            <!--<div v-if="item.ad_sense_uv > 0">-->
                                                <!--AdSense UV: {{item.ad_sense_uv | format_fixed}}-->
                                            <!--</div>-->
                                            <!--<div v-if="item.delta_uv > 0">-->
                                                <!--Delta UV: {{item.delta_uv | format_fixed}}-->
                                            <!--</div>-->
                                        <!--<span>-->
                                            <!--{{item.user_value + item.hb_user_value | _format(3) }}-->
                                        <!--</span>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.sessions}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.bounce_rate | _format(3)}}%</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'pages_session', true)]">{{item.pages_session | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.publisher_ctr | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="item.device==='desktop'">-->
                                        <!--{{item.sessions * item.hb_user_value | _format(3) }}$-->
                                    <!--</span>-->
                                    <!--<span v-else>-->
                                        <!--{{item.publisher_revenue | _format(3) }}$-->
                                    <!--</span>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.country_items.length" :per-page="perPage" v-model="country_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Device - Table-->
            <!--<div v-show="!device_hide">-->
                <!--<div v-loading="device_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="country_filter" v-model="country_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in device_headers">-->
                                    <!--<strong>{{field.label}}</strong>-->
                                <!--</th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _device_items" v-if="item!==undefined">-->
                                <!--<td>-->
                                    <!--<span>{{item.device}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.uv | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.sessions}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.bounce_rate | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'pages_session', true)]">{{item.pages_session | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.publisher_ctr | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.revenue | _format(3)}}</span>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.device_items.length" :per-page="perPage" v-model="device_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Campaigns - Table-->
            <!--<div v-show="!campaigns_hide">-->
                <!--<div v-loading="campaigns_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="campaigns_filter" v-model="campaigns_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in campaigns_headers">-->
                                    <!--<div>-->
                                        <!--<strong>{{field.label}}</strong>-->
                                    <!--</div>-->
                                <!--</th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _campaigns_items" v-if="item!==undefined && item.campaign_id!=null">-->
                                <!--<td>-->
                                    <!--<span>{{item.device}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.source}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.campaign_id}}</span>-->
                                    <!--<i :class="[item.mark === 'true' ? 'el-icon-warning red' : '']"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.sessions}}</span>-->
                                <!--</td>-->

                                <!--<td>-->
                                    <!--<span>{{item.revenue | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.cost | _format(2)}} / {{item.budget | _format(2)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<el-tooltip placement="top">-->
                                        <!--<div slot="content">-->
                                            <!--Taboola UV: {{item.taboola_uv | _format(3)}}<br/>-->
                                            <!--Revcontent UV: {{item.revcontent_uv | _format(3)}}<br/>-->
                                            <!--HB UV: {{(item.hb_user_value / 100) * factor | _format(3)}}<br/>-->
                                            <!--UV: {{item.user_value / 1000 | _format(3) }}<br/>-->
                                            <!--<div v-if="item.ad_sense_uv > 0">-->
                                                <!--AdSense UV: {{item.ad_sense_uv | format_fixed}}-->
                                            <!--</div>-->
                                            <!--<div v-if="item.delta_uv > 0">-->
                                                <!--Delta UV: {{item.delta_uv | format_fixed}}-->
                                            <!--</div>-->
                                        <!--</div>-->
                                        <!--<span v-if="item.device === 'desktop' && factor">-->
                                            <!--{{(item.taboola_uv + item.revcontent_uv + (item.user_value / 1000)) + ((item.hb_user_value / 100) * factor) | _format(4) }}-->
                                        <!--</span>-->
                                        <!--<span>-->
                                            <!--{{item.final_uv | _format(4) }}-->
                                        <!--</span>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td v-if="item.source === 'taboola'">-->
                                    <!--<span :class="[item.taboola_uv == 0 ? 'red' : '']">{{item.taboola_uv | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td v-else-if="item.source === 'revcontent'">-->
                                    <!--<span :class="[item.revcontent_uv == 0 ? 'red' : '']">{{item.revcontent_uv | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td v-else>-->

                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.bounce_rate | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.avg_cpc | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'pages_session')]">{{item.pages_session | _format(2)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'ctr')]">{{item.ctr | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span :class="[color(item, 'roi')]">{{item.roi}}</span>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.campaigns_items.length" :per-page="perPage" v-model="campaigns_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Content Ad - Table-->
            <!--<div v-show="!content_ad_hide">-->
                <!--<div v-loading="ad_content_load">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="country_filter" v-model="country_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th @click="headClick_pageviews(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in ad_content_headers">-->
                                    <!--<strong>{{field.label}}</strong>-->
                                <!--</th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _ad_content_items" v-if="item!==undefined">-->
                                <!--<td>-->
                                    <!--<span>{{item.ad_content}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<i :class="[item.mark == 1 ? 'el-icon-star-on yellow' : item.mark == -1 ? 'el-icon-warning red' : '']"></i>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.pageviews_d">{{item.pageviews}}</span>-->
                                    <!--<div v-else-if="item.pageviews_d">-->
                                        <!--<span>{{item.pageviews_d | _format(2) }}%-->
                                            <!--<i :class="[item._pageviews > item.pageviews ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._pageviews}} vs {{item.pageviews}}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.exit_rate_d">{{item.exit_rate}}</span>-->
                                    <!--<div v-else-if="item.exit_rate_d">-->
                                        <!--<span>{{item.exit_rate_d | _format(2) }}%-->
                                            <!--<i :class="[item._exit_rate > item.exit_rate ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._pageviews}} vs {{item.pageviews}}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.adsense_ctr_d">{{item.adsense_ctr}}</span>-->
                                    <!--<div v-else-if="item.adsense_ctr_d">-->
                                        <!--<span>{{item.adsense_ctr_d | _format(3) }}%-->
                                            <!--<i :class="[item._adsense_ctr > item.adsense_ctr ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._adsense_ctr | _format(3) }} vs {{item.adsense_ctr | _format(3)}}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.adsense_cpc_d">{{item.adsense_cpc}}</span>-->
                                    <!--<div v-else-if="item.adsense_cpc_d">-->
                                        <!--<span>{{item.adsense_cpc_d | _format(3) }}%-->
                                            <!--<i :class="[item._adsense_cpc > item.adsense_cpc ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._adsense_cpc | _format(3) }} vs {{item.adsense_cpc | _format(3)}}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.clicks_d">{{item.clicks}}</span>-->
                                    <!--<div v-else-if="item.clicks_d">-->
                                        <!--<span>{{item.clicks_d | _format(3) }}%-->
                                            <!--<i :class="[item._clicks > item.clicks ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._clicks }} vs {{item.clicks }}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.revenue_d">{{item.revenue}}</span>-->
                                    <!--<div v-else-if="item.revenue_d">-->
                                        <!--<span>{{item.revenue_d | _format(3) }}%-->
                                            <!--<i :class="[item._revenue > item.revenue ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._revenue }} vs {{item.revenue }}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span v-if="!item.hb_user_value_d">{{item.hb_user_value | _format(3)}}</span>-->
                                    <!--<div v-else-if="item.hb_user_value_d">-->
                                        <!--<span>{{item.hb_user_value_d | _format(3) }}%-->
                                            <!--<i :class="[item._hb_user_value > item.hb_user_value ? 'el-icon-caret-top up' : 'el-icon-caret-bottom down']"></i>-->
                                        <!--</span><br>-->
                                        <!--<hr class="percentage">-->
                                        <!--<span>{{item._hb_user_value }} vs {{item.hb_user_value }}</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{ (item.revenue / item.pageviews) * 1000 | _format(6) }}</span>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.ad_content_items.length" :per-page="perPage" v-model="ad_content_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->

            <!--Bulk Medium Block - Table-->
            <!--<div v-show="!medium_block_hide" >-->
                <!--<div v-loading="">-->
                    <!--<div class="top col-xs-2">-->
                        <!--<b-form-input ref="medium_block_filter" v-model="medium_block_filter" placeholder="Type to Search"></b-form-input>-->
                    <!--</div>-->
                    <!--<div class="top col-sm-1">-->
                        <!--<b-form-select :options="options" v-model="perPage"></b-form-select>-->
                    <!--</div>-->
                    <!--<div class="top col-xs-4">-->
                        <!--<button :class="['btn btn-danger']" @click="deleteNoticeMediums" :disabled="this.checked_mediums.length == 0 || bulk_update">Block Mediums</button>-->
                        <!--&lt;!&ndash;<span class="red" style="padding-left: 70px">The Data Is From Sunday 21 January 2018</span>&ndash;&gt;-->
                    <!--</div>-->
                    <!--<table class="table table-striped table-hover">-->
                        <!--<thead>-->
                            <!--<tr>-->
                                <!--<th><input type="checkbox" v-model="selectAll"></th>-->
                                <!--<th @click="headClick(field,key)"-->
                                    <!--:class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"-->
                                    <!--v-for="field,key in medium_block_headers">-->
                                    <!--<strong>{{field.label}}</strong>-->
                                <!--</th>-->
                                <!--<th @click="headClick(null,'cost')" v-if="item_selected.source == 'taboola'" :class="['sorting','sorting_'+(sortDesc?'desc':'asc')]">-->
                                    <!--<strong>Cost</strong>-->
                                <!--</th>-->
                                <!--<th @click="headClick(null,'lost')" v-if="item_selected.source == 'taboola'" :class="['sorting','sorting_'+(sortDesc?'desc':'asc')]">-->
                                    <!--<strong>Lost</strong>-->
                                <!--</th>-->
                                <!--<th @click="headClick(null,'roi')" v-if="item_selected.source == 'taboola'" :class="['sorting','sorting_'+(sortDesc?'desc':'asc')]">-->
                                    <!--<strong>ROI</strong>-->
                                <!--</th>-->
                                <!--<th><strong>Status</strong></th>-->
                            <!--</tr>-->
                        <!--</thead>-->
                        <!--<tbody>-->
                            <!--<tr v-for="(item, index) in _medium_block_items" v-if="item!==undefined && item.campaign_id!=null"-->
                                <!--:ref="'m_tr_'+index" :class="[item.status == 'IN_PROCESS' ? 'event_block':'']">-->
                                <!--<td>-->
                                    <!--<input type="checkbox" v-model="checked_mediums" :value="item">-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.medium}}</span>&nbsp;-->
                                    <!--<div class="red block" v-if="item.source == 'taboola' && item.block == '1'">-->
                                        <!--<span>(blocked)</span>-->
                                    <!--</div>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<el-tooltip placement="top">-->
                                        <!--<div v-if="item.device =='desktop'" slot="content">-->
                                            <!--HB UV: {{item.hb_user_value | _format(4) }}<br/>-->
                                            <!--P UV: {{item.provider_uv | divide(item.device, true) | _format(4) }}-->
                                        <!--</div>-->
                                        <!--<div v-else slot="content">-->
                                            <!--UV: {{item.user_value | divide(item.device) | _format(4) }}<br/>-->
                                            <!--P UV: {{item.provider_uv | divide(item.device) | _format(4) }}-->
                                        <!--</div>-->
                                        <!--<span>-->
                                            <!--{{item.final_uv | divide(item.device, true) | _format(4) }}-->
                                        <!--</span>-->
                                    <!--</el-tooltip>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.sessions}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.bounce_rate | _format(3) }}%</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.pages_session | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.publisher_ctr | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>{{item.adsense_cpc | _format(3) }}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<span>-->
                                        <!--{{item.publisher_revenue | _format(3) }}$-->
                                    <!--</span>-->
                                <!--</td>-->
                                <!--<td v-if="item_selected.source == 'taboola'">-->
                                    <!--<span>{{item.cost | _format(3) }}$</span>-->
                                <!--</td>-->
                                <!--<td v-if="item_selected.source == 'taboola'">-->
                                    <!--<span>{{item.lost || 0 | _format(3) }}$</span>-->
                                <!--</td>-->
                                <!--<td v-if="item.source === 'taboola'">-->
                                    <!--<span class="label" :class="[item.roi < 0 ? 'label-danger' : item.roi >= 0.30 ? 'label-success' : item.roi > 0 && item.roi < 0.30 ? 'label-warning' : 'label-info']">{{item.roi | _format(3)}}</span>-->
                                <!--</td>-->
                                <!--<td>-->
                                    <!--<div v-if="item.status =='DONE'">-->
                                        <!--<i class="fa fa-check-square green mleft"></i>-->
                                    <!--</div>-->
                                    <!--<div v-else-if="item.status =='IN_PROCESS' || item.status =='PENDING'">-->
                                        <!--<div class="hourglass mleft"></div>-->
                                    <!--</div>-->
                                    <!--<div v-else-if="item.status =='ERROR'">-->
                                        <!--<i class="fa fa-exclamation red mleft"></i>-->
                                    <!--</div>-->
                                    <!--<div v-else-if="item.status =='RETRY'">-->
                                        <!--<i class="el-icon-info mleft"></i>-->
                                    <!--</div>-->
                                <!--</td>-->
                            <!--</tr>-->
                        <!--</tbody>-->
                    <!--</table>-->
                    <!--<div v-show="!stop" class="col-md-11 text-center">-->
                        <!--<b-pagination size="md" :total-rows="this.medium_block_items.length" :per-page="perPage" v-model="medium_block_currentPage"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->
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
        },
        mounted () {
            window.addEventListener("keydown", this.keypressed);
        },
        data () {
            return {
                items: [],
                colors: [],
                checked_mediums:[],
                _items: [],
                websites: [],
                keyword_items: [],
                medium_items: [],
                medium_block_items: [],
                checked_roi_adjustment: [],
                roi_adjust_input: [],
                roi_adjustment: [],
                campaigns_items: [],
                country_items: [],
                ipageviews_items: [],
                ad_content_items: [],
                device_items: [],
                date_filter: [],
                tab_init : [],
                options: [{text: 5, value: 5}, {text: 10, value: 10},
                    {text: 15, value: 15},
                    {text: 20, value: 20},
                    {text: 25, value: 25},
                    {text: 30, value: 30}],
                keyword_headers: {
                    type: {label: 'Keyword', sortable: true},
                    bid: {label: 'CPC Bid', sortable: true, description:'Click to update cpc value'},
                    user_value: {label: 'UV', sortable: true},
                    sessions: {label: 'Sessions', sortable: true},
                    bounce_rate: {label: 'Bounce Rate', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    publisher_ctr: {label: 'Publisher CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    publisher_revenue: {label: 'Revenue', sortable: true}
                },
                medium_headers: {
                    medium: {label: 'Medium', sortable: true},
                    creative_ctr: {label: 'creative CTR', sortable: true},
                    Clicks: {label: 'Clicks', sortable: true},
                    uv: {label: 'UV', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    revenue: {label: 'Revenue', sortable: true},
                    cost: {label: 'Cost', sortable: true},
                    cpc: {label: 'CPC', sortable: true},
                },
                medium_block_headers: {
                    medium: {label: 'Medium', sortable: true},
                    final_uv: {label: 'UV', sortable: true},
                    sessions: {label: 'Sessions', sortable: true},
                    bounce_rate: {label: 'Bounce Rate', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    publisher_ctr: {label: 'Publisher CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    publisher_revenue: {label: 'Revenue', sortable: true},
                },
                country_headers: {
                    country: {label: 'Country', sortable: false},
                    mark: {label: 'Rule', sortable: true},
                    user_value: {label: 'UV', sortable: true},
                    sessions: {label: 'Sessions', sortable: true},
                    bounce_rate: {label: 'Bounce Rate', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    publisher_ctr: {label: 'Publisher CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    publisher_revenue: {label: 'Revenue', sortable: true}
                },
                ipageviews_headers: {
                    page_url: {label: 'Page URL', sortable: true},
                    mark: {label: 'Rule', sortable: true},
                    pageviews: {label: 'Pageviews', sortable: true},
                    exit_rate: {label: '% Exit', sortable: true},
                    adsense_ctr: {label: 'Adsense CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    clicks: {label: 'Ads Clicks', sortable: true},
                    revenue: {label: 'Revenue', sortable: true},
                    hb_user_value: {label: 'HB User Value', sortable: true},
                    adsense_rpm: {label: 'Adsense RPM', sortable: true},
                },
                device_headers: {
                    device: {label: 'Device', sortable: false},
                    uv: {label: 'UV', sortable: true},
                    sessions: {label: 'Sessions', sortable: true},
                    bounce_rate: {label: 'Bounce Rate', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true},
                    publisher_ctr: {label: 'Publisher CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    revenue: {label: 'Revenue', sortable: true}
                },
                ad_content_headers: {
                    ad_content: {label: 'Ad Content', sortable: true},
                    pageviews: {label: 'Pageviews', sortable: true},
                    exit_rate: {label: '% Exit', sortable: true},
                    adsense_ctr: {label: 'Adsense CTR', sortable: true},
                    adsense_cpc: {label: 'Adsense CPC', sortable: true},
                    clicks: {label: 'Ads Clicks', sortable: true},
                    revenue: {label: 'Revenue', sortable: true},
                    hb_user_value: {label: 'HB User Value', sortable: true},
                    adsense_rpm: {label: 'Adsense RPM', sortable: true},
                },
                campaigns_headers: {
                    device: {label: 'Device', sortable: false},
                    source: {label: 'Source', sortable: false},
                    campaign_id: {label: 'Campaign ID', sortable: true},
                    sessions: {label: 'Sessions', sortable: true, description:'Analytics sessions'},
                    revenue: {label: 'Revenue', sortable: true, description:'Final Revenue'},
                    cost: {label: 'Cost / Budget', sortable: false},
                    adsense_cpc: {label: 'CPC', sortable: true, description:'CPC - Adsense Revenue / Adsense Ads Clicks'},
                    user_value: {label: 'UV', sortable: true, description:'Final UV - SUM'},
                    provider_uv: {label: 'P UV', sortable: true, description:'Provider UV'},
                    bounce_rate: {label: 'Bounce rate', sortable: true},
                    avg_cpc: {label: 'Avg cpc', sortable: true},
                    pages_session: {label: 'Pages / Session', sortable: true, description:'Pages per session'},
                    ctr: {label: 'CTR', sortable: true, description:'Provider CTR'},
                    roi: {label: 'ROI', sortable: true}
                },
                perPage: 20,
                mperPage: 30,
                medium_currentPage: 1,
                medium_block_currentPage: 1,
                campaigns_currentPage: 1,
                keyword_currentPage: 1,
                country_currentPage: 1,
                ipageviews_currentPage: 1,
                ad_content_currentPage: 1,
                device_currentPage: 1,
                medium_star_count:0,
                keyword_star_count:0,
                country_star_count:0,
                block_medium_star_count:0,
                ipageviews_star_count:0,
                step:0.01,
                bstep:100,
                roi_adjust:0.3,
                sort: null,
                hide: false,
                sort_pageviews: null,
                medium_filter: null,
                medium_block_filter: null,
                campaigns_filter: null,
                keyword_filter: null,
                country_filter: null,
                inpage_filter: null,
                device_filter: null,
                medium_hide: true,
                medium_block_hide: true,
                campaigns_hide: true,
                keyword_hide: true,
                country_hide: true,
                ipageviews_hide: true,
                content_ad_hide: true,
                device_hide: true,
                sortDesc: true,
                sortDesc_pageviews: true,
                conflict: false,
                stop:false,
                sync:false,
                editable:false,
                rev_editable: false,
                index_edit: false,
                bid_mod_index: false,
                budget: false,
                budget_visible: false,
                expend: false,
                medium_load: true,
                campaigns_load: true,
                keyword_load: true,
                country_load: true,
                ipageviews_load: true,
                device_load: true,
                ad_content_load: true,
                stop_campaign:false,
                disable_reload:false,
                bulk_update: false,
                roi_adjust_update: false,
                roi_apply: false,
                roi_adjust_loading: false,
                activeName: 'medium',
                device_selected:'',
                source_selected:'',
                item_selected: '',
                site_id: '',
                saved_site_id: '',
                campaign_id: '',
                date_start: '',
                date_end: '',
                avg_cpc:'',
                rev_avg_cpc:'',
                bid_mod_change: '',
                cpc_modification: '',
                roi_adjust_input_length: null
            }
        },
        methods: {
            initializeView(item, items, websites, site_id, date_start, date_end, source, device){
                this.items = items;
                this.item_selected = item;
                this.websites = websites;
                this.date_start = date_start;
                this.date_end = date_start;
                this.date_filter = [date_start, date_end];
                this.campaign_id = item.campaign_id + ' - ' + item.name;
                this.site_id = item.site_id;
                this.saved_site_id = site_id;
                this.avg_cpc = item.bid;
                this.budget = item.budget;
                this.bid_mod_change = '';
                this.device_selected = device;
                this.source_selected = source;
                this.medium_hide = false;
                this.factor = item.factor;

                // Init chart
                // setTimeout(() => {
                //     item.start = date_start;
                //     this.$refs.chart.get_chart_data(item, true);
                // }, 1);

                setTimeout(() => {
                    this.get_colors({'device':'all', 'source': item.source, 'page_type': 'medium'});
                }, 1);

                // Init all tables
                this.initializeData(item, date_start, date_end);
            },
            initializeData(item, date_start, date_end, switch_dates){

                if(!item || !date_start || !date_end){return;}

                this.roi_adjust = 0.3;
                this.medium_star_count = 0;
                this.keyword_star_count = 0;
                this.country_star_count = 0 ;
                this.block_medium_star_count = 0 ;
                this.ipageviews_star_count = 0;
                this.checked_mediums = [];
                this.medium_block_items = [];
                this.checked_roi_adjustment = [];
                this.roi_adjust_input = [];

                if(switch_dates && date_start.length === 0){
                    return false;
                } else if(switch_dates){
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

                this.campaigns_hide = true;
                this.keyword_hide = true;
                this.country_hide = true;
                this.ipageviews_hide = true;
                this.content_ad_hide = true;
                this.device_hide = true;
                this.medium_block_hide = true;

                this.keyword_load = true;
                this.medium_load = true;
                this.ipageviews_load = true;

                //TODO: Add ad-content table request when ready
                let params = {'campaign_id':campaign_id, 'device': device, 'source': source, 'site_id': site_id, 'start': start, 'end': end};
                //let actions = ['mediums', 'keywords', 'inpage'];
                let actions = ['mediums'];

                //if (source == "taboola"){actions.push("block_mediums")}

                for(let act of actions){
                    let endpoint = '/api/website/' + act;
                    this.get_data(act, endpoint, params);
                }

                if(switch_dates){
                    this.refresh_items(item);
                }
            },
            get_data(req_action, endpoint, params, skip){
                const yesterday = moment().add(-1, 'days').format("YYYY-MM-DD");
                this.$http.get(endpoint, {params:params}).then(res => {
                    if (res.body) {
                        this._items = Object.keys(res.body).map(key => res.body[key]);
                        if (this._items.length === 0) {
                            this.warning(req_action.replace("_", " ") + ' data not found');
                            this.hide_load(req_action);
                        }else if(skip && this.disable_reload) {
                            return;
                        }else if(req_action === 'mediums'){
                            this.medium_items = this._items;
                            for (let key in this.medium_items) {
                                if(this.medium_items[key]['rule_mark'] === "-1"){
                                    this.medium_star_count ++;
                                }
                            }
                            if(this.item_selected.source == 'taboola'){
                                this.selectAllRoiChange(true)
                            }
                            if(!skip){
                                this.headClick(null, "sessions");
                                this.sortDesc = false;
                                this.medium_load = false;
                                this.medium_hide = false;
                            }

                        }else if(req_action === 'block_mediums'){

                            const result = this._items.filter
                            (
                                med => med.lost < 0 &&
                                med.ablock == '1' &&
                                med.block != '1' &&
                                med.data_date == yesterday
                            );

                            this.medium_block_items = result;
                            this.block_medium_star_count = result.length;

                        }else if (req_action === 'keywords') {
                            this.keyword_items = this._items;
                            for (let key in this.keyword_items) {
                                if(this.keyword_items[key]['rule_mark'] === "-1"){
                                    this.keyword_star_count ++;
                                }
                            }
                            if(this.item_selected.source == 'revcontent'){
                                this.selectAllRoiChange(true)
                            }
                            if(!skip) {
                                this.keyword_load = false;
                            }

                        }else if (req_action === 'countries'){
                            this.country_items = this._items;
                            for (let key in this.country_items) {
                                if(this.country_items[key]['rule_mark'] === "-1"){
                                    this.country_star_count ++;
                                }
                            }
                            if(!skip) {
                                this.country_load = false;
                            }

                        }else if (req_action === 'inpage'){
                            this.ipageviews_items = this._items;
                            for (let key in this.ipageviews_items) {
                                if(this.ipageviews_items[key]['mark'] === "-1"){
                                    this.ipageviews_star_count ++;
                                }
                            }
                            if(!skip) {
                                this.ipageviews_load = false;
                            }

                        }else if(req_action === 'devices'){
                            this.device_items = this._items;
                            this.device_load = false;

                        }else if (req_action === 'campaigns'){
                            this.campaigns_items = this._items;
                            if(!skip) {
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
            get_colors: function(params){
                params.page_type = 'campaign';
                this.$http.get('/api/website/colors', {params: params}).then(res => {
                    if (res.body) {
                        this.colors = Object.keys(res.body).map(key => res.body[key]);
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            navigate(action) {

                if(this.index_edit){
                    this.hideInput();
                }

                this.country_items = [];
                this.ipageviews_items = [];
                this.ad_content_items = [];
                this.rev_avg_cpc = '';
                this.disable_reload = true;

                if (action === "select" && !this.conflict) {
                    let select_index = this.campaign_id.split(' - ')[0];
                    if (select_index && parseInt(select_index) >= 0) {
                        window.stop();
                        if(!this.items[select_index]) {
                            this.refresh_items(this.item_selected);
                            this.initializeData(this.item_selected, this.date_start, this.date_end);
                        }
                        else{
                            this.item_selected = this.items[--select_index];
                            this.initializeData(this.items[select_index], this.date_start, this.date_end);
                        }
                        if(this.$parent.filter != ''){
                            this.$parent.filter = this.item_selected.campaign_id;
                        }

                    } else {
                        return;
                    }
                }

                if (this.item_selected) {
                    const campaign_id = this.item_selected.campaign_id;
                    const device = this.item_selected.device;

                    let index = this.items.findIndex(function (element) {
                        return element.campaign_id === campaign_id && element.device === device;
                    });
                    if ((action === "backward" && index === 0) || (action === "forward" && index > this.items.length)) {
                        return false;
                    } else if (action !== "select") {
                        this.conflict = true;
                        if (action === "backward") {
                            this.item_selected = this.items[--index];
                            this.campaign_id = this.items[index].campaign_id + ' - ' + this.items[index].name;
                        } else if (action === "forward") {
                            this.item_selected = this.items[++index];
                            this.campaign_id = this.items[index].campaign_id + ' - ' + this.items[index].name;
                        }
                        window.stop();
                        this.initializeData(this.items[index], this.date_start, this.date_end);

                    }
                    if(this.$parent.filter != ''){
                        this.$parent.filter = this.item_selected.campaign_id;
                    }
                    this.$parent.shown_item = ++index;
                }
            },
            refresh_items(item){

                if(!item){return;}

                let site_id = this.site_id !== null ? this.site_id : null;
                let device = item.device ? item.device : 'all';
                let source = item.source ? item.source : 'all';
                let start = this.date_filter[0] !== '' ? moment(this.date_filter[0]).format("YYYY-MM-DD") : moment(this.date_start).format("YYYY-MM-DD");
                let end = this.date_filter[1] !== '' ? moment(this.date_filter[1]).format("YYYY-MM-DD") : moment(this.date_end).format("YYYY-MM-DD");

                let params = {'site_id':site_id,'device':device,'source':source,'start':start,'end':end};

                item.start = start;
                item.end = end;

                this.refresh_campaign_summary(item);
                this.onClickRequest("campaigns", true);
                this.onClickRequest("countries", true);
                this.onClickRequest("devices", true);

                this.$http.get('/api/website/user_campaigns', {params: params}).then(res => {
                    if (res.body) {
                        this.items = Object.keys(res.body).map(key => res.body[key]);
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            showCampaigns(){
                window.stop();
                this.$parent.showMediumkey = false;
                this.activeName = 'medium';
                this.medium_items = [];
                this.medium_block_items = [];
                this.checked_roi_adjustment = [];
                this.roi_adjust_input = [];
                this.keyword_items = [];
                this.device_items = [];
                this.item_selected = '';
                this.items = [];
                this.index_edit =  false;
                this.sync =  false;
                this.firstInit = false;
                this.date_filter = [];
                this.device_selected = '';
                this.source_selected = false;
                this.ipageviews_star_count = 0;
                this.country_star_count = 0;
                this.block_medium_star_count = 0;
                this.medium_star_count = 0;
                this.keyword_star_count = 0;
                this.rev_editable = false;
                this.stop_campaign = false;
                this.editable = false;
                this.disable_reload = true;
                this.roi_adjust_loading = false;
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
                setTimeout(function(){
                    that.check_status_campaign();
                    that.stop_campaign = false;
                }, 10000);
            },
            submit_onchange(item){

                this.medium_load = true;
                this.keyword_load = true;
                this.country_load = true;
                this.ipageviews_load = true;

                let start = moment(this.date_start).format("YYYY-MM-DD");
                let end = moment(this.date_end).format("YYYY-MM-DD");
                let params = {'site_id':this.site_id,'source':item.source, 'device':item.device, 'start':start, 'end':end};

                this.$http.get('/api/website/user_campaigns', {params:params}).then(res => {
                    if (res.body) {
                        this._items = Object.keys(res.body).map(key => res.body[key]);
                        if (this._items.length === 0) {
                            this.notice("Sorry, No data was found for this website");
                            this.site_id = this.saved_site_id;
                        } else {
                            this.item_selected = this._items[0];
                            this.campaign_id = this._items[0].campaign_id + ' - ' + this._items[0].name;
                            this.saved_site_id = this.site_id;
                            this.items = this._items;
                            this.initializeData(this.item_selected,start,end,false);
                        }
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });

                //let new_item = {'site_id':this.site_id,'device':this.device_selected,'source':this.source_selected};
                //this.refresh_items(new_item);
                //const that = this;
                //setTimeout(function(){ that.stop = false;}, 2000);
            },
            update_keyword_status_revcontent(item, index){
                item.site_id = this.site_id;
                item.status = 'IN_PROCESS';
                this.$refs['k_tr_'+index][0].className = "event_block";
                this.disable_reload = false;

                this.$http.post('/api/website/revcontent/keyword/status_update', item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...',center: true,type: 'success'});
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function(){
                    that.check_status(item, 'keywords');
                    if(!that.disable_reload){
                        that.$refs['k_tr_'+index][0].className = "";
                    }
                }, 10000);
            },
            set_revcontent_cpc(item, new_value, action, index){

                if(new_value === null || action === "cancel"){
                    this.hideInput(index);
                    this.rev_editable = false;
                    this.rev_avg_cpc = '';
                    this.$message.error('Update canceled');
                    return;
                }

                if(new_value === parseFloat(item.avg_cpc) && action === "update"){
                    this.notice("Your entered the same value, Try again");
                    return;
                }

                this.$refs['k_tr_'+index][0].className = "event_block";
                this.disable_reload = false;

                item.site_id = this.site_id;
                item.new_bid = new_value;
                item.status = 'IN_PROCESS';

                const _index = index;

                this.$http.post('/api/website/revcontent/keyword/cpc_update', item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...',center: true,type: 'success'});
                        item.bid = new_value;
                        this.rev_avg_cpc = '';
                        this.hideInput(_index);
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function(){
                    that.check_status(item, 'keywords');
                    if(!that.disable_reload){
                        that.$refs['k_tr_'+index][0].className = "";
                    }
                }, 10000);
            },
            set_revcontent_budget(item){
                if(this.budget === parseFloat(item.budget)){
                    this.notice("Your entered the same value, No changes are made");
                    return;
                }
                this.budget_visible = false;
                item.status = 'IN_PROCESS';
                item.site_id = this.site_id;
                item.budget = this.budget;
                item.login_time =  this.$store.getters.getUser.loginTime;

                this.$http.post("/api/website/revcontent/campaign/change_budget", item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Campaign budget will update in few seconds'});
                    }else{
                        this.notice("Error has occurred, Please try again");
                    }
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
                const that = this;
                setTimeout(function(){
                    that.check_status_campaign();
                }, 10000);
            },
            update_campaign_cpc_taboola(item, new_value, action) {

                if(new_value === null || action === "cancel"){
                    this.$message.error('Update canceled');
                    this.editable = false;
                    this.avg_cpc = this.item_selected.bid;
                    return;
                }

                if(new_value === parseFloat(item.bid) && action === "update"){
                    this.notice("You entered the same value, No changes were made");
                    return;
                }else if(new_value === 0){
                    this.notice("Please enter value greater then 0");
                    return;
                }

                if((new_value + "").split(".")[1].length > 3) {
                    this.notice("'CPC Bid' sum must have no more than 3 decimal positions");
                    return;
                }

                item.site_id = this.site_id;
                item.new_bid = new_value;
                item.login_time =  this.$store.getters.getUser.loginTime;
                this.item_selected.status = 'IN_PROCESS';
                this.editable = false;

                this.$http.post("/api/website/taboola/campaign/bid_update", item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...',center: true,type: 'success'});
                        this.bid = '';
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
                const that = this;
                setTimeout(function(){
                    that.check_status_campaign();
                    that.stop_campaign = false;
                }, 10000);
            },
            update_medium_status(item, index) {
                this.$refs['m_tr_'+index][0].className = "event_block";
                this.disable_reload = false;

                item.site_id = this.site_id;
                item.status = 'IN_PROCESS';
                let endpoint = '';

                if(item.source === 'taboola'){
                    endpoint = '/api/website/mediums/taboola/toggle';
                }else if(item.source === 'revcontent'){
                    endpoint = '/api/website/mediums/revcontent/toggle';
                }

                this.$http.post(endpoint, item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...',center: true,type: 'success'});
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function(){
                    that.check_status(item, 'mediums');
                    if(!that.disable_reload){
                        that.$refs['m_tr_'+index][0].className = "";
                    }
                }, 10000);
            },
            update_medium_bid_taboola(item, bid, index){
                this.$refs['m_tr_'+index][0].className = "event_block";
                this.disable_reload = false;

                item.site_id = this.site_id;
                item.bid = bid;
                item.status = 'IN_PROCESS';

                this.$http.post('/api/mediums/taboola/update', item).then(res => {
                    if (res.body === "True") {
                        this.$message({message: 'Request Pending...',center: true,type: 'success'});
                        this.close_bid_mod(index);
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function(){
                    that.check_status(item, 'mediums');
                    if(!that.disable_reload){
                        that.$refs['m_tr_'+index][0].className = "";
                    }
                }, 10000);
            },
            BlockMediumsBulk(){
                this.disable_reload = false;
                this.bulk_update = true;

                let mediums = this.checked_mediums;
                for(let medium of mediums){
                    medium.status = 'IN_PROCESS';
                }

                let endpoint = '/api/website/mediums/taboola/toggle_bulk';
                this.$http.post(endpoint, this.checked_mediums).then(res => {
                    if (res.body === "True") {
                        this.checked_mediums = [];
                        this.bulk_update = false;
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });

                const that = this;
                setTimeout(function(){
                    that.check_status(mediums[0], 'block_mediums');
                }, 10000);
            },
            AdjustMediumsBulk(){
                let mediums = this.checked_roi_adjustment;
                let endpoint = '/api/website/mediums/taboola/bid_bulk';

                for(let medium of mediums){
                    medium.status = 'IN_PROCESS';
                }

                this.$http.post(endpoint, this.checked_roi_adjustment).then(res => {
                    if (res.body === "True") {
                        this.roi_adjust_loading = false;
                        this.checked_roi_adjustment = [];
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
                const that = this;
                setTimeout(function(){
                    that.check_status(mediums[0], 'mediums');
                }, 10000);
            },
            AdjustKeywordsBulk(){
                let keywords = this.checked_roi_adjustment;
                let endpoint = '/api/website/keywords/revcontent/bid_bulk';

                for(let keyword of keywords){
                    keyword.status = 'IN_PROCESS';
                }

                this.$http.post(endpoint, this.checked_roi_adjustment).then(res => {
                    if (res.body === "True") {
                        this.roi_adjust_loading = false;
                        this.checked_roi_adjustment = [];
                    }else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
                const that = this;
                setTimeout(function(){
                    that.check_status(keywords[0], 'keywords');
                }, 10000);
            },
            selectAllRoiChange(fast){
                this.roi_apply = true;
                const that = this;
                setTimeout(function(){
                    for(let i in that.roi_adjust_input){
                        that.roi_adjust_input[i] = that.roi_adjust;
                    }
                    that.roi_apply = false;
                }, fast?0:500);
            },
            check_status(item, action){
                let params = {
                    'campaign_id':item.campaign_id,
                    'device': item.device,
                    'source': item.source,
                    'site_id': item.site_id,
                    'start': moment(this.date_start).format("YYYY-MM-DD"),
                    'end': moment(this.date_end).format("YYYY-MM-DD")
                };
                this.get_data(action, '/api/website/' + action, params, true);
            },
            check_status_campaign(){
                let params = this.item_selected;
                this.$http.get('/api/website/check_status', {params}).then(res => {
                    if (res.body) {
                        this.item_selected = Object.keys(res.body).map(key => res.body[key])[0];
                        const campaign_id = this.item_selected.campaign_id;
                        let index = this.items.findIndex(function (element) {return element.campaign_id === campaign_id});
                        this.items[index].status = this.item_selected.status;
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            active_update_medium_bid_taboola(item, action, index, prcnt=0.0){
                let current_bid = item.bid ? item.bid : 1;
                let new_bid = current_bid;
                let _step = 0.1;
                if(action === "up"){
                  new_bid = Math.round((parseFloat(current_bid) + _step)*1000) / 1000;
                }else if (action === "down") {
                  new_bid = Math.round((parseFloat(current_bid) - _step)*1000) / 1000;
                }else if (action === "default"){
                  new_bid = 1.0;
                }else if (action === "mod"){
                    new_bid = (100.0 + parseFloat(prcnt)) / 100.0
                }
                if (new_bid > 1.5 || new_bid < 0.5){
                    this.notice("Bid range is +50% or -50%");
                    return;
                }
                item.bid = new_bid;
                this.bid = item.bid;
                this.update_medium_bid_taboola(item, new_bid, index);
            },
            refresh_campaign_summary(params) {
                this.$http.get('/api/website/refresh_campaign', {params: params}).then(res => {
                    if (res.body) {
                        this.item_selected = Object.keys(res.body).map(key => res.body[key])[0];
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            applyRoiAdjust(){
                this.roi_adjust_loading = true;
                for(let item of this.checked_roi_adjustment){

                    let val = this.roi_adjust_input[item.index];
                    let uv = item.device == 'desktop' ? 100 : 1000;
                    let bid = item.source == 'taboola' ? this.item_selected.bid : this.item_selected.avg_cpc;
                    let item_bid = item.source == 'taboola' ? this.calc_percentage(item.bid) : item.bid;

                    // Real Bid Adjustment
                    let real_bid = (item.final_uv / uv / (item.roi + 1)) / item_bid;
                    // Target Bid
                    let target_bid = ((item.final_uv / uv) / (val + 1)) / real_bid;
                    // Bid Adjustment
                    let bid_adjust = ((target_bid / bid) - 1);

                    if(item.source == 'taboola'){
                        bid_adjust = 1 + bid_adjust;
                        if(bid_adjust > 1.5){
                            item.bid_adjust = 1.5;
                        }else if(bid_adjust < 0.5){
                            item.bid_adjust = 0.5;
                        }else {
                            item.bid_adjust = bid_adjust;
                        }

                    }else if(item.source == 'revcontent'){
                        item.bid_adjust = Math.floor(target_bid * 100) / 100;
                    }
                    console.log("New bid: " + item.bid_adjust);
                    console.log("------------------------");
                }

                if(this.item_selected.source === 'taboola'){
                    this.AdjustMediumsBulk();
                }else if(this.item_selected.source === 'revcontent'){
                    this.AdjustKeywordsBulk();
                }
            },
            mediums_index_init(){
                for (let [index] in this.medium_items) {
                    this.medium_items[index]['index'] = index;
                }
            },
            keywords_index_init(){
                for (let [index] in this.keyword_items) {
                    this.keyword_items[index]['index'] = index;
                }
            },
            tabClick(tab) {
                if (tab.label.toLowerCase() === "keywords") {
                    this.keyword_hide = false;
                    this.device_hide = true;
                    this.medium_hide = true;
                    this.country_hide = true;
                    this.ipageviews_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase() === "mediums") {
                    this.medium_hide = false;
                    this.device_hide = true;
                    this.keyword_hide = true;
                    this.country_hide = true;
                    this.ipageviews_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase().replace(" ","_") === "increase_pageviews") {
                    this.ipageviews_hide = false;
                    this.device_hide = true;
                    this.country_hide = true;
                    this.medium_hide = true;
                    this.keyword_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase() === "content_ad") {
                    this.content_ad_hide = false;
                    this.device_hide = true;
                    this.ipageviews_hide = true;
                    this.country_hide = true;
                    this.medium_hide = true;
                    this.keyword_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase() === "campaigns") {
                    this.onClickRequest("campaigns");
                    this.tab_init.push("campaigns");
                    this.campaigns_hide = false;
                    this.country_hide = true;
                    this.device_hide = true;
                    this.medium_hide = true;
                    this.ipageviews_hide = true;
                    this.keyword_hide = true;
                    this.content_ad_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase() === "countries") {
                    this.onClickRequest("countries");
                    this.tab_init.push("countries");
                    this.country_hide = false;
                    this.device_hide = true;
                    this.medium_hide = true;
                    this.ipageviews_hide = true;
                    this.keyword_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase().replace(" ","_") === "mobile_devices") {
                    this.onClickRequest("devices");
                    this.tab_init.push("devices");
                    this.device_hide = false;
                    this.ipageviews_hide = true;
                    this.country_hide = true;
                    this.medium_hide = true;
                    this.keyword_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                    this.medium_block_hide = true;
                } else if (tab.label.toLowerCase().replace(" ","_") === "bulk_medium block") {
                    this.medium_block_hide = false;
                    this.country_hide = true;
                    this.device_hide = true;
                    this.medium_hide = true;
                    this.ipageviews_hide = true;
                    this.keyword_hide = true;
                    this.content_ad_hide = true;
                    this.campaigns_hide = true;
                }
            },
            onClickRequest(tab, refresh){
                if (!this.tab_init.includes(tab) || refresh){
                    let params = {
                    'campaign_id':this.item_selected.campaign_id,
                    'device': this.item_selected.device,
                    'source': this.item_selected.source,
                    'site_id': this.item_selected.site_id,
                    'start': moment(this.date_start).format("YYYY-MM-DD"),
                    'end': moment(this.date_end).format("YYYY-MM-DD")
                };
                    let endpoint = '/api/website/' + tab;
                    this.get_data(tab, endpoint, params);
                }
            },
            headClick(field, key){
                if (key === this.sort) {
                    this.sortDesc = !this.sortDesc;
                }
                this.sort = key;
            },
            headClick_pageviews(field, key){
                if (key === this.sort_pageviews) {
                    this.sortDesc_pageviews = !this.sortDesc_pageviews;
                }
                this.sort_pageviews = key;
            },
            showInput(index){
                this.$refs['rev-'+index][0].$el.className = this.$refs['rev-'+index][0].$el.className.replace("tb-hide","rev_edit");
                this.$refs['rev-check-'+index][0].className = this.$refs['rev-check-'+index][0].className.replace("tb-hide", "edit-bid");
                this.$refs['rev-close-'+index][0].className = this.$refs['rev-close-'+index][0].className.replace("tb-hide", "edit-bid");
            },
            hideInput(){
                if(this.$refs['rev-'+this.index_edit][0]){
                    this.$refs['rev-'+this.index_edit][0].$el.className = this.$refs['rev-'+this.index_edit][0].$el.className.replace("rev_edit","tb-hide");
                    this.$refs['rev-check-'+this.index_edit][0].className = this.$refs['rev-check-'+this.index_edit][0].className.replace("edit-bid","tb-hide");
                    this.$refs['rev-close-'+this.index_edit][0].className = this.$refs['rev-close-'+this.index_edit][0].className.replace("edit-bid","tb-hide");
                }
            },
            make_editable(source, index, bid){
                if(source === "taboola"){
                    if(bid){this.bid = bid;}
                    this.editable = true;
                } else if(source === "revcontent" && !this.index_edit){
                    if(bid){this.rev_avg_cpc = bid;}
                    if(this.index_edit === 0){this.hideInput();}
                    this.index_edit = index;
                    this.showInput(index);
                    this.rev_editable = true;
                }else if(this.index_edit){
                    this.rev_avg_cpc = bid;
                    this.avg_cpc = bid;
                    // Hide previous selected input
                    this.hideInput(index);
                    // Show current selected input
                    this.showInput(index);
                    this.index_edit = index;
                    this.rev_editable = true;
                }
            },
            keypressed(event){
                if(this.stop){return false;}
                if(event.keyCode === 37){
                    // Left
                    this.navigate('backward');
                }else if(event.keyCode === 39){
                    // Right
                    this.navigate('forward');
                }
            },
            calc_rev_diff(item) {
                let previous = item._hb_user_value * item._sessions;
                let current = item.hb_user_value * item.sessions;
                return Math.abs(current - previous) / (previous) * 100.0;
            },
            calc_bid_diff(item) {
                let previous = item._cost / item._sessions;
                let current = item.cost / item.sessions;
                return Math.abs(current - previous) / (previous) * 100.0;

            },
            open_bid_mod(index){
                this.expend = true;
                if(this.bid_mod_index >= 0 && this.bid_mod_index !== false){
                    this.close_bid_mod(this.bid_mod_index, true);
                }
                this.bid_mod_index = index;
                this.bid_mod_change = '';
                this.$refs['taboola-'+index][0].className = this.$refs['taboola-'+index][0].className.replace("tb-hide","edit_bid");
            },
            close_bid_mod(index, skip){
                this.expend = !!skip;
                this.bid_mod_index = index;
                this.bid_mod_change = '';
                this.$refs['taboola-'+index][0].className = this.$refs['taboola-'+index][0].className.replace("edit_bid","tb-hide");
            },
            calc_percentage(bid) {
                let cbid = this.item_selected.bid ? this.item_selected.bid : this.item_selected.avg_cpc;
                let round_cpc = Math.round(cbid*1000)/1000;
                let res = round_cpc * bid;
                return Math.round(res*1000)/1000;
            },
            calc_percentage_diff(item) {
                let prcnt = item * 100;
                return parseFloat(item) < 1 ?
                    "-" + (Math.round((100 - prcnt)*1000)/1000).toString() :
                    "+" + (Math.round((prcnt - 100)*1000)/1000).toString();
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
            deleteNoticeMediums(){
                this.$confirm('You Are About To Block ' + this.checked_mediums.length + ' Mediums, Continue ?', 'Warning', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'error'
                }).then(() => {
                    this.BlockMediumsBulk();
                })
            },
            roiAdjustNotice(){
                let msg = '';
                let type = this.item_selected.source == 'taboola' ? 'mediums' : 'keywords';
                if(this.checked_roi_adjustment.length == 1){
                    let index = this.checked_roi_adjustment[0].index;
                    let item = this.checked_roi_adjustment[0];
                    let val = parseFloat(this.roi_adjust_input[index]).toFixed(2);
                    msg = "You are about to adjust " + item.medium + " from "+ item.roi.toFixed(3) +" ROI to " + val + " ROI, Continue?"
                }else if(this.checked_roi_adjustment.length > 1){
                    msg = "You are about to adjust " + this.checked_roi_adjustment.length + " " + type + ", Continue?"
                }
                this.$confirm(msg, 'Warning', {
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                    center: true
                }).then(() => {
                    this.$message({
                        type: 'success',
                        message: 'Adjustment in process'
                    });
                    this.applyRoiAdjust();
                }).catch(() => {
                  this.$message({
                        type: 'info',
                        message: 'Adjustment canceled'
                    });
                });
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
            success_msg(action) {
                this.$message({
                    message: action,
                    type: 'success',
                    duration: 5000
                });
            },
            hide_load(typ){
                if (typ === 'mediums'){
                    this.medium_load = false;
                    this.medium_hide = true;
                }else if(typ === 'keywords'){
                    this.keyword_load = false;
                    this.keyword_hide = true;
                }else if(typ === 'countries'){
                    this.country_load = false;
                    this.country_hide = true;
                }else if(typ === 'inpage'){
                    this.ipageviews_load = false;
                    this.ipageviews_hide = true;
                }else if(typ === 'devices'){
                    this.device_load = false;
                    this.device_hide = true;
                }else if(typ === 'campaigns'){
                    this.campaigns_load = false;
                    this.campaigns_hide = true;
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
            color(item, key, skip){
                if (!item){return}
                item.source = item.source.toLowerCase().replace('.com','');
                let elem = null;
                if (skip){
                    elem = this.colors.find(color =>
                        color.source == item.source &&
                        color.field == key &&
                        color.from <= item[key] && item[key] <= color.to
                    );
                }else {
                    elem = this.colors.find(color =>
                        color.source == item.source &&
                        color.device == item.device &&
                        color.field == key &&
                        color.from <= item[key] && item[key] <= color.to
                    );
                }

                if (elem){
                    return elem.color + ' label'
                }else {
                    return ''
                }
            }
        },
        computed: {
            _medium_items() {
                if (!this.medium_items) {
                    return [];
                }

                let medium_items = this.medium_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.medium_filter && this.medium_filter.length > 0) {
                    const regex = new RegExp('.*' + this.medium_filter + '.*', 'ig');
                    medium_items = medium_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    medium_items = medium_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.mperPage) {
                    medium_items = medium_items.slice((this.medium_currentPage - 1) * this.mperPage, this.medium_currentPage * this.mperPage);
                }

                return medium_items;
            },
            _medium_block_items() {
                if (!this.medium_block_items) {
                    return [];
                }

                let medium_items = this.medium_block_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.medium_block_filter && this.medium_block_filter.length > 0) {
                    const regex = new RegExp('.*' + this.medium_block_filter + '.*', 'ig');
                    medium_items = medium_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    medium_items = medium_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    medium_items = medium_items.slice((this.medium_block_currentPage - 1) * this.perPage, this.medium_block_currentPage * this.perPage);
                }

                return medium_items;
            },
            _keywords_items() {
                if (!this.keyword_items) {
                    return [];
                }

                let keyword_items = this.keyword_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.keyword_filter && this.keyword_filter.length > 0) {
                    const regex = new RegExp('.*' + this.keyword_filter + '.*', 'ig');
                    keyword_items = keyword_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    keyword_items = keyword_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    keyword_items = keyword_items.slice((this.keyword_currentPage - 1) * this.perPage, this.keyword_currentPage * this.perPage);
                }

                return keyword_items;
            },
            _country_items() {
                if (!this.country_items) {
                    return [];
                }

                let country_items = this.country_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.country_filter && this.country_filter.length > 0) {
                    const regex = new RegExp('.*' + this.country_filter + '.*', 'ig');
                    country_items = country_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    country_items = country_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    country_items = country_items.slice((this.country_currentPage - 1) * this.perPage, this.country_currentPage * this.perPage);
                }

                return country_items;
            },
            _ipageviews_items() {
                if (!this.ipageviews_items) {
                    return [];
                }

                let ipageviews_items = this.ipageviews_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.inpage_filter && this.inpage_filter.length > 0) {
                    const regex = new RegExp('.*' + this.inpage_filter + '.*', 'ig');
                    ipageviews_items = ipageviews_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort_pageviews) {
                    ipageviews_items = ipageviews_items.sort((a, b) => {
                        const r = fix(a[this.sort_pageviews]).localeCompare(fix(b[this.sort_pageviews]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc_pageviews ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    ipageviews_items = ipageviews_items.slice((this.ipageviews_currentPage - 1) * this.perPage, this.ipageviews_currentPage * this.perPage);
                }

                return ipageviews_items;
            },
            _device_items() {
                if (!this.device_items) {
                    return [];
                }

                let device_items = this.device_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.device_filter && this.device_filter.length > 0) {
                    const regex = new RegExp('.*' + this.device_filter + '.*', 'ig');
                    device_items = device_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    device_items = device_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    device_items = device_items.slice((this.device_currentPage - 1) * this.perPage, this.device_currentPage * this.perPage);
                }

                return device_items;
            },
            _ad_content_items(){
                if (!this.ad_content_items) {
                    return [];
                }

                let ad_content_items = this.ad_content_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.inpage_filter && this.inpage_filter.length > 0) {
                    const regex = new RegExp('.*' + this.inpage_filter + '.*', 'ig');
                    ad_content_items = ad_content_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort_pageviews) {
                    ad_content_items = ad_content_items.sort((a, b) => {
                        const r = fix(a[this.sort_pageviews]).localeCompare(fix(b[this.sort_pageviews]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc_pageviews ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    ad_content_items = ad_content_items.slice((this.ad_content_currentPage - 1) * this.perPage, this.ad_content_currentPage * this.perPage);
                }

                return ad_content_items;
            },
            _campaigns_items() {
                if (!this.campaigns_items) {
                    return [];
                }

                let campaigns_items = this.campaigns_items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.campaigns_filter && this.campaigns_filter.length > 0) {
                    const regex = new RegExp('.*' + this.campaigns_filter + '.*', 'ig');
                    campaigns_items = campaigns_items.filter(item => regex.test(fix(item)));
                }

                // Apply Sort
                if (this.sort) {
                    campaigns_items = campaigns_items.sort((a, b) => {
                        const r = fix(a[this.sort]).localeCompare(fix(b[this.sort]), undefined, {
                            numeric: true,
                            sensitivity: 'base'
                        });
                        return this.sortDesc ? r : r * -1;
                    });
                }

                // Apply pagination
                if (this.perPage) {
                    campaigns_items = campaigns_items.slice((this.campaigns_currentPage - 1) * this.perPage, this.campaigns_currentPage * this.perPage);
                }

                return campaigns_items;
            },
            selectAll: {
                get: function () {
                    return this.medium_block_items ? this.checked_mediums.length == this.medium_block_items.length : false;
                },
                set: function (value) {
                    let selected = [];
                    if (value) {
                        this.medium_block_items.forEach(function (medium) {
                            selected.push(medium);
                        });
                    }
                    this.checked_mediums = selected;
                }
            },
            selectAllRoi:{
                get: function () {
                    return this.roi_adjust_input_length ? this.checked_roi_adjustment.length == this.roi_adjust_input_length : false;
                },
                set: function (value) {
                    let selected = [];
                    if (value) {
                        this.medium_items.forEach(function (medium) {
                            if(medium.sessions >= 100){selected.push(medium);}
                        });
                    }
                    this.checked_roi_adjustment = selected;
                    this.roi_adjust_input_length = this.checked_roi_adjustment.length
                }
            },
            selectAllRoiRev:{
                get: function () {
                    return this.roi_adjust_input_length ? this.checked_roi_adjustment.length == this.roi_adjust_input_length : false;
                },
                set: function (value) {
                    let selected = [];
                    if (value) {
                        this.keyword_items.forEach(function (keyword) {
                            if(keyword.sessions >= 100){selected.push(keyword);}
                        });
                    }
                    this.checked_roi_adjustment = selected;
                    this.roi_adjust_input_length = this.checked_roi_adjustment.length

                }
            },
        },
        filters: {
            divide : function (val, device, factor) {
                if(device == 'mobile'){
                    return val / 1000;
                }else if(!factor) {
                    return val / 100;
                }else {
                    return val;
                }
            },
            _format(value,fix){
                if ((!value && value !== 0) || !fix) {
                    return '';
                }
                return parseFloat(value).toFixed(fix);
            }
        }
    }
</script>

<style>
    @import "../../assets/styles/pages/_MediumKey.scss";
</style>
