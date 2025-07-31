$(document).on('click','.chk-report-box',function(){
    reportname = $(this).attr('name')
    status = $(this).is(':checked')
    if(status=='true'){
      status='True'
    }
    else{
      status='False'
    }
    $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token},
            url:`/invoice/starredreport`,
            data: {
                 'reportname':reportname,
                 'status':status
                  },
          
          })
          location.reload();
        })


      $(document).on('click', '.add_btn', function() {
        if (currency_count == 0) {
            new swal({
                title: "Update General Settings",
                button: "Ok",
            }).then((result) => {
                if (result.isConfirmed) {
                    document.location.href = generalSettingUrl;
                }
            });
            return false;
        }
    });
    
                