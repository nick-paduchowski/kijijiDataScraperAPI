const { Router } = require('express');
const controller = require('./controller');
const router = Router();

// Get All Jobs

router.get('/', controller.displayWelcomeMessage);


module.exports = router;