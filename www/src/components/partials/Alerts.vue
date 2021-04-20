<template>
    <div id="alerts">
        <div style="padding-bottom: 20px">
            <v-alert :value="true" type="error" outline>{{this.$store.state.alert}}</v-alert>
        </div>
    </div>
</template>

<script>
    export default {
        name: "alerts",
    }
</script>

<style scoped>

</style>