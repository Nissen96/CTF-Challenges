const uuid = require("uuid")

// TODO: Proper database setup, probably MongoDB
const users = [
    {
        name: "Runner M. Brunner",
        username: "admin",
        password: uuid.v4(),
    }
]

function getUser(username) {
    return users.find(user => user.username === username)
}

function addUser(user) {
    users.push(user)
}

function updateUser(username, userInfo) {
    // Merge provided user info into existing user object
    merge(getUser(username), userInfo)
}

function merge(target, source) {
    for (let key in source) {
        if (typeof target[key] === "object" && typeof source[key] === "object") {
            merge(target[key], source[key])
        } else {
            target[key] = source[key]
        }
    }
}

module.exports = { getUser, addUser, updateUser }
