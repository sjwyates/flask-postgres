const config = {responsive: true}

const data1 = [
    {
        x: ['Unopened', 'Open', 'Quarantine', 'Expired'],
        y: [73, 29, 6, 4],
        type: 'bar'
    }
];

const layout1 = {
    title: {
        text: 'Reagent Status'
    }
}

const plot1 = Plotly.newPlot('plot1', data1, layout1, config);

const traceUnopened = [
    {
        x: ['Acetonitrile', 'Acetone', 'Sodium Chloride', 'Acetic Acid', 'DMEM'],
        y: [0, 1, 1, 2, 4],
        name: 'Unopened',
        type: 'bar'
    }
];

const traceOpen = [
    {
        x: ['Acetonitrile', 'Acetone', 'Sodium Chloride', 'Acetic Acid', 'DMEM'],
        y: [2, 1, 1, 1, 0],
        name: 'Open',
        type: 'bar'
    }
];

const traceSafety = [
    {
        x: ['Acetonitrile', 'Acetone', 'Sodium Chloride', 'Acetic Acid', 'DMEM'],
        y: [2, 2, 2, 2, 6],
        name: 'Safety Stock',
        type: 'bar'
    }
];

const data2 = [traceUnopened, traceOpen, traceSafety];

const layout2 = {
    title: {
        text: 'Inventory'
    },
    barmode: 'stack'
}

const plot2 = Plotly.newPlot('plot2', data2, layout2, config);