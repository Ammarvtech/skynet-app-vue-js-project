import moment from 'moment-timezone';

export default {
    data() {
        return {
            bidder: moment(new Date(Date.now())),
            show_bidder_time: false,
            bidder_deleting: false,
            bidder_saving: false,
        }
    },
    methods: {
        init_bidders() {
            for (let i of this.items) {
                i.pop_visible = false;
                if (typeof(i.bidders) == "string") {
                    i.bidders = JSON.parse(i.bidders);
                }
            }
        },
        add_bidder(item) {
            if (!item.bidders) {
                item.bidders = [];
            }

            if (item.bidders.length > 7) {
                this.$message({
                    message: 'Only 7 auto bidders allowed at the same time',
                    type: 'warning',
                    center: true
                });
                return;
            }

            const est = moment().tz('America/New_York').format("YYYY-MM-DD HH:mm");
            const start = moment(new Date(est));
            const remainder = 15 - (start.minute() % 15);
            const dateTime = moment(start).add(remainder, "minutes").format("YYYY-MM-DD HH:mm");

            item.bidders.push({
                'execution_time': moment(dateTime).format("HH:mm"),
                'site_id': item.site_id,
                'campaign_id': item.campaign_id,
                'source': item.source,
                'new_bid': item.bid,
                'new': true,
            });
            this.$forceUpdate();
        },
        save_bidder(item) {
            item.pop_visible = false;
            this.bidder_saving = true;
            this.bidder_deleting = true;
            let bidders = item.bidders;

            bidders = bidders.filter((set => f => !set.has(f.execution_time) && set.add(f.execution_time))(new Set));

            if (item.bidders.length > bidders.length) {
                this.$message({
                    message: 'You trying to scheduled bids at the same time! only one will be saved',
                    type: 'error',
                    center: true
                });
            } else {
                this.$message({message: 'Saving...', type: 'warning', center: true});
            }

            bidders.forEach(function (v) {
                delete v.new;
                delete v.id;
            });

            let params = {
                'bidders': JSON.stringify(bidders),
                'source': item.source,
                'site_id': item.site_id,
                'campaign_id': item.campaign_id,
                'login_time': this.$store.getters.getUser.loginTime,
            };

            const self = this;
            this.$http.get('/api/bidder/save_bidders', {params: params}).then(res => {
                if (res.body) {
                    item.bidders = JSON.parse((res.body['res'][0].bidders));
                    this.bidder_saving = false;
                    this.bidder_deleting = false;
                    setTimeout(function () {
                        self.$message({message: 'Scheduled bid successfully saved', type: 'success', center: true});
                    }, 2000);
                } else {
                    this.$message({
                        message: 'Error has occurred while trying to delete scheduled bid, Please try again',
                        type: 'error',
                        center: true
                    });
                }
            }).catch(e => {
                if(e.status === 401) {
                    this.$emit('logout');
                }
                else {
                    this.$message({
                        message: 'Error has occurred while trying to delete scheduled bid, Please try again',
                        type: 'error',
                        center: true
                    });
                }
            });
        },
        remove_bidder(item, index) {
            if (item && item.bidders[index].new === true) {
                item.bidders.splice(index, 1);
                this.$forceUpdate();
            } else if (item && item.bidders[index].new === 'false') {
                this.bidder_deleting = true;
                this.$message({message: 'Deleting...', type: 'warning', center: true});
                let params = {
                    'id': item.bidders[index].id,
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.get('/api/bidder/remove_bidder', {params: params}).then(res => {
                    if (res.body) {
                        let deleted = res.body['res'];
                        if (deleted === 1) {
                            item.bidders.splice(index, 1);
                            this.$message({
                                message: 'Scheduled bid successfully deleted',
                                type: 'success',
                                center: true
                            });
                            this.bidder_deleting = false;
                        }
                    } else {
                        this.$message({
                            showClose: true,
                            message: 'Error has occurred while trying to delete scheduled bid, Please try again"',
                            type: 'error',
                            center: true
                        });
                    }
                }).catch(e => {
                    this.loading = false;
                    if (e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
            }
        },
        reset_bidder_time(item) {
            if (item && item.bidders && Array.isArray(item.bidders)) {
                if (item.bidders && item.bidders.length > 0) {
                    item.bidders = item.bidders.filter(i => i.new != true);
                }

                const est = moment().tz('America/New_York').format("YYYY-MM-DD HH:mm");
                const start = moment(new Date(est));
                this.bidder = moment(new Date(start));

                this.show_bidder_time = false;
                this.$forceUpdate();
            }
        },
        refresh_bidder() {
            this.$forceUpdate();
        },
    }
}