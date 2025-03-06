const express = require('express');

const Transaction = express.Router();

Transaction.get('/',(req,res)=>{
res.json();
})
Transaction.post('/',(req,res)=>{
res.json();
})
Transaction.post('/',(req,res)=>{
res.json();
})

export default Transaction;
