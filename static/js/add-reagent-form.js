const AddReagentForm = Vue.component('add-reagent-form', {
    props: {
        templates: Array,
        manufacturers: Array,
        lots: Array,
    },
    data: function () {
        return {
            template: [],
            manufacturer: null,
            lot: null,
            quantity: null
        }
    },
    computed: {
        tempLots: function () {
            return this.template.length ?
                this.lots.filter(lot => lot.template_id == this.template[0]) :
                [];
        },
        mfgWhere: function () {
            return this.tempLots.length ?
                this.manufacturers.filter(mfg => this.tempLots.find(lot => lot.mfg_id == mfg.id)) :
                [];
        },
        lotWhere: function () {
            return this.mfgWhere.length ?
                this.tempLots.filter(lot => lot.mfg_id == this.manufacturer) :
                [];
        },
        selectSize: function () {
            return this.templates.length > 8 ?
                8 :
                this.templates.length;
        },
        tempData: function () {
            return this.template.length ?
                this.templates.find(template => template.id == this.template[0]) :
                {container_size: '', container_type: ''};
        }
    },
    methods: {
        submit: async function () {
            const data = {
                lot_id: this.lot,
                quantity: +this.quantity
            }
            const res = await fetch('http://127.0.0.1:5000/reagents/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                redirect: 'follow',
                body: JSON.stringify(data)
            });
            console.log(res);
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
            <legend class="title has-text-primary-dark">Enter Details</legend>
            <div class="field py-2">
                <label for="templateSelect" class="label has-text-primary-dark">Template</label>
                <div class="control">
                    <div class="select is-multiple is-fullwidth"">
                        <select id="templateSelect" multiple :size="selectSize" class="qc-select__multi" v-model="template" required>
                            <option v-for="temp in templates" :key="'t-' + temp.id" :value="temp.id">{{ temp.description }}</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="columns py-2">
                <div class="field column">
                    <label for="mfgSelect" class="label has-text-primary-dark" :class="{'has-text-gray': template.length == 0}">Manufacturer</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select id="mfgSelect" v-model="manufacturer" :disabled="template.length == 0" required>
                                <option disabled selected value="">Select Manufacturer</option>
                                <option v-for="mfg in mfgWhere" :key="'m-' + mfg.id" :value="mfg.id">{{ mfg.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="field column">
                    <label for="lotSelect" class="label has-text-primary-dark" :class="{'has-text-gray': manufacturer == null}">Lot</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select id="lotSelect" v-model="lot" :disabled="manufacturer == null" required>
                                <option disabled selected value="">Select Lot</option>
                                <option v-for="lot in lotWhere" :key="'l-' + lot.id" :value="lot.id">{{ lot.lot_num }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="columns">
                <div class="field column is-narrow">
                    <label for="quantityInput" class="label has-text-primary-dark" :class="{'has-text-gray': lot == null}">Quantity</label>
                    <div class="control">
                        <input id="quantityInput" v-model="quantity" class="input" :disabled="lot == null" type="number" min="1" required>
                    </div>
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

