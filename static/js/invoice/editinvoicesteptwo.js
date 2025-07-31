
$(document).ready(function() {
    var submissionCount = 0;
    var maxSubmissions = 1; // Change this to the desired number of submissions
  
    $("form").submit(function(event) {
        submissionCount++;
        if (submissionCount >= maxSubmissions) {
            $(".generate_report_3").prop('disabled', true);
        }
    });
  });

// on load
$(document).ready(function(){
    let total_val = removeandlettercommaonly($('#id_totalvalue').val());

    let currency=$('.currency-clr').text()
    let splitcurrencysymbol=currency.split("-")
               if($('#id_totalvalue').prop('readonly')) {
                     $('#id_grossamountwithdis').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(total_val)));
                     $('#id_grossamountwithother').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(total_val)));;
  
               }
  
  })
$(document).ready(function(){
   
    let totalinvoice = totalvalueofinvoice
    
    if (totalinvoice == '' && $('#id_totalvalue').prop('readonly')){
        console.log("1st looop");
        $('.addinvoicecls').css('display','block');
    }
    else if(totalinvoice == ''){
        $('.addinvoicecls').css('display','none');


    }else{
        inv_func()
    }
})
// $.each(invoice_numbers, function(index, value) { 
// console.log(index + ': ' + value);
// });

if (vendorpaymentcount <= 1){
    // $('.addinvoicecls').removeAttr('style')
}
else{
    var milecount=1
    $('.duecls option').each(function(){
        if ($(this).text() == "Milestone Payment"){
            $(this).text('Milestone Payment-'+milecount)
            milecount ++;
        }
    })
}
// if (no_invoice == 1){
//     $('.addinvoicecls').css('display','none')
// }

if (no_invoice == created_invoices_count){
    $('.addinvoicecls').css('display','none')
}
else{
    $('.addinvoicecls').removeAttr("style")
}

// if (parseFloat(created_invoices_count) > 0){
//     $('.sum-heed').removeAttr('style')
// }


$('.jqtooltip').tooltip({ 
    content: function(callback) { 
        var value=$(this).prop('title').split('|')
        var html=''
        $.each(value, function(index, val) {
            html+='<p>'+val+'</p>'
        })
       callback(html); 
    }
  });

  $('.taxhead').tooltip({ 
    content: function(callback) { 
        var value=$(this).prop('title').split('|')
        var html=''
        $.each(value, function(index, val) {
            html+='<p>'+val+'</p>'
        })
       callback(html); 
    }
  });

  $('.taxnamehead').tooltip({ 
    content: function(callback) { 
        var value=$(this).prop('title').split('|')
        var html=''
        $.each(value, function(index, val) {
            html+='<p>'+val+'</p>'
        })
       callback(html); 
    }
  });

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


 
  

  
var optiondict={}
var list=[]

$("#id_tax option").each(function(){
    var thisOptionValue=$(this).val();
    var thispercentage=$(this).attr('dataid')
    var thistext=$(this).text()
    optiondict={"id":thisOptionValue,"taxname":thistext,"percentage":thispercentage}
   // optiondict=thisOptionValue
    list.push(optiondict)
});


var exclusiveoptiondict={}
var exclusivelist=[]
$("#id_exclusivetax option").each(function(){
    var thisOptionValue=$(this).val();
    var thispercentage=$(this).attr('dataid')
    var thistext=$(this).text()
    exclusiveoptiondict={"id":thisOptionValue,"taxname":thistext,"percentage":thispercentage}
   // exclusiveoptiondict=thisOptionValue
    exclusivelist.push(exclusiveoptiondict)
});


var countoptiondict={}
var countlist=[]
$("#id_count option").each(function(){
    var thisOptionValue=$(this).val();
    var thistext=$(this).text()
    countoptiondict={"val":thisOptionValue,"count":thistext}
    countlist.push(countoptiondict)
});

var bankoptiondict={}
var banklist=[]
$("#id_bank option").each(function(){
    var thisOptionValue=$(this).val();
    var thistext=$(this).text()
    var thisdataid=$(this).attr('dataid')
    bankoptiondict={"id":thisOptionValue,"bankdetail":thistext,'currencyid':thisdataid}
    banklist.push(bankoptiondict)
});

var paymentoptiondict={}
var paymentlist=[]
$("#id_payment option").each(function(){
    var thisOptionValue=$(this).val();
    var percentage=$(this).attr('percentage')
    var type=$(this).attr('type')
    var day=$(this).attr('day')
    paymentoptiondict={"id":thisOptionValue,"percentage":percentage,'type':type,'day':day}
    paymentlist.push(paymentoptiondict)
});

console.log(paymentlist)
$('.invoicetblcls tbody tr').each(function(){
    var newArr=""
    var currencyid=$(this).find('td:eq(5)').find('.paymentcurrencycls').attr('dataid')
    newArr = banklist.filter(object => {
    return object.currencyid === currencyid;
    });
    console.log(newArr)
    var bankselectoption='<option value="" selected>--Select--</option>'
            
    $.each(newArr,function(key,value){
          bankselectoption+='<option value='+value.id+'>'+value.bankdetail+'</option>'
    })
    $(this).find('td:eq(4)').find('.bankdetailcls').html(bankselectoption)
})

var companycurrencyoptiondict={}
var companycurrencylist=[]
$("#id_companycurrency option").each(function(){
    var thisOptionValue=$(this).val();
    var thistext=$(this).text()
    companycurrencyoptiondict={"id":thisOptionValue,"currency":thistext}
    companycurrencylist.push(companycurrencyoptiondict)
});



var singlecurrency=$('#id_contractcurency').val()

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
function todegitvalues(x) {
    return newRoundOfTwoValues(x)
}


function splitWithReplaceComma(x) {
    if (x.indexOf(',') > -1){
       
        var value=x.split(' ')
        var replaced=value[1]
        return replaced.replace(/,/g , '')
    }
    else{
        var value=x.split(' ')
        return value[1]
    }

}
function replaceWithComma(x) {
    if (x.indexOf(',') > -1){
        var value=x.split(' ')
        var replaced=value[0]
        console.log({'value':value})
        console.log({'erty':replaced})
        return replaced.replace(/,/g , '')
    }
    else{
        var value=x.split(' ')
        return value[0]
    }

}

function splitWithCurrency(x) {
var value=x.split(' ')
return value[0]
}

function removecommaonly(x) {
    console.log({'lllll':x.replace(/[^a-zA-Z0-9.]/g, '')})
return x.replace(/[^a-zA-Z0-9.]/g, '')
}

function removeandlettercommaonly(x) {
    return x.replace(/[^0-9.]/g, '')
    }


function decimal_value(val){
    if(isNaN(val)){
        return 0
    }else if (val !=""){
        var con_val=val.toString()
        var remove_commas= con_val.replace(/,/g, "");
        console.log("aiosuj",remove_commas)
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




var global;

$(window).keydown(function(event){
if(event.keyCode == 13) {
  event.preventDefault();
  return false;
}
});


$(document).on('change','#id_totalvalue',function(){
   
$('.addinvoicecls').removeAttr('style')
var total_val = total_old_val

if (total_val == 'No Max Limit'){
}
if(Number($(this).val()) > Number(total_val)){
    swal.fire('Total Value Inputted Exceeds Total Maximum Value for Contract',contract_reference)
    $(this).val('.')
}

$(this).removeClass('error')

var getval=$(this).val()
var val=removeandlettercommaonly(getval)
$(this).val(numberWithCommas(decimal_value(val)))

if (getval != ''){
    $('.addinvoicecls').removeAttr('style')
}

$('.maincls').removeAttr("style")
$('.sub-cls').removeAttr("style")
$('#id_submit1').attr('disabled',false)
$('#id_draft1').attr('disabled',false)
var convert_intval=parseInt(val)
var currency=$('.currency-clr').text()
var splitcurrencysymbol=currency.split("-")
var checkvalue=0;
    $('.distblcls > tbody  > tr').each(function(index, tr){
        removeval=$(this).find('td:eq(4) > .disvalcls').text()
        if (removeval != ''){
            var replacetext = removeval.replace('-'+splitcurrencysymbol[0],'')
            var removecomma=replacetext.replace(/,/g , '')
            checkvalue += parseInt(removecomma)
        }
    })
    if (checkvalue >= parseFloat(val)){
        swal.fire('Total amount cannot be lesser than the discount')
        $(this).val(global)
    }
    else{
        var discountvalue=0
        $('#id_grossamountwithdis').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(val)))
        $('.distblcls > tbody  > tr').each(function(index, tr){
            gettype=$(this).find('td:eq(1) > .amounttypeclsedit :selected').val()
            if (gettype == 'percentage'){
                var disper=$(this).find('td:eq(2) > .disamountclsedit').val()
                var minusdisval=val*disper/100
                discountvalue+=parseFloat(minusdisval)
                console.log(minusdisval)
                $(this).find('td:eq(4) > .disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(minusdisval)))
                $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(minusdisval)))
            }
            else if (gettype == 'amount') {
                var disper=$(this).find('td:eq(2) > .disamountclsedit').val()
                $(this).find('td:eq(4) > .disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper))) 
                discountvalue+=parseFloat(disper) 
                $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper)))
            }
        })
        var finaldisvalue=parseFloat(val)-discountvalue
        $('#id_grossamountwithdis').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finaldisvalue)))

        var data=parseFloat(finaldisvalue)
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            console.log({'discounttext':discounttext})
            if (discounttext){
                var replacetext=discounttext.replace("+ "+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
                data+=parseFloat(removecomma)
        })
        var checktotalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
        var checkvalue=0;
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            if (discounttext){
                var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
            checkvalue += parseFloat(removecomma)
        })
        // console.log("c",checkvalue)
        // console.log("t",checktotalinvoice)
        // if (checkvalue >= parseFloat(checktotalinvoice)){
        //     $(this).val('')
        //     $(this).closest('td').next('td').next('td').find('.disvalcls').text('')
        //     swal.fire('Discount is exceeding the total amount')
        // }
        // else{
            console.log({'data':data})
            $('#id_grossamountwithother').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(data)))
         
            var finaldisvalue=parseFloat(data)
            console.log({'finaldisvalue':finaldisvalue})
          

        var exclusivepercentage=0
        $('.exclusivetable > tbody  > tr').each(function(index, tr){
            var exclusivepercls=$(this).find('.exclusivepercls').val()
            if (exclusivepercls != ''){
            var exclusivetaxamount=exclusivepercls
            console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
            // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
            }
        })

        var finalexctax=parseFloat(decimal_value(exclusivepercentage+finaldisvalue))
        $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
        $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))
    }

    // var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
    var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
    
    
    $('.invoicetblcls tbody tr').each(function(){
        var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
        var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
        var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
        var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
        // var baseamount=decimal_value(totalall_tax*percentage/100)
        var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
        $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
        if(exchangetype == "1"){
            if (splitcurrencysymbol[0] == currencysymbol){
                $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                        
                        finaldisvalue=parseFloat(decimal_value(finaldisvalue))
                        var disinvoiceper=finaldisvalue*percentage/100
                         $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                         var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                         $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                        $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                         })
            }
            else{
                var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
            }
            if (exchangetypevalue == "N/A"){
                
                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=finaldisvalue*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=disinvoiceper+excinvoiceper
                var addamount=parseFloat(decimal_value(baseamount))*parseFloat(1)
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                // $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                //     var disinvoiceper=finaldisvalue*percentage/100
                //     console.log(disinvoiceper)
                //      $(this).find('td:eq(0)').find('.finaldiscountcls').text(currencysymbol+' '+numberWithCommas(disinvoiceper))
                //      var excinvoiceper=finalexctax*percentage/100
                //      $(this).find('td:eq(0)').find('.finaltaxcls').text(currencysymbol+' '+numberWithCommas(excinvoiceper))
                //     var finalalltotalinvoice=disinvoiceper*excinvoiceper
                //     $(this).find('td:eq(0)').find('.totalsumcls').text(currencysymbol+' '+numberWithCommas(finalalltotalinvoice))
                // })
            }
            else{
                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=parseFloat(decimal_value(finaldisvalue*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(decimal_value(exclusivepercentage*percentage/100)*parseFloat(decimal_value(exchangetypevalue))))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=disinvoiceper+excinvoiceper
                var addamount=parseFloat(decimal_value(baseamount))*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))

            }
            
        }
        else{
            //var addbaseamount=totalall_tax*percentage
            $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=parseFloat(decimal_value(finaldisvalue*percentage/100))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
        }

        // var index=$(this).find('td:eq(3)').find('.percls').attr('index')
        // $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
        //     var disinvoiceper=finaldisvalue*percentage/100
        //      $(this).find('td:eq(0)').find('.finaldiscountcls').text(currencysymbol+' '+numberWithCommas(disinvoiceper))
        //      var excinvoiceper=finalexctax*percentage/100
        //      $(this).find('td:eq(0)').find('.finaltaxcls').text(currencysymbol+' '+numberWithCommas(excinvoiceper))
        //     var finalalltotalinvoice=disinvoiceper*excinvoiceper
        //     $(this).find('td:eq(0)').find('.totalsumcls').text(currencysymbol+' '+numberWithCommas(finalalltotalinvoice))
        // })
    })

})
// show summary remove NaN value
$(document).on('change','input',function(){
let value1 = $('.finaldiscountcls').text()
let value2 = $('.totalsumcls').text()
let value3 = $('.finaltaxcls').text()
if (value1.includes('NaN')) {
$('.finaldiscountcls').text('')
}
if (value2.includes('NaN')) {
$('.totalsumcls').text('')
}
if (value3.includes('NaN')) {
$('.finaltaxcls').text('')
}
})
$(document).on('keyup','.disdesclsedit',function(){
$(this).next('.dis-span').remove()
var count=0
var val=$(this).val().toLowerCase();
if (val != ""){
    $('.disdesclsedit').each(function(){
        var current_val=$(this).val().toLowerCase();
        if (val == current_val){
            count ++;
        }

    })
}
console.log(count)
if (count > 1 ){
    $(this).after('<span class="dis-span error">Discount already exists</span>')
    $('.final-cls1').attr('disabled',true)
}
else{
    $(this).next('span').remove()
    $('.final-cls1').attr('disabled',false)
}

})


$(document).on('click','.addinvoiceclsbtn',function(){
// $('.con_invoice').removeAttr('style')
$('.coninvcls').addClass('highlightcls')
// $('.btnsumcls').removeAttr("style")
if (no_invoice != 1){
    $('.con_invoice').removeAttr('style')
}
if (no_invoice == 1){

// $('.con_invoice').removeAttr('style')
$('.invoicetblcls thead tr').find('th:eq(0)').text('Payment Currency-Split')
$('.invoicetblcls thead tr').find('th:eq(1)').text('Invoice No')
$('.invoicetblcls thead tr').find('th:eq(2)').text('Invoice Date')
$('.invoicetblcls thead tr').find('th:eq(3)').text('Percentage')
$('.invoicetblcls thead tr').find('th:eq(4)').text('Payment Currency')
$('.invoicetblcls thead tr').find('th:eq(5)').text('Amount in Base Currency')
$('.invoicetblcls thead tr').find('th:eq(6)').text('Exchange Rate')
$('.invoicetblcls thead tr').find('th:eq(7)').text('Amount in Payment Currency')
$('.invoicetblcls thead tr').find('th:eq(8)').text('Bank Details')
$('.invoicetblcls').find('thead tr th:eq(3)').css('display','none')
$('.invoicetblcls').find('thead tr th:eq(4)').css('display','none')
$('.btnsumcls').removeAttr('style')
$('.con_invoice tbody tr').find('.coninvcls > option').each(function(){
if ($(this).val() != ""){
    var val=$(this).val()
    var countrysymbol=$('#hdncomcurid').attr('dataid')
    $('.hd_con_cls').removeAttr('style')
    $('.invoicetblcls').removeAttr('style')
    var contractcurrencyid=$('#hdncomcurid').val()
    var percentage=$(this).attr('percentage')
    var currency=$(this).attr('currency')
    var currencyid=$(this).attr('currencyid')
    var exchangetype=$(this).attr('exchangetype')
var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))

//var finalvalue=totalall_tax*parseFloat(percentage)/100
var html='<tr>'
html+='<td><input type="hidden" name="hdnveninv" value=""><input type="hidden" name="contractinvoiceid" value="'+val+'" > <input type="hidden" name="invoicecurrencyid" value="'+currencyid+'" > <input type="text" name="splitinvoice" class="form-control in-bor-clr" value="'+currency+' '+percentage+'%" readonly></td><td><input type="text" name="invoicenum" class="form-control in-bor-clr invnumcls" index="'+val+'" percentage="'+percentage+'" companycurrency="'+countrysymbol+'" currencyid="'+currencyid+'" placeholder="Invoice Number"></td> <td><input type="text" name="invoicedate" class="form-control dateformat-cls in-bor-clr date-cls" index="'+val+'"></td> <td style="display:none;"><input type="text" name="percentage"  exchangetype="'+exchangetype+'" readonly class="form-control percls in-bor-clr" value="'+percentage+'" index="'+val+'"></td> <td><input type="text" name="basecurrencyamount" class="form-control baseamountcls" value="" readonly> <td style="display:none;"><input type="text" name="paymentcurrency" id="id_paymentcurrency" class="paymentcurrencycls form-control in-bor-clr" dataid="'+currencyid+'" value="'+currency+'" index="'+val+'" exchangetype="'+exchangetype+'" readonly></td>'
if (exchangetype == '1' && currencyid != contractcurrencyid){

    html+='<td><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="" index="'+val+'"></td>'   
    html+='<td><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" readonly index=""></td>'
}
else if (exchangetype == '1' && currencyid == contractcurrencyid){
    html+='<td><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="N/A" index="'+val+'" readonly ></td>' 
    
    var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
    var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
    // var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    var totalamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))

    // var totalamount=totalall_tax*parseFloat(percentage)/100
    
    html+='<td><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" value="'+currency+' '+numberWithCommas(decimal_value(totalamount))+'" readonly index=""></td>'

}
else{
    var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    var totalamount=totalall_tax*parseFloat(percentage)/100
    // var finalamount=totalamount
    $('.invoicetblcls').find('thead tr th:eq(6)').css('display','none')
    $('.invoicetblcls').find('thead tr th:eq(7)').css('display','none')
    // $(this).closest('table').find('thead tr th .hide_head_cls').css('display','none')
    html+='<td style="display:none;"><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="N/A" index="'+val+'" readonly></td>' 

    //var totalamount=totalall_tax*parseFloat(percentage)/100
    html+='<td style="display:none;"><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" value="'+currency+' '+numberWithCommas(decimal_value(totalamount))+'" readonly index=""></td>'

}
    
html+='<td><select name="bank" class="form-control bankdetailcls in-bor-clr" index="'+val+'"></select></td></tr>' 
//<td><button type="button" class="removerowcls clo-ss"><i class="fa fa-close" aria-hidden="true"></i></button></td>

// $('.invoicetblcls thead').html(thname)
$('.invoicetblcls tbody').html(html)

$('.invoicetblcls tbody tr:last').each(function(){
    var newArr=""
    var currencyid=$(this).find('td:eq(5)').find('.paymentcurrencycls').attr('dataid')
    newArr = banklist.filter(object => {
    return object.currencyid === currencyid;
    });
    console.log(newArr)
    var bankselectoption='<option value="" selected>--Select--</option>'
            
    $.each(newArr,function(key,value){
        bankselectoption+='<option value='+value.id+'>'+value.bankdetail+'</option>'
    })
    $(this).find('td:eq(8)').find('.bankdetailcls').html(bankselectoption)
})
$('.invoicetblcls').removeAttr('style')
$('.invdetailcls').removeAttr('style')
}            
})
}
else{
$('.addinvoicecls').removeAttr("style")
}

})

$(document).on('change','.coninvcls',function(){
$(this).removeClass('highlightcls')
var val=$(this).val()

if (val != ""){
    // var oninput="this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');"
    var countrysymbol=$('#hdncomcurid').attr('dataid')
    $('.hd_con_cls').removeAttr('style')
    $('.invoicetblcls').removeAttr('style')
    $('.invoicetblcls thead tr').find('th:eq(0)').text('Payment Currency-Split')
    $('.invoicetblcls thead tr').find('th:eq(1)').text('Invoice No')
    $('.invoicetblcls thead tr').find('th:eq(2)').text('Invoice Date')
    $('.invoicetblcls thead tr').find('th:eq(3)').text('Percentage')
    $('.invoicetblcls thead tr').find('th:eq(4)').text('Payment Currency')
    $('.invoicetblcls thead tr').find('th:eq(5)').text('Amount in Base Currency')
    $('.invoicetblcls thead tr').find('th:eq(6)').text('Exchange Rate')
    $('.invoicetblcls thead tr').find('th:eq(7)').text('Amount in Payment Currency')
    $('.invoicetblcls thead tr').find('th:eq(8)').text('Bank Details')
    
    var contractcurrencyid=$('#hdncomcurid').val()
    var percentage=$(this).find(':selected').attr('percentage')
    var currency=$(this).find(':selected').attr('currency')
    var currencyid=$(this).find(':selected').attr('currencyid')
    var exchangetype=$(this).find(':selected').attr('exchangetype')
    $('.coninvcls option').each(function(){
        if ($(this).val() == val){
            $(this).remove()
        }
    })
    if (exchangetype == '2'){
        $('.invoicetblcls').find('thead tr th:eq(3)').css('display','none')
        $('.invoicetblcls').find('thead tr th:eq(4)').css('display','none')
        $('.invoicetblcls').find('thead tr th:eq(6)').css('display','none')
        $('.invoicetblcls').find('thead tr th:eq(7)').css('display','none')
    }
    else{
        $('.invoicetblcls').find('thead tr th:eq(3)').css('display','none')
        $('.invoicetblcls').find('thead tr th:eq(4)').css('display','none')
    }

    var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    
    //var finalvalue=totalall_tax*parseFloat(percentage)/100
    var html='<tr>'
    html+='<td><input type="hidden" name="hdnveninv" value=""> <input type="hidden" name="contractinvoiceid" value="'+val+'" > <input type="hidden" name="invoicecurrencyid" value="'+currencyid+'" > <input type="text" name="splitinvoice" class="form-control in-bor-clr" value="'+currency+' '+percentage+'%" readonly></td><td><input type="text" name="invoicenum" class="form-control in-bor-clr invnumcls" index="'+val+'" percentage="'+percentage+'" companycurrency="'+countrysymbol+'" currencyid="'+currencyid+'" placeholder="Invoice Number"></td> <td><input type="text" name="invoicedate" class="form-control dateformat-cls in-bor-clr date-cls" index="'+val+'"></td> <td style="display:none;"><input type="text" name="percentage"  exchangetype="'+exchangetype+'" readonly class="form-control percls in-bor-clr" value="'+percentage+'" index="'+val+'"></td> <td><input type="text" name="basecurrencyamount" class="form-control baseamountcls" value="" readonly> <td style="display:none;"><input type="text" name="paymentcurrency" id="id_paymentcurrency" class="paymentcurrencycls form-control in-bor-clr" dataid="'+currencyid+'" value="'+currency+'" index="'+val+'" exchangetype="'+exchangetype+'" readonly></td>'
    if (exchangetype == '1' && currencyid != contractcurrencyid){
        html+='<td><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="" index="'+val+'"></td>'   
        html+='<td><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" readonly index=""></td>'
    }
    else if (exchangetype == '1' && currencyid == contractcurrencyid){
        html+='<td><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="N/A" index="'+val+'" readonly></td>' 
        var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
        var totalamount=totalall_tax*parseFloat(percentage)/100
        html+='<td><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" value="'+currency+' '+numberWithCommas(decimal_value(totalamount))+'" readonly index=""></td>'
    }
    else{
        var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
        var totalamount=totalall_tax*parseFloat(percentage)/100
        // var finalamount=totalamount
        $('.invoicetblcls').find('thead tr th:eq(6)').css('display','none')
        $('.invoicetblcls').find('thead tr th:eq(7)').css('display','none')
        // $(this).closest('table').find('thead tr th .hide_head_cls').css('display','none')
        html+='<td style="display:none;"><input type="text" name="exchangerate" id="id_exchangerate" class="exchangeratecls form-control in-bor-clr" dataid="" value="N/A" index="'+val+'" readonly></td>' 

        //var totalamount=totalall_tax*parseFloat(percentage)/100
        html+='<td style="display:none;"><input type="text" name="amount" id="id_amount" class="amountcls form-control in-bor-clr" placeholder="" value="'+currency+' '+numberWithCommas(decimal_value(totalamount))+'" readonly index=""></td>'

    }
    
    html+='<td><select name="bank" class="form-control form-select bankdetailcls in-bor-clr" index="'+val+'"></select></td><td class="text-center"><button type="button" class="removerowcls clo-ss"><i class="fa fa-close" aria-hidden="true"></i></button></td></tr>' 
    $('.invoicetblcls').append(html)
    $('.invoicetblcls tbody tr:last').each(function(){
        var newArr=""
        var currencyid=$(this).find('td:eq(5)').find('.paymentcurrencycls').attr('dataid')
        newArr = banklist.filter(object => {
        return object.currencyid === currencyid;
        });
        console.log(newArr)
        var bankselectoption='<option value="" selected>--Select--</option>'
                
        $.each(newArr,function(key,value){
            bankselectoption+='<option value='+value.id+'>'+value.bankdetail+'</option>'
        })
        $(this).find('td:eq(8)').find('.bankdetailcls').html(bankselectoption)
    })
    $('.invoicetblcls').removeAttr('style')
    $('.btnsumcls').removeAttr('style')
    
    var tablen=$('.invoicetblcls tbody tr').length
    var coninvoicecount=parseInt(no_invoice)
    if (tablen == coninvoicecount){
        $('.addinvoiceclsbtn').css('display','none')
        $('.con_invoice').css('display','none')
    }
}
})

// $(document).on('change','.exchangeratecls',function(){
//     var val=parseFloat($(this).val())
//     var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
//     var percentage=parseFloat($(this).closest('tr').find('.percls').val())
//     var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
//     var totalamount=totalall_tax*percentage/100
//     var finalamount=totalamount*val
//     $(this).closest('td').next('td').find('.amountcls').val(currency+' '+numberWithCommas((finalamount).toFixed(2)))
// })



$(document).on('click','.removerowcls',function(){
$('.addinvoicecls').removeAttr('style')
$('.addinvoiceclsbtn').removeAttr('style')
var percentage=$(this).closest('tr').find('.percls').val()
var invoiceid=$(this).closest('tr').find('.percls').attr('index')
var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
var exchangetype=$(this).closest('tr').find('.paymentcurrencycls').attr('exchangetype')
$('.coninvcls').append('<option value="'+invoiceid+'" percentage="'+percentage+'" currency="'+currency+'" currencyid="'+currencyid+'" exchangetype="'+exchangetype+'">'+currency+'-'+percentage+'%</option>')
console.log($('.coninvcls'))
$('.con_invoice').css('display','none')
var table_len=$('.invoicetblcls tbody tr').length
if (table_len > 1){
    $('.invoicesummarycls'+invoiceid+'').html('')
    console.log(('.invoicesummarycls'+invoiceid+''))
    $(this).closest('tr').remove()
}else{
    $('.invoicesummarycls'+invoiceid+'').html('')
    $('.invdetailcls').css('display','none')
    $('.summarytblcls').css('display','none')
    $(this).closest('tr').remove()
    $('.invoicetblcls').css('display','none')

}
$
})

$('.sum-btn').on('click',function(){
$('.inhead').removeAttr('style')
$('.summarytblcls').removeAttr('style')
})



$('.hide-btn').on('click',function(){
$('.summarytblcls').css('display','none')
})


$(document).on('change','.exclusivecls',function(){
var val=$(this).val()
var currency=$('.currency-clr').text()
var splitcurrencysymbol=currency.split("-")
var totalvalue=parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val()))
if (val != ''){
    $(this).closest('tr').find('#add-row').attr('disabled',false)
    $(this).closest('tr').find('.exclusivepercls').removeAttr('readonly')
    // var percentage=$(this).find(':selected').attr('dataid')
    // $(this).closest('td').next('td').find('.exclusivepercls').val(percentage)
    var addval=totalvalue
    // $(this).closest('td').next('td').next('td').next('td').find('.taxvalcls').text(splitcurrencysymbol[0]+
    // ' '+numberWithCommas(decimal_value(addval)))
    // $(this).closest('td').next('td').next('td').next('td').find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(addval)))
    $(this).closest('tr').find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+((addval)))
    var count=0
    $('.taxvalcls').each(function(){
        if ($.trim($(this).text()) != ''){
        var val=splitWithReplaceComma($(this).text())
        count += parseFloat(val)
        }
    })
    
    // var count=0
    // $('.taxvalcls').each(function(){
    //     var val=splitWithReplaceComma($(this).text())
    //     count += parseFloat(val)
    // })
    // console.log(count)
    // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(count)))
    totalvalue += count
    // $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(totalvalue)))

    // console.log("totalvalue",totalvalue)
    // var finaldisvalue=parseFloat(splitWithReplaceComma($('.grossamountwithdiscls').val()))
    // var totalall_tax=parseFloat(totalvalue)
    // var finalexctax=parseFloat(count)+finaldisvalue
    // $('.invoicetblcls tbody tr').each(function(){
    // var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
    // var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
    // var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
    // var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
    // var baseamount=totalall_tax*percentage/100
    // $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
    // if(exchangetype == "1"){
    // if (splitcurrencysymbol[0] == currencysymbol){
    // $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
    // var index=$(this).find('td:eq(3)').find('.percls').attr('index')
    // $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
    // var disinvoiceper=finaldisvalue*percentage/100
    // $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
    // var excinvoiceper=finalexctax*percentage/100
    // $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
    // var finalalltotalinvoice=disinvoiceper*excinvoiceper
    // $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    // })
    // }
    // else{
    // var addamount=baseamount*parseFloat(exchangetypevalue)
    // $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(deciimal_value(addamount)))
    // }
    // if (exchangetypevalue == "N/A"){
    // var index=$(this).find('td:eq(3)').find('.percls').attr('index')
    // var disinvoiceper=finaldisvalue*percentage/100
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
    // var excinvoiceper=parseFloat(count)*percentage/100
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
    // var finalalltotalinvoice=disinvoiceper+excinvoiceper
    // $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    // }
    // else{
    // var index=$(this).find('td:eq(3)').find('.percls').attr('index')
    // var disinvoiceper=finaldisvalue*percentage/100*parseFloat(exchangetypevalue)
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
    // var excinvoiceper=parseFloat(count)*percentage/100*parseFloat(exchangetypevalue)
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
    // var finalalltotalinvoice=disinvoiceper+excinvoiceper
    // $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))

    // }
    // }
    // else{
    // $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
    // var index=$(this).find('td:eq(3)').find('.percls').attr('index')
    // var disinvoiceper=finaldisvalue*percentage/100
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
    // var excinvoiceper=parseFloat(count)*percentage/100
    // $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
    // var finalalltotalinvoice=disinvoiceper+excinvoiceper
    // $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    // }
    // })

   
}else{

    $(this).closest('tr').find('#add-row').attr('disabled',true) 
    $(this).closest('tr').find('.exclusivepercls').val('')
    $(this).closest('tr').find('.taxvalcls').text('')
    $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+0)
    $(this).closest('tr').find('.exclusivepercls').attr('readonly','readonly')
    $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(totalvalue)))
}


// $('.invoicetblcls tbody tr').each(function(){
//     var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
//     var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
//     var sumval=totalall_tax*percentage/100
//     $(this).find('td:eq(5)').find('.amountcls').val(numberWithCommas(sumval))
// })

})

let exclusive_tax_value=1

$(document).on('click','#add-row',function(){
var html='<tr><td class="cat-wid"> <input type="hidden" name="hdninvexcl" value=""> <select name="exclusive" class="form-control exclusivecls in-bor-clr"></select></td> <td class=""><input type="text" name="" class="form-control exclusivepercls in-bor-clr width-decc" readonly ></td><td><input type="hidden" class="exclusive_percentage" readonly><input type="hidden" name="exclusive_percentage" value="" class="percentage_in_num"></td><td class=""> <button id="add-row" class="btn-clr add-row btn add-btn" type="button" value="add" disabled><i class="fa fa-plus"></i></button> <button id="delete-row" class="btn-clr delete-row btn add-btn" type="button" value="delete"><i class="fa fa-minus"></i></button> </td> <td class="per-wid"><input type="hidden" name="exclusive_value" class="exclusivevalcls"> <p class="taxvalcls"></p></td> </tr>'
$(this).closest('tbody').append(html)
exclusive_tax_value += 1;
var newArr=""
var selectedoptionarray=[];
$('.exclusivecls').each(function(){
    var currentvalue=$(this).find(':selected').val()
    if (currentvalue != undefined){
        selectedoptionarray.push(currentvalue)
    }
})
var selectoption='<option value="" dataid="">--Select--</option>'
$(exclusivelist).each(function(i,v){   
    selectoption+='<option value='+v.id+' dataid='+v.percentage+'>'+v.taxname+' -'+v.percentage+'%</option>'
})     
$(this).closest('tbody').find('tr').last().find('.exclusivecls').html(selectoption)
$(selectedoptionarray).each(function(i,v){ 
    console.log($('.exclusivetable tbody tr:last').find('.exclusivecls option[value='+v+']').remove())
 })
})


$(document).on('click','#delete-row',function(){
var currency=$('.currency-clr').text()
var splitcurrencysymbol=currency.split("-")
var tablelen=$('.exclusivetable tbody tr').length
var totalvalue=parseFloat(decimal_value(splitWithReplaceComma($('#id_grossamountwithother').val())))
if (tablelen > 1){
    $(this).closest('tr').remove()
    exclusive_tax_value -=1
    var count=0
    var symbol=splitWithCurrency($('#id_totalexclusivetax').val())
    $('.taxvalcls').each(function(){
        if ($.trim($(this).text()) != ''){
        var val=splitWithReplaceComma($(this).text())
        count += parseFloat(val)
        }
    })
    console.log(count)
    $('#id_totalexclusivetax').val(symbol+' '+numberWithCommas(decimal_value(count)))
    totalvalue += count
    $('#id_totalalltax').val(symbol+' '+numberWithCommas(decimal_value(totalvalue)))

    var finaldisvalue=parseFloat(decimal_value(splitWithReplaceComma($('.grossamountwithdiscls').val())))
    // var totalall_tax=parseFloat(decimal_value(totalvalue))
    var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
    var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
    var finalexctax=parseFloat(decimal_value(parseFloat(count)+finaldisvalue))
    $('.invoicetblcls tbody tr').each(function(){
    var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
    var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
    var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
    var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
    // var baseamount=totalall_tax*percentage/100
    var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
    $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
    if(exchangetype == "1"){
    if (splitcurrencysymbol[0] == currencysymbol){

            $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
            $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
            var disinvoiceper=finaldisvalue*percentage/100
            $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
            var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
            $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
            $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    })
    }
    else{
    var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
    }
    if (exchangetypevalue == "N/A"){

        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
        var disinvoiceper=finaldisvalue*percentage/100
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
        var excinvoiceper=parseFloat(decimal_value(parseFloat(count)*percentage/100))
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    }
    else{

        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
        var disinvoiceper=finaldisvalue*percentage/100*parseFloat(decimal_value(exchangetypevalue))
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
        var excinvoiceper=parseFloat(decimal_value(parseFloat(count)*percentage/100*parseFloat(decimal_value(exchangetypevalue))))
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))

    }
    }
    else{

        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
        var disinvoiceper=finaldisvalue*percentage/100
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
        var excinvoiceper=parseFloat(decimal_value(parseFloat(count)*percentage/100))
        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
    }
    })
}

})

var globaltext;
$(document).on('change','.invnumcls',function(){
$(this).next('span').remove()
var currentelement=$(this)
var val=$(this).val()||null
var index=$(this).attr('index') 
var duplicatecount=0
var companycurid=$('#hdncomcurid').val()
var companycursymbol=$('#hdncomcurid').attr('dataid')
var current_currency=$(this).closest('tr').find('#id_paymentcurrency').val()
var currencyid=$(this).attr('currencyid')
var percentage=$(this).attr('percentage')
var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
let id_exchangerate=$(this).closest('tr').find('#id_exchangerate').val()
if (id_exchangerate == 'N/A'){
    id_exchangerate=1
}
else{
    id_exchangerate=parseFloat(id_exchangerate)
}

var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
var finalvalue=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))


// var finalvalue=parseFloat(decimal_value(totalall_tax*parseFloat(percentage)/100))
if (val != null){
    $('.invnumcls').each(function(){
        if ($(this).val().toLowerCase() == val.toLowerCase()){
            duplicatecount ++;
        }
    })
    if (duplicatecount > 1){
        $(this).closest('input').after('<span class="waring-err invoicenumspn">Invoice number already exists</span>')
    }
    else if ($.inArray(val, invoice_numbers) != -1){
        console.log('old data')
    }
    else{
        $.ajax({
                    type:"GET",
                    url:'/invoice/checkvendorinvoice',
                    data:{'invoice_num':val,'vendorId':invoice_vendor_id},
                    async:false,
                    success: function(data){
                        console.log(data)
                        if (data.data == "exists"){
                            currentelement.after('<span class="waring-err invoicenumspn">Invoice number already exists</span>')
                        }
                    }
                })
    }
    $(this).closest('tr').find('.baseamountcls').val(companycursymbol+' '+(numberWithCommas(decimal_value(finalvalue))))
    if (currencyid == companycurid){    
        $(this).closest('tr').find('.amountcls').val(current_currency+' '+(numberWithCommas(decimal_value(id_exchangerate*finalvalue))))  
    }
}
else{
    $(this).closest('tr').find('.baseamountcls').val('')
    $(this).closest('tr').find('.amountcls').val('') 
    $(this).closest('tr').find('.exchangeratecls').val('')

}

var date=$(this).closest('tr').find('.dateformat-cls').val()|| null
var percentage=$(this).closest('tr').find('.percls').val()
var bankdetails=$(this).closest('tr').find('.bankdetailcls > :selected').val()|| null
var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
var exchangetype=$(this).closest('tr').find('.paymentcurrencycls').attr('exchangetype')
var exchangerate=$(this).closest('tr').find('.exchangeratecls').val()||null
if (exchangetype == '1'){
    if (companycurid == currencyid){
        var checkallfield=Checkfunc(val,date,bankdetails,exchangerate=true)
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var disfinalval=discountval*parseFloat(percentage)/100*parseFloat(exchangetype)
        // var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(decimal_value(splitWithReplaceComma(inv_exclusivetax)))
        }
        var taxfinalval=parseFloat(decimal_value(decimal_value(totalexclusivetax*parseFloat(percentage)/100)*parseFloat(exchangetype)))
        var finaltotalvalue=disfinalval+taxfinalval
    }
    else{
        var checkallfield=Checkfunc(val,date,bankdetails,exchangerate)
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var disfinalval=discountval*parseFloat(percentage)/100
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(splitWithReplaceComma(inv_exclusivetax))
        }

        var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100))
        var finaltotalvalue=disfinalval+taxfinalval
    }
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }

        var html = '';

        disfinalval=parseFloat(decimal_value(disfinalval))
        datafinal=parseFloat(decimal_value(disfinalval*id_exchangerate))
        finaltotalvalue=parseFloat(decimal_value(finaltotalvalue))
        html+='<div class="row"> <div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"><p class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+val+'</p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+date+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"> </div></div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+currency+' '+numberWithCommas(decimal_value(datafinal))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+currency+' '+numberWithCommas(decimal_value(taxfinalval*id_exchangerate))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+currency+' '+numberWithCommas(decimal_value(finaltotalvalue*id_exchangerate))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div> '
        $('.invoicesummarycls'+index+'').removeAttr('style')
        $('.invoicesummarycls'+index+'').html(html)
        
        //$('.invoicesummarycls'+index+'').removeAttr('style') (checkallfield == true && companycurid != currencyid)
    }
    
    else {
        
        // var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val()))
        // var disfinalval=discountval*parseFloat(percentage)/100
        // var exchangewithdiscount=disfinalval*parseFloat(exchangerate)
        // var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
        // var taxfinalval=totalexclusivetax*parseFloat(percentage)/100
        // var exchangewithtax=taxfinalval*parseFloat(exchangerate)
        // var finaltotalvalue=exchangewithdiscount+exchangewithtax
        // var html = '';
        // html+='<div class="row"> <div class="col-1"></div> <div class="col-3"> <label class="sum-vew">Invoice No:<span class="sum-date">'+val+'</span></label></div> <div class="col-3"><label class="sum-vew">Date:<span class="sum-date">'+date+'</span></label></div> <div class="col-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-1"></div> </div> <div class="row"> <div class="col-1"></div> <div class="col-9"> <table class="inv_sum_cls"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currency+' '+numberWithCommas(exchangewithdiscount.toFixed(2))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currency+' '+numberWithCommas(exchangewithtax.toFixed(2))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val">'+currency+' '+numberWithCommas(finaltotalvalue.toFixed(2))+'</td></tr> </tbody></table></div> <div class="col-1"></div> </div> <div class="bot-liine"></div>'
        // $('.invoicesummarycls'+index+'').html(html)
    // $('.invoicesummarycls'+index+'').removeAttr('style')
    $('.invoicesummarycls'+index+'').html('')
    }
    
}
else{
    var checkallfield=Checkfunc(val,date,bankdetails,exchangerate=true)
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(splitWithReplaceComma(inv_exclusivetax))
        }
        
        var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100))
        var finaltotalvalue=parseFloat(decimal_value(disfinalval))+parseFloat(decimal_value(taxfinalval))
        var html = '';
        html+='<div class="row"><div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"> <p class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+val+'</p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+date+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"></div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+companycursymbol+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+companycursymbol+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+companycursymbol+' '+numberWithCommas(decimal_value(finaltotalvalue))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div>'
        $('.invoicesummarycls'+index+'').removeAttr('style')
        $('.invoicesummarycls'+index+'').html(html)
    }
    else{
        
        $('.invoicesummarycls'+index+'').html('')
    }

}

})

$(document).on('change','.dateformat-cls',function(){
$(this).next('span').remove()
var val=$(this).val()||null
var index=$(this).attr('index') 
var companycurid=$('#hdncomcurid').val()
var companycursymbol=$('#hdncomcurid').attr('dataid')
var duplicatecount=0
var invoicenum=$(this).closest('tr').find('.invnumcls').val()|| null
var percentage=$(this).closest('tr').find('.percls').val()
var bankdetails=$(this).closest('tr').find('.bankdetailcls > :selected').val()|| null
var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
var exchangerate=$(this).closest('tr').find('.exchangeratecls').val()||null
var exchangetype=$(this).closest('tr').find('.paymentcurrencycls').attr('exchangetype')
if (exchangetype == '1'){
    if (companycurid == currencyid){
        var checkallfield=Checkfunc(invoicenum,val,bankdetails,exchangerate=true)
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var disfinalval=discountval*parseFloat(percentage)/100
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(splitWithReplaceComma(inv_exclusivetax))
        }
        var taxfinalval=totalexclusivetax*parseFloat(percentage)/100
        var finaltotalvalue=disfinalval+taxfinalval
    }
    else{
        var checkallfield=Checkfunc(invoicenum,val,bankdetails,exchangerate)
        var discountval=parseFloat(decimal_value(splitWithReplaceComma($('#id_grossamountwithother').val())))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100*parseFloat(exchangerate)))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(splitWithReplaceComma(inv_exclusivetax))
        }
        var taxfinalval=parseFloat(decimal_value(decimal_value(totalexclusivetax*parseFloat(percentage)/100)*parseFloat(exchangerate)))
        var finaltotalvalue=parseFloat(decimal_value(disfinalval))+parseFloat(decimal_value(taxfinalval))
    }
    console.log(checkallfield)
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }
        var html = '';
        html+='<div class="row"><div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"><p   class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+invoicenum+'</p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+val+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"></div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+currency+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+currency+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+currency+' '+numberWithCommas(decimal_value(finaltotalvalue))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div>'
        $('.invoicesummarycls'+index+'').html(html)
        $('.invoicesummarycls'+index+'').removeAttr('style')
        //$('.invoicesummarycls'+index+'').removeAttr('style') (checkallfield == true && index != "0")
    }

    else{
        $('.invoicesummarycls'+index+'').html(html)
        // var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val()))
        // var disfinalval=discountval*parseFloat(percentage)/100
        // var exchangewithdiscount=disfinalval*parseFloat(exchangerate)
        // var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
        // var taxfinalval=totalexclusivetax*parseFloat(percentage)/100
        // var exchangewithtax=taxfinalval*parseFloat(exchangerate)
        // var finaltotalvalue=exchangewithdiscount+exchangewithtax
        // var html = '';
        // html+='<div class="row"> <div class="col-1"></div> <div class="col-3"><label class="sum-vew">Invoice No:<span class="sum-date">'+invoicenum+'</span></label></div> <div class="col-3"><label class="sum-vew">Date:<span class="sum-date">'+val+'</span></label></div> <div class="col-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-1"></div> </div> <div class="row"> <div class="col-1"></div> <div class="col-9"> <table class="inv_sum_cls"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currency+' '+numberWithCommas(exchangewithdiscount)+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currency+' '+numberWithCommas(exchangewithtax)+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val">'+currency+' '+numberWithCommas(finaltotalvalue)+'</td></tr> </tbody></table></div> <div class="col-1"></div> </div> <div class="bot-liine"></div>'
        // $('.invoicesummarycls'+index+'').html(html)
        //$('.invoicesummarycls'+index+'').removeAttr('style')

    }
}
else{
    
    var checkallfield=Checkfunc(invoicenum,val,bankdetails,exchangerate=true)
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(decimal_value(splitWithReplaceComma(inv_exclusivetax)))
        }  
 
        
        var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100))
        var finaltotalvalue=parseFloat(decimal_value(disfinalval))+parseFloat(decimal_value(taxfinalval))
        var html = '';
        html+='<div class="row"><div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"><p class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+invoicenum+'</p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+val+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"></div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+companycursymbol+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+companycursymbol+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+companycursymbol+' '+numberWithCommas(decimal_value(finaltotalvalue))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div> '
        $('.invoicesummarycls'+index+'').removeAttr('style')
        $('.invoicesummarycls'+index+'').html(html)
    }
    else{
        $('.invoicesummarycls'+index+'').html(html)
    }
}

})


$(document).on('change','.bankdetailcls',function(){
$(this).next('span').remove()
var bankdetails=$(this).find(':selected').val()||null
var index=$(this).attr('index') 
var duplicatecount=0
var invoicenum=$(this).closest('tr').find('.invnumcls').val()|| null
var date=$(this).closest('tr').find('.dateformat-cls').val()|| null
var companycurid=$('#hdncomcurid').val()
var companycursymbol=$('#hdncomcurid').attr('dataid')
var percentage=$(this).closest('tr').find('.percls').val()
var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
var exchangerate=$(this).closest('tr').find('.exchangeratecls').val()||null
var exchangetype=$(this).closest('tr').find('.paymentcurrencycls').attr('exchangetype')
if (exchangetype == '1'){
    if (companycurid == currencyid){
        var checkallfield=Checkfunc(invoicenum,date,bankdetails,exchangerate=true)
        var discountval=parseFloat(decimal_value(splitWithReplaceComma($('#id_grossamountwithother').val())))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(decimal_value(splitWithReplaceComma(inv_exclusivetax)))
        }
        var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100))
        var finaltotalvalue=disfinalval+taxfinalval
    }
    else{
        var checkallfield=Checkfunc(invoicenum,date,bankdetails,exchangerate)
        var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var new_val = discountval * parseFloat(percentage) / 100;
        var new_val=parseFloat(decimal_value(new_val))
        var disfinalval =parseFloat( decimal_value(new_val * parseFloat(exchangerate)));
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(splitWithReplaceComma(inv_exclusivetax))
        }
        var taxfinalval=parseFloat(decimal_value(decimal_value(totalexclusivetax*parseFloat(percentage)/100)*parseFloat(exchangerate)))
        var finaltotalvalue=disfinalval+taxfinalval
    }
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }

        var html = '';
        var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
        var baseamount = decimal_value(totalall_tax * percentage / 100);
        exchangetypevalue =$(this).find('td:eq(6)').find('.exchangeratecls').val() || null;
        var addamount = parseFloat(decimal_value(baseamount)) * exchangerate;
        var newbaseamount=parseFloat(decimal_value(disfinalval)) + parseFloat(decimal_value(taxfinalval));
        html+='<div class="row"><div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"> <p class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+invoicenum+'</p></div></div> <div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+date+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"></div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+currency+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+currency+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+currency+' '+numberWithCommas(decimal_value(newbaseamount))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div> '
        $('.invoicesummarycls'+index+'').removeAttr('style')
        $('.invoicesummarycls'+index+'').html(html)
        //$('.invoicesummarycls'+index+'').removeAttr('style') (checkallfield == true && index != "0")
    }

    else{
        $('.invoicesummarycls'+index+'').html(html)
        // var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val()))
        // var disfinalval=discountval*parseFloat(percentage)/100
        // var exchangewithdiscount=disfinalval*parseFloat(exchangerate)
        // var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
        // var taxfinalval=totalexclusivetax*parseFloat(percentage)/100
        // var exchangewithtax=taxfinalval*parseFloat(exchangerate)
        // var finaltotalvalue=exchangewithdiscount+exchangewithtax
        // var html = '';
        // html+='<div class="row"> <div class="col-1"></div> <div class="col-3"><label class="sum-vew">Invoice No:<span class="sum-date">'+invoicenum+'</span></label></div> <div class="col-3"><label class="sum-vew">Date:<span class="sum-date">'+date+'</span></label></div> <div class="col-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-1"></div> </div> <div class="row"> <div class="col-1"></div> <div class="col-9"> <table class="inv_sum_cls"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currency+' '+numberWithCommas(exchangewithdiscount)+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currency+' '+numberWithCommas(exchangewithtax)+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val">'+currency+' '+numberWithCommas(finaltotalvalue)+'</td></tr> </tbody></table></div> <div class="col-1"></div> </div> <div class="bot-liine"></div>'
        // $('.invoicesummarycls'+index+'').html(html)
        //$('.invoicesummarycls'+index+'').removeAttr('style')

    }
}
else{
    
    var checkallfield=Checkfunc(invoicenum,date,bankdetails,exchangerate=true)
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
        var tablen=$('.invoicetblcls tbody tr').length
        console.log(coninvoicecount)
        console.log(tablen)
        if (tablen < coninvoicecount && tablen >= 1){
            Swal.fire({
            title: 'Do You Want To Add Another Invoice',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
          }).then((result) => {
            if (result.isConfirmed) {
                $('.con_invoice').css('display','none')
              }
               });
        }
        else{
            $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
        }
        var discountval=parseFloat(decimal_value(splitWithReplaceComma($('#id_grossamountwithother').val())))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(decimal_value(splitWithReplaceComma(inv_exclusivetax)))
        }

            var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100))
            var finaltotalvalue=parseFloat(decimal_value(disfinalval))+parseFloat(decimal_value(taxfinalval))
            var html = '';
            html+='<div class="row"><div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"> <p class="sum-vew">Invoice No :</p><p class="sum-date">'+invoicenum+'</p></div></div><div class="col-lg-3 col-md-5 cen-hed"><label class="sum-vew">Date :<span class="sum-date">'+date+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"></div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+companycursymbol+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+companycursymbol+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+companycursymbol+' '+numberWithCommas(decimal_value(finaltotalvalue))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div>'
            $('.invoicesummarycls'+index+'').removeAttr('style')
            $('.invoicesummarycls'+index+'').html(html)
    }
    else{
        $('.invoicesummarycls'+index+'').html(html)
    }
}

})


$(document).on('change','.exchangeratecls ',function(){
$(this).next('span').remove()
var value=$(this).val()
if ($.isNumeric(value)){
    new_val = value.replace(/\./,"#").replace(/\./g,"").replace(/#/,".");
    new_val = Math.round(value * 1000) / 1000
    new_val = value

    $(this).val(new_val);
    var val=parseFloat(decimal_value($(this).val()))
    var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    var percentage=parseFloat($(this).closest('tr').find('.percls').val())
    var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
    var totalamount=parseFloat(decimal_value(totalall_tax*percentage/100))
    var finalamount=totalamount*val
    $(this).closest('td').next('td').find('.amountcls').val(currency+' '+numberWithCommas(decimal_value(finalamount)))
    var exchangerate=$(this).val()||null
    var index=$(this).attr('index') 
    var duplicatecount=0
    var invoicenum=$(this).closest('tr').find('.invnumcls').val()|| null
    var date=$(this).closest('tr').find('.dateformat-cls').val()|| null
    var bankdetails=$(this).closest('tr').find('.bankdetailcls > :selected').val()|| null
    var companycurid=$('#hdncomcurid').val()
    var companycursymbol=$('#hdncomcurid').attr('dataid')
    var percentage=$(this).closest('tr').find('.percls').val()
    var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
    var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
    if (companycurid == currencyid){
        var checkallfield=Checkfunc(invoicenum,date,bankdetails,exchangerate=true)
    }
    else{
        var checkallfield=Checkfunc(invoicenum,date,bankdetails,exchangerate)
    }
    if (checkallfield == true){
        var coninvoicecount=parseInt(no_invoice)
            var tablen=$('.invoicetblcls tbody tr').length
            console.log(coninvoicecount)
            console.log(tablen)
            if (tablen < coninvoicecount && tablen >= 1){
                Swal.fire({
                title: 'Do You Want To Add Another Invoice',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
            }).then((result) => {
                if (result.isConfirmed) {
                    $('.con_invoice').css('display','none')
                }
                });
            }
            else{
                $('.addinvoiceclsbtn').css('display','none')
                $('.con_invoice').css('display','none')
            }
        var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
        var totalamountwithexchange=parseFloat(decimal_value(totalall_tax*percentage/100))*parseFloat(decimal_value(exchangerate))
        
        $(this).closest('td').next('td').find('.amountcls').val(currency+' '+numberWithCommas(decimal_value(totalamountwithexchange)))
        var discountval=parseFloat(decimal_value(splitWithReplaceComma($('#id_grossamountwithother').val())))
        var disfinalval=parseFloat(decimal_value(discountval*parseFloat(percentage)/100)*parseFloat(decimal_value(exchangerate)))
        var inv_exclusivetax=$('#id_totalexclusivetax').val()||0
        var totalexclusivetax;
        if ( inv_exclusivetax == ''){
            totalexclusivetax= 0
        }
        else{
            totalexclusivetax=parseFloat(decimal_value(splitWithReplaceComma(inv_exclusivetax)))
        }

        var taxfinalval=parseFloat(decimal_value(totalexclusivetax*parseFloat(percentage)/100)*parseFloat(exchangerate))
        var finaltotalvalue=disfinalval+taxfinalval
        var html = '';
        html+='<div class="row"> <div class="col-lg-1 col-md-0"> </div> <div class="col-lg-3 col-md-4"><div class="same-lline"> <p class="sum-vew p-head">Invoice No :</p><p class="sum-date p-value">'+invoicenum+'</p></div></div><div class="col-3"><label class="sum-vew">Date :<span class="sum-date">'+date+'</span></label></div> <div class="col-lg-3 col-md-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-lg-1 col-md-0"</div> </div> <div class="row"> <div class="col-lg-1 col-md-0"></div> <div class="col-lg-9 col-md-12"> <table class="inv_sum_cls bor-liness"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val finaldiscountcls">'+currency+' '+numberWithCommas(decimal_value(disfinalval))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val finaltaxcls">'+currency+' '+numberWithCommas(decimal_value(taxfinalval))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val totalsumcls">'+currency+' '+numberWithCommas(decimal_value(finalamount))+'</td></tr> </tbody></table></div> <div class="col-lg-1 col-md-0"></div> </div> '
        $('.invoicesummarycls'+index+'').removeAttr('style')
        $('.invoicesummarycls'+index+'').html(html)
        //$('.invoicesummarycls'+index+'').removeAttr('style') (checkallfield == true && index != "0")
    
    }

    else{
        // var discountval=parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val()))
        // var disfinalval=discountval*parseFloat(percentage)/100
        // var exchangewithdiscount=disfinalval*parseFloat(exchangerate)
        // var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
        // var taxfinalval=totalexclusivetax*parseFloat(percentage)/100
        // var exchangewithtax=taxfinalval*parseFloat(exchangerate)
        // var finaltotalvalue=exchangewithdiscount+exchangewithtax
        // var html = '';
        // html+='<div class="row"> <div class="col-1"></div> <div class="col-3"><label class="sum-vew">Invoice No:<span class="sum-date">'+invoicenum+'</span></label></div> <div class="col-3"><label class="sum-vew">Date:<span class="sum-date">'+date+'</span></label></div> <div class="col-3 ryt-ali"><label class="a-mount">Amount</label></div> <div class="col-1"></div> </div> <div class="row"> <div class="col-1"></div> <div class="col-9"> <table class="inv_sum_cls"><tbody> <tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currency+' '+numberWithCommas(exchangewithdiscount.toFixed(2))+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currency+' '+numberWithCommas(exchangewithtax.toFixed(2))+'</td></tr> <tr><th class="hed-inv-gro">Gross Total Inclusive of Taxes and Levies</th><td class="hed-inv-gro-val">'+currency+' '+numberWithCommas(finaltotalvalue.toFixed(2))+'</td></tr> </tbody></table></div> <div class="col-1"></div> </div> <div class="bot-liine"></div>'
        $('.invoicesummarycls'+index+'').html('')
    }
}
else{
    var new_val=(value.replace(/[^0-9 .]/g, ''));
    new_val = new_val.replace(/\./,"#").replace(/\./g,"").replace(/#/,".");
    new_val = Math.round(new_val * 1000) / 1000
    $(this).val(new_val);
    var val=parseFloat($(this).val())
    var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
    var percentage=parseFloat($(this).closest('tr').find('.percls').val())
    var currency=$(this).closest('tr').find('.paymentcurrencycls').val()
    var totalamount=parseFloat(decimal_value(totalall_tax*percentage/100))
    var finalamount=totalamount*parseFloat(decimal_value(val))
    $(this).closest('td').next('td').find('.amountcls').val(currency+' '+numberWithCommas(decimal_value(finalamount)))
    } 
})

   
function Checkfunc(number,date,bankdetails,exchangerate){
if (number != null && date != null && bankdetails != null && exchangerate != null){
    return true
}
else{
    return false 
}
}

$(document).on('change','.amounttypeclsedit',function(){
$(this).next('span').remove()
var val=$(this).val()
if (val != 'Not Applicable'){
    $(this).closest('tr').find('.disamountclsedit').attr('readonly',false)
    $(this).closest('tr').find('.disdesclsedit').attr('readonly',false) 
    $(this).closest('tr').find('#add_dis').removeAttr('style')
}
else{
    $(this).closest('tr').find('.disdesclsedit').attr('readonly',true)
    $(this).closest('tr').find('.disamountclsedit').attr('readonly',true)
    $(this).closest('tr').find('.disamountclsedit').val('')
    $(this).closest('tr').find('.disdesclsedit').val('')
    $(this).closest('tr').find('.discountvaluecls').val('')
    $(this).closest('tr').find('.disvalcls').text('')
    $(this).closest('tr').nextAll('tr').remove()
    $(this).closest('tr').find('#add_dis').css('display','none')
    $(this).closest('tr').find('.disdesclsedit').next('span').remove()
    $(this).closest('tr').find('.disamountclsedit').next('span').remove()
    var totalinvoice=parseFloat(decimal_value(removeandlettercommaonly($('#id_totalvalue').val())))
   
    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    $('.grossamountwithdiscls').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(totalinvoice)))
    var finaldisvalue=parseFloat(decimal_value(totalinvoice))
        var exclusivepercentage=0
        $('.exclusivetable > tbody > tr').each(function(index, tr){
            var exclusivepercls=$(this).find('.exclusivepercls').val()

            if (exclusivepercls != ''){
            var exclusivetaxamount=exclusivepercls
            console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
            // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
            }
        })
        var finalexctax=exclusivepercentage+finaldisvalue
        $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
        $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))

        // var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
        var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
        var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

        $('.invoicetblcls tbody tr').each(function(){
            var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
            var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
            var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
            var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
            // var baseamount=parseFloat(decimal_value(totalall_tax*percentage/100))


            var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
            $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
            
            if(exchangetype == "1"){
                if (splitcurrencysymbol[0] == currencysymbol){

                    $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                        // var disinvoiceper=finaldisvalue*percentage/100
                        var disinvoiceper=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))*percentage/100
                        $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        // var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                        var excinvoiceper=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))*percentage/100

                        $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                        $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    })
                }
                else{
                    var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                }
                if (exchangetypevalue == "N/A"){

                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }
                else{

                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=parseFloat(decimal_value(finaldisvalue*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }
            }
            else{

                $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=finaldisvalue*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
            }

        })
}
})




$(document).on('change','.exclusivecls',function(){
var val=$(this).val()
if (val != ''){
    $(this).closest('td').next('td').find('.exclusiveamtcls').attr('readonly',false)
}
else{
    $(this).closest('td').next('td').find('.exclusiveamtcls').attr('readonly',true)
}

})



/* discount starts here*/
var global_discount=''
$(document).on('change','.disamountclsedit',function(){
$(this).next('span').remove()
var conval=$(this).val()
console.log({'conval':conval})
var new_val=conval.replace(/[^0-9\.]+/g, "")
$(this).val(new_val)
if ($.isNumeric(conval)){
    var type=$(this).closest('td').prev('td').find('.amounttypeclsedit').val()
    var totalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
    global=totalinvoice

    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    var html='';
    if((conval == "")) {
        var val = 0
    }
    else{
        var val = parseFloat(conval)
    }
    //console.log('abc',val)
        if (type == 'percentage'){
            var discountval=parseFloat(totalinvoice)*val/100
            if(val != ''){
                $(this).closest('td').next('td').next('td').find('.disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(discountval)))
                $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(discountval)))
            }
            else{
                $(this).closest('td').next('td').next('td').find('.disvalcls').text('')
            }
        }
        else{
            if(val != ''){
            $(this).closest('td').next('td').next('td').find('.disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            }
            else{
                $(this).closest('td').next('td').next('td').find('.disvalcls').text('')      
            }
        }
        var data=parseFloat(totalinvoice)
        $('.distblcls > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('td:eq(4) > .disvalcls').text()
            if (discounttext){
                var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
                console.log(removecomma)
            }
            else{
                var removecomma =0
            }
                data-=parseFloat(removecomma)
        })
        var checktotalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
        var checkvalue=0;
        $('.distblcls > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('td:eq(4) > .disvalcls').text()
            if (discounttext){
                var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
            checkvalue += parseFloat(removecomma)
        })
        // console.log("c",checkvalue)
        // console.log("t",checktotalinvoice)
        if (checkvalue >= parseFloat(checktotalinvoice)){
            $(this).val('')
            $(this).closest('td').next('td').next('td').find('.disvalcls').text('')
            swal.fire('Discount is exceeding the total amount')
        }
        else{
            console.log({'data':data})
            $(this).closest('table').next('div').find('.grossamountwithdiscls').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(data)))
            //$('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(data))

            // var exclusiveamount=0
            // $('.exclusivetable > tbody  > tr').each(function(index, tr){
            //         var percentage=$(this).find('td:eq(1) > .exclusivepercls').val()
            //         if (percentage != ''){
            //             var sumval=parseFloat(data)*parseFloat(percentage)/100
            //             exclusiveamount += sumval
            //             $(this).find('td:eq(3) > .taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(sumval))
            //         }
            // })
            // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(exclusiveamount))
            // var finaltotalvalue=parseFloat(data)+exclusiveamount
            // $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(finaltotalvalue))
                

            // $('.invoicetblcls tbody tr').each(function(){
            //     var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
            //     var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
            //     var sumval=totalall_tax*percentage/100
            //     $(this).find('td:eq(5)').find('.amountcls').val(numberWithCommas(sumval))
            // })
            var other_value=0
            $('#otherstable > tbody  > tr').each(function(index, tr){
                    var disper=$.trim($(this).find('.others_amount').val())
                    if (disper == ''){
                        disper=0
                    }
                    console.log({'disper':disper})
                    $(this).find('.other_dis_val').text('+ '+splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper))) 
                    other_value+=parseFloat(disper) 
                    $(this).closest('tr').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper)))
            })
            var finalothervalue=parseFloat(data)+other_value
            $('#id_grossamountwithother').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalothervalue)))

            var finaldisvalue=parseFloat(decimal_value(finalothervalue))
            var exclusivepercentage=0
            $('.exclusivetable > tbody > tr').each(function(index, tr){
                var exclusivepercls=$(this).find('.exclusivepercls').val()
                if (exclusivepercls != ''){
                var exclusivetaxamount=exclusivepercls
                console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
                // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))
    
                // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))
    
                exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
                }
                })
            var finalexctax=parseFloat(decimal_value(exclusivepercentage+finaldisvalue))
            $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
            $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))

            var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
            $('.invoicetblcls tbody tr').each(function(){
                var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
                var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
                var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
                var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
                // var baseamount=parseFloat(decimal_value(totalall_tax*percentage/100))
                
                
                var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
                var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

                var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
                $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                if(exchangetype == "1"){
                    if (splitcurrencysymbol[0] == currencysymbol){

                        $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                            var disinvoiceper=finaldisvalue*percentage/100
                            $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                            $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                            $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        })
                    }
                    else{
                        var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                    }
                    if (exchangetypevalue == "N/A"){

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=finaldisvalue*percentage/100
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                    else{

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=decimal_value(finaldisvalue*percentage/100)*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                }
                else{
                    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }

            })


            }
}
else{
    // console.log(conval)
    var new_val=conval.replace(/[^0-9\.]+/g, "")
    $(this).val(new_val)
}       
})

$(document).on('click','#add_dis',function(){
var totalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
// var valoninput="this.value = this.value.replace(/[^0-9.]/g, '').replace(/(..*?)..*/g, '$1');"
var html ='<tr><td class="brif-wid"><input type="hidden" name="hdninvdis" value=""><input type="text" name="discountname" class="form-control disdesclsedit in-bor-clr"></td><td class="am-wid"><select name="discounttype" class="form-control in-bor-clr amounttypeclsedit"><option value="">-Select-</option><option value="percentage">Percentage</option><option value="amount">Fixed Amount</option></select></td></td><td class="am-wid"><input type="text" name="discountamount" class="form-control disamountclsedit in-bor-clr"></td><td class="in-btn-wid"><button id="add_dis" class="btn btn-clr add-btn" type="button" value="add"><i class="fa fa-add"></i></button> <button id="minus_dis" class="btn btn-clr add-btn" type="button" value="minus"><i class="fa fa-minus"></i></button></td><td class="dis-wid"><input type="hidden" name="discount_value" class="discountvaluecls"><p class="disvalcls"></p></td></tr>'
if (totalinvoice > '1'){
    $(this).closest('table').append(html)
}
else{
    $('#discounttableid').append(html)
}


})

$(document).on('click','#minus_dis',function(){
var lentable=$(this).closest('table').find('tbody tr').length
$('.final-cls1').attr('disabled',false)
if (lentable >1){
    var invoiceval=parseFloat(removeandlettercommaonly($('#id_totalvalue').val()))
    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    $(this).closest('tr').remove()
    $('.distblcls > tbody  > tr').each(function(index, tr){
        var discounttext=$(this).find('td:eq(4) > .disvalcls').text()
        var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
        var removecomma=replacetext.replace(/,/g , '')
        invoiceval -= parseFloat(removecomma)

    })
    $('.grossamountwithdiscls').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(invoiceval)))

    var other_value=0
        $('#otherstable > tbody  > tr').each(function(index, tr){
                var disper=$.trim($(this).find('.others_amount').val())
                if (disper == ''){
                    disper=0
                }
                console.log({'disper':disper})
                $(this).find('.other_dis_val').text('+ '+splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper))) 
                other_value+=parseFloat(disper) 
                $(this).closest('tr').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper)))
        })
        var finalothervalue=parseFloat(invoiceval)+other_value
        $('#id_grossamountwithother').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalothervalue)))


        var finaldisvalue=parseFloat(decimal_value(finalothervalue))
        var exclusivepercentage=0
        $('.exclusivetable > tbody > tr').each(function(index, tr){
            var exclusivepercls=$(this).find('.exclusivepercls').val()
            if (exclusivepercls != ''){
            var exclusivetaxamount=exclusivepercls
            console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
            // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
            }
            })
        var finalexctax=exclusivepercentage+finaldisvalue
        $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(todegitvalues(exclusivepercentage)))
        $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))
        
        var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
        $('.invoicetblcls tbody tr').each(function(){
            var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
            var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
            var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
            var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
            // var baseamount=totalall_tax*percentage/100
            var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
            var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

            var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))

            $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
            if(exchangetype == "1"){
                if (splitcurrencysymbol[0] == currencysymbol){
                    $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                        var disinvoiceper=finaldisvalue*percentage/100
                        $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                        $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                        $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    })
                }
                else{
                    var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                }
                if (exchangetypevalue == "N/A"){
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }
                else{

                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100*parseFloat(decimal_value(exchangetypevalue))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }
            }
            else{

                $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=finaldisvalue*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
            }

        })

    //
}

})



$(document).on('click','.btnsumcls',function(){
$('.maininvsumcls').show()
})

$(document).on('change','.percls',function(){
var dataid=$(this).attr('dataid')
var totalpercentage=0
var newarray=[]
$('.percls').each(function(){
    if ($(this).val() != ""){
        totalpercentage += parseFloat($(this).val())
    }
    else{
        var row_index = $(this).attr('dataid')
        newarray.push(row_index)
        console.log(row_index)
    }

})
if (totalpercentage > 100){
    swal.fire('Exceeding total amount')
    //$(this).val('')
}
else{
    var minusval=100-totalpercentage
    if (newarray.length ==1){
        $('.percls').each(function(){
            if (newarray[0] == $(this).attr('dataid')){
                $(this).val(minusval)
                var finaltotalamount=splitWithReplaceComma($('.totalalltaxcls').val())
                var amount=parseFloat(finaltotalamount)*parseFloat(minusval)/100
                $(this).closest('td').next('td').next('td').find('.amountcls').val(numberWithCommas(decimal_value(amount))).attr('readonly',true)
                var discountamount=parseFloat(splitWithReplaceComma($('.grossamountwithdiscls').val()))*parseFloat(minusval)/100
                var inv_num=$(this).closest('td').prev('td').prev('td').find('.invnumcls').val()
                var inv_data=$(this).closest('td').prev('td').find('.dateformat-cls').val()
                var finaldiscountamount=$('.grossamountwithdiscls').val()
                var currencysymbol=splitWithCurrency(finaldiscountamount)
                //var inctax=parseFloat(splitWithReplaceComma($('.totalinclusivetaxcls').val()))*parseFloat(val)/100
                var exctax=parseFloat(splitWithReplaceComma($('.totalexclusivetaxcls').val()))*parseFloat(minusval)/100
                var totalfinalvalue=discountamount+exctax
                var html='';
                html +='<div class="row invdetailcls"> <div class="col-4"><label class="sum-vew">Invoice No :</label><span class="sum-date">'+inv_num+'</span></div> <div class="col-4"><label class="sum-vew">Date :</label><span class="sum-date">'+inv_data+'</span></div> </div>'
                html += '<table><tbody><tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currencysymbol+' '+discountamount+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currencysymbol+' '+exctax+'</td></tr> <tr><th class="hed-inv">Gross Total Inclusive of all Taxes and Levies</th><td class="totalvaluecls">'+currencysymbol+' '+numberWithCommas(decimal_value(totalfinalvalue))+'</td></tr></tbody></table>'
                $(this).closest('table').next('div').find('.invoicecls'+newarray[0]+'').html(html)
            }
        })
    }
    var finaltotalamount=splitWithReplaceComma($('.totalalltaxcls').val())
    var val=$(this).val()
    var amount=parseFloat(finaltotalamount)*parseFloat(val)/100
    $(this).closest('td').next('td').next('td').find('.amountcls').val(numberWithCommas(decimal_value(amount))).attr('readonly',true)
    var discountamount=parseFloat(splitWithReplaceComma($('.grossamountwithdiscls').val()))*parseFloat(val)/100
    var inv_num=$(this).closest('td').prev('td').prev('td').find('.invnumcls').val()
    var inv_data=$(this).closest('td').prev('td').find('.dateformat-cls').val()
    var finaldiscountamount=$('.grossamountwithdiscls').val()
    var currencysymbol=splitWithCurrency(finaldiscountamount)
    //var inctax=parseFloat(splitWithReplaceComma($('.totalinclusivetaxcls').val()))*parseFloat(val)/100
    var exctax=parseFloat(splitWithReplaceComma($('.totalexclusivetaxcls').val()))*parseFloat(val)/100
    var totalfinalvalue=discountamount+exctax
    var html='';
    html +='<div class="row invdetailcls"> <div class="col-4"><label class="sum-vew">Invoice No:</label><span class="sum-date">'+inv_num+'</span></div> <div class="col-4"><label class="sum-vew">Date:</label><span class="sum-date">'+inv_data+'</span></div> </div>'
    html += '<table><tbody><tr><th class="hed-inv-gr">Gross Amount Payable After Discount</th><td class="hed-inv-gr-val">'+currencysymbol+' '+discountamount+'</td></tr> <tr><th class="hed-inv-gross">Exclusive Taxes and Levies</th><td class="hed-inv-gross-val">'+currencysymbol+' '+exctax+'</td></tr> <tr><th class="hed-inv">Gross Total Inclusive of all Taxes and Levies</th><td class="totalvaluecls">'+currencysymbol+' '+numberWithCommas(decimal_value(totalfinalvalue))+'</td></tr></tbody></table>'
    $(this).closest('table').next('div').find('.invoicecls'+dataid+'').html(html)
}


})

$(document).on('change','.percentagecls',function(){
var currencytype=$('.common_cls:checked').val()
var totalvalue=removeandlettercommaonly($('#id_totalvalue').val())
var currency=$('.currency-clr').text()
var splittotalvalue=currency.split("-")
var value=splittotalvalue[0]
var val=$(this).val()
$(this).next('span').remove()
if (currencytype == 'split_currency'){
    var exchangetype = $('.splitcommon_cls:checked').val()
    if (exchangetype == 'submissiondate'){
        var curattrid=$(this).attr('dataid')
        var hdncomcurid=$('#hdncomcurid').val()
        var count_total_percentage=0;
        $('.dynamiccls'+curattrid+'').each(function(i, obj) {
            if ($(this) != ''){
                var convert_int=parseInt($(this).val())
                if (!isNaN(convert_int)){
                    count_total_percentage += convert_int
                }
            }
        })
        if (count_total_percentage > 100){
            swal.fire('Exceeding the total amount')
            $(this).val('')
            $(this).parent().next('div').find('.amountcls').val('')
            $(this).parent('div').parent('div').next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val('')
        }
        else{
            if (hdncomcurid == curattrid){
                currencyval=$(this).parent('div').parent('div').parent('div').parent('div').parent('div').prev('div').find('.invoiceamount').val()
                var calculateval=currencyval*val/100
                $(this).parent().next('div').find('.amountcls').val(calculateval).attr('readonly',true)
                $(this).parent().parent().next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val(value+' '+numberWithCommas(decimal_value(calculateval)))
            }
            else{
                var curretcurid=$(this).parent('div').parent('div').parent('div').parent('div').parent('div').prev('div').find('.companycurrencycls > :selected').text()
                var splitcurid=curretcurid.split("-")
                currencyval=$(this).parent('div').parent('div').parent('div').parent('div').parent('div').prev('div').find('.exchangeamountcls').val()
                var calculateval=currencyval*val/100
                $(this).parent().next('div').find('.amountcls').attr('readonly',true).val(calculateval)
                $(this).parent().parent().next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val(splitcurid[0]+' '+numberWithCommas(decimal_value(calculateval)))
            }
        }
    }
    else{
        var curattrid=$(this).attr('dataid')
        var count_total_percentage=0;
        $('.dynamiccls'+curattrid+'').each(function(i, obj) {
            if ($(this) != ''){
                var convert_int=parseInt($(this).val())
                if (!isNaN(convert_int)){
                    count_total_percentage += convert_int
                }
            }
        })
        if (count_total_percentage > 100){
            swal.fire('Exceeding the total amount')
            $(this).val('')
            $(this).parent().next('div').find('.amountcls').val('')
            $(this).parent('div').parent('div').next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val('')
        }
        else{
            currencyval=$(this).parent('div').parent('div').parent('div').parent('div').parent('div').prev('div').find('.invoiceamount').val()
            var calculateval=currencyval*val/100
            $(this).parent().next('div').find('.amountcls').attr('readonly',true).val(numberWithCommas(calculateval))
            $(this).parent().parent().next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val(value+' '+numberWithCommas(calculateval))

            
        }
    }

}
else{
    var count_total_percentage=0;
    $('.percentagecls').each(function(i, obj) {
        if ($(this) != ''){
            var convert_int=parseInt($(this).val())
            if (!isNaN(convert_int)){
                count_total_percentage += convert_int
            }
        }
    })
    console.log(count_total_percentage)
    if (count_total_percentage > 100){
        swal.fire('Exceeding the total amount')
        $(this).val('')
        $(this).closest('div').next('div').find('.amountcls').val('')
        $(this).closest('div').parent('div').next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val('')
        tableclassname=$(this).closest('div').parent('div').next('div').next('div').next('table').attr('class')
        var splitclassname=tableclassname.split(' ')
        $('.'+splitclassname[1]+'> tbody  > tr').each(function(index, tr){        
            $(this).find('td:eq(3) > .taxvalcls').text('')
        })
        $('.'+splitclassname[1]).next('div').find('.grossamountwithbothcls').attr('readonly',true).val('')
    }
    else{
        var disminusval=$(this).parent().parent().parent().parent().prev('div').find('.grossamountwithdiscls').val()
        var splitdisminuval=disminusval.split(" ")
        var removecommaval=splitdisminuval[1].replace(/,/g , '')
        perval=removecommaval*val/100
        $(this).parent().next('div').find('.amountcls').val(numberWithCommas(decimal_value(perval))).attr('readonly',true)
        $(this).parent().parent().next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val(splitdisminuval[0]+' '+numberWithCommas(decimal_value(perval)))
        $(this).parent().parent().next('div').next('div').next('table').next('div').find('.grossamountwithbothcls').val(splitdisminuval[0]+' '+numberWithCommas(decimal_value(perval)))



        var invoiceval=$(this).parent('div').parent('div').next('div').find('.notaxdiscls > .grossamountnotaxdiscls').val().replace(/,/g , '')
        var splittotalvalue=invoiceval.split(" ")
        var convertval= parseInt(splittotalvalue[1])
        var tableclassname=$(this).parent('div').parent('div').next('div').next('div').next('table').attr('class')
        var splitclassname=tableclassname.split(' ')
        $('.'+splitclassname[1]+'> tbody  > tr').each(function(index, tr){        
            $(this).find('td:eq(3) > .taxvalcls').text('')
            var setvalue=convertval * parseInt($(this).find('td:eq(1) > .taxpercls').val()) / 100
            convertval += convertval * parseInt($(this).find('td:eq(1) > .taxpercls').val()) / 100
            if ($(this).find('td:eq(1) > .taxpercls').val() != ''){
                $(this).find('td:eq(3) > .taxvalcls').text('+'+splittotalvalue[0]+numberWithCommas(decimal_value(taxvalcls(setvalue))))
                
            }
            else{
                $(this).find('td:eq(3) > .taxvalcls').text('')
            }
        })
        $(this).closest('table').next('div').find('.grossamountwithbothcls').attr('readonly',true).val(splittotalvalue[0]+' '+numberWithCommas(decimal_value(convertval)))

       

    }
}
})

$(document).on('focus','.date-cls',function(){
var fromdate=$('#id_fromdate').val()
var todate=$('#id_todate').val()
var today = new Date();


var splitdate1=fromdate.split("-")
var fromyear=splitdate1[0]
// var frommonth=splitdate1[1]



// var splitdate2=todate.split("-")
// var toyear=splitdate2[0]
// var tomonth=splitdate2[1]
// console.log('date',new Date());


var hdn_dateformat = $('#companydateformat').val()
    if (hdn_dateformat == ''){
        $('.date-cls').datepicker({
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            dateFormat:'dd-M-yy',
            minDate: new Date(fromdate),
            maxDate: new Date(today),
            onClose: function(dateText, inst) {
                $(this).datepicker('widget').removeClass('hide-calendar');
            },
        })
    }
    else{
        $('.date-cls').datepicker({
            dateFormat: hdn_dateformat,
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            minDate: new Date(fromdate),
            maxDate: new Date(today),
            onClose: function(dateText, inst) {
                $(this).datepicker('widget').removeClass('hide-calendar');
            },
        })
    }

});
$(document).on('change','.duecls',function(){
// if (no_invoice !="1"){
//     $('.addinvoicecls').removeAttr("style")
// }
if (no_invoice == created_invoices_count){
    $('.addinvoicecls').css('display','none')
}
else{
    $('.addinvoicecls').removeAttr("style")
}


var val=$(this).find(':selected').val()
var type=$(this).find(':selected').attr('type')
var day=$(this).find(':selected').attr('day')
var percentage=$(this).find(':selected').attr('percentage')
if (val != ''){
    $(this).removeClass('add-error-cls')
    if (type == "1"){
        $('.paymentdiv').html('<div>Due in '+day+' Days</div>')
        //$(this).closest('tr').find('.payday').val('Immediate')
        //$(this).closest('tr').find('.payper').val(percentage)
    }
    else{
        $('.paymentdiv').html('<div>Due in '+day+' Days</div>')
        //$(this).closest('tr').find('.payday').val(day)
        //$(this).closest('tr').find('.payper').val(percentage)
    }
}
else{
    $('.paymentdiv').html('')
}
})


$(document).on('click','.payadd',function(){
//paymentlist

var html=''

html +='<tr><td><select name="" class="duecls form-control in-bor-clr"><option value="" selected>-Select-</option></select></td><td><input type="text" name="" class="form-control payday"></td><td><input type="text" name="" class="form-control payper"></td><td> <button type="button" class="payadd"><i class="fa fa-plus" aria-hidden="true"></i></button><button type="button" class="payminus"><i class="fa fa-minus" aria-hidden="true"></i></button></td></tr>'

$('#paytableid').append(html) 

var selectedoptionarray=[];
$('.duecls').each(function(){
    var currentvalue=$(this).find(':selected').val()
    if (currentvalue != undefined && currentvalue != ''){
        selectedoptionarray.push(currentvalue)
    }
})
var selectoption='<option value="" type="" percentage="">--Select--</option>'
$(paymentlist).each(function(i,v){   
    selectoption +='<option value='+v.id+' percentage='+v.percentage+' type="'+v.type+'" day="'+v.day+'">'
    if(v.type == '1'){
        selectoption +='Advance Payment'

    } 
    else{
        selectoption +='Regular Payment'

    }
    selectoption +='</option>'
})    
console.log('asd',selectedoptionarray)
$(this).closest('tr').next('tr').find('.duecls').html(selectoption)
 $(selectedoptionarray).each(function(i,v){ 
    $('#paytableid tbody tr:last').find('.duecls option[value='+v+']').remove()
  })

})

$(document).on('click','.payminus',function(){
var tablen=$('#paytableid tbody tr').length
if (tablen > 1){
    $(this).closest('tr').remove()
}
})


$(document).on('click','#draft_id1',function(e){
e.preventDefault();
var form = $('#invoiceform2')
var count=0
// $('.discountspan').remove()
$('#discounttableid tbody tr').each(function(index,val){
   
    var disname=$(this).closest('tr').find('.disdesclsedit').next('span')
    // var distype=$(this).closest('tr').find('.amounttypeclsedit :selected').val() || null
    // if (distype != 'Not Applicable'){
        if (disname.length > 0){
            count ++;
        }
    // }
})
$('.invoicetblcls tbody tr').each(function(index, tr){
    var spantxt=$(this).closest('tr').find('.invnumcls').next('span')
    if (spantxt.length > 0){
        count ++;
    }
})
if (count == 0){
    $("<input>").attr({
        name: "submit_type",
        id: "hiddenId",
        type: "hidden",
        value: 0
    }).appendTo("form");
    form.submit(); 
}
})

$(document).on('click','.final-cls1',function(e){
e.preventDefault();
$('.invspan').remove()
var form = $('#invoiceform2')
var total=$('#id_totalvalue').val()
var duedate=$('.duecls').find(":selected").val()
var tablen=$('.invoicetblcls tbody tr').length
var count=0
var companycurrencyid=$('#hdncomcurid').val()

$('.invnumcls,.bankdetailcls').not(':hidden').each(function(){
 if($.trim($(this).val()) == ''){
    count++
    $(this).addClass('con_error')
 }
})
if($('.invoicetblcls tbody tr').length == 0 ){
    swal.fire('Add Invoice Details')
    count++
}

$('.invoicetblcls tbody tr').each(function(index, tr){
    var index=$(this).closest('tr').find('.invnumcls').attr('index')
    var bankdetails=$(this).closest('tr').find('.bankdetailcls > :selected').val() || null
    var invoicenum=$(this).closest('tr').find('.invnumcls').val() || null
    var date=$(this).closest('tr').find('.dateformat-cls').val() || null
    var bankdetails=$(this).closest('tr').find('.bankdetailcls > :selected').val() || null
    var currencyid=$(this).closest('tr').find('.paymentcurrencycls').attr('dataid')
    var exchangerate=$(this).closest('tr').find('.exchangeratecls').val() || null
    var exchangetype=$(this).closest('tr').find('.exchangeratecls').attr('dataid')
    var spantxt=$(this).closest('tr').find('.invnumcls').next('span')
    if (spantxt.length > 0){
        count ++;
    }

    if (invoicenum == null){
        $(this).closest('tr').find('.invnumcls').after('<span class="invspan error">This field is required</span>')
    }

    if (date == null){
        $(this).closest('tr').find('.dateformat-cls').after('<span class="invspan error">This field is required</span>')
    }
    
    if (bankdetails == null){
        $(this).closest('tr').find('.bankdetailcls').after('<span class="invspan error">This field is required</span>')
    }
    if (exchangerate == null){
        $(this).closest('tr').find('.exchangeratecls').after('<span class="invspan error">This field is required</span>')
    }

    if (exchangetype == '1'){
        if (companycurrencyid == currencyid){
            if(invoicenum == null || date == null || bankdetails == null){
                console.log('a')
                // $('#id_totalvalue').addClass('error')
                count ++;
            }
        }
        else{
            if(invoicenum == null || date == null || bankdetails == null || exchangerate == null){
                console.log('b')
                count ++;
            }
        }
    }
    else{
        if(invoicenum == null || date == null || bankdetails == null){
            console.log('c',invoicenum,date,bankdetails)
            count ++;
        }
    }
})
if (total == ""){
    $('#id_totalvalue').addClass('error')
}
else{
    $('#id_totalvalue').removeClass('error')
}
if (duedate == ""){
    $('.duecls').addClass('error')
}
else{
    $('.duecls').removeClass('error')
}
$('.discountspan').remove()
$('#discounttableid tbody tr').each(function(index,val){
   
    var disname=$(this).closest('tr').find('.disdesclsedit').val() || null
    var distype=$(this).closest('tr').find('.amounttypeclsedit :selected').val() || null
    var disamount=$(this).closest('tr').find('.disamountclseditedit').val() || null
    // if (distype != 'Not Applicable'){
    //     if (disname == null){
    //         $(this).closest('tr').find('.disdesclsedit').after('<span class="error discountspan">This field is required</span>')
    //         count ++;
    //     }
    //     if (distype == null){
    //         $(this).closest('tr').find('.amounttypeclsedit').after('<span class="error discountspan">This field is required</span>')   
    //         count ++;
    //     }
    //     if (disamount == null){
    //         $(this).closest('tr').find('.disamountclseditedit').after('<span class="error discountspan">This field is required</span>')  
    //         count ++; 
    //     }
    // }
    // if (disname != null || disamount != null){
    //     if (disname == null){
    //         // $(this).find('td:eq(0) > .disdesclseditedit')
    //     }
    // }
})
var exc_count=0;
$('.exclusivecls').each(function(index,value){
    var val=$(value).find(':selected').val()
    if (val == ''){
        exc_count += 1
        $(this).addClass('con_error')
    }
    else{
        tax_amount=$(this).closest('tr').find('.exclusivepercls')
        if(tax_amount.val() == ''){
            tax_amount.addClass('warning')
            exc_count+=1
        }
        else{
            tax_amount.removeClass('warning')
        }
    }
})
$('.payment-cls').each(function(index,value){
    var val=$(value).find(':selected').val()
    if (val == ''){
        $(this).addClass('con_error')
    }
})
if($.trim($('.others_name').val()) != ''){
    if($('.others_amount').val() == ''){
        $('.others_amount').addClass('con_error')
    }
}

$('.tax_cls').each(function(){
    let length = $(this).find(':checked')
    if (!length){
        $(this).addClass('con_error')
    }
})
// if ($('input[name="tax_type"]:checked').length == 0) {
//     $('.radiobtn_class').addClass('con_error')
// }
// if (tablen),
// console.log(count,tablen,duedate,total)
if (count == 0 && tablen > 0 && duedate != "" && total != "" && exc_count == 0 && $('.con_error').length == 0){ 
    if (no_invoice != tablen){
        Swal.fire({
                title: 'You have Pending Invoice(s). Do you want to Proceed?',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes,I Confirm',
                cancelButtonText: 'No',
            }).then((result) => {
                if (result.isConfirmed) { 
                    $("<input>").attr({
                    name: "submit_type",
                    id: "hiddenId",
                    type: "hidden",
                    value: 1
                    }).appendTo("form");
                    form.submit(); 
                }
            });
    }
    else{
        $("<input>").attr({
            name: "submit_type",
            id: "hiddenId",
            type: "hidden",
            value: 1
        }).appendTo("form");
        form.submit(); 
    }
}
})

$(document).on('change','.con_error',function(){
$(this).removeClass('con_error') 
})

$(document).on('change','.cur_symbol',function(){

var val = $(this).val()

console.log({'val':val})

var currency=$('.currency-clr').text()
var splitcurrencysymbol=currency.split("-")

console.log('currency',currency)
console.log('splitcurrencysymbol',splitcurrencysymbol)
    
$('.cur_symbol').val(splitcurrencysymbol[0]+' '+(val))

})


function inv_func(){
    let  total_value=splitWithReplaceComma($('#id_totalvalue').val())
    var total_val=total_old_val
    if (total_val == 'No Max Limit'){
    }
    if(Number(total_value) > Number(total_val)){
        swal.fire('Total Value Inputted Exceeds Total Maximum Value for Contract '+contract_reference+'')
        $('#id_totalvalue').val('')
    }
    // var getval=$('#id_totalvalue').val()
    var val=removeandlettercommaonly(total_value)
    $('#id_totalvalue').val(numberWithCommas(decimal_value(val)))
    var convert_intval=parseInt(val)
    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    var checkvalue=0;
        $('.distblcls > tbody  > tr').each(function(index, tr){
            removeval=$(this).find('td:eq(4) > .disvalcls').text()
            if (removeval != ''){
                var replacetext = removeval.replace('-'+splitcurrencysymbol[0],'')
                var removecomma=replacetext.replace(/,/g , '')
                checkvalue += parseInt(removecomma)
            }
        })
        if (checkvalue >= parseFloat(val)){
            swal.fire('Total amount cannot be lesser than the discount')
            $('#id_totalvalue').val(global)
        }
        else{
            var discountvalue=0
            $('#id_grossamountwithdis').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(val)))
            $('.distblcls > tbody  > tr').each(function(index, tr){
                gettype=$(this).find('td:eq(1) > .amounttypeclsedit :selected').val()
                if (gettype == 'percentage'){
                    var disper=$(this).find('td:eq(2) > .disamountclsedit').val()
                    var minusdisval=val*disper/100
                    discountvalue+=parseFloat(minusdisval)
                    console.log(minusdisval)
                    $(this).find('td:eq(4) > .disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(minusdisval)))
                    $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(minusdisval)))
                }
                else if (gettype == 'amount') {
                    var disper=$(this).find('td:eq(2) > .disamountclsedit').val()
                    $(this).find('td:eq(4) > .disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper))) 
                    discountvalue+=parseFloat(disper) 
                    $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper)))
                }
            })
            var finaldisvalue=parseFloat(decimal_value(parseFloat(val)-discountvalue))
            $('#id_grossamountwithdis').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finaldisvalue)))

            var other_value=0
            $('#otherstable > tbody  > tr').each(function(index, tr){
                    var disper=$.trim($(this).find('.others_amount').val())
                    if (disper == ''){
                        disper=0
                    }
                    console.log({'disper':disper})
                    $(this).find('.other_dis_val').text('+ '+splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper))) 
                    other_value+=parseFloat(decimal_value(disper)) 
                    $(this).closest('tr').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(disper)))
            })
            var finalothervalue=finaldisvalue+other_value
            $('#id_grossamountwithother').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalothervalue)))
            console.log({'other_value':finalothervalue})

            var exclusivepercentage=0
            $('.exclusivetable > tbody > tr').each(function(index, tr){
                var exclusivepercls=$(this).find('.exclusivepercls').val()
                if (exclusivepercls != ''){
                var exclusivetaxamount=exclusivepercls
                console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
                // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))
    
                // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))
    
                exclusivepercentage+=parseFloat(removeandlettercommaonly(exclusivepercls))
                }
                })
            // $('.exclusivetable > tbody  > tr').each(function(index, tr){
            //     var exclusivepercls=gettype=$(this).find('td:eq(1) > .exclusivepercls').val()
            //     console.log('exclusivepercls',exclusivepercls)
            //     if (exclusivepercls != ''){
            //         var exclusivetaxamount=finaldisvalue*parseFloat(exclusivepercls)/100
            //         // console.log({'exclusivetaxamount':exclusivetaxamount,'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls})
            //         $(this).find('td:eq(3) > .taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercls)))

            //         $(this).find('td:eq(3) > .exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercls)))
            //         exclusivepercentage+=parseFloat(replaceWithComma(exclusivepercls))
            //     }
            // })

            var finalexctax=exclusivepercentage+finalothervalue
            console.log({'finalexctax':finalexctax,'exclusivepercentage':exclusivepercentage,'finaldisvalue':finaldisvalue})
            $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
            $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))
            $('.hd_con_cls').removeAttr('style')
        }
}


$(document).on('keyup','.exclusivepercls',function(){

    let val=$.trim($(this).val())

    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    var final_value=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
    var finaled_val = $('#id_grossamountwithother').val();
    var totalvalue=0
    if(val == ''){
        val=0
    }
    var get_percentage=parseInt(val)/((final_value/100))
    console.log({'parseInt(val)':parseInt(val),'final_value':final_value,'get_percentage':get_percentage})
    if (val != '' || val==0){
        if (final_value > parseInt(val)){
        var addval = val.replace(/,/g, '')
        
        $(this).closest('tr').find('.exclusive_percentage').val(get_percentage+ '%')
        $(this).closest('tr').find('.percentage_in_num').val(get_percentage)
        $(this).closest('tr').find('.exclusive_percentage').attr('data-id',get_percentage)
        $(this).closest('tr').find('.taxvalcls').text(splitcurrencysymbol[0] + ' ' +numberWithCommas(decimal_value(addval)))
        
        var count=0
        $('.taxvalcls').each(function(){
            if ($.trim($(this).text()) != ''){
            var vals=splitWithReplaceComma($(this).text())
            count += parseFloat(vals)
            }
        })
        $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(count)))
        totalvalue += count
        final_value+=count
        $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(final_value)))
        
       
        $(this).closest('tr').find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+(todegitvalues(addval)))

        var finaldisvalue=todegitvalues(splitWithReplaceComma($('#id_grossamountwithother').val()))
        finaldisvalue=parseFloat(decimal_value(finaldisvalue))
        var totalall_tax=parseFloat(decimal_value(final_value))
        var finalexctax=parseFloat(decimal_value(parseFloat(count)+finaldisvalue))
        $('.invoicetblcls tbody tr').each(function(){
            var percentage=parseFloat($(this).find('td').find('.percls').val())
            var currencysymbol=$(this).find('td').find('.paymentcurrencycls').val()
            var exchangetype=$(this).find('td').find('.percls').attr('exchangetype')
            var exchangetypevalue=$(this).find('td').find('.exchangeratecls').val() || 0
            // var baseamount=parseFloat(decimal_value(totalall_tax*percentage/100))
            var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
            var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))
            
            var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
            $(this).find('td').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
            if(exchangetype == "1"){
            if (splitcurrencysymbol[0] == currencysymbol){

                $(this).find('td').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                var index=$(this).find('td').find('.percls').attr('index')
                $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                    var disinvoiceper=finaldisvalue*percentage/100
                $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
            })
            }
            else{
            var addamount=parseFloat(baseamount)*parseFloat(decimal_value(exchangetypevalue))
            $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
            }
            if (exchangetypevalue == "N/A"){

                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=finaldisvalue*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(count))*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
            }
            else{

                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=(finaldisvalue*percentage/100)*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                count=decimal_value(count)
                var excinvoiceper=parseFloat(decimal_value(decimal_value(count)*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var baseamount=decimal_value(totalall_tax*percentage/100)
                var finalalltotalinvoice=disinvoiceper+excinvoiceper
                var addamount=parseFloat(baseamount)*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas((decimal_value(addamount))))
    
            }
            }
            else{

                $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                var disinvoiceper=finaldisvalue*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                var excinvoiceper=parseFloat(decimal_value(count))*percentage/100
                $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                var finalalltotalinvoice=disinvoiceper+excinvoiceper
                if(exchangetypevalue == 'N/A'){
                    exchangetypevalue=1
                }
                var addamount=parseFloat(baseamount)*parseFloat(decimal_value(exchangetypevalue))
                $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
            }
            })
        }
        else{
            swal.fire('Tax Amount Exceeded Invoice Amount')
            var get_tax=$(this).closest('tr').find('.taxvalcls')
            $(this).val('')
            $(this).closest('tr').find('.exclusive_percentage').val('')
            $(this).closest('tr').find('.taxvalcls').text(splitcurrencysymbol[0]+
                ' '+numberWithCommas(decimal_value(0)))
            var finaldisvalue=parseFloat(decimal_value(splitWithReplaceComma($('.grossamountwithdiscls').val())))
            var exclusivepercentage=0
                $('.exclusivetable > tbody  > tr').each(function(index, tr){
                    console.log('$this------------',$(this).find('.exclusivepercls'))
                    var exclusivepercls=$(this).find('.exclusivepercls').val()
                    if (exclusivepercls != ''){
                    var exclusivetaxamount=exclusivepercls
                    console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
                    exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
                    }
                })
                var finalexctax=exclusivepercentage+finaldisvalue
                $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
                $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))
                var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
                $('.invoicetblcls tbody tr').each(function(){
                    var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
                    var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
                    var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
                    var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
                    // var baseamount=totalall_tax*percentage/100
                    var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
                    var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

                    var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))
                    $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                    if(exchangetype == "1"){
                        if (splitcurrencysymbol[0] == currencysymbol){

                            $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                                var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                                $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                                    var disinvoiceper=finaldisvalue*percentage/100
                                     $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                                     var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                                     $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                                    $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                                })
                        }
                        else{
                            var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                            $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                        }
                        if (exchangetypevalue == "N/A"){

                            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            var disinvoiceper=finaldisvalue*percentage/100
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        }
                        else{

                            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            var disinvoiceper=finaldisvalue*percentage/100*parseFloat(decimal_value(exchangetypevalue))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
        
                        }
                        
                    }
                    else{

                        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            var disinvoiceper=finaldisvalue*percentage/100
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                })
       
        }
    }
    else{
        var get_tax=$(this).closest('tr').find('.taxvalcls')
        $(this).closest('tr').find('.taxvalcls').text('')
        var count=0
        $('.taxvalcls').not(get_tax).each(function(){
            var vals=splitWithReplaceComma($(this).text())
            count += parseFloat(vals)
        })
        $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(count)))
        final_value+=count
        $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(final_value)))
        $(this).closest('tr').find('.exclusivevalcls').val('')
        $(this).closest('tr').find('.taxvalcls').text('')
           
    }
})



$(document).on('change','.exclusivepercls',function(){
  const this_value = $(this).val()

  // Convert the string to a numeric value (integer or floating-point)
  var numericValue = parseFloat(this_value.replace(/,/g, ''));

  var formattedValue = todegitvalues(numericValue);
  // Display the result with commas
//   var formattedValue = numericValue.toLocaleString();
  if (numericValue == '' || isNaN(numericValue)){
    $(this).val('')
  }
  else{
    $(this).val(formattedValue)
  }
})

$(document).on('change','.others_name',function(){
    if($.trim($(this).val()) != ""){
        $(this).closest('tr').find('.others_amount').removeAttr('readonly')
    }
    else{
    var totalinvoice=removeandlettercommaonly($('#id_grossamountwithdis').val())
    global=totalinvoice

    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    var val = 0
    $(this).closest('tr').find('.others_amount').val('')
    
            if(val != ''){
            $(this).closest('tr').find('.other_dis_val').text('+ '+splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            $(this).closest('tr').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            }
            else{
                $(this).closest('tr').find('.other_dis_val').text('')      
            }
        var data=parseFloat(totalinvoice)
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            if (discounttext){
                var replacetext=discounttext.replace("+ "+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
                data+=parseFloat(removecomma)
        })
        var checkvalue=0;
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            if (discounttext){
                var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
            checkvalue += parseFloat(removecomma)
        })
            $(this).closest('table').next('div').find('.grossamountwithother').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(data)))
            var finaldisvalue=parseFloat(decimal_value(data))
            var exclusivepercentage=0
            $('.exclusivetable > tbody > tr').each(function(index, tr){
            var exclusivepercls=$(this).find('.exclusivepercls').val()
            if (exclusivepercls != ''){
            var exclusivetaxamount=exclusivepercls
            console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
            exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
            }
            })
            var finalexctax=exclusivepercentage+finaldisvalue
            // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
            $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))

            var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
            $('.invoicetblcls tbody tr').each(function(){
                var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
                var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
                var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
                var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
                // var baseamount=totalall_tax*percentage/100
                var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
                var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

                var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))

                $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                if(exchangetype == "1"){
                    if (splitcurrencysymbol[0] == currencysymbol){

                        $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                            var disinvoiceper=finaldisvalue*percentage/100
                            $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                            $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                            $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        })
                    }
                    else{
                        var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                    }
                    if (exchangetypevalue == "N/A"){
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=finaldisvalue*percentage/100
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                    else{

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=finaldisvalue*percentage/100*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                }
                else{

                    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }

            })
        $(this).closest('tr').find('.others_amount').attr('readonly','readonly')
    }
    
})

// global_thers=''
$(document).on('change','.others_amount',function(){
//  $(this).next('span').remove()
var conval=$(this).val()
var new_val=conval.replace(/[^0-9\.]+/g, "")
$(this).val(new_val)
conval = new_val
// if ($.isNumeric(new_val)){
    // var new_val=conval.replace(/[^0-9\.]+/g, "")
    // $(this).val(new_val)
    // var type=$(this).closest('td').prev('td').find('.amounttypeclsedit').val()
    var totalinvoice=removeandlettercommaonly($('#id_grossamountwithdis').val())
    global=totalinvoice

    var currency=$('.currency-clr').text()
    var splitcurrencysymbol=currency.split("-")
    var html='';
    if(($.trim(conval) == "")) {
        var val = 0
    }
    else{
        var val = parseFloat(conval)
    }
    //console.log('abc',val)
        // if (type == 'percentage'){
            // var discountval=parseFloat(totalinvoice)*val/100
            // if(val != ''){
            //     $(this).closest('td').next('td').next('td').find('.disvalcls').text('-'+splitcurrencysymbol[0]+numberWithCommas(decimal_value(discountval)))
            //     $(this).closest('td').next('td').next('td').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(discountval)))
            // }
            // else{
            //     $(this).closest('td').next('td').next('td').find('.disvalcls').text('')
            // }
        // }
        // else{

            if(val != ''){
            $(this).closest('tr').find('.other_dis_val').text('+ '+splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            $(this).closest('tr').find('.discountvaluecls').val(splitcurrencysymbol[0]+numberWithCommas(decimal_value(val)))
            }
            else{
                $(this).closest('tr').find('.other_dis_val').text('')      
            }
        // }
        var data=parseFloat(totalinvoice.replace(/[^\d.]/g, ''));
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            console.log({'discounttext':discounttext})
            if (discounttext){
                var replacetext=discounttext.replace("+ "+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else{
                var removecomma =0
            }
                data+=parseFloat(removecomma)
        })
        var checktotalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
        var checkvalue=0;
        $('.Others_amount_table > tbody  > tr').each(function(index, tr){
            var discounttext=$(this).find('.other_dis_val').text()
            if (discounttext){
                var replacetext=discounttext.replace("-"+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
            }
            else {
                var removecomma =0
            }
            checkvalue += parseFloat(removecomma)
        })
        // console.log("c",checkvalue)
        // console.log("t",checktotalinvoice)
        // if (checkvalue >= parseFloat(checktotalinvoice)){
        //     $(this).val('')
        //     $(this).closest('td').next('td').next('td').find('.disvalcls').text('')
        //     swal.fire('Discount is exceeding the total amount')
        // }
        // else{
            console.log({'data':data})
            $(this).closest('table').next('div').find('.grossamountwithother').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(data)))
            //$('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(data))

            // var exclusiveamount=0
            // $('.exclusivetable > tbody  > tr').each(function(index, tr){
            //         var percentage=$(this).find('td:eq(1) > .exclusivepercls').val()
            //         if (percentage != ''){
            //             var sumval=parseFloat(data)*parseFloat(percentage)/100
            //             exclusiveamount += sumval
            //             $(this).find('td:eq(3) > .taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(sumval))
            //         }
            // })
            // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(exclusiveamount))
            // var finaltotalvalue=parseFloat(data)+exclusiveamount
            // $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(finaltotalvalue))
                

            // $('.invoicetblcls tbody tr').each(function(){
            //     var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
            //     var totalall_tax=parseFloat(splitWithReplaceComma($('#id_totalalltax').val()))
            //     var sumval=totalall_tax*percentage/100
            //     $(this).find('td:eq(5)').find('.amountcls').val(numberWithCommas(sumval))
            // })
            var finaldisvalue=parseFloat(decimal_value(data))
            console.log({'finaldisvalue':finaldisvalue})
            var exclusivepercentage=0
            $('.exclusivetable > tbody > tr').each(function(index, tr){
            var exclusivepercls=$(this).find('.exclusivepercls').val()
            if (exclusivepercls != ''){
            var exclusivetaxamount=exclusivepercls
            console.log({'finaldisvalue':finaldisvalue,'exclusivepercls':exclusivepercls,'exclusiveperclsexclusivepercls':parseFloat(removeandlettercommaonly(exclusivepercls)),'exclusivetaxamount':exclusivepercls})
            // $(this).find('.taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            // $(this).find('.exclusivevalcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))

            exclusivepercentage+=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
            }
            })
            var finalexctax=exclusivepercentage+finaldisvalue
            // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivepercentage)))
            $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))

            var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
            $('.invoicetblcls tbody tr').each(function(){
                var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
                var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
                var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
                var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
                // var baseamount=parseFloat(decimal_value(totalall_tax*percentage/100))
                var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
                var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

                var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))

                $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                if(exchangetype == "1"){
                    if (splitcurrencysymbol[0] == currencysymbol){

                        $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                            var disinvoiceper=finaldisvalue*percentage/100
                            $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                            $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                            $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        })
                    }
                    else{
                        var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                    }
                    if (exchangetypevalue == "N/A"){

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=finaldisvalue*percentage/100
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                    else{

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=decimal_value(finaldisvalue*percentage/100)*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
                }
                else{

                    $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                    var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                    var disinvoiceper=finaldisvalue*percentage/100
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                    var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                    var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))+parseFloat(decimal_value(excinvoiceper))
                    $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                }

            })


            // }
// }
// else{
    // console.log(conval)
    // var new_val=conval.replace(/[^0-9\.]+/g, "")
    // $(this).val(new_val)
// }
})


$(document).on('click','.add-other',function(){
    var totalinvoice=removeandlettercommaonly($('#id_totalvalue').val())
                                            
    // var valoninput="this.value = this.value.replace(/[^0-9.]/g, '').replace(/(..*?)..*/g, '$1');"
    var html ='<tr><td class="brif-wid"><input type="hidden" name="hdninvother" value=""><input type="text" name="others_name" class="form-control others_name in-bor-clr" ></td><td class="am-wid"><input type="text" name="others_amount" class="form-control others_amount in-bor-clr" readonly></td><td class="in-btn-wid"><button  id="add_others" class="btn btn-clr add-other" type="button" value="add"><i class="fa fa-add"></i></button> <button id="del_others" class="btn btn-clr add-btn del_others" type="button" value="minus"><i class="fa fa-minus"></i></button></td><td class="dis-wid"><input type="hidden" name="other_value" class="discountvaluecls"><h5 class="other_dis_val"></h5></td></div></tr>'
    if (totalinvoice > '1'){
        $(this).closest('table').append(html)
    }
    else{
        $('#otherstable').append(html)
    }
    
    
    })


    $(document).on('click','.del_others',function(){
        var lentable=$(this).closest('table').find('tbody tr').length
        $('.final-cls1').attr('disabled',false)
        if (lentable >1){
            var invoiceval=parseFloat(removeandlettercommaonly($('#id_grossamountwithdis').val()))
            var currency=$('.currency-clr').text()
            var splitcurrencysymbol=currency.split("-")
            $(this).closest('tr').remove()
            $('#otherstable > tbody  > tr').each(function(index, tr){
                var discounttext=$(this).find('.other_dis_val').text()
                var replacetext=discounttext.replace("+ "+splitcurrencysymbol[0],"")
                var removecomma=replacetext.replace(/,/g , '')
                if($.trim(removecomma) == ''){
                    removecomma=0
                }
                console.log({'removecomma':removecomma})
                invoiceval += parseFloat(removecomma)
            })
            $('#id_grossamountwithother').attr('readonly',true).val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(invoiceval)))
        
                var finaldisvalue=parseFloat(decimal_value(invoiceval))
                var exclusivepercentage=0
                $('.exclusivetable > tbody > tr').each(function(index, tr){
                var exclusivepercls=$(this).find('.exclusivepercls').val()
                if (exclusivepercls != ''){ 
                var exclusivetaxamount=parseFloat(decimal_value(removeandlettercommaonly(exclusivepercls)))
                // $(this).find('td:eq(3) > .taxvalcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(exclusivetaxamount)))
                exclusivepercentage+=exclusivetaxamount
                }
                })
                var finalexctax=exclusivepercentage+finaldisvalue
                // $('#id_totalexclusivetax').val('+'+splitcurrencysymbol[0]+' '+numberWithCommas(exclusivepercentage.toFixed(2)))
                $('#id_totalalltax').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalexctax)))
                
                var totalall_tax=parseFloat(decimal_value(splitWithReplaceComma($('#id_totalalltax').val())))
                $('.invoicetblcls tbody tr').each(function(){
                    var percentage=parseFloat($(this).find('td:eq(3)').find('.percls').val())
                    var currencysymbol=$(this).find('td:eq(5)').find('.paymentcurrencycls').val()
                    var exchangetype=$(this).find('td:eq(3)').find('.percls').attr('exchangetype')
                    var exchangetypevalue=$(this).find('td:eq(6)').find('.exchangeratecls').val() || 0
                    // var baseamount=totalall_tax*percentage/100

                    var grossamountwithother=parseFloat(splitWithReplaceComma($('#id_grossamountwithother').val()))
                    var totalexclusivetax=parseFloat(splitWithReplaceComma($('#id_totalexclusivetax').val()))

                    var baseamount=parseFloat(decimal_value(grossamountwithother*percentage/100))+parseFloat(decimal_value(totalexclusivetax*percentage/100))

                    $(this).find('td:eq(4)').find('.baseamountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                    if(exchangetype == "1"){
                        if (splitcurrencysymbol[0] == currencysymbol){

                            $(this).find('td:eq(7)').find('.amountcls').val(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(baseamount)))
                            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            $('.invoicesummarycls'+index+'').find('table tbody tr').each(function(){
                                var disinvoiceper=finaldisvalue*percentage/100
                                $(this).find('td:eq(0)').find('.finaldiscountcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(disinvoiceper)))
                                var excinvoiceper=parseFloat(decimal_value(finalexctax*percentage/100))
                                $(this).find('td:eq(0)').find('.finaltaxcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(excinvoiceper)))
                                var finalalltotalinvoice=parseFloat(decimal_value(disinvoiceper))*parseFloat(decimal_value(excinvoiceper))
                                $(this).find('td:eq(0)').find('.totalsumcls').text(splitcurrencysymbol[0]+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                            })
                        }
                        else{
                            var addamount=baseamount*parseFloat(decimal_value(exchangetypevalue))
                            $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+numberWithCommas(decimal_value(addamount)))
                        }
                        if (exchangetypevalue == "N/A"){

                            var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            var disinvoiceper=finaldisvalue*percentage/100
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=decimal_value(disinvoiceper)+decimal_value(excinvoiceper)
                            $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        }
                        else{

                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                            var disinvoiceper=finaldisvalue*percentage/100*parseFloat(decimal_value(exchangetypevalue))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                            var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))*parseFloat(decimal_value(exchangetypevalue))
                            $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                            var finalalltotalinvoice=decimal_value(disinvoiceper)+decimal_value(excinvoiceper)
                            $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                        }
                    }
                    else{
                        $(this).find('td:eq(7)').find('.amountcls').val(currencysymbol+' '+baseamount)
                        var index=$(this).find('td:eq(3)').find('.percls').attr('index')
                        var disinvoiceper=finaldisvalue*percentage/100
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaldiscountcls').text(currencysymbol+' '+numberWithCommas(decimal_value(disinvoiceper)))
                        var excinvoiceper=parseFloat(decimal_value(exclusivepercentage*percentage/100))
                        $('.invoicesummarycls'+index+'').find('table tbody tr .finaltaxcls').text(currencysymbol+' '+numberWithCommas(decimal_value(excinvoiceper)))
                        var finalalltotalinvoice=decimal_value(disinvoiceper)+decimal_value(excinvoiceper)
                        $('.invoicesummarycls'+index+'').find('table tbody tr .totalsumcls').text(currencysymbol+' '+numberWithCommas(decimal_value(finalalltotalinvoice)))
                    }
        
                })
        
            //
        }
        
        })


$(document).on('change','.tax_cls',function(){
    $(this).closest('thead').find('.tax_type').val($(this).val())
    $('.radiobtn_class').removeClass('con_error')

})

$(document).on('change', '.cls1, .cls2', function() {
    var $this = $(this);
    
    if ($this.hasClass('cls1')) {
        $('.cls2').prop({'disabled': false, 'checked': false});
    } else if ($this.hasClass('cls2')) {
        $('.cls1').prop({'disabled': false, 'checked': false});
    }
});

$(document).on('click','.exclusivepercls,.delete-row',function(){
    $(this).removeClass('warning')
    $('.final-cls1').attr('disabled',false)
})
if(invoice_tax_types == 2) {
    $('.cls2').prop({'disabled': false, 'checked': true});
    $('.cls1').prop({'disabled': true, 'checked': false});
}
$(document).on('blur','.exclusivepercls', function(){
    let tax_length = $(this).closest('tr').index();
    let tax_type 
        if(tax_length >= 1) { 
            tax_type = 2
            $('.cls2').prop({'disabled': false, 'checked': true});
            $('.cls1').prop({'disabled': true, 'checked': false});
            // $('.cls2').prop('disabled', false); 
            // $('.cls2').prop('checked',true); 
            // $('.cls1').prop('disabled',true);
            // $('.cls1').prop('checked',false); 
         } else {
            tax_type = 1
            $('.cls2').prop('disabled',false);
            $('.cls1').prop('disabled', false);      
        }
        $('.tax_type').val(tax_type)
   });

   $(document).on('click', '.delete-row', function() {
    if (exclusive_tax_value === 1) {
         

         let tax_length = $('.exclusivepercls').closest('tr').index();

         if (tax_length <= 1) {
            $('.cls2').prop({'disabled': false, 'checked': true});
            $('.cls1').prop({'disabled': false, 'checked': false});
            // $('.cls2').prop('disabled', false);
            // $('.cls2').prop('checked', true);
            // $('.cls1').prop('disabled', false);
            // $('.cls1').prop('checked', false);
        }
    }
});
$(document).ready(function(){
    var inclusive_tax_pecentage=0
    var inclusivetaxValues2 = $('.includetaxes').text().match(/\d+/g);
    if(inclusivetaxValues2){
        for(let i=0 ; i<inclusivetaxValues2.length ;i++){
            
            inclusive_tax_pecentage +=parseFloat(inclusivetaxValues2[i])
        }
    }
    else{
        inclusive_tax_pecentage=0
    }

        $('#incpercentage').val(inclusive_tax_pecentage);
       
    $(document).on('change','#id_totalvalue',function(){
        $('#grossamout').val(parseFloat(splitWithReplaceComma($('#id_grossamountwithdis').val())))
    })
    })
    
 




