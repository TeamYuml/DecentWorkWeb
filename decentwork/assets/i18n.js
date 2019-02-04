import Vue from 'vue';
import VueI18n from 'vue-i18n';

Vue.use(VueI18n);

const messages = {
    en: {
        // Translations in navbar component.
        navbar: {
            workers: 'Workers',
            notices: 'Notices',
            addNotice: 'Add notice',
            myProfile: 'My profile',
            changePassword: 'Change password',
            myNotices: 'My notices',
            logout: 'Logout',
            login: 'Login',
        },
    },
    pl: {
        navbar: {
            workers: 'Pracownicy',
            notices: 'Ogłoszenia',
            addNotice: 'Dodaj ogłoszenie',
            myProfile: 'Mój profil',
            changePassword: 'Zmień hasło',
            myNotices: 'Moje ogłoszenia',
            logout: 'Wyloguj',
            login: 'Zaloguj',
        },
    },
};

const i18n = new VueI18n({
    locale: navigator.language.split('-')[0],
    messages,
});


export { i18n };