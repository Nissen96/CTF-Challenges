require('dotenv').config()
const cors = require('cors')
const express = require("express")
const jwt = require("jsonwebtoken")
const uuid = require("uuid")
const { VM } = require('vm2')

const auth = require("./middleware/auth")
const db = require("./db")

const app = express()
app.use(cors())
app.use(express.json())


// Catch otherwise uncaught async exceptions
process.on('uncaughtException', (err) => console.log(err))

app.post('/register', (req, res) => {
    const name = req.body.name
    const username = req.body.username
    const password = req.body.password
    if (!(username && password)) {
        return res.status(400).json({msg: "Username and password required"})
    }

    // Check exists already
    if (db.getUser(username)) {
        return res.status(403).json({ msg: "Username already exists" })
    }

    // Set user-specific secret for token generation
    db.addUser({ name, username, password, secret: uuid.v4() })
    
    return res.json({ msg: "User registered" })
})


app.post('/login', (req, res) => {
    const username = req.body.username
    const password = req.body.password
    if (!(username && password)) {
        return res.status(400).json({ msg: "Username and password required" })
    }

    // Check if username and password match
    const user = db.getUser(username)
    if (!user || user.password !== password) {
        return res.status(401).json({ msg: "Username or password invalid" })
    }

    // Generate and sign user token with user-specific secret (fallback to default server secret)
    const token = jwt.sign({ username: user.username }, user.secret || process.env.SERVER_SECRET)
    return res.json({ msg: token })
})


app.post('/update', auth, (req, res) => {
    // auth middleware verifies token and sets username
    const verified_username = req.username
    if (!verified_username) {
        return res.status(400).json({ msg: "Token issue" })
    }

    // Don't allow username or secret updates
    if (req.body.hasOwnProperty("username")) {
        return res.status(403).json({ msg: "You cannot change your username" })
    }

    if (req.body.hasOwnProperty("secret")) {
        return res.status(403).json({ msg: "Nice try..." })
    }

    if (!db.getUser(verified_username)) {
        return res.status(401).json({ msg: "User not found" })
    }

    db.updateUser(verified_username, req.body)

    return res.json({ msg: "User info updated" })
})

app.post('/run', auth, (req, res) => {
    const verified_username = req.username
    if (!verified_username) {
        return res.status(400).json({ msg: "Token issue" })
    }

    const code = req.body.code
    if (!code) {
        return res.status(400).json({ msg: "No code provided" })
    }
    
    try {
        let result
        if (verified_username !== "admin") {
            // Run untrusted user code safely in sandbox
            const vm = new VM();
            result = vm.run(code)
        } else {
            // Run admin code without restrictions
            result = eval(code)
        }
        return res.json({ msg: result })
    } catch (e) {
        return res.status(400).json({ msg: "Error running function" })
    }
})


PORT = 80
app.listen(PORT, () => console.log(`Server started at 0.0.0.0:${PORT}`))
