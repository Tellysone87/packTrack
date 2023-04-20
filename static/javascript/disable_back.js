// <!-- Script to stop user from going into profile after logging out -->

// alert("js here!")

function preventBack(){window.history.forward();}
setTimeout("preventBack()", 0);
window.onunload=function(){null};