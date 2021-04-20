<template>
    <div id="app_factor" v-if="this.$store.state.user.role === 'admin'">
        <h1>Discrepancy Factor</h1>
        <div class="flex-grid" v-show="!loading">
            <div>
                <h2 style="font-size:25px;">Factor to all sites
                    <p style="font-size:15px;">the factor will be deducted from revenue report, campaigns (including
                        real time), and mediums</p>
                    <p style="font-size:11px;">example :</p>
                    <p style="font-size:10px;">if factor = 5 then 5 precent will be deducted</p>
                </h2>
                <el-input-number v-model="num" :precision="0" :step="1" :max="100" :min="0"></el-input-number>
                <span style="padding-left:5px;font-size:25px;">%</span>
                <el-button type="primary" plain @click="handleSubmit()" style="margin-left:30px">Submit</el-button>
            </div>
            <el-table :data="factorData" style="width: 100%">
                <el-table-column prop="factor" label="Factor Changed To" width="auto"></el-table-column>
                <el-table-column prop="data_date" label="Date Of Change" width="auto"></el-table-column>
            </el-table>
        </div>
        <div class="_centered" v-loading="loading" style="width: 100%"></div>
    </div>
</template>

<script>
    import moment from 'moment-timezone';


    export default {
        name: 'Factor',
        mounted() {
            this.getHistory()
        },
        data() {
            return {
                date: moment().subtract(0, "days").tz("America/New_York").format("YYYY-MM-DD"),
                num: 0,
                loading: true,
                status: '',
                factorData: [],
            }
        },
        methods: {
            getHistory() {
                this.loading = true;
                this.$http.get("/api/get_factor").then(res => {
                    this.factorData = res.body.data;
                    this.loading = false;
                }, res => {
                    this.$notify({
                        title: "Warning",
                        message: "Failed to get factor history",
                        type: "warning"
                    });
                    this.loading = false;
                });
            },
            handleSubmit() {
                this.loading = true;
                this.$http.post("/api/set_factor", {
                    factor: (1 - (this.num / 100)),
                    date: this.date
                }).then(res => {
                    this.status = res.status;
                    if (this.status === 200) {
                        this.$notify({
                            title: "Great!",
                            message: "Submitted Factor!",
                            type: "success"
                        });
                        this.loading = false;
                        this.getHistory();
                    }
                }, res => {
                    this.error = true;
                    this.$notify({
                        title: "Warning",
                        message: "Failed to Submit Factor",
                        type: "warning"
                    });
                });

            },
        },
    }
</script>
<style scoped>
    .flex-grid {
        min-width: 50%;
        max-width: 90%;
    }

    ._centered {
        position: fixed;
        top: 50% !important;
        left: 0 !important;
    }
</style>

