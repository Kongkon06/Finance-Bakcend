import { PrismaClient } from '@prisma/client';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import bcrypt from 'bcrypt';

dotenv.config();

const express = require('express');
const User = express.Router();
const prisma = new PrismaClient();
const jwt_secret = process.env.JWT_SECRET;

User.post('/signup', async (req, res) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ msg: 'Name, email, and password are required' });
    }
    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
        joinedAt: new Date(),
      },
    });

    const token = jwt.sign({ userId: user.id }, jwt_secret);

    res.status(201).json({ user, token });
  } catch (e) {
    console.error('Error during signup:', e);
    res.status(500).json({ msg: 'Error while creating user' });
  }
});

User.post('/signin', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ msg: 'Email and password are required' });
    }

    const user = await prisma.user.findFirst({
      where: {
        email,
      },
    });

    if (!user) {
      return res.status(404).json({ msg: 'User not found' });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ msg: 'Invalid password' });
    }

    const token = jwt.sign({ userId: user.id }, jwt_secret);

    res.json({ user, token });
  } catch (e) {
    console.error('Error during signin:', e);
    res.status(500).json({ msg: 'Error while authenticating user' });
  }
});

export default User;
