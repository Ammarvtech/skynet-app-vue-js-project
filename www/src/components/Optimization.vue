<template>
    <div id="campaigns_main">
        <h1 id="optimization">Automation Rules

            <span style="float:right;font-size:16px;">
                <el-tooltip content="process might take...be patient" class="item" effect="dark">
                    <span style="float:right;font-size:16px;">Next Run: <strong>3:00 AM EST</strong></span>
                </el-tooltip>
            </span>
        </h1>
        <div id="overlay" v-show="showPopup"></div>

        <div id="topbar" v-show="!loading">
            <el-select v-model="filters.website" placeholder="website">
                <el-option
                        v-for="website in websites"
                        :key="website.website_id"
                        :label="website.website_name"
                        :value="website.website_id">
                </el-option>
            </el-select>
            <el-select v-model="filters.source" placeholder="provider">
                <el-option
                        v-for="provider in providers"
                        :key="provider.provider_id"
                        :label="provider.provider_name"
                        :value="provider.provider_name">
                </el-option>
            </el-select>
            <el-input v-model="filters.text" placeholder="search" style="max-width:220px;"></el-input>

            <el-button type="primary" style="float:right;" @click="createOptimization">Create New Optimization
            </el-button>
            <el-button type="info" style="float:right;margin-right: 10px;" :disabled="!multipleSelected"
                       @click="deleteMultiple()">Delete Selected
            </el-button>
            <el-button type="info" style="float:right;" :disabled="!multipleSelected" @click="switchMultiple(0)">
                Pause Selected
            </el-button>
            <el-button type="info" style="float:right;" :disabled="!multipleSelected" @click="switchMultiple(1)">
                Start Selected
            </el-button>
        </div>

        <!--POPUP-->
        <div id="edit-popup" v-show="showPopup">
            <el-form :inline="true" :model="ruleForm">
                <el-form-item label="Campaign ID" v-if="this.createOpt">
                    <el-autocomplete
                            class="inline-input"
                            v-model="ruleForm.campaign_id"
                            :fetch-suggestions="cidSearch"
                            placeholder="Campaign Id"
                    ></el-autocomplete>
                    <el-select v-model="allWebsite" placeholder="website" v-show="ruleForm.campaign_id === 'All'">
                        <el-option
                                v-for="website in websites" v-if="uniqueAllRule(website.website_id)"
                                :key="website.website_id"
                                :label="website.website_name"
                                :value="website.website_id">
                        </el-option>
                    </el-select>
                </el-form-item>
                </br>
                <el-form-item label="If medium session is higher than ">
                    <el-input v-model="ruleForm.sessions" placeholder="Sessions" style="max-width: 100px;"></el-input>
                </el-form-item>
                <el-form-item label="adjust medium bid to ">
                    <el-input v-model="ruleForm.roi" placeholder="ROI" style="max-width: 60px;"></el-input>
                </el-form-item>
                <el-form-item label="and set max spread to ">
                    <el-input v-model="ruleForm.spread" placeholder="Spread" style="max-width: 100px;"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="setRule()" :disabled="_ruleValid">Submit</el-button>
                    <el-button type="primary" @click="resetForm()">Cancel</el-button>
                </el-form-item>
                <br>
                <el-form-item>
                    <div v-for="period,idx in periods" style="display: inline-block;margin-right: 15px;">
                        <input v-model="ruleForm.dataPeriod[idx]" type="checkbox" :value="period.value"
                               @change="periodChange($event,idx)">{{period.label}}
                    </div>
                </el-form-item>
            </el-form>
        </div>
        <!--/POPUP-->


        <!--MAIN TABLE-->
        <el-table
                :data="_data1"
                style="width: 100%"
                @selection-change="handleSelection"
                v-show="!loading"
        >
            <el-table-column type="expand">
                <template slot-scope="scope">
                    <div class="rule-row">
                        <el-table :data="scope.row.rules">
                            <el-table-column
                                    prop=""
                                    label="Rule"
                                    :formatter="const_col"
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="roi"
                                    label="ROI">
                            </el-table-column>
                            <el-table-column
                                    prop="sessions"
                                    label="Sessions">
                            </el-table-column>
                            <el-table-column
                                    prop="spread"
                                    label="Spread">
                            </el-table-column>
                            <el-table-column
                                    label="Enabled">
                                <template slot-scope="props">
                                    <el-switch v-model="props.row.active" @change="switchRule(props.row, scope.row)">
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="Actions">
                                <template slot-scope="props">
                                    <el-tooltip class="item" effect="dark" content="Edit"
                                                placement="top-start">
                                        <el-button type="primary" size="small" @click="editRule(props.row, scope.row)">
                                            <i class="el-icon-edit"></i></el-button>
                                    </el-tooltip>
                                    <el-tooltip class="item" effect="dark" content="Delete"
                                                placement="top-start">
                                        <el-button type="primary" size="small"
                                                   @click="deleteRule(props.row, scope.row)">
                                            <i class="el-icon-delete"></i></el-button>
                                    </el-tooltip>
                                    <el-tooltip class="item" effect="dark" content="Run Rule"
                                                placement="top-start">
                                        <el-button type="primary" size="small" @click="runRule(props.row, scope.row)"
                                                   :disabled="isRunning || !props.row.active">
                                            <i class="el-icon-caret-right" v-show="!isRunning"></i>
                                            <i class="el-icon-loading" v-show="isRunning"></i>
                                        </el-button>
                                    </el-tooltip>
                                </template>
                            </el-table-column>
                        </el-table>
                        <el-button type="primary" style="margin-top: 5px;" @click="addRule(scope.row)">
                            + Add optimization rule
                        </el-button>
                    </div>
                </template>
            </el-table-column>
            <el-table-column
                    prop="source"
                    label="Source"
                    :formatter="sourceFormatter">
            </el-table-column>
            <el-table-column
                    prop="site_id"
                    label="Website"
                    :formatter="websiteFormatter">
            </el-table-column>
            <el-table-column
                    prop="campaign_id"
                    label="Campaign Id">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="Campaign Name">
            </el-table-column>
            <el-table-column label="Enabled"
                             width="180">
                <template slot-scope="scope">
                    <el-switch v-model="data[scope.$index].active" @change="switchOptimization(scope.row)">
                    </el-switch>
                </template>
            </el-table-column>
            <el-table-column
                    prop="status"
                    label="Status"
            >
                <template slot-scope="props">
                    <el-tooltip class="item" effect="dark" placement="top-start">
                        <div slot="content"><p class="log-row" v-for="ln in tooltipFormat(props.row.status)">{{ln}}</p></div>
                        <div>{{statusFormatter(props.row.status)}}</div>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column
                    type="selection">
            </el-table-column>
        </el-table>
        <!--/MAIN TABLE-->
        <scaleloader class="centered" :loading="loading"></scaleloader>

    </div>
</template>

<script>
    import Scaleloader from '../../node_modules/vue-spinner/src/ScaleLoader.vue'

    export default {
        components: {
            scaleloader: Scaleloader
        },
        mounted() {
            this.getData();
        },
        data() {
            return {
                data: [],
                websites: [],
                providers: [],
                campaigns: [],
                showPopup: false,
                multipleSelected: false,
                multipleSelectedIds: [],
                loading: false,
                createOpt: false,
                isRunning: false,
                ruleForm: {
                    id: '',
                    record_id: '',
                    campaign_id: '',
                    roi: '',
                    sessions: '',
                    spread: '',
                    dataPeriod: [],
                    isNew: ''
                },
                filters: {
                    website: '',
                    source: '',
                    text: ''
                },
                periods: [
                    {"value": 1, "label": "Daily Data"},
                    {"value": 7, "label": "Weekly Data"}
                ],
                allWebsite: '',
                siteIdsAll: []
            }
        },
        methods: {
            getData() {
                this.loading = true;
                this.$http.get("/api/optimization").then(res => {
                    this.loading = false;
                    this.data = res.body.data;
                    for (let item of this.data) {
                        if (item.campaign_id === 'All') this.siteIdsAll.push(parseInt(item.site_id));
                        item.active = !!parseInt(item.active);
                        item.rules = JSON.parse(item.rules);
                        for (let rule of item.rules) {
                            rule.active = !!parseInt(rule.active);
                        }
                    }
                    this.websites = res.body.websites;
                    this.providers = res.body.providers;
                    this.campaigns = res.body.campaigns;
                    this.loading = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                    this.loading = false;
                });
            },
            createOptimization() {
                this.ruleForm = {
                    id: '',
                    record_id: '',
                    campaign_id: '',
                    roi: '',
                    sessions: '',
                    spread: '',
                    dataPeriod: [],
                    isNew: ''
                };
                this.createOpt = true;
                this.showPopup = true;
            },
            handleSelection(val) {
                this.multipleSelected = val.length;
                this.multipleSelectedIds = val.map(item => item.id);
            },
            resetForm() {
                this.showPopup = false;
                this.ruleForm = {
                    id: '',
                    record_id: '',
                    campaign_id: '',
                    roi: '',
                    sessions: '',
                    spread: '',
                    dataPeriod: [],
                    isNew: ''
                };

            },
            addRule(row) {
                this.showPopup = true;
                this.createOpt = false;
                this.ruleForm.isNew = true;
                this.ruleForm.record_id = row.id;
                this.ruleForm.campaign_id = row.campaign_id;
            },
            setRule() {
                this.$http.post("/api/optimization", {
                    data: this.ruleForm,
                    website_id: this.allWebsite,
                    create: this.createOpt,
                }).then(res => {
                    this.handleRes(res.body, this.createOpt, this.ruleForm.id);
                }, res => {
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            runRule(row, campaign) {
                this.isRunning = true;
                this.$http.post("/api/optimization/rule/run", {
                    campaign: campaign
                }).then(res => {
                    this.isRunning = false;
                }, res => {
                    this.isRunning = false;
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            switchOptimization(opt) {
                const item = this.data.filter(item => this.compareStrings(item.campaign_id, opt.campaign_id))[0];
                const status = opt.active;
                for (let rule of item.rules) {
                    rule.active = status;
                }

                this.$http.post("/api/optimization/switch", {
                    id: opt.id,
                    active: opt.active,
                    campaign_id: opt.campaign_id
                }).then(res => {
                    this.success("Enabled updated successfully");
                }, res => {
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            switchRule(row, campaign) {
                this.$http.post("/api/optimization/rule/switch", {
                    data: row,
                    record_id: campaign.id,
                    campaign_id: campaign.campaign_id
                }).then(res => {
                }, res => {
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            handleRes(res, isCreate, ruleId) {
                if (res === '-1') {
                    this.warning("Failed to create rule")
                }
                if (isCreate) {
                    if (res.length) {
                        let newCmp = {
                            "active": true,
                            "campaign_id": res[0]["campaign_id"],
                            "id": res[0]["id"],
                            "name": res[0]["name"],
                            "rules": JSON.parse(res[0]["rules"]),
                            "site_id": res[0]["site_id"],
                            "source": res[0]["source"],
                            "status": "Pending"
                        };
                        for (let rule of newCmp.rules) {
                            rule.active = !!parseInt(rule.active);
                        }
                        this.data.push(newCmp);
                    }
                } else if (!isCreate) {
                    const item = this.data.filter(item => this.compareInts(item.campaign_id, this.ruleForm.campaign_id));
                    if (item.length) {
                        if (this.ruleForm.isNew) { //if new rule in existing campaign
                            let newRule = {
                                active: true,
                                id: "",
                                roi: this.ruleForm.roi,
                                sessions: this.ruleForm.sessions,
                                spread: this.ruleForm.spread,
                                rule: "medium",
                                time_period: this.ruleForm.dataPeriod
                            };
                            item[0]["rules"].push(newRule);
                            item[0]["active"] = true;
                        } else if (res) { //if updating rule
                            const toUpdate = item[0].rules.filter(i => this.compareInts(i.id, ruleId))[0];
                            toUpdate.roi = this.ruleForm.roi;
                            toUpdate.sessions = this.ruleForm.sessions;
                            toUpdate.spread = this.ruleForm.spread;
                            toUpdate.dataPeriod = this.ruleForm.dataPeriod;
                        }
                    }
                }
                this.success("Created Successfully");
                this.resetForm();
            },
            editRule(row, campaign) {
                this.createOpt = false;
                this.showPopup = true;
                this.ruleForm.record_id = campaign.id;
                this.ruleForm.id = row.id;
                this.ruleForm.campaign_id = campaign.campaign_id;
                this.ruleForm.roi = row.roi;
                this.ruleForm.sessions = row.sessions;
                this.ruleForm.spread = row.spread;
                this.ruleForm.dataPeriod = row.time_period;
                this.ruleForm.isNew = false;
            },
            deleteRule(row, campaign) {
                let cid = campaign.campaign_id;
                const item = this.data.filter(item => this.compareInts(item.campaign_id, cid));

                this.$http.post("/api/optimization/rule/delete", {
                    campaign: campaign,
                    row: row,
                }).then(res => {
                    if (item.length)
                        item[0].rules = item[0].rules.filter(r => !this.compareInts(r.id, row.id));
                    this.success("Deleted Successfully")
                }, res => {
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            _rules(row) {
                let rules = JSON.parse(row.rules);
                for (let rule of rules) {
                    rule.active = !!parseInt(rule.active);
                }
                return rules;
            },
            const_col() {
                return "Bid Optimization";
            },
            websiteFormatter(row, column) {
                if (row.website_id !== "") {
                    let res = this.websites.filter(w => this.compareInts(w.website_id, row.site_id));
                    return res.length ? res[0].website_name : "NA";
                } else {
                    return "NA"
                }
            },
            statusFormatter(status) {
                if (status === '-1') {
                    return "Failed";
                } else if (status === "null" || status === null || status === "Pending") {
                    return "Pending"
                } else {
                    return "Finished"
                }
            },
            cidSearch(queryString, cb) {
                let ids = this.campaigns.map(c => {
                    return {value: c.campaign_id}
                });
                ids.unshift({value: "All"});

                let results = queryString ? ids.filter(this.createFilter(queryString)) : ids;
                cb(results);
            },
            createFilter(queryString) {
                return (id) => {
                    return (id.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
                };
            },
            switchMultiple(status) {
                this.$http.post("/api/optimization/multiple/switch", {
                    ids: this.multipleSelectedIds,
                    status: status
                }).then(res => {
                    const items = this.data.filter(item => this.multipleSelectedIds.includes(item.id));
                    for (let item of items) {
                        item.active = !!status;
                        for (let rule of item.rules) {
                            rule.active = !!status;
                        }
                    }
                    this.showPopup = false;
                }, res => {
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            deleteMultiple() {
                this.$http.post("/api/optimization/multiple/delete", {
                    ids: this.multipleSelectedIds
                }).then(res => {
                    this.data = this.data.filter(item => !this.multipleSelectedIds.includes(item.id))
                }, res => {
                    this.showPopup = false;
                    // TODO: Handle server error
                    this.error = true;
                });
            },
            success(msg) {
                this.$notify({
                    title: 'Great!',
                    message: msg,
                    type: 'success'
                });
            },
            warning(msg) {
                this.$notify({
                    title: 'Warning!',
                    message: msg,
                    type: 'warning'
                });
            },
            compareInts(x, y) {
                return parseInt(x) === parseInt(y);
            },
            compareStrings(x, y) {
                return x.toString() === y.toString();
            },
            periodExs(val) {
                return [1, 7].includes(parseInt(val))
            },
            periodChange(event, idx) {
                if (event.target.checked) {
                    this.ruleForm.dataPeriod[idx] = this.compareInts(0, idx) ? '1' : '7';
                } else {
                    this.ruleForm.dataPeriod[idx] = null;
                }
            },
            uniqueAllRule(siteId) {
                return this.siteIdsAll.indexOf(siteId) === -1;
            },
            tooltipFormat(arr) {
                if (arr !== null) {
                    arr = arr.replace(/"/g, "").replace(/[\[\]']/g, '').split(",");
                    return arr;
                } else {
                    return "NA";
                }
            },
            sourceFormatter(row, column) {
                return "taboola";
            }
        },
        computed: {
            _data1() {
                if (!this.data) {
                    return [];
                }

                let data = this.data;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
                    }
                    return String(v);
                };

                if (this.filters.text && this.filters.text.length > 0) {
                    data = data.filter(item =>
                        item.site_id.toString().toLowerCase().includes(this.filters.text.toLowerCase()) ||
                        item.campaign_id.toString().toLowerCase().includes(this.filters.text.toLowerCase()) ||
                        item.name.toLowerCase().includes(this.filters.text.toLowerCase())
                    );
                }

                if (this.filters.website > 0) {
                    data = data.filter(item => this.compareInts(item.site_id, this.filters.website));
                } else if (this.filters.website === 'All') {
                    data = this.data;
                }

                if (this.filters.source.length > 0) {
                    data = data.filter(item =>
                        item.source.toLowerCase().trim() === this.filters.source.toLowerCase().trim())
                }

                return data
            },
            _ruleValid() {
                return this.ruleForm.sessions.length <= 0 || this.ruleForm.roi.length <= 0 || this.ruleForm.spread.length <= 0
                    || this.ruleForm.dataPeriod.filter(r => r !== null).length <= 0;
            }
        }
    }
</script>

<style scoped>
    .all {
        background-color: yellow;
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

    div#edit-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        background: #fff;
        display: inline-table;
        padding: 35px 25px 15px;
        border-radius: 5px;
    }

    #checkbox-group .el-checkbox__label {
        display: none !important;
    }

    .log-row{
        margin-bottom: 10px;
    }
</style>