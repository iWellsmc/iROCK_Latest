$(document).ready(function() {
    
    var optiondict={}
    var list=[]
    $("#id_tax option").each(function(){
        var thisOptionValue=$(this).val();
        var thistext=$(this).text()
        optiondict={"id":thisOptionValue,"taxname":thistext}
        list.push(optiondict)
    });

    var companyoptiondict={}
    var companycurlist=[]
    $("#id_companycurrenices option").each(function(){
        var thisOptionValue=$(this).val();
        var thistext=$(this).text()
        companyoptiondict={"id":thisOptionValue,"symbol":thistext}

        companycurlist.push(companyoptiondict)
    });

    //add summer note for bank details

    $('.bank-cls, #inputaddress').summernote({
        toolbar: false,
          height: 100,
          disableFormatting: true,
      });

    // $('.bank-cls, #inputaddress').on('summernote.keydown', function(we, e) {
    //     // Check if the pressed key is a special character
    //     var isSpecialCharacter = e.key.length === 1 && !e.key.match(/[a-zA-Z0-9\s]/);
    //     if (isSpecialCharacter) {
    //         // Prevent the default action (input of the special character)
    //         e.preventDefault();
    //     }
    // });

    //get state when onchange country
    $(document).on('change', '#Operation_country_id', function() {
        var country_id=$(this).val();
        var html=''
        $.ajax({
            type:"GET",
            url:'/projects/getstate',
            data:{'countryid':country_id},
            success: function(data){
                html +='<option  value="" selected="selected">---Select State---</option>'
                $.each(data.data,function(key,val){
                    html +='<option value='+val.id+'>'+val.name+'</option>'
                })
                $('#Operation_state_id').html(html)
            }
        })
    });
    
    //add bank details
    var bankrow=1;
    $(document).on('click','#add_bank_details',function(){
        var val =$(this).closest('td').prev('td').find('.note-editor').find('.note-editable').find('p').text().length
        var country=$(this).closest('tr').find('.currency_bank_cls').find(':selected').val()
        var bank_name=$(this).closest('tr').find('.banknamecls').val()
        var account_no=$(this).closest('tr').find('.accnocls').val()
        var new_row1='<tr class="same-line-err"> <td><select name="currency_bank" class="form-control currency_bank_cls" id=""></select></td><td><input type="text" name="bankname" oninput="validateInput(this)" class="form-control banknamecls" id="" placeholder="Bank Name"></td> <td><input type="text" name="accno" oninput="validateInput(this)" class="form-control accnocls" id="" placeholder="Account No"></td> <td class="width-td-bank" ><input type="hidden" name="bankhdid" value="" > <textarea rows="4" cols="40" name="bankdetails"  id="bankid'+bankrow+'" class="form-control bank-cls" placeholder="Add Bank Details"></textarea> </td> <td class="btn-top-bank btn-flex"><button id="add_bank_details" class="btn btn-clr add-btn" row="'+bankrow+'" type="button" value="Add"> <i class="fa fa-plus"></i> </button> <button id="delete_bank_details" class="btn btn-clr" delete-"btn" type="button" row="'+bankrow+'" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>'

        $("#bank_information").append(new_row1);
        var selectoption='<option value="" selected>--Select--</option>'

        $.each(companycurlist,function(key,value){
            selectoption+='<option value='+value.id+'>'+value.symbol+'</option>'
        })
        $('#bank_information').find('tr:last').find('.currency_bank_cls').html(selectoption)
        $('#bank_information').find('tr:last').find('.bank-cls').summernote({toolbar: false,height: 110 })
        bankrow++;
        return false;
    })
    
    //check tax number already exists
    $(document).on('keyup','.taxnumber-cls',function(){
        $(this).val(($(this).val().replace(/[^A-Za-z0-9]/g,'')))
        $(this).next('span').remove()
        var val=$(this).val()||null
        var duplicatecount=0
        if (val != null){
            $('.taxnumber-cls').each(function(){
                if ($(this).val().toLowerCase() == val.toLowerCase()){
                    duplicatecount ++;
                }
            })
            if (duplicatecount > 1){
                $(this).closest('textarea').after('<span class="waring-err invoicenumspn">Tax number already exists</span>')
                $(this).addClass('con_error') 
            }
        else{
            $(this).removeClass('con_error')
         
            }
        }
    })

    //delete bank details
    $(document).on("click", "#delete_bank_details", function () {
        if ($('#bank_information tbody tr').length > 1){
            $(this).closest('tr').remove()
           
        }
    })
    
    $(document).on('keyup','.note-editable',function(){
       $(this).closest('td').find('.note-editor').removeClass('con_error')
    })
    
    //delete vendor tax details
    $(document).on("click", "#delete", function () {
        emptytaxnamedata = true
        emptytaxnumdata = true
            if ($('#tax tbody tr').length > 1){
                if (taxname == true && taxnum == true && emptytaxnamedata == true && emptytaxnumdata == true){
                    $(this).closest('tr').remove()
                }
            }
        
    })
    
    //check tax number already exists
    var taxnum=true;
    $(document).on('keyup','.taxnumber-cls',function(){
        var val=$(this).val();
        var spanid=$(this).closest('tr').index()
        $('#taxnum-'+spanid+'').remove()
        var z=0;
        if (val.length <= 50){
            taxnum=true
            $('#taxnum'+spanid+'').remove()
        }
        else {
            taxnum = false;
            $('#taxnum'+spanid+'').remove()
            $(this).closest('td').find('input[type="text"]').after('<span class="waring-err" id=taxnum'+spanid+'>Maximum 50 Characters only</span>')
        }
    })
    
    //check tax name already exists
    var taxname=true;
    $(document).on('keyup','.taxname-cls',function(){
        var val=$(this).val();
        var z=0;
        $('input').each(function(){
            if (val !='' && y !=''){
                var y=$(this).val();
                if(val==y){
                    z=z+1;
                }
            }
        });
        if(z>1){
            var spanid=$(this).closest('tr').index()
            $('#taxnm-'+spanid+'').remove()
            $(this).addClass("error")
            taxname=false
            $(this).closest('td').find('input[type="text"]').after('<span class="waring-err" id="taxnm-'+spanid+'" >Tax Name Already exists</span>')
        }
        else{
            var spanid=$(this).closest('tr').index()
            $(this).removeClass("error")
            taxname = true;
            $('#taxnm-'+spanid+'').remove()
        }

    })
     //submit vendor
    $(document).on("click", ".submit-cls", function (e){
        e.preventDefault()
        var count=0
        $('select').each(function(){
            var val=$(this).find(':selected').val()
            if (val == ''){
                count ++;
                $(this).addClass('con_error')
                console.log($(this))
            }
        })
    
        $(".taxname-cls").each(function(){
           var val=$(this).val()
           if (val == ''){
               count ++;
               $(this).addClass('con_error')
               console.log($(this))
           }
        });
    
        $(".address-cls").each(function(){
           var val=$(this).val()
           if (val == ''){
               count ++;
               $(this).addClass('con_error')
               console.log($(this))
           }else if(val === "<br>"){
                count ++;
                $(this).addClass('con_error')
           }
            console.log({'error':$('.con_error').length})
            if ($('.con_error').length > 0) {
            return false
        }
        });
        $(".taxnumber-cls").each(function(){
            var val=$(this).val()
            if (val == ''){
                count ++;
                $(this).addClass('con_error')
                console.log($(this))
            }
             console.log({'error':$('.con_error').length})
             if ($('.con_error').length > 0) {
             return false
         }
         });
    
        $(".banknamecls,.accnocls,.vendor-inp-cls").each(function(){
            var val=$(this).val()
            if (val == ''){
                count ++;
                $(this).addClass('con_error')
                console.log($(this))
            }
        });
    
        if ($('.con_error').length > 0) {
                return false
        }
    
        if (count == 0){
            $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 1}).appendTo("form");
            $("#vendorRegistration").submit();
        }
    })

    $(document).on('blur','.accnocls',function(){ 
        var val=$(this).val()||null
        var duplicatecount=0
        if (val != null){
            $('.accnocls').each(function(){
                if ($(this).val().toLowerCase() == val.toLowerCase()){
                    duplicatecount ++;
                }
            })
        if (duplicatecount > 1 ){
                $(this).closest('input').after('<span class="waring-err invoicenumspn">Account number already exists</span>')
                $(this).addClass('con_error') 
            }
        else{
            $(this).removeClass('con_error')
        }
        }
    var currentpos = $(this)
    var query = $.trim($(this).val());
     $.ajax({
         url: '/projects/check_accountno/',  
         type: 'GET',
         data: {
             'account_no': query , 
         },
         success: function(data) {
          if(data.account_num == true){
            swal.fire("Account number already exists")
            currentpos.val("")
          }
         },
         error: function(xhr, status, error) {
             console.log('Error: ' + error); 
         }
     });
    })
    $(document).on("click", ".draft-cls", function (e){
        if ($('.con_error').length > 0) {
            return false
        }
    })
    
    $(document).on('change','.con_error',function(){
        $(this).removeClass('con_error')
    })

    var row=1;
    var emptytaxnamedata;
    var emptytaxnumdata;
    $(document).on("click","#add", function(){
        var rows=$(this).attr('row')
        var rowid=parseInt(rows)+1
        var spanid=$(this).closest('tr').index()
        $('#taxnm-'+spanid+'').remove()
        $('#taxnum-'+spanid+'').remove()
        $('.taxname-cls').each(function(){
            var val =$(this).val()
            if (val  == ''){
                emptytaxnamedata = false;
                $(this).closest('td').find('textarea').after('<span class="waring-err" id="taxnm-'+spanid+'" >Please Provide a Tax Name</span>')
            }
            else{
                emptytaxnamedata = true;
                $('#taxnm-'+spanid+'').remove()
            }
        })

        $('.taxnumber-cls').each(function(){
            var val =$(this).val()
            if (val  == ''){
                emptytaxnumdata = false;
                $(this).closest('td').find('textarea').after('<span class="waring-err" id="taxnum-'+spanid+'" >Please Provide a Tax Number</span>')
            }
            else{
                emptytaxnumdata = true;
                $('#taxnum-'+spanid+'').remove()

            }
        })

        if (taxname == true && taxnum == true  && emptytaxnamedata == true && emptytaxnumdata == true){
            var new_row1='<tr class="same-line-err" id="blockrow'+row+'"><div class="row"><div class="col-6"><td><input type="hidden" name="taxnamehdid" value="" > <textarea rows="4" cols="40" id="taxname'+row+'"  name="taxname" class="form-control taxname-cls"></textarea></td></div><div class="col-6"><td><textarea rows="4" cols="40"  id="taxnumber'+row+'"  name="taxnumber" class="form-control taxnumber-cls"></textarea></td> <td><button id="add" class="btn btn-clr add-btn" row="'+rowid+'" type="button" value="Add"> <i class="fa fa-plus"></i> </button> <button id="delete" class="btn btn-clr" delete-"btn" type="button" row="'+rowid+'" value="delete"> <i class="fa fa-minus"></i> </button></td></div></div></tr>'

            $("#tax").append(new_row1);
            row++;
            return false;
        }
    })
});

$(document).ready(function() {
    function validateBankName(input) {
        var bankname = $(input).val();
        var new_name = bankname.replace(/[^a-zA-Z\s]+/g, "");
        $(input).val(new_name);
    }
    // Attach bank name validation to existing rows
    $('.banknamecls').on('input', function() {
        validateBankName(this);
    });

    // Attach bank name validation to dynamically added rows
    $('#bank_information').on('input', '.banknamecls', function() {
        validateBankName(this);
    });

    function validateAccountNumber(input) {
        var banknumber = $(input).val();
        var new_number = banknumber.replace(/[^a-zA-Z0-9]+/g, ""); 
        $(input).val(new_number);
    }
    

    // Attach account number validation to existing rows
    $('.accnocls').on('input', function() {
        validateAccountNumber(this);
    });

    // Attach account number validation to dynamically added rows
    $('#bank_information').on('input', '.accnocls', function() {
        validateAccountNumber(this);
    });
});
