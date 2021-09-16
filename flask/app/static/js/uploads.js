
Dropzone.options.myAwesomeDropzone = {
    maxFilesize: 1000,
    init: function() { 
		myDropzone = this;
		this.on("complete", function(file) { 
			this.removeAllFiles(true); 
			location.reload();
		});
  }
};
