<template>
    <div id='container' style="margin:18px auto 0; width:250px;">
        <label aria-hidden="true">Websites</label>
        <ejs-multiselect :dataSource='sites' placeholder="Websites" mode="CheckBox" :fields='fields'
                         :showSelectAll='showSelectAll' selectAllText="Select All" unSelectAllText="Unselect All"
                         v-model="selected_sites" @change="select_website"></ejs-multiselect>
    </div>
</template>

<script>
    export default {
        name: "Websites",
        props: {
            display_all: {
                default: true,
                type: Boolean
            },
            display_global: {
                default: false,
                type: Boolean
            },
            filter: {
                default: null,
                type: String
            }
        },
        data() {
          return {
              fields: { text: "website_name", value: "website_id" },
              site_id: '',
              websites: [],
              selected_sites: [],
              showSelectAll: false,
          }
        },
        mounted() {
            this.get_websites();
            if(this.display_all) {
                this.showSelectAll = true;
            }
        },
        methods: {
            get_websites: function() {
                this.$http.get('/api/website/user_websites').then(res => {
                    if (res.body) {
                        this.websites = Object.keys(res.body).map(function(key) {
                            return {
                                'website_name': res.body[key]['website_name'],
                                'website_id': res.body[key]['website_id']
                            }
                        });
                        if(this.display_global) {
                            this.websites.unshift({'website_id': -1, 'website_name': 'Global'});
                        }
                    } else {
                        console.log("---------ERROR-----------");
                    }
                });
            },
            select_website: function() {
                this.site_id = [];
                if (this.selected_sites.length === this.websites.length) {
                    this.site_id = [{'website_id': 'all', 'website_name': 'all'}];
                } else {
                    this.selected_sites.forEach(selection => {
                        this.websites.forEach(website => {
                            if (website['website_id'] === selection) {
                                this.site_id.push(website);
                            }
                        })
                    });
                }
                this.$emit('selectWebsite', this.site_id);
            }
        },
        computed: {
            sites() {
                let sites = this.websites;

                if (this.filter) {
                    const filter = JSON.parse(this.filter);
                    sites = sites.filter(i => filter.indexOf(i.website_id) !== -1);
                }

                return sites;
            }
        }
    }
</script>

<style scoped>
@import "../../assets/styles/syncfusion/material.css";

label {
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
    text-align: left;
    box-sizing: inherit;
    background-repeat: no-repeat;
    display: inline-block;
    touch-action: manipulation;
    font: inherit;
    vertical-align: baseline;
    font-size: 16px;
    min-height: 8px;
    transition: .3s cubic-bezier(.25,.8,.5,1);
    overflow: hidden;
    text-overflow: ellipsis;
    transform-origin: top left;
    white-space: nowrap;
    pointer-events: none;
    max-width: 133%;
    transform: translateY(-18px) scale(.75);
    height: 20px;
    line-height: 20px;
    color: rgba(0,0,0,.54);
    position: absolute;
    margin-top: 4px;
}
</style>