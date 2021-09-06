
document.onclick = hideMenu; 
//document.oncontextmenu = rightClick; 

const Http = new XMLHttpRequest();

var curr_item;

function hideMenu() { 
    document.getElementById("contextMenu") 
	    .style.display = "none" 
} 

function rightClick(e) { 
    e.preventDefault(); 

    if (document.getElementById("contextMenu") .style.display == "block"){ 
		hideMenu(); 
    }else{ 
		var menu = document.getElementById("contextMenu")      
		menu.style.display = 'block'; 
		menu.style.left = e.pageX + "px"; 
		menu.style.top = e.pageY + "px";
		var items = menu.querySelectorAll("li"); 
		Array.prototype.forEach.call(items, function(el) {
			el.style.display = "none";
		});
    } 
} 

function rightClickFolder(e, item) { 
    rightClick(e);
	var menu = document.getElementById("contextMenu")
	var elements = menu.getElementsByClassName("folder-item")

    if (menu.style.display == "block"){ 
		Array.prototype.forEach.call(elements, function(el) {
			el.style.display = "block";
		});
		curr_item = item;
    }
}

function rightClickFile(e, item) { 
    rightClick(e);
	var menu = document.getElementById("contextMenu")
	var elements = menu.getElementsByClassName("file-item")

    if (menu.style.display == "block"){ 
		Array.prototype.forEach.call(elements, function(el) {
			el.style.display = "block";
		});
		curr_item = item;
    }
}


function clickDelete(e){
	var url = "http://" + location.hostname + ":" + location.port + "/delete-file" + "?filename=" + curr_item.dataset.fname;
	Http.open("GET", url);
	Http.send();
	location.reload();
}

function clickDownload(e, item){
	item.href = "/uploads" + "/" + curr_item.dataset.fname;
	console.log(item.href);
}