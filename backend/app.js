const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('../frontend'));

app.post('/upload', upload.single('file'), (req, res) => {
    console.log("File upload attempted");
    console.log(req.file); 
    res.status(200).send("File upload successful");
});

app.post('/process-video', upload.array('photos'), (req, res) => {
    const photoFiles = req.files;
    const photoDurations = req.body.durations; 

    console.log(photoFiles, photoDurations); 

    res.status(200).send('Video processing started');
  
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
