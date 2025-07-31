
$(document).ready(function(){
  
    if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
      window.location.href = `${scheme}://${gethost}/finance/listdetails`
    } 
    // window.location.href = `${scheme}://${gethost}/invoiceguard/listflow/?pageperdata=${value}`
});

  // $(".changevalue").change(function(){
  //       window.location.href = `{{scheme}}://{{gethost}}/finance/listdetails/?pageperdata=${$(this).val()}`
  //   });
    $(document).ready(function() {
        const queryString = window.location.search;
        const parameters = new URLSearchParams(queryString);
        const value = parameters.get('pageperdata');
        if(value!=null){    
        $('.changevalue').val(value)
        }
        else{
            $('.changevalue').val(10)
        }
    });

    $('input').on('change',function() {
      const queryString = window.location.search;
      const parameters = new URLSearchParams(queryString);
      const value = parameters.get('q');
        if(value!=null && $(this).val() == '') {
            window.location.href = `{{scheme}}://{{gethost}}/finance/listdetails/`
        }
    });

    $(document).on("click", ".delete_bank", function (e) {
      var bank_name = $(this).attr('bank_name');
      var bank_id = $(this).attr('data-id');
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
          url:`/finance/companybankdelete/${bank_id}/`,
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
    //search and pagination

    
$(document).on('input', "#myInput", function () {
     let query = $(this).val()
    let pageperdata = $('#datafilters').val()
    setTimeout(function () {
        searchBank(query,1,pageperdata)
    }, 100);
});


$(document).on('click','.pg-circle',function(e){
    e.preventDefault();
    let query = $('#myInput').val();
    let page = $(this).attr('data-id')
    let pageperdata = $('#datafilters').val()
    
    searchBank(query,page,pageperdata)
})

$(document).on('change','#datafilters',function(e){
    let query = $('#myInput').val();
    //let page = $(this).attr('data-id')
    let pageperdata = $(this).val()
    searchBank(query,1,pageperdata)
});

function searchBank(query,page,pageperdata) {
  console.log({'val':query,page,pageperdata})
    $.ajax({
        url: "/finance/listdetails/",
        headers: { 'X-CSRFToken': csrf_token },
        data: {
            'q': query,
            'page':page,
            'pageperdata':pageperdata
        },
        type: 'POST',
        success: function (response) {
            if (response.status) {
                console.log('right')
                console.log(response)
                $('section').replaceWith(response.html)
                let focusElement = $(document).find('#myInput')
                let elementLength = focusElement.val().length;
                focusElement[0].focus();
                focusElement[0].setSelectionRange(elementLength,elementLength);
                $('#datafilters').val($('.entries').val())
            } else {
                console.log('wrong')
            }
        },
        error: function () {
            // Error message
        }
    });
}

