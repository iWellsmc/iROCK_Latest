$(document).ready(function() {
    let index=1
//     let len_tr=$("#wcc_approval_list tbody tr").length
//     if(len_tr > 0){
//     $("#wcc_approval_list tbody tr").each(function(){
//         $(this).find('td:eq(0)').text(index);
//         index +=1;
//     });
// }
    let len_tr=$("#wcc_approval_list tbody tr.wcc_approved_details").length
    if(len_tr > 0){
        $("#wcc_approval_list tbody tr.wcc_approved_details").each(function(){
            $(this).find('td:eq(0)').text(index);
            index +=1;
        });
    }
})

$(document).ready(function() {
    $('.filter-btn').click(function() {
        var table = $(this).closest('table');
        var rows = table.find('tbody > tr').get();
        var idx = $(this).closest('th').index();
        var filter = $(this).data('filter');
        var icon = $(this).find('i');

        // Remove active class from other filter buttons
        $('.filter-btn').not(this).removeClass('active');

        // Toggle active class for the clicked filter button
        $(this).toggleClass('active');

        rows.sort(function(a, b) {
            var A, B;

            switch (filter) {
                case 'vin-number':
                    A = $(a).children('td').eq(1).text().toUpperCase();
                    B = $(b).children('td').eq(1).text().toUpperCase();
                    break;
                case 'vendor':
                    A = $(a).children('td').eq(2).text().toUpperCase();
                    B = $(b).children('td').eq(2).text().toUpperCase();
                    break;
                case 'wcc-number':
                    A = $(a).children('td').eq(3).text().toUpperCase();
                    B = $(b).children('td').eq(3).text().toUpperCase();
                    break;
                case 'peroid-service':
                    A = $(a).children('td').eq(4).text().toUpperCase();
                    B = $(b).children('td').eq(4).text().toUpperCase();
                    break;
                case 'submitted-date':
                    A = new Date(convertDateFormat($(a).children('td').eq(5).text())).getTime();
                    B = new Date(convertDateFormat($(b).children('td').eq(5).text())).getTime();
                    break;
                case 'approval-status':
                    A = $(a).children('td').eq(6).text().toUpperCase();
                    B = $(b).children('td').eq(6).text().toUpperCase();
                    break;
                default:
                    break;
            }

            // Determine sorting order based on the presence of 'fa-sort-up' or 'fa-sort-down' class
            if (icon.hasClass('fa-sort-up')) {
                return (A < B) ? 1 : -1;
            } else {
                return (A > B) ? 1 : -1;
            }
        });

        $.each(rows, function(index, row) {
            table.children('tbody').append(row);
        });

        // Toggle between 'fa-sort-up' and 'fa-sort-down' classes for the icon
        icon.toggleClass('fa-sort-up fa-sort-down');
        $(this).closest('th').siblings().find('i').removeClass('fa-sort-up fa-sort-down').addClass('fa-sort');
    });
});