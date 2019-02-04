import 'bootstrap';

import Vue from 'vue';
import App from './app.vue';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { store } from './store';
import { router } from './router';
import { i18n } from './i18n';
import './scss/main.scss';

import { faUser } from '@fortawesome/free-solid-svg-icons'

Vue.use(require('vue-cookies'));
Vue.component('navbar', require('./components/navbar.vue').default);
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('cities-input', require('./components/cities.vue').default)
Vue.component('profession-input', require('./components/professions.vue').default)

library.add(faUser);

var app = new Vue({
    el: '#app',
    store,
    router,
    i18n,
    render: h => h(App)
}).$mount('#apps');
