const express = require('express');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const router = express.Router();

// POST /financial-profile - Create a financial profile
router.post('/', async (req, res) => {
  try {
    const { userId, ...data } = req.body;

    // Validate required fields
    if (!userId || !data.Income || !data.Age || !data.Dependents || !data.Disposable_Income || !data.Desired_Savings) {
      return res.status(400).json({ msg: 'userId, Income, Age, Dependents, Disposable_Income, and Desired_Savings are required' });
    }

    // Create the financial profile
    const financialProfile = await prisma.financialProfile.create({
      data: {
        userId,
        ...data,
      },
    });

    res.status(201).json(financialProfile);
  } catch (e) {
    console.error('Error creating financial profile:', e);
    res.status(500).json({ msg: 'Error while creating financial profile' });
  }
});

// GET /financial-profile/:userId - Fetch a financial profile by userId
router.get('/:userId', async (req, res) => {
  try {
    const { userId } = req.params;

    // Find the financial profile
    const financialProfile = await prisma.financialProfile.findUnique({
      where: {
        userId,
      },
    });

    if (!financialProfile) {
      return res.status(404).json({ msg: 'Financial profile not found' });
    }

    res.json(financialProfile);
  } catch (e) {
    console.error('Error fetching financial profile:', e);
    res.status(500).json({ msg: 'Error while fetching financial profile' });
  }
});

// PUT /financial-profile/:userId - Update a financial profile by userId
router.put('/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const data = req.body;

    // Validate required fields
    if (!userId) {
      return res.status(400).json({ msg: 'userId is required' });
    }

    // Update the financial profile
    const financialProfile = await prisma.financialProfile.update({
      where: {
        userId,
      },
      data,
    });

    res.json(financialProfile);
  } catch (e) {
    console.error('Error updating financial profile:', e);
    res.status(500).json({ msg: 'Error while updating financial profile' });
  }
});

module.exports = router;
