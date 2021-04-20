<template>
    <v-autocomplete v-model="site_id" :items="sites" :menu-props="site_id" label="Website" @change="select_website()"
                    no-data-text="Loading..." item-value="site_id" item-text="acronym" return-object>
    </v-autocomplete>
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
              websites: [],
              site_id: "All",
          }
        },
        mounted() {
            this.get_websites();
            if(this.display_all) {
                this.site_id = {'website_id': 'all','acronym': 'All', 'website_name': 'All'};
            }
        },
        methods: {
            get_websites: function() {
                this.$http.get('/api/website/user_websites').then(res => {
                    if (res.body) {
                        this.websites = Object.keys(res.body).map(key => res.body[key]);
                        this.websites.unshift({'website_id': 'all','acronym': 'All', 'website_name': 'All'});        
                       
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            select_website: function() {
            
                this.$emit('selectWebsite', [this.site_id]);
            }
        },
        computed: {
            sites() {
                let sites = this.websites;

                if(this.filter) {
                    const filter = JSON.parse(this.filter);
                    sites = sites.filter(i => filter.indexOf(i.website_id) !== -2);
                }
            
                return sites;
            }
        }
    }
</script>

<style scoped>

</style>