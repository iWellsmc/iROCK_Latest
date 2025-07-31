

$(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
  $(document).ready(function(){
    var serial_no=$('#serial_id').val();
    console.log('ad',serial_no)
    $('.creditno').each(function (index, value) {
        var get_val=$(this).val().split('/');
        $(this).val('').val(get_val[0]+'/'+serial_no+'/'+get_val[2])
        var id = $(this).closest('tr').find('.ven_id').val()
        var current_split = $(this).closest('tr').val(get_val[0]+'/'+serial_no+'/'+get_val[2]).val()
        $('.inv' + id).children('div').children('div').find('.p-value').text(get_val[0]+'/'+serial_no+'/'+get_val[2])
    })
  })

  $(document).ready(function() {
    var inputValue = $('#creditvalue_total').val();
        var numericValue = inputValue.replace(/[^0-9.]/g, '');
        $('#creditvalue_total').val(numericValue);
});

var global_currency_symbol=$('#change-currency').attr('curreny_symbol')
var contract_id=$('.contractcls').find(':selected').val()
contract_type=$('.contractcls').find(':selected').attr('contract_type')
var created_inv_ids=$('#created_inv').val()
var remove_bracket=created_inv_ids.replace('[','')
var remove_bracket=remove_bracket.replace(']','')
var split_array=remove_bracket.split(',')
array = $.map(split_array, function(value){
    return value.replace(/ /g, '');
  });
console.log('a',array)
$.ajax({
    type:"GET",
    url:'/credit/getcontractinvoices',
    data:{'contract_id':contract_id,'contract_type':contract_type},
    async:false,
    success: function(data){
        console.log(data)
        var html =''
        $.each(data.data,function (key,val) {
            // console.log(val.invoice_id)
            html+='<option value='+val.invoice_id+' data-id='
            $.each(val.invoice_num,function (key1,val1) {
                html+=val1.invoice_date
                if (key1 != (len -1)){
                    html+=','
                }
            })  
            html+='>'
            var len = (val.invoice_num).length;
            $.each(val.invoice_num,function (key1,val1) {
                html+=''+val1.invoice_number+''
                if (key1 != (len -1)){
                    html+=', '
                }
            })
            html+='</option>'
        })
        $('.invoicecls').html(html);
        $('.invoicecls').val(array).trigger('change')
        
    }    
})


var exchange_rate_value ;
$('.contractcls').change(function(){
    $('.com-save').removeAttr('style')
    var contract_id=$(this).find(':selected').val()
    var contract_type=$(this).find(':selected').attr('contract_type')
    var currency_symbol=$(this).find(':selected').attr('currency_symbol')
    var currency=$(this).find(':selected').attr('currency') 
    global_currency_symbol = currency_symbol
    var currency_id=$(this).find(':selected').attr('currency_id')
    $('#cont_type').val(contract_type)
    $('#total_val_id').val('');
    $('#creditvalue_total').val(0);
    $('#id_totalalltax').val('');
    $('.invoicecls').html('');
    $.ajax({
        type:"GET",
        url:'/credit/getcontractinvoices',
        data:{'contract_id':contract_id,'contract_type':contract_type},
        success: function(data){
            console.log(data)
            var html =''
            // html +='<option value="">--Select Invoice Nos for Allocation--</option>'
            $.each(data.data,function (key,val) {
                // console.log(val.invoice_id)
                html+='<option value='+val.invoice_id+' data-id=';
                $.each(val.invoice_num,function (key1,val1) {
                    html+=val1.invoice_date
                    if (key1 != (len -1)){
                        html+=','
                    }
                })
                html +='>'
                var len = (val.invoice_num).length;
                $.each(val.invoice_num,function (key1,val1) {
                    html+=''+val1.invoice_number+''
                    if (key1 != (len -1)){
                        html+=', '
                    }
                    // console.log(val1.invoice_number)
                })
                html+='</option>'
            })
            $('.invoicecls').html(html);
            $('.cur-show').removeAttr('style')
            $('#change-currency').text(currency_symbol+' '+currency)
            var exclusive='';
            if ((data.exclusive_taxes).length == 0){
                $('.exclusivetable').css('display','none')
            }
            else if ((data.exclusive_taxes).length == 1){
                var get_id=''
                var get_percentage=''
                exclusive += '<tr><td><select name="exclusive" class="form-control exc-cls">'
                $.each(data.exclusive_taxes,function (key,val) {
                    exclusive +='<option value="'+val.id+'" data_id="'+val.taxpercentage+'">'+val.vendortax_id__tax__Tax_Name+' '+val.taxpercentage+'%</option>'
                    get_id += val.id
                    get_percentage += val.taxpercentage
                })
                exclusive +='</select></td><td><input type="text" name="exclusive_percentage" class="exclusivepercls in-bor-clr width-decc" readonly></td><td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls"> <p class="taxvalcls"></p></td></tr>' 
                $('.exclusivetable tbody').html(exclusive)
                $('.exc-cls option[value="'+get_id+'"]').attr("selected", "selected");
                $('.exclusivepercls').val(get_percentage)
                // $('.exc-cls').attr('disabled',true)
                $('.exclusivepercls').attr('readonly',true)
            }
            else{
                exclusive += '<tr class="tr_clone"><td><select name="exclusive" class="form-control exc-cls">'
                exclusive +='<option value="">--Select Tax--</option>'
                $.each(data.exclusive_taxes,function (key,val) {
                    exclusive +='<option value="'+val.id+'" data_id="'+val.taxpercentage+'">'+val.vendortax_id__tax__Tax_Name+' '+val.taxpercentage+'%</option>'
                })
                exclusive +='</select></td><td><input type="text" name="exclusive_percentage" class="exclusivepercls in-bor-clr width-decc" readonly></td><td class=""> <button id="add-row" class="btn-clr add-row btn add-btn" type="button" value="add"><i class="fa fa-plus"></i></button> <button id="delete-row" class="btn-clr delete-row btn add-btn" type="button" value="delete"><i class="fa fa-minus"></i></button> </td> <td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls"> <p class="taxvalcls"></p></td> </tr>'
                // console.log(exclusive)
                $('.exclusivetable tbody').html(exclusive)
            }
            var inclusive =''
            if ((data.inclusive_taxes).length > 0){
                $.each(data.inclusive_taxes,function (key,val) {
                    inclusive +=''+val.vendortax_id__tax__Tax_Name+' '+val.taxpercentage+'%,'
                })
                inclusive +='(already included in Total value above)'
                $('.inv-tax-cls').removeAttr('style')
            }
            else{
                $('.inv-tax-cls').css('display','none')
            }
            $('.in-clu').text(inclusive)
            //split-invoice-tbl
            // if (data.invoice_count == '1'){
            // }
            exchange_rate_value = data.exchange_rate_value
            var invoice_head='<th>S/No</th><th>Currency-Split</th><th>Credit Note No.</th><th>Date</th><th>Amount in Base Currency</th><th>Exchange Rate</th><th>Amount in Payment Currency</th><th>File Upload</th>'
            var invoice_tr=''
            $.each(data.vendor_invoices,function (key,val) {
              
                invoice_tr += '<tr><td>'+(key+1)+'</td><td><input type="hidden" name="invoice_id" class="ven_id" value="'+val.id+'" ><input type="text" name="invoice_split" class="form-control split-cls" value="'+val.currency_id__currency_symbol+'-'+val.percentage+'%" inv_percentage="'+val.percentage+'"  readonly><input type="hidden" name="invoice_percentage" value="'+val.percentage+'"><input type="hidden" name="invoice_symbol" class="inv_symbol" value="'+val.currency_id__currency_symbol+'"><td><input type="text" name="credit_date" class="credit-date-cls form-control dateformat-cls"></td><td><input type="text" name="base_amount" class="base-amount-cls form-control" readonly></td>'

                if (val.exchange_rate == '1'){
                    if(currency_id == val.currency_id){
                        invoice_tr +='<td><input type="text" name="exchange" class="exchange-cls form-control exchangecls" value="N/A" readonly></td>'
                    }
                    else{
                        invoice_tr +='<td><input type="text" name="exchange" class="exchange-cls form-control com_val exchangecls"></td>'
                    }
                    
                }
                else{
                    invoice_tr +='<td style="display:none"><input type="text" name="exchange" class="exchange-cls form-control exchangecls" value="N/A" readonly></td>'
                }

                invoice_tr +='<td><input type="text" name="final_amount" class="final-amount-cls form-control" readonly></td><td><input type="file" name="credit_file'+val.id+'" class="credit-file-cls form-control filesize" accept="image, .png, .jpeg, .pdf, .jpg"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td>'

                invoice_tr += '</tr>'

            })
            console.log('',$('.main_cls').html())
            $('#split-invoice-tbl thead').html(invoice_head)
            $('#split-invoice-tbl tbody').html(invoice_tr)
            if (exchange_rate_value == '2'){
                $('#split-invoice-tbl thead th:eq(5)').css('display','none')
                $('#split-invoice-tbl thead th:eq(6)').css('display','none')
                $('#split-invoice-tbl tbody tr').each(function () {
                    $(this).find('td:eq(5)').css('display','none')
                    $(this).find('td:eq(6)').css('display','none')
                })
            }
        }
    })
})



$('.sum-btn').on('click',function(){
    $('.insum_detail').removeAttr('style')
})

$('.hide-btn').on('click',function(){
    $('.insum_detail').css('display','none')
})

function newRoundOfTwoValues(number) {
    var numberStr = number.toString();
    var decimalPos = numberStr.indexOf('.');

    // If there is no decimal point, simply return the number with two decimal places
    if (decimalPos === -1) {
        return parseFloat(number).toFixed(2);
    }

    var integerPart = numberStr.substring(0, decimalPos);
    var decimalPart = numberStr.substring(decimalPos + 1);
    var newDecimalPart;
    
    if (decimalPart.length > 2) {
        // Check the third digit to determine whether to round up or not
        if (parseInt(decimalPart.charAt(2)) >= 5) {
            newDecimalPart = (parseInt(decimalPart.substring(0, 2)) + 1).toString().padStart(2, '0');
            
            // Check if rounding causes the decimal part to be "100", meaning we need to carry over to the integer part
            if (newDecimalPart === '100') {
                newDecimalPart = '00';
                integerPart = (parseInt(integerPart) + 1).toString();
            }
        } else {
            newDecimalPart = decimalPart.substring(0, 2);
        }
    } else if (decimalPart.length === 2) {
        newDecimalPart = decimalPart;
    } else {
      newDecimalPart = decimalPart.padEnd(2, '0');
    }

    var result = integerPart + '.' + newDecimalPart;
    
    return parseFloat(result).toFixed(2);
}




function decimal_value(val){
    if (val != ''){
        var con_val=val.toString()
        var remove_commas= con_val.replace(/[,()]/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)){
            return newRoundOfTwoValues(remove_commas)
        }
        else{
            return newRoundOfTwoValues(remove_commas)
        }
    }
    else{
        return newRoundOfTwoValues(val)
    }
}



function numberWithCommas(x) {
    console.log('a',x)
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


$('#total_val_id').change(function(){
    var new_val=$(this).val().replace(/[^0-9.]/g,'');
    $(this).val(numberWithCommas(decimal_value(new_val)))
    $('#creditvalue_total').val(new_val)
    calculation_func()
})

$(document).on('change','.exc-cls',function(){
    var val=$(this).find(':selected').val()
    var z=0;
    if (val!= ''){
        $(".exc-cls").each(function(){
            var y=$(this).find(':selected').val();
            if (val !='' && y !=''){
                if(val==y){
                    z=z+1;
                    
                }
            }
        })
        if (z > 1){
            Swal.fire('Tax Already Selected')
            $(this).closest('tr').remove()
            calculation_func()
            // $(this).addClass('con_error')
        }
        else{
            // $(this).removeClass('con_error')
            var percentage=$(this).find(':selected').attr('data_id')
            $(this).closest('tr').find('.exclusivepercls').val(percentage)
            calculation_func()
        }
    }
    else{
        $(this).closest('tr').find('.exclusivepercls').val('')
        $(this).closest('tr').find('.exclusivevalcls').val('')
        $(this).closest('tr').find('.taxvalcls').text('')
        calculation_func()
    }
})

$('.exclusivetable').on('click', '.add-row', function() {
    var $tr = $(this).closest('.tr_clone');
    var $clone = $tr.clone();
    console.log($clone);
    $clone.find('.exc-cls option:selected').removeAttr('selected');
    $clone.find('.hdn_ex_cls').val('');
    $clone.find('.exclusivepercls').val('');
    $clone.find('.taxvalcls').text('');
    $clone.find('.exclusivevalcls').val('')
    $tr.after($clone);
});

$('.exclusivetable').on('click','#delete-row',function(){
    var tablen=$('.exclusivetable tbody tr').length
    if (tablen > 1){
        $(this).closest('tr').remove()
        calculation_func()
    }
})

var hdn_dateformat=$('#companydateformat').val()
if (hdn_dateformat ==''){
    $(document).on('focus',".credit-date-cls", function(){
        $(this).attr('autocomplete', 'off');
        min_date=$(this).attr('inv_sel_date')
        $(this).datepicker({
            dateFormat: 'dd-M-yy',
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:+0',
            minDate:new Date(min_date),
            maxDate:new Date(),
        });
      });
      
}
else{
    $(document).on('focus',".credit-date-cls", function(){
        $(this).attr('autocomplete', 'off');
        min_date=$(this).attr('inv_sel_date')
        $(this).datepicker({
            dateFormat: hdn_dateformat,
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:+0',
            minDate:new Date(min_date),
            maxDate:new Date(),
        });
      });

}

$('.support_tbl').on('click', '.add-file-row', function() {
    var $tr = $(this).closest('.tr_file_clone');
    // console.log({'tr':$tr})
    var $clone = $tr.clone();
    // console.log({'$clone'});
    // $clone.find('.exc-cls').removeClass('con_error');
    $clone.find(':file').val('');
    // $clone.find('.taxvalcls').text('');
    // $clone.find('.exclusivevalcls').val('')
    $tr.after($clone);
});

$('.support_tbl').on('click','.delete-file-row',function(){
    var tablen=$('.support_tbl tbody .tr_file_clone').length
    console.log(tablen)
    if (tablen > 1){
        $(this).closest('tr').remove()
    }
})

function calculation_func(){
    var credit_value=$('#total_val_id').val().replace(/[^0-9.]/g,'') || 0;
    $('#creditvalue_total').val(credit_value)
    console.log('123',credit_value)
    var calculate_exclusive_tax = 0
    var exclusivepercentage=0

    var exchangetype =$('#exchange_rate_value').val();
    var baseoncurrency =$('#baseoncurrency').val();
    // if (credit_value != ""){
    $('.exclusivetable tbody tr').each(function(){
        var exclusivepercls=$(this).find('.exclusivepercls').val()
        if (exclusivepercls != ''){
        var exclusivetaxamount=exclusivepercls
        // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

        // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

        exclusivepercentage+=parseFloat(removecommaonly(exclusivepercls))
        }
    })
    // console.log('nanvlasd',calculate_exclusive_tax)
    var con_calculate_val=decimal_value(exclusivepercentage)
    // console.log('1',con_calculate_val)
    var add_totalvalue_tax=parseFloat(credit_value)+parseFloat(con_calculate_val)
    // console.log('v',add_totalvalue_tax)
    $('#add_exclusive_value').val(con_calculate_val)
    $('#id_tot_exc').val('('+global_currency_symbol+' '+numberWithCommas(decimal_value(con_calculate_val))+')')
    $('#id_totalalltax').val('('+global_currency_symbol+' '+numberWithCommas(decimal_value(add_totalvalue_tax))+')')
    $('#creditvalue_total').val('('+global_currency_symbol+' '+numberWithCommas(decimal_value(add_totalvalue_tax))+')')     

    $('#split-invoice-tbl tbody tr').each(function(){
        var percentage=$(this).find('.split-cls').attr('inv_percentage')
        var calculate_amount= add_totalvalue_tax*percentage/100
        var con_val=decimal_value(calculate_amount)
        var get_curency_symbol=$(this).find('.inv_symbol').val()
        console.log('con_val',calculate_amount)
        $(this).find('.base-amount-cls').val('('+global_currency_symbol+' '+numberWithCommas(decimal_value(con_val))+')')
        var get_exchange_rate=$(this).find('.exchange-cls').val()
        if (get_exchange_rate != 'N/A'){
            console.log('12',$(this))
            if (get_exchange_rate != 0){
                var exchange_with_amount=get_exchange_rate*con_val
                // convert to string interpolation
                $(this).find('.final-amount-cls').val(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exchange_with_amount))})`)
            }

        }
        else{
            // convert to string interpolation
            $(this).find('.final-amount-cls').val(`(${get_curency_symbol} ${numberWithCommas(decimal_value(con_val))})`)
        }
        var get_ven_id=$(this).find('.ven_id').val()
        // console.log($('.inv_sum_cls'+get_ven_id+' tbody tr'))
        $('.inv_sum_cls'+get_ven_id+' tbody tr').each(function(){
            if (get_exchange_rate != 'N/A'){
                if (get_exchange_rate != 0){
                    var total_val=credit_value
                    // console.log('total_val',total_val)
                    var totalval_finalval=total_val*parseFloat(percentage)/100 || ''
                    // convert to string interpolation
                    var totalval_finalvalue=get_exchange_rate*totalval_finalval

                    if (exchangetype == '1' || exchangetype == 1){
                    $('.inv'+get_ven_id+'').find('.finaldiscountcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalval_finalvalue))})`)
                    }else{
                    $('.inv'+get_ven_id+'').find('.finaldiscountcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalval_finalvalue))})`)
                    }
                    // console.log('sev',$('.inv'+get_ven_id+'').find('.finaldiscountcls').text(totalval_finalval))
                    // console.log('totalval_finalval',totalval_finalval)
                    var total_exclusive=$('#id_tot_exc').val().replace(/[^0-9.]/g,'') || 0;
                    // console.log('total_exclusive',total_exclusive)
                    var exclusive_finalval=total_exclusive*parseFloat(percentage)/100
                    // console.log('exclusive_finalval',exclusive_finalval)
                    // convert to string interpolation
                    var exclusive_finalvalue=get_exchange_rate*exclusive_finalval
                    if (exchangetype == '1' || exchangetype == 1){
                    $('.inv'+get_ven_id+'').find('.finaltaxcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exclusive_finalvalue))})`)
                    }else{
                    $('.inv'+get_ven_id+'').find('.finaltaxcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(exclusive_finalvalue))})`)
                    }
                    var totalfinalval=totalval_finalval+exclusive_finalval
                    // console.log('totalfinalval',totalfinalval)
                    var totalinclusive_finalvalue=get_exchange_rate*totalfinalval
                    // convert to string interpolation
                    if (exchangetype == '1' || exchangetype == 1){
                    $('.inv'+get_ven_id+'').find('.totalsumcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalinclusive_finalvalue))})`)
                    }else{
                    $('.inv'+get_ven_id+'').find('.totalsumcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalinclusive_finalvalue))})`)
                    }
                }
            }
            else{
                var total_val=credit_value
                // console.log('total_val',total_val)
                var totalval_finalval=total_val*parseFloat(percentage)/100 || ''
                // convert to string interpolation
                if (exchangetype == '1' || exchangetype == 1){
                $('.inv'+get_ven_id+'').find('.decimal_value').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalval_finalval))})`)
                }else{
                $('.inv'+get_ven_id+'').find('.finaldiscountcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalval_finalval))})`)
                }
                // console.log('sev',$('.inv'+get_ven_id+'').find('.finaldiscountcls').text(totalval_finalval))
                // console.log('totalval_finalval',totalval_finalval)
                var total_exclusive=$('#id_tot_exc').val().replace(/[^0-9.]/g,'') || 0;
                // console.log('total_exclusive',total_exclusive)
                var exclusive_finalval=total_exclusive*parseFloat(percentage)/100
                // console.log('exclusive_finalval',exclusive_finalval)
                if (exchangetype == '1' || exchangetype == 1){
                $('.inv'+get_ven_id+'').find('.finaltaxcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exclusive_finalval))})`)
                }else{
                $('.inv'+get_ven_id+'').find('.finaltaxcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(exclusive_finalval))})`)
                }
                var totalfinalval=totalval_finalval+exclusive_finalval
                // console.log('totalfinalval',totalfinalval)
                if (exchangetype == '1' || exchangetype == 1){
                $('.inv'+get_ven_id+'').find('.totalsumcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalfinalval))})`)
                }else{
                $('.inv'+get_ven_id+'').find('.totalsumcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalfinalval))})`)
                }
            }


        })


    })
    // }
    // else{

    // }
}
$(document).on('change','.exchange-cls',function(){
    var new_val=$(this).val().replace(/[^0-9\.]+/g,'');
    new_val = new_val.replace(/\./,"#").replace(/\./g,"").replace(/#/,".");
    // new_val = Math.round(new_val * 1000) / 1000
    $(this).val(new_val)
    // $(this).val(decimal_value(new_val))
    calculation_func()
})

$(document).on('click','.com-save',function(e){
    e.preventDefault()
    var submit_value=$(this).attr('value')
    if (submit_value == '0'){
        $("<input>").attr({name: "submit_value",id: "hiddenId",type: "hidden",value: 0}).appendTo("form");
        $('#creditnote1')[0].submit()
    }
    else if (submit_value == '1'){
        var validate_value=validation_func()
        if (validate_value == 0){
            Swal.fire({
                text: 'Do You Want to Submit Credit Note?',
                showDenyButton: true,
                // showCancelButton: true,
                // textColor:'#77d61f',
                confirmButtonColor: '#77d61f',
                denyButtonColor:'#AF2B50',
                confirmButtonText: 'Yes',
                denyButtonText: 'No',
                customClass: {
                actions: 'my-actions',
                //   cancelButton: 'order-1 right-gap',
                confirmButton: 'order-2',
                denyButton: 'order-3',
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    $("<input>").attr({name: "submit_value",id: "hiddenId",type: "hidden",value: 1}).appendTo("form");
                    $('#creditnote1')[0].submit()
                    // window.location.href = '../list';
                    return true;
                }
            })
        }
    }
    else{
        var validate_value=validation_func()
        if (validate_value == 0){
            $("<input>").attr({name: "submit_value",id: "hiddenId",type: "hidden",value: 2}).appendTo("form");
            $('#creditnote1')[0].submit()
        }
    }

})

$(document).on('change','.credit-file-cls',function(){
    var val=$(this).val()
    if (val != ''){
        $(this).next('p').remove()
        $(this).closest('td').find('.hdn_fl_cls').val('')
    }
    // else{
    //     $(this).next('p').show()
    // }
})

$(document).on('click','.remove_file',function(){
    $(this).closest('tr').remove()
})


function validation_func(){
    var count=0;
    $('select').each(function(){
        var val=$(this).find(':selected').val()
        if (val == ''){
            count ++;
            $(this).addClass('con_error')
        }
    })
    var inv_val=$('.invoicecls').val()
    if (inv_val.length == 0){
        $('.select2-selection--multiple').addClass('con_error')
    }
    else{
        $('.select2-selection--multiple').removeClass('con_error')
    }
    $(".exchange-cls").each(function(){
        var val=$(this).val()
        
        if (val == ''){
            count ++;
            $(this).addClass('con_error')
        }
    })
    $(".com_val").each(function(){
       
        var val=$(this).val()
        if (val == ''){
            count ++;
            
            $(this).addClass('con_error')
        }
       
    });

    $(".credit-file-cls").each(function(){
        var val=$(this).val()
        var hdn_val=$(this).closest('td').find('.hdn_fl_cls').val()
        if (hdn_val == ''){
            if (val == ''){
                count ++;
                $(this).addClass('con_error')
            }
        }
    });

    $(".exclusivepercls").each(function () {

        var val = $.trim($(this).val())
        if (val == '') {
            count++;
            // console.log($(this))
            $(this).addClass('con_error')
           
        }

    });
    

    return count
}

$(document).on('change','.con_error',function(){
    $(this).removeClass('con_error') 
})
/*
$(document).on('change','.invoicecls',function(){
    var val=$(this).val()
    if (val.length > 0){
        $('.select2-selection--multiple').removeClass('con_error')  
    }
})
*/
$(document).on('change','.credit_name',function(){
    
    currentelement=$(this)
    $(this).closest('tr').find('.creditnumspancls').remove()
    var val=$(this).val()||null
    if ( val != ''){
        $.ajax({
            type: "GET",
            url:'/credit/checkcreditno',
            data: {'val':val},
            success: function(data)
            {
                if (data.data == "exists"){
                    currentelement.after('<span class="waring-err creditnumspancls">Credit number already exists</span>')
                    $('.com-save').attr('disabled',true)
                }
                else{
                    var z=0
                    $(".credit_name").each(function(index,value){
                        var y=$(value).val().toLowerCase();
                        var con_val=val.toLowerCase();
                        if (con_val !='' && y !=''){
                            if(con_val == y){
                                // console.log("true",y)
                                z=z+1;
                            }
                        }
                    })
                    console.log("z",z)
                    if (z>1){
                        currentelement.after('<span class="waring-err creditnumspancls">Credit number already exists</span>')
                        $('.com-save').attr('disabled',true)
                    }
                    else{
                        $('.com-save').attr('disabled',false)
                    }
                }
            }
        })
    }
    else{

    }
    var get_ven_id=$(this).closest('tr').find('.ven_id').val().toLowerCase()
    $('.inv'+get_ven_id+'').find('.p-value').text(val)
    console.log('get_ven_id',get_ven_id)

    // $('.styleremove').removeAttr('style')
    var current_row=$(this).closest('tr')
    check_credit_row(current_row)




})


$(document).on('change','.dateformat-cls',function(){
   

    var val=$(this).val()||null

    var id=$(this).closest('tr').find('.ven_id').val()
    $('.inv'+id).children('div').children('div').find('.val-datecls').text(val)
    // $('.styleremove').removeAttr('style')
    var current_row=$(this).closest('tr')
    console.log('current_row',current_row)
    //check_credit_row(current_row)



})

$(document).on('change','.exchangecls',function(){
  
    $('.styleremove').removeAttr('style')
    var id=$(this).closest('tr').find('.ven_id').val()
    var current_row=$(this).closest('tr')
    check_credit_row(current_row)
})


//$(document).readyunction() {
    window.onload = function () {
    $.ajax({
        type: 'GET',
        url:'/credit/totalcost',
        data: {'invoice_id':$('.invoicecls').val()},
        success: function(data)
        {
            $('#invoicetotalcost').val(data.cost)
        }
    })
    getInvoiceData($('.invoicecls').val())
}


$(document).on('change','.invoicecls',function(){
    getInvoiceData($(this).val())
    $.ajax({
        type: 'GET',
        url: '/credit/totalcost',
        data: { 'invoice_id': $(this).val() },
        async: false,
        success: function (data) {
            $('#credit_sum').val(data.credit_sum);
            $('#credit_sum_count').val(data.credit_sum_count);

            console.log('data',data.credit_sum)
            $('.creditno').each(function (index, value) {
                var get_id = ''
                var get_percentage = ''
                exclusive=''
            
                $.each(data.new_list, function (key, val) {
                    exclusive += '<input type="hidden" name="hdn_exclusive_tax" value="" class="hdn_ex_cls"><tr><td><select class="form-control exc-cls" disabled>'
                    exclusive += '<option value="' + val.percentage_id + '" data_id="' + val.percentage + '">' + val.tax_name + ' ' + val.percentage + '%</option>'
                    get_id += val.percentage_id
                    get_percentage += val.percentage
                    exclusive += '</select></td><td><input type="text"  class="exclusivepercls "  oninput="$(this).val(($(this).val().replace(/[^0-9.]/g,"")))"></td><td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls new_exclusive" value=""> <input type="hidden" name="exclusive" value='+val.percentage_id+'><input type="hidden" name="exclusive_percentage" value='+val.percentage+'><p class="taxvalcls"></p></td></tr>'
                })
                $('.exclusivetable tbody').html(exclusive)
                $('.exclusivetable').removeAttr('style')
                calculation_func()
            })

        }
    })
    // if user change invoice then remove all credit rows
    $('#total_val_id').val('')
    $('#creditvalue_total').val(0)
    $('#total_val_id').trigger('change')
})

function getInvoiceData(data){
    var val = $('.invoicecls option:selected').text()
    var selected_date = $('.invoicecls option:selected').attr('data-id')
    console.log('selected_date',selected_date[0])
    var splitval =val.split(',')

    var selected_date_split = selected_date.split(',')
    var currency_symbol=$('.contractcls').find(':selected').attr('currency_symbol') 
    $.ajax({
        type: 'GET',
        url: '/credit/totalcost',
        data: { 'invoice_id': data },
        async: false,
        success: function (data) {
            // $('#invoicetotalcost').val(data.cost)
            $('#total_cost').val(currency_symbol + '' + (data.invoice_cost))
            console.log(data)
            $('.creditno').each(function (index, value) {
                $(this).val('CN/'+data.serial_no+'/' + '' + splitval[index]);

                // console.log('val',$(this).val('CN/'+data.serial_no+'/'+ +splitval[index]).val())
                var id = $(this).closest('tr').find('.ven_id').val()

                var current_split = $(this).closest('tr').val('CN/'+data.serial_no+'/'+''+splitval[index]).val()
                console.log('current_split',current_split)
                $(this).closest('tr').find('.credit-date-cls').attr('inv_sel_date',selected_date_split[index])

                var current_split = $(this).closest('tr').val('CN/'+data.serial_no+'/' + '' + splitval[index]).val()
                console.log('current_split', current_split)

                $('.inv' + id).children('div').children('div').find('.p-value').text(current_split)
            })

        }
    })
}
    // $('.creditno').each(function(index,value){
    //     $(this).val('CN/1/'+''+splitval[index]);
        
    //     var id=$(this).closest('tr').find('.ven_id').val()
    //     console.log('id',id)

    //     var current_split = $(this).closest('tr').val('CN/1/'+''+splitval[index]).val()
    //     console.log('current_split',current_split)
    //     console.log('current_split',current_split)
    //     $(this).closest('tr').find('.credit-date-cls').attr('inv_sel_date',selected_date_split[index])

    //     $('.inv'+id).children('div').children('div').find('.p-value').text(current_split)

    // })
    // $.ajax({
    //     type: 'GET',
    //     url:'/credit/totalcost',
    //     data: {'invoice_id':$(this).val()},
    //     success: function(data)
    //     {
    //         // $('#invoicetotalcost').val(data.cost)
    //         $('#total_cost').val(currency_symbol+''+(data.invoice_cost))
    //         console.log('data',$('#total_cost').val(currency_symbol+''+(data.invoice_cost))
    //         )

    //     }
    // })


$(document).on('change','#total_val_id',function(){
    
    // var myStr = 'thisisatest';
    // var newStr = myStr.replace(/,/g, '-');

    // console.log('newStr', newStr );
    let ajax_value =parseInt($('#total_cost').val().replace(/[^0-9\.]/g,''))

    console.log('ajax_value',typeof(ajax_value))
    let credit_total = parseInt($('#credit_sum').val().replace(/[^0-9\.]/g, ''))
    let credit_sum_count = parseInt($('#credit_sum_count').val())
    let this_value =parseInt($(this).val().replace(/[^0-9\.]/g,''))
    $('#creditvalue_total').val(parseFloat($(this).val().replace(/[^0-9\.]/g,'')) || 0)
    
    console.log('this_value',typeof(this_value))
    let creditvalue_total = parseFloat($('#creditvalue_total').val());
    new_val=credit_total+creditvalue_total

if( this_value > ajax_value || this_value == typeof NaN || new_val> ajax_value){
    if (credit_sum_count > 0) {
        Swal.fire('Multi Credit Note values Exceeds Total Value of Invoice(s) - Balance Credit Note Value is ' + numberWithCommas(decimal_value(ajax_value - credit_total)))
    }else{
        Swal.fire('Total Value of Credit Note Exceeds Total Value of Invoice(s)')
    }
    $(this).val('')
    $('#creditvalue_total').val(0);
    $('#id_totalalltax').val('')
    $('.base-amount-cls').val('')
    $('.final-amount-cls').val('')
    $('#id_tot_exc').val('')

}
else{
    $(this).val("("+$('.contractcls').find(':selected').attr('currency_symbol')+$(this).val()+")")
}
})

// $(document).on('change','.inputcls',function(){
   
    // var html =''
    // html='<div class="row"><div class="col-6"><label class="contractfilehead">Total Value of invoice <i class="fa fa-info-circle paymentcurcls i-con-clr-to" title="Total value before taxes/levies" ></i></label></div>'
    // '<div class="col-3"><input type="text" name="total_value" id="total_val_id" class="form-control com_val in-bor-clr-start inp-ut-wid wid-to-box in-bor-clr"></div>'
    // $('.totalval_cls').append(html);
    // $('.totalval_cls').removeAttr('style');


// })


$(document).on('change','.exclusivepercls',function(){
    var val=$.trim($(this).val())
    var currency_symbol = $('.contractcls').find(':selected').attr('currency_symbol')
    var addval=$(this).val()
    const this_value = $(this).val()
    var numericValue = parseFloat(this_value.replace(/,/g, ''));
    var formattedValue = numericValue
    console.log({'numberWithCommas(decimal_value(addval))':numberWithCommas(decimal_value(addval))})
    if (numericValue == '' || isNaN(numericValue)){
        $(this).val('')
    }
    else{
        $(this).val(newRoundOfTwoValues(parseFloat(formattedValue)))
    }
    if (val != ''){
            $(this).closest('tr').find('.taxvalcls').text(currency_symbol+' '+numberWithCommas(decimal_value(addval)))
            $(this).closest('tr').find('.exclusivevalcls').val(currency_symbol+' '+numberWithCommas(decimal_value(addval)))
    }
    else{
        $(this).closest('tr').find('.taxvalcls').text(currency_symbol+' '+0)
        $(this).closest('tr').find('.exclusivevalcls').val(currency_symbol+' '+0)
    }
    calculation_func()
})

function splitWithReplaceComma(x) {
    if (x.indexOf(',') > -1){
        var value=x.split(' ')
        var replace=value[1]
        return replace.replace(/,/g , '')
    }
    else{
        var value=x.split(' ')
        return value[1]
    }

}

function numberWithCommas(x) {
    // console.log('a',x)
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function removecommaonly(x) {
    return x.replace(/[^a-zA-Z0-9.]/g, '')
}

$(document).on('keyup','.exclusivepercls',function(e){
    e.preventDefault();
    $(this).removeClass('con_error')
})