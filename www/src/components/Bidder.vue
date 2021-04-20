<template>
    <div id="bidder_data" v-loading.fullscreen.lock="loading">
        <div class="row">
            <form class="top" @submit="submit">
                <div class="col-xs-12">
                    <div class="filter panel">
                        <div class="field_title f-filter">Date</div>
                        <el-switch v-model="switches.date_switch" name="date" active-text="ON"
                                   inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <el-date-picker v-model="date_range" type="daterange" placeholder="Range"></el-date-picker>
                    </div>
                    <div class="filter panel f-filter">
                        <div class="field_title">Site</div>
                        <el-switch v-model="switches.site_switch" name="site" active-text="ON" inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <el-select v-model="site_id">
                            <el-option v-for="website in websites" :label="website.website_name"
                                       :value="website.website_id" :key="website.website_id">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="filter panel f-filter">
                        <div class="field_title">Device</div>
                        <el-switch v-model="switches.device_switch" name="device" active-text="ON" inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <el-select v-model="device" placeholder="Device">
                            <el-option v-for="device in devices" :label="device" :value="device"
                                       :key="device"></el-option>
                        </el-select>
                    </div>
                    <div class="filter panel f-filter">
                        <div class="field_title">Advertiser</div>
                        <el-switch v-model="switches.advertiser_switch" name="advertiser" active-text="ON"
                                   inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <el-select v-model="advertiser" placeholder="Advertiser">
                            <el-option v-for="advertiser in advertisers" :label="advertiser.publisher"
                                       :value="advertiser.publisher" :key="advertiser.publisher"></el-option>
                        </el-select>
                    </div>
                    <div class="filter panel f-filter">
                        <div class="field_title">Placement</div>
                        <el-switch v-model="switches.placement_switch" name="placement" active-text="ON"
                                   inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <b-form-input v-model="placement" placeholder="Placement"></b-form-input>
                    </div>
                    <div class="filter panel f-filter">
                        <div class="field_title">Source</div>
                        <el-switch v-model="switches.source_switch" name="source" active-text="ON" inactive-text="OFF"
                                   active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                        <b-form-input v-model="source" placeholder="Source"></b-form-input>
                    </div>
                </div>
                <div class="col-xs-12">
                    <div>&nbsp</div>
                    <el-input v-model="filter" placeholder="Search" style="width: 15%;margin-right: 25px;">
                    </el-input>
                    <button type="submit" class="btn btn-primary submit" @submit="submit" :disabled="_validDate">Submit
                    </button>
                    <el-button @click="exportTableToCSV()" class="pull-right">Export To CSV</el-button>
                </div>
            </form>
        </div>
        <div class="row">
            <!--Results Table-->
            <el-table :data="_items" show-summary :class="[hide ? 'thide' : '']">
                <el-table-column
                        v-for="column in active_columns"
                        :prop="column"
                        :label="fixTheaders(column)"
                        :key="column"
                        sortable
                >
                </el-table-column>
                <el-table-column
                        prop="impressions"
                        label="Impressions"
                        sortable
                >
                </el-table-column>
                <el-table-column
                        prop="revenue"
                        label="Revenue"
                        sortable
                >
                </el-table-column>
            </el-table>

        </div>
    </div>
</template>


<script>
    import moment from 'moment-timezone';

    export default {
        mounted() {
            this.get_dropdowns();
        },
        data() {
            return {
                filters: [
                    'date',
                    'site_id',
                    'device',
                    'advertiser',
                    'placement',
                    'source'
                ],
                filter: '',
                date_range: '',
                site_id: [],
                device: '',
                placement: '',
                advertiser: '',
                advertisers: '',
                source: '',
                country_code: '',
                websites: [],
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                columns: [
                    'date',
                    'website_name',
                    'device',
                    'publisher',
                    'placement',
                    'source',
                    'impressions',
                    'revenue'
                ],
                active_columns: [],
                view_columns: [],
                active_filters: [],
                items: [],
                loading: false,
                sw: '',
                switches: {
                    date_switch: true,
                    site_switch: false,
                    device_switch: false,
                    placement_switch: false,
                    advertiser_switch: false,
                    source_switch: false
                },
                hide: true,
                currentPage: 1,
                perPage: 20,
            }
        },
        watch: {
            date_range: function (value) {
                this.switches.date_switch = value.length !== 0;
            },
            site_id: function (value) {
                this.switches.site_switch = value.length !== 0;
            },
            device: function (value) {
                this.switches.device_switch = value.length !== 0;
            },
            placement: function (value) {
                this.switches.placement_switch = value.length !== 0;
            },
            advertiser: function (value) {
                this.switches.advertiser_switch = value.length !== 0;
            },
            source: function (value) {
                this.switches.source_switch = value.length !== 0;
            },
        },
        methods: {
            submit: function (event) {
                this.loading = true;
                event.preventDefault();
                if (this.switch_on()) {
                    let iterable = [
                        ['start_date', moment(this.date_range[0]).format("YYYY-MM-DD"), true],
                        ['end_date', moment(this.date_range[1]).format("YYYY-MM-DD"), true],
                        ['website_name', this.site_id, this.switches.site_switch],
                        ['device', this.device, this.switches.device_switch],
                        ['publisher', this.advertiser, this.switches.advertiser_switch], //stored as "publisher" in DB
                        ['placement', this.placement, this.switches.placement_switch],
                        ['source', this.source, this.switches.source_switch]
                    ];

                    let endpoint = this.set_endpoint(iterable);

                    this.$http.get(endpoint).then(res => {
                        if (res.body.data) {
                            let data = res.body.data;
                            this.active_columns = [];
                            this.active_columns = this.getActiveColumns();

                            this.items = Object.keys(data).map(key => data[key]);
                            if (this.items.length === 0) {
                                this.notice('Sorry, No data was found');
                                this.hide = true;
                            } else {
                                this.hide = false;
                            }
                            this.loading = false;
                        } else {
                            this.loading = false;
                            console.log("---------ERROR-----------");
                        }
                    });
                }
            },
            set_endpoint: function (switches) {
                let endpoint = `/api/bidder?date_switch=${this.switches.date_switch}&`;

                for (let filter of switches) {
                    if (filter[2] || filter[0] === "date_switch") { //if switch ON
                        let param = filter[0] + "=" + filter[1] + "&";
                        endpoint += param;
                    }
                }

                return endpoint.slice(0, -1)
            },
            get_dropdowns: function () {
                this.$http.get("/api/bidder/data").then(res => {
                    if (res.body.websites && res.body.advertisers) {
                        this.websites = Object.keys(res.body.websites).map(key => res.body.websites[key]);
                        this.websites.unshift({value: "all", website_name: "All", website_id: "0"});
                        this.advertisers = Object.keys(res.body.advertisers).map(key => res.body.advertisers[key]);
                        this.advertisers.unshift({publisher: "All"});

                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            groupArr(arr, prop) {
                if (prop.indexOf("advertiser") > -1) {
                    prop[prop.indexOf("advertiser")] = "publisher";
                }
                prop = Array.isArray(prop) ? prop : [prop];         //Convert to array if not

                return arr.reduce(function (groups, item) {
                    const val = prop.map(o => item[o]).join('|');     //Map and Concat all values of prop and use as key

                    groups[val] = groups[val] || [];
                    groups[val].push(item);
                    return groups
                }, {})
            },
            notice(message) {
                this.$alert(message, ' ', {
                    confirmButtonText: 'OK',
                    type: 'warning'
                });
            },
            switch_on() {
                for (const key in this.switches) {
                    if (this.switches.hasOwnProperty(key) && this.switches[key]) {
                        return true;
                    }
                }
                this.notice('At least one switch must be ON');
                this.loading = false;
                return false;
            },
            downloadCSV(csv, filename) {
                let csvFile;
                let downloadLink;

                csvFile = new Blob([csv], {type: "text/csv"});

                downloadLink = document.createElement("a");
                downloadLink.download = filename;
                downloadLink.href = window.URL.createObjectURL(csvFile);
                downloadLink.style.display = "none";
                document.body.appendChild(downloadLink);
                downloadLink.click();
            },
            exportTableToCSV() {
                let filename = 'header_bidder_' + moment().format('YYYY-MM-DD') + '.csv'
                let csv = [];
                let cols = Object.keys(this.items[0]);
                csv.push(cols);

                for (let i = 0; i < this.items.length; i++) {
                    let row = [];
                    for (var j = 0; j < cols.length; j++)
                        row.push(this.items[i][cols[j]]);
                    csv.push(row.join(","));
                }
                // Download CSV file
                this.downloadCSV(csv.join("\n"), filename);
            },
            fixTheaders(index) {

                if (index === 'website_name') return 'Website';
                if (index === 'publisher') return 'Advertiser';
                return index.charAt(0).toUpperCase().replace('_', ' ') + index.slice(1);
            },
            hasProperty(obj, column) {
                try {
                    if (obj.hasOwnProperty(column)) {
                        return true;
                    }
                } catch (err) {

                    return false;
                }
            },
            sumRow(column) {
                switch (column) {
                    case 'date':
                        let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                        let end = moment(this.date_range[1]).format("YYYY-MM-DD");
                        return `${start} / ${end}`;
                    case 'publisher':
                        return this.items[0][column];
                    case 'impressions':
                        let totalImp = 0;
                        for (let item of this.items) {
                            totalImp += item['impressions'];
                        }
                        return totalImp;
                    case 'revenue':
                        let totalRev = 0;
                        for (let item of this.items) {
                            totalRev += item['revenue'];
                        }
                        return totalRev.toFixed(2);
                    default:
                        return 'All';
                }
            },
            getActiveColumns() {
                const cols = [];
                for (let sw in this.switches) {
                    if (this.switches[sw]) {
                        let field = sw.replace("_switch", "");
                        field = field === "site" ? "website_name" : field;
                        field = field === "advertiser" ? "publisher" : field;
                        if (cols.indexOf(field) === -1) {
                            cols.push(field);
                        }
                    }
                }
                return cols;
            }
        },
        computed: {
            _items() {
                if (!this.items) {
                    return [];
                }

                let final_items = [];
                let items = this.items;
                let filter = this.filter;

                if (items.length) {
                    items = this.groupArr(items, this.getActiveColumns());
                }

                for (let idx in items) {
                    final_items.push(items[idx][0])
                }

                // Apply filter
                if (this.filter && this.filter.length > 0) {
                    final_items = final_items.filter(function (o) {
                        for (let i of Object.keys(o)) {
                            if (o[i].toString().toLowerCase().includes(filter.toString().toLowerCase())) {
                                return true;
                            }
                        }
                    })

                }

                return final_items;
            },
            _validDate() {
                return !(this.date_range.length === 2 && this.date_range[0] !== "undefined" && this.date_range[1] !== "undefined");
            }
        }
    }
</script>


<style scoped>
    .field_title {
        display: inline-block;
    }

    .el-switch {
        float: right;
        margin-bottom: 5px;
    }

    .filter {
        background: #dddddd;
        padding: 10px;
        border-radius: 5px;
        max-width: 15%;
        float: left;
        margin: 10px;
    }

    .f-filter {
        width: 14.9%;
    }

    .thide {
        display: none;
    }

    .el-button, .submit {
        display: inline-block;
    }

    .el-date-editor--daterange {
        width: inherit;
    }

    .summery {
        box-shadow: 0px 1px 5px 1px #777;
        background-color: #623542 !important;
        color: #fff;
    }
</style>