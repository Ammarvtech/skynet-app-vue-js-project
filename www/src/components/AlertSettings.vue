<template>
    <div id="alert_settings">
        <form>
            <v-text-field
                    v-validate="'max:200'"
                    v-model="alert"
                    :counter="200"
                    :error-messages="errors.collect('alert')"
                    label="Alert Text"
                    data-vv-name="alert"
            ></v-text-field>
            <v-btn color="info" @click="submit" :disabled="alert == ''">submit</v-btn>
            <v-btn color="warning" @click="clear" :disabled="alert == ''">clear text</v-btn>
            <v-btn v-show="this.$store.state.alert !=''" color="error" @click="submit(true)">delete current alert</v-btn>
        </form>
    </div>
</template>

<script>

    export default {
        $_veeValidate: {
            validator: 'new'
        },
        name: "AlertSettings",
        data: () => ({
            alert: '',
            dictionary: {
                custom: {
                    alert: {
                        required: () => 'Alert field can not be empty',
                        max: 'The name field may not be greater than 200 characters'
                    },
                }
            }
        }),

        methods: {
            submit(remove) {
                this.$validator.validateAll().then((result) => {
                    if (result || remove) {
                        this.$http.post('/api/setalert', {'alert': remove == true ? '' : this.alert}).then(res => {
                            if (res.body === "true") {
                                this.$message({message: 'Done, Please Refresh Your Page', center: true, type: 'success'});
                            } else {
                                this.$alert('Sorry, Error has occurred', ' ', {
                                    confirmButtonText: 'OK',
                                    type: 'warning'
                                });
                            }
                        });
                    }
                    return false;
                });
            },
            clear() {
                this.alert = '';
                this.$validator.reset()
            }
        }
    }
</script>

<style scoped>

</style>