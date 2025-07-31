//global variable
var field_name_id=[];
var field_name_ids=[];
var obj=[];
var subarray=[];
var fieldsub=[];
var project_id='';
var project_pkid='';
$(".submit-cls").click(function(){
  var get_data_id=$(this).attr("data-id");
  project_pkid=$(this).attr('project_id');
  if (get_data_id=="1"){
  var form=$("#create-masterproject");
  $.ajax({
    type:"POST",
    container:"#create-masterproject",
    url:'/projects/masterprojectcreate',
    data:form.serialize(),
    success: function(data){
      if (data.is_taken) {
          ("Project name is already exists.");
      }
  else{
    $.each(data.project,function(key,val){
      project_id=val.id
    })
  }
    }
    })
  }
  else if (get_data_id=="2") {
    var form=$("#create-block");
    $.ajax({
      type:"POST",
      container:"#create-block",
      url:'/projects/createblock',
      data:form.serialize(),
      success: function(data){
        console.log(data)
      }
    })
  }
  else if (get_data_id=="3") {
    var form=$("#create-field");
    $.ajax({
      type:"POST",
      container:"#create-field",
      url:'/projects/createfield',
      data:form.serialize(),
      success: function(data){
        console.log(data)
      }
    })
  }
  else if (get_data_id=="4") {
    var form=$("#create-cluster");
    $.ajax({
      type:"POST",
      container:"#create-cluster",
      url:'/projects/createcluster',
      data:form.serialize(),
      success: function(data){
        console.log(data)
      }
    })
  }   
  else if (get_data_id=="5") {
    var form=$("#create-well");
    $.ajax({
      type:"POST",
      container:"#create-well",
      url:'/projects/createwell',
      data:form.serialize(),
      success: function(data){
        console.log(data)
        // alert("working")
        var current_url=$(location).attr("href")
        var replace_url=current_url.replace('createwell/'+project_pkid+'','listmaster/')
        window.location.href = replace_url;

      }
    })
  }  
    var projectname=$("#id_name").val()
    var country=$("#id_country option:selected").text();
    var environment=$("#id_project_environment option:selected").text();
    var project='<p>'+projectname+'</p>';
    var country_name='<p>'+country+'</p>'
    $(".project_name").html(project);
    $(".project_country").html(country_name);
    var block_array=[];


    $('input[name="block_name_check"]').on('change', function(){
      var ids=$(this).attr('data-id');
  })

  $.each(field_name_ids,function(key,val){
    field_name_id[val]=[]
      $('input[name=field_name'+val+']').each(function() {
        // console.log($(this).val())
          field_name_id[val].push($(this).val());
      })
  })
  var field_name_show=[];
  // $(document).on('each','.fieldsubtype-class:checked', function (){
  $(".fieldsubtype-class:checked").each(function(){
    fieldsub.push($(this).attr('p_id'));
    field_name_show.push($(this).next('label').text());
  })
  console.log(fieldsub);//work
  var show_field_name=''
  $.each(field_name_show,function(key,val){
    show_field_name+='<p>'+val+'</p><br>'
  })
  $(".field-show-cls").html(show_field_name)
  
  var sub_name=''
  var sub_list=[];
  $.each(fieldsub,function(key,val){

    $('#fieldsub_id'+val+' input[type=checkbox]:checked').each(function(){
      sub_name=$(this).attr('data-name')
      subarray.push({"type":val,"value":sub_name})
    })

  })
  console.log(subarray);
  var sub_sub_name=[];
  $.each(subarray,function(key,val){
    // console.log(val.type);
    // console.log(val.value);
    $('#table_fieldsub-'+val.value+''+val.type+' input[type=text]').each(function(){
    // $(document).on('each', '#table_fieldsub-'+val.value+''+val.type+' input[type=text]', function () {
      sub_sub_name.push({"types":val.value+val.type,"values":$(this).val()});
    })
  })
  console.log(sub_sub_name); 
  var sub_sub_checkbox=''
  $.each(sub_sub_name,function(key,val){
    sub_sub_checkbox+='<input type="checkbox" name="sub_checkbox" data-id="'+val.types+'" class="sub_sub_field_cls" value="'+val.values+'">&emsp;'+val.values+'<br>'
  })
  if ($(".sub_sub_check_cls").children().length==0){
    $(".sub_sub_check_cls").append(sub_sub_checkbox)
  }

    var checked_block=[];
    var check_value=[];
    $('input[name="block_name_check"]:checked').each(function() {
      checked_block.push($(this).val())
      check_value.push($(this).attr('data-id'))
   });
    var show_block=''
    $.each(checked_block,function(key,val){
     
      show_block+='<p>'+val+'</p><br>'
    })
    $(".show-checked-block").html(show_block);
    $.each(check_value,function(key,val){
      // console.log(val)
      //  console.log(obj); 
    // $.each(obj,function(keys,values){
    //     // if ($(val==values)
    //     console.log(values)
      })
    // })
    if (get_data_id=="1"){
        Swal.fire({
            text: 'Do you want to add  block(s) to this project?',
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
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createmaster/",'createblock/'+project_id+'')
              window.location.href = replace_url;
                // $(".step-1").hide();
                // $(".step-2").show();
            //   Swal.fire('Saved!', '', 'success')
            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createmaster/","listmaster/")
              window.location.href = replace_url;
              // Swal.fire('Changes are not saved', '', 'info')
            }
          })
    }
    else if(get_data_id=="2"){
        Swal.fire({
            text: 'Do you want to add  field(s) to this project?',
            showDenyButton: true,
            // showCancelButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            confirmButtonColor: '#AF2B50',
            denyButtonColor:'#AF2B50',
            customClass: {
              actions: 'my-actions',
            //   cancelButton: 'order-1 right-gap',
              confirmButton: 'order-2',
              denyButton: 'order-3',
            }
          }).then((result) => {
            if (result.isConfirmed) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createblock/",'createfield/'+project_id+'')
              window.location.href = replace_url;
                // $(".step-2").hide();
                // $(".step-3").show();
            //   Swal.fire('Saved!', '', 'success')
            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createblock/","listmaster/")
              window.location.href = replace_url;
            }
          })
    }else if (get_data_id=="3"){
        Swal.fire({
            text: 'Do you want to add  Well Pad/ Well Platform/ Subsea Cluster (s) to this project?',
            showDenyButton: true,
            // showCancelButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            confirmButtonColor: '#77d61f',
            denyButtonColor:'#AF2B50',
            customClass: {
              actions: 'my-actions',
            //   cancelButton: 'order-1 right-gap',
              confirmButton: 'order-2',
              denyButton: 'order-3',
            }
          }).then((result) => {
            if (result.isConfirmed) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createfield/",'createcluster/'+project_id+'')
              window.location.href = replace_url;               
              // $(".step-3").hide();
                // $(".step-4").show();

            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createfield/","listmaster/")
              window.location.href = replace_url;
            }
          })
    }else if (get_data_id=="4"){
        Swal.fire({
            text: 'Do you want to add  Well (s) to this project?',
            showDenyButton: true,
            // showCancelButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            confirmButtonColor: '#77d61f',
            denyButtonColor:'#AF2B50',
            customClass: {
              actions: 'my-actions',
            //   cancelButton: 'order-1 right-gap',
              confirmButton: 'order-2',
              denyButton: 'order-3',
            }
          }).then((result) => {
            if (result.isConfirmed) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createcluster/",'createwell/'+project_id+'')
              window.location.href = replace_url;  
                // $(".step-4").hide();
                // $(".step-5").show();
            //   Swal.fire('Saved!', '', 'success')
            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace("createcluster/","listmaster/")
              window.location.href = replace_url;
            }
          })
    }

})
var row=1;
$(document).on("click","#block-add-row", function(){
    var new_row='<tr id="blockrow'+row+'"><td><input name="block_name" type="text" id="block'+row+'"class="form-control" placeholder="Block Name"/></td><td><button id="delete-row" class="btn-clr block-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $("#block_table").append(new_row);
    // alert(new_row)
    row++;
    return false;
})
$(document).on("click", ".block-delete-row", function () {
    if(row>1) {
        $(this).closest('tr').remove();
        row--;
      }
    return false;
})
$(document).on("change","[name=block_name_check]", function(){
    var val=$(this).attr('data-id');
    var field=''
    if ($(this).is(":checked")){
        field+='<table id=table-'+val+'><tbody id ="field_table"><tr><td id="fieldrow0"><input type="text" name="field_name'+val+'" class="form-control" placeholder="Field Name"></td><td><button id="field-add-row" class="btn btn-clr add-btn" type="button" data-id='+val+' value="Add"><i class="fa fa-plus"></i></button></td></tr></tbody></table>'
        //ui next start
        let appendTable = $(this).parent().next();
        appendTable.append(field);
      
    }
    else{
        $('#table-'+val+'').remove();
    }

})
var row=1;
$(document).on("click","#field-add-row", function(){
    var get_table_id=$(this).attr('data-id');
    // var table_id=get_table_id[1];
    // alert(get_table_id)
    var new_row='<tr id="fieldrow'+row+'"><td><input name="field_name'+get_table_id+'" type="text" id="field'+row+'"class="form-control" placeholder="Field Name"/></td><td><button id="delete-row" class="btn-clr field-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $('#table-'+get_table_id+'').append(new_row);
    // alert(new_row)
    row++;
    return false;
})
$(document).on("click", ".field-delete-row", function () {
    if(row>1) {
        $(this).closest('tr').remove();
        row--;
      }
    return false;
})

$(".back-cls").click(function(){
  var get_id=$(this).attr('data-id');
  if (get_id=="2"){
    $(".step-1").show();
    $(".step-2").hide();
  }
  else if(get_id=="3"){
    $(".step-2").show();
    $(".step-3").hide();
  }
  else if(get_id=="4"){
    $(".step-3").show();
    $(".step-4").hide();
  }
  else if(get_id=="5"){
    $(".step-4").show();
    $(".step-5").hide();
  }
})
// field sub wellpad etc..
$(document).on("change", ".field-class", function (){
  get_dataid=$(this).attr('data-id');
  get_text=$(this).next('label').text();
  get_name=$(this).attr('data-name');
  var table=''
  table+='<table id=table_fieldsub-'+get_name+''+get_dataid+'><tbody id ="fieldsub_table"><tr><td id="fieldsubrow0"><input type="text" name="fieldsub_name-'+get_name+''+get_dataid+'" class="form-control" data-name="'+get_name+'"></td><td><button id="fieldsub-add-row" class="btn btn-clr add-btn" type="button" data-name="'+get_name+'" data-id="'+get_dataid+'" value="Add"><i class="fa fa-plus"></i></button></td></tr></tbody></table>'
  if ($(this).is(":checked")){
    $(this).next("label").after(table);
  }
  else{
    $('#table_fieldsub-'+get_name+''+get_dataid+'').remove();    
  }
})

// add row in wellpad etc..
var row=1;
$(document).on("click","#fieldsub-add-row", function(){
  get_field_name=$(this).attr('data-name');
  // alert(get_field_name.replace("_"," "))
  get_field_id=$(this).attr('data-id');
  // alert(get_field_id)
    var new_row='<tr id="fieldsubrow'+row+'"><td><input name="fieldsub_name-'+get_field_name+''+get_field_id+'" type="text" id="fieldsubrow'+row+'"class="form-control" placeholder=" "/></td><td><button id="delete-row" class="btn-clr fieldsub-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $('#table_fieldsub-'+get_field_name+''+get_field_id+'').append(new_row);
    // alert(new_row)
    row++;
    return false;
})

// delete row in wellpad etc..
$(document).on("click", ".fieldsub-delete-row", function () {
  if(row>1) {
      $(this).closest('tr').remove();
      row--;
    }
  return false;
})
//well add multiple
$(document).on("change", ".well_add_cls", function (){
  get_well_data_id=$(this).attr('data-id');
  get_well_val=$(this).val();
  var well_table=''
  if ($(this).is(":checked")){
    well_table+='<table id=table_wellsub-'+get_well_data_id+''+get_well_val+'><tbody id ="wellsub_table"><tr><td id="wellsubrow0"><input type="text" name="wellsub_name-'+get_well_data_id+'-'+get_well_val+'" class="form-control"></td><td><button id="wellsub-add-row" class="btn btn-clr add-btn" type="button" data-name="'+get_well_data_id+''+get_well_val+'" data-val="'+get_well_data_id+'-'+get_well_val+'" value="Add"><i class="fa fa-plus"></i></button></td></tr></tbody></table>'
    $(this).next("label").after(well_table);
  }
  else{
    $('#table_wellsub-'+get_well_data_id+''+get_well_val+'').remove();    
  }
})

// add row in wellsub ..
var row=1;
$(document).on("click","#wellsub-add-row", function(){
  get_well_sub_name=$(this).attr('data-name');
  // alert(get_field_id)
  get_well_val=$(this).attr('data-val');
    var new_row='<tr id="wellsubrow'+row+'"><td><input name="wellsub_name-'+get_well_val+'" type="text" id="wellsubrow'+row+'"class="form-control" placeholder=" "/></td><td><button id="delete-row" class="btn-clr wellsub-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $('#table_wellsub-'+get_well_sub_name+'').append(new_row);
    // alert(new_row)
    row++;
    return false;
})

// delete row in wellsub etc..
$(document).on("click", ".wellsub-delete-row", function () {
  if(row>1) {
      $(this).closest('tr').remove();
      row--;
    }
  return false;
})

$(document).on('change','input[name="field_checkbox"]',function(){
    var data_id=$(this).attr('p_id');
    var get_check_field=$(this).next('label').text();
    var field_type=''
    if ($(this).is(":checked")){
      field_type+='<div id="fieldsub_id'+data_id+'"><h5 class="sub-fld">'+get_check_field+'</h5>'
      field_type+='<input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id1"  data-id="'+data_id+'" data-name="well_pad" class="field-class" value="well_pad">&emsp;<label>Well Pad</label><br><input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id2"  data-id="'+data_id+'" class="field-class" data-name="well_platform" value="well_platform">&emsp;<label>Well Platform</label><br><input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id3" data-id="'+data_id+'" class="field-class" data-name="subsea_clusters" value="subsea_clusters">&emsp;<label>Subsea Clusters</label><br>'
      field_type+='<br>'
      // $(".field_subtype").append(field_type);
      let parent1 = $(this).parent();
      let nextClm = parent1.parent().next();
      let subtype = nextClm.children('.field_subtype');
      subtype.append(field_type)
      console.log()
    }
    else{
        $('#fieldsub_id'+data_id+'').remove();
    }
})
$(document).on('change','.sub_sub_field_cls',function(){
  var wells=''
  var data=$(this).val();
  var get_val=data.replace(" ","_");
  var subdataid=$(this).attr('data-id');
  if ($(this).is(":checked")){
    wells+='<div id="well-'+get_val+'"><h5>'+data+'</h5>'
    wells+='<input type="checkbox" name="wells'+get_val+'" class="well_add_cls"  data-id="'+get_val+'" value="Exploration_Wells">&emsp;<label>Exploration Wells</label><br><input type="checkbox" class="well_add_cls" name="wells'+get_val+'" data-id="'+get_val+'" value="Appraisal_Wells">&emsp;<label>Appraisal Wells</label><br><input type="checkbox" name="wells'+get_val+'" class="well_add_cls" data-id="'+get_val+'" value="Development_Wells">&emsp;<label>Development Wells</label><br><input type="checkbox" name="wells'+get_val+'" class="well_add_cls" data-id="'+get_val+'" value="Pilot_Wells">&emsp;<label>Pilot Wells</label><br><input type="checkbox" name="wells'+get_val+'" class="well_add_cls" data-id="'+get_val+'" value="Well_Intervention">&emsp;<label>Workovers/Well Intervention</label><br><input type="checkbox" name="wells'+get_val+'" data-id="'+get_val+'" class="well_add_cls" value="Infill_Wells">&emsp;<label>Infill Wells</label><br>';
    $(".well_cls").append(wells)
  }
  else{
    $('#well-'+subdataid+'').remove();
  }
})