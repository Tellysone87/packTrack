// javascript file to catch when the user clicks any buttons on the site

// I will use event listerner to wait until the user interacts with any buttons 
// or prompts and then call the specified function.
// first I will set it up for the homepage submit button.
// if submit button is pressed, I the user prompted to check their email. 
const reset_link = document.querySelector('#reset_message');
const track_area = document.querySelector('#track_num');
const table = document.querySelector('#packages');
const message_area= document.querySelector("#rmessage")

//  function for event listener when the user submits a email
document.querySelector('#reset').addEventListener('submit', (evt) => {
    /*  This function is to display a messages to the user know when the reset email form is submittted.
    we are grabing the returned json from the reset_password Post route */

    evt.preventDefault(); /* prevent default actions to reload page */

    const formInputs = {

        email: document.querySelector('#email_field').value /* Pass this field value to the route using fetch */

    };

    //  send the fetch request to this server route
    fetch('/reset_password', {
        method: 'POST',
        body: JSON.stringify(formInputs), 
        headers: {
        'Content-Type': 'application/json',
        },
    })  
        /* Grab the response as a josn and use that data for my condition */
        .then((response) => response.json())
        .then((responseJson) => {

            if(responseJson.current_user === true){
                reset_link.innerHTML= "please check your email for reset link";
                message_area.remove();
            }

            else if(responseJson.current_user === false){
                message_area.innerHTML = "This email is not registered with an account. Please try again";
                
            }
    });
});

