<template>
    <div id="dealer-status-screen">
        <vue-headful title="Dealer Status"/>
        <div v-if="role=='admin'" class="row">
            <div class="col-xs-2">
                <el-date-picker v-model="date_range" type="daterange"></el-date-picker>
            </div>
            <div class="col-xs-2 col-xs-push-1">
                <el-select v-model="user_id">
                    <el-option v-for="user in users" :label="user.full_name" :value="user.user_id" :key="user.user_id">
                    </el-option>
                </el-select>
            </div>
            <div class="col-xs-2 col-xs-push-1">
                <button type="submit" class="btn btn-primary" @click="submit()" :disabled="loading">Submit</button>
            </div>
        </div>
        <hr class="style-one">
        <el-table v-loading="loading" :data="items" style="width: 100%">
            <el-table-column type="expand"><template slot-scope="props"><p>{{ props.row.status | msg}}</p></template></el-table-column>
            <el-table-column prop="update_date" label="Last Update" sortable width="180">                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="top">
                                <span>Israel Time: {{isr_time(scope.row.update_date)}} </span>
                                <div slot="reference">
                                    <span>{{ scope.row.update_date }}</span>
                                </div>
                            </el-popover>
                        </template></el-table-column>
            <el-table-column prop="source" label="Source" sortable width="180"></el-table-column>
            <el-table-column prop="action" label="Action Name" sortable width="270"></el-table-column>
            <el-table-column prop="website_name" sortable label="Website" :filters="filter_website" :filter-method="filterWebsite" filter-placement="bottom-end"></el-table-column>
            <!--<el-table-column prop="account" sortable label="Account"></el-table-column>-->
            <el-table-column prop="campaign_id" sortable label="Campaign ID"></el-table-column>
            <el-table-column prop="item_id" sortable label="Item Id"></el-table-column>
            <el-table-column prop="status_name" sortable label="Status" :filters="filter_status" :filter-method="filterStatus" filter-placement="bottom-end">
                <template slot-scope="scope">
                    <el-tag
                            :type="scope.row.status_name === 'DONE' ? 'success' : scope.row.status_name === 'ERROR' ? 'danger' : 'primary'"
                            close-transition>{{scope.row.status_name}}
                    </el-tag>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import moment from 'moment-timezone';
    import alerts from "./mixins/alerts";

    export default {
        name: 'dealer-status-screen',
        mixins: [alerts],
        mounted() {
            this.$emit('validateUser');
            this.get_users();
            // this.get_data();
        },
        data() {
            return {
                items: [],
                websites: [],
                user_id: null,
                role: 'admin',
                filter_status: [{text: 'DONE', value: 'DONE'}, {text: 'STAGED', value: 'STAGED'}, {text: 'ERROR', value: 'ERROR'}, {text: 'IN_PROCESS', value: 'IN_PROCESS'}],
                filter_website: [],
                users: [],
                date_range: [new Date(Date.now()), new Date(Date.now())],
                loading: false,
            }
        },
        methods: {
            get_data(usr) {
                this.loading = true;
                let start = moment(this.date_range[0]).format("YYYY-MM-DD");
                let end = moment(this.date_range[1]).format("YYYY-MM-DD");

                let params = {'date_start': start, 'date_end': end};

                if (usr) {
                    params['user_id'] = this.user_id
                }

                this.$http.get("/api/dealer/data", {params: params}).then(res => {
                    if (res.body) {
                        this.items = Object.keys(res.body).map(key => res.body[key]);
                        let websites = this.filter_website;

                        for (let i = 0; i < this.items.length; i++) {
                            if (!websites.find(x => x.text === this.items[i].website_name)) {
                                websites.push({text: this.items[i].website_name, value: this.items[i].website_name})
                            }
                        }
                    }
                    else {
                        this.notice('Sorry, No Data was found');
                        console.log("---------ERROR-----------");
                    }
                    this.loading = false;
                });
            },
            get_users() {
                this.$http.get("/api/dealer/users").then(res => {
                    if (res.body) {
                        this.users = Object.keys(res.body).map(key => res.body[key]);
                        this.user_id = this.users[0]['user_id'];
                    }
                    else {
                        this.notice('Sorry, No Data was found');
                        console.log("---------ERROR-----------");
                    }
                });
            },
            isr_time(value) {
                let local_time = new Date(value+' UTC').toLocaleString();
                return new Date(local_time).toLocaleTimeString("en-US", {timeZone: "Asia/Jerusalem"});
            },
            submit() {
                this.get_data(true);
            },
            filterStatus(value, row) {
                return row.status_name === value;
            },
            filterWebsite(value, row) {
                return row.website_name === value;
            },
        },
        filters: {
            msg: function (value) {
                let msg = value.toLowerCase();
                if (msg.indexOf('done') > -1) {
                    return "DONE"
                }
                if (msg.indexOf('keyerror') > -1 || msg.indexOf('valueerror') > -1) {
                    if(msg.indexOf('decoded') > -1 || msg.indexOf('callable') > -1){
                        return "Error has occurred, Please try again"
                    }
                    return JSON.parse(msg)['info']
                }
                if (msg.indexOf('message') > -1) {
                    return value.split("u'message': u'")[1].split("'")[0]
                }
                if (msg.indexOf('exception') > -1) {
                    return value.split("Exception: ")[1].split('n"')[0]
                }

                return value;
            }
        }
    }

</script>