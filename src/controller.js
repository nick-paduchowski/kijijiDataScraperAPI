const pool = require("../db");
const queries = require("./queries");

const validQueryParams = ["category", "city", "province", "job-type"];

const displayWelcomeMessage = (req, res) => {
  try {
    res.status(200).json({
      "Hello!": "Welcome to the Kijiji Ads Data API.",
      "Current Jobs Data Available": "All Job Data is available to fetch.",
    });
    console.log("Request Received");
  } catch (error) {
    res.status(500).json({
      Error: "There was an error with your request. Try again later.",
    });
  }
};

const getAllJobs = (req, res) => {
  pool.query(queries.getAllJobs, (error, results) => {
    if (error) {
      console.log("An error occurred");
      throw error;
    }
    res.status(200).json(results.rows);
  });
};

const getJobs = (req, res) => {
  const queryInfo = req.query;
  const queryDB = true;
  for (let query in queryInfo) {
    if (!validQueryParams.includes(query)) {
      res.status(400).json({
        "Bad Request": "The request you sent includes non-valid parameters.",
        "Non-Valid Parameter": `${query}`,
      });
      queryDB = false;
      break;
    }
  }
  if (queryDB === true){
    pool.query(queries.buildQuery(queryInfo), (error, results) => {
      if (error){
        throw error;
      } else {
        res.status(200).json(results.rows);
      }
    });
  }
};

module.exports = {
  displayWelcomeMessage,
  getAllJobs,
  getJobs,
};
