const pool = require("../db");
const queries = require("./queries");

const displayWelcomeMessage = (req, res) => {
  try {
    res.status(200).json({
        "Hello!": "Welcome to the Kijiji Ads Data API.",
        "Current Jobs Data Available": "All Job Data is available to fetch.",
      });
  } catch (error) {
    res.status(500).json({
        "Error": "There was an error with your request. Try again later."
    })
  }
  
};

module.exports = {
  displayWelcomeMessage,
};
