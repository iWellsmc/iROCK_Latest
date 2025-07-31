$(document).ready(function() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()

    $(document).on('click','#conform_costcode_btn',function(e){
        vendor_costcode=$('#vendor_costcode').val()
        $('#conform_costcode_btn').html('<i class="fas fa-spinner fa-spin"></i> Loading...');

        $.ajax({
            type:"POST",
            data:{'vendor_costcode':vendor_costcode,'invoice_id':invoiceid,'module_id':module_id,'csrfmiddlewaretoken':csrftoken,'comments':$('#conform_costcode_comments').val()},
            url:'/invoice/conformcostcode',
            success: function(data){
                $('#conform_costcode_btn').html('Submit');
                location.reload();
            }
        })
    })
    $(document).on('click','.notconform_costcode',function(e){
        e.preventDefault();
        swal.fire('Confirm Cost Code')
    }) 

})