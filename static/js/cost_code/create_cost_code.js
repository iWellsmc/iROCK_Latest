let edit_table_length=$('#edit_rows').val()

$(document).on('click','.level_cls',function(){
  let value=$(this).find(':selected').val()
  if (value == 'create'){
    $(this).hide(500)
    $(this).next('.new_level_cls').show(500)
  }
})

$(document).on('click','.del_button',function(){
  let this_val=$(this)
  let del_master=$(this).attr('data-id')
  Swal.fire({
    title: 'Are you sure you want to delete ',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, I Confirm',
    cancelButtonText: 'No',
  }).then((result) => {
  if (result.isConfirmed) 
  $.ajax({
    url: "/cost_code/deletemaster/",
    type: 'POST',
    headers: { "X-CSRFToken": csrf_token},
    data: { 
      'id':del_master,
     },
    success: function (response) {
      this_val.closest('tr').remove()
    }
  })
})
})


$('#add').click(function(){ 
  
  var pagetype=$('#pagetype').val() 
  if(pagetype=='edit'){
    get_tr=$('#id_edit_cost_tbl >tbody > tr:last')
    new_tr=$('#id_edit_cost_tbl >tbody > tr:first')
    get_tbl_len=$('#id_edit_cost_tbl >tbody > tr').length
    let add_level_count = get_tbl_len-1
    let clone =new_tr.clone();
    clone.find(':text').val('');
    clone.find('.del_button').parent().remove()
    clone.find('.lev_nm_cls').text('Level '+add_level_count)
    console.log('get_tbl_len',get_tbl_len)
    if(get_tbl_len == 2){
      clone.find('.level_type').val('Discipline');
      clone.find('.level_cls').val('Discipline')
      clone.find('.level_type').attr('readonly');
      clone.find('.lev_nm_cls').text('Level 2')
      clone.find('td:last').find('a').attr('href','#collapseExample2');
      clone.find('.level_1').addClass('level_2')
      clone.find('.level_1').text('Component L2 ')
      clone.find('.level_1').removeClass('level_1')
      let subtype_category=subtype.replace(/&quot;/g,'')
      let subtype_format=subtype_category.replace(/&amp;/g,"&")
      let final_subtype=subtype_format.replace("[",'')
      let data=final_subtype.replace("]",'')
      let sub_data=data.split(",")
      let tr_value=`<tr><td colspan="12" class="p-0"><div class="collapse coll_2" id="collapseExample2"><div class="card card-body shadow-none master-crd pad-adj"><div role="tabpanel" class="tab-pane active space" id="roles{{obj.id}}"><div class="row"><div class="col-12"><h4 class="proj-hd">Discipline Type</h4></div></div><div class="row" id="name"><div class="col-12">`
      $(sub_data).each(function(index, value){
        tr_value+=`<div class="row"><div class="col-12"><li class="role-cls" process_id="{{flow.process.id}}" pk="{{obj.id}}">${value}</li></div></div>`
        console.log("index : ",index, " value :", value);
    });
    tr_value+=`</div></div></div></div></div></div></td></tr>`
    $('#id_edit_cost_tbl >tbody').append(tr_value)
    console.log('tr_value',tr_value)
      // clone.find('.check_type').html('')
     
      // <a class="btn p-0" data-toggle="collapse" href="#collapseExample{{master.id}}" role="button" aria-expanded="false" aria-controls="collapseExample">
      //                           <span class="action-edit align-icons">
      //                               <!-- <i class="fa fa-eye eyebutton" title="View" style="font-size:17px; color:#95183a;"></i> -->
      //                               <button class="comp-btn level_2" title="View">Component L2 <i class="fa-solid fa-chevron-down" id="bac-eye"></i></butto></span></a>
    }
    else{
      clone.find('.level_type').removeAttr('readonly');
      clone.find('.leveltype').val('new')
      clone.find('.level_cls').val('')
    }
    if(get_tbl_len > 2){
      clone.find('td:last').html('<button id="remove-btn" type="button" class="remove-btn btn btn-clr waves-effect waves-float waves-light">Remove</button>')
    }
    console.log('get_tbl_len',get_tbl_len)
    if(get_tbl_len == 2 || get_tbl_len == 3 || get_tbl_len == 4){
      clone.find('.digit_cls').val('3');
    }
    else{
      clone.find('.digit_cls').val('2');
    }
    // if(get_tbl_len == 2){
    //   clone.find('.lev_nm_cls').text('Level 2')
    // }
    let allselected_option=[]
    $('.level_cls').each((index, value) => {
      allselected_option.push($(value).val())
    })
    console.log(allselected_option)
    clone.find('.costcodemasterid').val('')
    clone.find('.level_cls').prop("disabled", false)
    clone.find('.level_cls').val("")

    clone.find('.digit_cls').prop("disabled", false)
    
    if(get_tbl_len == 2 || get_tbl_len == 3 || get_tbl_len == 4){
      clone.find('.type_based_cls').prop("maxlength", 3)
    }
    else{
      clone.find('.type_based_cls').prop("maxlength", 2)
    }
    clone.find('.level_cls').removeAttr('readonly');
    

    clone.find('.digit_cls').removeAttr('readonly');

    clone.find('.type_cls').removeAttr('readonly');
    clone.find('.type_based_cls').removeAttr('readonly');
    clone.find('.seq_cls').removeAttr('readonly');


    clone.find('.type_cls').prop("disabled", false)
    clone.find('.type_based_cls').prop("disabled", false)
    clone.find('.seq_cls').prop("disabled", false)
    clone.find('.level_cls option').each(function() {
      var optionValue = $(this).val();
      console.log(optionValue)
      if (allselected_option.includes(optionValue)) {
        $(this).prop('disabled', true);
      }

    })
    get_tr.after(clone);
  }
  else{
    get_tr=$('#id_create_cost_tbl >tbody > tr:last')
    new_tr=$('#id_create_cost_tbl >tbody > tr:first')
    get_tbl_len=$('#id_create_cost_tbl >tbody > tr').length
    let add_level_count = get_tbl_len+1
    let clone =new_tr.clone();
    console.log('len',get_tbl_len)
    clone.find(':text').val('');
    clone.find('.level_1').html('Component L2<i class="fa-solid fa-chevron-down pl-1" id="bac-eye"></i>')
    clone.find('.level_1').addClass('level_2')
    clone.find('.level_1').removeClass('level_1')
    // clone.find('.collapse').addClass('coll_2')
    if(get_tbl_len == 5 || get_tbl_len == 4 ){
      clone.find('.digit_cls').val('3');
    }
 
    else{
      clone.find('.digit_cls').val('2');
    }
    if(get_tbl_len == 5 || get_tbl_len == 4){
      clone.find('.type_based_cls').prop("maxlength", 3)
    }
   
    if(get_tbl_len == 2){
      clone.find('.lev_nm_cls').text("Level 2")
    }
    else{
      clone.find('.lev_nm_cls').text(`Level ${parseInt(add_level_count)-2}`)
    }
    
    clone.find('.seq_cls').val("")
    clone.find('.calbtn').attr('data-target','#exampleModalCenter2');
    if(get_tbl_len == 2){
      var levelmaster_dropdown=''
      levelmaster_dropdown += '<input class="form-control level_cls" value="Discipline" name="level_cls" readonly>'
      levelmaster_dropdown += '<select name="level_type" class="form-control level_cls" style="display:none">'
      levelmaster_dropdown += '<option value="2" selected>Discipline</option>'
      levelmaster_dropdown +='</select>'
      levelmaster_dropdown +='<input type="text" name="new_level" class="form-control new_level_cls" style="display:none" placeholder="Type New Level">'
      levelmaster_dropdown +='<input type="hidden" name="leveltype" class="leveltype"></input>'
      clone.find('td:nth-child(2)').html(levelmaster_dropdown)
      clone.find('td:last').find('a').attr('href','#collapseExample2');
      let subtype_category=subtype.replace(/&quot;/g,'')
      let subtype_format=subtype_category.replace(/&amp;/g,"&")
      let final_subtype=subtype_format.replace("[",'')
      let data=final_subtype.replace("]",'')
      let sub_data=data.split(",")
      let tr_value=`<tr><td colspan="12" class="p-0"><div class="collapse coll_2" id="collapseExample2"><div class="card card-body shadow-none master-crd pad-adj"><div role="tabpanel" class="tab-pane active space" id="roles{{obj.id}}"><div class="row"><div class="col-12"><h4 class="proj-hd">Discipline Type</h4></div></div><div class="row" id="name"><div class="col-12">`
      $(sub_data).each(function(index, value){
        tr_value+=`<div class="row"><div class="col-12"><li class="role-cls" process_id="{{flow.process.id}}" pk="{{obj.id}}">${value}</li></div></div>`
        console.log("index : ",index, " value :", value);
    });
    tr_value+=`</div></div></div></div></div></div></td></tr>`
      $('#id_create_cost_tbl >tbody').append(tr_value)
      // clone.find('td:last').html('<button id="remove-btn" type="button" class="remove-btn btn btn-clr btn-master waves-effect waves-float waves-light">Remove</button>')
    }
    if(get_tbl_len >= 3){
      var levelmaster_dropdown=''
      levelmaster_dropdown +='<input class="form-control new_level_cls" type="text" name="new_level"></input>'
      levelmaster_dropdown +='<input type="hidden" name="level_type" class="level_type" value="create"></input>'
      // levelmaster_dropdown +='<input type="hidden" name="leveltype" class="leveltype"></input>'

// levelmaster_dropdown +='<select name="level_type" class="form-control level_cls">'
      // levelmaster_dropdown += '<option value="">--Select--</option>'
      // levelmaster_dropdown += '<option value="create">Create New level</option>'
      // levelmaster_dropdown +='</select>'
      // levelmaster_dropdown +='<input type="text" name="new_level" class="form-control new_level_cls" style="display:none" placeholder="Type New Level">'
      levelmaster_dropdown +='<input type="hidden" name="leveltype" class="leveltype" value="new"></input>'
      levelmaster_dropdown +='<input type="hidden" name="level_cls"></input>'
      clone.find('td:nth-child(2)').html(levelmaster_dropdown)
      clone.find('td:last').html('<button id="remove-btn" type="button" class="remove-btn btn btn-clr waves-effect waves-float waves-light">Remove</button>')
    }
    get_tr.after(clone);

  }
})


$(document).on('change','.digit_cls',function(){
  let value=$(this).val();
  $(this).closest('tr').find('.type_based_cls').val('');
  $(this).closest('tr').find('.type_based_cls').attr('maxlength',value);
})

$(document).on('click','.remove-btn',function(){
  $(this).closest('tr').remove()
})


$(document).on('change','.new_level_cls',function(){
  let value=$(this).next('.level_type').val();
   if(value=='create'){
    $(this).closest('tr').find('.leveltype').val('new')
  }else{
    $(this).closest('tr').find('.leveltype').val('old')
  }
})


// $(document).on('change','.type_cls',function(){
//   $(this).closest('tr').find('.type_based_cls').val('')
// })



$(document).on('keyup','.type_based_cls',function(){
  if(!$(this).val()){
    $(this).css("border", "1px solid red");
  }
  else{
    if (event.keyCode === 190 || event.keyCode === 110) {
      if ($(this).val().indexOf('.') !== -1) {
        var value = $(this).val().replace('.', '');
        $(this).val(value)
        event.preventDefault();
      }
    }
    $(this).css("border", "");

  }
})






$('#createcostcode_master').submit(function(e) {

  e.preventDefault(); 
  let validation=false
  let startwith_values=[]
  let no_of_digit=[]
  let costcodeformat=$('#costcodeformat').val()
  if(costcodeformat==''){
    $('#costcodeformat').css("border", "1px solid red");
  }else{
    $('#costcodeformat').css("border", "");
  }
  $('.type_based_cls,.seq_cls,.level_cls').each(function(){
    current_val=$(this).val()
    altered_text=$.trim(current_val)
    $(this).val(altered_text)
  })

  $('#id_create_cost_tbl').find('tr').each((rowindex, row) => {
    console.log(rowindex)
    $(row).find('.digit_cls').each((index, digit) => {
      if(!$(digit).val()){   
        console.log('rr1')
        validation=true
        $(digit).css("border", "1px solid red");
      }else{
        no_of_digit.push($(digit).val())
        $(digit).css("border", "");

      }
    })
    console.log('startwith_values',startwith_values)
    $(row).find('.type_based_cls').each((index, startwith) => {
      // console.log($(row).find('.type_based_cls').eq(rowindex).val())

      if(!$(startwith).val()){    
        console.log('rr2')
        validation=true
        $(startwith).css("border", "1px solid red");
        startwith_values.push('')
      }else{
        startwith_values.push($(startwith).val())
        $(startwith).css("border", "");

      }
    })

    $(row).find('.seq_cls').each((index, sequence) => {
      if(!$(sequence).val()){   
        console.log('rr3')         
        validation=true
        $(sequence).css("border", "1px solid red");
      }else{
        $(sequence).css("border", "");

      }
    })

    $(row).find('.type_cls').each((index, type) => {
      if(!$(type).val()){   
        console.log('rr4')  
        validation=true
        $(type).css("border", "1px solid red");
      }else{
        $(type).css("border", "");

      }
    })

    $(row).find('.level_cls').each((index, level) => {
      if(!$(level).val()){   
        console.log('rr5')         
        validation=true
        $(level).css("border", "1px solid red");
      }else{
        $(level).css("border", "");

      }
    })
    if(rowindex>2){
      $(row).find('.new_level_cls').not(':hidden').each((index, newlevel) => {
        if(!$(newlevel).val()){   
          console.log('rr6')         
          validation=true
          $(newlevel).css("border", "1px solid red");
        }else{
          $(newlevel).css("border", "");
  
        }
      })


    }
  })

  // console.log(startwith_values)
  // console.log(no_of_digit)

  let hasduplicate=checkduplicatevalue(startwith_values)
  console.log('asd',startwith_values,no_of_digit)
  let comparelength=checklength(startwith_values,no_of_digit)
  // console.log(comparelength)

  // if(comparelength.length>0){
  //   for (var j = 0; j < comparelength.length; j++) {
  //       console.log(comparelength[j]+1)
  //       $('#id_create_cost_tbl tr').eq(comparelength[j]+1).find('td .type_based_cls').css("border", "1px solid red");
  //   }
  // }
  console.log({'comparelength.length == 0':comparelength.length == 0,'validation':validation,'hasduplicate':hasduplicate,'costcodeformat':costcodeformat})
  if(comparelength.length == 0 && validation==false && costcodeformat!=''){
    this.submit();
  }else{
    return false
  }

})


//cost code master edit form validations
$('#edit_costcode_form').submit(function(e) {
  e.preventDefault(); 
  let validation=false
  let startwith_values=[]
  let val=0
  let no_of_digit=[]
  let costcodeformat=$('#costcodeformat').val()

  if(costcodeformat==''){
    $('#costcodeformat').css("border", "1px solid red");
  }else{
    $('#costcodeformat').css("border", "");
  }

  $('.type_based_cls,.seq_cls,.level_cls,.new_level_cls').each(function(){
    current_val=$(this).val()
    altered_text=$.trim(current_val)
    $(this).val(altered_text)
  })

  $('#id_edit_cost_tbl').find('tr').each((rowindex, row) => {
    // console.log("rowindex"+rowindex)
    $(row).find('.digit_cls').each((index, digit) => {
      if(!$(digit).val()){ 
        console.log(0)           
        validation=true
        val++
        $(digit).css("border", "1px solid red");
        console.log('digit',digit)
      }else{
        no_of_digit.push($(digit).val())
        $(digit).css("border", "");

      }
    })
    $(row).find('.level_new_cls').not('[readonly]').not(':hidden').each((index, digit) => {
      if(!$(digit).val()){    
        validation=true
        val++
        $(digit).css("border", "1px solid red");
      }else{
        $(digit).css("border", "");

      }
    })
    $(row).find('.type_based_cls').each((index, startwith) => {

      if(!$(startwith).val()){     
        validation=true
        val++
        $(startwith).css("border", "1px solid red");
        // check
        startwith_values.push('')
      }else{
        startwith_values.push($(startwith).val())
        $(startwith).css("border", "");

      }
    })

    $(row).find('.seq_cls').each((index, sequence) => {
      if(!$(sequence).val()){    
        validation=true
        val++
        $(sequence).css("border", "1px solid red");
      }else{
        $(sequence).css("border", "");

      }
    })

    $(row).find('.type_cls').each((index, type) => {
      if(!$(type).val()){        
        validation=true
        val++
        $(type).css("border", "1px solid red");
      }else{
        $(type).css("border", "");

      }
    })

    $(row).find('.level_cls').each((index, level) => {
      if(!$(level).val()){
        validation=true
        val++
        $(level).css("border", "1px solid red");
      }else{
        $(level).css("border", "");

      }
    })
    if(rowindex>edit_table_length){
      $(row).find('.new_level_cls').each((index, newlevel) => {
        // if(!$(newlevel).val()){            
        //   validation=true
        //   $(newlevel).css("border", "1px solid red");
        // }else{
        //   $(newlevel).css("border", "");
  
        // }
      })


    }
  })


  let hasduplicate=checkduplicatevalue(startwith_values)
  console.log('asd',startwith_values,no_of_digit)
  let comparelength=checklength(startwith_values,no_of_digit)
  console.log('comparelength',comparelength)
  if(comparelength.length>0){
    for (var j = 0; j < comparelength.length; j++) {  
      console.log('ad')
        // $('#id_create_cost_tbl tbody tr').eq(comparelength[j]+1).find('td .type_based_cls').css("border", "1px solid red");
        // $('#id_edit_cost_tbl tbody tr').eq(comparelength[j]+1).find('td .type_based_cls').css("border", "1px solid red");

    }
  }



  if(comparelength.length == 0 && validation==false && costcodeformat!='' ){
    this.submit();
  }else{
    return false
  }
})



//cost code master create form validations
$('#createcostcode_master').submit(function(e) {
  e.preventDefault(); 
  let validation=false
  let startwith_values=[]
  let no_of_digit=[]
  let costcodeformat=$('#costcodeformat').val()
  if(costcodeformat==''){
    $('#costcodeformat').css("border", "1px solid red");
  }else{
    $('#costcodeformat').css("border", "");
  }

  $('.type_based_cls,.seq_cls').each(function(){
    current_val=$(this).val()
    altered_text=$.trim(current_val)
    $(this).val(altered_text)
  })

  $('#id_create_cost_tbl').find('tr').each((rowindex, row) => {
    $(row).find('.digit_cls').each((index, digit) => {
      if(!$(digit).val()){            
        validation=true
        $(digit).css("border", "1px solid red");
      }else{
        no_of_digit.push($(digit).val())
        $(digit).css("border", "");

      }
    })
    $(row).find('.type_based_cls').each((index, startwith) => {

      if(!$(startwith).val()){            
        validation=true
        $(startwith).css("border", "1px solid red");
      }else{
        startwith_values.push($(startwith).val())
        $(startwith).css("border", "");

      }
    })

    $(row).find('.seq_cls').each((index, sequence) => {
      if(!$(sequence).val()){            
        validation=true
        $(sequence).css("border", "1px solid red");
      }else{
        $(sequence).css("border", "");

      }
    })

    $(row).find('.type_cls').each((index, type) => {
      if(!$(type).val()){            
        validation=true
        $(type).css("border", "1px solid red");
      }else{
        $(type).css("border", "");

      }
    })

    $(row).find('.level_cls').each((index, level) => {
      if(!$(level).val()){            
        validation=true
        $(level).css("border", "1px solid red");
      }else{
        $(level).css("border", "");

      }
    })
    if(rowindex>2){
      $(row).find('.new_level_cls').each((index, newlevel) => {
        if(!$(newlevel).val()){            
          validation=true
          $(newlevel).css("border", "1px solid red");
        }else{
          $(newlevel).css("border", "");
  
        }
      })


    }
  })

  // console.log(startwith_values)
  // console.log(no_of_digit)

  let hasduplicate=checkduplicatevalue(startwith_values)
  let comparelength=checklength(startwith_values,no_of_digit)
  // console.log(comparelength)
  // if(comparelength.length>0){
  //   for (var j = 0; j < comparelength.length; j++) {

  //       $('#id_create_cost_tbl tr').eq(comparelength[j]+1).find('td .type_based_cls').css("border", "1px solid red");
  //   }
  // }

  // if(comparelength.length == 0 && validation==false && costcodeformat!=''){
  //   this.submit();
  // }else{
  //   return false
  // }

})






$(document).on('keyup','.seq_cls',function(event){
  if(!$(this).val()){
    $(this).css("border", "1px solid red");
  }
  else{
    if (event.keyCode === 190 || event.keyCode === 110) {
      if ($(this).val().indexOf('.') !== -1) {
        var value = $(this).val().replace('.', '');
        $(this).val(value)
        event.preventDefault();
      }
    }
    $(this).css("border", "");
  }
})

$(document).on('keyup','.digit_cls',function(event){
  if(!$(this).val()){
    $(this).css("border", "1px solid red");
  }else{
    if (event.keyCode === 190 || event.keyCode === 110) {
      if ($(this).val().indexOf('.') !== -1) {
        var value = $(this).val().replace('.', '');
        $(this).val(value)
        event.preventDefault();
      }
    }
    $(this).css("border", "");

  }
})


$(document).on('change','#costcodeformat',function(){
  if(!$(this).val()){
    $(this).css("border", "1px solid red");
  }else{
    $(this).css("border", "");

  }
})

$(document).on('change','.new_level_cls',function(){
  if(!$(this).val()){
    $(this).css("border", "1px solid red");
  }else{
    $(this).css("border", "");

  }
})





function checklength(startwith_values,no_of_digit) {
  let errorrows=[]
  console.log('startwith_values.length',startwith_values.length)
  console.log('no_of_digit.length',no_of_digit.length)
  let table_tr=$('.main_tr')
  if(startwith_values.length == no_of_digit.length){
    for (var i = 0; i < startwith_values.length; i++) {
      if(parseInt(no_of_digit[i]) != startwith_values[i].length){
        $(table_tr[i]).find('td .type_based_cls').css("border", "1px solid red");
        // console.log('#id_edit_cost_tbl tbody .main_tr tr:eq('+[i]+')','inddex',$('#id_edit_cost_tbl tbody tr:eq('+[i]+')'))
        // $('#id_create_cost_tbl tbody .main_tr tr:eq('+[i]+')').find('td .type_based_cls').css("border", "1px solid red");
        // $('#id_edit_cost_tbl tbody .main_tr tr:eq('+[i]+')').find('td .type_based_cls').css("border", "1px solid red");
        errorrows.push(i)
      }
    }
    return errorrows
  }

}

function checkduplicatevalue(array) {
  console.log('1',array)
  var valueSet = new Set();
  for (var i = 0; i < array.length; i++) {
    var value = array[i];
    if (valueSet.has(value)) {
      return true; 
    }
    valueSet.add(value);
  }
  return false; 
}
// $('.mySelect_cls').select2({
//   language: {
//     noResults: function(term) {
//       typed = $('.select2-search__field').val();
//     }
//   }
//   else if (value == 'Alphabets'){
//     $(this).val($(this).val().replace(/[^a-zA-Z]/g,''));
//   }
//   else{
//     $(this).val($(this).val().replace(/[^a-zA-Z0-9 _]/g,''));
//   }
// })


$(document).on('keyup','.level_cls',function(){
  $(this).removeAttr('style')
})

$(document).on('keypress','.type_based_cls',function(){
  old_val = $(this).val()
  $(this).val(old_val.replace(/\D/g, ''))
})

$(document).on('click','.level_1',function(e){
  $('.coll_1').toggle();
  $('.coll_2').hide();
})
$(document).on('click','.level_2',function(){
  $('.coll_2').toggle();
  $('.coll_1').hide();
})
