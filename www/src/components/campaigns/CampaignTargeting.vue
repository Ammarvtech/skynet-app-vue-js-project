<template>
    <div id="targeting" v-loading.fullscreen.lock="loading">
        <h1>Campaign Targeting <span class="cid" v-show="cid"> Campaign No. {{cid}}</span></h1>

        <div class="row menu-tabs">
            <el-tabs type="border-card" v-model="activeName">
                <el-tab-pane label="Properties" name="properties">
                    <span slot="label">
                        <router-link
                                :to="{path: `/campaign/properties/${cid}?op=update`}">Properties</router-link></span>
                    Properties
                </el-tab-pane>
                <el-tab-pane label="Inventory" name="inventory">
                    <span slot="label">
                        <router-link :to="{path: `/campaign/inventory/${cid}`}">Inventory</router-link></span>
                    Inventory
                </el-tab-pane>
                <el-tab-pane label="Targeting" name="targeting">
                    <span slot="label">
                        <router-link :to="{path: `/campaign/targeting/${cid}`}">Targeting</router-link></span>
                    <el-input class="filter" placeholder="Search" v-model="filter"></el-input>
                    <el-button class="wo_button" type="text" @click="promptWidgetOptimization">
                        <i class="fa fa-sliders"></i>
                        Widget Optimization
                        <span id="total" :class="isBlacklist ? 'blacklist' : 'target'">{{widget_ids.length}}</span>
                    </el-button>
                </el-tab-pane>
            </el-tabs>
        </div>

        <div>
            <table class="table table-striped table-hover">
                <thead>
                <tr>
                    <th>
                        <el-checkbox @change="checkAll"></el-checkbox>
                    </th>
                    <th>Targets</th>
                    <th class="bid">
                        <span :class="[!_checked ? '' : 'hide']">Max CPC Bid</span>
                        <div v-model="showGlobalBid" :class="[_checked ? '' : 'hide']">
                            <el-input-number v-model="globalBid"
                                             :step="step"
                                             size="small"></el-input-number>
                            <el-button @click="updateAll" type="success" size="small">OK
                            </el-button>
                        </div>
                    </th>
                    <th>Bid Range</th>
                    <th>Clicks/Week</th>
                    <th>Avg CPC</th>
                    <th>Status</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(keyword, index) in _keywords">
                    <td>
                        <el-checkbox v-model="keywords[index].edited" @click="edit_keyword(index,'checkbox')">
                        </el-checkbox>
                    </td>
                    <td>{{keywords[index].tag_name}}</td>
                    <td class="bid" @click="edit_keyword(index, 'field')">
                        <span :class="[!keywords[index].edited ? '' : 'hide']">${{keywords[index].bid}}</span>
                        <el-input-number :class="[keywords[index].edited ? '' : 'hide']" :step="step" size="small"
                                         v-model="keywords[index].bid">
                        </el-input-number>
                        <el-button :class="[keywords[index].edited ? '' : 'hide']" type="success" size="small"
                                   @click="updateSingleBid(keywords[index])">OK
                        </el-button>
                    </td>
                    <td>${{keywords[index].min_bid}} - ${{keywords[index].max_bid}}</td>
                    <td>{{keywords[index].clicks_week}}</td>
                    <td>{{keywords[index].avg_cpc}}</td>
                    <td>
                        <el-switch v-model="keywords[index].enabled === 'enabled'"
                                   @change="setStatus(keywords[index])"
                                   active-color="#13ce66"
                                   inactive-color="#ff4949"
                        >
                        </el-switch>
                    </td>
                </tr>
                </tbody>
            </table>
            <el-button v-show="_updating" type="success" @click="Dealer">{{_action}}</el-button>
            <el-button v-show="!_updating" type="success" @click="">Update</el-button>
        </div>
    </div>

</template>


<script>
    import optimization from '../utils/OptimizationPrompt.vue'

    export default {
        components: {
            optimization
        },
        data() {
            return {
                filter: null,
                activeName: 'targeting',
                keywords: [],
                showOpt: false,
                campaign: [],
                widget_ids: [],
                widgets_action: 'target',
                cid: this.$route.params.campaignId,
                step: 0.01,
                globalBid: 0.03,
                showGlobalBid: false,
                globalCheck: false,
                loading: false,
                action: ''
            }
        },
        mounted() {
            this.getKeywords();
            this.getCampaignWidgets();
            this.getOptimizerType();
        },
        computed: {
            isBlacklist() {
                return this.widgets_action === 'blacklist'
            },
            _updating() {
                if (this.cid) {
                    return this.cid.startsWith("TBD")
                }
            },
            _checked() {
                for (let keyword of this.keywords) {
                    if (keyword.edited) {
                        this.showGlobalBid = true
                        return true
                    }
                    this.showGlobalBid = false
                }
            },
            _action() {
                this.action = this.cid.includes("TBD") ? "create" : "update"
                return this.action
            },
            _keywords() {
                if (!this.keywords) {
                    return [];
                }

                let keywords = this.keywords;

                //
                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                // Apply filter
                if (this.filter && this.filter.length > 0) {
                    keywords = keywords.filter(item =>
                        item.tag_name.toLowerCase().includes(this.filter.toLowerCase())
                    );
                }

                return keywords
            }
        },
        methods: {
            Dealer() {
                this.$http.post('/api/campaignManager/create', {
                    campaign_id: this.cid,
                    keywords: this.keywords,
                    action: this._action
                }).then(res => {
                    console.log(res)
                    this.cid = res.body.cid;
                    this.$route.params.campaignId = this.cid;
                    this.$router.push({path: `/campaigns`});
                }), res => {
                    console.log("error: " + res)
                }
            },
            updateSingleBid(keyword) {
                this.$http.post('/api/campaignManager/targeting', {
                    campaign_id: this.cid,
                    multiple: false,
                    keywords: keyword,
                    action: this._action
                }).then(res => {
                    keyword.edited = false;
                    this.$notify({
                        title: 'Notice',
                        message: `${keyword.tag_name} status updated to: <b> ${new_status} </b>`,
                        duration: 0,
                        type: 'success'
                    });

                    console.log(res.body)
                }, response => {
                    // error callback
                    console.log("error")
                })
            },
            updateAll() {
                // TODO: waiting for spapi support

                this.loading = true
                let updated = []
                for (let keyword of this.keywords) {
                    if (keyword.edited) {
                        keyword.bid = this.globalBid
                        updated.push({
                            "id": keyword.tag_id,
                            "bid": keyword.bid
                        })
                    }
                }

                this.$http.post('/api/campaignManager/targeting', {
                    campaign_id: this.cid,
                    set_status: false,
                    multiple: true,
                    keywords: this.keywords,
                    bid: this.globalBid,
                    action: this._action
                }).then(res => {
                    this.loading = false;
                    for (let keyword of this.keywords) {
                        keyword.edited = false
                    }

                    this.$notify({
                        title: 'Great!',
                        message: `Targeting updated to: ${this.globalBid}`,
                        duration: 0,
                        type: 'success'
                    });

                    console.log(res.body)
                }, response => {
                    // error callback
                    this.loading = false
                    console.log("error")
                })
            },
            setStatus(keyword) {
                keyword.enabled = this.switchStatus(keyword);
                this.loading = true;
                this.$http.post('/api/campaignManager/targeting/status', {
                    campaign_id: this.cid,
                    keyword: keyword,
                    action: this._action
                }).then(res => {
                    this.loading = false;
                    keyword.edited = false;
                    this.$notify({
                        title: 'Notice',
                        message: `${keyword.tag_name} status updated to: ${keyword.enabled}`,
                        duration: 0,
                        type: 'success'
                    });
                }, response => {
                    this.loading = false;

                    // error callback
                    console.log("error")
                })
            },
            getKeywords() {
                this.loading = true;
                this.$http.get(`/api/campaignManager/targeting?cid=${this.cid}`).then(res => {
                    let targetingData = res.body.targeting;
                    for (let keyword of targetingData) {
                        keyword.edited = false;
                    }
                    this.keywords = targetingData;
                    this.loading = false;
                    return this.keywords
                }, res => {
                    this.loading = false;
                    // error callback
                    console.log("error")
                })
            },
            getCampaignWidgets() {
                this.$http.get(`/api/campaignManager/wio?cid=${this.cid}`).then(res => {
                    let w_ids = [];
                    if (res.body.widget_ids) {
                        w_ids = res.body.widget_ids;
                    }
                    if (w_ids) {
                        this.widget_ids = w_ids
                    }
                    else {
                        console.log("no widget ids")
                    }
                }, res => {
                    // error callback
                    console.log("error")
                })
            },
            getOptimizerType() {
                this.$http.get(`/api/campaignManager/wio/type?cid=${this.cid}`).then(res => {
                    this.widgets_action = res.body.type ? res.body.type : 'target'
                }, res => {
                    // error callback
                    console.log("error: " + res)
                })
            },
            promptWidgetOptimization() {
                this.showOpt = !this.showOpt;
                const h = this.$createElement;
                this.$msgbox({
                    title: 'Widget Optimization',
                    message: h(optimization),
                    campaign_id: this.cid,
                    widget_ids: this.widget_ids,
                    action: this.widgets_action,
                    showCancelButton: true,
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    beforeClose: (action, instance, done) => {
                        if (action === 'confirm') {
                            instance.confirmButtonLoading = true;
                            instance.confirmButtonText = 'Loading...';
                            setTimeout(() => {
                                done();
                                setTimeout(() => {
                                    instance.confirmButtonLoading = false;
                                }, 300);
                            }, 200);
                        } else {
                            done();
                        }
                    }
                }).then(action => {
                    this.getOptimizerType();
                    this.getCampaignWidgets();
                });
            },
            checkAll() {
                this.globalCheck = !this.globalCheck;
                for (let keyword of this.keywords) {
                    keyword.edited = this.globalCheck
                }
            },
            updateWidgetAction() {

                this.widgets_action = this.widgets_action === "blacklist" ? "target" : "blacklist";
            },
            switchStatus(keyword) {
                return keyword.enabled === "enabled" ? "disabled" : "enabled";
            },
            edit_keyword(index, field) {
                if (field === 'checkbox') {
                    this.$set(this.keywords[index], 'edited', !this.keywords[index]);
                    return;
                }
                this.$set(this.keywords[index], 'edited', true)
            }
        },
        watch: {
            keywords: {
                handler: function (val, oldVal) {
                },
                deep: true
            }
        }
    }
</script>

<style>
    .menu-tabs {
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .el-message-box__wrapper {
        overflow: auto;
    }

    .cid {
        font-size: 15px;
        float: right;
    }

    #targeting .el-tabs {
        border-bottom-color: #f5f5f5;
    }

    #targeting .filter {
        max-width: 20%;
    }

    #targeting .wo_button {
        float: right;
        background: #13ce66;
        color: #FFF;
        padding: 10px 20px;
    }

    .el-message-box {
        width: 45% !important;
        margin: 15px;
    }

    .hide {
        display: none;
    }

    .bid {
        display: flex;
    }

    .menu-tabs > div > div {
        pointer-events: none !important;
    }

    .el-tabs__item a, .el-tabs__content div {
        pointer-events: all;
    }

    span#total {
        border-radius: 10px;
        padding: 3px;
        min-width: 10px;
    }

    .target {
        background-color: #5cb85c;
    }

    .blacklist {
        background-color: #d9534f;
    }
</style>

