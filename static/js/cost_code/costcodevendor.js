
$(document).on("click", ".delete", function (e) {
  e.preventDefault();
  var pk = $(this).closest('tr').find('.delete_data').attr('data-id');
  console.log({'pk':pk})
  Swal.fire({
      title: 'Do You Want To Delete?',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, I Confirm',
      cancelButtonText: 'No',
    }).then((result) => {
      if (result.isConfirmed) {
          //return window.location.href = 'delete-userdepartment-form/'+url;
          $.ajax({
              // url: '{% url "InvoiceGuard:delete-flow-form" %}',
              url: "/cost_code/deletevendorcostcode/",
              headers: {'X-CSRFToken': csrf_token },
              data: {
                  'pk': pk
              },
              type: 'POST',
              success: function(response) {
                  if (response.status) {
                      // reload the page
                      window.location.reload();
                      // Success message
                  } else {
                      // Error message
                  }
              },
              error: function() {
                  // Error message
              }
          });
        }
         });
  return false;
});

$(document).on('click','.err_popup',function(){
    Swal.fire({
      icon: 'error',
      title: 'Error...',
      text: 'Please Assign Cost Code To Vendor ',
      })
  })

// Access the URL from the data-url attribute
var costCodeMasterListUrl = $('script[src$="costcodevendor.js"]').data('url');

$(document).on('click', '.empty_list', function () {
  Swal.fire({
    text: 'Please add Cost Code information',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'OK',
  }).then((result) => {
    if (result.isConfirmed) {
      // Redirect to costcodemasterlist using the URL from data-url
      window.location.href = costCodeMasterListUrl;
    }
  });
});

  