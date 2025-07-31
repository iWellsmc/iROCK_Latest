$(document).ready(function() {
    $(document).on('change','#vendor_contracts',function(){
        var contract_id=$(this).val()
        var vendorId = $('#vendor_id').val();
        $.ajax({
            //     type: "GET",
              url: "/cost_code/getcostcodevalues",
              data: { 'vendorId':vendorId ,'contract_id':contract_id },
              success: function (data) {
                
                var tableBody = $('#table_cost_body');
                    tableBody.empty();  // Clear existing table rows
                    // Populate table rows with fetched data

                    if (data.data.length === 0) {
                        // If no data returned, show a message row
                        var noDataRow = '<tr><td colspan="3" class="text-center">---</td></tr>';
                        tableBody.append(noDataRow);
                    } else {
                    $.each(data.data, function(index, row) {
                        var newRow = '<tr>' +
                            '<td>' + row.serial_number + '</td>' +
                            '<td>' + row.costcode_preview + '</td>' +
                            '<td>' + row.code_category_paths + '</td>' +
                            '</tr>';
                        tableBody.append(newRow);
                    });
                }
              },
              error: function(xhr, status, error) {
                console.error('AJAX Error: ' + status + ' - ' + error);
            }
          })
    })
    })