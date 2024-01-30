const getAllJobs = "SELECT * from job_data";
const getJobsByCategory = "SELECT * from job_data WHERE category = $1"

module.exports = {
    getAllJobs,
    getJobsByCategory
}