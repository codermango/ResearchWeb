function checkInput() {
    var txt = document.querySelector("#textarea-ids");
    var txtValue = txt.value;
    var submitIdsForm = document.querySelector("#submit-ids-form")
    if (txtValue.length == 0) {
        alert("Please input imdb ids, one id each line.");
        return false;
    } else {
        return true;
    }
}