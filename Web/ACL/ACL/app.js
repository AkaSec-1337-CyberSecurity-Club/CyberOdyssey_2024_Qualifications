const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const crypto = require('crypto');
require('dotenv').config();

const app = express();
const PORT = 3000;

const FLAG = require('child_process').execSync('cat /flag_*').toString().trim();

app.set('view engine', 'ejs');

app.use(bodyParser.json());
app.use(session({
    secret: crypto.randomBytes(32).toString('hex'),
    resave: false,
    saveUninitialized: true
}));

app.post('/register', (req, res) => {
    const { username, ACL } = req.body;

    if (ACL > 1) {
        return res.status(403).json({ message: 'Unauthorized' });
    }

    const user = { username: username, ACL: parseInt(ACL) };
    Object.assign(req.session, user)
    return res.status(200).json({ message: 'User registered', user });
});

app.post('/flag', (req, res) => {
    const ACL = req.session?.ACL;

    if (!(ACL > 1)) {
        return res.status(403).json({ message: 'Unauthorized' });
    }

    if (!req.body.flag) {
        return res.status(421).json({ message: 'Provide a FLAG to check.' });
    }
    Object.assign(req.body, {flagCorrect: req.body.flag == FLAG});
    res.render('flag', req.body);
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
