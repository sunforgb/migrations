<template>
    <v-dialog v-model="dialogLogin" scrollable max-width="800px">
        <template v-slot:activator="{ props }">
            <v-btn @click="dialogLogin=true" v-bind="props">
                Войти
            </v-btn>
        </template>
        <v-card>
            <v-card-title> Вход </v-card-title>
            <v-card-text>
                <v-container>
                    <v-form>
                        <label>Email</label>
                        <v-text-field background-color="white" name="username" v-model="email" single-line outlined>
                        </v-text-field>
                        <label>Password</label>
                        <v-text-field background-color="white" type="password" name="password" v-model="password" single-line outlined>
                        </v-text-field>
                    </v-form>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-btn color="blue darken-1" text @click="dialogLogin=false"> Отмена </v-btn>
                <v-btn color="success" text @click="submitLogin()"> Войти </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';
export default {
    name: 'LoginUser',
    data () {
        return {
            email: '',
            password: '',
            dialogLogin: false
        }
    },
    beforeCreate () {
        axios.defaults.baseURL = 'http://185.231.153.231:8000'
    },
    methods: {
        submitLogin() {
            console.log("login submit")
            const formData = {
                email: this.email,
                password: this.password
            }
            axios.post('/api/jwt/create/', formData).then((response) => {
                const access = response.data.access

                this.$store.commit('setAccess', access)
                axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getAccessToken
                this.$router.push('/')
                this.dialogLogin = false
                axios.get('/api/users/me/').then((response) => {
                    console.log(response.data)
                    const user_type = response.data.user_type
                    const email = response.data.email
                    this.$store.commit('setUserType', user_type)
                    this.$store.commit('setEmail', email)
                    location.reload()
                }).catch(error => {
                    console.log(error)
                })
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>