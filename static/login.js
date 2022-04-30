function showPass() {
    const x = document.getElementById("passw");
    if (x.type === "password") {
        x.type = "text";
    }
    else {
        x.type = "password";
    }
}

function displayErr(alert_id) {

    let err = document.getElementById(alert_id);
    err.style.opacity = 1;
    setTimeout(function () { err.style.opacity = 0;}, 1000);
}

function verify_Login() {

    let ret = 0;
    let p = document.getElementById("passw");
    if (p.length < 8) {
        ret = 1;
        console.log("password too short");
    }

    let e = document.getElementById("email");
    let e_pattern = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$/;

    if (!RegExp(e_pattern).test(e.value)){
        ret = 1;
        console.log("mail match: " + e.value.match((e_pattern)));
    }

    if (ret == 1) {
        displayErr("alertLogin");
    }
    else {
        document.getElementById("submitForm").submit();
    }
}

function verify_2fa() {

    let code = document.getElementById("2fa");

    if (code.value == "") {
        console.log("empty")
        displayErr("alert2FA");
    } else {
        console.log(code.value)
        document.getElementById("2FA_form").submit();
    }
}