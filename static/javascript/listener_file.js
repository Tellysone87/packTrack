// javascript file to catch when the user clicks any buttons on the site

// I will use event listerner to wait until the user interacts with any buttons 
// or prompts and then call the specified function.
// first I will set it up for the homepage submit button.
// if submit button is pressed, I the user prompted to check their email. 
const reset_link = document.querySelector('#reset');
const track_area = document.querySelector('#track_num');
const table = document.querySelector('#packages');
alert('here');

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
            if (responseJson.current_user === true){
                reset_link.innerHTML= "please check your email for reset link";
                message_area.remove();
            };
            if (responseJson.current_user === false){
                message_area.innerHTML = "This email is not registered with an account. Please try again"
                
            };
    });
});

// document.querySelector('#more_info').addEventListener('click', (evt) => {
//     evt.preventDefault();

//     const formInputs = {

//         track_pack: document.querySelector('#track_num').innerHTML

//     };

//     fetch('/history', {
//         method: 'POST',
//         body: JSON.stringify(formInputs),
//         headers: {
//         'Content-Type': 'application/json',
//         },
//     })
//         .then((response) => response.json())
//         .then((responseJson) => {
//             alert(responseJson.text)
           
//     });
// });

const button = document.querySelector("#more_info");

const handleClick = () => {
    alert('More info button!');
  };
  
button.addEventListener('click',handleClick);