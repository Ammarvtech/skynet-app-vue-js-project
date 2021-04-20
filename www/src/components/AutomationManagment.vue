<template>
    <div v-if="show_auto_management" id="AutomationManagment">
       
        <div class="flex-grid" v-show="!loading">
        </div>
        <div class="_centered" v-loading="loading" style="width: 100%"></div>
        <vue-progress-bar></vue-progress-bar>
        

              <form @submit="submit">
          
        <div class="row">
        
            <div class="col-xs-1">

                <websites-multi-dropdown-checkbox @selectWebsite="selectWebsite($event)">
                </websites-multi-dropdown-checkbox>
        
            </div>

            <div class="col-xs-3">
                <v-autocomplete v-model="selected_automation" :items="automation_items" label="Automation" @change="selectAutomation($event)"
                    no-data-text="Loading..." >                       
                </v-autocomplete>
            </div>


            <div class="col-xs-1">
                <v-autocomplete v-model="selected_status_val" :items="status" label="Status" @change="selectStatus($event)"
                    no-data-text="Loading..." >                       
                </v-autocomplete>
            </div>
            <div class="col-xs-1">
                <sources-dropdown @selectSource="selectSource($event)"></sources-dropdown>
            </div>
            
                <el-col :xs="{offset: 0}" :sm="{offset: 0}" :md="{offset: 0}" :lg="{span: 5, offset: 1}" :xl="3"
                        style="width: 15.833% !important;margin-left: 0.167% !important; " class="col-xs-1">
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

                <div class="col-xs-1">
                    <v-btn type="submit" color="info">Submit</v-btn>
                </div>

                <div v-if="_items.length > 0" class="col-xs-1">
                    <download-excel style="" class="excel v-btn theme--light info" name="report_AutomationManagment.xls"
                                    :fields="json_fields" :data="items_copy">Export excel
                        <i style="padding-left:10px;padding-bottom: 3px;" class="far fa-file-excel"></i>
                    </download-excel>
                </div>
            </div>
        </form>
       
           <div v-if="_items.length > 0">
            <table class="table table-striped table-hover">
                <thead>
                <tr>
             
                  <!--   <th @click="headClick(field,key, true)" class="pointer">
                        <input type="checkbox" v-model="selectAll">
                    </th> -->
                    <th @click="headClick(field,key, true)" class="pointer"
                        :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"
                        v-for="(field, key) in myfields" >
                        {{ field.label }}

                    </th>
            </tr>
        </thead>
        <tbody>
             
              <tr v-if="items.length > 0"
                    style="background-image: linear-gradient(180deg, #cbdbf7 0%, #e8f1f7 100%);">
                   <!--  <td>
                        
                    </td> -->
               <td style="width: 50px;">            
                    <span  v-if="!sumSites">Null</span>
                    <span  v-else>{{ sumSites }}</span>
                </td>        
                <td style="width: 92px;">          
                    <span  v-if="!sumOfAutomation">0</span>
                    <span  v-else>{{ sumOfAutomation }}</span>
                </td>
                <td style="width: 92px;">            
                    <span  v-if="!sumOfSource">0</span>
                    <span  v-else>{{ sumOfSource }}</span>
                </td> 
                 <td style="width: 92px;">            
                    <span  v-if="!sum_profit">0</span>
                    <span  v-else>{{ Number((sum_profit).toFixed(3)) }}</span>
                </td> 
                 <td style="width: 92px;">            
                    <span  v-if="!sum_profit_percentage">0</span>
                    <span  v-else>{{ Number((sum_profit_percentage).toFixed(3)) }}</span>
                </td> 
                <td style="width: 92px;">            
                    <span  v-if="!sum_comapaign">0</span>
                    <span  v-else>{{ Number(( sum_comapaign ).toFixed(3)) }}</span>
                </td> 
                <td style="width: 92px;">            
                    <span  v-if="!sum_spend">0</span>
                    <span  v-else>{{ Number(( sum_spend ).toFixed(3)) }}</span>
                </td> 
                <td style="width: 92px;">            
                    <span  v-if="!sum_negative_profit">0</span>
                    <span  v-else>{{ Number(( sum_negative_profit ).toFixed(3)) }}</span>
                </td> 
                <td style="width: 92px;">            
                    <span  v-if="!sum_negative_profit_percentage">0</span>
                    <span  v-else>{{ Number(( sum_negative_profit_percentage ).toFixed(3)) }}</span>
                </td> 
                <td style="width: 92px;">            
                    <span  v-if="!( (sum_profit + sum_spend) / sum_spend )">0</span>
                    <span  v-else>{{ Number(( (sum_profit + sum_spend) / sum_spend ).toFixed(3)) }}</span>
                </td> 
              
                <td style="width: 92px;">     
                    <span  v-if="!sum_is_active">0</span>
                    <span  v-else>{{ sum_is_active }}</span>
                </td>

            </tr>
            <tr v-for="(item, index) in _items" v-if="item!==undefined" :ref="++index">
           <!--      <td style="width: 50px;"> 
                <input type="checkbox" v-model="selected" :value="item.site_id" number>  
                </td>    -->          
                <td style="width: 92px;">
                    <span  v-if="!item.acronym">NA</span>
                    <span  v-else>{{ item.acronym }}</span>
                </td>

                <td style="width: 92px;">
                       <el-tooltip placement="top">
                            <div slot="content">{{item.description}}</div>
                            <span  v-if="!item.name">NA</span>
                            <span  v-else>{{ item.name }}</span>
                        </el-tooltip>
                    
                </td>
                <td style="width: 92px;">
                    <span  v-if="!item.source">NA</span>
                    <span  v-else>{{ item.source }}</span>
                </td>
                <td style="width: 92px;">
                  
                  <span  v-if="item.profit == null">NA</span>
                    <span  v-else>{{ item.profit }}</span>
                </td>
                <td style="width: 92px;">
                   

                 <span  v-if="item.profit_prcnt == null">NA</span>
                    <span  v-else>{{ item.profit_prcnt }}</span> 
                </td>
                <td style="width: 92px;">
                    <span  v-if="item.campaigns_amount == null">NA</span>
                    <span  v-else>{{ item.campaigns_amount }}</span>
                </td>
                <td style="width: 92px;">
                    <span  v-if="item.spend == null">NA</span>
                    <span  v-else>{{ item.spend }}</span>
                </td>
                <td style="width: 92px;">
                    <span  v-if="item.negative_profit == null">NA</span>
                    <span  v-else>{{ item.negative_profit }}</span>
                </td>
                <td style="width: 92px;">
                    <span  v-if="item.negative_profit_prcnt == null">NA</span>
                    <span  v-else>{{ item.negative_profit_prcnt }}</span>
                </td>
                <td style="width: 92px;">
                    <span  v-if="item.ROI == null">NA</span>
                    <span  v-else>{{ item.ROI }}</span>
                </td>
                <td style="width: 92px;">

                 
                    <span>

                        <v-switch v-model="item.is_active" 
                                  @change="forceUpdate(item.site_id,item.name,item.is_active)">
                                      
                        </v-switch>
                     
                    </span> 
                </td>   
                 
            </tr>
            <tr >
              
                   <el-tooltip placement="top">
                                <div slot="content">
                                    <div>No revenue to display</div>
                                </div>
                              
                    </el-tooltip>
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
                                style="height: 31px">
                        <el-input-number size="small" v-model="minClicks" controls-position="right" :min="0"
                                         :step="100"></el-input-number>
                    </el-tooltip>
                    <div class="col-md-11 text-center" style="top: -52px">
                        <b-pagination size="md" :total-rows="items.length" :per-page="perPage" v-model="currentPage"/>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import moment from 'moment-timezone';

    export default {
      name: 'AutomationManagment',

      mounted() {
      
        this.get_automation_data();
        this.get_status_data();

        this.$emit('validateUser');

      },

      data() {

        return {
        website_name:[],
    

                // selected_site: "All",
                // site_filter: [],
                currentState: this.defaultState,
                selected_status: "All",
                selected_status_val: "All",          
                items: [],
                summary: [],
                selected: [],
                sumSites: [],         
                sumOfSource: [],
                sumOfCompaigns: [],
                sumOfSpend: [],
                sumOfRoi: [],
                sumOfActive: [],
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
                show_auto_management: this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.auto_management == 1,
                sumOfAutomation: [],
                inited_summary: {},
                sortDesc: true,
                sortFlag: false,
                loading: false,
                error: false,
                loadingbtn: false,
                refreshLoading: false,
                disabled: true,
                hide: true,
                animated: false,

                sort: null,
                filter: null,  
                currentPage: 1,
                perPage: 20,
                minClicks: 0,
                brl_currency: 1,
                date_range: [
                    moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                    moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
                ],
                items_copy: [],
                site_id: "All",
                sum_profit: undefined,
                sum_profit_percentage: undefined,
                sum_comapaign: undefined,
                sum_spend: undefined,
                sum_negative_profit: undefined,
                sum_negative_profit_percentage: undefined,
                sum_roi: undefined,
                sum_is_active: undefined,
         
                automation_keyword: [],
                source: [],          
                profit: [],          
                profit_prcnt: [],          
                campaigns_amount: [],
                spend: [],
                negative_profit: [],
                negative_profit_prcnt: [],
                ROI: [],
                is_active: [],   
                field: [],   
                key: [], 
                selected_campaign_source: [], 
                selected_automation: [], 

                status: [
                  "Enabled",
                  "Disabled",                             
                ], 
                automation_items:[],
                selectedPerson: "",           
                myfields: {
                        acronym: {label:'Site', sortable: true},
                        name: {label:'Automation', sortable: true},
                        source: {label:'Source', sortable: true},          
                        profit: {label:'Profit', sortable: true},          
                        profit_prcnt: {label:'Profit %', sortable: true},          
                        campaigns_amount: {label:'Campaign amount', sortable: true},
                        spend: {label:'Spend', sortable: true},
                        negative_profit: {label:'Negative profit', sortable: true},
                        negative_profit_prcnt: {label:'Negative %', sortable: true},
                        ROI: {label:'ROI', sortable: true},
                        is_active: {label:'Status'},           
                    },
                json_fields: {

                    "Website": "acronym",
                    "Automation": "name",
                    "Source": "source",
                    "Profit": "profit",
                    "Profit %": "profit_prcnt",
                    "Campaign amount": "campaigns_amount",
                    "Spend": "spend",
                    "Negative profit": "negative_profit",
                    "Negative %": "negative_profit_prcnt",
                    "ROI": "ROI",
                    "Status": "is_active"
                },
        }
      },
      methods: { 
      
    
        forceUpdate: function (site_id,automation,is_active) {
         
            // this.$confirm('You are about to reverse the automation for X automations', 'Alert',
            //     {
            //         confirmButtonText: 'Approve',
            //         cancelButtonText: 'Cancel',
            //         type: 'warning'
            //     }).then(() => {

                if(is_active === true){
                    is_active = 1;
                }
                if(is_active === false){
                    is_active = 0;
                }
                let params = {
                'name': automation,
                'active': is_active,
                'site': site_id,
                'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.get("/api/reports/toggle_automation",{params: params}); 
                // }).catch(() => {

                // this.is_active = 1;
                //  }); 
            },
        get_status_data: function () {

            this.status.unshift('All');     
            this.selected_status = this.status[0];


        },
        get_automation_data: function () {

            let params = {
            'login_time': this.$store.getters.getUser.loginTime,
            };
                    // this.$http.get("/api/website/source").then(res => {
                this.$http.get("/api/reports/get_automation_names",{params: params}).then(res => {
                        
                        this.automation_items = res.body.data;
                        this.automation_items = Object.values(res.body.data).map(i => i.name);
                        this.automation_items.unshift('All');
                        this.selected_automation = this.automation_items[0];
                    });
             
            },
        selectWebsite(sites) {
               
                this.site_id = {'website_id': '', 'website_name': ''};
                sites.forEach(site => {
                    this.site_id['website_id'] += site['website_id'] + ',';
                    this.site_id['website_name'] += site + ',';
                });
               
                this.site_id['website_id'] = this.site_id['website_id'].slice(0, -1);
                this.site_id['website_name'] = this.site_id['website_name'].slice(0, -1);
               
        },
        selectStatus(status) {
            this.selected_status_val = status;

            if(status === 'Enabled'){
                status = 1;
                this.selected_status = status;

            }  
            if(status === 'Disabled'){
                status = 0;
                this.selected_status = status;

            } 

        },
        selectAutomation(automation) {
            this.selected_automation = automation;
        },
        onDateRangeChange(range) {

                this.date_range = range;
        },
               submit: function () {

                this.$Progress.start();
                this.loadingbtn = true;
                this.loading = true;
                let site_id = this.site_id === 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
                if(site_id === '' || site_id === undefined){
                    site_id = 'All';
                }
                if(this.selected_automation === '' || this.selected_automation === undefined){
                    this.selected_automation = 'All';
                }
                if(this.selected_status === '' || this.selected_status === undefined){
                    this.selected_status = 'All';
                }
                if(this.selected_campaign_source === '' || this.selected_campaign_source === undefined){
                    this.selected_campaign_source = 'All';
                }             
            
                
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");

                this.loadingbtn = true;
                this.disabled = true;
                this.hide = true;
                let params = {
      
                    'sites': site_id,
                    'sources': this.selected_campaign_source,
                    'status': this.selected_status,
                    'name': this.selected_automation,
                    'start': start,
                    'end': end,
                    'login_time': this.$store.getters.getUser.loginTime,
                    };
                this.$http.get("/api/reports/get_automation_data",{params: params}).then(res => {
                        
                           
                        if (res.body.data) {
                            this.items = res.body.data;
                            this.items_copy = this.items;
                            this.sortDesc = false;
                            this.hide = false;
                            this.disabled = false;  
                            this.refreshLoading = false;
                            this.$Progress.finish();  
                            if (this.items.length === 0) {
                            this.filterClose();
                            } else {
                                this.sortDesc = false;
                                this.hide = false;
                                this.disabled = false;
                            }
                            this.loading = false;
                            this.currentPage = 1;
                            this.error = false;

                        }
                });

               
            },
        selectSource(source) {
                this.selected_campaign_source = source;

        },
       triggerEvent(value) {
          this.active = value;
        },
      
        count_values(key, data) {
           return Object.keys(data.reduce((acc, o) => (acc[o[key]] = (acc[o[key]] || 0) + 1, acc), {})).length;
        },
            filter_summary() {
                let items = this.items;
            
                if (this.filter && this.filter.length > 0) {
                    this.filter = this.filter.trim().toLowerCase();
                    const regex = new RegExp('.*' + this.filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                }
                return items;
            },
            headClick(field, key, flag = false) {
                
                if (flag) this.sortFlag = !this.sortFlag;

                if (!field.sortable) {
                    return;
                }
                if (key === this.sort) {
                    this.sortDesc = !this.sortDesc;
                }
             
                this.sort = key;
            },
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
                let keys = ['profit','profit_prcnt','negative_profit','negative_profit_prcnt','campaigns_amount','spend','ROI','is_active'];
                const self = this;
               
                    
                _.each(data, function (item) {
                    
                    _.each(keys, function (key) {
                         
                        sums[key] = (sums[key] || 0) + item[key];
                    });
                });
                
                this.sum_profit = sums.profit;
                this.sum_profit_percentage = sums.profit_prcnt;
                this.sum_comapaign = sums.campaigns_amount;
                this.sum_spend = sums.spend;
                this.sum_negative_profit = sums.negative_profit;
                this.sum_negative_profit_percentage = this.sum_negative_profit / (this.sum_profit - this.sum_negative_profit);

                this.sum_roi = sums.ROI;
                this.sum_is_active = sums.is_active;
        

                this.emptySummary = true;
            },
        defaultState: function defaultState() {
            this.currentState = Boolean(this.defaultState)
        }

    },
       computed: {
        
        selectAll: {
            get: function () {
                return this.items ? this.selected.length == this.items.length : false;
            },
            set: function (value) {
                var selected = [];

                if (value) {
                    this.items.forEach(function (items) {
                        selected.push(items.site_id);
                    });
                }

                this.selected = selected;
               
        }},

        isActive() {
            return this.currentState;
        },

        enableText() {
            return this.labelEnableText;
        },

        disabledText() {
            return this.labelDisableText;
        },

        checkedValue: {
            get() {
                return this.currentState;
            },

            set(newValue) {
                this.currentState = newValue;
                this.$emit('change', newValue);
            }
        },
                _items() {
                if (!this.items) {
                    return [];
                }


                let items = this.items;
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

                this.sumSites =this.count_values('acronym',this.items);
                this.sumOfAutomation =this.count_values('name',this.items);
                this.sumOfSource =this.count_values('source',this.items);
                this.sumOfCompaigns =this.count_values('campaigns_amount',this.items);
                this.sumOfSpend =this.count_values('spend',this.items);
                this.sumOfRoi =this.count_values('ROI',this.items);
                this.sumOfActive =this.count_values('is_active',this.items);

                return items;
            },
       },

    }
</script>

<style scoped>

.toggle__button {
    vertical-align: middle;
    user-select: none;
    cursor: pointer;
}
.toggle__button input[type="checkbox"] {
    opacity: 0;
    position: absolute;
    width: 1px;
    height: 1px;
}
.toggle__button .toggle__switch {
    display:inline-block;
    height:12px;
    border-radius:6px;
    width:40px;
    background: #BFCBD9;
    box-shadow: inset 0 0 1px #BFCBD9;
    position:relative;
    margin-left: 10px;
    transition: all .25s;
}

.toggle__button .toggle__switch::after, 
.toggle__button .toggle__switch::before {
    content: "";
    position: absolute;
    display: block;
    height: 18px;
    width: 18px;
    border-radius: 50%;
    left: 0;
    top: -3px;
    transform: translateX(0);
    transition: all .25s cubic-bezier(.5, -.6, .5, 1.6);
}

.toggle__button .toggle__switch::after {
    background: #4D4D4D;
    box-shadow: 0 0 1px #666;
}
.toggle__button .toggle__switch::before {
    background: #4D4D4D;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.1);
    opacity:0;
}

.active .toggle__switch {
    background: #adedcb;
    box-shadow: inset 0 0 1px #adedcb;
}

.active .toggle__switch::after,

.active .toggle__switch::before{
transform:translateX(40px - 18px);
}

.active .toggle__switch::after {
    left: 23px;
    background: #53B883;
    box-shadow: 0 0 1px #53B883;
}
    .box {
      text-align: center;
      margin-bottom: 30px;
    }

    .toggle_container {
        margin: 0px auto;
        background: #efefef;
        width: 120px;
        padding: 10px 0;
        border-radius: 30px;
        transition: all .25s;
    }
    .toggle_container.active {
        background: #e9ffef;
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
    ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }

    td {
        vertical-align: middle !important;
        padding: 8px !important;
    }
    @import "../../node_modules/vuetify/dist/vuetify.min.css";
    @import "../assets/styles/pages/_CampaignData.scss";


</style>
