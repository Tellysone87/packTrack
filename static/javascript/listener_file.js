// javascript file to catch when the user clicks any buttons on the site

// I will use event listerner to wait until the user interacts with any buttons 
// or prompts and then call the specified function.

// first I will set it up for the homepage submit button.
// if submit button is pressed, I need the sign in page rendered. 
const reset_link = document.querySelector('#reset');
const message_area = document.querySelector('p#rmessage');

function display_reset_message()
{
    // window.location
    message_area.innerHTML="please check your email for reset link"
    alert('Stop clicking me!');

}

reset_link.addEventListener('submit', (evt) => {
    evt.preventDefault();
    display_reset_message()
});