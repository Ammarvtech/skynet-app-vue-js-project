<template>
    <v-autocomplete v-model="selected_source" :items="sources" label="Source" @change="select_source()"
                    no-data-text="Loading..." cache-items></v-autocomplete>
</template>

<script>
    export default {
        name: "Sources",
        data() {
            return {
                selected_source: "All",
                sources: [],
            }
        },
        mounted() {
            this.get_source();
            this.select_source();
        },
        methods: {
            get_source: function () {
                let source = this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.wl_sources ? this.$store.getters.getUser.settings.wl_sources : '';
                if (source.indexOf(',') > -1) {
                    this.sources = eval(source);
                    for (let i in this.sources) {
                        this.sources[i] = (this.sources[i].charAt(0).toUpperCase() + this.sources[i].slice(1));
                    }
                    this.selected_source = this.sources[0];
                }
                else if (source !== '' && source !== 'all') {
                    this.sources.unshift(source.charAt(0).toUpperCase() + source.slice(1));
                    this.selected_source = source.charAt(0).toUpperCase() + source.slice(1);
                }
                else {
                    this.$http.get("/api/website/source").then(res => {
                        if (res.body) {
                            this.sources = Object.values(res.body).map(i => i.provider_name);
                            this.sources.unshift('All');

                            this.selected_source = this.sources[0];
                        }
                    });
                }
            },
            select_source: function() {
              this.$emit('selectSource', this.selected_source);
            },
        }
    }
</script>

<style scoped>

</style>