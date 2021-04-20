export default {
    data() {
        return {
            checked_items: [],
            brl_currency: 1,
            roi_adjust: 1.3,
            bulk_adjust_loading: false,
            roiAdjustView: false,
            stop: false,
            min_bulk_value: 0.7,
            max_bulk_value: 2,
            display_bulk_change: false,
        }
    },
    mounted() {
        this.display_bulk_change = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.display_bulk ? this.$store.getters.getUser.settings.display_bulk === '1' : false;
    },
    methods: {
        campaign_selected_init() {
            for (let index in this.items) {
                this.items[index]['index'] = index;
            }
        },
        adjustNotice(items, action = 'roiAdjust') {
            let msg = '';
            let item = this.checked_items[0];
            if (action === 'roiAdjust') {
                if (items.length === 1) {
                    let val = this.roi_adjust;
                    msg = "You are about to adjust ROI on campaign " + item.campaign_id + " from " + parseInt(item.roi_current * 100) + "% to " + parseInt(val * 100) + "%\n"
                }
                if (items.length > 1) {
                    msg = "You are about to adjust ROI on " + items.length + " campaigns to " + parseInt(this.roi_adjust * 100) + "%"
                }
            }
            this.$confirm(msg, 'Warning', {
                confirmButtonText: 'Yes',
                cancelButtonText: 'Cancel',
                type: 'warning',
                center: true,
                customClass: 'roi_notice_msg'
            }).then(() => {
                this.$message({
                    type: 'success',
                    message: 'Action in process',
                    center: true
                });
                if (action === 'roiAdjust') {
                    this.applyRoiAdjust();
                }
            }).catch(() => {
                this.bulk_adjust_loading = false;
                this.$message({
                    type: 'warning',
                    message: 'Action canceled',
                    center: true
                });
            });
        },
        applyRoiAdjust() {
            this.bulk_adjust_loading = true;
            let items = this.checked_items.filter(item => item.roi_current !== 0); // Filter out items with ROI 0

            if (items.length <= 0) {
                this.bulk_adjust_loading = false;
                return;
            }

            items.forEach(item => {
                item.bid_adjust = item.final_uv / this.roi_adjust;
                if (item.br) {
                    item.bid_adjust = item.bid_adjust * this.brl_currency;
                }
                item.bid_adjust = Math.round(item.bid_adjust * 10000) / 10000; // Round 4 digits after decimal point
                console.log("New bid: " + item.bid_adjust);

                if (parseFloat(item.bid_adjust) === parseFloat(item.bid)) {
                    this.notice("You entered the same value, No changes were made");
                    return;
                } else if (parseFloat(item.bid_adjust) === 0) {
                    this.notice("Please enter value greater then 0");
                    return;
                } else if (item.source !== 'facebook' && parseInt(item.br) === 0 && parseFloat(item.bid_adjust) > 0.25) {
                    this.notice("Please enter value less then 0.25$");
                    return;
                } else if (item.source !== 'facebook' && parseInt(item.br) === 1 && parseFloat(item.bid_adjust / this.brl_currency) > 0.25) {
                    this.notice("Please enter value less then 0.25$");
                    return;
                }
                item.status = 'IN_PROCESS';
                item.login_time = this.$store.getters.getUser.loginTime;
            });

            const chunk = (arr, size) =>
                Array.from({length: Math.ceil(arr.length / size)}, (v, i) =>
                    arr.slice(i * size, i * size + size)
                );

            let chunked_items = chunk(items, 5);
            chunked_items.forEach(chunk => {
                this.$http.post('/api/website/campaigns/bulk', chunk).then(res => {
                    if (res.body === "True") {
                        this.bulk_adjust_loading = false;
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                    this.checked_items = [];
                }).catch(e => {
                    this.bulk_adjust_loading = false;
                    if (e.status === 401) {
                        this.$emit('logout');
                    } else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
            });
            const that = this;
            setTimeout(function () {
                items.forEach(item => {
                    that.refresh_campaign_status(item);
                });
            }, 10000);
        },
        selectAllRoiChange(fast) {
            this.roi_apply = true;
            const that = this;
            setTimeout(function () {
                for (let i of that.checked_items) {
                    i.roi_adjust = that.roi_adjust;
                }
                that.roi_apply = false;
            }, fast ? 0 : 500);
        },
    },
    computed: {
        selectItem: {
            get: function () {
                return this.checked_items;
            },
            set: function (items) {
                this.checked_items = items;
            }
        },
        filtered_items: {
            get: function() {
                let items = this.items;

                if (this.filter) {
                    const fix = v => {
                        if (v instanceof Object) {
                            return ['name', 'campaign_id', 'device', 'source'].map(k => fix(v[k])).join(' ');
                        }
                        return String(v);
                    };

                    if (this.filter && this.filter.length > 0) {
                        const regex = new RegExp('.*' + this.filter + '.*');
                        items = items.filter(item => regex.test(fix(item)));
                    }
                }

                return items;
            }
        },
        selectAllItems: {
            get: function () {
                const items = this.filtered_items;
                return items ? this.checked_items.length === items.length : false;
            },
            set: function (value) {
                let selected = [];

                if (value) {
                    const items = this.filtered_items;

                    items.forEach(function (item) {
                        selected.push(item);
                    });
                }

                this.checked_items = selected;
            }
        },
    }
}