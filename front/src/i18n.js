import { createI18n } from 'vue-i18n'
import EN from './locale/en.json'
import ES from './locale/es.json'
import FR from './locale/fr.json'
import MA from './locale/mando\'a.json'

const i18n = createI18n({
    locale: 'ES',
    messages: {
        EN: EN,
        ES: ES,
        FR: FR,
        MA: MA,
    }
})

export default i18n;
