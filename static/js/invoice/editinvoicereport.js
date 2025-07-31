$(document).ready(function() {
    $('#country').select2({
       placeholder: "Select Country",
      });
      $('#project').select2({
       placeholder: "Select Project",
      });
      $('#discipline').select2({
       placeholder: "Select discipline",
      });
      $('#service').select2({
       placeholder: "Select Service",
      });
      $('#vendor').select2({
       placeholder: "Select Vendor",
      });
      $('#currency').select2({
       placeholder: "Select Currency",
      });
      $('#approval').select2({
       placeholder: "Select Approval Status",
      });
      $('#paymentstatus').select2({
       placeholder: "Select Payment Status",
      });
      $('#ageingperiod').select2({
       placeholder: "Select Ageing Period",
      });
    });

    $(document).on('focus',".dateformat-cls", function(){
      $(this).datepicker({
          dateFormat: 'dd-M-yy',
          maxDate:new Date(),
          changeMonth:true,
          changeYear:true,
          yearRange: '1900:+0',
      });
    });

$(document).on('click','.draftsave',function(){
      $('.submitfield').val('draft')
   })
$(document).on('click','.savebtn',function(){
    $('.submitfield').val('save')
  })
$(document).ready(function(){
    $('.snocls').each(function(){
     $(this).html(($(this).closest('tr').index())+1)
    })
})

$(document).ready(function(){
  sum=0
  $('.grossamount').each(function(){
    sum += parseInt($(this).text())
    lastElement = $(this);
    console.log('sum',$(this).text())
  })
  // console.log('sum',lastElement,sum)
})