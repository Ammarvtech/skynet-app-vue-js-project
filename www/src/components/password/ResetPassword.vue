<template>
    <div id="reset-password-screen">
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <transition name="fade">
                        <div v-show="error" class="alert alert-danger" role="alert">
                            <strong>{{error}}</strong> Wrong username or password...
                        </div>
                    </transition>
                    <transition name="fade">
                        <div v-show="success" class="alert alert-success" role="alert">
                            <strong>{{success}}</strong>
                        </div>
                    </transition>
                    <transition name="fade">
                        <form v-show="!error" class="form-group"  @submit.prevent="">
                            <input v-model="username" type="text" class="form-control" placeholder="Username">
                            <input v-model="email" type="email" class="form-control" placeholder="Email">
                            <button v-on:click="reset_password" class="btn btn-primary btn-block" :disabled="loading">Reset Password</button>
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
        name: "reset-password-screen",
        components: {},

        data () {

            return {
                loading: false,
                error: null,
                success:null,
                username: "",
                email: ""
            }
        },

        methods: {
            reset_password () {
                event.preventDefault();
                this.loading = true;
                console.log(this.$parent.login);
                this.$http.post("/api/reset_password", {
                    "username": this.username,
                    "email": this.email
                }).then(res => {
                    if (res.body.success) {
                        this.success = res.body.success;
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
    #reset-password-screen {
        margin-top: 5%;
    }

    #reset-password-screen button {
        margin-top: 20px;
    }

    #reset-password-screen img {
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
