var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()
$('.ven-cls').change(function(){
    let int_value=$(this).find(':selected').val()
    if (int_value == ''){
        $('.head_cls').css('display','none')
        $('.search-box').css('display','none')
    }
    else{
    let val=$(this).find(':selected').attr('data_id');
    let vendor_id=$(this).find(':selected').val();
    let get_name=$(this).find(':selected').text()
    $('.search-field').css('display','block')
    if (val != ''){
        $('.head_cls').show();
        $('#vin_id').text(val);
        $('#ven_id').text(get_name);
        $('#vendor_ids').val(vendor_id);
        $('#vendor_name_for_user_log').val(get_name);
        $.ajax({
            type: "POST",
            url: '/cost_code/getvendorcostcode',
            data: { 'vendor_id': vendor_id,'csrfmiddlewaretoken':csrftoken},
            success: function (data) {
                $('.cost_check_cls').attr('checked',false);
                console.log('sa',data)
                $(data.data).each(function(key,val){
                    let costcode_main_id=val.costcode_main_id.toString()
                    let order=  val.order
                    let final_val = costcode_main_id+'-'+order
                    $('#cost_table_id > tbody > tr').each(function(index,tr){
                        let td_data = $(tr).find('.cost_check_cls').val();
                        if (final_val == td_data ){
                            $(tr).find('.cost_check_cls').attr('checked',true)
                        }
                    })
                })
            }
        })
    }
    else{
        $('.head_cls').hide();
        $('#vin_id').text('');
        $('#ven_id').text('');
    }
}
})

$('#search-box').keyup(function () {
    var searchText = $('#search-box').val();
    setTimeout(function() {
        showResults(searchText);
    }, 1500);
});

showResults = function (searchText) {
    
    $('tbody tr').hide();

    $('tbody tr:contains(' + searchText + ')').show();

    $('tbody tr.vin-no, tbody tr.ven-name').show();
};
jQuery.expr[':'].Contains = jQuery.expr.createPseudo(function (arg) {
    return function (elem) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});


$('.final-cls').click(function(e){
    e.preventDefault()
    let vendor=$('.ven-cls').find(':selected').val()
    console.log('vendor',vendor)
    var count = $("[type='checkbox']:checked").length;
    if (count > 0  && vendor != ''){
        $('#vedorcostcodeid')[0].submit();
    }
    if(vendor == ''){
        $('.ven-cls').css("border", "1px solid red");
    }
    else{
        $('.ven-cls').css("border", "");
    }
})

$(document).on('change','.ven-cls',function(){
    let new_val=$(this).find(':selected').val()
    if(new_val != ''){
        $(this).css("border", "");
    }
})
$(document).ready(function() {
    $('#vendor_id').select2({
       placeholder: "Select Vendor",
    });
})
var checkedValues=[]
$(document).on('change','#vendor_id',function(){
    var vendor_id=$(this).val()

    $.ajax({
        type: "POST",
        url: '/projects/getcontracts_byvendor',
        data: { 'vendor_id': vendor_id,'csrfmiddlewaretoken':csrftoken},
        success: function (data) {
            var failed_comments =""
            var contracts_dropdown=''
            contracts_dropdown += '<option value="">Select Contract</option>';

            data.contracts.map(function(contract) {
                contracts_dropdown += '<option value='+contract.id+'>'+contract.contract_name+'-'+contract.field_type+'-'+contract.development_type+'-'+contract.disciplinename+'('+contract.reference_number+')</option>';
                failed_comments = `${contract.field_type }(${contract.development_type }) and ${contract.disciplinename} `
            })
            $('#error_comment').val(failed_comments)
            $('#contract').html(contracts_dropdown)
            if (data.contracts.length === 0) {
                if ($.fn.DataTable.isDataTable('#cost_table_id')) {
                    $('#cost_table_id').DataTable().destroy();
                }
                $('#cost_table_id').empty();
            }
      
        }
    })
})
$(document).on('change','#contract',function(){
    var vendor_id=$('#vendor_id').val()
    var contract_id=$(this).val()
    var emptycomment=$('#error_comment').val()
    $('#contract_id').val(contract_id)
    if ($.fn.DataTable.isDataTable('#cost_table_id')) {
        
        $('#cost_table_id').DataTable().destroy();
    }
    
    $('#cost_table_id').DataTable({
        serverSide: true,
        "ordering": false,
        ajax: {
            url: "/cost_code/getvendor_costcode",                    
            type: 'GET',
            "data": function (d) {
                d.vendor_id = vendor_id;
                d.contract_id=contract_id;
            }
        },
        columns: [
            {
                "data": null,
                "render": function (data, type, row) {
                    var isChecked = row.vendor_costcode_exists ? "checked" : "";
                    return "<input type='checkbox' name='maincode' value='" + row.costcode_main_id + "-" + row.order + "' class='cost_check_cls costcode_checkbox' " + isChecked + ">";
                },
                "orderable": false,
            },
            { data: 'costcode' },
            { data: 'codecode_component' },
    
    
        ],
        language: {
          emptyTable: "No Results Found"
        },
        drawCallback: function() {
            console.log(checkedValues)
            $('.costcode_checkbox').each(function() {
                var checkboxValue = $(this).val();
                if (checkedValues.includes(checkboxValue)) {
                    $(this).prop('checked', true);
                }
            });
        },
        "initComplete": function(settings, json) {
            $('.dataTables_filter input').attr('placeholder', 'Search Code Category Path');
        }
      });
})

$(document).on('change','#vendor_contracts',function(){
    var queryParams = $.param({contract: $(this).val()});
    if($(this).val() != ""){
        window.location.href = '/cost_code/vendorcostcodeview/'+vendor_id+'?' + queryParams;
    }else{
        window.location.href = '/cost_code/vendorcostcodeview/'+vendor_id;
    }

    

})
$(document).on('change','.costcode_checkbox',function(){
   $('.costcode_checkbox:checked').map(function() {
        checkedValues.push(this.value)
    })
    console.log(checkedValues)
    $('#selected_costcode').val(checkedValues)
})


