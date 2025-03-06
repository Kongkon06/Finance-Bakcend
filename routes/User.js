const express = require('express');

const User = express.Router();

User.post('/',async(req,res)=>{
  const data = req.body;
  res.json()
})

User.post('/signin',async(req,res)=>{
  const data = req.body;
  res.json()
})

export default User;
