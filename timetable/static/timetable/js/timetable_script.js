function labelTimeCreation(tr_id, week_day_number){
    let arr = ['8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00',
               '15:00-16:00', '16:00-17:00', '17:00-18:00',	'18:00-19:00', '19:00-20:00', '20:00-21:00']
    arr.forEach(function(item, i, arr){
        document.getElementById(`${tr_id}`).innerHTML+= `<td id="${week_day_number}_${i+1}" class="time_day"><input type="checkbox" name="${week_day_number}_${i+1}" value="${item}" hidden></td>`;
    });

}


function changeInputAndBackgroundTime(label_time, time) {
    if (document.getElementsByName(`${time}`)[0].checked === true){
        document.getElementsByName(`${time}`)[0].checked = false;
        label_time.style = "background: white";
    }else{
        label_time.style = "background: aquamarine";
        document.getElementsByName(`${time}`)[0].checked = true;
    }
}


function createCalendar(week_day, start_day, arr){
    document.getElementById(`${week_day}`).abbr = "1";
    document.getElementById(`${week_day}`).innerHTML = `1<input type="checkbox" name="${week_day}" value="1" hidden>`;
    arr.forEach(function(item, i, arr) {
        start_day += 1;
        document.getElementById(`week_day_${start_day}`).abbr = `${item}`;
        document.getElementById(`week_day_${start_day}`).innerHTML = `${item}<input type="checkbox" name="week_day_${start_day}" value="${item}" hidden>`;
    })
}


function changeInputAndBackgroundDate(th_label, name_input, today){
    if (document.getElementsByName(`${name_input}`)[0].checked === true  ){
        th_label.style = "background: white";
        document.getElementsByName(`${name_input}`)[0].checked = false;
    }else if (today < parseInt(th_label.abbr)){
        th_label.style = "background: aquamarine";
        document.getElementsByName(`${name_input}`)[0].checked = true;
    }
}

function defaultCheckedCheckboxTime(id_set){
    id_set.forEach(function(item, i, id_set){
        document.getElementsByName(`${item}`)[0].checked = true;
        document.getElementById(`${item}`).style = "background: aquamarine";
    })
}


function defaultCheckedCheckboxDate(data_list){
    let elements = document.getElementsByClassName(`week_day`);
    for (let key in data_list) {
        for (let i = 0; i < elements.length; i += 1) {
           if (elements[i].abbr === key ) {
             elements[i].style = "background: aquamarine"
             document.getElementsByName(`${elements[i].id}`)[0].checked = true;
          }
        }
    }
}

function todayLabelStyleChange(today_date){
    let elements = document.getElementsByClassName(`week_day`);

    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].abbr === today_date ) {
            elements[i].style.fontWeight = "bold";
            break
        }
    }
}
