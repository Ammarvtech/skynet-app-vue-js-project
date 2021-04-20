<template>
    <div id="feed-container">
        <div id="feed-button">
            <el-button v-show="!show" type="primary" icon="el-icon-tickets" @click="show = !show" style="border-radius: 0; width: 64px;">
                <span>({{logs.length}})</span>
            </el-button>
        </div>
        <transition name="el-zoom-in-bottom">
            <div v-show="show" id="feed-box">
                <div id="title-bar">
                    <i class="el-icon-close" @click="show = !show"></i>
                    <h4 style="float: right">Feed</h4>
                </div>
                <div id="feed">
                    <div v-for="log in logs" class="log">
                        <el-alert :title="log.toString()" type="info"></el-alert>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.popLogInterval();
        },
        data() {
            return {
                show: false,
                logs: this.$store.getters.getLogs
            }
        },
        methods: {
            popLogInterval() {
                let self = this;
                setInterval(function () {
                    self.$store.commit('popLog');
                }, 20000)
            }
        },
        computed: {}
    }
</script>

<style scoped>
    i:hover {
        cursor: pointer;
    }

    #feed-container {
        display: none;
        bottom: 0;
        position: fixed;
        z-index: 9999;
    }

    #feed-box {
        width: 15vw;
        height: 30vh;
        box-shadow: 0 1px 4px rgba(0, 0, 0, .3);
        background-color: #FFF;
        overflow-y: auto;
    }

    #title-bar {
        background-color: #ddd;
        padding: 5px;
        position: fixed;
        width: inherit;
    }

    .log {
        padding: 5px;
    }

    #feed {
        padding-top: 25px;
    }

    #feed-button {
        position: absolute;
        left: 0;
        bottom: 0;
    }

</style>