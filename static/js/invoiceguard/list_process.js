var scheme = $('.scheme').val()
var gethost = $('.gethost').val()
var csrf_token = $('.csrf_token').val()


/*

$(".changevalue").change(function () {
    var value = $(this).val()
    // console.log(`hello ${value}`)
    window.location.href = `${scheme}://${gethost}/invoiceguard/listprocess/?pageperdata=${value}`
    // console.log(`${scheme}://${gethost}/invoiceguard/listprocess/?pageperdata=${value}`)
});
$(document).ready(function () {
    // alert(scheme)
    // alert(gethost)
    // alert(csrf_token)
    const queryString = window.location.search;
    const parameters = new URLSearchParams(queryString);
    const value = parameters.get('pageperdata');
    if (value != null) {
        $('.changevalue').val(value)
    }
    else {
        $('.changevalue').val(10)
    }
});

// when user press enter key in search input field sumbit form
$('input').on('keypress',function(e) {
    if(e.which == 13) {
        $('form').submit();
    }
});
*/

// when search box is empty then remove search query string from url
$('input').on('change', function () {
    const queryString = window.location.search;
    const parameters = new URLSearchParams(queryString);
    const value = parameters.get('q');
    if (value != null && $(this).val() == '') {
        window.location.href = `scheme://gethost/invoiceguard/listprocess/`
    }
});



$(document).on('input', "#myInput", function () {
    let query = $(this).val()
    let pageperdata = $('#datafilters').val()
    setTimeout(function () {
        searchProcess(query,1,pageperdata)
    }, 100);
});


$(document).on('click','.pg-circle',function(e){
    e.preventDefault();
    let query = $('#myInput').val();
    let page = $(this).attr('data-id')
    let pageperdata = $('#datafilters').val()
    searchProcess(query,page,pageperdata)
})

$(document).on('change','#datafilters',function(e){
    let query = $('#myInput').val();
    //let page = $(this).attr('data-id')
    let pageperdata = $(this).val()
    searchProcess(query,1,pageperdata)
});

$(document).on("click", ".delete_tax", function (e) {
    e.preventDefault();
    //let url = $(this).data('id');
    let name = $(this).closest('tr').find('.del_class').text()
    console.log({ 'name': csrf_token })
    //var pk = $(this).data('data-id');
    var pk = $(this).attr('data-id');
    console.log({ 'pk': pk })
    //let name = $(this).attr('data-name');
    Swal.fire({
        title: 'Do You Want To Delete ' + name + ' ?',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, I Confirm',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            //return window.location.href = 'delete-userdepartment-form/'+url;
            $.ajax({
                url: "/invoiceguard/deleteprocess/",
                headers: { 'X-CSRFToken': csrf_token },
                data: {
                    'pk': pk
                },
                type: 'POST',
                success: function (response) {
                    if (response.status) {
                        console.log('right')
                        // reload the page
                        window.location.reload();
                        // Success message
                    } else {
                        console.log('wrong')
                    }
                },
                error: function () {
                    // Error message
                }
            });
        }
    });
    return false;
});


// ajax call for edit process
//var pk = $(this).attr('data-id');
//console.log({'pk':pk})

function searchProcess(query,page,pageperdata) {
    $.ajax({
        url: "/invoiceguard/listprocess/",
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

$(document).ready(function() {
    $(".showtoggle").on('click', function() {
      let nxttr = $(this).closest('tr').next('tr');
      $(this).closest('table tbody').find('.collapse').not(nxttr.find('.collapse')).removeClass('show');
    });
  
  });