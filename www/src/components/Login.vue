<template>
    <div v-else-if="true" id="login-screen">
        <vue-headful title="Login"/>
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <img class="mx-auto d-block center-block" src="../assets/story-logo.png"/>
                    <transition name="fade">
                        <div v-show="error" class="alert alert-danger" role="alert">
                            <strong>Error:</strong> Wrong username or password...
                        </div>
                    </transition>
                    <transition name="fade">
                        <form v-show="!error" class="form-group" @submit.prevent="">
                            <v-text-field label="Username" v-model="username" placeholder=" " append-icon="perm_identity"></v-text-field>
                            <v-text-field
                                    style="text-decoration: underline; !important;"
                                    v-model="password"
                                    :append-icon="show_pass ? 'visibility_off' : 'visibility'"
                                    :type="show_pass ? 'text' : 'password'"
                                    label="Password"
                                    placeholder=" "
                                    @click:append="show_pass = !show_pass"
                            ></v-text-field>
                            <v-btn v-on:click="login" color="info" class="btn-primary btn-block" :disabled="loading">Login</v-btn>
                            <p id="reset-link" class="text-center">
                                <router-link to="/password/reset">Reset Password</router-link>
                            </p>
                        </form>
                    </transition>
                </div>
                <div class="col"></div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login-screen",
        components: {},
        data() {
            return {
                show_pass: false,
                loading: false,
                error: null,
                username: "",
                password: ""
            }
        },
        methods: {
            login() {
                event.preventDefault();
                this.loading = true;
                // console.log(this.$parent.login);
                this.$http.post("/api/login", {
                    "username": this.username,
                    "password": this.password
                }).then(res => {
                    if (res.body.success) {
                        this.$parent.user = res.body.user.username;
                        this.$parent.login = false;
                        this.$store.commit('setLoginTime');
                        this.$store.commit('setUser', res.body.user);
                        this.$store.commit('setLogin', true);
                        // this.$store.commit('setSocket', this.$socket);
                        // this.$store.dispatch('socket_identify')

                    } else {
                        this.error = true;
                        setTimeout(() => {
                            this.error = false;
                        }, 2000);
                    }

                    this.loading = false;
                }, res => {
                    this.loading = false;
                });
            }
        }
    }
</script>

<style scoped>
    #login-screen {
        padding-top: 200px;
        background-color: white;
        color: white;
    }

    #reset-link {
        margin-top: 5%;
        color: #2196f3;
    }

    #login-screen button {
        margin-left: 0;
    }

    #login-screen img {
        margin-bottom: 20px;
        width: 200px;
    }

    .fade-enter-active {
        transition: opacity .5s
    }

    .fade-enter, .fade-leave-to {
        opacity: 0
    }

    .container {
        max-width: 300px;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover
    textarea:-webkit-autofill:focus,
    select:-webkit-autofill,
    select:-webkit-autofill:hover,
    select:-webkit-autofill:focus {
        border: 1px solid white;
        -webkit-text-fill-color: black;
        -webkit-box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0) inset;
        transition: background-color 5000s ease-in-out 0s;
    }

    .theme--light.v-btn {
        background-color: #2196f3 !important;
        border-color: #2196f3 !important;
    }

    .v-input--is-focused{
        text-decoration: underline !important;
    }
</style>
