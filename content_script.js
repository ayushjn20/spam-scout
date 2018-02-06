
var n=document.getElementsByTagName("a");
var l=document.getElementsByTagName("link");
var s=document.getElementsByTagName("script");
var im=document.getElementsByTagName("img");
var ifr=document.getElementsByTagName("iframe");

var anchor_arr=[];	
for (var i = n.length - 1; i >= 0; i--) {
	if(n[i].hostname!="")
	anchor_arr.push(n[i].hostname)

}
var link_arr=[];
for (var i = l.length - 1; i >= 0; i--) {
	if(l[i].href!=""){
	var t=l[i].href.split("//");
	link_arr.push((String(t[1]).split("/"))[0])
}}
var script_arr=[];
for (var i = s.length - 1; i >= 0; i--) {
	var z=s[i].src;
	if(z!==""){
	var z1=String(z).split("//")
	script_arr.push((String(z1[1]).split("/"))[0])
}}
img_arr=[];
for (var i = im.length - 1; i >= 0; i--) {
	var im1=im[i].src;
	im2=String(im1).split("//");
	im3=String(im2[1]).split("/");
	img_arr.push(String(im3[0]));
}
iframe_arr=[];
for (var i = ifr.length - 1; i >= 0; i--) {
	var ifr1=ifr[i].src;
	ifr2=String(ifr1).split("//");
	ifr3=String(ifr2[1]).split("/");
	iframe_arr.push(String(ifr3[0]));
}

iframe_array=new Set(iframe_arr);	
anchor_array=new Set(anchor_arr);
link_array=new Set(link_arr);
img_array=new Set(img_arr);
script_array=new Set(script_arr);



xhttp.open("POST", "ajax_test.asp", true);
xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xhttp.send("");

/*
console.log(iframe_array);
console.log(anchor_array);
console.log(link_array);
console.log(script_array);
console.log(img_array);
*/

