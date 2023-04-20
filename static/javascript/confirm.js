// function to verify if user wants to update their profile
document.querySelector('#update_profile').addEventListener('submit',(evt) => {
    check = confirm('Are you sure you want to update your profile?');
    if(check === false){
        evt.preventDefault(); /* prevent default actions to update profile*/
    };
});