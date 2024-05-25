// model.js
const mongoose = require('mongoose');

const patientSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    age: {
        type: Number,
        required: true
    },
    condition: {
        type: String,
        required: true
    }
});

const Patient = mongoose.model('Patient', patientSchema);

module.exports = Patient;

