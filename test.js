const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

app.post("/predict-expense", async (req, res) => {
    try {
        const { month } = req.body;

        // Call Python API
        const response = await axios.post("http://127.0.0.1:8000/predict", { month });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: "Failed to get prediction" });
    }
});

app.listen(3000, () => console.log("Node.js server running on port 3000"));
