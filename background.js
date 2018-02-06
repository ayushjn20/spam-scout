console.log(1)
element = document.getElementById("myBtn")
if (element){
element.addEventListener("click", displayDate);
function displayDate() {
chrome.tabs.create({url: "https://www.facebook.com/"})
   }
}
else
	console.log(2);
