let wcc_check=Number($('#wcc_check').val());
$(function() {
    if (wcc_check > 0){
        Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'WCC Approval Inprogress',
            showConfirmButton: true,
            timer:6000
            }).then(function() {
                window.history.back();
            });
    }
})
$(document).on('click','.addbtn',function(){
  console.log('Addbtn')
    let sno = parseInt($('.invoice_trigger tbody tr:last').text())+1
    let invoicefromday = parseInt($('.invoice_trigger tbody tr:last').find('.invoicetodate').val())
    let invoicetoday = invoicefromday+1
    console.log('invoicefromday',invoicefromday)
    if(invoicefromday < 0 || isNaN(invoicefromday)){
      console.log('if--')
        Swal.fire("Enter Wcc Payment To Day")
    }
    else{
      console.log('else--')
    let add_field = `<tr><td>${sno}</td><input type="hidden" name="pk" class="form-control" value=0><td><input type="text"name="payment_terms_from"class="form-control invoicefromdate"  value=${invoicetoday} readonly ></td><td><input type="text" name="payment_terms_to"class="form-control invoicetodate"></td><td><input type="text"class="form-control" value="Day" readonly><input type="hidden" name="time_unit" class="form-control" value="1" readonly></td><td class="d-flex"><input type="text" name="time_allotted" class="form-control time_allotted"><button id="delete-user" class="ml-2 btn btn-clr delete-btn"type="button" value="delete"><i class="fa fa-minus"></i></button></td><tr>`
    $('table').append(add_field)
    }
})

$(document).on('change','.invoicetodate',function(){
   let fromval = $(this).closest('tr').find('.invoicefromdate').val()
  if(parseInt($(this).val()) <= fromval){
    Swal.fire('To Day Must Be Greater Than From Day')
    $(this).val('')
  }
  if(parseInt($(this).val()) > 365){
    Swal.fire('To Day Must Be Less Than 365')
    $(this).val('')
  }
})


$(document).on('keyup','.invoicetodate',function(){
  var $th = $(this);
  $th.val($th.val().replace(/[^0-9]/g, ''))
})

function getMaxValue(timeUnit) {
  if (timeUnit === '0') {
      return 72;
  } else if (timeUnit === '1') {
      return 3;
  } else if (timeUnit === '2') {
      return 4320;
  }
}
$(document).ready(function () {
  
  // Initialize the form validation
  var validator = $('.editwcctriggertime_form').validate({
      rules: {
          time_allotted: {
              required: true,
              range: [1, getMaxValue()]
          }
      },
      messages: {
          time_allotted: {
              required: 'Please enter a value.',
              range: 'Choose a value between 1 and ' + getMaxValue() + '.'
          }
      }
  });
  let time_units_selected = $('.time_unit').find(':selected').val();
  validator.settings.rules.time_allotted.range = [1, getMaxValue(time_units_selected)];
  validator.settings.messages.time_allotted.range = 'Choose a value between 1 and ' + getMaxValue(time_units_selected) + '.';
  // Update validation rules when time_unit changes
  $(document).on('change', '.time_unit', function () {
      // Get the selected value from the time_unit dropdown
      var selectedTimeUnit = $(this).val();

      // Update the validation rules based on the selected time_unit
      validator.settings.rules.time_allotted.range = [1, getMaxValue(selectedTimeUnit)];
      validator.settings.messages.time_allotted.range = 'Choose a value between 1 and ' + getMaxValue(selectedTimeUnit) + '.';
  });

  // Submit event handler
  $(document).on('submit', '.editwcctriggertime_form', function (event) {
      // Prevent the form from submitting initially
      event.preventDefault();

      // Trigger form validation
      if ($(this).valid()) {
          // Form is valid, proceed with submission
          // Uncomment the line below to submit the form
          this.submit();
      } else {
          // Form is invalid, you can show an error message or take other actions
          // alert('Form is invalid');
      }
  });

 
});

$(document).on('click','.delete-btn',function(){
  console.log('fid',$(this).closest('tr'))
  $(this).closest('tr').nextAll('tr').remove()
  $(this).closest('tr').remove()
})

$(document).on('change','.invoicetodate',function(){
  $(this).closest('tr').nextAll('tr').remove()
 })


$(document).on('click', '.mainsave', function(e){

  $('input').each(function(index,val) {
    if ($(this).val() == '') {
      $(this).addClass('con_error')
    }else{
      $(this).removeClass('con_error')
    }
  })

  if ($('.con_error').length > 0) {
    return false
}
// }
})