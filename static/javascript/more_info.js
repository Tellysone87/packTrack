// // javascript file to diplay the tracking history when the more button is clicked
const date_row = document.querySelector("#dates")
const event_row = document.querySelector("#events")
const location_row = document.querySelector("#locations")
const table= document.querySelector("#history_tab")
const area=document.querySelector("#history_area")
const table_appear = document.getElementById("history_tab")
let data_showing = false //sets the newly loaded page history data to false

document.querySelector('#more_info').addEventListener('click', (evt) => {
    evt.preventDefault();
    
     
    const formInputs = {
        track_pack: document.querySelector('#track_num').innerHTML
    };
    fetch('/history', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
        'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            
            for(let i in responseJson){
                table.insertAdjacentHTML('beforeend',`<tr><td> ${responseJson[i]['date']}</td>
                <td> ${responseJson[i]['event']} </td>
                <td> ${responseJson[i]['location']} </td></tr>`);
                // console.log(responseJson[i]['date']);
                // console.log(responseJson[i]['event']);
                // console.log(responseJson[i]['location']);
                i++;
            };  
        table_appear.style.visibility ="visible";
        data_showing = true // history data is now loaded
    });
});