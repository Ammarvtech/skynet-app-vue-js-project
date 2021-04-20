<template>
    <div>
        <div class="col-xs-2">
            <v-text-field label="Search" @input="check_empty" v-on:keyup="enterPressed" v-model="search"
                          @click:clear="clearSearch" clearable :loading="loading"></v-text-field>
        </div>
        <div class="search col-xs-1">
            <v-btn outline small fab color="primary" @click="applyFilter" :disabled="!search || search === ''">
                <v-icon>search</v-icon>
            </v-btn>
        </div>
    </div>
</template>

<script>
    export default {
        name: "SearchBox",
        data() {
            return {
                search: '',
                loading: false
            }
        },
        mounted() {
        },
        methods: {
            check_empty() {
                if (this.search === '' || !this.search) {
                    this.$emit('selectFilter', '');
                }
            },
            clearSearch() {
                this.$emit('selectFilter', '');
            },
            enterPressed(e) {
                if (e.keyCode === 13) {
                    this.applyFilter();
                }
            },
            applyFilter() {
                if (!this.filter) {
                    this.loading = true;
                }
                this.edit_index = null;
                setTimeout(() => {
                    this.search = this.search.trim().toLowerCase();
                    this.$emit('selectFilter', this.search);
                    this.loading = false;
                }, 500);
            },
        }
    }
</script>

<style scoped>

</style>