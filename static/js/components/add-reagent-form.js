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
        }
    },
    template: `
<form id="add-reagent-form">
    <div class="field">
        <label for="templateSelect" class="label">Template</label>
        <div class="control">
            <div class="select">
                <select id="templateSelect" v-model="template">
                    <option v-for="template in templates" :key="'t-' + template.id" :value="template.id">{{ template.description }}</option>
                </select>
            </div>
        </div>
    </div>   
    <div class="field">
        <label for="mfgSelect" class="label">Manufacturer</label>
        <div class="control">
            <div class="select">
                <select id="mfgSelect" v-model="manufacturer">
                    <option v-for="mfg in mfgWhere" :key="'m-' + mfg.id" :value="mfg.id">{{ mfg.name }}</option>
                </select>
            </div>
        </div>
    </div>   
    <div class="field">
        <label for="lotSelect" class="label">Lot</label>
        <div class="control">
            <div class="select">
                <select id="lotSelect" v-model="lot">
                    <option v-for="lot in lotWhere" :key="'l-' + lot.id" :value="lot.id">{{ lot.lot_num }}</option>
                </select>
            </div>
        </div>
    </div>   
</form>
    `,
    computed: {
        tempLots: function () {
            return this.template ? this.lots.filter(lot => lot.template_id == this.template) : null;
        },
        mfgWhere: function () {
            return this.tempLots ? this.manufacturers.filter(mfg => this.tempLots.find(lot => lot.mfg_id == mfg.id)) : null;
        },
        lotWhere: function () {
            return this.manufacturer ? this.tempLots.filter(lot => lot.mfg_id == this.manufacturer) : null;
        },
    },
    methods: {
        submit: function () {

        }
    }
})

const vm = new Vue({
    el: '#v-add',
    data: data,
    components: {
        'add-reagent-form': AddReagentForm
    }
})

