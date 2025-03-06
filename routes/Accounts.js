const express = require('express');

const Accounts = express.Router();

Accounts.get('',(req,res)=>{
  res.json();
});
Accounts.post('',(req,res)=>{
  res.json();
});

export default Accounts;
