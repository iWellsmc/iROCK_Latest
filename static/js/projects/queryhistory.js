$('.querytype-cls').change(function(){
    var val=$(this).find(':selected').val();
    if (val == '3'){
         $('.file-cls').removeAttr('style');
    }
    else if (val == '1'){
        $('.file-cls').removeAttr('style');
        $('.replace_filename').removeAttr('style');

        var contractId = $('#contract_id').val();
    var ammendmentId = $('#amendment_id').val();
    var contracttype = $('#contract_types').val();
    ids=''
    if(contracttype == 'Original' ){
        ids= contractId
    }else{
        ids=ammendmentId
    }

        $.ajax({
        url:"/projects/getcontractrelationfile",
        method: "GET",
        data: {
            id: ids,
            contract_type: contracttype,
            file_type: "1",
        },  
        success: function(data) {

        html=''
        $(data.data).each(function(key,val){
                html += '<option  value='+val.id+'>'+val.original_file_name+"</option>";
        })
        // alert(html)
        $('#replace_filename').html(html);
        },
        error: function(xhr, status, error) {
                // Handle errors
         console.error(status, error);
        } 
    });
    }
    else{
        $('.file-cls').css('display','none')
        $('.replace_filename').css('display','none')
    }
    $('.file-cls').val('');
    $('.replace_filename').val('');
})

