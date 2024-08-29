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

function login() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  if (username === "" || password === "") {
    message_block("login_message", "Please fill all fields", 5);
    reset_block("login_message", 5);
    return;
  }

  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        message_block("login_message", data.error);
        reset_block("login_message");
      } else {
        message_block("login_message", data.message);
        reset_block("login_message");

        setTimeout(() => {
          localStorage.setItem("JWT", data.token);
          window.location.href = "/sings";
        }, 5000);
      }
    });
}
