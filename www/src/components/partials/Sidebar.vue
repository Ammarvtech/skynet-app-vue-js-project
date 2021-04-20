<template>
    <div id="sidebar">
        <el-radio-group v-model="isCollapse" class="toggle-menu" style="margin: 23px 0">
            <el-radio-button :label="!isCollapse"><i class="toggle-menu fa fa-bars"></i></el-radio-button>
        </el-radio-group>
        <el-menu
                text-color="#fff"
                active-text-color="#ffd04b"
                :router="true"
                :default-active="$route.path"
                class="el-menu-vertical"
                @open="handleOpen"
                @close="handleOpen"
                :collapse="isCollapse">
            <el-menu-item :index="$route.path" id="cur-user" style="background: none">
                <i class="fw-icon fa-user-circle-o"></i>
                <span slot="title">{{ username }}</span>
                <a id="logout" v-show="!isCollapse" v-on:click="logout"></a>
            </el-menu-item>
            <!--<el-menu-item index="/realtime">-->
            <!--<i class="fw-icon fa-sellsy"></i>-->
            <!--<span slot="title">-->
            <!--Real Time-->
            <!--</span>-->
            <!--</el-menu-item>-->
            <el-menu-item index="/revenue">
                <i class="fw-icon fa-usd padding"></i>
                <span slot="title">
                    Revenue Report
                </span>
            </el-menu-item>
            <el-menu-item index="/websites-dfp">
                <i class="fw-icon fa-globe"></i>
                <span slot="title">
                    Websites - DFP
                </span>
            </el-menu-item>
            <el-menu-item index="/websites-rt">
                <i class="fw-icon fa-signal"></i>
                <span slot="title">
                    Websites - RT
                </span>
            </el-menu-item>
            <!--<el-menu-item index="/tasks">-->
            <!--<i class="fw-icon fa-tasks"></i>-->
            <!--<span slot="title">-->
            <!--Task Manager-->
            <!--</span>-->
            <!--</el-menu-item>-->
            <el-menu-item index="/dealer">
                <i class="fw-icon fa-cube"></i>
                <span slot="title">
                  Dealer Status
                </span>
            </el-menu-item>
            <el-menu-item index="/action-log">
                <i class="fas fa-file-medical-alt" style="top:15px;left:18px;padding-right:12px"></i>
                <span slot="title">
                  Action Log
                </span>
            </el-menu-item>
            <el-menu-item index="/ReportDynamic" v-if="this.$store.state.user.role === 'admin'">
                <i class="fw-icon fa-area-chart"></i>
                <span slot="title">
                    ReportDynamic
                </span>
            </el-menu-item>
            <el-menu-item index="/AutomationManagment" v-if="show_auto_management">
                <!-- <i class="fw-icon fa-area-chart padding"></i> -->
                <i class="fab fa-adn" style="font-size: 21px;"></i>
                <span slot="title" style="font-size:12px;">
                    Automation Management
                </span>
            </el-menu-item>
            <!--<el-menu-item index="/campaigns">-->
            <!--<i class="fw-icon fa-bar-chart"></i>-->
            <!--<span slot="title">-->
            <!--Campaigns Manager-->
            <!--</span>-->
            <!--</el-menu-item>-->
            <!--<el-menu-item index="/broker">-->
            <!--<i class="fw-icon fa-clock-o"></i>-->
            <!--<span slot="title">-->
            <!--Broker-->
            <!--</span>-->
            <!--</el-menu-item>-->
            <!--<el-menu-item index="/optimization">-->
            <!--<i class="fw-icon fa-line-chart"></i>-->
            <!--<span slot="title">-->
            <!--Automation Rules-->
            <!--</span>-->
            <!--</el-menu-item>-->
            <el-menu-item index="/validation">
                <i class="fw-icon fa-check"></i>
                <span slot="title">
                    Skynet Validation
                </span>
            </el-menu-item>
            <el-menu-item index="/site-configuration"
                          v-if="this.$store.state.user.role === 'admin'">
                <i class="fw-icon fa-sliders-h"></i>
                <span slot="title">
                    Site Configuration
                </span>
            </el-menu-item>


            <el-submenu :index="$route.path" title="Settings" v-if="this.$store.state.user.role === 'admin'">
                <template slot="title">
                    <i class="fw-icon fa-cogs"></i>
                    <span slot="title">Settings</span>
                </template>
                <el-menu-item v-if="this.$store.state.user.role === 'admin'" index="/alerts">
                    <span class="white-label" slot="title">Alerts</span>
                </el-menu-item>
                <el-menu-item index="/settings">
                    <span class="white-label" slot="title">User</span>
                </el-menu-item>
                <el-menu-item index="/backstage">
                    <span slot="title">Backstage</span>
                </el-menu-item>
                <el-menu-item index="/hb-settings">
                    <span slot="title">Bidder</span>
                </el-menu-item>
                <el-menu-item index="/campaigns/profiler">
                    <span slot="title">Duplicate Profiler</span>
                </el-menu-item>
                <el-menu-item v-if="this.$store.state.user.role === 'admin'" index="/factor">
                    <i class="fw-icon fa-line-chart"></i>
                    <span slot="title">Skynet Factor</span>
                </el-menu-item>
            </el-submenu>
        </el-menu>
    </div>
</template>

<script>

    export default {
        components: {
            "navigation-header": require("../partials/NavigationHeader.vue")
        },
        props: ["username"],
        data() {
            return {
                isCollapse: true,
                settings_seen: false,
                campaigns_seen: false,
                loading: false,
                show_auto_management: this.$store.getters.getUser.settings && this.$store.getters.getUser.settings.auto_management == 1,
            };
        },
        methods: {
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            },
            logout() {
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

<style>
    .el-menu-vertical:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }

    .toggle-menu, .toggle-menu span {
        background: transparent;
        border: none !important;
        color: #FFF;
    }

    .fw-icon, .fab {
        color: #939da8;
        font: normal 16px fontawesome;
        top: 15px;
        left: 18px;
        padding-right: 8px;
    }

    header {
        position: relative;
        height: 80px;
        padding: 20px 0 0 15px;
        font-size: 16px;
        color: #fff;
        /*background: #1F262D;*/
    }

    #img {
        position: relative;
        display: inline-block;
        width: 36px;
        height: 36px;
        margin: 0 10px 0 0;
        vertical-align: middle;
        border: 1px solid #fff;
    }

    #logout:before {
        content: '\f08b';
        font: normal 20px fontawesome;
        top: 28px;
        right: 15px;
    }

    #cur-user {
        background-color: #fff;
        pointer-events: none;
    }

    #cur-user a {
        float: right;
        pointer-events: auto;
    }

    #cur-user span {
        color: #ffff;
        font-weight: bold;
    }

    div#sidebar, .el-menu {
        background: #2e363f;
    }

    .el-menu-item {
        border-top: 1px solid #37414b;
        border-bottom: 1px solid #1f262d;
    }

    .el-tooltip a {
        background: transparent;
        padding: 19px;
        position: relative;
        left: -20px;
    }

    .el-menu-item span a {
        color: #939da8;
        text-decoration: none;
    }

    .el-menu-item span a {
        color: #939da8;
    }

    #sidebar .is-active {
        background-color: #20a0ff;
        color: #ffffff;
        font-weight: bold;
    }

    #sidebar .is-active i {
        color: #ffffff !important;
    }

    .el-menu {
        border-right: none !important;
    }

    .padding {
        padding-left: 3px;
    }

    .white-label {
        color: white;
    }
</style>
