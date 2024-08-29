function reset_block(tag_name, count = 5) {
  setTimeout(() => {
    document.getElementsByName(tag_name)[0].style.display = "none";
  }, count * 1000);
}

function message_block(tag_name, message, count = 5) {
  message_tag = document.getElementById(tag_name);
  message_tag.innerHTML = message;
  document.getElementsByName(tag_name)[0].style.display = "block";

  const intervalId = setInterval(() => {
    count--;
    message_tag.innerHTML = message;

    if (count === 0) {
      clearInterval(intervalId);
    }
  }, 1000);
}

function register() {
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  confirm_password = document.getElementById("confirm_password").value;
  email = document.getElementById("email").value;

  if (confirm_password !== password) {
    message_block("reg_message", "Passwords do not match!", 5);
    reset_block("reg_message", 5);
    return;
  }

  if (username === "" || password === "" || email === "") {
    message_tag = document.getElementById("reg_message");
    message_block("reg_message", "Please fill all fields", 5);
    reset_block("reg_message", 5);
    return;
  } else {
    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        email: email,
      }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // Reset token stored
        if (data.reset_token) {
          message_block(
            "reset_token",
            data.reset_token +
              ": (This is your reset token, keep it safe, disappears in 15s.)",
            15,
          );
          reset_block("reset_token", 15);
          setTimeout(() => {
            window.location.href = "/login";
          }, 15000);
        }

        message_block("reg_message", data.message, 3);
        reset_block("reg_message", 3);
      })
      .catch((error) => {
        message_block("reg_message", error, 5);
        reset_block("reg_message");
      });
  }
}
