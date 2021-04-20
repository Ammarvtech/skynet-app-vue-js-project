<template>
    <div class="switch">
        <div id="on" @click="switchCampaign(item)" :class="{active: isSwitched(item)}">
            <i class="el-icon-check "></i><i
                v-bind:class="this.loading ? '' : 'wait'" class="el-icon-loading"></i></div>
        <div id="off" @click="switchCampaign(item)" :class="{active: !isSwitched(item)}"><i class="el-icon-close"></i><i
                v-bind:class="this.loading ? '' : 'wait'" class="el-icon-loading"></i>
        </div>
    </div>
</template>

<script>
    export default{
        props: ["item"],
        data(){
            return {
                loading: false
            }
        },
        methods: {
            isSwitched(item) {
                return item.enabled === 'active'
            },
            switchCampaign(campaign){
                campaign.enabled === 'inactive' ? campaign.enabled = 'active' : campaign.enabled = 'inactive';
                this.loading = true;
                let endpoint = `/api/campaignManager/switch`;
                this.$http.post(endpoint, {
                    "campaign_id": campaign.campaign_id,
                    "enabled": campaign.enabled
                }).then(res => {
                    if (res.body) {
                        this.$message({
                            type: 'success',
                            message: `Campaign Set To ${campaign.enabled} Successfully`
                        });
                    } else {
                        this.$alert('Sorry, Error has occurred while trying stop the campaign', ' ', {
                            confirmButtonText: 'OK',
                            type: 'warning'
                        });
                    }
                    this.loading = false;
                });
//                let index = this.items.findIndex(function (element) {
//                    return element.campaign_id === campaign_id && element.device === device;
//                });
//                this.items[index].status = "disabled";
            }
        }
    }
</script>

<style scoped>
    #on, #off {
        width: 40px;
        height: 20px;
        display: inline-block;
        margin: 5px 3px;
        top: 2px;
        position: relative;
        color: #FFF;
        -webkit-box-sizing: content-box;
        -moz-box-sizing: content-box;
        box-sizing: content-box;
        cursor: pointer;
        text-align: center;
        border: 1px solid #c4c4c4;
        border-radius: 2px;
    }

    #on.active {
        background-color: #13ce66;
        font-weight: 600;
    }

    #off.active {
        background-color: #ff4949;
    }

    div.switch {
        display: inline;
    }

    div.switch div:not(.active) {
        display: none !important;
    }

    i {
        font-size: 12px;
        vertical-align: baselin
    }

    .wait {
        display: none;
    }
</style>