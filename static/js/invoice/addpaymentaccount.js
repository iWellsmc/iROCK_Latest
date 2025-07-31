$(document).on('change','#vendor_id',function(){

})

$(document).ready(function() {
  $('#vendor_id').select2({
       placeholder: "Select Vendor",
      });
      $('#currency').select2({
        placeholder: "Select Currency",
       });
    })

    $(document).on('click', '.add-btn', function () {
      //  var appendRow = '<tr class="tr_row">' +
      //                       '<td><input type="text" class="form-control amount" value="" placeholder="Amount"></td>' +
      //                       '<td><input type="file" class="form-control file file_1" value=""></td>' +
      //                       '<td><button id="add" class="btn btn-clr add-btn add" type="button" value="Add"><i class="fa fa-plus"></i></button></td>' +
      //                       '<td class="col-md-4"><button class="btn btn-clr remove_btn" type="button" value="Minus"><i class="fa fa-minus"></i></button></td>' +
      //                   '</tr>';
      var appendRow = '<div class="row tr_row my-3">' +
                            '<div class="col-md-4"><input type="text" class="form-control amount" value="" placeholder="Amount"></div>' + 
                            '<div class="col-md-4"><input type="file" class="form-control file file_1 filesize" value=""><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></div>' +
                            '<div class="col-md-4 minus-btn"><button id="add" class="mr-2 btn btn-clr add-btn add" type="button" value="Add"><i class="fa fa-plus"></i></button><button class="btn btn-clr remove_btn" type="button" value="Minus"><i class="fa fa-minus"></i></button></div>'
                        '</div>'
        
      $('.tablefield').append(appendRow);
      
  });
  
  $(document).on('click', '.remove_btn', function () {
       $(this).parent().parent().remove();
  });
  
    



$(document).on('click','.generate_report',function(){
  $('.inputfield').val('1')
})
$(document).on('click','.delete_paymentact',function(){
  paymentact_id=$(this).attr('data-id')
  Swal.fire({
    title: `Are you sure you want to delete details?`,
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, I Confirm',
    cancelButtonText: 'No',
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url:`/invoice/delete_paymentact/${paymentact_id}`,
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
  });

 

$(document).on('click', '.generate_report-1', function(e){
  var anyEmpty = false;

  $('.file_1').each(function(index, element) {
    if ($.trim($(element).val()) == '') {
      anyEmpty = true;
      $(element).addClass('con_error');
    } else {
      $(element).removeClass('con_error');
    }
  });

  if (anyEmpty) {
    e.preventDefault(); 
  }

});

$(document).on('input', '.file_1', function(index, element) {
  var inputValue = $(this).val();
  $('.file_1').each(function(index, element) {
    if ($.trim($(element).val()) == '') {
      anyEmpty = true;
      $(element).addClass('con_error');
    } else {
      $(element).removeClass('con_error');
    }
  });

});


$(document).on('input', '.amount', function() {
  var inputValue = $(this).val();

  if (/^\d+(\.\d+)?$/.test(inputValue)) {
     $(this).removeClass('con_error');
  } else {
     $(this).addClass('con_error');
  }
});

$(document).on('click', '.generate_report-1', function(e){
  var anyInvalidInput = false;

  $('.amount').each(function(index, element) {
    var inputValue = $(element).val();

    if (!/^\d+(\.\d+)?$/.test(inputValue)) {
      anyInvalidInput = true;
      $(element).addClass('con_error');
    } else {
      $(element).removeClass('con_error');
    }
  });

  if (anyInvalidInput) {
    e.preventDefault();
  }
});

$(document).on('click', '.generate_report-1, .View-1', function(e) {
  var vendor_src = $('.vendor_src').next(".select2-container").find('.select2-selection__rendered').attr('title');

  if (vendor_src == undefined || vendor_src.trim() == '') {
    
    
    $(".select2-selection").css("border", "1px solid red");
    $('.generate_report-1').attr('disabled', 'disabled');
    e.preventDefault();
  } else {
    
    $(".select2-selection").css("border", "");
  }
});

$(document).on('change','.vendor_src',function(){
  $(this).next(".select2-container").find('.select2-selection').css("border", "");
 
});

$(document).on('change','.currency_src',function(){
  $(this).next(".select2-container").find('.select2-selection').css("border", "");
 
});

$(document).on('change', '.vendor_src, .currency_src', function () {
  var vendorValue = $('.vendor_src').next(".select2-container").find('.select2-selection__rendered').attr('title');
  var currencyValue = $('.currency_src').next(".select2-container").find('.select2-selection__rendered').attr('title');

  if (vendorValue === undefined || vendorValue.trim() === '') {
    $(".vendor_src").next(".select2-container").find('.select2-selection').addClass("con_error").css("border", "1px solid red");
  } else {
    $(".vendor_src").next(".select2-container").find('.select2-selection').removeClass("con_error").css("border", "");
  }

  if (currencyValue === undefined || currencyValue.trim() === '') {
    $(".currency_src").next(".select2-container").find('.select2-selection').addClass("con_error").css("border", "1px solid red");
    $('.generate_report-1').attr('disabled', 'disabled');
    $('.View-1').attr('disabled', 'disabled');
  } else {
    $(".currency_src").next(".select2-container").find('.select2-selection').removeClass("con_error").css("border", "");
    $('.generate_report-1').removeAttr('disabled');
    $('.View-1').removeAttr('disabled');
  }
});

$(document).on('click', ".add-btn", function() {
  $('.generate_report-1').attr('disabled', false); 
});


$(document).ready(function() {
  var submissionCount = 0;
  var maxSubmissions = 1; // Change this to the desired number of submissions

  $("form").submit(function(event) {
      submissionCount++;
      if (submissionCount >= maxSubmissions) {
          $(".generate_report-1").prop('disabled', true);
      }
  });
});


 


 










 
 



