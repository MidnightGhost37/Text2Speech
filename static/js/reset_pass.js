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

function reset_pass() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("new_password").value;
  let confirm_password = document.getElementById("confirm_password").value;
  let reset_token = document.getElementById("reset_token").value;

  if (confirm_password !== password) {
    message_block("reset_pass_message", "Passwords do not match!", 5);
    reset_block("reset_pass_message", 5);
    return;
  }

  if (
    username === "" ||
    password === "" ||
    confirm_password === "" ||
    reset_token === ""
  ) {
    message_block("reset_pass_message", "Please fill all fields", 5);
    reset_block("reset_pass_message", 5);
    return;
  }

  fetch("/reset_pass", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
      reset_token: reset_token,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        message_block("reset_pass_message", data.error);
        reset_block("reset_pass_message");
      } else {
        message_block("reset_pass_message", data.message);
        reset_block("reset_pass_message");

        // Redirect to login page
        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      }
    });
}
