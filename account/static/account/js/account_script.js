function calendarDateAdd(today_day, today_weekday, current_month, max_day_month){
    let date_dict = {};
    let start_day = today_day;
    switch(today_weekday) {
        case 0:
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 1:
            start_day = today_day - 1;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 2:
            start_day = today_day - 2;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 3:
            start_day = today_day - 3;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 4:
            start_day = today_day - 4;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 5:
            start_day = today_day - 5;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
        case 6:
            start_day = today_day - 6;
            for (let i = 1; i < 8; i++){
                date_dict[i] = start_day;
                if (start_day === max_day_month){
                    start_day = 0
                }
                start_day += 1;
            }
            helpFunctionWeekCalendar(date_dict, current_month);
            break;
    }
    return date_dict
}

function helpFunctionWeekCalendar(data_dict, current_month){
    let elements = document.getElementById('monday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "Понеділок") {
            if (current_month < 10){
                current_month_monday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[1]}`;
            elements[i].innerHTML = `Понеділок ${data_dict[1]}.${current_month_monday}`;
        }
        break;
    }
    elements = document.getElementById('tuesday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "Вівторок" ) {
            if (data_dict[1] > data_dict[2]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_tuesday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[2]}`;
            elements[i].innerHTML = `Вівторок ${data_dict[2]}.${current_month_tuesday}`;
        }
        break;
    }
    elements = document.getElementById('wednesday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "Середа" ) {
            if (data_dict[2] > data_dict[3]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_wednesday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[3]}`;
            elements[i].innerHTML = `Середа ${data_dict[3]}.${current_month_wednesday}`;
        }
        break;
    }
    elements = document.getElementById('thursday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "Четвер" ) {
            if (data_dict[3] > data_dict[4]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_thursday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[4]}`;
            elements[i].innerHTML = `Четвер ${data_dict[4]}.${current_month_thursday}`;
        }
        break;
    }
    elements = document.getElementById('friday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "П'ятниця" ) {
            if (data_dict[4] > data_dict[5]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_friday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[5]}`;
            elements[i].innerHTML = `П'ятниця ${data_dict[5]}.${current_month_friday}`;
        }
        break;
    }
    elements = document.getElementById('saturday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (elements[i].innerHTML === "Субота" ) {
            if (data_dict[5] > data_dict[6]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_saturday = '0' + current_month;
            }
            elements[i].abbr = `${data_dict[6]}`;
            elements[i].innerHTML = `Субота ${data_dict[6]}.${current_month_saturday}`;
        }
        break;
    }
    elements = document.getElementById('sunday_time').getElementsByTagName("td");
    for (let i = 0; i < elements.length; i += 1) {
        if (data_dict[6] > data_dict[7]){
                if (current_month < 11) {
                    current_month += 1;
                }
            }
            if (current_month < 10){
                current_month_sunday = '0' + current_month;
            }
        if (elements[i].innerHTML === "Неділя" ) {
            elements[i].abbr = `${data_dict[7]}`;
            elements[i].innerHTML = `Неділя ${data_dict[7]}.${current_month_sunday}`;
        }
        break;
    }
}

function labelTimeCreationForCabinet(tr_id, week_day_number){
    let arr = ['8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00',
               '15:00-16:00', '16:00-17:00', '17:00-18:00',	'18:00-19:00', '19:00-20:00', '20:00-21:00']
    arr.forEach(function(item, i, arr){
        document.getElementById(`${tr_id}`).innerHTML+= `<td id="${week_day_number}_${i+1}" class="time_day"></td>`;
    });
}
