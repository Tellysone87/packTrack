// javascript file to catch when the user clicks any buttons on the site

// I will use event listerner to wait until the user interacts with any buttons 
// or prompts and then call the specified function.

// first I will set it up for the homepage submit button.
// if submit button is pressed, I need the sign in page rendered. 
const sign_in_button = document.querySelector('#sign_in');

function redirect_to_signin_page()
{
    // window.location
}

sign_in_button.addEventListener('click', redirect_to_signin_page);