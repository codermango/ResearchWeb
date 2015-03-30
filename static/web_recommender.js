function checkInput() {
    var txt = document.querySelector("#submit-input");
    var txtValue = txt.value;
    
    if (txtValue.length == 0) {
        alert("Please input imdb ids, one id each line.");
        return false;
    } else {
        return true;
    }
}