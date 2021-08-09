const login_form = document.getElementById("login_form");
const login_email = document.querySelector(".login_email");
const login_pass = document.querySelector(".login_pass1");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

/**
 * * This will remove django default Messages from the user interface.
 */
django_default_msg = document.querySelector(".msg");

if (django_default_msg) {
  setTimeout(() => {
    django_default_msg.style.display = "none";
  }, 3000);
}

/**
 * * Event listener on login form which will collect the data from input fields and make an Ajax call to the server.
 */

login_form.addEventListener("submit", (e) => {
  e.preventDefault(); // * This will prevent the default behavior of submit form.

  let data = new FormData(); // * This is the data to be sent to the server
  data.append("email", login_email.value);
  data.append("password", login_pass.value);

  //* This class added to the backdrop class
  document.querySelector(".back_drop").classList.add("active");

  // * This is for opacity transition;
  setTimeout(() => {
    document.querySelector(".back_drop").classList.add("opacity");
  }, 300);

  // *  This is an Ajax call to login the user.
  axios({
    method: "POST",
    url: "/login/",
    data: data,
    headers: {
      "X-CSRFToken": csrf[0].value,
    },
  })
    .then((res) => {
      //  * If it return the success === true, then this block of code is executed otherwise the else part will be executed.
      if (res.data.success) {
        // * For removing back_drop
        document.querySelector(".back_drop").classList.remove("active");
        document.querySelector(".back_drop").classList.remove("opacity");

        // * redirect the user to the dashboard.
        window.location.replace(`${window.location.origin}/dashboard`);
      } else {
        // * For removing back_drop
        document.querySelector(".back_drop").classList.remove("active");
        document.querySelector(".back_drop").classList.remove("opacity");
        // * Create the p node and add text to the this node and then append to the parent node
        let node = document.createElement("p");
        let textnode = document.createTextNode(`Invalid Credentials`);
        node.appendChild(textnode);
        document.querySelector(".message").appendChild(node);
        document.querySelector(".message").classList.add("active_danger");
        // * Remove message from user interface
        setTimeout(() => {
          document.querySelector(".message").classList.remove("active_danger");
          document
            .querySelector(".message")
            .removeChild(document.querySelector(".message > p"));
        }, 3000);
      }
    })
    .catch((err) => {
      //  * if there is some other error then this will be executed immediately.
      document.querySelector(".back_drop").classList.remove("active");
      document.querySelector(".back_drop").classList.remove("opacity");
      // * Create the p node and add text to the this node and then append to the parent node
      let node = document.createElement("p");
      let textnode = document.createTextNode(`Error in the Server`);
      node.appendChild(textnode);
      document.querySelector(".message").appendChild(node);
      document.querySelector(".message").classList.add("active_danger");
      // * Remove message from user interface
      setTimeout(() => {
        document.querySelector(".message").classList.remove("active_danger");
        document
          .querySelector(".message")
          .removeChild(document.querySelector(".message > p"));
      }, 3000);
    });
});
