$(document).on('click','.checkfile',function(){
    var val=$(this).val();
    if ($(this).is(':checked')){
        var html ='<table class="che-table"><tbody><tr><td><input type="file" accept="image/png, image/jpeg, application/pdf" name="file'+val+'" class="form-control filecls inp-voice3 filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td> <td class="in-btn-wid che-smline"><button id="add_file" class="btn btn-clr add-btn mr-1" type="button" dataid="'+val+'" value="add"><i class="fa fa-add"></i></button> <button id="remove_file" class="btn btn-clr add-btn" type="button" dataid="'+val+'" value="minus"><i class="fa fa-minus"></i></button></td> </tr></tbody></table>'
        $(this).closest('tr').find('.addfilecls').html(html)
    }
    else{
        $(this).closest('tr').find('.addfilecls').html('')
    }
})

$(document).on('click','#add_file',function(){
    var table = $(this).closest('table');
    table.find('.file-error-message').text(''); // Clear existing error messages
    var html = table.find('tr:first').clone(); // Clone the first row
    table.append(html); // Append the cloned row
    table.find('tr:last td:eq(0) .filecls').val(null); // Clear the file input in the last row
})
$(document).on('change', '.filecls', function() {
    var fileSize = this.files[0].size; // Size in bytes
    var maxSize = 25 * 1024 * 1024; // 25MB in bytes
    var errorMessageElement = $(this).closest('tr').find('.file-error-message');
    
    if (fileSize > maxSize) {
        errorMessageElement.text('*File size exceeds 25MB limit. Please choose a smaller file.');
        errorMessageElement.css('color', 'red');
        $(this).val(''); // Clear the file input
    } else {
        errorMessageElement.text('');
    }
});


$(document).on('click','#remove_file',function(){
    var table_len=$(this).closest('table').find('tr').length;
    if (table_len >1){
        $(this).closest('tr').remove()
    }
})


$(document).on('change','#id_totalvalue',function(){
    var total_val = total_value;
    console.log('total_val',total_val)
    if (total_val == 'No Max Limit'){
    }
    if(Number($(this).val()) > Number(total_val)){
        swal.fire('Total Value Inputted Exceeds Total Maximum Value for Contract',contract_reference)
        $(this).val('')
    }
    var getval=$(this).val();
    var val=removecommaonly(getval)
    $(this).val(numberWithCommas(decimal_value(val)))
})

function removecommaonly(x) {
    return x.replace(/[^a-zA-Z0-9.]/g, '');
}
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function decimal_value(val){
    if (val != ''){
        var con_val=val.toString();
        var remove_commas= con_val.replace(/,/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)){
            return remove_commas
        }
        else{
            return parseFloat(remove_commas).toFixed(2);
        }
    }
    else{
        return val
    }  
}

$(document).on('click','.remove-file',function(){
    $(this).closest('div').remove();
})

$(document).on('change','.cur_symbol',function(){
    var val = $(this).val();
    var currency=$('.currency-clr').text();
    var splitcurrencysymbol=currency.split("-");
    $('.cur_symbol').val(splitcurrencysymbol[0]+' '+(val));
  
})

$(document).on('click','.submit-cls',function(e){
    e.preventDefault();
    let get_value=$(this).val();
    $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: get_value}).appendTo("form");
    if (get_value != '0'){
        $("input:text").each(function(){
            var val=$(this).val()
            if (val == ''){
                $(this).addClass('con_error')
            }
        });
        let wcc_file=$('.wccfilecls').length;
        console.log('wcc_file',wcc_file)
        if (wcc_file == 0){
            $(".wcc_file_cls").each(function(){
                var val=$(this).val()
                if (val == ''){
                    $(this).addClass('con_error')
                }
            }); 
        }
        let supportingfile=$('.supportingfile').length;
        if (supportingfile == 0){
            $(".filecls").each(function(){
                var val=$(this).val()
                if (val == ''){
                    $(this).addClass('con_error')
                }
            })
        }

        let class_exist=$('.con_error').length
        if (class_exist == 0){
            $('#wccform2')[0].submit();
        }
    }
    else{
        $('#wccform2')[0].submit();
    }
    
})

$(document).on('change','.wcc_file_cls',function(){
    $(this).closest('div').next('div').remove();
})


$(document).on('keyup','.wcc_num_cls',function(){
    var val=$(this).val();
    var pk=$('#hdnid').val() || '';
    $(this).next('.span_cls').remove();
    var that=$(this);
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: '/wcc/checkwccnumber',
        data: { 'wcc_id': pk,'wcc_number':val,'csrfmiddlewaretoken':csrftoken},
        success: function (data) {
            console.log(data)
            if (data.status == false){
                that.addClass('con_error')
                $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                $(".submit-cls").attr("disabled", true);
            }
            else{
                that.removeClass('con_error')
                $(".submit-cls").attr("disabled", false);
    
            }
        }
    })
})

// $(document).on('click','#add_file',function(){
//     var html=$(this).closest('tr').clone()
//     $(this).closest('table').append(html)
    
//     $(this).closest('table').find('tr:last td:eq(0) .filecls').val(null)
// })


$(document).on('change','.con_error',function(){
    $(this).removeClass('con_error')
})



var hdn_dateformat = $('#companydateformat').val();
var contract_date = $('#fromdate').val();
console.log('contract_date',contract_date);
var split_date = contract_date.split("-");
console.log(split_date);
// Parse the contract date using a specific format
console.log("jaiiii");
var selectedDate = moment(contract_date, "MMMM D, YYYY").toDate();
if (hdn_dateformat == ''){
    $(document).on('focus', ".wccdateformat-cls", function(){
        console.log('s',contract_date);
        $(this).datepicker({
            dateFormat: 'dd-M-yy',
            minDate: selectedDate, // Set minDate to the contract date
            maxDate: new Date(), // Set maxDate to today's date
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:+0',
        });
    });
} else {
    $(document).on('focus', ".wccdateformat-cls", function(){
        console.log('syghbh',selectedDate);
        $(this).datepicker({
            dateFormat: 'dd-M-yy',
            showButtonPanel: true,
            changeMonth: true,
            changeYear: true,
            minDate: selectedDate, // Set minDate to the selected date
            maxDate: new Date(),
            yearRange: '1900:+0',  // Set maxDate to today
            // Add other options if needed
        });
    });
}