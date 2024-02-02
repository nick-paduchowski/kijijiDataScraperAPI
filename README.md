# kijijiDataScraperAPI
This is a Kijiji Job Data API for people who would like to add Kijiji Job Data to their application.

You can currently query this API for all job data or job data by category.

 ## How to Query It

 Since there are roughly ~20,000 records in the database it is not recommended to query the /all endpoint. It can take anywhere from 15-30 seconds to respond with all the data. It is better to do multiple requests for smaller responses such as querying by category. 


## Future Plans

In the current version, you can query the DB for things such as category, city, province, and, job-type. My next change will be querying the database also by time posted. However, I expect server costs will be astronomical when I deploy this to AWS if I keep all the ad data. So I expect I will only keep ads up to 60 days old in my DB.
