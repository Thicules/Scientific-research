function loadFile(event) {
    var profilePic = document.getElementById('profilePic');
    var input = event.target;

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            profilePic.style.backgroundImage = "url('" + e.target.result + "')";
        };

        reader.readAsDataURL(input.files[0]);
    }
}
