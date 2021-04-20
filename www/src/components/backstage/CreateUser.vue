<template>
    <div id="create-user-screen">
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <transition name="fade">
                        <div v-show="error" class="alert alert-danger" role="alert">
                            <strong>Error:</strong> Username Already In DB
                        </div>
                    </transition>
                    <transition name="fade">

                        <form v-show="!error" class="form-group">
                            <span>Selected Role: {{ selected_role }}</span>
                            <select class="form-control" v-model="selected_role">
                                <option v-for="(role, role_name) in roles" :value="role_name">
                                    {{role_name.charAt(0).toUpperCase() + role_name.slice(1)}}
                                </option>
                            </select>
                            <input v-model="username" type="text" class="form-control" placeholder="Username">
                            <input v-model="password" type="password" class="form-control" placeholder="Password">
                            <input v-model="email" type="text" class="form-control" placeholder="Email">
                            <button v-on:click="create_user" class="btn btn-primary btn-block" :disabled="loading">
                                Create
                            </button>
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
        name: "create-user-screen",
        components: {},
        mounted() {
            this.get_roles();
        },
        data() {
            return {
                loading: false,
                error: null,
                username: "",
                email: "",
                password: "",
                selected_role: "user",
                roles:[]
            }
        },

        methods: {
            get_roles: function () {
                this.$http.get("/api/role").then(res => {
                    if (res.body) {
                        console.log(res.body);
                        this.roles = res.body;
                    } else {
                        console.log("---------ERROR-----------");
                        this.error = true;
                    }
                });
            },
            create_user() {
                this.loading = true;
                this.$http.post("/api/create_user", {
                    "username": this.username,
                    "role": this.selected_role,
                    "password": this.password,
                    "email": this.email
                }).then(res => {
                    if (res.body.success) {
                    } else {
                        this.error = true;
                        setTimeout(() => {
                            this.error = false
                        }, 2000);
                    }

                    this.loading = false;
                }, res => {
                    // TODO: handle error
                });
            }
        }
    }
</script>

<style>
    #login-screen {
        margin-top: 5%;
    }

    #login-screen button {
        margin-top: 20px;
    }

    #login-screen img {
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
