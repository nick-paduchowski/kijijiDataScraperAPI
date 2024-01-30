const getAllJobs = "SELECT * FROM job_data";
const getJobsByCategory = "SELECT * FROM job_data WHERE category = $1"

module.exports = {
    getAllJobs,
    getJobsByCategory
}