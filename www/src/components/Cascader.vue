<template>
    <div id="cascader">
        <el-row :gutter="20" @mouseover.native="active=true" @mouseout.native="active=false">
            <el-col style="padding-top: 5px;padding-right: 0;width: 140px">
                <div class="grid-content">
                    <el-cascader size="small" placeholder="Add filter" expand-trigger="hover" :options="options" v-model="selectedOptions" :change-on-select="false" @change="handleChange" filterable></el-cascader>
                </div>
            </el-col>
            <el-col v-for="(chip, index) in chips_arry" :key="index" :span="1"
                    style="width: max-content;padding-left: 0;padding-right: 0;">
                <div>
                    <v-chip v-model="chips_data[index]" @input="remove(chip, index)" close>{{chip.label}}</v-chip>
                </div>
            </el-col>
            <el-col :span="1">
                <v-fade-transition>
                    <v-chip class="close_chip" @click="clear_all" v-show="chips_arry.length > 0 && active"
                            style="padding-right: 9px">
                        <v-avatar class="blue darken-1">{{chips_arry.length}}</v-avatar>Clear filters
                    </v-chip>
                </v-fade-transition>
            </el-col>
        </el-row>

        <v-layout row justify-center>
            <v-dialog v-model="dialog" max-width="450px">
                <v-card>
                    <v-card-actions>
                        <v-text-field ref="form" v-model="input" v-bind:label="$t()" clearable></v-text-field>
                        <v-spacer v-if="chip_label[1] == 'between'" style="padding-left: 27px;padding-right: 27px;">
                            and
                        </v-spacer>
                        <v-text-field v-if="chip_label[1] == 'between'" ref="between_form" v-model="between_input"
                                      v-bind:label="$t()" @keypress="onlyNumber" clearable></v-text-field>
                        <v-btn color="blue darken-1" outline @click="apply()"
                               style="margin-left: 20px;border-radius: 5px;">Cancel
                        </v-btn>
                        <v-btn color="blue darken-1" outline @click="apply(true)" :disabled="verify()"
                               style="border-radius: 5px;">Save
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-layout>

        <v-layout row justify-center>
            <v-dialog v-model="date_dialog" width="500">
                <v-card>
                    <v-card-actions>
                        <el-date-picker
                                v-model="date_range"
                                type="daterange"
                                range-separator="To"
                                start-placeholder="Start date"
                                end-placeholder="End date"
                                style="width: 100% !important;padding-right: 0 !important;font-weight: lighter !important;font-size: larger;border: 1px solid #2196f3 !important;"
                                @change="date_filter"
                                :clearable="false"
                                :picker-options="pickerOptions"
                        >
                        </el-date-picker>
                        <!--<v-btn color="primary" text @click="date_dialog = false">I accept</v-btn>-->
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-layout>

    </div>
</template>

<script>
    import moment from 'moment-timezone';

    export default {
        name: "Cascader",
        mounted() {
            let self = this;
            window.addEventListener('keyup', function (event) {
                if (event.keyCode === 13) {
                    self.apply(true)
                }
            });
            this.initializeOptions();
        },
        data() {
            let children_options = [{value: 'less', label: 'Less than'}, {
                value: 'between',
                label: 'Between'
            }, {value: 'greater', label: 'Greater than'}];
            let children_options2 = [{value: 'enabled', label: 'Enabled'}, {value: 'disabled', label: 'Disabled'}];
            return {
                dialog: false,
                date_dialog: false,
                active: false,
                label: '',
                input: '',
                between_input: '',
                chip_label: [],
                chips_data: [],
                chips_arry: [],
                labels: [],
                selectedOptions: [],
                date_range: [moment(), moment()],
                options: [
                    {value: 'clicks', label: 'Clicks', children: children_options},
                    {value: 'ctr', label: 'CTR', children: children_options},
                    {value: 'revenue', label: 'Revenue', children: children_options},
                    {value: 'cost', label: 'Cost', children: children_options},
                    {value: 'budget', label: 'Budget', children: children_options},
                    {value: 'profit', label: 'Profit', children: children_options},
                    {value: 'final_uv', label: 'UV', children: children_options},
                    {value: 'pages_session', label: 'P/S', children: children_options},
                    {value: 'avg_bid', label: 'Avg Bid', children: children_options},
                    {value: 'roi_final', label: 'ROI', children: children_options},
                    {value: 'profit_diff', label: 'Profit Change', children: children_options},
                    {value: 'automation', label: 'Automation Rule', children: children_options2},
                    {value: 'creation_date', label: 'Creation Date'},
                    {value: 'losing_campaigns', label: 'Losing'},
                    {value: 'landing_page', label: 'Landing Page'},
                    {value: 'exceeded_budget', label: 'Exceeded Budget'},
                    {value: 'bidder', label: 'Bidder '},

                ],
                medium_cascader_options_to_remove: ['automation','bidder', 'exceeded_budget', 'landing_page', 'profit_diff', 'creation_date', 'avg_bid'],
                chips_conversion: {
                    'revenue': 'Revenue',
                    'clicks': 'Clicks',
                    'cost': 'Cost',
                    'budget': 'Budget',
                    'profit': 'Profit',
                    'ctr': 'CTR',
                    'roi_final': 'ROI',
                    'pages_session': 'Pages session',
                    'final_uv': 'UV',
                    'avg_bid': 'Avg bid',
                    'profit_diff': 'Profit Changes',
                    'losing_campaigns': 'Losing campaigns',
                    'landing_page': 'Landing page',
                    'exceeded_budget': 'Exceeded budget',
                    'creation_date': 'Creation Date',
                    'automation': 'Automation Rule',
                    'bidder': 'Bidder',
                },
                pickerOptions: {
                    disabledDate(time) {
                        return time.getTime() > Date.now();
                    }
                },
            }
        },
        methods: {
            initializeOptions() {
                let options = this.options;
                for (let i = 0; i < options.length; i++) {
                    if ((options[i].value == 'losing_campaigns' || options[i].value == 'ctr') && this.$parent.$options.name == 'campaign_data_rt') {
                        options.splice(i, 1);
                        i--;
                    }
                    if (this.$parent.$options.name == 'medium_key' && this.medium_cascader_options_to_remove.includes(options[i].value)) {
                        options.splice(i, 1);
                        i--;
                    }
                }
            },
            handleChange(value) {
                this.init();
                this.chip_label = value;
                this.label = this.chip_label[0] = this.chips_conversion[value[0]];

                let skip = ['Losing campaigns', 'Exceeded budget', 'Automation Rule', 'Bidder'];

                if (value[0] == 'Creation Date') {
                    this.date_dialog = true;
                }
                else if (!skip.includes(value[0])) {
                    this.dialog = true;
                    this.selectedOptions = [];
                    setTimeout(x => {
                        this.$nextTick(() => this.$refs.form.focus())
                    }, 300);

                } else {
                    this.instant_filter()
                }
            },
            date_filter() {
                let label = this.build_text();
                let params = {
                    'label': label[0],
                    'type': label[1],
                    'field': label[2],
                    'value': [moment(this.date_range[0]).format("YYYY-MM-DD"), moment(this.date_range[1]).format("YYYY-MM-DD")]
                };
                this.chips_arry.push(params);
                this.labels.push(label[1]);
                this.$parent.$options.methods.cascaderFilter(params, this.$parent);
                this.date_dialog = false;
                this.date_range = [moment(), moment()];
            },
            apply(save) {
                this.dialog = false;
                if (!this.input) return;

                let lp = this.chip_label[0] == 'Landing page';
                if (lp) {
                    this.instant_filter()
                }

                else if (!lp && save) {
                    let label = this.build_text();
                    let params = {
                        'type': this.chip_label[1],
                        'field': Object.keys(this.chips_conversion).find(key => this.chips_conversion[key] === this.chip_label[0]),
                        'between': this.chip_label[0] == 'ROI' ? this.between_input / 100 : this.between_input,
                        'amount': this.chip_label[0] == 'ROI' ? this.input / 100 : this.input,
                        'label': label
                    };
                    this.chips_arry.push(params);
                    this.$parent.$options.methods.cascaderFilter(params, this.$parent);
                    this.input = '';
                    this.between_input = '';
                }
            },
            build_text(losing_notification) {
                if (this.chip_label[0] == 'Losing campaigns' || losing_notification) {
                    return ['Losing campaigns (3 days in a row)', 'losing', 'alert']
                } else if (this.chip_label[0] == 'Landing page') {
                    return ['Landing page like: ' + this.input, 'landing', 'url']
                } else if (this.chip_label[0] == 'Exceeded budget') {
                    return ['Exceeded budget campaigns' + this.input, 'exceeded', 'exhausted_status']
                } else if (this.chip_label[0] == 'Creation Date') {
                    return ['Creation Date: ' + moment(this.date_range[0]).format("YYYY-MM-DD") + ' to ' + moment(this.date_range[1]).format("YYYY-MM-DD"), 'creation', 'creation_date']
                } else if (this.chip_label[0] == 'Automation Rule') {
                    return ['Automation rules campaigns',this.chip_label[1], 'automation_active']
                } else if (this.chip_label[0] == 'Bidder') {
                    return ['Campaigns with auto bidder', 'bidder', 'bidders']
                }

                let precent = this.chip_label[0] == 'roi' ? '%' : '';
                if (this.chip_label[1] == 'greater' || this.chip_label[1] == 'less') {
                    return this.chip_label[0] + (' is ' + this.chip_label[1] + ' than ') + this.input + precent;
                } else if (this.chip_label[1] == 'equals') {
                    return this.chip_label[0] + ' equals to ' + this.input + precent;
                } else {
                    return this.chip_label[0] + ' between ' + this.input + precent + ' and ' + this.between_input + precent;
                }
            },
            instant_filter(losing_notification) {
                let label = this.build_text(losing_notification);
                if (this.labels.indexOf(label[1]) > -1) {
                    return;
                }
                let params = {
                    'label': label[0],
                    'type': label[1],
                    'field': label[2],
                    'value': this.input
                };
                this.chips_arry.push(params);
                this.labels.push(label[1]);
                this.$parent.$options.methods.cascaderFilter(params, this.$parent);
                this.input = '';
                this.between_input = '';
            },
            init(data) {
                if (data) {
                    for (let i of this.options) {
                        i.children = data;
                    }
                }
            },
            verify() {
                if (this.chip_label[1] != 'between') {
                    return !this.input;
                } else {
                    return !this.input || !this.between_input;
                }
            },
            remove(item) {
                this.chips_arry.splice(this.chips_arry.indexOf(item), 1);
                this.chips_arry = [...this.chips_arry];
                this.labels.splice(this.labels.indexOf(item), 1);
                this.$parent.$options.methods.cascaderFilter(undefined, this.$parent, item, undefined, this.chips_arry);
            },
            reapply() {
                if (this.chips_arry.length > 0) {
                    this.$parent.$options.methods.cascaderFilter(undefined, this.$parent, undefined, undefined, this.chips_arry);
                }
            },
            clear_all() {
                this.chips_arry = [];
                this.labels = [];
                this.$parent.$options.methods.cascaderFilter(undefined, this.$parent, undefined, true);
            },
            onlyNumber($event) {
                let keyCode = ($event.keyCode ? $event.keyCode : $event.which);
                if ((keyCode < 48 || keyCode > 57) && keyCode !== 46) { // 46 is dot
                    $event.preventDefault();
                }
            },
            $t() {
                return this.label.toUpperCase();
            },
        }
        ,
    }
</script>

<style scoped>
    /deep/ .el-input__inner {
        width: 130px !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        /*letter-spacing: 1px !important;*/
        text-align: center !important;
        border: 2px solid #e2d7d7 !important;
        color: transparent;
        outline: none;
    }

    /deep/ .el-input__suffix {
        display: none;
    }

    /deep/ .el-input__inner {
        padding-right: 20px !important;
    }

    /deep/ .el-cascader-menu__item--extensible:after {
        display: none;
    }

    /deep/ .theme--light.v-chip {
        background: #F6F6F7 !important;
        height: 32px;
    }

    /deep/ .v-chip .v-chip__content {
        white-space: pre !important;
        color: #848183;
        cursor: pointer;
        line-height: 1px;
        padding: 0 4px 0 0;
    }

    /deep/ .v-chip--removable {
        padding: 0 2px 0 13px !important;
        display: block !important;
    }

    /deep/ .v-chip__close {
        padding-left: 5px;
    }

    /deep/ .v-input__control {
        padding-top: 5px;
    }

    /deep/ .v-avatar {
        color: white !important;
        height: 29px !important;
    }

    /deep/ .close_chip {
        height: 29px !important;
    }

    /deep/ .v-card__text {
        height: 80px;
    }

</style>

<style>
    .el-cascader-menu {
        min-height: 100px;
        height: auto;
        overflow: auto;
    }

    .el-message-box__header {
        display: none !important;
    }

    .el-message-box__content {
        height: 70px;
    }
</style>