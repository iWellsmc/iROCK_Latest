
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
                case 'Sno':
                    A = $(a).children('td').eq(0).text().toUpperCase();
                    B = $(b).children('td').eq(0).text().toUpperCase();
                    break;
                case 'inv-num':
                    A = $(a).children('td').eq(1).text().toUpperCase();
                    B = $(b).children('td').eq(1).text().toUpperCase();
                    break;
                case 'submit-date':
                    A = new Date(convertDateFormat($(a).children('td').eq(2).text())).getTime();
                    B = new Date(convertDateFormat($(b).children('td').eq(2).text())).getTime();
                    break;
                case 'approval':
                    A = $(a).children('td').eq(3).text().toUpperCase();
                    B = $(b).children('td').eq(3).text().toUpperCase();
                    break;
                case 'appr-date':
                    A = new Date(convertDateFormat($(a).children('td').eq(4).text())).getTime();
                    B = new Date(convertDateFormat($(b).children('td').eq(4).text())).getTime();
                    break;
                case 'pay-status':
                    A = $(a).children('td').eq(5).text().toUpperCase();
                    B = $(b).children('td').eq(5).text().toUpperCase();
                    break;
                case 'pay-date':
                    A = new Date(convertDateFormat($(a).children('td').eq(6).text())).getTime();
                    B = new Date(convertDateFormat($(b).children('td').eq(6).text())).getTime();
                    break;
                case 'status':
                    A = $(a).children('td').eq(7).text().toUpperCase();
                    B = $(b).children('td').eq(7).text().toUpperCase();
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




// insert table records
$(document).ready(function() {
    $('#loader').show();
$('#master_project_list').DataTable({
    serverSide: true,
    ajax: {
        url: "/wcc/getallwcc",                    
        type: 'GET',
    },
    language: {
      emptyTable: "---"
    },
    "rowCallback": function(row, data) {
      $(row).attr('data-id', data.id);
    },
    columns: [
        { data: "s_no" },
        { data: "wcc_num" },
        { data: "period_Service" },
        { data: 'submit_date' },
        { data: "approval_status" },
        { data: "approval_date"},
        { data: "invoice_status" },
        { data: "status" },
        {
            data: null,
           render: function (data, type, row) {
            actions_html=''
            actions_html +='<a class="btn px-1" href="/wcc/wccview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a>'
            if(data.vendorid_active_status == 1){
                if(data.vendor_status == true){
                    if(data.wcc_status != 1){
                        actions_html +=' <a class="btn px-1" href="/wcc/wcceditformone/'+data.id+'"><i class="fa fa-edit" title="edit"></i></a>'
                    }
                }
                if(data.wcc_wcc_status == 1){
                    if(data.wcc_data_count == 0){
                        actions_html +='<a class="btn px-1" href="/invoice/createinvoice?wcc_id='+data.id+'"><i class="fa-solid fa-file-invoice" title="Submit Invoice"></i></a>'
                    }
                }                      
            }
            if(data.return_query_stataus == 1){
                actions_html +=' <a class="btn his-oty px-1" href="/wcc/wccqueryhistory/'+data.id+'"> <i class="fa fa-history" title="History" aria-hidden="true"></i></a>'   
            }
           return actions_html  
           }
        },

    ],  initComplete: function(settings, json) {
        // Hide the loader once DataTable is initialized and data is rendered
        $('#loader').hide();
    }
})
});