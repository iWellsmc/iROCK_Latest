$('#comp_ven_invoice').DataTable({
  serverSide: true,
  ajax: {
      url: "/invoice/getunpaidinvoices",                    
      type: 'GET',
      data:{
          'payment_type':payment_type,
      }
  },
  language: {
      emptyTable: "---"
  },
  "rowCallback": function(row, data) {
      $(row).attr('data-id', data.id);
  },
  columns: [
      { data: 's_no' },
      { data: 'vin' },
      { data: 'vendor_name' },
      { data: 'service_name' },
      {
          data: null,
          render: function(data, type, row) {
              var actions_html = '';
              var paid_count = 0;
              $(data.instruction_number).each(function(ind, val) {
                  actions_html += '<div class="get_paid_invcost">' + val["cost_number"] + '<input type="hidden" id="inv_cost_id" value="' + val["cost_id"] + '"></div>';
                  paid_count++;
              });
              $(data.inv_number).each(function(ind, val) {
                  actions_html += '<div>' + val + '</div>';
              });
              actions_html += "<input type='hidden' class='input_tag' value='{\"id\":" + data.id + ", \"len\":" + paid_count + ", \"file\":[]}' >";
              return actions_html;
          }
      },
      {
          data: null,
          render: function(data, type, row) {
              var actions_html = '';
              $(data.date).each(function(ind, val) {
                  actions_html += '<div>' + val + '</div>';
              });
              return actions_html;
          }
      },
      {
          data: null,
          render: function(data, type, row) {
              var actions_html = '';
              $(data.approval_status).each(function(ind, val) {
                  actions_html += '<div>' + val + '</div>';
              });
              return actions_html;
          }
      },
      {
          data: null,
          render: function(data, type, row) {
              var actions_html = '';
              $(data.payment_status).each(function(ind, val) {
                  actions_html += '<div>' + val + '</div>';
              });
              return actions_html;
          }
      },
      {
          data: null,
          render: function(data, type, row) {
              var actions_html = '';
              actions_html += '<a class="btn px-1" href="/invoice/invoiceview/' + data.id + '"><i class="fa fa-eye" title="View"></i></a>';
              if (data.invoiceapproval_dispute > 0) {
                  actions_html += '<a class="btn his-oty px-1" href="/invoice/invoicequeryhistory/' + data.id + '"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>';
              }
              if (data.returned_user == 1) {
                  actions_html += '<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/checklist/' + data.id + '" data_id="' + data.id + '"><i class="fa-solid fa-list-check" title="Invoice Receipt"></i></a>';
              } else if (data.returned_user == 2) {
                  actions_html += '<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/invoiceapproval/' + data.id + '" data_id="' + data.id + '"><i class="fa-solid fa-file-invoice" title="Invoice Approval"></i></a>';
              }
              return actions_html;
          }
      }
  ],
  error: function(xhr, status, error) {
      console.error("DataTable initialization error:", error);
  }
});

