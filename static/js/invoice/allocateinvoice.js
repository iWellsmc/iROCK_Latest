total_allocatedamt=0
$(document).on('click','.checkbox_allocate',function(){
    invoiceid=$(this).attr('data-id')
    allotedamount=parseFloat($('.amountallocated').val())
    pending_amount=parseFloat(($('.pending_amount').text()).replace(/,/g, ''))
    netamount = parseFloat($(this).closest('td').find('.netamount').val())
    saveallocate = parseFloat($('.saveallocate').val())
    if ($(this).is(':checked')) {
        if(netamount>pending_amount){
          Swal.fire('Invoice Amount is Greater Than Alloted Amount')
          $(this).prop('checked', false)
        }
        else{
            $(this).closest('td').find('.invoiceid').val(invoiceid)
            $('.pending_amount').text((pending_amount-netamount).toLocaleString())
            if($('.allocated_amount').text()==0){
                $('.allocated_amount').text(netamount.toLocaleString())
            }
            else{
                allocated_amount=parseFloat(($('.allocated_amount').text()).replace(/,/g, ''))
                $('.allocated_amount').text((allocated_amount+netamount).toLocaleString())
            }
        }
    }
    else{
        invoiceid=$(this).attr('data-id')
        $.ajax({
            url: "/invoice/remove_draft_paymentaccount/",
            headers: { 'X-CSRFToken': csrf_token },
            data: {
               'invoiceid':invoiceid
            },
            type: 'POST',
        });
        $(this).closest('td').find('.invoiceid').val('')
        $('.pending_amount').text((pending_amount+netamount).toLocaleString())
        allocated_amount=parseFloat(($('.allocated_amount').text()).replace(/,/g, ''))
        $('.allocated_amount').text((allocated_amount-netamount).toLocaleString())
    }
  })

$(document).on('click','.draft_btn',function(){
    $('.draft_field').val(1)
})

$(document).on('click','.com-save',function(e){
    total_allocatedamt=0
    $('.checkbox_allocate').each(function(){
        if($(this).is(':checked')){
            $(this).closest('td').find('.invoiceid').val($(this).attr('data-id'))
            total_allocatedamt+=parseFloat($(this).closest('td').find('.netamount').val())
        }
    })
    if(total_allocatedamt!=0){
        total_amount=parseFloat($('.amountallocated').val())-total_allocatedamt
        $('.saveallocate').val(total_amount)
    }

})  

$(document).ready(function(){
    total_allocatedamt=0
    $('.checkbox_allocate').each(function(){
        if($(this).is(':checked')){
            $(this).closest('td').find('.invoiceid').val($(this).attr('data-id'))
            total_allocatedamt+=parseFloat($(this).closest('td').find('.netamount').val())
        }
    })
    if(total_allocatedamt!=0){
        pending_amount=parseFloat(($('.pending_amount').text()).replace(/,/g, ''))
        console.log('val--------',pending_amount)
        $('.pending_amount').text((pending_amount-total_allocatedamt).toLocaleString())
        $('.allocated_amount').text(total_allocatedamt.toLocaleString())
    }
})
$(document).on('click','.submit_btn',function(e){
    select_count=0
    $('.checkbox_allocate').each(function(){
        if($(this).is(':checked')){
            select_count++
        }
    })
    if(select_count==0){
        Swal.fire("Allocate Invoice Before Submitting")
        e.preventDefault()
    }
})