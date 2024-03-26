document.addEventListener('DOMContentLoaded', function() {
    if (window.Dropzone) {
        Dropzone.options.imageUpload = {
            url: "/api/upload",
            paramName: "file",
            maxFilesize: 5, // MB
            acceptedFiles: 'image/jpeg,image/png',
            dictDefaultMessage: 'Drop images here to upload (or click)',
            init: function() {
                this.on("success", function(file, response) {
                    console.log("Successfully uploaded: ", response);
            
                });
            }
        };
    }
    document.getElementById('background-music').addEventListener('change', function(event) {
        console.log('Background music selected:', event.target.files[0].name);
        // handle the selected file here if needed.
    });
    document.getElementById('transition-effect').addEventListener('change', function(event) {
        console.log('Transition effect selected:', event.target.value);
        // handle the selected effect if required.
    });
    document.getElementById('image-duration').addEventListener('change', function(event) {
        console.log('Image duration set to:', event.target.value, 'seconds');
        // handling for the image duration .
    });
    document.getElementById('resolution').addEventListener('change', function(event) {
        console.log('Output resolution selected:', event.target.value);
        // Handle the resolution change .
    });
});

function createvideo() {
    const ImageFile = document.getElementById('imageUpload').files;
    const musicFile = document.getElementById('background-music').files[0];
    const effect = document.getElementById('transition-effect').value;
    const duration = document.getElementById('image-duration').value;
    const resolution = document.getElementById('resolution').value;

    console.log('Creating video with the following options:', {
        ImageFile: ImageFile ? ImageFile : 'None',
        musicFile: musicFile ? musicFile.name : 'None',
        effect: effect,
        duration: duration,
        resolution: resolution
    });

    const formData = new FormData();
    for (const file of ImageFile) {
        formData.append('ImageFile', file);
    }
    if (musicFile) {
        formData.append('musicFile', musicFile);
    }
    formData.append('effect', effect);
    formData.append('duration', duration);
    formData.append('resolution', resolution);

    fetch('/api/create-video', {
        method: 'POST',
        body: formData,
    }).then(response => {
        console.log('Video created:', response);
        document.getElementById('video-preview').style.display = 'block';
    }).catch(error => {
        console.error('Error creating video:', error);
    });
};
