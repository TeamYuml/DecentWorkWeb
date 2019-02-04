<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12 notice">
                <h1>{{ $t("messages.addNotice") }}</h1>
                <form @submit.prevent>
                    <button class="primaryAction" type="submit" @click="addNotice" name="action">Dodaj ogłoszenie</button>
                    <br>
                    <label for="title">Tytuł</label>
                    <br>
                    <input class="input_data" type="text" id="title" required v-model.trim="title"
                        placeholder="Podaj tytuł ogłoszenia(Wymagane)" autocomplete="off">

                    <cities-input />

                    <profession-input />

                    <br>
                    <label>Opis</label>
                    <br>
                    <textarea placeholder="Opis ogłoszenia" v-model.trim="description"></textarea>
                    <br>
                </form>

                <p>{{ status }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { mapState, mapGetters } from 'vuex'
import { not, required, sameAs, minLength } from 'vuelidate/lib/validators'

export default {
    data () {
        return {
            title: '',
            description: '',
            status: '',
            STATUS_TEXTS: {
                ADDED: 'Ogłoszenie dodane',
                AUTH_ERROR: 'Błąd autoryzacji',
                WRONG_DATA_ERROR: 'Wprowadzone dane są nie poprawne',
                SOMETHING_WRONG: 'Coś poszło nie tak',
            }
        }
    },
    computed: {
        ...mapState({
            choosenCity: state => state.choosenCity,
            choosenProfession: state => state.choosenProfession,
        }),
        ...mapGetters([
            'axiosConfig',
        ])
    },
    methods: {
        addNotice () {
            if (!this.$v.$invalid) {
                let params = {
                    'title': this.title,
                    'description': this.description,
                    'city': this.choosenCity,
                    'profession': this.choosenProfession
                }

                axios.post('/notices/notices/', params, this.axiosConfig)
                    .then((response) => this.status = this.STATUS_TEXTS.ADDED)
                    .catch((error) => {
                        if (error.response.status === 401) {
                            this.status = this.STATUS_TEXTS.AUTH_ERROR
                        } else if (error.response.status === 400) {
                            this.status = this.STATUS_TEXTS.WRONG_DATA_ERROR
                        } else {
                            this.status = this.STATUS_TEXTS.SOMETHING_WRONG
                        }
                    })
            }
        }
    },
    validations: {
        title: {
            required
        },
        choosenCity: {
            required
        }
    }
}
</script>