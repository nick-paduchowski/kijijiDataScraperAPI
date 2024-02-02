const { param } = require("./routes");

const getAllJobs = "SELECT * FROM job_data";
const getJobsByCategory = "SELECT * FROM job_data WHERE category = $1"


const buildQuery = (parameters) => {
    let baseQuery = "SELECT * FROM job_data WHERE ";
    let query = baseQuery;

    let lastIndex = 0;
    let totalProps = Object.keys(parameters).length;
    console.log(parameters)
    for (let param in parameters) {
        if (++lastIndex === totalProps){
            query += param + " = " + "'" + parameters[param] + "'"; 
            console.log(query)
            return query;
        } else {
            query += param + " = " + "'" + parameters[param] + "'"; 
            query += " AND ";
        }       
    }
    
}

module.exports = {
    getAllJobs,
    getJobsByCategory,
    buildQuery,
}