<template>
    <v-data-table :headers="headers" :items="history" class="elevation-1" no-data-text="No data to display"
                  :disable-pagination="true" :rows-per-page-items="[3]">
        <template slot="items" slot-scope="props">
            <tr>
                <td> {{ props.item.updated_date | formatDate }} </td>
                <td>
                    <v-dialog v-model="value_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="value_dialog=false">
                            <v-btn slot="activator" @click="edit_item(props.item, 'value')" style="margin-left: 0"
                                   type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Value
                                </v-card-title>
                                <div v-if="value_type === 'json'">
                                    <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px">
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
                                           @click.native="value_dialog=false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                </td>
                <td> {{ props.item.ab_testing_percentage }} </td>
                <td> <v-dialog v-model="ab_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="ab_dialog = false">
                            <v-btn slot="activator" @click="edit_item(props.item, 'ab_settings')"
                                   style="margin-left: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    AB Settings
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat @click.native="ab_dialog = false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog> </td>
                <td> {{ props.item.use_group | formatBool }} </td>
                <td>
                    <v-dialog v-model="group_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="group_dialog = false">
                            <v-btn slot="activator" @click="edit_item(props.item, 'group_vals')"
                                   style="margin-left: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Group Values:
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="group_dialog = false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                </td>
                <td>
                    <v-dialog v-model="country_dialog" persistent max-width="75%" max-height="80%"
                                  @keydown.esc="country_dialog = false">
                            <v-btn slot="activator" @click="edit_item(props.item, 'group_country_settings')"
                                   style="margin-left: 0;" type="submit" fab small color="info">
                                <v-icon>fas fa-edit</v-icon>
                            </v-btn>
                            <v-card>
                                <v-card-title class="headline">
                                    Group Country Settings
                                </v-card-title>
                                <v-jsoneditor :options="json_editor_options" v-model="edited_json" height="700px">
                                </v-jsoneditor>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" flat
                                           @click.native="country_dialog = false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                </td>
                <td><v-btn color="info" flat @click="revert(props.item)">Revert to this version</v-btn></td>
            </tr>
        </template>
    </v-data-table>
</template>

<script>
    import moment from 'moment';

    export default {
        name: "WebsiteSettingsHistory",
        props: {
            history: Array,
            value_type: String,
            json_editor_options: Object,
        },
        data() {
            return {
                edited_item: null,
                edited_json: null,
                value_dialog: false,
                ab_dialog: false,
                group_dialog: false,
                country_dialog: false,
                headers: [
                    {value: 'updated_date', text: 'Updated Date'},
                    {value: 'value', text: 'Default Value', sortable: false},
                    {value: 'ab_testing_percentage', text: 'AB %', sortable: false},
                    {value: 'ab_testing_config', text: 'AB Settings', sortable: false},
                    {value: 'use_group', text: 'Use Group', sortable: false},
                    {value: 'group_vals', text: 'Group Values', sortable: false},
                    {value: 'group_country_settings', text: 'Group Country Settings', sortable: false},
                    {value: '', text: '', sortable: false},
                ],
            }
        },
        methods: {
          edit_item(item, text) {
                this.edited_item = Object.assign({}, item);
                if (text === 'value') {
                    if (this.value_type === 'json') {
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
                    this.old_value = JSON.parse(this.edited_item.prev_value);
                    this.old_ab = JSON.parse(this.edited_item.prev_ab_testing_config);
                    if(this.edited_item.prev_group_vals === null) {
                        this.old_group_vals = {};
                    } else {
                        this.old_group_vals = JSON.parse(this.edited_item.prev_group_vals);
                    }
                }
            },
            revert(item) {
              this.$emit('revertItem', item);
            }
        },
        filters: {
            formatDate: function(value) {
                if (value) {
                    return moment(String(value, "'")).format('YYYY-MM-DD HH:mm:ss')
                }
            },
            formatBool: function(value) {
                if (value === 0){
                    return 'false';
                }

                return 'true';
            }
        }
    }
</script>

<style scoped>
    @import "../../../node_modules/vuetify/dist/vuetify.min.css";
</style>