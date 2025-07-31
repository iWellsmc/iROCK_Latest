$(document).ready(function() {
    $(".showtoggle").on('click', function() {

let nxttr = $(this).closest('tr').next('tr');
console.log(nxttr)
$(this).closest('table tbody').find('.collapse').not(nxttr.find('.collapse')).removeClass('show');
});

});