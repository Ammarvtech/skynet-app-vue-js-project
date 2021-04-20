<template>
    <div id="DealerActionLog">
        <vue-headful title="Action Log"/>
        <div>
            <form @submit="submit">
                <div class="row">
                    <div class="col-xs-2">
                        <websites-dropdown @selectWebsite="selectWebsite($event)"></websites-dropdown>
                    </div>
                    <!--<div class="col-xs-2">-->
                    <!--<v-select v-model="selected_device" :items="devices" label="Device"></v-select>-->
                    <!--</div>-->
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
                </div>
            </div>

            <template>
                <el-table :class="[hide ? 'tb-hide' : '','']"
                          :data="_items"
                          style="width: 100%">
                    <el-table-column type="expand">
                        <template slot-scope="props">
                            <p>Data Info: {{ props.row.data_info }}</p>
                            <p>Status Message: <span v-html="props.row.status_message.replace(/\\n/g, '<br />').replace(/\\/g, '').replace(/Exception: /g, '<br />Exception: ')"></span></p>
                        </template>
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Timestamp"
                            prop="est_time">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="top">
                                <span>Israel Time: {{isr_time(scope.row.est_time)}} </span>
                                <div slot="reference">
                                    <span>{{ scope.row.est_time }}</span>
                                </div>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Campaign Id"
                            prop="campaign_id">
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Site"
                            prop="website_name">
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Source"
                            prop="source">
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="User Name"
                            prop="username"
                            :filters="filter_users" :filter-method="filterUser" filter-placement="bottom-end">
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Auto Rules"
                            prop="is_auto">
                    </el-table-column>
                    <el-table-column
                            sortable
                            label="Action"
                            prop="action"
                            :filters="filter_actions" :filter-method="filterAction" filter-placement="bottom-end">
                    </el-table-column>
                    <!--<el-table-column-->
                    <!--label="Medium"-->
                    <!--prop="targeting_id">-->
                    <!--</el-table-column>-->
                    <el-table-column
                            sortable
                            label="Status"
                            prop="status">
                        <template slot-scope="scope">
                            <el-tag
                                    :type="scope.row.status === 'DONE' ? 'success' : scope.row.status === 'ERROR' ? 'danger' : 'primary'"
                                    close-transition>{{scope.row.status}}
                            </el-tag>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
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
        name: 'DealerActionLog',
        components: {},
        mixins: [alerts],
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
                websites: [],
                filter_users: [],
                filter_actions: [],
                colors: [],
                shown_item: '',
                step: 0.001,
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                sources: ['All', 'Taboola', 'Facebook', 'Gemini', 'Outbrain', 'Revcontent'],
                filterMobile: true,
                filter_fields_hide: true,
                sortDesc: true,
                sortFlag: false,
                loading: false,
                disabled: true,
                hide: true,
                sort: null,
                filter: null,
                edit_index: null,
                selected_campaign_source: "All",
                selected_device: "All",
                currentPage: 1,
                perPage: 500,
                // minClicks: 0,
                date_range: [
                    moment().format("HH") >= '17' ? moment(new Date(Date.now())).format("YYYY-MM-DD") : moment(new Date(Date.now())).format("YYYY-MM-DD"),
                    moment().format("HH") >= '17' ? moment(new Date(Date.now())).format("YYYY-MM-DD") : moment(new Date(Date.now())).format("YYYY-MM-DD")
                ],
                site_id: "All",
                inited_summary: {},
            }
        },
        methods: {
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
            },
            onDateRangeChange(range) {
                this.date_range = range
            },
            submit: function () {
                this.items = [];

                let site_id = this.site_id == 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
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

                this.$http.get('/api/website/action_log', {params: params}).then(res => {
                    if (res.body) {
                        this.items = Object.keys(res.body).map(key => res.body[key]);

                        let users = this.filter_users;
                        let action = this.filter_actions;

                        for (let i = 0; i < this.items.length; i++) {
                            if (!users.find(x => x.text === this.items[i].username)) {
                                users.push({text: this.items[i].username, value: this.items[i].username})
                            }
                        }


                        for (let i = 0; i < this.items.length; i++) {
                            if (!action.find(x => x.text === this.items[i].action)) {
                                action.push({text: this.items[i].action, value: this.items[i].action})
                            }
                        }

                        if (this.items.length === 0) {
                            this.filterClose();
                        } else {
                            // this.headClick(this.tfields.est_time, "est_time");
                            this.sortDesc = false;
                            this.hide = false;
                            this.disabled = false;
                        }
                        this.loading = false;
                    } else {
                        console.log("---------ERROR-----------");
                    }
                }).catch(e => {
                    this.loading = false;
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
            filterUser(value, row) {
                return row.username === value;
            },
            filterAction(value, row) {
                return row.action === value;
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
            isr_time(value) {
                let local_time = new Date(value+' EDT').toLocaleString();
                return new Date(local_time).toLocaleTimeString("en-US", {timeZone: "Asia/Jerusalem"});
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
            }
        },
        computed: {
            _items() {
                if (!this.items) {
                    return [];
                }

                let items = this.items;

                const fix = v => {
                    if (v instanceof Object) {
                        return Object.keys(v).map(k => fix(v[k])).join(' ');
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
                        if (field == 'creation_date') {
                            return flag ? new Date(a[field]) - new Date(b[field]) : new Date(b[field]) - new Date(a[field]);
                        } else {
                            return flag ? a[field] - b[field] : b[field] - a[field];
                        }
                    });
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
                if (value == 0) {
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
