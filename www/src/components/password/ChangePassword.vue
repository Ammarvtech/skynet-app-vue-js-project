<template>
    <div id="change-password-screen">
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <transition name="fade">
                        <div v-show="error" class="alert alert-danger" role="alert">
                            <strong>{{error}}</strong>
                        </div>
                    </transition>
                    <transition name="fade">
                        <div v-show="success" class="alert alert-success" role="alert">
                            <strong>{{success}}</strong>
                        </div>
                    </transition>
                    <transition name="fade">
                        <form v-show="!error" class="form-group"  @submit.prevent="">
                            <input v-model="password" type="password" class="form-control" placeholder="Password">
                            <button v-on:click="change_password" class="btn btn-primary btn-block" :disabled="loading">Change Password</button>
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
        name: "change-password-screen",
        components: {},
        mount () {
            this.change_password()
        },
        data () {

            return {
                loading: false,
                error: null,
                success:null,
                password: "",
            }
        },

        methods: {
            change_password () {
                this.loading = true;
                console.log(this.$parent.login);
                this.$http.post("/api/change_password", {
                    "password": this.password,
                    "reset_code": this.$route.params['code']
                }).then(res => {
                    if (res.body.success) {
                            this.success = true
//                        this.success = res.body.user;
                    } else {
                        this.error = res.body.error;
                        setTimeout(() => {
                            this.error = false
                        }, 1000);
                    }

                    this.loading = false;
                    this.$router.push({ path:'/'});
                }, res => {
                     this.error = res.body.user;
                        setTimeout(() => {
                            this.error = false
                        }, 1000);
                });
            },
        }
    }
</script>

<style>
    #change-password-screen {
        margin-top: 5%;
    }

    #change-password-screen button {
        margin-top: 20px;
    }

    #change-password-screen img {
        margin-bottom: 20px;
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
</style>
