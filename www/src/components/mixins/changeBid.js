export default {
    data() {
        return {
            bid: '',
            taboola_bid: '',
            gemini_bid: '',
            facebook_bid: '',
            zemanta_bid: '',
            outbrain_bid: '',
            timer: undefined,
        }
    },
    methods: {
        edit_bid(item) {
            let brl_currency = this.$store.getters.getCurrency;
            if (item.source === 'gemini') {
                this.bid = this.gemini_bid;
            } else if (item.source === 'facebook') {
                this.bid = this.facebook_bid;
            } else if (item.source === 'zemanta') {
                this.bid = this.zemanta_bid;
            } else if (item.source === 'outbrain') {
                this.bid = this.outbrain_bid;
            } else {
                this.bid = this.taboola_bid;
            }

            if (!this.bid) {
                return
            }
            if (parseFloat(this.bid) === parseFloat(item.bid)) {
                this.notice("You entered the same value, No changes were made");
                return;
            } else if (parseFloat(this.bid) === 0) {
                this.notice("Please enter value greater then 0");
                return;
            }else if (item.source !== 'facebook' && parseInt(item.br) === 0 && parseFloat(this.bid) > 0.25 ) {
                this.notice("Please enter value less then 0.25$");
                return;
            }else if (item.source !== 'facebook' && parseInt(item.br) === 1 && parseFloat(this.bid / brl_currency) > 0.25) {
                this.notice("Please enter value less then 0.25$");
                return;
            }

            let threshold = item.final_uv / parseFloat(this.bid);
            if (item.br) {
                threshold = item.final_uv / (parseFloat(this.bid) / this.$store.getters.getCurrency);
            }
            if (item.source !== 'facebook' && item.cost >= 5 && threshold < 0.5) {
                this.$confirm('High bid alert! The current ROI is below 50%. Continue?', 'Alert',
                    {
                        confirmButtonText: 'Yes',
                        cancelButtonText: 'No',
                        type: 'warning'
                    }).then(() => {
                        this.change_bid(item, this.bid);
                }).catch(() => {
                    this.notice('Bid was not changed.');
                });
            } else {
                this.change_bid(item, this.bid);
            }
        },
        edit_bid_key_press(e, item) {
            if (e.keyCode === 13) {
                this.edit_bid(item);
            }
        },
        change_bid(item, new_bid) {
            item.pop_visible = false;
            item.status = 'IN_PROCESS';
            item.new_bid = new_bid;
            item.new_bid = Math.round(item.new_bid * 10000) / 10000; // Round 4 digits after decimal point
            item.login_time =  this.$store.getters.getUser.loginTime;

            this.$http.post("/api/website/" + item.source + "/campaign/bid_update", item).then(res => {
                if (res.body === "True") {
                    this.$message({message: 'Request Pending...', center: true, type: 'success'});
                } else {
                    this.notice("Error has occurred, Please try again");
                }
            }).catch(e => {
                if(e.status === 401) {
                    this.$emit('logout');
                }
                else {
                    this.notice("Error has occurred, Please try again");
                }
            });

            this.refresh_campaign_status(item);
        },
        refresh_campaign_status(item) {
            this.$el.click();
            if (!this.timer) {
                const that = this;
                this.timer = new this.Timer(function () {
                    that.check_status_campaign(item);
                }, 10000);
            } else {
                this.timer.add(1000);
            }
        },
    }
}