<template>
    <div id="campaigns_main">
        <h1>Campaign Manager</h1>
        <div id="overlay" v-show="popupOn"></div>

        <div class="row" v-show="!loading">
            <data-tables :data="campaigns" :custom-filters="customFilters" :search-def="searchDef" style="width:95vw;">

                <el-row slot="custom-tool-bar" style="margin-bottom: 10px">
                    <el-col :span="5" style="padding-right: 5px;">
                        <el-input v-model="customFilters[0].vals" placeholder="Search">
                        </el-input>
                    </el-col>
                    <el-col :span="3">
                        <el-select v-model="customFilters[1].vals" multiple="multiple" placeholder="websites">
                            <el-option v-for="website in websites" :label="website.website_name"
                                       :value="website.website_name"
                                       :key="website.website_name"
                                       >
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="3">
                        <el-select v-model="customFilters[2].vals" multiple="multiple" placeholder="accounts">
                            <el-option v-for="account in accounts"
                                       :label="account.account_name"
                                       :value="account.account_name"
                                       :key="account.account_name"
                                       >
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="6" :offset="7">
                        <el-button class="create_campaign">
                            <router-link to="/campaign/properties?op=create">Create New Campaign <i
                                    class="el-icon-plus"></i></router-link>
                        </el-button>
                    </el-col>
                </el-row>

                <el-table-column v-for="col in cols" :key="col.prop" :prop="col.prop" :label="col.label"
                                 :formatter="col.formatter"
                                 sortable="custom">
                </el-table-column>

                <el-table-column label="Enabled">
                    <template slot-scope="scope">
                        <app-switch :item="scope.row"></app-switch>
                    </template>
                </el-table-column>

                <el-table-column label="Actions" class-name="actions-col">
                    <template slot-scope="scope">
                    <span class="bar-link">
                        <router-link :to="{path: `/campaign/properties/${scope.row.campaign_id}?op=update`}">
                            <el-button type="primary" size="mini"><i class="fa fa-cog"></i></el-button>
                        </router-link>
                    </span>
                        <span class="bar-link">
                        <router-link :to="{path: `/campaign/inventory/${scope.row.campaign_id}?op=update`}">
                            <el-button type="primary" size="mini"><i class="fa fa-file-text"></i></el-button>
                        </router-link>
                    </span>

                        <span class="bar-link">
                        <router-link :to="{path: `/campaign/targeting/${scope.row.campaign_id}?op=update`}">
                            <el-button type="primary" size="mini"><i class="fa fa-bullseye"></i></el-button>
                        </router-link>
                    </span>

                        <!--DUPLICATE POPUP-->

                        <el-popover ref="popover1" width="500" popperClass="dup" placement="left" trigger="click"
                                    v-on:hide="hidePopup">
                            <h2 class="dup-title">Campaign ID: {{scope.row.campaign_id}}</h2>
                            <el-form :model="duplicateCampaign" class="duplicate" labelPosition="right">
                                <el-form-item prop="website">
                                    <el-select v-model="duplicateCampaign.website_id" placeholder="Website">
                                        <el-option
                                                v-for="website in websites"
                                                :label="website.website_name"
                                                :value="website.website_id"
                                                :key="website.website_id"
                                                >
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item prop="provider">
                                    <el-select v-model="duplicateCampaign.provider" placeholder="Provider">
                                        <el-option v-for="provider in ['revcontent']"
                                                   :label="provider"
                                                   :value="provider"
                                                   :key="provider">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item prop="account">
                                    <el-select v-model="duplicateCampaign.account_id" placeholder="Account">
                                        <el-option v-for="account in accounts"
                                                   :label="account.account_name"
                                                   :value="account.account_id"
                                                   :key="account.account_id">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item prop="profile">
                                    <el-select v-model="duplicateCampaign.profile_id" placeholder="Profile">
                                        <el-option v-for="profile in profiles"
                                                   :label="profile.name"
                                                   :value="profile.id"
                                                   :key="profile.id">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item>
                                    <el-input placeholder="Name" v-model="duplicateCampaign.name"
                                              :value="normalizeName"
                                    ></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-input placeholder='Inventory url - must start with http://'
                                              v-model="duplicateCampaign.inventory_url"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-input placeholder="Brand Name"
                                              v-model="duplicateCampaign.brand_name" :value="brandName">

                                    </el-input>
                                </el-form-item>
                            </el-form>
                            <div style="text-align: right; margin: 0">
                                <el-button type="primary" size="large"
                                           @click.native="duplicateCpn(scope.row.campaign_id)"
                                           :disabled="isValidUrl(duplicateCampaign.inventory_url)">duplicate
                                    <i v-bind:class="duplicateLoading ? 'el-icon-loading' : 'wait'"></i>
                                </el-button>
                            </div>
                            <el-button size="mini" slot="reference" class="dup-button"
                                       @click="showPopup(scope.row.campaign_name)">
                                <i class="fa fa-clone"></i>
                            </el-button>
                        </el-popover>

                        <!--/DUPLICATE POPUP-->
                    </template>
                </el-table-column>
            </data-tables>
        </div>
        <scaleloader class="centered" :loading="loading"></scaleloader>
    </div>
</template>

<script>
    import Switch from '../partials/Switch.vue';
    import Scaleloader from '../../../node_modules/vue-spinner/src/ScaleLoader.vue'

    export default {
        components: {
            appSwitch: Switch,
            scaleloader: Scaleloader
        },
        mounted() {
            this.getUserCampaigns();
            this.getUserData();
        },
        data() {
            return {
                cols: [
                    {
                        prop: "campaign_id",
                        label: "Id",
                        formatter: this.formatter
                    },
                    {
                        prop: "campaign_name",
                        label: "Name",
                        formatter: this.formatter
                    }, {
                        prop: "website_name",
                        label: "Website",
                        formatter: this.formatter
                    },
                    {
                        prop: "account_name",
                        label: "Account",
                        formatter: this.formatter
                    },
                    {
                        prop: "budget",
                        label: "Budget",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "avg_cpc",
                        label: "Avg CPC",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "start_date",
                        label: "Start",
                        formatter: this.dateFormatter
                    },
                    {
                        prop: "spend",
                        label: "Spend",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "spend_yesterday",
                        label: "Spend Y",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "ctr",
                        label: "CTR",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "revenue",
                        label: "Revenue",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "revenue_yesterday",
                        label: "Revenue Y",
                        formatter: this.intFormatter
                    },
                    {
                        prop: "roi",
                        label: "ROI",
                        formatter: this.roiFormatter
                    },
                    {
                        prop: "roi_yesterday",
                        label: "ROI Y",
                        formatter: this.roiyFormatter
                    }
                ],
                filter: null,
                prv_filter: null,
                site_filter: null,
                account_filter: null,
                campaign: '',
                user_id: '',
                provider_id: '',
                perPage: 20,
                currentPage: 1,
                hide: false,
                providers: [
                    {id: 1, name: 'Taboola'},
                    {id: 2, name: 'Revcontent'},
                    {id: 3, name: 'Teads'},
                    {id: 4, name: 'Content.ad'}
                ],
                filterAccounts: [],
                customFilters: [
                    {
                        vals: ''
                    },
                    {
                        vals: '',
                        props: 'website_name'
                    },
                    {
                        vals: []
                    }],
                searchDef: {
                    show: false
                },
                websites: [],
                accounts: [],
                campaigns: [],
                profiles: [{}],
                loading: true,
                popupOn: false,
                duplicateLoading: false,
                duplicateCampaign: {
                    name: '',
                    website_id: '',
                    provider: '',
                    account_id: '',
                    profile_id: '',
                    account_name: '',
                    inventory_url: '',
                    brand_name: ''
                },
                duplicateName: '',
                visible1: false
            }
        },
        methods: {
            getUserData()
            {
                this.$http.get("/api/campaignManager/data").then(res => {
                    this.websites = res.body.websites;
                    this.countries = res.body.country_targets;
                    this.accounts = res.body.accounts;
                    this.accounts.map(a => {
                        this.filterAccounts[a.account_id] = a.account_name
                    });
                    this.profiles = res.body.profiles;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            getUserCampaigns()
            {
                this.$http.get("/api/campaignManager/campaigns").then(res => {
                    this.campaigns = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            duplicateCpn(campaign_id)
            {
                this.duplicateLoading = true;
                this.$http.post('/api/campaignManager/duplicate', {
                    campaign_id: campaign_id,
                    data: this.duplicateCampaign
                }).then(res => {
                    if (res.body) {
                        this.$notify({
                            title: 'Great!',
                            message: 'Duplicate task submitted',
                            type: 'success'
                        });

                    } else {
                        this.$notify({
                            title: 'Duplicate Failed',
                            message: `Campaign ${campaign_id} failed to duplicate`,
                            type: 'alert'
                        });
                    }
                    this.hidePopup();
                    this.duplicateLoading = false;

                }, res => {
                    // TODO: Handle server error
                    console.log("error: " + res);
                    this.duplicateLoading = false;
                    this.error = true;
                });
            },
            showPopup(cName) {
                this.popupOn = true;
                this.duplicateName = cName;
                this.visible1 = !this.visible1
            },
            isValidUrl(url)
            {
                let regex = /(http|https):\/\/(\w+:{0,1}\w*)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%!\-\/]))?/;
                return !regex.test(url)
            },
            hidePopup()
            {
                this.visible1 = false;
                this.popupOn = false;
                Object.keys(this.duplicateCampaign).forEach(key => this.duplicateCampaign[key] = "")
            },
            formatter(row, column)
            {
                return row[column.property];
            },
            dateFormatter(row, column)
            {
                if (row.start_date === "immediately") {
                    return row.creation_date.split(" ")[0];
                } else {
                    return row.start_date.split(" ")[0];
                }
            },
            intFormatter(row, column)
            {

                return parseFloat(row[column.property])
            },
            roiFormatter(row, column)
            {
                if (row.roi !== 0) {
                    return parseFloat(row.roi).toFixed(4)
                } else {
                    return "NA"
                }
            },
            roiyFormatter(row, column)
            {
                if (row.roi_yesterday !== 0) {
                    return parseFloat(row.roi_yesterday).toFixed(4)
                } else {
                    return "NA"
                }
            },
            accountFormatter(row, column) {
                if (row.account_id !== "") {
                    return this.filterAccounts[row.account_id];
                } else {
                    return "NA"
                }
            },
            websiteFormatter(row, column) {
                if (row.website_id !== "") {
                    let res = this.websites.filter(w => w.website_id === row.website_id);
                    return res.length ? res[0].website_name : "NA";
                } else {
                    return "NA"
                }
            },
            formatter(row, column)
            {
                return row[column.property]
            }
        },
        watch: {
            'duplicateCampaign.account_id': function (val) {
                if (val !== "") {
                    try {
                        this.duplicateCampaign.account_name = this.accounts.find(
                            obj => obj.account_id === val
                        ).account_name;
                    } catch (err) {
                        this.duplicateCampaign.account_name = "NA";
                    }
                }
            },
            'duplicateCampaign.website_id': function (val) {
                if (val !== "") {
                    try {
                        this.duplicateCampaign.brand_name = this.websites.find(
                            obj => obj.website_id === val
                        ).website_name;
                    } catch (err) {
                        this.duplicateCampaign.brand_name = "NA";
                    }
                }
            }
        },
        computed: {
            normalizeName()
            {
                if (!this.duplicateCampaign.website_id) {
                    this.duplicateCampaign.name = this.duplicateName;
                    return this.duplicateName;
                }
                let website = this.duplicateCampaign.website_id;
                let websites = this.websites;
                let res = '', new_val = '';
                if (websites.find(obj => obj.website_id === website)) {
                    this.duplicateCampaign.name = '';
                    res = websites.find(obj => obj.website_id === website);
                    new_val = res.acronym + ' - ' + this.duplicateName;
                    this.duplicateCampaign.name = new_val;
                    return new_val
                }
            },
            brandName()
            {
                return this.duplicateCampaign.website_id
            }
        },
    }
</script>

<style>
    .filter .el-input {
        display: inline-block;
        max-width: 220px !important;
    }

    .duplicate {
        width: 100%;
    }

    .dup {
        background: #f5f5f5;
    }

    .dup .el-popover__title {
        margin-bottom: 20px;
        text-align: center;
    }

    h2.dup-title {
        color: #a0aabe;
        font-size: 15px;
        margin-bottom: 15px;
        text-align: center;
    }

    .el-button {
        margin: 0 1px;
    }

    .filter {
        margin: 25px 0;
    }

    .create_campaign {
        float: right;
        background: #20a0ff;
    }

    .create_campaign a {
        color: #FFF;
        text-decoration: none;
    }

    .link {
        cursor: pointer;
        max-width: 20vw;
    }

    .link:hover {
        color: #20a0ff;
    }

    .wait {
        display: none;
    }

    .bar-link button, .dup-button {
        padding: 7px 5px;
    }

    .actions-col span {
        display: table-cell;
    }

    #overlay {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 2;
        cursor: pointer;
    }

    td.el-table_1_column_14 .cell {
        text-align: center;
    }

    .green {
        color: #08d208;
    }
    .red {
        color: red;
    }
</style>
