
Dropzone.options.myAwesomeDropzone = {
    autoProcessQueue: false,
    uploadMultiple: true,
    parallelUploads: 10, 
    maxFiles: 10, 
    maxFilesize: 1000,
    init: function() { 
		myDropzone = this;
		this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {  
			e.preventDefault();
			e.stopPropagation();
			myDropzone.processQueue();
		});
		this.on("complete", function(file) { 
			this.removeAllFiles(true); 
			location.reload();
		});
  }
};
