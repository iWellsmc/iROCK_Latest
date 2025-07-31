$(document).on('change','.select-invoice',function(){
    if (parseInt($(this).val()) == 2){
      $('.with_invoice').css('display','none')
      $('.without_invoice').css('display','')
    }
    else{
      $('.without_invoice').css('display','none')
      $('.with_invoice').css('display','')
    }
  })


  $(document).on('change','.select-Signatory',function(){
    let signatory_value=$(this).val()
    let currency_count=$('#currency_count').val()
    if(currency_count == 0){
      new swal({
        title: "Update General Settings",
        button: "Ok",
      }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = generalSettingUrl;
        }
    });
      $(this).val('')
    }
    else{
    if(signatory_value == '1'){
      $('#company_level').css('display','block')
      $('#Project_level').css('display','none')
      $('#project_sign').css('display','none')
    }
    if(signatory_value == '2'){
      $('#company_level').css('display','none')
      $('#Project_level').css('display','block')
      $('#project_sign').css('display','none')
      $('#get_project').val('')
    }
    if(signatory_value == ''){
      $('#company_level').css('display','none')
      $('#Project_level').css('display','none')
      $('#project_sign').css('display','none')
    }
  }
  })
  

  $(document).on('change','.select-invoice-project',function(){
    let invoice_val=$(this).val()
    if(invoice_val == '1'){
      $('#master_project_list_project').removeAttr('style')
      $('#master_project').css('display','none')
    }
    if(invoice_val == '2'){
      $('#master_project').removeAttr('style')
      $('#master_project_list_project').css('display','none')
    }
  })