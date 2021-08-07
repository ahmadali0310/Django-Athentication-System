/**
 * * These Are All the selectors that we need for form validation and submission.
 * */

const first_name = document.querySelector(".first_name");
const last_name = document.querySelector(".last_name");
const email = document.querySelector(".email");
const pass1 = document.querySelector(".pass1");
const pass2 = document.querySelector(".pass2");
const form = document.getElementById("form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

/**
 *
 * @param {How many characters you want to validate a specific input field.} length
 * @param {Which Input field you want to validate} input
 * @returns
 */
const check_length_of_input = (length, input) => {
  if (input.value.length < length) {
    alert(`Minimum ${length} characters needed in ${input.classList}`);
    return false;
  } else {
    return true;
  }
};

/**
 *
 * @param {value of password.} pass1
 * @param {value of Confirm Password.} pass2
 * @returns
 */
const check_passwords = (pass1, pass2) => {
  if (pass1 != pass2) {
    alert(`Passwords do not match`);
    return false;
  } else {
    return true;
  }
};

/**
 *
 * @param {The input field which you want to validate for email.} input
 * @returns
 */
const ValidateEmail = (input) => {
  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (input.value.match(mailformat)) {
    return true;
  } else {
    alert("You have entered an invalid email address!");
    return false;
  }
};

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
 * * The Event listener on form submission.
 */
form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (check_length_of_input(3, first_name)) {
    if (check_length_of_input(3, last_name)) {
      if (ValidateEmail(email)) {
        if (check_length_of_input(8, pass1)) {
          if (check_length_of_input(8, pass2)) {
            if (check_passwords(pass1.value, pass2.value)) {
              let data = new FormData(); //* Form data which will be passed to backend through ajax call.
              data.append("firstName", first_name.value);
              data.append("lastName", last_name.value);
              data.append("email", email.value);
              data.append("pass", pass1.value);

              //* This class added to the backdrop class
              document.querySelector(".back_drop").classList.add("active");

              // * This is for opacity transition;
              setTimeout(() => {
                document.querySelector(".back_drop").classList.add("opacity");
              }, 300);

              //* Ajax Call Axios
              axios({
                method: "post",
                url: "/",
                data: data,
                headers: { "X-CSRFToken": csrf[0].value },
              })
                .then((res) => {
                  // * For removing back_drop
                  document
                    .querySelector(".back_drop")
                    .classList.remove("active");
                  document
                    .querySelector(".back_drop")
                    .classList.remove("opacity");

                  // * If success message is coming from server then it will show success message with green background
                  if (res.data.success) {
                    // * Create the p node and add text to the this node and then append to the parent node
                    console.log(res.data.success);
                    let node = document.createElement("p");
                    let textnode = document.createTextNode(
                      `${res.data.success}`
                    );
                    node.appendChild(textnode);
                    document.querySelector(".message").appendChild(node);
                    document
                      .querySelector(".message")
                      .classList.add("active_success");

                    // * reset all the input fields
                    first_name.value = "";
                    last_name.value = "";
                    email.value = "";
                    pass1.value = "";
                    pass2.value = "";

                    // * Remove message from user interface
                    setTimeout(() => {
                      document
                        .querySelector(".message")
                        .classList.remove("active_success");
                      document
                        .querySelector(".message")
                        .removeChild(document.querySelector(".message > p"));
                    }, 3000);
                  }
                  // * It will run if there is any error
                  else if (res.data.error) {
                    // * Create the p node and add text to the this node and then append to the parent node
                    let node = document.createElement("p");
                    let textnode = document.createTextNode(`${res.data.error}`);
                    node.appendChild(textnode);
                    document.querySelector(".message").appendChild(node);
                    document
                      .querySelector(".message")
                      .classList.add("active_danger");
                    // * Remove message from user interface
                    setTimeout(() => {
                      document
                        .querySelector(".message")
                        .classList.remove("active_danger");
                      document
                        .querySelector(".message")
                        .removeChild(document.querySelector(".message > p"));
                    }, 3000);
                  }
                })
                .catch((err) => {
                  //* This class removing the backdrop class
                  document
                    .querySelector(".back_drop")
                    .classList.remove("active");
                  document
                    .querySelector(".back_drop")
                    .classList.remove("opacity");

                  // * Create the p node and add text to the this node and then append to the parent node
                  let node = document.createElement("p");
                  let textnode = document.createTextNode(
                    `There is Error in the server. Try again.`
                  );
                  node.appendChild(textnode);
                  document.querySelector(".message").appendChild(node);
                  document
                    .querySelector(".message")
                    .classList.add("active_danger");
                  // * Remove message from user interface
                  setTimeout(() => {
                    document
                      .querySelector(".message")
                      .classList.remove("active_danger");
                    document
                      .querySelector(".message")
                      .removeChild(document.querySelector(".message > p"));
                  }, 3000);
                });
            }
          }
        }
      }
    }
  }
});

