let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
let invoicecost_id=$('#invoicecost_id').val()
let invoice_id=$('#invoice_id').val()

const notyf = new Notyf({
        duration: 5000,
        position: {
            x: 'right',
            y: 'top',
        },
        types: [
            {
            type: 'warning',
            // background: '#D3D3D3',
            duration: 4000,
            icon: {
                className: 'material-icons',
                tagName: 'i',
                // text: 'warning',
                // dismissible: true
            }
            },
            {
            type: 'error',
            // background: '#D3D3D',
            duration: 4000,
            // dismissible: true
            },
            {
            type: 'success',
            // background: '#D3D3D',
            // background: '##BD2753',
            duration: 4000,
            // dismissible: true
            }
        ]
        });
$(document).ready(function(){


$('.send_cls').click(function(){
    console.log('asd')
    ajax_func('send',null)
})

let ajaxInProgress = false;



    $(document).on('click','#id_verify',function(){
        if (ajaxInProgress) return;
        let get_val=$('#id_verification_code').val();
        let remove_space=get_val.replace(/ /g, '');
        let type='verify'
        let code=remove_space
        let invoicecost =$(this).attr('data-id')
        let payment_id=$(this).attr('payment-id')
        console.log(remove_space.length)
        $('#id_verify').prop("disabled", true);
        if (remove_space.length == 6){
            ajaxInProgress = true;
            $.ajax({
                type:"POST",
                data:{'csrfmiddlewaretoken':csrftoken,'invoice_id':invoice_id,'invoicecost_id':invoicecost,'type':type,'code':code,'payment_id':payment_id,'pay_id':pay_id},
                url:'/invoice/bankuserapprovalajax',
                success: function(data){
                    console.log(data)
                    if (type == "send"){
                        if (data.data == "success"){
                            notfy_func('success','Verification Code Send Successfully','#D3D3D3')
                            $('#id_verification_code').attr('readonly',false);
                            $('#id_send').hide(400);
                            $('#id_verify').show(400);
                            $('#id_resend').show(400);
                        }
                    }
                    else{
                        if (data.data == "success"){
                            notfy_func('success','Code Verified Successfully','#D3D3D3')
                            $('#id_verify').text('Verified').addClass('btn btn-success').removeClass('btn-clr').removeAttr('id');
                            $('#id_resend').hide();
                            $('#final_Save_id').show();
                            window.location.href = '/invoice/vendorbasedinvoice';
                        }
                        else{
                            notfy_func('error','Incorrect Verification Code','##D3D3D3')
                        } 
                    }
            },
            complete: function() {
                ajaxInProgress = false;
            }
        })
        // ajax_func('verify',remove_space)
    //     $.ajax({
    //         type:"POST",
    //         data:{'csrfmiddlewaretoken':csrftoken,'invoice_id':'','code':remove_space,'type':'verify'},
    //         url:'/invoice/bankuserapprovalajax',
    //         success: function(data){
    //             console.log(data)
    //             if (data.data == "success"){
    //                 $('#id_verify').text('Verified').addClass('btn btn-success').removeClass('btn-clr');
    //                 $('.pay_voucher').show();
    //             }
    //             else{
    //                 console.log('wrong code')
    //             }
    //     },})
    }
    else{

    }
})

$(document).on('keypress', '#id_verification_code', function(e) {
    if (ajaxInProgress) {
        e.preventDefault();
        return;
    }
    if (e.which === 13) { // Check if the key pressed is Enter (key code 13)
        e.preventDefault(); // Prevent default form submission behavior
        // Add your code to handle verification here
        // For example, trigger the verification button click
        $('#id_verify').click();
    }
});
function ajax_func(type,code){
    $.ajax({
        type:"POST",
        data:{'csrfmiddlewaretoken':csrftoken,'invoice_id':invoice_id,'invoicecost_id':invoicecost_id,'type':type,'code':code},
        url:'/invoice/bankuserapprovalajax',
        success: function(data){
            console.log(data)
            if (type == "send"){
                if (data.data == "success"){
                    notfy_func('success','Verification Code Send Successfully','##D3D3D3')
                    $('#id_verification_code').attr('readonly',false);
                    $('#id_send').hide(400);
                    $('#id_verify').show(400);
                    $('#id_resend').show(400);
                }
            }
            else{
                if (data.data == "success"){
                    notfy_func('success','Code Verified Successfully','##D3D3D3')
                    $('#id_verify').text('Verified').addClass('btn btn-success').removeClass('btn-clr').removeAttr('id');
                    $('#id_resend').hide();
                    $('#final_Save_id').show();
                }
                else{
                    notfy_func('error','Incorrect Verification Code','##D3D3D3')
                } 
            }
    },})

}

$(document).on('keyup','#id_verification_code',function(){
    $('#id_verify').prop("disabled", false);
 })


function notfy_func(type,message,bg){
    if (document.querySelector('.notyf__toast')) {
        return; // If there are existing notifications, exit the function
    }

    notyf.open({
        type: type,
        message: message,
        background:bg ,

    });
}

$(document).on('click','#add_file',function(){
    var html=$(this).closest('tr').clone();
    $(this).closest('table').append(html);
    $(this).closest('table').find('tr:last td:eq(0) .filecls').val(null);
})

$(document).on('click','#remove_file',function(){
    var table_len=$(this).closest('table').find('tr').length;
    if (table_len >1){
        $(this).closest('tr').remove();
    }

})


$(document).on('change','.verify_code',function(){
   var html="<input type='text' name='verification_code' id='id_verification_code' maxlength='6' autocomplete='off' oninput='this.value = this.value.replace(/[^0-9]/g, '')'  class='form-control me-3' placeholder='input code' ></input><button type='button' class='btn btn-clr' id='id_verify' data-id='"+$(this).val()+"' payment-id='"+$(this).find('option:selected').attr('payment-id')+"'>Verify</button>"
    $(this).closest('div').find('.code_verification').html(html)
})

$(document).on('click','.check_code',function(){
    $('.codes_invoice').removeAttr('style')
    $('.codes_hide').css('display','none')
    $('.hide_code').removeAttr('style')
    $(this).css('display','none')
    
})

$(document).on('click','.hide_code',function(){
    $('.codes_hide').removeAttr('style')
    $('.codes_invoice').css('display','none')
    $('.check_code').removeAttr('style')
    $(this).css('display','none')
    
})

$(document).on('click','.popup_viewcode',function(){
    notfy_func('success','Verification Code Send To User','##BD2753')
                    $('#id_verification_code').attr('readonly',false);
                    $('#id_send').hide(400);
                    $('#id_verify').show(400);
                    $('#id_resend').show(400);

})

$(document).on('input','#id_verification_code',function(){
    
    $(this).val($(this).val().replace(/\D/g, ''));
});


});

