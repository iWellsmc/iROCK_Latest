
//$('.invoicecls').select2({
//    placeholder: "Select Invoice Nos.for Allocation"
//});
//$('.select2-selection__arrow').remove()

$(document).ready(function () {
    $('#creditnote1').append('<div class="text-center btn-cls btn-1 save_submit"><button type="submit" id="draft_id" class="btn btn-clr text-left draft-cls com-save" name="submit_type" value="0" style="display:none">Save as Draft</button><button type="submit" id="save_id" value="1" style="display:none" class="btn btn-clr text-left save-cls com-save">Save and Submit</button><button type="submit" id="next_id" value="2" style="display:none" class="btn btn-clr text-left next-cls com-save">Preview</button></div>')
})

// $(document).on('change', '#total_val_id', function () {
//     var new_val = $(this).val().replace(/[^0-9\.]+/g, '');
//     $(this).val(decimal_value(new_val))
// })


var exchange_rate_value;
var global_currency_symbol = ''
$('.contractcls').change(function () {
    var active_check=$(this).find('option:selected').attr('active_status')
    var project_name=$(this).find('option:selected').attr('projectname')
    if(active_check == 0){
        $(this).val('')
        swal.fire(''+project_name+' is inactive and contact the client Administrator')
    }
    $('.com-save').removeAttr('style')
    $('.invdetailcls').removeAttr('style')
    $('.insum_detail').css('display', 'none')
    var contract_id = $(this).find(':selected').val()
    console.log({'contract_id':contract_id})
    var contract_type = $(this).find(':selected').attr('contract_type')
    console.log({'contract_type':contract_type})
    var currency_symbol = $(this).find(':selected').attr('currency_symbol')
    var currency = $(this).find(':selected').attr('currency')
    var val = $(this).val()
    global_currency_symbol = currency_symbol
    var currency_id = $(this).find(':selected').attr('currency_id')
    $('#cont_type').val(contract_type)
    $('#total_val_id').val('.');
    $('#creditvalue_total').val(0);
    $('#id_totalalltax').val('');
    $('.inv-val').val('');
    $('.change_invoice').val('');
    $('.invoicecls').html('');
    $('#total_cost').val('');
    if (contract_id==''){
        $('.cur-show').css('display','none')
        $('.invdetailcls').css('display','none')
        $('.save_submit').css('display','none')
    }
    else{
        $('.save_submit').removeAttr('style')
    }

    // $('#total_cost').html('');

    $.ajax({
        type: "GET",
        url: '/credit/getcontractinvoices',
        data: { 'contract_id': contract_id, 'contract_type': contract_type },
        success: function (data) {
            // console.log(data)
            var html = ''
            html += '<option value="">--Select Invoice Nos for Allocation--</option>'
            $.each(data.data, function (key, val) {
                // alert(val.invoice_date)
                // console.log(val.invoice_id)
                // html+='<option>--Select--</option>'
                html += '<option value=' + val.invoice_id + ' inv_status='+val.inv_status+' data-id=';
                $.each(val.invoice_num, function (key1, val1) {
                    html += val1.invoice_date
                    if (key1 != (len - 1)) {
                        html += ','
                    }
                })
                html += '>'
                var len = (val.invoice_num).length;
                $.each(val.invoice_num, function (key1, val1) {
                    html += '' + val1.invoice_number + ''
                    if (key1 != (len - 1)) {
                        html += ', '
                    }
                    // console.log(val1.invoice_number)
                })
                html += ' </option>'
            })
            console.log({'html':html})
            $('.invoicecls').html(html);
            $('.cur-show').removeAttr('style')
            $('#change-currency').text(currency_symbol + ' ' + currency)
            $('.exclusivetable tbody').html('')
            $('#exchangetyp').val(data.exchange_rate_value);
            var exclusive = '';
            if ((data.exclusive_taxes).length == 0) {
                $('.exclusivetable').css('display', 'none')
            }
            else if ((data.exclusive_taxes).length == 1) {
                // var get_id = ''
                // var get_percentage = ''
                // exclusive += '<tr><td><select name="exclusive" class="form-control exc-cls">'
                // $.each(data.exclusive_taxes, function (key, val) {
                //     exclusive += '<option value="' + val.id + '" data_id="' + val.taxpercentage + '">' + val.vendortax_id__tax__Tax_Name + ' ' + val.taxpercentage + '%</option>'
                //     get_id += val.id
                //     get_percentage += val.taxpercentage
                // })
                // exclusive += '</select></td><td><input type="text" name="exclusive_percentage" class="exclusivepercls in-bor-clr width-decc" readonly></td><td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls new_exclusive"> <p class="taxvalcls"></p></td></tr>'
                // $('.exclusivetable tbody').html(exclusive)
                // $('.exc-cls option[value="' + get_id + '"]').attr("selected", "selected");
                // // $('.exclusivepercls').val(get_percentage)
                // // $('.exc-cls').attr('disabled',true)
                // $('.exclusivepercls').attr('readonly', true)
                // $('.exclusivetable').removeAttr('style')
            }
            else {
                // exclusive += '<tr class="tr_clone"><td><select name="exclusive" class="form-control exc-cls">'
                // exclusive += '<option value="">--Select Tax--</option>'
                // $.each(data.exclusive_taxes, function (key, val) {
                //     exclusive += '<option value="' + val.id + '" data_id="' + val.taxpercentage + '">' + val.vendortax_id__tax__Tax_Name + ' ' + val.taxpercentage + '%</option>'
                // })
                // exclusive += '</select></td><td><input type="text" name="exclusive_percentage" class="exclusivepercls in-bor-clr width-decc" readonly ></td><td class=""> <button id="add-row" class="btn-clr add-row btn add-btn" type="button" value="add"><i class="fa fa-plus"></i></button> <button id="delete-row" class="btn-clr delete-row btn add-btn" type="button" value="delete"><i class="fa fa-minus"></i></button> </td> <td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls"> <p class="taxvalcls"></p></td> </tr>'
                // // console.log(exclusive)
                // $('.exclusivetable tbody').html(exclusive)
                // $('.exclusivetable').removeAttr('style')
            }
            var inclusive = ''
            if ((data.inclusive_taxes).length > 0) {
                $.each(data.inclusive_taxes, function (key, val) {
                    inclusive += '' + val.vendortax_id__tax__Tax_Name + ' ' + val.taxpercentage + '%,'
                })
                inclusive += '(already included in Total value above)'
                $('.inv-tax-cls').removeAttr('style')
            }
            else {
                $('.inv-tax-cls').css('display', 'none')
            }
            $('.in-clu').text(inclusive)
            console.log('afds', (data.inclusive_taxes).length)
            if ((data.inclusive_taxes).length > 0) {
                $('.tax_lev_cls').show()
            }
            else {
                $('.tax_lev_cls').hide()
            }
            //split-invoice-tbl
            // if (data.invoice_count == '1'){
            // }
            exchange_rate_value = data.exchange_rate_value
            if(exchange_rate_value == 1){
                var invoice_head = '<th>S/No</th>'+
                '<th>Currency-Split</th>'+
                '<th>Credit Note No.</th>'+
                '<th>Date</th>'+
                '<th>Amount in Base Currency</th>'+
                '<th>Exchange Rate</th>'+
                '<th>Amount in Payment Currency</th>'+
                '<th>File Upload</th>'
            }else if (exchange_rate_value == 2){
                var invoice_head = '<th>S/No</th>'+
                '<th>Currency-Split</th>'+
                '<th>Credit Note No.</th>'+
                '<th>Date</th>'+
                '<th>Amount in Base Currency</th>'+
                '<th>File Upload</th>'
            }
            
            // var invoice_payment_head='<th>S/No</th><th>Currency-Split</th><th>Credit Note No.</th><th>Date</th><th>Amount in Base Currency</th><th>Amount in Payment Currency</th><th>File Upload</th>'
            var invoice_tr = ''
            var add_div = ''
            $.each(data.vendor_invoices, function (key, val) {
                console.log('val', val)
                invoice_tr += '<tr><td>' + (key + 1) + '</td><td><input type="hidden" name="invoice_id" class="ven_id" value="' + val.id + '" ><input type="text" name="invoice_split" class="form-control split-cls" value="' + val.currency_id__currency_symbol + '-' + val.percentage + '%" inv_percentage="' + val.percentage + '"  readonly><input type="hidden" name="invoice_percentage" value="' + val.percentage + '"><input type="hidden" name="invoice_symbol" class="inv_symbol" value="' + val.currency_id__currency_symbol + '"></td><td><input type="text" name="credit_name" class="credit_name form-control com_val creditno" readonly></td><td><input type="text" name="credit_date" class="credit-date-cls form-control com_val dateformat-cls  cus-date" ></td><td><input type="text" name="base_amount" class="base-amount-cls form-control" readonly></td>'
                if (val.exchange_rate == '1') {
                    if (currency_id == val.currency_id) {
                        invoice_tr += '<td><input type="text" name="exchange" class="exchange-cls form-control exchangecls" value="N/A" readonly></td>'
                    }
                    else {
                        invoice_tr += '<td><input type="text" name="exchange" class="exchange-cls form-control com_val exchangecls"></td>'
                    }
                    invoice_tr += '<td><input type="text" name="final_amount" class="final-amount-cls form-control" readonly></td>'
                }
                else {
                    invoice_tr += '<td style="display: none;" ><input type="text" name="exchange" class="exchange-cls form-control exchangecls"  value="N/A" readonly></td>'
                    invoice_tr += '<td style="display: none;" ><input type="text" name="final_amount" class="final-amount-cls form-control" readonly></td>'
                }
                
                invoice_tr += '<td><input type="file" name="credit_file' + val.id + '" class="credit-file-cls form-control filecls filesize credit-m"  accept="image, .png, .jpeg, .pdf, .jpg" ><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td>'
                invoice_tr += '</tr>'
                add_div += '<div class="inv' + val.id + ' styleremove" style="display:none;">'
                add_div += '<div class="row">  <div class="col-lg-1 col-md-0"> </div> <div class=" col-lg-3 col-md-4"> <div class="same-lline"><p class="sum-vew p-head">Credit No :</p><p class="sum-date p-value"></p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew date-cls">Date :<span class="sum-date val-datecls"></span></label></div>   <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"> </div> </div>'

                add_div += '<div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"><table class="inv_sum_cls' + val.id + ' new-sum"><tbody> <tr><th class="hed-inv-gr">Gross Amount Before Taxes</th><td class="hed-inv-gr-val finaldiscountcls"></td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls"></td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls"></td></tr></tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div>'
                add_div += '</div>'
                add_div += '<div class="bot-liine styleremove" style="display:none;"></div>'

            })
            $('.main_cls').html(add_div)
            $('#split-invoice-tbl thead').html(invoice_head)

            $('#split-invoice-tbl tbody').html(invoice_tr)
            // if (exchange_rate_value == '2') {
            //     $('#split-invoice-tbl thead th:eq(5)').css('display', 'none')
            //     $('#split-invoice-tbl thead th:eq(6)').css('display', 'none')
            //     $('#split-invoice-tbl tbody tr').each(function () {
            //         $(this).find('td:eq(5)').css('display', 'none')
            //         $(this).find('td:eq(6)').css('display', 'none')

            //     })
            // }

        }
    })
})

$('.sum-btn').on('click', function () {
    $('.insum_detail').removeAttr('style')
})

$('.hide-btn').on('click', function () {
    $('.insum_detail').css('display', 'none')
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
        // If the decimal part has exactly two digits, use them as they are
        newDecimalPart = decimalPart;
    } else {
        // If the decimal part has fewer than two digits, pad it with zeros
        newDecimalPart = decimalPart.padEnd(2, '0');
    }

    var result = integerPart + '.' + newDecimalPart;
    
    return parseFloat(result).toFixed(2);
}


function decimal_value(val) {
    if (val != '') {
        var con_val = val.toString()
        var remove_commas = con_val.replace(/,/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)) {
            return newRoundOfTwoValues(remove_commas)
        }
        else {
            return newRoundOfTwoValues(remove_commas)
        }
    }
    else {
        return newRoundOfTwoValues(val)
    }
}



function numberWithCommas(x) {
    // console.log('a',x)
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


$('#total_val_id').change(function () {
    var new_val = $(this).val().replace(/[^0-9.]/g, '');
    $(this).val(numberWithCommas(decimal_value(new_val)))
    $('#creditvalue_total').val(new_val)
    calculation_func()
})

$(document).on('change', '.exc-cls', function () {
    var totalvalue = $('#total_val_id').val().replace(/[^0-9.]/g, '') || 0;
    var currency_symbol = $('.contractcls').find(':selected').attr('currency_symbol')
    var val = $(this).find(':selected').val()
    var z = 0;
    if (val != '') {
        $(this).closest('tr').find('#add-row').attr('disabled',false)
        $(this).closest('tr').find('.exclusivepercls').removeAttr('readonly') 
        var addval=totalvalue
        // $(this).closest('tr').find('.exclusivevalcls').val(currency_symbol+' '+numberWithCommas(decimal_value(addval)))
        var count=0
            $('.taxvalcls').each(function(){
                if ($.trim($(this).text()) != ''){
                var val=splitWithReplaceComma($(this).text())
                count += parseFloat(val)
                }
            })
        totalvalue += count

        $(".exc-cls").each(function () {
            var y = $(this).find(':selected').val()
            if (val != '' && y != '') {
                if (val == y) {
                    z = z + 1;

                }
            }
        })
        if (z > 1) {
            Swal.fire('Tax Already Selected')
            $(this).closest('tr').remove()
            calculation_func()
            // $(this).addClass('con_error')
        }
        else {
            // $(this).removeClass('con_error')
            var percentage = $(this).find(':selected').attr('data_id')
            // $(this).closest('tr').find('.exclusivepercls').val(percentage)
            calculation_func()
        }
    }
    else {
        $(this).closest('tr').find('.exclusivepercls').val('')
        $(this).closest('tr').find('.exclusivevalcls').val('')
        $(this).closest('tr').find('.taxvalcls').text('')
        calculation_func()
    }
})

$('.exclusivetable').on('click', '.add-row', function () {
    var $tr = $(this).closest('.tr_clone');
    var $clone = $tr.clone();
    // console.log($clone);
    $clone.find('.exc-cls').removeClass('con_error');
    $clone.find(':text').val('');
    $clone.find('.taxvalcls').text('');
    $clone.find('.exclusivevalcls').val('')
    $clone.find('.add-row').attr('readonly','readonly')
    // console.log('2222',$clone.find('.add-row'))
    $tr.after($clone);
});

$('.exclusivetable').on('click', '#delete-row', function () {
    var tablen = $('.exclusivetable tbody tr').length
    if (tablen > 1) {
        $(this).closest('tr').remove()
        calculation_func()
    }
})

var hdn_dateformat = $('#companydateformat').val()
if (hdn_dateformat == '') {
    $(document).on('focus', ".credit-date-cls", function () {
        $(this).attr('autocomplete', 'off');
        min_date = $(this).attr('inv_sel_date')
        console.log('wsf', min_date)
        console.log('last', new Date())
        $(this).datepicker({
            dateFormat: 'dd-M-yy',
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:+0',
            minDate: new Date(min_date),
            maxDate: new Date(),
        });
    });
    

}
else {
    $(document).on('focus', ".credit-date-cls", function () {
        $(this).attr('autocomplete', 'off');
        min_date = $(this).attr('inv_sel_date')
        console.log('wsf', min_date)
        console.log('last', new Date())
        $(this).datepicker({
            dateFormat: hdn_dateformat,
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:+0',
            minDate: new Date(min_date),
            maxDate: new Date(),
        });
    });

}

$('.support_tbl').on('click', '.add-file-row', function () {
    var $tr = $(this).closest('.tr_file_clone');
    var $clone = $tr.clone();
    // console.log($clone);
    // $clone.find('.exc-cls').removeClass('con_error');
    $clone.find(':file').val('');
    // $clone.find('.taxvalcls').text('');
    // $clone.find('.exclusivevalcls').val('')
    $tr.after($clone);
});

$('.support_tbl').on('click', '.delete-file-row', function () {
    var tablen = $('.support_tbl tbody tr').length
    if (tablen > 1) {
        $(this).closest('tr').remove()
    }
})
function validateInput(input) {
    input.value = input.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
    validateTotalValue();
}
function validateTotalValue() {
    var credit_value = $('#total_val_id').val().replace(/[^0-9.]/g, '') || 0;
    if (!isNaN(credit_value) && credit_value >= 0) {
        $('#creditvalue_total').val(credit_value);
        calculation_func();
    } else {
        Swal.fire('Please enter a valid total value for the credit note.');
    }
}

function calculation_func() {
    var credit_value = $('#total_val_id').val().replace(/[^0-9.]/g, '') || 0;
    $('#creditvalue_total').val(credit_value)
    var calculate_exclusive_tax = 0
    var exclusivepercentage=0
    var exchangetype =$('#exchangetyp').val();
    var baseoncurrency =$('#basecurrency').val();

    // alert('exchangetype '+ exchangetype)
    // alert('basecurrency '+ baseoncurrency)
    // if (credit_value != ""){
    $('.exclusivetable tbody tr').each(function () {
        var exclusivepercls=$(this).find('.exclusivepercls').val()
        if (exclusivepercls != ''){
        var exclusivetaxamount=exclusivepercls
        // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

        // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

        exclusivepercentage+=parseFloat(removecommaonly(exclusivepercls))
        }

        // var tax_percentage = $(this).find('.exclusivepercls').val()
        // // console.log(tax_percentage)
        // if (tax_percentage == '') {
        //     // calculate_exclusive_tax += 0
        //     $(this).find('.exclusivevalcls').val('')
        //     $(this).find('.taxvalcls').text('')
        // }
        // else {
        //     var exc_value = credit_value * tax_percentage / 100
        //     var con_val = decimal_value(exc_value)
        //     $(this).find('.exclusivevalcls').val(numberWithCommas(decimal_value(con_val)))
        //     $(this).find('.taxvalcls').text(global_currency_symbol + ' ' + numberWithCommas(decimal_value(con_val)))
        //     calculate_exclusive_tax += parseFloat(con_val)
        // }
    })
    var con_calculate_val = decimal_value(exclusivepercentage)
    // console.log('1',con_calculate_val)
    var add_totalvalue_tax = parseFloat(decimal_value(parseFloat(credit_value) + parseFloat(con_calculate_val)))
    // console.log('v',add_totalvalue_tax)
    $('#add_exclusive_value').val(con_calculate_val)
    $('#id_tot_exc').val('(' + global_currency_symbol + ' ' + numberWithCommas(decimal_value(con_calculate_val)) + ')')
    $('#id_totalalltax').val('(' + global_currency_symbol + ' ' + numberWithCommas(decimal_value(add_totalvalue_tax)) + ')')
    // $('#creditvalue_total').val('(' + global_currency_symbol + ' ' + numberWithCommas(decimal_value(add_totalvalue_tax)) + ')')

    $('#split-invoice-tbl tbody tr').each(function () {
        var percentage = $(this).find('.split-cls').attr('inv_percentage')
        var calculate_amount = add_totalvalue_tax * percentage / 100
        var con_val = parseFloat(decimal_value(calculate_amount))
        var get_curency_symbol = $(this).find('.inv_symbol').val()
        // console.log('con_val',calculate_amount)
        $(this).find('.base-amount-cls').val('(' + global_currency_symbol + ' ' + numberWithCommas(decimal_value(con_val)) + ')')
        var get_exchange_rate = $(this).find('.exchange-cls').val()
        if (get_exchange_rate != 'N/A') {
            if (get_exchange_rate != 0) {
                var exchange_with_amount = parseFloat(decimal_value(get_exchange_rate * con_val))
                // console.log('b',get_exchange_rate,'c',con_val,'as',typeof(exchange_with_amount))
                // convert to string interpolation
                $(this).find('.final-amount-cls').val(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exchange_with_amount))})`)
            }
        }
        else {
            // convert to string interpolation
            $(this).find('.final-amount-cls').val(`(${get_curency_symbol} ${numberWithCommas(decimal_value(con_val))})`)
        }
        var get_ven_id = $(this).find('.ven_id').val()
        // console.log($('.inv_sum_cls'+get_ven_id+' tbody tr'))
        $('.inv_sum_cls' + get_ven_id + ' tbody tr').each(function () {
            if (get_exchange_rate != 'N/A') {
                if (get_exchange_rate != 0) {
                    var total_val = credit_value
                    console.log({'total_val':total_val})
                    // console.log('total_val',total_val)
                    var totalval_finalval = parseFloat(decimal_value(decimal_value(total_val) * parseFloat(percentage) / 100)) || ''
                    console.log({'totalval_finalval':totalval_finalval})
                    // string interpolation
                    if (exchangetype == '1' || exchangetype == 1){
                        $('.inv' + get_ven_id + '').find('.finaldiscountcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(get_exchange_rate*totalval_finalval))})`)
                    }else {
                        $('.inv' + get_ven_id + '').find('.finaldiscountcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(get_exchange_rate*totalval_finalval))})`)

                    }
                    // console.log('sev',$('.inv'+get_ven_id+'').find('.finaldiscountcls').text(totalval_finalval))
                    // console.log('totalval_finalval',totalval_finalval)
                    var total_exclusive = $('#id_tot_exc').val().replace(/[^0-9.]/g, '') || 0;
                    // console.log('total_exclusive',total_exclusive)
                    var exclusive_finalval = parseFloat(decimal_value(decimal_value(total_exclusive) * parseFloat(percentage) / 100))
                    console.log({'exclusive_finalval':exclusive_finalval})
                    // console.log('exclusive_finalval',exclusive_finalval)
                    // string interpolation
                    if (exchangetype == '1' || exchangetype == 1){
                    $('.inv' + get_ven_id + '').find('.finaltaxcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exclusive_finalval*get_exchange_rate))})`)
                    }else{
                    $('.inv' + get_ven_id + '').find('.finaltaxcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(exclusive_finalval*get_exchange_rate))})`)
                    
                    }
                    var totalfinalval = parseFloat(decimal_value(totalval_finalval + exclusive_finalval))
                    console.log({'totalfinalval':totalfinalval})
                    // console.log('totalfinalval',totalfinalval)
                    var totalinclusive_finalvalue = parseFloat(decimal_value(get_exchange_rate * totalfinalval))
                    console.log({'totalinclusive_finalval':totalinclusive_finalvalue})
                    if (exchangetype == '1' || exchangetype == 1){
                        $('.inv' + get_ven_id + '').find('.totalsumcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalinclusive_finalvalue))})`)
                    }else{
                        $('.inv' + get_ven_id + '').find('.totalsumcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalinclusive_finalvalue))})`)
                    }
                }
            }
            else {
                
                var total_val = credit_value
                console.log({'total_val':total_val})
                // console.log('total_val',total_val)
                var totalval_finalval = parseFloat(decimal_value(decimal_value(total_val) * parseFloat(percentage)) / 100) || ''
                console.log({'totalval_finalval':totalval_finalval})
                // string interpolation

                if (exchangetype == '1' || exchangetype == 1){
                $('.inv' + get_ven_id + '').find('.finaldiscountcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalval_finalval))})`)
                }else{
                $('.inv' + get_ven_id + '').find('.finaldiscountcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalval_finalval))})`)
                }
                // console.log('sev',$('.inv'+get_ven_id+'').find('.finaldiscountcls').text(totalval_finalval))
                // console.log('totalval_finalval',totalval_finalval)
                var total_exclusive = $('#id_tot_exc').val().replace(/[^0-9.]/g, '') || 0;
                console.log({'total_exclusive':total_exclusive})
                // console.log('total_exclusive',total_exclusive)
                var exclusive_finalval = decimal_value(decimal_value(total_exclusive) * parseFloat(percentage) / 100)
                console.log({'exclusive_finalval':exclusive_finalval})
                // console.log('exclusive_finalval',exclusive_finalval)
                if (exchangetype == '1' || exchangetype == 1){
                $('.inv' + get_ven_id + '').find('.finaltaxcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(exclusive_finalval))})`)
                }else{
                $('.inv' + get_ven_id + '').find('.finaltaxcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(exclusive_finalval))})`)
                }
                var totalfinalval = (parseFloat(decimal_value(totalval_finalval)) + parseFloat(decimal_value(exclusive_finalval)))
                // console.log('totalfinalval',totalfinalval)
                if (exchangetype == '1' || exchangetype == 1){
                    $('.inv' + get_ven_id + '').find('.totalsumcls').text(`(${get_curency_symbol} ${numberWithCommas(decimal_value(totalfinalval))})`)
                }else{
                    $('.inv' + get_ven_id + '').find('.totalsumcls').text(`(${baseoncurrency} ${numberWithCommas(decimal_value(totalfinalval))})`)
                }
            }


        })

    })

}
// $(document).on('change', '.exchange-cls', function () {
//     var new_val = $(this).val().replace(/[^0-9\.]+/g, '');
//     new_val = Math.round(new_val * 1000) / 1000
//     $(this).val(new_val)
//     alert(new_val)
//     // $(this).val(decimal_value(new_val))
//     calculation_func()
// })
$(document).on('change','.exchange-cls',function(){
    var new_val=$(this).val().replace(/[^0-9\.]+/g,'');
   
    new_val = new_val.replace(/\./,"#").replace(/\./g,"").replace(/#/,".");
    // new_val = Math.round(new_val * 1000) / 1000
    // new_val = parseFloat(new_val).toFixed(2);
    $(this).val(new_val)
    // $(this).val(decimal_value(new_val))
    calculation_func()
});

$(document).on('click', '.com-save', function (e) {
    e.preventDefault()
    var submit_value = $(this).attr('value')
    if (submit_value == '0') {
        $("<input>").attr({ name: "submit_value", id: "hiddenId", type: "hidden", value: 0 }).appendTo("form");
        $('#creditnote1')[0].submit()
    }
    else if (submit_value == '1') {
        var validate_value = validation_func()
        if (validate_value == 0) {
            Swal.fire({
                text: 'Do You Want to Submit Credit Note?',
                showDenyButton: true,
                // showCancelButton: true,
                // textColor:'#77d61f',
                confirmButtonColor: '#77d61f',
                denyButtonColor: '#AF2B50',
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
                    $("<input>").attr({ name: "submit_value", id: "hiddenId", type: "hidden", value: 1 }).appendTo("form");
                    $('#creditnote1')[0].submit()
                    // window.location.href = '../list';
                    return true;
                }
            })
        }
    }
    else {
        var validate_value = validation_func()
        if (validate_value == 0) {
            $("<input>").attr({ name: "submit_value", id: "hiddenId", type: "hidden", value: 2 }).appendTo("form");
            $('#creditnote1')[0].submit()
        }
    }
})

function validation_func() {
    var count = 0;
    $('select').each(function () {
        var val = $(this).find(':selected').val()
        if (val == '') {
            count++;
            $(this).addClass('con_error')
        }
    })
    var inv_val = $('.invoicecls').val()
    if (inv_val.length == 0) {
        $('.select2-selection--multiple').addClass('con_error')
    }
    else {
        $('.select2-selection--multiple').removeClass('con_error')
    }

    $(".com_val, .credit-file-cls").each(function () {

        var val = $(this).val()
        if (val == '') {
            count++;
            // console.log($(this))
            $(this).addClass('con_error')
        }

    });

    $(".exclusivepercls").each(function () {
        var val = $.trim($(this).val());
        if (val == '') {
            count++;
            $(this).addClass('con_error').css('border-color', 'red');
        } else {
            $(this).removeClass('con_error').css('border-color', '');
        }
    });

    var new_val = $('#total_val_id').val();
    var remove = removecommaonly(new_val);
    if (remove.trim() === "") {
        count++;
        $('.totalvalue').addClass('con_error');
    } else {
        $('.totalvalue').removeClass('con_error');
    }
    

    return count
}

$(document).on('change', '.con_error', function () {
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

$(document).on('change', '.credit_name', function () {
    currentelement = $(this)
    $(this).closest('tr').find('.creditnumspancls').remove()
    var val = $(this).val() || null
    console.log('val', val)
    if (val != '') {
        $.ajax({
            type: "GET",
            url: '/credit/checkcreditno',
            data: { 'val': val },
            success: function (data) {
                if (data.data == "exists") {
                    currentelement.after('<span class="waring-err creditnumspancls">Credit number already exists</span>')
                    $('.com-save').attr('disabled', true)
                }
                else {
                    var z = 0
                    $(".credit_name").each(function (index, value) {
                        var y = $(value).val().toLowerCase();
                        var con_val = val.toLowerCase();
                        if (con_val != '' && y != '') {
                            if (con_val == y) {
                                // console.log("true",y)
                                z = z + 1;
                            }
                        }
                    })
                    // console.log("z",z)
                    if (z > 1) {
                        currentelement.after('<span class="waring-err creditnumspancls">Credit number already exists</span>')
                        $('.com-save').attr('disabled', true)
                    }
                    else {
                        $('.com-save').attr('disabled', false)
                    }

                }
            }
        })
    }
    else {
    }

    $('.styleremove').removeAttr('style')
    var current_row = $(this).closest('tr')
    check_credit_row(current_row)


    var get_ven_id = $(this).closest('tr').find('.ven_id').val()

    console.log('get_ven_id', get_ven_id)

    $('.inv' + get_ven_id).children('div').children('div').find('.p-value').text(val)



})

$(document).on('change', '.dateformat-cls', function () {
    // alert('123')

    var val = $(this).val() || null

    var id = $(this).closest('tr').find('.ven_id').val()
    // console.log('id',id)
    $('.inv' + id).children('div').children('div').find('.val-datecls').text(val)
    // $('.styleremove').removeAttr('style')
    var current_row = $(this).closest('tr')
    console.log('current_row', current_row)
    check_credit_row(current_row)



})

$(document).on('change', '.exchangecls', function () {
    // $('.styleremove').removeAttr('style')

    var id = $(this).closest('tr').find('.ven_id').val()

    var current_row = $(this).closest('tr')
    check_credit_row(current_row)




})

// $(document).on('change','.contract_no',function(){
//     console.log('its working')
//     $('#total_cost').val('')
// })


// function remove_char(value){
//     // value.replace(/[a-zA-Z`~!@#$%^&*()_|+\-=?;:'"<>\{\}\[\]\\\/]/gi, '');
//     value.replace(/[^0-9.]/g,'');
//     return value
// }
$(document).on('change', '.invoicecls', function () {
    var inv_status=$(this).find('option:selected').attr('inv_status')
    if (inv_status == 3){
        swal.fire('Invoice Paid, Credit Note to be applied to Subsequent Invoice.')
    }
    // alert('1322')
    var val = $('.invoicecls option:selected').text()
    var selected_date = $('.invoicecls option:selected').attr('data-id')
    console.log('da', selected_date)

    if(selected_date==undefined){
        $('#total_cost').val('')
        $('#total_val_id').val('.')
        $('#creditvalue_total').val(0)
        $('#id_tot_exc').val('')
        $('#id_totalalltax').val('')
        $('.exclusivevalcls').val('')
        $('.taxvalcls').text('')
    }
    // console.log('val',val)
    var splitval = val.split(',')
    var selected_date_split = selected_date.split(',')

    var currency_symbol = $('.contractcls').find(':selected').attr('currency_symbol')

    console.log('currency_symbol', currency_symbol)
    $('#basecurrency').val(currency_symbol)



    $('#total_val_id').val('.')
    $('#creditvalue_total').val(0)
    $('#total_val_id').trigger('change')
    $('#total_cost').val('')
    

    // $('.creditno').each(function (index, value) {
    //     $(this).val('CN/1/' + '' + splitval[index]);

    //     // console.log('val',$(this).val('CN/1/'+ +splitval[index]).val())
    //     var id = $(this).closest('tr').find('.ven_id').val()

    //     var current_split = $(this).closest('tr').val('CN/1/'+''+splitval[index]).val()
    //     console.log('current_split',current_split)
    //     $(this).closest('tr').find('.credit-date-cls').attr('inv_sel_date',selected_date_split[index])

    //     var current_split = $(this).closest('tr').val('CN/1/' + '' + splitval[index]).val()
    //     console.log('current_split', current_split)

    //     $('.inv' + id).children('div').children('div').find('.p-value').text(current_split)

    // })
    $.ajax({
        type: 'GET',
        url: '/credit/totalcost',
        data: { 'invoice_id': $(this).val() },
        async: false,
        success: function (data) {
            // $('#invoicetotalcost').val(data.cost)
            $('#total_cost').val(currency_symbol + ' ' + numberWithCommas(data.invoice_cost))
            console.log({'credit/totalcost':data})
            $('#credit_sum').val(data.credit_sum);
            $('#credit_sum_count').val(data.credit_sum_count);
            // alert(data.credit_sum)
            $('.creditno').each(function (index, value) {
                $(this).val('CN/' + data.serial_no + '/' + '' + splitval[index]);

                // console.log('val',$(this).val('CN/'+data.serial_no+'/'+ +splitval[index]).val())
                var id = $(this).closest('tr').find('.ven_id').val()

                var current_split = $(this).closest('tr').val('CN/' + data.serial_no + '/' + '' + splitval[index]).val()
                console.log('current_split', current_split)
                $(this).closest('tr').find('.credit-date-cls').attr('inv_sel_date', selected_date_split[index])

                var current_split = $(this).closest('tr').val('CN/' + data.serial_no + '/' + '' + splitval[index]).val()
                console.log('current_split', current_split)

                $('.inv' + id).children('div').children('div').find('.p-value').text(current_split)
            })
            var get_id = ''
            var get_percentage = ''
            exclusive=''
            
                $.each(data.new_list, function (key, val) {
                    exclusive += '<tr><td><select class="form-control exc-cls" disabled>'
                    exclusive += '<option value="' + val.percentage_id + '" data_id="' + val.percentage + '">' + val.tax_name + ' ' + val.percentage + '%</option>'
                    get_id += val.percentage_id
                    get_percentage += val.percentage
                    exclusive += '</select></td><td><input type="text"  class="exclusivepercls in-bor-clr width-decc" ></td><td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls new_exclusive" value=""> <input type="hidden" name="exclusive" value='+val.percentage_id+'><input type="hidden" name="exclusive_percentage" value='+val.percentage+'><p class="taxvalcls"></p></td></tr>'
                })
                $('.exclusivetable tbody').html(exclusive)
                // $('.exc-cls option[value="' + get_id + '"]').attr("selected", "selected");
                // $('.exclusivepercls').val(get_percentage)
                // $('.exc-cls').attr('disabled',true)
                // $('.exclusivepercls').attr('readonly', true)
                $('.exclusivetable').removeAttr('style')
                calculation_func()
            

        }
    })



})



$(document).on('change', '#total_val_id', function () {
    // alert(123)
    // var myStr = 'thisisatest';
    // var newStr = myStr.replace(/,/g, '-');

    // console.log('newStr', newStr );
    let ajax_value = parseInt($('#total_cost').val().replace(/[^0-9\.]/g, ''))
    let Tax = parseInt($('#id_totalalltax').val().replace(/[^0-9\.]/g, ''))
    let credit_total = parseInt($('#credit_sum').val().replace(/[^0-9\.]/g, ''))
    let credit_sum_count = parseInt($('#credit_sum_count').val())
    let this_value = parseInt($(this).val().replace(/[^0-9\.]/g, ''))
    $('#creditvalue_total').val(parseFloat($(this).val().replace(/[^0-9\.]/g,'')) || 0)
    let creditvalue_total = parseFloat($('#creditvalue_total').val());
    new_val=credit_total+creditvalue_total
    
    if (Tax > ajax_value || this_value == typeof NaN || new_val> ajax_value) {
        if (credit_sum_count > 0) {
            Swal.fire('Multi Credit Note values Exceeds Total Value of Invoice(s) - Balance Credit Note Value is ' + numberWithCommas(decimal_value(ajax_value - credit_total)))
        }else{
            Swal.fire('Total Value of Credit Note Exceeds Total Value of Invoice(s)')
        }

        $(this).val('')
        
        $('#id_tot_exc').val('')
        $('#id_totalalltax').val('')
        $('.base-amount-cls').val('')
        $('.final-amount-cls').val('')
        $('.exclusivevalcls').val('')
        $('.taxvalcls').text('')
        
    }
    else {
        $(this).val("(" + $('.contractcls').find(':selected').attr('currency_symbol')+" "+ $(this).val() + ")")
    }
})

function check_credit_row(tr) {
    let inv_id = tr.find('.ven_id').val()
    let credit_name = tr.find('.credit_name').val() || ''
    let credit_date = tr.find('.credit-date-cls').val() || ''
    let credit_exchange = tr.find('.exchange-cls').val() || ''
    if (credit_name != '' && credit_date && credit_exchange != '') {
        $('.inv' + inv_id + '').removeAttr('style')
    }
    else {
        $('.inv' + inv_id + '').css('style', 'none')
    }
}

function removecommaonly(x) {
    return x.replace(/[^0-9.]/g, '')
}

$(document).on('change','.exclusivepercls',function(){
    var val=$.trim($(this).val())
    var currency_symbol = $('.contractcls').find(':selected').attr('currency_symbol')
    var addval=$(this).val()
    const this_value = $(this).val()
    var numericValue = parseFloat(this_value.replace(/,/g, ''));
    // var formattedValue = numericValue.toLocaleString();
    var formattedValue = numericValue
    addval=removecommaonly(decimal_value(addval))
    if (numericValue == '' || isNaN(numericValue)){
        $(this).val('')
    }
    else{
        $(this).val(formattedValue)
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
$(document).on('keyup','.exclusivepercls',function(e){
    e.preventDefault();
    $(this).removeClass('con_error')
})


$(document).on('change', '.exclusivepercls', function () {

    let ajax_value = parseInt($('#total_cost').val().replace(/[^0-9\.]/g, ''));
    let Tax = parseInt($('#id_totalalltax').val().replace(/[^0-9\.]/g, ''));
    val=$.trim($(this).val());
    let this_value = parseFloat($(this).val().replace(/[^0-9\.]/g, ''));
    // $('#creditvalue_total').val(parseFloat($(this).val().replace(/[^0-9\.]/g,'')) || 0)
    if (Tax > ajax_value || this_value == typeof NaN) {
        Swal.fire('Total Value of Credit Note Exceeds Total Value of Invoice(s)');
        $(this).val(''); 
        
        $('#id_tot_exc').val('');
        $('#id_totalalltax').val('');
        $('.base-amount-cls').val('');
        $('.final-amount-cls').val('');
        $('.exclusivevalcls').val('');
        $('.taxvalcls').text('');
        
    }
    else {
        $(this).val(decimal_value(this_value)); 
    }
})