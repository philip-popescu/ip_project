function showPass() {
    const x = document.getElementById("passw");
    if (x.type === "password") {
        x.type = "text";
    }
    else {
        x.type = "password";
    }
}

function displayErr(check) {

    let err = document.getElementById("alert");
    let new_message = document.getElementById("message")

    if (check == 0) {
        location.href = "/home/"+document.getElementById("nume").value;
    }
    else if (check > 1) {
        err.style.opacity = 1;
        err.innerHTML = "Parolele nu sunt identice!";
        document.getElementById("passw").value = '';
        document.getElementById("r_passw").value = '';
    }
    else{
        err.style.opacity = 1;
        err.innerHTML = "Date incorecte introduse!"
        document.getElementById("nume").value = '';
        document.getElementById("telefon").value = '';
        document.getElementById("email").value = '';
        document.getElementById("passw").value = '';
        document.getElementById("r_passw").value = '';
    }
    setTimeout(function () { err.style.opacity = 0;}, 1000);

}

function checkCredentials() {
    let ret = 0;

    if (document.getElementById("nume").value === "") {
        ret = 1;
        console.log("name null")
    }

    let p = document.getElementById("passw");
    if (p.length < 8) {
        ret = 1;
        console.log("password too short");
    }

    let t = document.getElementById("telefon");
    let e = document.getElementById("email");
    let t_pattern = /[07]{2}[0-9]{2}[0-9]{3}[0-9]{3}/;
    let e_pattern = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$/;

    if ( !RegExp(t_pattern).test(t.value) || !RegExp(e_pattern).test(e.value)){
        ret = 1;
        console.log("phone match: " + t.value.match(t_pattern));
        console.log("mail match: " + e.value.match((e_pattern)));

    }

    let rp = document.getElementById("r_passw");
    if (p.textContent !== rp.textContent){
        ret = 2;
        console.log("different passwords");
    }
    console.log(ret);

    displayErr(ret);
}
