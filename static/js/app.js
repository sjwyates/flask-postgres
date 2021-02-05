const vm = new Vue({
    el: '#app',
    data: {
        message: 'hello world'
    }
})

const AddReagentForm = Vue.component('add-reagent-form', {
    data: function () {
        return {
            template: null,

        }
    },
    template: `
<form id="add-reagent-form">
    <div class="field">
        <label class="label">Template</label>
        <div class="control">
            <div class="select">
                <select>
                    <option>Select dropdown</option>
                    <option>With options</option>
                </select>
            </div>
        </div>
    </div>   
</form>
    `,
    methods: {
        submit: function() {

        }
    }
})