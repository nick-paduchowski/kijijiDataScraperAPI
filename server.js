const express = require('express');
const app = express();
const port = 1748;
const apiRoutes = require('./src/routes')


app.use(express.json());

app.use('/api/v1/kijijiJobData', apiRoutes);

app.listen(port, () => console.log(`App is running on port: ${port}`))