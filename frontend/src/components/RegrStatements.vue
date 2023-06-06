<template>
    <v-container fluid>
        <v-row align="center" class="list px-3 mx-auto">
            <v-col cols="12" sm="12">
                <v-card class="mx-auto">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" sm="6" md="4">
                                <span>Заявки на регистрацию по месту жительства</span>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                                <v-btn :disabled="analyst" color="blue-darken-1" variant="text" @click="createReport">Сформировать отчет</v-btn>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-card-text>
                        <v-data-table-server
                            v-model:items-per-page="optionStatements['itemsPerPage']"
                            :headers = "headersStatementsMap"
                            :loading="loadingStatements"
                            :items = "statements"
                            hide-default-footer
                            show-expand
                            :items-length="totalItemsStatements"
                            @update:options="optionStatements= $event"
                        >
                        <template v-slot:item.approve="{ item }">
                            <v-btn v-if="(item.raw.status != 'approved')&&(item.raw.status != 'declined')" color="success" size="small" outlined class="me-2" @click="updateAppRegStatus(item.raw)">
                                Одобрить
                            </v-btn>
                        </template>
                        <template v-slot:item.decline="{ item }">
                            <v-btn v-if="(item.raw.status != 'approved')&&(item.raw.status != 'declined')" color="red" size="small" outlined class="me-2" @click="updateDecRegStatus(item.raw)">
                                Отклонить
                            </v-btn>
                        </template>
                        <template v-slot:bottom>
                                <v-row cols="12" justify="end" align="end">
                                    <v-col cols="7">
                                        <v-spacer></v-spacer>
                                    </v-col>
                                    <v-col align-self="end" cols="1">
                                        <span>Items per page</span>
                                    </v-col>
                                    <v-col cols="1" align-self="end">
                                        <v-select hide-details density="compact" v-model="optionStatements['itemsPerPage']" :items="pageSizesStatements">
                                        </v-select>
                                    </v-col>
                                    <v-col cols="3" align-self="end">
                                        <v-pagination variant="outlined" total-visible="6" density="compact" v-model="optionStatements['page']" :length="totalPagesStatements">   
                                        </v-pagination>
                                    </v-col>
                                </v-row>
                            </template>
                        </v-data-table-server>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from 'axios'

export default {
    name: "RegrStatements",
    data () {
        return {
            optionStatements: {
                'itemsPerPage': 5,
                'page': 1,
            },
            dialogStatement: false,
            loadingStatements: true,
            statements: [],
            headersStatementsMap: [
                {title: 'id', key: 'id'},
                {title: 'Адрес департамента', key: 'department.address'},
                {title: 'Телефон департамента', key: 'department.contact.number'},
                {title: 'Почтовый индекс', key: 'department.post_index'},
                {title: 'ФИО', key: 'person.name'},
                {title: 'Адрес проживания', key: 'person.address'},
                {title: 'Дата рождения', key: 'person.birthday'},
                {title: 'Страна рождения', key: 'person.birthday_place'},
                {title: 'Гражданство', key: 'person.citizenship.name'},
                {title: 'Профессия', key: 'person.profession'},
                {title: 'Контактный номер', key: 'person.contact.number'},
                {title: 'Серия и номер', key: 'person.document.serial_number'},
                {title: 'Выдан', key: 'person.document.issued_by'},
                {title: 'Когда выдан', key: 'person.document.issued_when'},
                {title: 'Выдан до', key: 'person.document.expires_when'},
                {title: 'Статус гражданина', key: 'person.status'},
                {title: 'Дата подачи', key: 'date'},
                {title: 'Текущий статус', key: 'status'},
                {title: "Одобрить", key: "approve"},
                {title: "Отклонить", key: "decline"},
            ],
            totalPagesStatements: 0,
            pageSizesStatements: [1,2,5,10,20],
            totalItemsStatements: 0,
            analyst: false
        }
    },
    beforeCreate() {
        if (this.$store.state.user_type == "analyst"){
            this.analyst = true
        }
    },
    methods: {
        getParamsStatements() {
            let params = {
                'limit': this.optionStatements.itemsPerPage,
                'offset': (this.optionStatements.page -1) * this.optionStatements.itemsPerPage
            }
            return params
        },
        retrieveDataStaements(params) {
            axios.get('/api/statements/', {params: params}).then(response => {
                this.statements = []
                response.data.results.forEach(element => {
                    this.statements.push(element)
                })
                this.totalPagesStatements = Math.floor(response.data.count / this.optionStatements['itemsPerPage'])+1;
                this.totalItemsStatements = response.data.count;
                if (response.data.count <= (this.optionStatements['itemsPerPage'] * (this.totalPagesStatements - 1))){
                    this.totalPagesStatements = this.totalPagesStatements - 1
                }
            }).catch(() => {
                console.log('not authorized')
            })
        },
        loadItemsStatements(){
            this.loadingStatements = true;
            this.retrieveDataStaements(this.getParamsStatements());
            this.loadingStatements = false;
        },
        createReport(){
            axios.get('/api/reportRegStatements').then(response => {
                console.log(response)
            }).catch(error => {
                console.log(error)
            })
        },
        updateAppRegStatus(item) {
            console.log(item)
            axios.patch('/api/updateAppRegStatus/', {'id': item.id}).then(response => {
                console.log(response)
            }).catch(error => {
                console.log(error)
            })
            this.loadItemsStatements();
        },
        updateDecRegStatus(item) {
            console.log(item)
            axios.patch('/api/updateDecRegStatus/', {'id': item.id}).then(response => {
                console.log(response)
            }).catch(error => {
                console.log(error)
            })
            this.loadItemsStatements();
        },

    },
    mounted () {
        this.loadItemsStatements();
    },
    watch: {
        optionStatements: {
            handler() {
                this.loadingStatements = true;
                this.loadItemsStatements();
                this.loadingStatements = false;
            },
            deep: true
        }
    }
}
</script>