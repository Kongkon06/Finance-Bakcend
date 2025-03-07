const express = require('express');
const Transaction = express.Router();
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// GET all transactions
Transaction.get('/', async (req, res) => {
  try {
    const transactions = await prisma.transaction.findMany({
      include: {
        user: true,
        account: true,
      },
    });
    res.json(transactions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch transactions' });
  }
});

// GET a specific transaction by ID
Transaction.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const transaction = await prisma.transaction.findUnique({
      where: { id },
      include: {
        user: true,
        account: true,
      },
    });
    if (!transaction) {
      return res.status(404).json({ error: 'Transaction not found' });
    }
    res.json(transaction);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch transaction' });
  }
});

// POST a new transaction
Transaction.post('/', async (req, res) => {
  const { accountId, userId, Type, Date, isRecurring, status, description } = req.body;
  try {
    const newTransaction = await prisma.transaction.create({
      data: {
        accountId,
        userId,
        Type,
        Date,
        isRecurring,
        status,
        description,
      },
    });
    res.status(201).json(newTransaction);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create transaction' });
  }
});

// PUT (update) an existing transaction
Transaction.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { accountId, userId, Type, Date, isRecurring, status, description } = req.body;
  try {
    const updatedTransaction = await prisma.transaction.update({
      where: { id },
      data: {
        accountId,
        userId,
        Type,
        Date,
        isRecurring,
        status,
        description,
      },
    });
    res.json(updatedTransaction);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update transaction' });
  }
});

// DELETE a transaction
Transaction.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.transaction.delete({
      where: { id },
    });
    res.status(204).send(); // No content
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete transaction' });
  }
});

module.exports = Transaction;
