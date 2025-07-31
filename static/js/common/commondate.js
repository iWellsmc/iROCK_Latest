$(document).ready(function() {
    var datetime=$('.local_time').attr('login_date')
    if (datetime && moment.unix(datetime).isValid()) {
        const date = moment.unix(datetime).format('DD-MMM-YYYY');
        const time = moment.unix(datetime).format('hh:mm A');
        const dateTimeString = date + " at " + time;

        $('.local_time').text(dateTimeString);
    }

    
  
})