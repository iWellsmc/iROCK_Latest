$(document).on('click','.add_btn',function(){
   if(currency_count == 0){
      new swal({
        title: "Update General Settings",
        button: "Ok",
      }).then(function() {
        var currentLocation = window.location.origin;
        window.location.href =  currentLocation + '/generalsetting/'+comp_ids+'/'
    });
      return false
    }
})

$(document).on('click','.action-delete',function(){
  var bank_name = $(this).closest('tr').find('.delete_bank').attr('bank_name');
  var bank_id = $(this).closest('tr').find('.delete_bank').attr('data-id');
Swal.fire({
  title: `Are you sure you want to delete ${bank_name} details?`,
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, I Confirm',
  cancelButtonText: 'No',
}).then((result) => {
  if (result.isConfirmed) {
    $.ajax({
      url:`/finance/deletebankuser/${bank_id}/`,
      data: {
           'csrfmiddlewaretoken': csrf_token ,
            },
      type: "POST",
      success: function (data) {
        if(data.status){
          location.reload();  
        }          
      }
    });
  }
})

})

