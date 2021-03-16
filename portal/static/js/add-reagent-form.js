const AddReagentForm = Vue.component('add-reagent-form', {
    props: {
        templates: Array,
        manufacturers: Array,
        lots: Array,
    },
    data: function () {
        return {
            template: null,
            manufacturer: null,
            lot: null,
            quantity: null,
            addLotURL: addLotURL,
        }
    },
    computed: {
        tempLots: function () {
            return this.template ?
                this.lots.filter(lot => lot.template_id === this.template) :
                [];
        },
        mfgWhere: function () {
            return this.tempLots.length ?
                this.manufacturers.filter(mfg => this.tempLots.find(lot => lot.mfg_id === mfg.id)) :
                [];
        },
        lotWhere: function () {
            return this.mfgWhere.length ?
                this.tempLots.filter(lot => lot.mfg_id === this.manufacturer) :
                [];
        },
        tempData: function () {
            return this.template ?
                this.templates.find(template => template.id === this.template) :
                {container_size: '', container_type: ''};
        }
    },
    methods: {
        submit: function () {
            const data = {
                lot_id: this.lot,
                quantity: +this.quantity
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
            this.template = [];
            this.manufacturer = null;
            this.lot = null;
            this.quantity = null;
        }
    },
    template: `
    <form id="add-reagent-form" class="qc-form has-background-white p-6" @submit.prevent="submit" @reset.prevent="clear">
        <fieldset>
            <legend class="subtitle has-text-primary-dark">Reagent Details</legend>
            <div class="field py-2">
                <label for="templateSelect" class="label has-text-primary-dark">Template</label>
                <div class="control">
                    <select id="templateSelect" size="8" class="textarea is-fullwidth" v-model="template" required>
                        <option v-for="temp in templates" :key="'t-' + temp.id" :value="temp.id">{{ temp.description }}</option>
                    </select>
                </div>
            </div>
            <div class="columns py-2">
                <div class="field column">
                    <label for="mfgSelect" class="label has-text-primary-dark">Manufacturer</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select id="mfgSelect" v-model="manufacturer" :disabled="!template" required>
                                <option disabled selected value="">Select Manufacturer</option>
                                <option v-for="mfg in mfgWhere" :key="'m-' + mfg.id" :value="mfg.id">{{ mfg.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="field column">
                    <label for="lotSelect" class="label has-text-primary-dark">Lot</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select id="lotSelect" v-model="lot" :disabled="!manufacturer" required>
                                <option disabled selected value="">Select Lot</option>
                                <option v-for="lot in lotWhere" :key="'l-' + lot.id" :value="lot.id">{{ lot.lot_num }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="columns">
                <div class="field column is-narrow">
                    <label for="quantityInput" class="label has-text-primary-dark">Quantity</label>
                    <div class="control">
                        <input id="quantityInput" v-model="quantity" class="input" :disabled="!lot" type="number" min="1" required>
                    </div>
                </div>
                <div>
                    <a class="button is-success is-light" :href="addLotURL">Add New Lot</a>
                </div>
            </div>
            <div class="field is-grouped columns is-centered py-4">
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
        'add-reagent-form': AddReagentForm
    }
})

