const { Router } = require('express');
const controller = require('./controller');
const router = Router();

// Get All Jobs

router.get('/', controller.displayWelcomeMessage);
router.get('/all', controller.getAllJobs);
router.get('/jobs', controller.getJobs)


module.exports = router;