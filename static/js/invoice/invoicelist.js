$( document ).ready(function() {
    var notyf = new Notyf({
        duration: 2000,
        position: {
          x: 'right',
          y: 'top',
        },
        types: [
          {
            type: 'success',
            background: '#D3D3D',
            icon: {
              className: 'fa fa-check-circle',
              tagName: 'i',
              color: '#000',
            },
          },
        ]
      });
  
    var msg=$('.msg-cls').text();
    if (msg){
      notyf.open({
      type: 'success',
      message: msg,
    }); 
    }
  })

  function convertDateFormat(dateString) {
    var parts = dateString.split('-');
    return parts[2] + '-' + parts[1] + '-' + parts[0];
}     


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
      url: "/invoice/getinvoicedetails",                    
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
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.invoice_num).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.submit_date).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.approval_status).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.approval_date).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.payment_status).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
         $(data.payment_date).each(function(ind,val){
         actions_html+='<div>'+val+'</div>'
         })
     return actions_html  
     }
    },
    { data: "status" },
    {
      data: null,
     render: function (data, type, row) {
      actions_html=''
      actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a>'

      if (data.invoice_invoice_status == 4){
         if(data.user_id == 3 || data.user_id == 2){
            if(data.haspermission_invoicerecipt > 0){
              actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a><a href="/invoice/invoicequeryhistory/'+data.id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
            }
         }else{
            if(data.vendorid_active_status == 1){
                if(data.inv_count == 0){
                  actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a><a href="/invoice/invoicequeryhistory/'+data.id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
                }
            }
         }
      }
      else {
        if(data.query_status>0){
          actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a><a href="/invoice/invoicequeryhistory/'+data.id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
        }else{
          if(data.query_history_status == 1){
            actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a><a href="/invoice/invoicequeryhistory/'+data.id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
          }
        }
    }

      if (data.vendorid_active_status == 1){
        if(data.vendor_status == true){
           if(data.invoice_invoice_status == 1){
              if( data.invoice_wcc_id != null){
                actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a> <a class="btn px-1" href="/invoice/editinvoiceform/'+data.id+'/1?wcc_id='+data.invoice_wcc_id+'"><i class="fa fa-edit" ></i></a>'
              }else{
                actions_html='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a> <a class="btn px-1" href="/invoice/editinvoiceform/'+data.id+'/1"><i class="fa fa-edit" ></i></a>'
              }
           }
        }
      }
     return actions_html  
     }
    },

  ],
  initComplete: function(settings, json) {
    // Hide the loader once DataTable is initialized and data is rendered
    $('#loader').hide();
}
})
})