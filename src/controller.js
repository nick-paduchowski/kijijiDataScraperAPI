const pool = require("../db");
const queries = require("./queries");

const displayWelcomeMessage = (req, res) => {
  try {
    res.status(200).json({
        "Hello!": "Welcome to the Kijiji Ads Data API.",
        "Current Jobs Data Available": "All Job Data is available to fetch.",
      });
    console.log("Request Received")
  } catch (error) {
    res.status(500).json({
        "Error": "There was an error with your request. Try again later."
    })
  }
  
};

const getJobsByCategory = (req, res) => {
    const category = req.params.category;
    console.log(category);
    pool.query(queries.getJobsByCategory, [category], (error, results) => {
        if (error) throw error;
        res.status(200).json(results.rows);
    });
}

const getAllJobs = (req,res) => {
    pool.query(queries.getAllJobs, (error, results) => {
        if (erorr) throw error;
        res.status(200).json(results.rows);
    })
}

module.exports = {
  displayWelcomeMessage,
  getJobsByCategory,
  getAllJobs,
};
