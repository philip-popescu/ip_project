function showPass() {
    const x = document.getElementById("passw");
    if (x.type === "password") {
        x.type = "text";
    }
    else {
        x.type = "password";
    }
}

function displayErr() {

    console.log("show err");
    let err = document.getElementById("alert");

    err.style.opacityty = 1;
    document.getElementById("email").value = '';
    document.getElementById("passw").value = '';

    setTimeout(function () { err.style.opacity = 0;}, 1000);
}