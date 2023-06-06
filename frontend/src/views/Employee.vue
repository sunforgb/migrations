<template>
    <v-container fluid>
        <RegrStatements v-if="logged_in"></RegrStatements>
        <UnRegrStatements v-if="logged_in"></UnRegrStatements>
    </v-container>
</template>
<script>
import axios from 'axios';
import RegrStatements from '../components/RegrStatements.vue';
import UnRegrStatements from '../components/UnRegrStatements.vue';
export default {
    name: "EmployeeView",
    components: {
        RegrStatements,
        UnRegrStatements
    },
    data () {
        return {
            type: "",
            logged_in: false,
            email: ""
        }
    },
    beforeCreate() {
        this.type = this.$store.state.user_type;
        if (this.$store.getters.getAccessToken){
            axios.get('/api/users/me/').then((response) => {
                if (response.data.email){
                    this.logged_in = true
                    this.email = response.data.email
                }
            }).catch(error => {
                this.logged_in = false
                console.log("Not authorized");
                console.log(error);
            })
        }
    }
}
</script>