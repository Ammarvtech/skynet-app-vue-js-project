<!--suppress CssUnusedSymbol -->
<template>
    <div id="site-configuration">
        <vue-progress-bar></vue-progress-bar>
        <vue-headful title="Site Configuration"/>
        <div v-if="this.$store.state.user.role === 'admin'">
            <!--Site Selection Form-->
            <div style="width: 100%; float:left; padding-bottom: 40px;">
                <div>
                    <form @submit="submit">
                        <el-row :gutter="20">
                            <el-col :span="4">
                                <v-autocomplete v-model="selected_theme" :items="themes" :menu-props="selected_theme"
                                                label="Theme" item-value="selected_theme" item-text="name" @change="refreshSite()"
                                                no-data-text="Loading..." return-object cache-items></v-autocomplete>
                            </el-col>
                            <el-col :span="4">
                                <websites-multi-dropdown @selectWebsite="selectWebsite($event)"
                                                   v-bind:display_all="true" v-bind:display_global="true"
                                                   :filter="selected_theme['theme_sites']"></websites-multi-dropdown>
                            </el-col>
                            <el-col :span="4">
                                <v-select v-model="selected_device" :items="devices" label="Device"></v-select>
                            </el-col>
                            <el-col :span="4">
                                <v-autocomplete v-model="selected_key" :items="keys" :menu-props="selected_key"
                                                label="Key" item-value="selected_key" item-text="name"
                                                no-data-text="Loading..." return-object cache-items></v-autocomplete>
                            </el-col>
                            <el-col :span="1" style="padding-top: 8px;">
                                <v-btn @click="items=[]" type="submit" color="info"
                                       :disabled="loading || this.site_id === ''">Submit</v-btn>
                            </el-col>
                        </el-row>
                    </form>
                </div>
                <!--Filter-->
                <div class="row">
                    <search-box @selectFilter="selectFilter($event)"></search-box>
                </div>
            </div>

            <!--Site Configuration Table-->
            <v-data-table :headers="headers" :items="_items" :rows-per-page-items="[20,15,10,5,{'text':'All','value':-1}]"
                          class="elevation-1" no-data-text="No data to display" :loading="loading" item-key="id">
                <template slot="items" slot-scope="props">
                    <tr>
                    <td>
                        <div style="float: left; margin-top: 18px;">
                            <el-tooltip placement="top">
                                <div slot="content">History</div>
                                <span @click="openHistory(props)"><i class="fas fa-history" style="font-size: 18px; cursor:pointer;"></i></span>
                            </el-tooltip>
                        </div>
                    </td>
                    <td>
                        <el-tooltip placement="top">
                            <div slot="content"> {{ props.item.theme }}</div>
                            <span>{{ props.item.site_name }}</span>
                        </el-tooltip>
                    </td>
                    <td>{{ props.item.key }}</td>
                    <td>{{ props.item.device }}</td>
                    <td v-if="props.item.value_type === 'json' || props.item.value_type === 'string'">
                        <v-dialog v-model="value_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="change_value(false)">
                            <v-btn slot="activator" @click="edit_item(props.item, 'value')" style="margin: 0"
                                   type="submit" fab small color="info" :disabled="props.item.use_group">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Edit Value: {{edited_item.site_name}}: {{edited_item.key}}: {{edited_item.device}} ({{edited_item.value_type}})
                                </v-card-title>
                                <div v-if="edited_item.value_type === 'json'">
                                    <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px"
                                                  @error="blockApplyJson()" @input="allowApplyJson()">
                                    </v-jsoneditor>
                                </div>
                                <div v-else>
                                    <v-textarea
                                    v-model="edited_item.value"
                                    background-color="grey lighten-2"
                                    rows="30"
                                    ></v-textarea>
                                </div>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="change_value(false)">Discard</v-btn>
                                    <v-btn color="green darken-1" flat :disabled="!allow_apply_json"
                                           @click.native="change_value(true)">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td v-else>
                        <template v-slot:input>
                          <v-text-field
                            v-model="props.item.value"
                            @keydown="only_number"
                            label="Edit"
                            single-line
                          ></v-text-field>
                        </template>
                    </td>
                    <td>
                        <el-popover v-model="props.item.ab_percentage_pop" placement="bottom" width="400px"
                            popperClass="percentage_popover" trigger="click">
                            <el-form :inline="true" style="height: 50px;margin: 0 0 0 45px;">
                                <el-form-item style="margin-left: -20px">
                                    <el-col>
                                        <span class="larger_font" style="margin-left: -23px;">Change percentage to:</span>
                                        <a-input-number
                                            @keydown="only_number"
                                            size="large"
                                            :min="-1"
                                            :max="100"
                                            step="1"
                                            v-model="props.item.ab_testing_percentage"
                                            v-on:input="set_changes_made"
                                            :disabled="props.item.use_group"
                                        />
                                    </el-col>
                                </el-form-item>
                            </el-form>
                            <span slot="reference" :style="link_style">{{ props.item.ab_testing_percentage }}</span>
                        </el-popover>
                    </td>
                    <td v-if="props.item.use_group">
                        <v-btn style="margin: 0;" fab small color="info" :disabled="true">
                            <v-icon>fas fa-edit</v-icon>
                        </v-btn>
                    </td>
                    <td v-if="!props.item.use_group">
                        <v-dialog v-model="ab_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="change_ab_settings(false)">
                            <v-btn slot="activator" @click="edit_item(props.item, 'ab_settings')"
                                   style="margin: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Edit AB Settings: {{edited_item.site_name}}: {{edited_item.key}}: {{edited_item.device}} ({{edited_item.value_type}})
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px"
                                              @error="blockApplyJson()" @input="allowApplyJson()">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="change_ab_settings(false)">Discard</v-btn>
                                    <v-btn color="green darken-1" flat :disabled="!allow_apply_json"
                                           @click.native="change_ab_settings(true)">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td><v-switch v-model="props.item.use_group" :label="`${props.item.use_group.toString()}`"
                                  @change="$forceUpdate()"></v-switch></td>
                    <td v-if="!props.item.use_group">
                        <v-btn style="margin: 0;" fab small color="info" :disabled="true">
                            <v-icon>fas fa-edit</v-icon>
                        </v-btn>
                    </td>
                    <td v-if="props.item.use_group">
                        <v-dialog v-model="group_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="change_group_vals(false)">
                            <v-btn slot="activator" @click="edit_item(props.item, 'group_vals')"
                                   style="margin: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Edit Group Values: {{edited_item.site_name}}: {{edited_item.key}}: {{edited_item.device}} ({{edited_item.value_type}})
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px"
                                              @error="blockApplyJson()" @input="allowApplyJson()">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="change_group_vals(false)">Discard</v-btn>
                                    <v-btn color="green darken-1" flat :disabled="!allow_apply_json"
                                           @click.native="change_group_vals(true)">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td v-if="!props.item.use_group">
                        <v-btn style="margin: 0;" fab small color="info" :disabled="true">
                            <v-icon>fas fa-edit</v-icon>
                        </v-btn>
                    </td>
                    <td v-if="props.item.use_group">
                        <v-dialog v-model="country_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="change_group_country_settings(false)">
                            <v-btn slot="activator" @click="edit_item(props.item, 'group_country_settings')"
                                   style="margin: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Edit Group Country Settings: {{edited_item.site_name}}: {{edited_item.key}}: {{edited_item.device}} ({{edited_item.value_type}})
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px"
                                              @error="blockApplyJson()" @input="allowApplyJson()">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="change_group_country_settings(false)">Discard</v-btn>
                                    <v-btn color="green darken-1" flat :disabled="!allow_apply_json"
                                           @click.native="change_group_country_settings(true)">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td v-if="disable_button(props.item) || props.item.site_id === -1">
                        <v-btn color="info" :disabled="true">
                            Compare
                        </v-btn>
                    </td>
                    <td v-else>
                        <v-dialog v-model="compare_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="compare_dialog = false">
                            <v-btn slot="activator" @click="edit_item(props.item, '')" type="submit" color="info">
                                Compare
                            </v-btn>
                            <v-card :style="gray_background">
                                <v-card-title class="headline">Diff</v-card-title>
                                <div style="width: 100%; padding:16px" v-if="edited_item.changes_made">
                                    <div style="width:50%; float: left;">
                                        <u>Previous Values</u>
                                    </div>
                                    <div style="overflow:hidden;">
                                        <u>New Values</u>
                                    </div>
                                </div>
                                <div style="padding-left:16px;"
                                     v-if="edited_item.value !== edited_item.prev_value">
                                    <div v-if="edited_item.value_type !== 'json'">
                                        <div style="width:50%; float: left;">
                                            {{ edited_item.prev_value }}
                                        </div>
                                        <div style="overflow:hidden;">
                                            {{ edited_item.value }}
                                        </div>
                                    </div>
                                    <div v-else>
                                        <div style="width: 100%; overflow: hidden;">
                                            <div style="width:50%; float: left;">
                                                <vue-json-cool :style="gray_background" :data="old_value">
                                                </vue-json-cool>
                                            </div>
                                            <div style="overflow:hidden;">
                                                <vue-json-compare :style="gray_background"
                                                                  :oldData="old_value" :newData="new_value">
                                                </vue-json-compare>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div style="padding-left:16px"
                                     v-if="edited_item.ab_testing_percentage !== edited_item.prev_ab_testing_percentage">
                                    <div style="width: 100%; overflow: hidden;">
                                        <div style="width:50%; float: left;">
                                            {{ edited_item.prev_ab_testing_percentage }}
                                        </div>
                                        <div style="overflow:hidden;">
                                            {{ edited_item.ab_testing_percentage }}
                                        </div>
                                    </div>
                                </div>
                                <div style="padding-left:16px"
                                     v-if="edited_item.use_group !== edited_item.prev_use_group">
                                    <div style="width: 100%; overflow: hidden;">
                                        <div style="width:50%; float: left;">
                                            <b><u>Use group</u></b>: {{ edited_item.prev_use_group }}
                                        </div>
                                        <div style="overflow:hidden;">
                                            <b><u>Use group</u></b>: {{ edited_item.use_group }}
                                        </div>
                                    </div>
                                </div>
                                <div style="padding-left:16px"
                                     v-if="edited_item.ab_testing_config !== edited_item.prev_ab_testing_config">
                                    <div style="width: 100%; overflow: hidden;">
                                        <div style="width:50%; float: left;">
                                            <vue-json-cool :data="old_ab">
                                            </vue-json-cool>
                                        </div>
                                        <div style="overflow:hidden;">
                                            <vue-json-compare :oldData="old_ab" :newData="new_ab">
                                            </vue-json-compare>
                                        </div>
                                    </div>
                                </div>
                                <div style="padding-left:16px"
                                     v-if="edited_item.group_vals !== edited_item.prev_group_vals">
                                    <div style="width: 100%; overflow: hidden;">
                                        <div style="width:50%; float: left;">
                                            <vue-json-cool :data="old_group_vals">
                                            </vue-json-cool>
                                        </div>
                                        <div style="overflow:hidden;">
                                            <vue-json-compare :oldData="old_group_vals" :newData="new_group_vals">
                                            </vue-json-compare>
                                        </div>
                                    </div>
                                </div>
                                <div style="padding-left:16px"
                                     v-if="edited_item.group_country_settings !== edited_item.prev_group_country_settings">
                                    <div style="width: 100%; overflow: hidden;">
                                        <div style="width:50%; float: left;">
                                            <vue-json-cool :data="old_group_country_settings">
                                            </vue-json-cool>
                                        </div>
                                        <div style="overflow:hidden;">
                                            <vue-json-compare :oldData="old_group_country_settings" :newData="new_group_country_settings">
                                            </vue-json-compare>
                                        </div>
                                    </div>
                                </div>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat @click.native="close_changes()">
                                        Close
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td v-if="disable_button(props.item) || props.item.site_id === -1">
                        <v-btn color="info" :disabled="true">
                            {{ applyText(props.item) }}
                        </v-btn>
                    </td>
                    <td v-else>
                        <v-dialog v-model="apply_dialog" persistent max-width="290">
                            <v-btn slot="activator" @click="edit_item(props.item, '')" type="submit" color="info">
                                {{ applyText(props.item) }}
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">Are you sure?</v-card-title>
                                <v-card-text>
                                    Apply changes to {{edited_item.site_name}}: {{edited_item.key}}: {{edited_item.device}}
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="red darken-1" flat @click="apply_dialog = false">Cancel</v-btn>
                                    <v-btn color="green darken-1" flat @click="apply()">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    <td v-if="!disable_button(props.item) || keys_publish[props.item.key] === 0">
                        <v-btn color="info" :disabled="true">
                            Apply to multiple sites
                        </v-btn>
                    </td>
                    <td v-else>
                        <v-dialog v-model="publish_dialog" persistent max-width="30%">
                            <v-btn slot="activator" @click="edit_item(props.item, '')" type="submit" color="info">
                                Apply to multiple sites
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">1. Which parameters do you want to apply?</v-card-title>
                                <v-card-text>
                                        <v-checkbox v-model="apply_value" label="Default Value"></v-checkbox>
                                        <v-checkbox v-model="apply_ab_settings" label="AB Tests"></v-checkbox>
                                        <v-checkbox v-model="apply_group_vals" label="Group Tests"></v-checkbox>
                                </v-card-text>
                                <v-card-title class="headline">2. To which sites?</v-card-title>
                                <v-card-text>
                                    <div style="float:left;">
                                        <websites-multi-dropdown @selectWebsite="selectPublishWebsite($event)"
                                                                 v-bind:display_all="false" v-bind:display_global="false"
                                                                 :filter="selected_theme['theme_sites']"></websites-multi-dropdown>
                                    </div>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="red darken-1" flat @click="publish_dialog = false">Cancel</v-btn>
                                    <v-btn color="green darken-1" flat @click="publish()" v-if="apply_value || apply_ab_settings || apply_group_vals">Apply</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </td>
                    </tr>
                </template>
                 <template slot="expand" slot-scope="props">
                     <v-card flat>
                         <v-card-text class="no-padding">
                             <div v-if="!history_loaded">Loading. . .</div>
                             <div v-else class="no-padding">
                                 <websites-settings-history @revertItem="revertItem(props.item, $event)"
                                         v-bind:history="history" v-bind:value_type="props.item.value_type">
                                 </websites-settings-history>
                             </div>
                         </v-card-text>
                     </v-card>
             </template>
            </v-data-table>
        </div>
    </div>
</template>

<script>
    import moment from 'moment';
    import alerts from "./mixins/alerts";

    export default {
        name: 'SiteConfiguration',
        mixins: [alerts],
        mounted() {
            this.$emit('validateUser');
            this.getThemes();
            this.getKeys();
        },
        data() {
            return {
                history: [],
                history_loaded: false,
                search: '',
                keys: [],
                keys_publish: {},
                themes: [],
                devices: [
                    'All',
                    'Mobile',
                    'Tablet',
                    'Desktop'
                ],
                items: [],
                headers: [
                    {value: '', text: '', sortable: false},
                    {value: 'site_name', text: 'Site', sortable: false},
                    {value: 'key', text: 'Key'},
                    {value: 'device', text: 'Device'},
                    {value: 'value', text: 'Default Value', sortable: false},
                    {value: 'ab_testing_percentage', text: 'AB %'},
                    {value: 'ab_testing_config', text: 'AB Settings', sortable: false},
                    {value: 'use_group', text: 'Use Group', sortable: false},
                    {value: 'group_vals', text: 'Group Values', sortable: false},
                    {value: 'group_country_settings', text: 'Group Country Settings', sortable: false},
                    {value: '', text: '', sortable: false},
                    {value: '', text: '', sortable: false},
                    {value: '', text: '', sortable: false},
                ],
                site_id: '',
                publish_site_id: '',
                selected_device: 'All',
                selected_theme: 'All',
                selected_key: 'All',
                loading: false,
                value_dialog: false,
                ab_dialog: false,
                compare_dialog: false,
                apply_dialog: false,
                group_dialog: false,
                country_dialog: false,
                publish_dialog: false,
                link_style: {
                    cursor: 'pointer'
                },
                dialog_text: '',
                dialog_json: {},
                edited_index: -1,
                edited_item: {
                    site_name: '',
                    key: '',
                    device: '',
                    value: {},
                    value_type: 'json',
                    ab_testing_percentage: 0,
                    ab_testing_config: {},
                    use_group: 0,
                    group_vals: {},
                    group_country_settings: {},
                    admin_enabled: 1,
                    changes_made: false,
                },
                default_item: {
                    site_name: '',
                    key: '',
                    device: '',
                    value: {},
                    value_type: 'json',
                    ab_testing_percentage: 0,
                    ab_testing_config: {},
                    use_group: 0,
                    group_vals: {},
                    group_country_settings: {},
                    admin_enabled: 1,
                    changes_made: false,
                },
                filter: null,
                edited_json : {},
                allow_apply_json: true,
                new_value: {},
                new_ab: {},
                new_group_vals: {},
                new_group_country_settings: {},
                old_value: {},
                old_ab: {},
                old_group_vals: {},
                old_group_country_settings: {},
                json_editor_options: {
                    mode: 'code', // initial mode
                    modes: ['code', 'tree'], // allowed modes
                    enableTransform: false,
                },
                gray_background: {
                  backgroundColor: '#f6f8fa'
                },
                apply_value: false,
                apply_ab_settings: false,
                apply_group_vals: false,
            }
        },
        methods: {
            refreshSite() {
                const sites = JSON.parse(this.selected_theme.theme_sites);
                if (sites.indexOf(this.site_id.website_id) === -1) {
                    this.site_id = '';
                }
            },
            revertItem(props, item) {
                const updated_time = moment(String(item['updated_date'], "'")).format('YYYY-MM-DD hh:mm:ss');
                const message = 'You are about to revert the key to the value from ' + updated_time + ', are you sure?';
                this.$confirm(message, 'Revert Key Properties',
                    {
                        confirmButtonText: 'Yes',
                        cancelButtonText: 'No',
                        type: 'warning'
                    }).then(() => {
                        this.edited_index = this.items.indexOf(props);

                        this.items[this.edited_index].value = item.value;
                        this.items[this.edited_index].ab_testing_config = item.ab_testing_config;
                        this.items[this.edited_index].ab_testing_percentage = item.ab_testing_percentage;
                        this.items[this.edited_index].use_group = item.use_group === 1;
                        this.items[this.edited_index].group_vals = item.group_vals;
                        this.items[this.edited_index].group_country_settings = item.group_country_settings;

                        this.set_changes_made();
                        this.edited_index = -1;
                }).catch();
            },
            openHistory(props) {
                props.expanded = !props.expanded;

                if (props.expanded) {
                    let params = {
                        'site_id': props.item.site_id,
                        'device': props.item.device,
                        'key': props.item.key
                    };

                    this.$http.get('/api/website/config_history', {params: params}).then(res => {
                        if (res.body) {
                            this.history = Object.keys(res.body.result).map((key) => { return res.body.result[key]});
                            this.history_loaded = true;
                        }
                    }).catch(e => {
                        this.notice('Error has occurred, Please try again');
                        props.expanded = !props.expanded;
                        console.log(e);
                    })
                } else {
                    this.history_loaded = false;
                }
            },
            applyText(item) {
                if (item.site_id === "-1") {
                    return 'Apply to global';
                }

                return 'Apply';
            },
            allowApplyJson() {
                this.allow_apply_json = true;
            },
            blockApplyJson() {
                this.allow_apply_json = false;
            },
            selectPublishWebsite(sites) {
                this.publish_site_id = {'website_id': '', 'website_name': ''};
                sites.forEach(site => {
                    this.publish_site_id['website_id'] += site['website_id'] + ',';
                    this.publish_site_id['website_name'] += site['website_name'] + ',';
                });
                this.publish_site_id['website_id'] = this.publish_site_id['website_id'].slice(0, -1);
                this.publish_site_id['website_name'] = this.publish_site_id['website_name'].slice(0, -1);
            },
            selectWebsite(sites) {
                this.site_id = {'website_id': '', 'website_name': ''};
                sites.forEach(site => {
                    this.site_id['website_id'] += site['website_id'] + ',';
                    this.site_id['website_name'] += site['website_name'] + ',';
                });
                this.site_id['website_id'] = this.site_id['website_id'].slice(0, -1);
                this.site_id['website_name'] = this.site_id['website_name'].slice(0, -1);
            },
            selectFilter(filter) {
                this.filter = filter;
            },
            submit(event) {
                if (event !== null) event.preventDefault();
                let site_id = this.site_id.website_id;
                let device = (this.selected_device ? this.selected_device : 'all').toLocaleLowerCase();
                let key = (this.selected_key.name ? this.selected_key.name : 'all').toLocaleLowerCase();
                let params = {
                    'site_id': site_id,
                    'device': device,
                    'key': key
                };

                this.start_loading();
                this.$http.get('/api/website/site_config', {params: params}).then(res => {
                    if (res.body) {
                        this.items = Object.keys(res.body.result).map((key) => { return res.body.result[key]});

                        if (this.items) {
                            this.init_items();
                        }

                        this.finish_loading(true);
                    } else {
                        this.finish_loading(false);
                        this.notice('Error has occurred, Please try again');
                    }
                }).catch(e => {
                    this.finish_loading(false);
                    this.notice('Error has occurred, Please try again');
                    console.log(e);
                })
            },
            init_items() {
                this.items.forEach((item) => {
                    if(item.ab_testing_config) {
                        item.ab_testing_config = JSON.stringify(JSON.parse(item.ab_testing_config));
                    } else {
                        item.ab_testing_config = '{}';
                    }
                    if (item.value_type === 'json') {
                        item.value = JSON.stringify(JSON.parse(item.value));
                    }

                    item.use_group = item.use_group === 1;
                    item.prev_value = item.value;
                    item.prev_ab_testing_percentage = item.ab_testing_percentage;
                    item.prev_ab_testing_config = item.ab_testing_config;
                    item.prev_use_group = item.use_group;
                    item.prev_group_vals = item.group_vals;
                    item.prev_group_country_settings = item.group_country_settings;
                    item.ab_percentage_pop = false;
                    item.changes_made = false;
                    item.id = item.key + '_' + item.device + '_' + item.site_name;

                    if (item.value_type !== 'json' && item.value_type !== 'string')
                    {
                        item.value_pop = false;
                    }
                });
            },
            getKeys() {
                this.$http.get('/api/website/keys').then(res => {
                    if (res.body) {
                        this.keys = Object.keys(res.body).map(key => res.body[key]);
                        this.keys_publish = this.keys.reduce(function(map, obj) {
                            map[obj.name] = obj.allow_publish;
                            return map;
                        }, {})
                        this.keys.unshift('All');
                    }
                }).catch(e => {
                    this.notice('Error has occurred, Please try again');
                    console.log(e);
                });
            },
            getThemes() {
                this.$http.get('/api/website/themes').then(res => {
                    if (res.body) {
                        this.themes = Object.keys(res.body).map(key => res.body[key]);
                        this.themes.unshift({'name': 'All', 'theme_sites': null});
                    }
                }).catch(e => {
                    this.notice('Error has occurred, Please try again');
                    console.log(e);
                });
            },
            only_number($event) {
                let evt = ($event) ? $event : Window.event;
                let charCode = (evt.which) ? evt.which : evt.keyCode;
                console.log(charCode);
                if ([46, 8, 9, 27, 13, 110, 190].indexOf(charCode) !== -1 ||
                    // Allow: Ctrl+A
                    (charCode === 65 && evt.ctrlKey === true) ||
                    // Allow: Ctrl+C
                    (charCode === 67 && evt.ctrlKey === true) ||
                    // Allow: Ctrl+X
                    (charCode === 88 && evt.ctrlKey === true) ||
                    // Allow: home, end, left, right
                    (charCode === 189 || charCode === 109) ||
                    // Allow: minus sign
                    (charCode >= 35 && charCode <= 39)) {
                    // let it happen, don't do anything
                    return;
                }
                // Ensure that it is a number and stop the keypress
                if (($event.shiftKey || (charCode < 48 || charCode > 57)) && (charCode < 96 || charCode > 105)) {
                    $event.preventDefault();
                }
            },
            edit_item(site_id, text) {
                this.start_loading();
                this.edited_index = this.items.indexOf(site_id);
                this.edited_item = Object.assign({}, site_id);
                if (text === 'value') {
                    if (this.edited_item.value_type === 'json') {
                        this.edited_json = JSON.parse(this.edited_item.value);
                    }
                } else if (text === 'ab_settings') {
                    this.edited_json = JSON.parse(this.edited_item.ab_testing_config);
                } else if (text === 'group_vals') {
                    this.edited_json = JSON.parse(this.edited_item.group_vals);
                } else if (text === 'group_country_settings') {
                    this.edited_json = JSON.parse(this.edited_item.group_country_settings);
                } else {
                    this.new_value = JSON.parse(this.edited_item.value);
                    this.new_ab = JSON.parse(this.edited_item.ab_testing_config);
                    this.new_group_vals = JSON.parse(this.edited_item.group_vals);
                    this.new_group_country_settings = JSON.parse(this.edited_item.group_country_settings);
                    this.old_value = JSON.parse(this.edited_item.prev_value);
                    this.old_ab = JSON.parse(this.edited_item.prev_ab_testing_config);
                    if(this.edited_item.prev_group_vals === null) {
                        this.old_group_vals = {};
                    } else {
                        this.old_group_vals = JSON.parse(this.edited_item.prev_group_vals);
                    }
                    if(this.edited_item.prev_group_country_settings === null) {
                        this.old_group_country_settings = {};
                    } else {
                        this.old_group_country_settings = JSON.parse(this.edited_item.prev_group_country_settings);
                    }
                }

                this.finish_loading(true);
            },
            change_value(apply_changes) {
                this.value_dialog = false;
                if (apply_changes) {
                    if (this.items[this.edited_index].value_type === 'json') {
                        this.items[this.edited_index].value = JSON.stringify(this.edited_json);
                        this.allow_apply_json = true;
                    } else {
                        this.items[this.edited_index].value = this.edited_item.value;
                    }

                    this.set_changes_made();
                }

                this.close_dialog();
            },
            change_ab_settings(apply_changes) {
                this.ab_dialog = false;
                if (apply_changes) {
                    this.items[this.edited_index].ab_testing_config = JSON.stringify(this.edited_json);

                    this.set_changes_made();
                }

                this.close_dialog();
            },
            change_group_vals(apply_changes) {
                this.group_dialog = false;
                if (apply_changes) {
                    this.items[this.edited_index].group_vals = JSON.stringify(this.edited_json);

                    this.set_changes_made();
                }

                this.close_dialog();
            },
            change_group_country_settings(apply_changes) {
                this.country_dialog = false;
                if (apply_changes) {
                    this.items[this.edited_index].group_country_settings = JSON.stringify(this.edited_json);

                    this.set_changes_made();
                }

                this.close_dialog();
            },
            set_changes_made() {
                const ab_testing_changed = this.items[this.edited_index].ab_testing_config !== this.items[this.edited_index].prev_ab_testing_config;
                const ab_percentage_changed = this.items[this.edited_index].prev_ab_testing_percentage !== this.items[this.edited_index].ab_testing_percentage;
                const value_changed = this.items[this.edited_index].value !== this.items[this.edited_index].prev_value;
                const group_vals_changed = this.items[this.edited_index].group_vals !== this.items[this.edited_index].prev_group_vals;
                const group_country_settings_changed = this.items[this.edited_index].group_country_settings !== this.items[this.edited_index].prev_group_country_settings;

                this.items[this.edited_index].changes_made = ab_testing_changed || ab_percentage_changed || value_changed || group_vals_changed || group_country_settings_changed;

                this.$forceUpdate();
            },
            start_loading() {
                this.loading = true;
                this.$Progress.start();
            },
            finish_loading(status) {
                this.loading = false;
                if (status) {
                    this.$Progress.finish();
                } else {
                    this.$Progress.fail();
                }
            },
            close_changes() {
                this.compare_dialog = false;
                this.apply_dialog = false;
                this.close_dialog();
            },
            close_dialog() {
                setTimeout(() => {
                    this.edited_item = Object.assign({}, this.default_item);
                    this.edited_index = -1;
                    this.edited_json = {};
                }, 300)
            },
            ab_discrepancy(item) {
              return item.ab_testing_percentage > -1 && item.ab_testing_config === "{}";
            },
            disable_button(item) {
                return this.loading
                    || this.ab_discrepancy(item)
                    || (!item.changes_made
                        && item.prev_ab_testing_percentage === item.ab_testing_percentage
                        && item.use_group === item.prev_use_group);
            },
            publish() {
                const c = this.publish_site_id['website_id'].split(',').length;
                let params = {
                    'source': this.edited_item.site_id,
                    'key': this.edited_item.key,
                    'device': this.edited_item.device,
                    'sites': this.publish_site_id.website_id,
                    'fields': {
                        'value': this.apply_value,
                        'ab_testing_percentage': this.apply_ab_settings,
                        'ab_testing_config': this.apply_ab_settings,
                        'use_group': this.apply_group_vals,
                        'group_vals': this.apply_group_vals,
                        'group_country_settings': this.apply_group_vals,
                    },
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                const message = 'You are about to publish ' + this.edited_item.key + ' ' + this.edited_item.device + ' to ' + c + ' sites, are you sure?';
                this.$confirm(message, 'Apply to multiple sites',
                    {
                        confirmButtonText: 'Yes',
                        cancelButtonText: 'No',
                        type: 'warning'
                    }).then(() => {
                        this.$Progress.start();
                        this.$http.post('/api/website/batch/site_config', {params: params}).then(res => {
                            if (res.body) {
                                if (res.body.status) {
                                    this.$Progress.finish();
                                    this.publish_dialog = false;
                                } else {
                                    this.notice('Error has occurred, Please try again');
                                    this.$Progress.fail();
                                }
                            }
                        }).catch(e => {
                            this.loading = false;
                            if(e.status === 401 || e.status === 500) {
                                this.$emit('logout');
                            }
                            else {
                                this.notice('Error has occurred, Please try again');
                            }
                        });
                    }).catch();
            },
            apply() {
                let params = {
                    'site_id': this.edited_item.site_id,
                    'key': this.edited_item.key,
                    'device': this.edited_item.device,
                    'value': this.edited_item.value,
                    'ab_testing_percentage': this.edited_item.ab_testing_percentage,
                    'ab_testing_config': this.edited_item.ab_testing_config,
                    'group_vals': this.edited_item.group_vals,
                    'use_group_vals': this.edited_item.use_group,
                    'group_country_settings': this.edited_item.group_country_settings,
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$Progress.start();
                this.$http.post('/api/website/site_config', {params: params}).then(res => {
                    if (res.body) {
                        if (res.body.status[0]) {
                            this.items[this.edited_index].prev_value = this.items[this.edited_index].value;
                            this.items[this.edited_index].prev_ab_testing_percentage = this.items[this.edited_index].ab_testing_percentage;
                            this.items[this.edited_index].prev_ab_testing_config = this.items[this.edited_index].ab_testing_config;
                            this.items[this.edited_index].prev_group_vals = this.items[this.edited_index].group_vals;
                            this.items[this.edited_index].prev_use_group = this.items[this.edited_index].use_group;
                            this.items[this.edited_index].prev_group_country_settings = this.items[this.edited_index].group_country_settings;
                            this.items[this.edited_index].changes_made = false;
                            this.$Progress.finish();
                            this.close_changes();
                        } else {
                            this.notice('Error has occurred, Please try again');
                            this.$Progress.fail();
                        }
                    }
                }).catch(e => {
                    this.loading = false;
                    if(e.status === 401 || e.status === 500) {
                        this.$emit('logout');
                    }
                    else {
                        this.notice('Error has occurred, Please try again');
                    }
                });
            }
        },
        computed: {
            sites() {
                let sites = this.items;

                if(this.search) {
                    sites = sites.filter(i =>
                    i.key.toLocaleLowerCase().indexOf(this.search.toLocaleLowerCase()) !== -1);
                }

                return sites;
            },
            _items() {
                if (!this.items) {
                    return [];
                }

                let items = this.items;

                // Apply theme name to items
                items.forEach(item => {
                    item['theme'] = '';
                    for (let j = 0; j < this.themes.length; j++){
                        const theme = this.themes[j];
                        if(theme['name'] !== 'All') {
                            const sites = JSON.parse(theme['theme_sites']);
                            if (sites.indexOf(parseInt(item.site_id)) !== -1) {
                                item['theme'] = theme['name'];
                                break;
                            }
                        }
                    }
                });

                const fix = v => {
                    if (v instanceof Object) {
                        return ['value', 'ab_testing_config', 'group_vals', 'group_country_settings'].map(k => fix(v[k])).join(' ');
                    }
                    return String(v, 'string');
                };

                // Apply filter
                if (this.filter && this.filter.length > 0) {
                    const regex = new RegExp('.*' + this.filter + '.*');
                    items = items.filter(item => regex.test(fix(item)));
                    this.$Progress.finish();
                }

                return items;
            }
        }
    }
</script>

<style scoped>
    @import "../../node_modules/vuetify/dist/vuetify.min.css";
</style>

<style>
    /* Below styles are overrides to used components, thus THEY ARE IN USE, do not remove thinking they are not used */
    .v-dialog__activator {
        cursor: initial;
    }
    .alpaca-string {
        color: #2c962c;
    }
    .alpaca-upd {
        background-color: #fff8a5;
    }
    .el-popover {
        z-index: 201!important;
    }
    table.v-table thead th:first-child, table.v-table thead th:not(:first-child) {
        vertical-align: bottom!important;
        padding-bottom: 5px;
        font-size: 16px;
    }
    .no-padding {
        padding: 0!important;
    }
    .v-input--selection-controls:not(.v-input--hide-details) .v-input__slot {
        margin-bottom: 0;
    }
</style>
