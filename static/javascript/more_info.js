// // javascript file to diplay the tracking history when the more button is clicked
const table = document.querySelector("#history_tab")
const table_appear = document.getElementById("history_tab")
let data_showing = false //sets the newly loaded page history data to false
let info_buttons = document.querySelectorAll('#more_info')

for (const button of info_buttons) {

    button.addEventListener('click', (evt) => {
        evt.preventDefault();

        if (data_showing === false) {
            const formInputs = {
                track_pack: button.dataset.tracking
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

                    // Add the table headers in before the loop
                    table.insertAdjacentHTML('beforeend', "<th>Dates</th><th>Events</th><th>Locations</th>")
                    for (let i in responseJson) {
                        table.insertAdjacentHTML('beforeend',`<tr><td> ${responseJson[i]['date']}</td>
                        <td> ${responseJson[i]['event']} </td>
                        <td> ${responseJson[i]['location']} </td></tr>`);
                        i++;
                    };
                    table_appear.style.visibility = "visible";
                    data_showing = true // history data is now loaded
                });
        }
        else if (data_showing === true) {

            table_appear.style.visibility = "hidden";
            table.innerHTML = "";
            data_showing = false // history data is now loaded
        }
    });
}


