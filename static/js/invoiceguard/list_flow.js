
// $(".changevalue").change(function(){
//     var value = $(this).val()
//     window.location.href = `${scheme}://${gethost}/invoiceguard/listflow/?pageperdata=${value}`
// });

// $(document).ready(function() {
//     console.log({'csrf_token':csrf_token})
//     const queryString = window.location.search;
//     const parameters = new URLSearchParams(queryString);
//     const value = parameters.get('pageperdata');
//     if(value!=null){    
//     $('.changevalue').val(value)
//     }
//     else{
//         $('.changevalue').val(10)
//     }
// });
// when user press enter key in search input field sumbit form
// $('input').on('keypress',function(e) {
//     if(e.which == 13) {
//         $('form').submit();
//     }
// });
// when search box is empty then remove search query string from url
$(document).ready(function() {
    $(".showtoggle").on('click', function() {
      let nxttr = $(this).closest('tr').next('tr');
      $(this).closest('table tbody').find('.collapse').not(nxttr.find('.collapse')).removeClass('show');
    });
  
  });


$('input').on('change',function() {
  const queryString = window.location.search;
  const parameters = new URLSearchParams(queryString);
  const value = parameters.get('q');
    if(value!=null && $(this).val() == '') {
        window.location.href = `${scheme}://${gethost}/invoiceguard/listflow/`
    }
});

        $(document).on("click", ".delete_tax", function (e) {
        // var csrftoken = csrf_token
        console.log({'csrf_token':  csrf_token })
        e.preventDefault();
        let name = $(this).attr('data-name');
        var pk = $(this).attr('data-id');
        console.log({'pk':pk})
        Swal.fire({
            title: 'Do You Want To Delete '+name+' ?',
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
                    url: "/invoiceguard/deleteflow/",
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



$(document).on('click', '.role-cls', function() {
var id = $(this).attr('process_id');
$('.sub-main-cls').html('');
$('.projectblock-cls').removeClass('tree_menu active');
$(this).addClass('tree_menu active');
$(this).parent().parent().siblings().find('.role-cls').removeClass('hand-icon active')
$.ajax({
url: '/invoiceguard/getModule/',
headers: {'X-CSRFToken': csrf_token },
data: {
  'process_id': id
},
type: 'POST',
success: function(response) {
  console.log('id',id)
  var html = '';
  if (response.datas.length == 0) {
    html += '-';
  }
  $.each(response.datas, function(key, val) {
    html += '<div class="row"><div class="col-12 colum-line"><p class="tree-content hand-icon projectfield-cls prjt-viewfont">' + val.module_name + '</p></div></div>';
  });
  $('.role-right-cls-' + id + '').html(html);
},
error: function() {

}
});
});

$(document).on('input', "#myInput", function () {
   
   
    let query = $(this).val()
    let pageperdata = $('#datafilters').val()
    
    setTimeout(function () {
        searchList(query,1,pageperdata)
        }, 100);

});
$(document).on('click','.pg-circle',function(e){
    e.preventDefault();
    let query = $('#myInput').val();
    let page = $(this).attr('data-id')
    let pageperdata = $('#datafilters').val()
    console.log({'page':  page })
    searchList(query,page,pageperdata)
})
$(document).on('change','.changevalue',function(e){
    
    let query = $('#myInput').val();
    //let page = $(this).attr('data-id')
    let pageperdata = $(this).val()
    console.log({'csrf_tokensearchList':  pageperdata })
    searchList(query,1,pageperdata)
});

function searchList(query,page,pageperdata) {
    console.log({'csrf_tokensearchList':  pageperdata })
    $.ajax({
        url: "/invoiceguard/listflow/",
        headers: {'X-CSRFToken': csrf_token },
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
