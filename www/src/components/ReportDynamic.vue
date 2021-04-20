<template>
  <div id="report_dynamic" v-if="this.$store.state.user.role === 'admin'">

    <div class="flex-grid" v-show="!loading">

    </div>
    <div class="_centered" v-loading="loading" style="width: 100%"></div>

    <vue-progress-bar></vue-progress-bar>
    <vue-headful title="Report Dynamic"/>

    <form @submit="submit">
      <div class="row">

        <div class="col-xs-2">
          <websites-dropdown @selectWebsite="selectWebsite($event)"></websites-dropdown>
        </div>
        <div class="col-xs-1">
          <v-autocomplete v-model="selected_test" :items="test_filter_values" label="Test" @change="selectTest($event)"
                          no-data-text="Loading...">
          </v-autocomplete>
        </div>

        <div class="col-xs-1">
          <v-autocomplete v-model="selected_country" :items="country_filter" label="Country"
                          @change="selectCountry($event)"
                          no-data-text="Loading...">
          </v-autocomplete>
        </div>

        <div class="col-xs-1">
          <v-autocomplete v-model="selected_group" :items="group_filter" label="Group" @change="selectGroup($event)"
                          no-data-text="Loading...">
          </v-autocomplete>
        </div>
        <div class="col-xs-1">
          <v-autocomplete v-model="selected_devices" :items="devices_filter" label="Device"
                          @change="selectDevices($event)"
                          no-data-text="Loading...">
          </v-autocomplete>
        </div>
        <div class="col-xs-1">
          <v-autocomplete v-model="selected_win" :items="win_filter" label="Win" @change="selectWin($event)"
                          no-data-text="Loading...">
          </v-autocomplete>
        </div>
        <el-col :xs="{offset: 0}" :sm="{offset: 0}" :md="{offset: 0}" :lg="{span: 5, offset: 1}" :xl="3"
                style="width: 15.833% !important;margin-left: 0.167% !important; " class="col-xs-1">
          <v-menu full-width offset-y :close-on-content-click="false" bottom v-model="dateMenu">
            <v-btn color="primary" outline slot="activator">{{ date_range[0] }} &mdash; {{
                date_range[1]
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

          <v-btn type="submit" color="info" :disabled="!loadingbtn">Submit</v-btn>

        </div>

        <div class="col-xs-1">
          <download-excel style="" class="excel v-btn theme--light info" name="report_dynamic.xls"
                          :fields="json_fields"
                          :fetch="fetchData"
                          :before-generate="startDownload"
                          :before-finish="finishDownload"
                          type="xls"
                          >Export excel
            <i style="padding-left:10px;padding-bottom: 3px;" class="far fa-file-excel"></i>
          </download-excel>
        </div>
      </div>
    </form>
    <div v-show="!loading" v-if="_items.length > 0">

<table class="table table-striped">
  <thead>
    <tr>
      <th @click="headClick(field,key, true)" class="pointer"
              :class="[field.sortable?'sorting':null,sort===key?'sorting_'+(sortDesc?'desc':'asc'):'']"
              v-for="(field, key) in myfields">
            <span style="padding-right: 30px;">
            {{ field.label }}
            </span>
        </th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(item, index) in _items" v-if="item!==undefined" :ref="++index">
          <td>{{ item.website_name }}</td>
          <td>{{ item.test_name }}</td>
          <td>{{ item.country_code }}</td>
          <td>{{ item.test_group }}</td>
          <td>{{ item.device }}</td>
          <td>{{ item.dfp_pixel_test_group_total_sessions }}</td>

          <td>{{ item.dfp_total_revenue | _format(3) }}</td>
          <td>{{ item.dfp_total_imps }}</td>

          <td>{{ item.dfp_pixel_total_sessions }}</td>

          <td>{{ item.dfp_uv | _format(3) }}</td>
          <td>{{ item.tb_uv | _format(3) }}</td>
          <td>{{ item.total_uv | _format(3) }}</td>
          <td>{{ item.tb_revenue }}</td>
          <td>{{ item.total_revenue | _format(2) }}</td>
          <td>{{ item.win_order }}</td>
          <td>{{ item.diff }}</td>


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
    <div role="alert" class="el-alert el-alert--error is-center" style="font-weight: bold;" v-show='error'>
      <i class="el-alert__icon el-icon-error"></i>
      <div class="el-alert__content">
        <span class="el-alert__title">Sorry There is no records found! </span>
        <!----><i class="el-alert__closebtn el-icon-close" style="display: none;">

      </i>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment-timezone';

export default {
  name: 'report_dynamic',

  mounted() {
    this.get_filter_data();
    this.$emit('validateUser');

  },

  data() {
    return {
      selected_test: "All",
      test_filter_values: [],
      selected_country: "All",
      country_filter: [],
      selected_group: "All",
      group_filter: [],
      selected_devices: "All",
      devices_filter: [],
      selected_win: "All",
      win_filter: [],


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
      websites: [],

      json_fields: {
        "Website": "website_name",
        "Test": "test_name",
        "Country": "country_code",
        "Group": "test_group",
        "Device": "device",
        "Group sessions": "dfp_pixel_test_group_total_sessions",
        "DFP Total Revenue": "dfp_total_revenue",
        "IMPS": "dfp_total_imps",
        "total sessions": "dfp_pixel_total_sessions",
        "dfp uv": "dfp_uv",
        "tb uv": "tb_uv",
        "total uv": "total_uv",
        "tb_revenue": "tb_revenue",
        "total revenue": "total_revenue",
        "Win Order": "win_order",
        "diff": "diff"
      },
      myfields: {
        website_name: {label: 'Website', sortable: true},
        test_name: {label: 'Test', sortable: true},
        country_code: {label: 'Country', sortable: true},
        test_group: {label: 'Group', sortable: true},
        device: {label: 'Device', sortable: true},
        dfp_pixel_test_group_total_sessions: {label: 'Group sessions', sortable: true},
        dfp_total_revenue: {label: 'DFP Total Revenue', sortable: true},
        dfp_total_imps: {label: 'IMPS', sortable: true},
        dfp_pixel_total_sessions: {label: 'total sessions', sortable: true},
        dfp_uv: {label: 'dfp uv', sortable: true},
        tb_uv: {label: 'tb uv', sortable: true},
        total_uv: {label: 'total uv', sortable: true},
        tb_revenue: {label: 'tb revenue', sortable: true},
        total_revenue: {label: 'total revenue', sortable: true},
        win_order: {label: 'Win Order', sortable: true},
        diff: {label: 'diff', sortable: true},

      },

      limit_date: moment.utc().startOf('day').format("YYYY-MM-DD"),

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
      test: "All",
      country: "All",
      group: "All",
      win: "All",
      devices: "All",

      currentPage: 1,
      perPage: 20,
      minClicks: 0,
      brl_currency: 1,
      date_range: [
        moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
        moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
      ],
      site_id: "All",

    }
  },
  methods: {

    get_filter_data: function () {
      this.loadingbtn = false;

      let params = {

        'start': moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
        'end': moment(new Date(Date.now() - 8.64e7)).format("YYYY-MM-DD"),
        'login_time': this.$store.getters.getUser.loginTime,
      };
      // this.$http.get("/api/website/source").then(res => {
      this.$http.get("/api/reports/get_dynamic_filters", {params: params}).then(res => {


        if (res.body) {

          this.test_filter_values = res.body.test;
          this.test_filter_values.unshift('All');
          this.selected_test = this.test_filter_values[0];

          this.country_filter = res.body.country;

          this.country_filter.unshift('All');
          this.selected_country = this.country_filter[0];

          this.group_filter = res.body.group;
          this.group_filter.unshift('All');
          this.selected_group = this.group_filter[0];

          this.devices_filter = res.body.devices;
          this.devices_filter.unshift('All');
          this.selected_devices = this.devices_filter[0];

          this.win_filter = res.body.win;
          this.win_filter.unshift('All');
          this.selected_win = this.win_filter[0];
          this.loadingbtn = true;

        }
      });

    },
    async fetchData() {
      let site_id = this.site_id === 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;
      let start = moment(this.date_range[0]).format("YYYY-MM-DD");
      let end = moment(this.date_range[1]).format("YYYY-MM-DD");
      let params = {
        'site_id': 'all',
        'test': 'all',
        'country': 'all',
        'group': 'all',
        'devices': 'all',
        'win': 'all',
        'start': start,
        'end': end,
        'login_time': this.$store.getters.getUser.loginTime,
      };
      const response = await this.$http.get('/api/reports/get_dynamic_all_data', {params: params});
        return response.body.data;
    },
    
    startDownload() {
      this.loading = true;
    },
    finishDownload() {
      this.loading = false;
    },
    selectDevices(devices) {
      this.devices = devices;

    },
    selectWin(win) {
      this.win = win;

    },
    selectGroup(group) {
      this.group = group;
    },
    selectCountry(country) {
      this.country = country;
    },
    selectTest(test) {

      this.test = test;

    },

    selectWebsite(sites) {

      this.site_id = {'website_id': '', 'website_name': ''};
      sites.forEach(site => {
        this.site_id['website_id'] += site['website_id'] + ',';
        this.site_id['website_name'] += site['website_name'] + ',';
      });
      this.site_id['website_id'] = this.site_id['website_id'].slice(0, -1);
      this.site_id['website_name'] = this.site_id['website_name'].slice(0, -1);
      // this.submit();
    },

    onDateRangeChange(range) {

      this.date_range = range;
    },
    submit: function () {

      this.$Progress.start();
      this.loadingbtn = true;
      this.loading = true;
      let site_id = this.site_id === 'All' ? this.site_id.toLocaleLowerCase() : this.site_id.website_id;


      if (this.test === '') {
        this.test = 'all';
      }

      if (this.country === '') {
        this.country = 'all';
      }

      if (this.group === '') {
        this.group = 'all';
      }

      if (this.devices === '') {
        this.devices = 'all';
      }

      if (this.win === '') {
        this.win = 'all';
      }


      let start = moment(this.date_range[0]).format("YYYY-MM-DD");
      let end = moment(this.date_range[1]).format("YYYY-MM-DD");

      if (site_id === null) {
        this.alert('website');
        return;
      }

      this.loadingbtn = true;
      this.disabled = true;
      this.hide = true;

      let params = {
        'site_id': site_id,
        'test': this.test,
        'country': this.country,
        'group': this.group,
        'devices': this.devices,
        'win': this.win,
        'start': start,
        'end': end,
        'login_time': this.$store.getters.getUser.loginTime,
      };

      this.$http.get('/api/reports/get_dynamic_data', {params: params}).then(res => {

        if (res.body.data) {
          // return false;
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

          this.refreshLoading = false;
          this.$Progress.finish();
          this.loading = false;
          this.currentPage = 1;
          this.error = false;


        } else {
          this.$Progress.fail();
          this.error = true;


          console.log("---------ERROR-----------");
        }
      }).catch(e => {
        if (e.status === 401) {
          this.$emit('logout');
        }

        this.error = true;

        this.refreshLoading = false;
        this.loading = false;
        this.$Progress.fail();

      })
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
    filters: {
      _format(value, fix) {
          if ((!value && value !== 0) || !fix) {
              return '';
          }
          return parseFloat(value).toFixed(fix);
        }
    },
  computed: {

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

      return items;
    },
  },

}


</script>

<style scoped>
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
 white-space: nowrap; 
}

th{
  white-space: nowrap;
}


@import "../../node_modules/vuetify/dist/vuetify.min.css";
@import "../assets/styles/pages/_CampaignData.scss";
</style>
