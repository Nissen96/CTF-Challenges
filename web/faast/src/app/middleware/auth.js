const jwt = require("jsonwebtoken")
const db = require("../db")

module.exports = (req, res, next) => {
    const token = req.header('x-auth-token')

    if (!token) {
        return res.status(401).json({ msg: "No token provided in x-auth-token header" })
    }

    try {
        // Get username from token and lookup in db to get user-specific secret
        const decoded = jwt.decode(token)
        const user = db.getUser(decoded.username)
        if (!user) {
            return res.status(401).json({ msg: "User not found" })
        }
        
        // Verify token with user-specific secret (fallback to default server secret)
        req.username = jwt.verify(token, user.secret || process.env.SERVER_SECRET).username
        next()
    } catch (error) {
        return res.status(401).json({ msg: error.message })
    }
}
