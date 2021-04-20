<template>
    <div id="campaign_properties">
        <h1>Campaign Properties <span class="cid" v-show="action === 'update'"> Campaign No. {{cid}}</span></h1>

        <!--TABS-->
        <div class="row menu-tabs" v-show="$route.query.op === 'update'">
            <el-tabs type="border-card" v-model="activeName">
                <el-tab-pane label="Properties" name="properties">
                    <span slot="label">
                        <router-link
                                :to="{path: `/campaign/properties/${cid}?op=update`}">Properties</router-link></span>
                    <div class="row">
                        <div class="col-xs-3">
                            <el-button @click="submitForm('form')" type="primary"
                                       :class="true ? '' : 'wait'">
                                Clone <i v-bind:class="this.loading ? '' : 'wait'" class="el-icon-loading"></i>
                            </el-button>
                        </div>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="Inventory" name="inventory">
                    <span slot="label">
                        <router-link :to="{path: `/campaign/inventory/${cid}`}">Inventory</router-link></span>
                    Inventory
                </el-tab-pane>
                <el-tab-pane label="Targeting" name="targeting">
                    <span slot="label">
                        <router-link :to="{path: `/campaign/targeting/${cid}`}">Targeting</router-link>
                     </span>
                </el-tab-pane>
            </el-tabs>
        </div>
        <!--/TABS-->

        <hr class="style-one">


        <!--Edit Campaign Form start-->

        <el-form :model="form" :rules="rules" ref="form" label-width="120px">

            <h2 class="section_title">OMG Settings</h2><br>
            <hr class="style-one">

            <div class="row">
                <el-form-item label="Website" prop="website">
                    <el-select v-model="form.website_id" placeholder="select website" filterable
                               :disabled="action==='update'">
                        <el-option
                                v-for="website in websites"
                                :label="website.website_name"
                                :value="website.website_id"
                                :key="website.website_id"
                        >{{website.website_name}}
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Provider" prop="provider">
                    <el-select v-model="form.provider_name" placeholder="select provider"
                               :disabled="action==='update'">
                        <el-option v-for="provider in providers"
                                   :label="provider.provider_name"
                                   :value="provider.provider_name"
                                   :key="provider.provider_name">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Accounts" prop="account">
                    <el-select v-model="form.account_id" placeholder="Select account" filterable
                               :disabled="action==='update'">
                        <el-option v-for="account in accounts"
                                   :label="account.account_name"
                                   :key="account.account_id"
                                   :value="account.account_id">
                        </el-option>
                    </el-select>
                </el-form-item>
            </div>

            <h2 class="section_title">Basic Info</h2><br>
            <hr class="style-one">

            <div class="row">
                <el-form-item label="Campaign name" prop="name">
                    <el-input ref="form.name" v-model="form.name" :value="normalizeName"></el-input>
                </el-form-item>

                <el-form-item label="Bid Amount">
                    <el-input-number v-model="form.default_bid" :step="0.01" :min="0.01"></el-input-number>
                </el-form-item>

                <el-form-item label="Daily Budget">
                    <el-input-number v-model="form.budget" :min="100"></el-input-number>
                </el-form-item>
            </div>

            <h2 class="section_title">Scheduling</h2><br>
            <hr class="style-one">

            <div class="row">
                <el-form-item label="Start Date">
                    <el-radio-group v-model="radio_start" :disabled="action==='update'">
                        <el-radio-button label="Immediately"></el-radio-button>
                        <el-radio-button label="Specific date"></el-radio-button>
                    </el-radio-group>
                </el-form-item>

                <div :class="[radio_start === 'Specific date' ? 'show' : 'hide']">
                    <el-form-item>
                        <el-col :span="11">
                            <el-date-picker type="date" placeholder="Pick a date" v-model="form.pre_start"
                                            :disabled="action === 'update'"
                                            style="width: 100%;"></el-date-picker>
                        </el-col>
                    </el-form-item>
                </div>

                <el-form-item label="End Date">
                    <el-radio-group v-model="radio_end">
                        <el-radio-button label="Never ends"></el-radio-button>
                        <el-radio-button label="Specific date"></el-radio-button>
                    </el-radio-group>
                </el-form-item>

                <div :class="[radio_end === 'Specific date' ? 'show' : 'hide']">
                    <el-form-item>
                        <el-col :span="11">
                            <el-date-picker type="date" placeholder="Pick a date" v-model="form.pre_end"
                                            style="width: 100%;"></el-date-picker>
                        </el-col>
                    </el-form-item>
                </div>
            </div>

            <h2 class="section_title">Targeting</h2><br>
            <hr class="style-one">

            <div class="row">
                <el-alert
                        title="Country Codes can't be empty when country targeting set to include/exclude"
                        type="warning"
                        :class="{hide:!formVerify}"
                        :closable="false">
                </el-alert>
                <el-form-item label="Country Targeting">
                    <el-radio-group v-model="form.country_targeting">
                        <el-radio-button label="all">All countries</el-radio-button>
                        <el-radio-button label="include">Include</el-radio-button>
                        <el-radio-button label="exclude">Exclude</el-radio-button>
                    </el-radio-group>
                </el-form-item>

                <div :class="[form.country_targeting === 'include' || form.country_targeting === 'exclude' ? 'show' : 'hide']">
                    <el-form-item label="">
                        <el-select v-model="form.country_codes" multiple placeholder="Select" filterable>
                            <el-option
                                    v-for="item in countries"
                                    :label="item.id"
                                    :value="item.id"
                                    :key="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>

                <el-form-item label="Device targeting">
                    <el-checkbox-group v-model="form.device_targeting" @change="deviceValid">
                        <el-checkbox-button label="all_devices" :disabled="_all_devices">All Devices
                        </el-checkbox-button>
                        <el-checkbox-button label="1">Desktop</el-checkbox-button>
                        <el-checkbox-button label="2">Mobile</el-checkbox-button>
                        <el-checkbox-button label="3">Tablet</el-checkbox-button>
                    </el-checkbox-group>

                    <el-checkbox-group v-model="form.device_targeting" v-show="_has_mobile" @change="deviceValid">
                        <el-checkbox-button label="all_os" :disabled="_all_os">
                            All Operating Systems
                        </el-checkbox-button>
                        <el-checkbox-button label="4">Android
                        </el-checkbox-button>
                        <el-checkbox-button label="5">IOS
                        </el-checkbox-button>
                        <el-checkbox-button label="6">Windows
                        </el-checkbox-button>
                    </el-checkbox-group>
                </el-form-item>

                <div>
                    <el-form-item label="Language Targeting">
                        <el-select v-model="form.language_targeting" multiple placeholder="Default: All Languages">
                            <el-option label="English" value="1"></el-option>
                            <el-option label="French" value="5"></el-option>
                            <el-option label="German" value="4"></el-option>
                            <el-option label="Spanish" value="2"></el-option>
                            <el-option label="Portuguese" value="8"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Exclude Low Volume Widgets">
                        <el-radio-group v-model="form.exclude_low_volume">
                            <el-radio-button label="on">Yes</el-radio-button>
                            <el-radio-button label="off">No</el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </div>
            </div>

            <h2 class="section_title">Tracking</h2>
            <hr class="style-one">
            <div class="row">
                <el-form-item label="Tracking code">
                    <el-input v-model="accounts_provider" :disabled="action==='update'"></el-input>
                </el-form-item>
            </div>

            <el-button @click="submitForm('form')" type="primary" :class="{'is-disabled prevents':formVerify}">
                {{action}}
                <i v-bind:class="this.loading ? '' : 'wait'" class="el-icon-loading"></i>
            </el-button>

        </el-form>

        <!--Edit Campaign Form End-->

    </div>
</template>

<script>
    import moment from 'moment-timezone';

    export default {
        mounted() {
            this.initData();
            if (this.action === 'create') {
                this.revConst();
            } else if (this.action === 'update') {
                this.currentCampaign();
            }
        },
        watch: {
            'form.website_id': function (val) {
                this.form.website_name = this.websites.find(
                    obj => obj.website_id === val
                ).website_name;
            },
            'form.provider_id': function (val) {
                this.form.provider_name = this.providers.find(
                    obj => obj.account_id === val.toLowerCase()
                ).provider_name;
            },
            'form.account_id': function (val) {
                this.form.account_name = this.accounts.find(
                    obj => obj.account_id === val
                ).account_name;
            },
            'form.default_bid': function () {
                if (this.form.default_bid > 0.15) {
                    this.$notify({
                        title: 'Are you sure?',
                        message: `${this.form.default_bid} is quite high`,
                        type: 'warning'
                    });
                }
            },
            radio_start: function (val) {
                if (val === 'Specific date') this.form.start_date = '';
                if (val === 'Immediately') this.form.start_date = 'immediately'
            },
            radio_end: function (val) {
                if (val === 'Specific date') this.form.end_date = '';
                if (val === 'Never ends') this.form.end_date = 'never'
            },
            'form.pre_start': function (val) {
                this.form.start_date = val === 'Invalid date' ? 'immediately' : moment(val).format("YYYY-MM-DD HH:mm:ss");
            },
            'form.pre_end': function (val) {
                this.form.end_date = val === 'Invalid date' ? 'never' : moment(val).format("YYYY-MM-DD");
            },
            'form.language_targeting': function (val) {
                let idx = Object.values(val).indexOf("all");

                if (val.length > 1 && idx > -1) { //if any language checked
                    let idx = Object.values(val).indexOf("all");
                    val.splice(idx, 1);
                } else if (!val.length) {
                    val.push("all");
                }
            }
        },
        computed: {
            formVerify() {
                // Revcontent Limitation:
                // if country_targeting set to include/exclude, country_codes can;t be empty
                if (['include', 'exclude'].indexOf(this.form.country_targeting) > -1) {
                    if (this.form.country_codes.length <= 0) {
                        return true;
                    }
                }
            },
            normalizeName() {
                if (this.form.name.length > 0) {
                    return
                }
                let website = this.form.website_id;
                let res = '', new_val = '';
                if (this.websites.find(obj => obj.website_id === website)) {
                    this.form.name = '';
                    res = this.websites.find(obj => obj.website_id === website);
                    new_val = res.acronym + ' - ';
                    this.form.name = new_val;
                    return new_val
                }
            },
            accounts_provider() {
                let provider = this.form.provider_name.toLowerCase();
                if (provider === 'revcontent') {
                    this.form.tracking_code = "utm_source=revcontent&utm_medium={widget_id}&utm_term={adv_targets}&utm_content={content_id}&utm_campaign={boost_id}&utm_widget_id={widget_id}"
                    return this.form.tracking_code
                } else if (provider === 'taboola') {
                }
            },
            _has_mobile() {
                for (let val of this.form.device_targeting) {
                    if (val === '2' || val === '3') return true
                }
                return false
            },
            _all_devices() {
                for (let val of this.form.device_targeting) {
                    if (['1', '2', '3'].includes(val)) return true
                }
                return false
            },
            _all_os() {
                for (let val of this.form.device_targeting) {
                    if (['4', '5', '6'].includes(val)) return true
                }
                return false
            }
        },
        data() {
            return {
                campaign: [],
                activeName: 'properties',
                user: '',
                websites: [],
                providers: [],
                accounts: [],
                targeting: {
                    countries: [],
                    keywords: []
                },
                form: {
                    name: '',
                    website_id: '',
                    website_name: '',
                    provider_id: '',
                    provider_name: '',
                    account_id: '',
                    acronym: '',
                    start_date: 'immediately',
                    end_date: 'never',
                    pre_start: '',
                    pre_end: '',
                    language_targeting: [],
                    device_targeting: ['all_os'],
                    country_codes: [],
                    country_targeting: [],
                    bid_type: 'cpc',
                    optimize: 'cpc',
                    default_bid: '0.03',
                    budget: '',
                    tracking_code: '',
                    exclude_low_volume: 'off',
                    device_flag: false
                },
                rules: {
                    website: [
                        {required: false, message: 'Please select Website', trigger: 'blur'}
                    ],
                    provider: [
                        {required: false, message: 'Please select Provider', trigger: 'blur'}
                    ],
                    account: [
                        {required: false, message: 'Please select Account'}
                    ],
                    name: [
                        {required: true, message: 'Campaign Name is required', trigger: 'blur'}
                    ]

                },
                countries_options: [],
                countries: [],
                radio_start: 'Immediately',
                radio_end: 'Never ends',
                device_targeting: '',
                show_form: false,
                loading: false,
                action: this.$route.query.op,
                cid: this.$route.params.campaignId
            }
        },
        methods: {
            currentCampaign() {
                this.$http.get(`/api/campaignManager/properties?cid=${this.cid}`).then(res => {
                    this.campaign = res.body.campaign;
                    this.updateForm(this.campaign);
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                });
                return true
            },
            submitForm(formName) {
                this.loading = true;
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post('/api/campaignManager/properties', {
                            "form_data": this.form,
                            "campaign_id": this.cid,
                            "action": this.action
                        }).then(res => {
                            if (res.body.cid) {
                                this.loading = false;
                                if (this.action === 'create') {
                                    this.$router.push({path: `/campaign/inventory/${res.body.cid}`});
                                }

                                const h = this.$createElement;
                                this.$notify({
                                    title: 'Great!',
                                    message: h('i', {style: 'color: teal'}, 'Task Submitted')
                                });
                                this.cid = res.body.cid;
                                this.action = 'update'
                            } else {
                                this.loading = false;
                                this.$notify({
                                    title: 'Failed',
                                    message: `${this.form.name} Failed to ${this.action}`,
                                    type: 'error'
                                });
                            }
                        }, res => {
                            console.log("error");
                            this.loading = false;
                            // error callback
                        });
                    } else {
                        this.loading = false;
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            initData() {
                // this.user = this.$store.getters.getUser.user_id;
                this.$http.get("/api/campaignManager/data").then(res => {
                    this.websites = res.body.websites;
                    this.countries = res.body.country_targets;
                    this.providers = res.body.providers;
                    this.accounts = res.body.accounts;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            revConst() {
                this.form.country_codes.push('US');
                this.form.language_targeting.push('1');
                this.form.country_targeting = 'include';
                this.form.provider_name = 'Revcontent';
                this.provider = "revcontent";
            },
            updateForm(campaign) {
                if (campaign.country_codes.slice(1, -1).length) {
                    let cc_array = campaign.country_codes.slice(1, -1).replace(/["]+/g, '').split(',');
                    if (cc_array && cc_array.length) this.form.country_codes = cc_array
                }

                if (this.$route.query.op === 'update' && (campaign.device_targeting === '[]' || !campaign.device_targeting.length)) {
                    this.form.device_targeting.push('all_devices')
                }
                if (campaign.device_targeting.slice(1, -1).length) {
                    let dt_array = campaign.device_targeting.slice(1, -1).replace(/["]+/g, '').replace(/\s+/g, "").split(',');
                    if (dt_array && dt_array.length) this.form.device_targeting = dt_array
                }

                if (campaign.language_targeting.slice(1, -1).length) {
                    let lt_array = campaign.language_targeting.slice(1, -1).replace(/["]+/g, '').split(',');
                    if (lt_array && lt_array.length) this.form.language_targeting = lt_array.map(function (item) {
                        return item.trim();
                    });
                }

                if (typeof this.form.start_date !== 'undefined') this.radio_start = 'Specific date';
                if (typeof this.form.end_date !== 'undefined') this.radio_end = 'Specific date';

                this.form.website_name = campaign.website_name;
                this.form.website_id = campaign.website_id;
                this.form.provider_name = campaign.provider;
                this.form.account_name = campaign.account_name;
                this.form.account_id = campaign.account_id;
                this.form.name = campaign.campaign_name;
                this.form.default_bid = campaign.default_bid;
                this.form.budget = campaign.budget;
                this.form.pre_start = campaign.start_date;
                if (campaign.end_date === null || campaign.end_date === 'never') {
                    this.radio_end = 'Never ends'
                } else {
                    this.radio_end = 'Specific date'
                    this.form.pre_end = campaign.end_date;
                }
                this.form.tracking = campaign.utm_codes;
                this.form.country_targeting = campaign.country_targeting;
                this.form.exclude_low_volume = campaign.exclude_low_volume
            },
            deviceValid() {
                let el = this.form.device_targeting;
                let adIdx = Object.values(el).indexOf("all_devices");
                let osIdx = Object.values(el).indexOf("all_os");
                let dext = el.map(Number).some(r => [1, 2, 3].includes(r));
                let oext = el.map(Number).some(r => [4, 5, 6].includes(r));
                let mext = el.map(Number).some(r => [2, 3].includes(r));

                if (dext && adIdx >= 0) { // if any device code checked and "all_devices" exist
                    el.splice(adIdx, 1); // remove "all_devices"
                } else if (!dext && adIdx < 0) {
                    el.push("all_devices");
                }

                if (oext && osIdx >= 0) { // if any device code checked and "all_devices" exist
                    el.splice(osIdx, 1); // remove "all_devices"
                } else if (!oext && osIdx < 0) {
                    el.push("all_os");
                }

                if (!mext) { // if NO mobile code checked
                    el = el.filter(c => !["4", "5", "6"].includes(c));
                    if (osIdx < 0) {
                        el.push("all_os");
                    }
                }

                this.form.device_targeting = el;
            },
        }
    }
</script>

<style scoped>
    .cid {
        font-size: 15px;
        float: right;
    }

    .el-tabs {
        border-bottom-color: #f5f5f5;
    }

    .acronym {
        max-width: 85px;
    }

    h2.section_title {
        font-size: 24px;
    }

    .el-form {
        max-width: 70%;
    }

    .el-form .row {
        padding-left: 10vw;
    }

    .wait, .hide {
        display: none;
    }

    .menu-tabs > div > div {
        pointer-events: none !important;
    }

    .el-tabs__item a {
        pointer-events: all;
    }

    .prevents {
        pointer-events: none !important;
    }
</style>