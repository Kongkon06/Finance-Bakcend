const express = require('express');
const User = require('./routes/User.js')
const Transaction = require('./routes/Transactions.js')
const Account= require('./routes/Accounts.js')
const app = express();

app.use(express.json());

app.get("Hello there");
app.use('/User',User);
app.use('/Account',Account);
app.use('/Transaction',Transaction);

app.listen(3000,()=>console.log('Server is online'));
