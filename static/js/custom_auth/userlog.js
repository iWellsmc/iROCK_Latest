

    
    $(document).ready( function () {
        var company_id = $('.company_id').val();
         $('#user_log').DataTable({
             serverSide: true,
             searching: false,
             language: {
                          emptyTable: "---"
                },
         ajax: {
             url: "/user_log_datatable",                   
             type: 'GET',
         },
        
     
         columns: [
             { data: null, className: "serial-number", orderable: false, searchable: false },
             { data: 'Message' },
             { data: 'Source Name' },
             { data: 'Source Type' },
             { data: 'Created By' },
             { data: 'Date'},
            
       
         ],
         rowCallback: function (row, data, index) {
            var api = this.api();
            var startIndex = api.page() * api.page.len();
            var serialNumber = startIndex + index + 1;
            $('td.serial-number', row).html(serialNumber);
        }
     });
     
      
     });


