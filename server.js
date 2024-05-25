const express = require('express');
const { GoogleGenerativeAI } = require("@google/generative-ai");
const cors = require('cors');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const Patient = require('./model.js'); // Import the patient model

const geminiApiKey = "AIzaSyCXsf2wkBUf_QqGfISAwxhrqUtrEnvDxhs";
const app = express();
const port = 3000;
const genAI = new GoogleGenerativeAI(geminiApiKey);

app.use(bodyParser.json());
app.use(cors());
app.use(express.static("public"));

const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });

mongoose.connect('mongodb+srv://abdouovi:12345@hackaton.izxafdf.mongodb.net/?retryWrites=true&w=majority&appName=hackaton', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

app.post('/add_patient', async (req, res) => {
    const { name, age, condition } = req.body;
    const patient = new Patient({ name, age, condition });
    try {
        await patient.save();
        res.status(201).send(patient);
    } catch (error) {
        res.status(400).send(error);
    }
});

app.get('/patients', async (req, res) => {
    try {
        const patients = await Patient.find();
        res.status(200).send(patients);
    } catch (error) {
        res.status(500).send(error);
    }
});

app.get('/search_patient', async (req, res) => {
    const { name } = req.query;
    try {
        const patients = await Patient.find({ name: new RegExp(name, 'i') }); // Case-insensitive search
        res.status(200).send(patients);
    } catch (error) {
        res.status(500).send(error);
    }
});

app.get("/", (req, res) => {
    res.sendFile(__dirname + '/public/main.html');
});

app.post('/chat', async (req, res) => {
    const message = req.body.message;

    if (!message || typeof message !== 'string') {
        return res.status(400).send('Invalid message format.');
    }

    console.log("Received message:", message);
    console.log("Using OpenAI API key:", geminiApiKey); // Debugging line

    try {
        const result = await model.generateContent(message);
        const response = await result.response;
        res.json({
            "message": response.text()
        });
    } catch (error) {
        if (error.response) {
            console.error("Error response data:", error.response.data);
            if (error.response.status === 429) {
                res.status(429).send('You have exceeded your current quota. Please check your OpenAI plan and billing details.');
            } else if (error.response.status === 403) {
                res.status(403).send('Access to the model is restricted. Please check your API key and subscription plan.');
            } else if (error.response.status === 401) {
                res.status(401).send('Unauthorized. Please check your API key.');
            } else {
                res.status(error.response.status).send(error.response.data);
            }
        } else if (error.request) {
            console.error("Error request data:", error.request);
            res.status(500).send('No response received from the API.');
        } else {
            console.error("Error message:", error.message);
            res.status(500).send('An error occurred while processing your request.');
        }
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
