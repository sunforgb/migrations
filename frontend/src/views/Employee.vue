<template>
    <v-container fluid>
        <RegrStatements></RegrStatements>
        <UnRegrStatements></UnRegrStatements>
    </v-container>
</template>
<script>
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
            type: ""
        }
    },
    beforeCreate() {
        this.type = this.$store.state.user_type;
    }
}
</script>