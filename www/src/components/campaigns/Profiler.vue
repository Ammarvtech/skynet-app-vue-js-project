<template>

    <div id="profiler">
        <h1>Duplicate Profiler</h1>
        <div id="overlay" v-show="showOverlay"></div>
        <div class="row" v-show="!loading">

            <!--TABS-->
            <div class="row menu-tabs">
                <el-tabs tab-position="top" v-model="tab">
                    <el-tab-pane label="Profiler">

                        <!--ADD PROFILE POPUP-->
                        <el-popover trigger="click" placement="top" ref="popover2" v-on:hide="closePopup()"
                                    v-model="visible1">
                            <el-form label-position="left" label-width="100px" :model="form">
                                <el-form-item label="Name">
                                    <el-input v-model="form.name"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="primary" size="medium" @click="createProfile()">Create Profile
                                    </el-button>
                                </el-form-item>
                            </el-form>
                        </el-popover>
                        <el-button type="primary" size="medium" v-popover:popover2 @click="showOverlay = true">
                            Add Profile
                        </el-button>
                        <!--/ADD PROFILE POPUP-->

                    </el-tab-pane>

                    <el-tab-pane label="Widget List">

                        <!--ADD WIDGET LIST POPUP-->
                        <el-popover width="500" trigger="click" placement="top" ref="popover3" v-on:hide="closeEdit()"
                                    v-model="visible3">
                            <el-form label-position="left" label-width="100px" :model="widgetsForm">
                                <el-form-item label="Name">
                                    <el-input v-model="widgetsForm.name"></el-input>
                                </el-form-item>
                                <el-form-item label="Widget List">
                                    <el-input type="textarea" v-model="widgetsForm.widget_list"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="primary" size="medium" @click="createList()" :disabled="validList">
                                        Create List
                                    </el-button>
                                    <el-button @click="closeEdit()">Cancel</el-button>
                                </el-form-item>
                            </el-form>
                        </el-popover>
                        <el-button type="primary" size="medium" v-popover:popover3 @click="showOverlay = true">
                            Add Widget List
                        </el-button>
                        <!--/ADD WIDGET LIST POPUP-->

                    </el-tab-pane>
                </el-tabs>
            </div>
            <!--/TABS-->

            <!--PROFILES TABLE-->
            <el-table :data="profiles" v-show="tab == 0">
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <table class="table table-bordered table-hover">
                            <thead class="thead-default">
                            <tr v-if="hasSet(profiles[props.$index].profile_id)">
                                <th>Country</th>
                                <th>Bid</th>
                                <th>Budget</th>
                                <th>Widget List</th>
                                <th>Widget Type</th>
                                <th>Device</th>
                                <th>Description</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="set in sets" v-if="set.profile_id == profiles[props.$index].profile_id">
                                <td>{{adjCountry(set.country)}}</td>
                                <td>{{set.bid}}</td>
                                <td>{{set.budget}}</td>
                                <td>{{listName(set.widget_list_id)}}</td>
                                <td>{{set.widget_type}}</td>
                                <td>{{adjDevice(set.device)}}</td>
                                <td>{{set.desc}}</td>
                                <td>
                                    <el-button size="small" type="primary" icon="el-icon-delete"
                                               @click="deleteSet(set.id)">
                                    </el-button>
                                    <el-button size="small" type="primary" icon="el-icon-edit"
                                               @click="editSet(set)"></el-button>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div class="last-field"><a @click="addSet(profiles[props.$index].profile_id)">
                            + Add another set</a>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="Created By" prop="username"></el-table-column>
                <el-table-column label="Name" prop="name"></el-table-column>
                <el-table-column label="Creation Date" prop="creation_date"></el-table-column>
                <el-table-column label="Profile ID">
                    <template slot-scope="props">
                        <el-button size="medium" type="primary" icon="el-icon-delete"
                                   @click="deleteProfile(profiles[props.$index].profile_id)"></el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--/PROFILES TABLE-->


            <!--WIDGETS TABLE-->
            <el-table :data="wList" v-show="tab == 1">
                <el-table-column label="Name" prop="name"></el-table-column>
                <el-table-column label="List" prop="widget_list" :formatter="listFormatter"></el-table-column>
                <el-table-column>
                    <template slot-scope="scope">
                        <el-button type="primary" size="small" icon="el-icon-edit"
                                   @click="editList(scope.row)"></el-button>
                        <el-button type="primary" size="small" icon="el-icon-delete"
                                   @click="deleteList(scope.row.id)"></el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--/WIDGETS TABLE-->

            <!--EDIT SET POPUP-->
            <div class="edit-form" v-show="visible2" style="width: 40vw;height: 72vh">
                <el-form label-position="center" label-width="100px" v-model="editForm" ref="editForm">
                    <el-form-item label="Countries" prop="countries">
                        <el-select v-model="editForm.country" placeholder="Select" filterable multiple>
                            <el-option
                                    v-for="country in countries"
                                    :label="country.id"
                                    :value="country.id"
                                    :key="country.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Bid*" prop="bid">
                        <el-input-number v-model="editForm.bid" :step="0.01"></el-input-number>
                    </el-form-item>
                    <el-form-item label="Budget*" prop="budget">
                        <el-input-number v-model="editForm.budget"></el-input-number>
                    </el-form-item>
                    <el-form-item label="Widget List*" prop="wlist">
                        <el-select v-model="editForm.widget_list_id" placeholder="Select" filterable>
                            <el-option
                                    v-for="list in wList"
                                    :label="list.name"
                                    :value="list.id"
                                    :key="list.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Widget Type*" prop="wtype">
                        <el-radio-group v-model="editForm.widget_type" size="small">
                            <el-radio-button label="include">Include</el-radio-button>
                            <el-radio-button label="exclude">Exclude</el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="Device">
                        <el-checkbox-group v-model="editForm.device" @change="deviceValid">
                            <el-checkbox-button label="all_devices" :disabled="_all_devices">All Devices
                            </el-checkbox-button>
                            <el-checkbox-button label="1">Desktop</el-checkbox-button>
                            <el-checkbox-button label="2">Mobile</el-checkbox-button>
                            <el-checkbox-button label="3">Tablet</el-checkbox-button>
                        </el-checkbox-group>
                        <el-checkbox-group v-model="editForm.device" v-show="_has_mobile" @change="deviceValid">
                            <el-checkbox-button label="all_os" :disabled="_all_os">
                                All Operating Systems
                            </el-checkbox-button>
                            <el-checkbox-button label="4">Android
                            </el-checkbox-button>
                            <el-checkbox-button label="5">IOS
                            </el-checkbox-button>
                            <el-checkbox-button label="6">Windows
                            </el-checkbox-button>
                        </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="Description*" prop="desc">
                        <el-input v-model="editForm.desc"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitSet('editForm')" :disabled="mandFill">Submit
                        </el-button>
                        <el-button @click="closeEdit('editForm')">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <!--/EDIT SET POPUP-->

            <!--EDIT WLIST POPUP-->
            <div class="edit-form" v-show="visible4" style="width: 40vw;">
                <h2 class="form-title">Edit Widgets List</h2>
                <el-form label-position="center" label-width="100px">
                    <el-form-item label="Name">
                        <el-input v-model="editWidgets.name"></el-input>
                    </el-form-item>
                    <el-form-item label="Widget List">
                        <el-input type="textarea" :rows="rowsHeight" v-model="editWidgets.list"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" size="medium" @click="updateList()" :disabled="validList2">
                            Update List
                        </el-button>
                        <el-button @click="closeEdit()">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <!--/EDIT WLIST POPUP-->
        <scaleloader class="centered" :loading="loading"></scaleloader>

    </div>
</template>

<script>
    import Scaleloader from '../../../node_modules/vue-spinner/src/ScaleLoader.vue'

    export default {
        components: {
            scaleloader: Scaleloader
        },
        mounted() {
            this.getData()
        },
        data() {
            return {
                tab: '',
                userId: '',
                profile: [],
                sets: [],
                form: {
                    name: ''
                },
                widgetsForm: {
                    name: '',
                    widget_list: ''
                },
                editForm: {
                    bid: '',
                    budget: '',
                    country: [],
                    desc: '',
                    device: ['all_os'],
                    id: '',
                    profile_id: '',
                    user_id: '',
                    widget_list_id: '',
                    widget_list_name: '',
                    widget_type: ''
                },
                editWidgets: {
                    list_id: '',
                    name: '',
                    list: ''
                },
                profiles: [],
                wList: [],
                iterable: [],
                countries: [],
                visible1: false,
                visible2: false,
                visible3: false,
                visible4: false,
                showOverlay: false,
                loading: false,
                ruleForm2: {},
                deviceCodes: {
                    1: "Desktop",
                    2: "Mobile",
                    3: "Tablet",
                    4: "Android",
                    5: "iOS",
                    6: "Windows",
                    "all_devices": "All Devices",
                    "all_os": "All OS",
                },
                rowsHeight: 10
            }
        },
        methods: {
            getData() {
                this.loading = true;
                this.$http.get('/api/profiler').then(res => {
                    if (res.body.sets) {
                        this.sets = res.body.sets;  // profile exist only if related set exist
                        this.profiles = res.body.profiles;
                        this.wList = res.body.w_list;
                        this.countries = res.body.countries;
                        this.userId = res.body.user_id;
                        this.loading = false;
                    }
                }, res => {
                    this.loading = false;
                });
            },
            createProfile() {
                this.showOverlay = true;
                this.$http.post('/api/profiler/profile', {
                    data: this.form
                }).then(res => {
                    let newProfile = {
                        "profile_id": res.body.last_id,
                        "creation_date": new Date().toISOString().slice(0, 10),
                        "name": this.form.name,
                        "username": this.$store.getters.getUser
                    };
                    this.profiles.push(newProfile);
                    this.$notify({
                        title: "Great!",
                        message: "Profile created successfully ",
                        type: "success"
                    });
                    this.closePopup();
                    this.showOverlay = false;
                }, res => {
                    this.$notify({
                        title: "Warning",
                        message: "Failed to create profile",
                        type: "warning"
                    });
                    this.closePopup();
                    this.showOverlay = false;
                });
            },
            createList() {
                this.$http.post('/api/profiler/list', {
                    name: this.widgetsForm.name,
                    list: this.widgetsForm.widget_list
                }).then(res => {
                    if (res.body.last_id !== null) {
                        this.widgetsForm.id = res.body.last_id;
                        this.wList.push(this.widgetsForm);
                        this.closeListPup();
                        this.$notify({
                            title: "Great!",
                            message: "List created successfully ",
                            type: "success"
                        });
                    }
                }, res => {
                    this.$notify({
                        title: "Warning",
                        message: "Failed to create set",
                        type: "warning"
                    });
                });
            },
            updateList() {
                this.$http.post('/api/profiler/list/update', {
                    list_id: this.editWidgets.id,
                    name: this.editWidgets.name,
                    list: this.editWidgets.list
                }).then(res => {
                    this.$notify({
                        title: "Great!",
                        message: "List updated successfully",
                        type: "success"
                    });
                    this.wList.filter(
                        l => l.id === this.editWidgets.id
                    )[0].widget_list = this.editWidgets.list;
                    this.visible4 = false;
                    this.showOverlay = false;
                }, res => {
                    this.$notify({
                        title: "Warning",
                        message: "Failed to create set",
                        type: "warning"
                    });
                });
            },
            submitSet() {
                this.$http.post('/api/profiler/set', {
                    data: this.editForm
                }).then(res => {
                    if (res.body.last_id !== null) {
                        this.editForm.id = res.body.last_id;
                        this.editForm.country = this.editForm.country.toString();
                        this.editForm.device = this.editForm.device.toString();
                        const lasts = this.sets.filter(s => s.id === res.body.last_id);
                        if (lasts.length) {
                            lasts[0].id = this.editForm.id;
                            lasts[0].bid = this.editForm.bid;
                            lasts[0].budget = this.editForm.budget;
                            lasts[0].country = this.editForm.country;
                            lasts[0].desc = this.editForm.desc;
                            lasts[0].device = this.editForm.device;
                            lasts[0].profile_id = this.editForm.profile_id;
                            lasts[0].user_id = this.userId;
                            lasts[0].widget_type = this.editForm.widget_type;
                            lasts[0].widget_list_id = this.editForm.widget_list_id;
                        }
                        else {
                            this.sets.push(this.editForm);
                        }
                        this.closeEdit();
                        this.$notify({
                            title: "Great!",
                            message: "Set created successfully ",
                            type: "success"
                        });
                    }
                }, res => {
                    this.$notify({
                        title: "Warning",
                        message: "Failed to create set",
                        type: "warning"
                    });
                });
            },
            addSet(profileId) {
                let emptySet = {
                    id: 0,
                    bid: '',
                    budget: '',
                    country: [],
                    desc: '',
                    device: ['all_os'],
                    profile_id: profileId,
                    user_id: this.userId,
                    widget_list_id: '',
                    widget_type: ''
                };
                this.showOverlay = true;
                this.visible2 = true;
                this.editForm = emptySet;
            },
            editSet(set) {
                this.showOverlay = true;
                this.visible2 = true;
                this.editForm.id = set.id;
                this.editForm.bid = set.bid;
                this.editForm.budget = set.budget;
                this.editForm.widget_list_id = parseInt(set.widget_list_id);
                this.editForm.widget_list_name = set.list_name;
                this.editForm.widget_type = set.widget_type;
                this.editForm.desc = set.desc;
                this.editForm.profile_id = set.profile_id;
                if (set.country.slice(1, -1).length) {
                    let cc_array = set.country.slice(1, -1).replace(/["]+/g, '').split(',');
                    if (cc_array && cc_array.length) this.editForm.country = cc_array;
                }
                if (set.device.slice(1, -1).length) {
                    let dt_array = set.device.slice(1, -1).replace(/["]+/g, '').replace(/\s+/g, "").split(',');
                    if (dt_array && dt_array.length) this.editForm.device = dt_array;
                }
            },
            editList(list) {
                this.visible4 = true;
                this.showOverlay = true;
                this.editWidgets.name = list.name;
                this.editWidgets.id = list.id;
                this.editWidgets.list = list.widget_list;
            },
            deleteSet(setId) {
                this.$http.post('/api/profiler/deletes', {
                    id: setId
                }).then(res => {
                    if (res.body.success) {
                        this.sets = this.sets.filter(s => s.id !== setId);
                        this.$notify({
                            title: "Great!",
                            message: "Set deleted successfully ",
                            type: "success"
                        });
                    }
                }, res => {
                    console.log(res)
                });
            },
            deleteList(listId) {
                this.$http.post('/api/profiler/deletel', {
                    id: listId
                }).then(res => {
                    if (res.body.success) {
                        this.wList = this.wList.filter(l => l.id !== listId);
                        this.$notify({
                            title: "Great!",
                            message: "List deleted successfully ",
                            type: "success"
                        });
                    }
                }, res => {
                    console.log(res)
                });
            },
            deleteProfile(profileId) {
                this.$http.post('/api/profiler/deletep', {
                    id: profileId
                }).then(res => {
                    if (res.body.success) {
                        this.profiles = this.profiles.filter(p => p.profile_id !== profileId);
                        this.$notify({
                            title: "Great!",
                            message: "Profile deleted successfully ",
                            type: "success"
                        });
                    }
                }, res => {
                    console.log(res)
                });
            },
            closePopup(popupId) {
                this.form.name = '';
                this.showOverlay = false;
                this.visible1 = false;
            },
            closeListPup() {
                this.widgetsForm = {
                    name: '',
                    widget_list: ''
                };
                this.showOverlay = false;
                this.visible3 = false;
            },
            closeEdit(formName) {
                this.widgetsForm.widget_list = '';
                this.widgetsForm.name = '';
                this.editForm = {
                    bid: '',
                    budget: '',
                    country: [],
                    desc: '',
                    device: ['all_os'],
                    id: '',
                    name: '',
                    profile_id: '',
                    user_id: '',
                    widget_list_id: '',
                    widget_type: ''
                };
                this.showOverlay = false;
                this.visible2 = false;
                this.visible3 = false;
                this.visible4 = false;
            },
            hasSet(profileId) {
                return this.sets.filter(s => parseInt(s.profile_id) === parseInt(profileId)).length > 0;
            },
            adjCountry(country) {
                if ((typeof country === 'string' || country instanceof String))
                    return country.replace(/"| |[\[\]']| /g, '').trim();
            },
            adjDevice(device) {
                if ((typeof device === 'string' || device instanceof String)) {
                    let devices = device.replace(/"| |[\[\]']| /g, '').trim().split(',');
                    devices = devices.map(d => this.deviceCodes[d]).toString();
                    return devices;
                }

            },
            listFormatter(row, column) {
                if (row.widget_list.length > 50) {
                    return row.widget_list.substring(0, 50).concat("...");
                } else {
                    return row.widget_list.substring(0, 50);
                }
            },
            listName(listId) {
                if (this.wList.filter(l => l.id === parseInt(listId)).length) {
                    return this.wList.filter(l => l.id === parseInt(listId))[0].name;
                } else {
                    return "NA"
                }
            },
            deviceValid() {
                let adIdx = Object.values(this.editForm.device).indexOf("all_devices");
                let osIdx = Object.values(this.editForm.device).indexOf("all_os");
                let dext = this.editForm.device.map(Number).some(r => [1, 2, 3].includes(r));
                let oext = this.editForm.device.map(Number).some(r => [4, 5, 6].includes(r));
                let mext = this.editForm.device.map(Number).some(r => [2, 3].includes(r));

                if (dext && adIdx >= 0) { // if any device code checked and "all_devices" exist
                    this.editForm.device.splice(adIdx, 1); // remove "all_devices"
                } else if (!dext && adIdx < 0) {
                    this.editForm.device.push("all_devices");
                }

                if (oext && osIdx >= 0) { // if any device code checked and "all_devices" exist
                    this.editForm.device.splice(osIdx, 1); // remove "all_devices"
                } else if (!oext && osIdx < 0) {
                    this.editForm.device.push("all_os");
                }

                if (!mext) { // if NO mobile code checked
                    this.editForm.device = this.editForm.device.filter(c => !["4", "5", "6"].includes(c));
                    if (osIdx < 0) {
                        this.editForm.device.push("all_os");
                    }
                }
            },
        },
        computed: {
            _all_devices()
            {
                for (let val of this.editForm.device) {
                    if (['1', '2', '3'].includes(val)) return true
                }
                return false
            },
            _all_os()
            {
                for (let val of this.editForm.device) {
                    if (['4', '5', '6'].includes(val)) return true
                }
                return false
            },
            _has_mobile()
            {
                for (let val of this.editForm.device) {
                    if (val === '2' || val === '3') return true
                }
                return false
            },
            validList()
            {
                let re = new RegExp("^(([0-9](,)?))+$");
                let validList = re.test(this.widgetsForm.widget_list.toString());
                return !validList || this.widgetsForm.widget_list.length <= 0;
            },
            validList2()
            {
                let re = new RegExp("^(([0-9](,)?))+$");
                let validList = re.test(this.editWidgets.list.toString());
                return !validList || this.editWidgets.list.length <= 0;
            },
            mandFill() {
                return !this.editForm.bid || !this.editForm.budget || !this.editForm.widget_list_id
                    || !this.editForm.widget_type > 0 || !this.editForm.desc || !this.editForm.country.length;
            }

        },
        watch: {
            'widgetsForm.widget_list': function (val) {  // keep unique values
                let unique = val.split(',').filter(function (elem, index, self) {
                    return index === self.indexOf(elem);
                });
                this.widgetsForm.widget_list = unique.toString().trim();
            },
            'editWidgets.list': function (val) {
                this.editWidgets.list = val.trim();
            },
        }
    }
</script>

<style scoped>
    .row.menu-tabs {
        max-width: 99% !important;
        margin-left: 0.5%;
        background: #f3f3f3;
        padding: 10px;
        border-radius: 5px;
    }

    .set-container .el-input {
        width: 10% !important;
        margin: 10px 0;
    }

    .last-field {
        margin: 15px 0;
    }

    .form-title {
        text-align: center;
        padding-bottom: 30px;
        font-size: 22px;
    }

    #overlay {
        position: fixed; /* Sit on top of the page content */
        width: 100%; /* Full width (cover the whole page) */
        height: 100%; /* Full height (cover the whole page) */
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5); /* Black background with opacity */
        z-index: 2; /* Specify a stack order in case you're using a different order for other elements */
        cursor: pointer; /* Add a pointer on hover */
    }

    .edit-form {
        z-index: 3;
        background: #ffffff;
        padding: 50px 50px 45px;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border-radius: 5px;
    }
</style>