function login() {
    window.location.replace("/login")
}

function sign_in() {
    let username = $("#input-username").val();
    let password = $("#input-password").val();

    if (username === "") {
        $("#help-id-login").text("Please input your id.");
        $("#input-username").focus();
        return;
    } else {
        $("#help-id-login").text("");
    }

    if (password === "") {
        $("#help-password-login").text("Please input your password.");
        $("#input-password").focus();
        return;
    } else {
        $("#help-password-login").text("");
    }

    console.log(username, password);
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                $.cookie("mytoken", response["token"], { path: "/" });
                window.location.replace("/tambah");
            } else {
                alert(response["msg"]);
            }
        },
    });
}

function toggle_sign_up() {
    $("#sign-up-box").toggleClass("is-hidden");
    $("#div-sign-in-or-up").toggleClass("is-hidden");
    $("#btn-check-dup").toggleClass("is-hidden");
    $("#help-id").toggleClass("is-hidden");
    $("#help-password").toggleClass("is-hidden");
}

function is_nickname(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function check_dup() {
    let username = $("#input-username").val();
    console.log(username);
    if (username === "") {
        $("#help-id")
            .text("Enter in your id")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-username").focus();
        return;
    }
    if (!is_nickname(username)) {
        $("#help-id")
            .text(
                "Please check your id. For your id, please enter 2-10 English characters, numbers, or the following special characters (._-)"
            )
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-username").focus();
        return;
    }
    $("#help-id").addClass("is-loading");
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            username_give: username,
        },
        success: function (response) {
            console.log(response);
            if (response["exists"]) {
                $("#help-id")
                    .text("This id is already in use.")
                    .removeClass("is-safe")
                    .addClass("is-danger");
                $("#input-username").focus();
            } else {
                $("#help-id")
                    .text("This id is available!")
                    .removeClass("is-danger")
                    .addClass("is-success");
            }
            $("#help-id").removeClass("is-loading");
        },
    });
}

function sign_up() {
    let username = $("#input-username").val();
    let password = $("#input-password").val();
    let password2 = $("#input-password2").val();
    console.log(username, password, password2);
    console.log($("#help-id").attr("class"));

    if ($("#help-id").hasClass("is-danger")) {
        alert("Please check your id");
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("Please double check your id");
        return;
    }

    if (password === "") {
        $("#help-password")
            .text("Please enter your password")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password").focus();
        return;
    } else if (!is_password(password)) {
        $("#help-password")
            .text(
                "Please check your password. For your password, please enter 8-20 English characters, numbers, or the following special characters (!@#$%^&*)"
            )
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password").focus();
        return;
    } else {
        $("#help-password")
            .text("This password can be used!")
            .removeClass("is-danger")
            .addClass("is-success");
    }
    if (password2 === "") {
        $("#help-password2")
            .text("Please enter your password")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else if (password2 !== password) {
        $("#help-password2")
            .text("Your passwords do not match")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else {
        $("#help-password2")
            .text("Your passwords match!!!")
            .removeClass("is-danger")
            .addClass("is-success");
    }
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            username_give: username,
            password_give: password,
        },
        success: function (response) {
            alert("Your are signed up! Nice!");
            window.location.replace("/login");
        },
    });
}

function clearInputs() {
    $("#input-username").val("");
    $("#input-password").val("");
    $("#input-password2").val("");
}

// function posting() {
//     let file = $("#inputfile").prop("files")[0];
//     let nama = $("#nama").val();
//     let deskripsi = $("#deskripsi").val();

//     let form_data = new FormData();
//     form_data.append("file_give", file);
//     form_data.append("nama_give", nama);
//     form_data.append("deskripsi_give", deskripsi);
//     console.log(file, nama, deskripsi, form_data);

//     $.ajax({
//         type: "POST",
//         url: "/posting",
//         data: form_data,
//         cache: false,
//         contentType: false,
//         processData: false,
//         success: function (response) {
//             alert(response["msg"]);
//             window.location.reload();
//         },
//     });
// }

function to_job(){
    window.location.replace("/job")
}

function to_tambah(){
    window.location.replace("/tambah")
}

function to_add(){
    window.location.replace("/addjob")
}