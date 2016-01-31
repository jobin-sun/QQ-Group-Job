$T = {}
$T.toast = function(txt,t){
	if(t == undefined){
		t = 3
	}
	if(txt == undefined){
		return
	}
	document.querySelector(".rz_toast_txt").innerHTML = txt;
	document.querySelector(".rz_toast_ctn").style.display = "block";
	setTimeout(function(){
		document.querySelector(".rz_toast_ctn").style.display = "";
	},t*1000)
}