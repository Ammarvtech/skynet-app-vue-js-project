export default {
    data() {
        return {
            toggle_auto_providers: ['taboola', 'gemini', 'zemanta'],
        }
    },
    methods: {
            change_automation(item) {
                let action = parseInt(item.automation_active) === 1 ? 'Activating' : 'Deactivating';
                let type = parseInt(item.automation_active) === 1 ? 'success' : 'warning';
                let count = parseInt(item.automation_active) === 1 ? 1 : -1;
                let is_active = parseInt(item.automation_active) === 1 ? '1' : '0';

                this.$message({
                    message: action + ' Automation rules for campaign ' + item.campaign_id,
                    type: type
                });
                this.automation_campaigns += this.automation_campaigns === 0 && count === -1 ? 0 : count;

                let params = {
                    'is_active': is_active,
                    'target_value': item.campaign_id,
                    'login_time': this.$store.getters.getUser.loginTime,
                };

                this.$http.get('/api/website/campaign/automation_toggle', {params: params}).then(() => {
                }).catch(e => {
                    if(e.status === 401) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice("Error has occurred, Please try again");
                    }
                });
            },
    }
}