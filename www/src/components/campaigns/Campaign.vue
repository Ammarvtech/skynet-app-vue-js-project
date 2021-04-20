<template>
    <div id="campaign">
        <div class="row">
            <div class="col-xs-3">
                <span>Select Action</span>
                <el-radio-group v-model="action_radio">
                    <el-radio-button label="New Campaign"></el-radio-button>
                    <el-radio-button label="Clone Existing"></el-radio-button>
                </el-radio-group>
            </div>

            <div :class="[action_radio === 'Clone Existing' ? 'show' : 'hide', 'col-xs-3']">
                <span>Campaign</span>
                <el-select v-model="form.campaigns" placeholder="Select existing campaign">
                    <el-option label="1111" value="1111"></el-option>
                    <el-option label="2222" value="2222"></el-option>
                    <el-option label="3333" value="3333"></el-option>
                </el-select>
            </div>
        </div>

        <hr class="style-one">

        <el-form ref="form" :model="form" :class="[action_radio === 'New Campaign' || show_form ? 'show' : 'hide']" label-width="120px">

            <el-form-item label="Provider">
                <el-select v-model="form.provider" placeholder="please select provider">
                    <el-option label="Revcontent" value="revcontent"></el-option>
                    <el-option label="Taboola" value="taboola"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="Accounts">
                <el-select v-model="form.accounts" placeholder="Select account">
                    <el-option label="account 1" value="account 1"></el-option>
                    <el-option label="account 2" value="account 2"></el-option>
                    <el-option label="account 3" value="account 2"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="Campaign name">
                <el-input v-model="form.name"></el-input>
            </el-form-item>

            <!--only taboola-->
            <div :class="[form.provider === 'taboola' ? 'show' : 'hide']">
                <el-form-item label="Branding text">
                    <el-input v-model="form.branding"></el-input>
                </el-form-item>
            </div>
            <!--end-->

            <el-form-item label="Start Date">
                <el-radio-group v-model="radio_start">
                    <el-radio-button label="Immediately"></el-radio-button>
                    <el-radio-button label="Specific date"></el-radio-button>
                </el-radio-group>
            </el-form-item>

            <div :class="[radio_start === 'Specific date' ? 'show' : 'hide']">
                <el-form-item>
                    <el-col :span="11">
                        <el-date-picker type="date" placeholder="Pick a date" v-model="form.start_date" style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>
            </div>

            <el-form-item label="End Date">
                <el-radio-group v-model="radio_end">
                    <el-radio-button label="Never ends"></el-radio-button>
                    <el-radio-button label="Specific date"></el-radio-button>
                </el-radio-group>
            </el-form-item>

            <div :class="[radio_end === 'Specific date' ? 'show' : 'hide']">
                <el-form-item>
                    <el-col :span="11">
                        <el-date-picker type="date" placeholder="Pick a date" v-model="form.end_date" style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>
            </div>

            <el-form-item label="Country targeting">
                <el-radio-group v-model="radio_country">
                    <el-radio-button label="All countries"></el-radio-button>
                    <el-radio-button label="Include"></el-radio-button>
                    <el-radio-button label="Exclude"></el-radio-button>
                </el-radio-group>
            </el-form-item>

            <div :class="[radio_country === 'Include' || radio_country === 'Exclude' ? 'show' : 'hide']">
                <el-form-item label="">
                    <el-select v-model="form.countries" multiple placeholder="Select">
                        <el-option
                                v-for="item in countries_options"
                                :label="item.label"
                                :value="item.value"
                                :key="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
            </div>

            <el-form-item label="Device targeting">
                <el-radio-group v-model="radio_device">
                    <el-radio-button label="All Devices"></el-radio-button>
                    <el-radio-button label="Mobile"></el-radio-button>
                    <el-radio-button label="Tablet"></el-radio-button>
                    <el-radio-button label="Desktop"></el-radio-button>
                </el-radio-group>

                <el-radio-group v-model="radio_operating">
                    <el-radio-button label="All Operating Systems" :disabled="radio_device ==='Desktop'"></el-radio-button>
                    <el-radio-button label="Android" :disabled="radio_device ==='Desktop'"></el-radio-button>
                    <el-radio-button label="IOS" :disabled="radio_device ==='Desktop'"></el-radio-button>
                    <el-radio-button label="Windows" :disabled="radio_device ==='Desktop'"></el-radio-button>
                </el-radio-group>
            </el-form-item>


            <el-form-item label="Bid Amount">
                <el-input-number v-model="form.bid" @change="" :min="1" :max="1000000"></el-input-number>
            </el-form-item>


            <el-form-item label="Budget Amount">
                <el-radio-group v-model="radio_budget">
                    <el-radio-button label="Unlimited"></el-radio-button>
                    <el-radio-button label="Daily"></el-radio-button>
                </el-radio-group>

                <el-input-number v-model="form.budget" @change="" :min="1" :max="10000000"></el-input-number>
            </el-form-item>


            <el-form-item label="Tracking code">
                <el-input v-model="form.tracking"></el-input>
            </el-form-item>


            <!--revcontent-->
            <div :class="[form.provider === 'revcontent' ? 'show' : 'hide']">
                <el-form-item label="Language Targeting">
                    <el-select v-model="languages" placeholder="Default: All Languages">
                        <el-option label="English" value="account 1"></el-option>
                        <el-option label="Spanish" value="account 2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Exclude Low Volume Widgets">
                    <el-radio-group v-model="widgets_vol">
                        <el-radio-button label="Yes"></el-radio-button>
                        <el-radio-button label="No"></el-radio-button>
                    </el-radio-group>
                </el-form-item>
            </div>
            <!--revcontent end-->

            <!--taboola-->
            <div :class="[form.provider === 'taboola' ? 'show' : 'hide']">
                <el-form-item label="Daily Ad Delivery:">
                <el-radio-group v-model="radio_delivery">
                    <el-radio-button label="Balanced"></el-radio-button>
                    <el-radio-button label="Accelerated"></el-radio-button>
                    <el-radio-button label="Strict"></el-radio-button>
                </el-radio-group>
            </el-form-item>
            </div>
            <!--taboola end-->

            <el-button @click="submit" type="primary">Submit</el-button>
        </el-form>

    </div>
</template>

<script>
    export default {
        name: 'campaign',
        data() {
            return {
                form: {
                    name: '',
                    provider: '',
                    campaigns: ['1111','2222','3333','4444'],
                    start_date: '',
                    end_date: '',
                    type: [],
                    branding: '',
                    countries: [],
                    bid: '',
                    budget:'',
                    tracking: '',
                },
                countries_options: [{
                    value: 'Option1',
                    label: 'US'
                }, {
                    value: 'Option2',
                    label: 'UK'
                }, {
                    value: 'Option3',
                    label: 'DE'
                }, {
                    value: 'Option4',
                    label: 'FR'
                }, {
                    value: 'Option5',
                    label: 'IT'
                }],
                accounts: ['1','2','3'],
                action_radio: '',
                radio_start: '',
                radio_end: '',
                radio_country: '',
                radio_device: '',
                radio_operating: '',
                radio_budget: '',
                radio_delivery: '',
                languages: '',
                widgets_vol: '',
                show_form: false
            }
        },
        methods: {
            submit() {
                console.log('submit!');
            },
        }
    }
</script>

<style>
    .show {
        display: block;
    }

    .hide {
        display: none;
    }
</style>
