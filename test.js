const express = require("express");
const axios = require("axios");
const z = require("zod");
const {Schema} = require("zod");
const CityTier = z.enum([
    Tier_1,
    Tier_2,
    Tier_3
])
const Inputdata = z.object({
    Income : z.float(), Age : z.float(), Dependents:z.float(), Disposable_Income:z.float(), Desired_Savings:z.float(),
            Groceries:z.float(), Transport:z.float(), Eating_Out:z.float(), Entertainment:z.float(), Utilities:z.float(),
            Healthcare:z.float(), Education:z.float(), Miscellaneous:z.float(), Occupation:z.float(), City_Tier:CityTier
})
const app = express();
app.use(express.json());

app.post("/predict-saving", async (req, res) => {
    try {
        const data = req.body;
        const parsedData = Inputdata.safeParse(data)
        if(!parsedData){
            res.status(411).json({
                msg:"Incorrect Data format"
            })
            return
        }
        const response = await axios.post("http://127.0.0.1:8000/predict", { data });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: "Failed to get prediction" });
    }
});

app.listen(3000, () => console.log("Node.js server running on port 3000"));
