import { PrismaClient } from '@prisma/client/extension';

const express = require('express');

const User = express.Router();
const prisma = new PrismaClient;
User.post('/',async(req,res)=>{
  try{
  const data = req.body;
  const user = await prisma.user.create({
    data:{
      name:data.name,
      password:data.password,
      email:data.email,
      joinedAt:Date.now()
    }
  })
  res.json(user);
  }catch(e){
    res.status(411).json({msg:"error while connecting"});
  }
})

User.post('/signin',async(req,res)=>{
  const data = req.body;
  try{
    const user = await prisma.user.findFirst({
      where:{
        email:data.email,
        name:data.name
      }
    })
    if(!user){
      res.status(411).json({
        msg:'User not found'
      })
      return
    }
    res.jon(user)
  }catch(e){
    res.status(411).json();
    return
  }
})

export default User;
