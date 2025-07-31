$(document).ready(function() {
   
    $('#vendor_id').select2({
       placeholder: "Select Vendor",
      });
    })
    $(document).on('change','.ven-cls',function(){
        let new_val=$(this).find(':selected').val()
        if(new_val != ''){
            $(this).css("border", "");
        }
    })