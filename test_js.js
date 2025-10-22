const express = require('express');
const exec = require('child_process').exec;

const app = express();

// SQL Injection
app.get('/user/:id', (req, res) => {
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    db.query(query);
});

// Command Injection
app.get('/ping', (req, res) => {
    exec(`ping ${req.query.host}`);
});

// Hardcoded secret
const API_KEY = 'sk_live_abc123';
