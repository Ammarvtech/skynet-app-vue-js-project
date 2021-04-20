<template>
    <header>
        <span></span>
        {{ username }}
        <a v-show="!loading" v-on:click="logout"></a>
    </header>
</template>

<script>
export default {
    name: "navigation-header",
    props: ["username"],
    data () {
        return {
            loading: false,
        }
    },

    methods: {
        logout () {
            this.$http.get("/api/logout").then(res => {
                this.$store.commit('removeLoginTime');
                this.loading = true;
                location.reload();
            }, res => {
                // TODO: handle server error
            });
        }
    }
}
</script>

<style scoped>
header {
    position: relative;
    height: 80px;
    padding: 20px 0 0 15px;
    font-size: 16px;
    color: #fff;
    background: #1F262D;
}

header span {
    position: relative;
    display: inline-block;
    width: 36px;
    height: 36px;
    margin: 0 10px 0 0;
    vertical-align: middle;
    border: 1px solid #fff;
}

header span:before {
    content: '\f007';
    font: normal 20px fontawesome;
    top: 7px;
    left: 9px;
}

header a:before {
    content: '\f08b';
    font: normal 20px fontawesome;
    top: 28px;
    right: 15px;
}
:before, :after {
    content: '';
    display: block;
    position: absolute;
}
</style>
