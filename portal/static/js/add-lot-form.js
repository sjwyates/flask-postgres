const AddLotForm = Vue.component('add-lot-form', {
    props: {
        templates: Array,
        manufacturers: Array,
        lots: Array,
    },
    data: function () {
        return {
            template: null,
            manufacturer: null,
            lot_num: '',
            cofa: {
                name: '',
                path: '',
                display: '',
            },
        }
    },
    methods: {
        submit: function () {
            const data = {
                template_id: this.template,
                manufacturer_id: this.manufacturer,
                lot_num: this.lot_num
            }
            fetch('http://127.0.0.1:5000/reagents/add', {
                method: 'POST',
                redirect: 'follow',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
                .then(res => {
                    if (res.redirected) {
                        window.location.href = res.url;
                    }
                })
                .catch(err => console.error(err));
        },
        clear: function () {
            this.template = null;
            this.manufacturer = null;
            this.lot_num = null;
        },
        cofaChange: function (target) {
            let name = target.files[0].name;
            this.cofa.name = name;
            this.cofa.path = target.value;
            const max = target.clientWidth / 12;
            if (name.length > max) {
                const sliceSize = max / 2 - 5;
                console.log('slice: ' + sliceSize)
                name = name.slice(0, sliceSize) + ' ... ' + name.slice(-sliceSize);
            }
            this.cofa.display = name;
        }
    },
    template: `
    <form id="add-lot-form" class="qc-form has-background-white p-6" @submit.prevent="submit" @reset.prevent="clear">
        <fieldset class="qc-form__fieldset">
            <legend class="is-size-3 has-text-primary-dark pb-4">Lot Information</legend>
            <div class="field py-2">
                <label for="templateSelect" class="label has-text-primary-dark">Template</label>
                <div class="control">
                    <select id="templateSelect" name="template" size="8" class="textarea qc-form__field" v-model="template" required>
                        <option v-for="temp in templates" :key="'t-' + temp.id" :value="temp.id">{{ temp.description }}</option>
                    </select>
                </div>
            </div>
            <div class="field py-2">
                <label for="mfgSelect" class="label has-text-primary-dark">Manufacturer</label>
                <div class="control">
                    <div class="select qc-form__field">
                        <select id="mfgSelect" name="manufacturer" v-model="manufacturer" :disabled="!template" class="qc-form__field" required>
                            <option disabled selected value="">Select Manufacturer</option>
                            <option v-for="mfg in manufacturers" :key="'m-' + mfg.id" :value="mfg.id">{{ mfg.name }}</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field py-2">
                <label for="lotInput" class="label has-text-primary-dark">Lot Number</label>
                <div class="control">
                    <input type="text" class="input qc-form__field" v-model="lot_num" :disabled="!manufacturer" required>
                </div>
            </div>
            <div class="field py-2">
                <div id="cofaUploadLabel" class="label has-text-primary-dark">Certificate of Analysis</div>
                <label class="file has-name">
                    <div class="file-label qc-form__field qc-span">
                        <input
                            id="cofaUpload"
                            name="cofa"
                            class="file-input"
                            type="file"
                            accept="application/pdf"
                            @change="cofaChange($event.target)"
                            aria-labelledby="cofaUploadLabel">
                        <span class="file-cta">
                            <span class="file-label">
                                Choose a file…
                            </span>
                        </span>
                        <span class="file-name qc-span__parent">
                            <div ref="fileNameDisplay" class="qc-span__child--text has-text-black">
                                {{ cofa.name }}
                            </div>
                            <div class="qc-span__child--spacer"></div>
                        </span>
                    </div>
                </label>
            </div>
            <div class="field qc-form__field is-grouped columns is-centered py-4">
                <div class="control column is-narrow">
                    <button type="submit" class="button is-primary">Submit</button>
                </div>
                <div class="control column is-narrow">
                    <button type="reset" class="button is-grey is-light">Cancel</button>
                </div>
            </div>
        </fieldset>
    </form>
    `
})

const vm = new Vue({
    el: '#v-add',
    data: data,
    components: {
        'add-lot-form': AddLotForm
    }
})

