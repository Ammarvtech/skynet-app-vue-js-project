<template>
    <div id="op-box">
        <el-row type="flex" justify="center">
            <el-col>
                <div class="box-body">
                    <p>The Widget Optimizer allows you to
                        <el-select v-model="opt_type" v-on:change="setType" placeholder="Select">
                            <el-option label="Target Only" value="target"></el-option>
                            <el-option label="Blacklist" value="blacklist"></el-option>
                        </el-select>
                        specific widget ID's from your targets
                    </p>
                    <p>Very low volume widgets cannot be included/excluded using this feature.
                        In order to restrict widget ids that do not meet a specified volume threshold,
                        advertisers must select the "Exclude Low Volume Widgets"
                        checkbox within boost settings.
                    </p>
                </div>

                <div class="add_widget">
                    <el-input placeholder="Enter Widget ID #'s (Ex. 5 or 5,6,7)" v-model="input"></el-input>
                    <el-button type="success" @click="add_ids()">Add Widgets</el-button>
                </div>

                <el-button type="danger" class="remove_all" @click="remove_all()">Remove All</el-button>

                <div id="selected_container">
                    <span class="loading" v-show="loading"><i class="el-icon-loading"></i>submitting...</span>
                    <h2 v-if="!_exs">No widgets found</h2>
                    <ul id="widgets_list">
                        <li v-for="id in widget_ids"><i class="el-icon-close" @click="remove_id(id)"></i> Widget ID
                            #{{id}}
                        </li>
                    </ul>
                </div>

            </el-col>
        </el-row>
    </div>
</template>

<script>

    export default {
        data() {
            return {
                campaign_id: this.$parent.campaign_id,
                widget_ids: this.$parent.widget_ids,
                opt_type: this.$parent.action,
                widgets_length: '',
                input: '',
                loading: false
            }
        },
        methods: {
            add_ids() {
                let new_ids = this.input.split(',').map(Number);
                this.widget_ids.push.apply(this.widget_ids, new_ids);
                this.widget_ids = Object.keys(this.widget_ids.reduce((p, c) => (p[c] = true, p), {})).map(Number);
                this.input = '';
                this.$http.post('/api/campaignManager/wio', {
                    campaign_id: this.campaign_id,
                    type: this.opt_type,
                    widget_ids: new_ids,
                    action: this.api_action
                }).then(res => {
                    console.log(res)
                }, response => {
                    // error callback
                });
            },
            remove_id(widget_id) {
                this.loading = true;
                this.$http.post('/api/campaignManager/wio/delete', {
                    campaign_id: this.campaign_id,
                    single: true,
                    type: this.opt_type,
                    widget_ids: widget_id,
                    action: this.api_action
                }).then(res => {
                    this.loading = false;
                    let idx = this.widget_ids.indexOf(widget_id);
                    this.widget_ids.splice(idx, 1);
                }, response => {
                    this.loading = false;
                    // error callback
                });
            },
            remove_all() {
                this.loading = true;
                this.$http.post('/api/campaignManager/wio/delete', {
                    campaign_id: this.campaign_id,
                    single: false,
                    type: this.opt_type,
                    widget_ids: this.widget_ids,
                    action: this.api_action
                }).then(res => {
                    console.log(res.body);
                    this.loading = false;

                }, response => {
                    this.loading = false;

                    // error callback
                });
                this.widget_ids = [];
            },
            setType() {
                this.$http.post('/api/campaignManager/wio/type', {
                    campaign_id: this.campaign_id,
                    type: this.opt_type,
                    widget_ids: this.widget_ids,
                    action: this.api_action
                }).then(res => {
                    console.log(res.body);
                }, response => {
                    // error callback
                });
            }
        },
        computed: {
            _exs() {
                this.widget_length = this.widget_ids.length;
                return this.widget_ids.length
            },
            api_action() {
                let api_action = this.campaign_id.includes("TBD") ? "create" : "update"
                return api_action
            },
        }
    }
</script>

<style scoped>


    div.add_widget {
        display: flex;
        padding: 10px 0;
    }

    .remove_all {
        float: right;
    }

    #selected_container {
        background: #dddddd;
        top: 45px;
        margin: 0 0 35px 0;
        position: relative;
        -webkit-border-radius: 3px;
        -moz-border-radius: 3px;
        border-radius: 3px;
        padding: 10px;
    }

    .campaign_num {
        position: absolute;
        left: 0px;
        top: -20px;
        font-weight: 700;
    }

    .el-icon-delete:hover {
        cursor: pointer;
    }

    #widgets_list li {
        display: -webkit-inline-box;
        display: inline-block;
        min-width: 25%;
        padding: 4px 5px;
    }

    i.el-icon-close {
        font-size: 10px;
    }

    i.el-icon-close:hover {
        cursor: pointer;
        font-weight: bold;
    }
</style>
