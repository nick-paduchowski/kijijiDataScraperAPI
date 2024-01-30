const { Router } = require('express');
const controller = require('./controller');
const router = Router();

// Get All Jobs

router.get('/', controller.displayWelcomeMessage);
router.get('/:category',controller.getJobByCategory);
router.get('/all', controller.getAllJobs)


module.exports = router;