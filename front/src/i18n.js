import { createI18n } from 'vue-i18n'
import EN from './locale/en.json'
import ES from './locale/es.json'
import FR from './locale/fr.json'
import DE from './locale/de.json'
import IT from './locale/it.json'
import MA from './locale/mando\'a.json'

const i18n = createI18n({
    locale: 'EN',
    messages: {
        EN: EN,
        ES: ES,
        FR: FR,
        MA: MA,
        DE: DE,
        IT: IT,
    }
})

export default i18n;
