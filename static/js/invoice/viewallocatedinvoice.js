$(document).on('click','.reallocate',function(){
  paymentid=$(this).attr('data-id')
  Swal.fire({
   title: `Are you sure you want to Reallocate this Payment ?`,
   showCancelButton: true,
   confirmButtonColor: '#3085d6',
   cancelButtonColor: '#d33',
   confirmButtonText: 'Yes, I Confirm',
   cancelButtonText: 'No',
 }).then((result) => {
   if (result.isConfirmed) {
     $.ajax({
       url:`/invoice/reallocateinvoice/${paymentid}/`,
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
$(document).ready(function() {
   $('#vendor_id').select2({
        placeholder: "Select Vendor",
       });
       $('#currency').select2({
         placeholder: "Select Currency",
        });
     })
     $(document).on('click', '.generate_report', function(e) {
       var vendor_src = $('.vendor_src').next(".select2-container").find('.select2-selection__rendered').attr('title');
     
       if (vendor_src == undefined || vendor_src.trim() == '') {
         
         
         $(".select2-selection").css("border", "1px solid red");
         $('.generate_report').attr('disabled', 'disabled');
         e.preventDefault();
       } else {
         
         $(".select2-selection").css("border", "");
       }
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
         $('.generate_report').attr('disabled', 'disabled');
          
       } else {
         $(".currency_src").next(".select2-container").find('.select2-selection').removeClass("con_error").css("border", "");
         $('.generate_report').removeAttr('disabled');
       
       }
     });      