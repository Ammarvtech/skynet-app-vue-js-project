<template>
    <div id="app" class="wrapper" v-if="user">
        <!--<mobile-navigation-menu v-if="(wXS)"></mobile-navigation-menu>-->
        <navigation-menu :username="user"></navigation-menu>
        <main>
            <alert v-if="alert">{{this.alert}}</alert>
            <v-app>
                <router-view @validateUser="validateUser" @logout="logout"></router-view>
            </v-app>
        </main>
    </div>
    <reset-password-screen v-else-if="resetPass"></reset-password-screen>
    <change-password-screen v-else-if="changePass"></change-password-screen>
    <login-screen v-else-if="login"></login-screen>
</template>

<script>

    export default {
        name: 'app',
        components: {
            "notification-feed": require("./components/partials/NotificationFeed.vue").default,
            "navigation-menu": require("./components/partials/Sidebar.vue").default,
            "login-screen": require("./components/Login.vue").default,
            "reset-password-screen": require("./components/password/ResetPassword.vue").default,
            "change-password-screen": require("./components/password/ChangePassword.vue").default,
            "mobile-navigation-menu": require("./components/partials/MobileBar.vue").default,
            "alert": require("./components/partials/Alerts.vue").default
        },
        mounted() {
            // Set Store Global Socket
            this.getUser();
            this.setValidationTimer();
        },
        destroyed() {
            clearTimeout(this.validationTimer);
        },
        data() {
            return {
                user: false,
                login: false,
                error: null,
                alert: false,
                validationTimer: null,
                validationFlag: false,
            }
        },
        computed: {
            resetPass: function () {
                return this.$route.path.indexOf('/password/reset') == 0;
            },
            changePass: function () {
                return this.$route.path.indexOf('/password/change') == 0;
            },
            userMsg: function () {
                return this.$store.getters.getUserMessage;
            },
            dealerMsg: function () {
                return this.$store.getters.getDealerMessage;
            }
        },
        watch: {
            dealerMsg: {
                handler(newMsg, oldMsg) {
                    let statusType = {
                        'PENDING': 'info',
                        'STAGED': 'info',
                        'IN_PROCESS': 'info',
                        'DONE': 'success',
                        'ERROR': 'error',
                        'RETRY': 'warning'
                    };
                    let types = statusType[newMsg['status']['value']];
                    if (types === 'info') {
                        console.log('dealer info msg');
                    } else {
                        this.$notify({
                            title: newMsg['params']['campaign_id'],
                            message: newMsg['status']['value'],
                            type: types,
                            position: 'bottom-right'
                        });

                        // let log = `${newMsg['params']['campaign_id']}-${newMsg['status']['value']}`;
                        // this.$store.commit('setLog', log)
                    }
                }
            },
            userMsg: {
                handler(newMsg, oldMsg) {
                    this.$store.commit('setLog', newMsg)
                }
            }
        },
        methods: {
            setValidationTimer() {
                this.validationFlag = false;
                this.validationTimer = setTimeout(this.setValidationFlag, 5 * 60 * 1000);
            },
            setValidationFlag() {
                this.validationFlag = true;
            },
            resetValidationTimer() {
                clearTimeout(this.validationTimer);
                this.setValidationTimer();
            },
            validateUser() {
                if (!this.validationFlag)
                    return;
                let params = {
                    'login_time': this.$store.getters.getUser.loginTime,
                };
                this.$http.post('/api/website/validate', {params: params}).then(res => {
                    if (!res.body || !res.body['allowed_access']) {
                        this.logout();
                    }
                    else {
                        this.resetValidationTimer();
                    }
                }).catch(e => {
                    console.log(e);
                    this.logout();
                });
            },
            logout() {
                this.$http.get("/api/logout").then(() => {
                    this.$store.commit('removeLoginTime');
                    location.reload();
                }, err => {
                    console.log(err);
                });
            },
            getUser() {
                if (this.login) {
                    console.log("user authenticated" + this.login);
                } else {
                    this.$http.get("/api/me").then(res => {
                        if (res.body.user === null) {
                            this.user = false;
                            this.login = true;
                        } else {
                            this.login = false;
                            this.user = res.body.user.username;
                            this.$store.commit('setUser', res.body.user);
                            this.$store.commit('setLogin', true);
                            // this.$store.commit('setSocket', this.$socket);
                            // this.$store.dispatch('socket_identify')
                        }
                    }, res => {
                        // TODO: Handle server error
                        this.error = true;
                        this.login = true;
                    });

                    const that = this;
                    this.check_alert();
                    this.get_currency();
                    setInterval(function(){ that.check_alert(); }, 600000);
                }
            },
            check_alert() {
                this.$http.get("/api/alert").then(res => {
                    if (res.bodyText === "") {
                        this.alert = false;
                    } else {
                        this.$store.commit('setAlert', res.bodyText);
                        this.alert = true;
                    }
                });
            },
            get_currency() {
                this.$http.get("/api/currency").then(res => {
                    if (res.bodyText !== "") {
                        this.$store.commit('setCurrency', parseFloat(res.bodyText));
                    }
                });
            },

        }
    }
</script>

<style lang="scss">
    @import "assets/styles/_main.scss";
</style>
