const dotenv = require('dotenv')

dotenv.config()

const Pool = require('pg').Pool;

const pool = new Pool({
    user: "postgres",
    host: "localhost",
    database: "kijiji_ad_data",
    password: process.env.USER_PASS,
    port: 5432
})

module.exports = pool;
