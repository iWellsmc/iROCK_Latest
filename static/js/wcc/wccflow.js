
$(function() {
let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
let wcc_check=Number($('#wcc_check').val());
let project_hdn=$('#project_hdn').val();
let options = $('#users_id').find('option');
let wcc_options = $('#wccroles_id').find('option');
let that=$(this)
let hdn_level_type_id=$('#hdn_level_type_id').val();
let user_array=create_array_obj(options);
let wcc_array=create_array_obj(wcc_options);

function create_array_obj(array_obj){
    new_list=[{'value':'','name':'--Select--'}];
    array_obj.each(function() {
        var value = $(this).val();
        var text = $(this).text();
        new_list.push({'value':value,'name':text})
    });
    return new_list
}


        if (wcc_check > 0){
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'WCC Approval Inprogress',
                showConfirmButton: true,
                timer:6000
                }).then(function() {
                    window.history.back();
                });
        }
        let level_type=$('.level_cls').find(':selected').val()
        if (level_type){
            // level_set_func(level_type)
        }
   

$(document).on('change','.station_cls',function(){
    let old_data=$(this).attr('st_old_data') || ''
    let val=Number($(this).val()) || 0;
    let data_id=$(this).attr('data_id')
    let html='';
    if (old_data){
        if (val > Number(old_data)){ 
            // may be use later
            let myDiv =  $(this).closest('div').next('div');
            // myDiv.children().each(function(index,value) {
            //     let count=index+1
            //     let con_data=(Number(old_data)*2)
            //     console.log('con_data',con_data)
            //     if (count > Number(con_data)){
            //         $(value).remove()
            //     }
            // })
            // $(this).attr('st_old_data','')
            for (let i = Number(old_data) || 0; i < val; i++) {
                // html +='<div class="row">'
                html +='<div class="col-3"><input type="hidden" name="hdnstation_user'+data_id+'-'+i+'" value="">';
                html +='<select name="station_role'+data_id+'-'+i+'" class="form-control role_cls">';
                $.each(wcc_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html += '</select></div>';
                html += '<div class="col-4">';
                html +='<input type="text" oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station_user'+data_id+'-'+i+'" class="form-control station_user_cls" autocomplete="off" data_id="'+i+'" level_id="'+data_id+'"></input>';
                html += '</div>';
                html +='<div class="col-5 pr-0"></div>'
                // html +='</div>'
                }
            $(this).closest('div').next('div').append(html)
        }
        else if (val == Number(old_data)){
            let myDiv =  $(this).closest('div').next('div');
            myDiv.children().each(function(index,value) {
                let count=index+1
                if (count > (val*2)){
                    $(value).remove()
                }
            })
            let role_class_count = myDiv.find('.role_cls').length
            for (let i = role_class_count; i < val; i++) {
                // html +='<div class="row pr-0">'
                html +='<div class="col-3"><input type="hidden" name="hdnstation_user'+data_id+'-'+i+'" value="">'
                html +='<select name="station_role'+data_id+'-'+i+'" class="form-control role_cls">';
                $.each(wcc_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html += '</select></div>';
                html += '<div class="col-4">';
                html +='<input type="text" oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station_user'+data_id+'-'+i+'" class="form-control station_user_cls" autocomplete="off" data_id="'+i+'" level_id="'+data_id+'"></input>';
                html += '</div>';
                html +='<div class="col-5 pr-0"></div>';
                // html +='</div>'
              }
            $(this).closest('div').next('div').html(html)
        }
        else{ 
            $(this).attr('st_old_data','')
            for (let i = 0; i < val; i++) {
                // html +='<div class="row pr-0">'
                html +='<div class="col-3"><input type="hidden" name="hdnstation_user'+data_id+'-'+i+'" value="">'
                html +='<select name="station_role'+data_id+'-'+i+'" class="form-control role_cls">';
                $.each(wcc_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html += '</select></div>';
                html += '<div class="col-4">';
                html +='<input type="text" oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station_user'+data_id+'-'+i+'" class="form-control station_user_cls" autocomplete="off" data_id="'+i+'" level_id="'+data_id+'"></input>';
                html += '</div>';
                html +='<div class="col-5 pr-0"></div>';
                // html +='</div>'
              }
            $(this).closest('div').next('div').html(html)
        }
    }
    else{
        for (let i = 0; i < val; i++) {
            // html +='<div class="row ">'
            html +='<div class="col-3">'
            html +='<select name="station_role'+data_id+'-'+i+'" class="form-control role_cls">';
            $.each(wcc_array, function(index, option) {
                html +='<option value="'+option.value+'">'+option.name+'</option>';
            });
            html += '</select></div>';
            html += '<div class="col-4">';
            html +='<input type="text" oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station_user'+data_id+'-'+i+'" class="form-control station_user_cls" autocomplete="off" data_id="'+i+'" level_id="'+data_id+'"></input>';
            html += '</div>';
            html +='<div class="col-5 pr-0"></div>';
          }
        $(this).closest('div').next('div').html(html)
    }
    // }
})
$('.station_user_cls').each(function() {
    let old_data=$(this).attr('old_data') || ''
    let val=Number($(this).val()) || 0;
    let get_data_id=$(this).attr('data_id')
    let level_id=$(this).attr('level_id')
    let html='';
    if (old_data) {
        if (val > Number(old_data)) {
            let myDiv = $(this).closest('div').next('div');
            myDiv.children().each(function(index,value) {
                let count=index+1
                if (count > Number(old_data)) {
                    $(value).remove()
                }
            })
            for (let i = Number(old_data); i < val; i++) {
                html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
                $.each(user_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html+='</select></div>';
            }
            $(this).closest('div').next('div').append(html);
        } else if (val == Number(old_data)) {
            let myDiv = $(this).closest('div').next('div');
            myDiv.children().each(function(index,value) {
                let count=index+1
                if (count > val) {
                    $(value).remove()
                }
            })
            let user_class_count = myDiv.find('.user_cls').length
            for (let i = user_class_count; i < Number(old_data); i++) {
               
                html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
                $.each(user_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html+='</select></div>';
            }
                $(this).closest('div').next('div').append(html);
        } else {
            for (let i = 0; i < val; i++) {
                html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
                $.each(user_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html+='</select></div>';
            }
            $(this).closest('div').next('div').html(html); 
        }
    } else {
        for (let i = 0; i < val; i++) {
            html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
            $.each(user_array, function(index, option) {
                html +='<option value="'+option.value+'">'+option.name+'</option>';
            });
            html+='</select></div>';
        }
        $(this).closest('div').next('div').html(html);
    }
});
$(document).on('change','.station_user_cls',function() {
    let old_data=$(this).attr('old_data') || ''
    let val=Number($(this).val()) || 0;
    let get_data_id=$(this).attr('data_id')
    let level_id=$(this).attr('level_id')
    let html='';
    if (old_data){
        if (val > Number(old_data)){

            let myDiv = $(this).closest('div').next('div');
            myDiv.children().each(function(index,value) {
                let count=index+1
                if (count > Number(old_data)){
                    $(value).remove()
                }
            })
            $(this).attr('old_data','')
            for (let i = Number(old_data); i < val; i++) {
                html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
                $.each(user_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html+='</select></div>';
            }
            $(this).closest('div').next('div').append(html);
        }
        else if (val == Number(old_data)){ 
            let myDiv = $(this).closest('div').next('div');
            myDiv.children().each(function(index,value) {
                let count=index+1
                if (count > val){
                    $(value).remove()
                }
            })
        }
        else{ 
            $(this).attr('old_data','')
            for (let i = 0; i < val; i++) {
                html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
                $.each(user_array, function(index, option) {
                    html +='<option value="'+option.value+'">'+option.name+'</option>';
                });
                html+='</select></div>';
            }
            $(this).closest('div').next('div').html(html); 
        }
    }
    else{ 
        for (let i = 0; i < val; i++) {
            html +='<div class=""><select name="user'+level_id+'-'+get_data_id+'" class="form-control user_cls" autocomplete="off">'
            $.each(user_array, function(index, option) {
                html +='<option value="'+option.value+'">'+option.name+'</option>';
            });
            html+='</select></div>';
        }
        $(this).closest('div').next('div').html(html);
    }
})


$(document).on('change','.level_cls',function(){
    let val=$(this).find(':selected').val()
    if (val){
        level_set_func(val)
    }
    else{
        $('.level_div').html('')
    }
    
})

function level_set_func(val){

    $.ajax({
        type:"POST",
        data:{'csrfmiddlewaretoken':csrftoken,'type':val,'project_id':project_hdn},
        url:'/wcc/wccprojectlevels',
        success: function (data) {
            // console.log(data)
            let html='';
            if (val == "well"){
                $.each(data.data,function(index,value){
                    console.log(data)
                    html +='<div class="row my-2"><div class="col-3 check-label">'
                    html += '<input type="checkbox"  name="well_discipline" class="lvl_app_cls check_val'+value.discipline_id+' well_discipline_cls" value="'+value.discipline_id+'"><label>'+value.discipline_name+'-'+value.project_discipline+'-'+value.cluster+'</label>'
                    html +='</div><div class="col-9"></div></div>'
                    $.each(value.well_datas,function(index2,value2){
                        html +='<div class="row my-2"><div class="col-3 check-label">'
                        html += '<input type="checkbox"  name="level" class="lvl_app_cls check_well_dis well_dis_id'+value.discipline_id+'" check_val="'+value.discipline_id+'" value="'+value2.id+'"><label>'+value2.wellname__well_subname+'</label>'
                        html +='</div><div class="col-9"></div></div>'
                    })
                })
            }
            else{
                $.each(data.data,function(index,value){
                    if (val == "discipline"){
                        let project_discipline="";
                        let get_discipline=value.project_discipline__project_discipline
                        let cluster=value.project_discipline__cluster__clustersubname__cluster_subname
                        if (get_discipline == "1"){
                            project_discipline = "Green Field Development"
                        }
                        else if (get_discipline == "2"){
                            project_discipline = "Brown Field Development"
                        }
                        else{
                            project_discipline = "Others"
                        }
                        html +='<div class="row my-2"><div class="col-3 check-label demo">'
                        html += '<input type="checkbox" name="level" class="lvl_app_cls" value="'+value.id+'"><label>'+value.name+'-'+project_discipline+'-'+cluster+'</label>'
                        html +='</div><div class="col-9"></div></div>'
                    }
                    else{
                        html +='<div class="row my-2"><div class="col-3 check-label">'
                        html += '<input type="checkbox"  name="level" class="lvl_app_cls" value="'+value.id+'"><label>'+value.name+'</label>'
                        html +='</div><div class="col-9"></div></div>'
                    }
                })             
            }
            $('.level_div').html(html)
            // $('.lvl_app_cls option[value='+hdn_level_type_id+']').attr("selected", "selected");
            // $('.lvl_app_cls').removeClass('con_error')
        }
    })
}


$(document).on('click','.lvl_app_cls',function(){
    let val=$(this).val()
    let check_val=$(this).attr('check_val') || ''
   
    // check below code
    if (check_val){
        if ($('.well_dis_id'+check_val+':checked').length > 0){
            let html ='';
            html += '<div class="row input-wid"><input type="hidden" name="hdnstation'+check_val+'" value=""><div class="col-3 station">'
            html +='<input type="text"  oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station'+check_val+'" class="form-control station_cls" autocomplete="off" data_id="'+check_val+'"></div><div class="row col-9 station_per_div"></div></div>';

            if ($('.check_val'+check_val+'').is(':checked') ==  false){
                $('.check_val'+check_val+'').prop('checked',true)
                $('.check_val'+check_val+'').closest('div').next('div').html(html);
                console.log('check_val',check_val)
            }
        }
        else{
            $('.check_val'+check_val+'').prop('checked',false)
            $('.check_val'+check_val+'').closest('div').next('div').html('');
        }
    }
    if ($(this).is(':checked')){
        let html ='';
        console.log('val',val)
        html += '<div class="row input-wid"><input type="hidden" name="hdnstation'+val+'" value=""><div class="col-3 station">'
        html +='<input type="text"  oninput="this.value = this.value.replace(/[^0-9]/g,'+"''"+')" name="station'+val+'" class="form-control station_cls" autocomplete="off" data_id="'+val+'"></div><div class="row col-9 station_per_div"></div></div>';
        $(this).closest('div').next('div').html(html);
    }
    else{
        if ($(this).hasClass('well_discipline_cls')){
            if ($('.well_dis_id'+val+':checked').length == 0){
                $(this).closest('div').next('div').html('');
            }
            else{
                $('.check_val'+val+'').prop('checked',true)
            }
        }
        else{
            $(this).closest('div').next('div').html('');
        }
    }
})
//validation starts here//

$(document).on('click','#save_id',function(e){
    e.preventDefault()
    let count=0;
    $('select').each(function(){
        var val=$(this).find(':selected').val()
        if (val == ''){
            count ++;
            $(this).addClass('con_error')
        }
    })

    $("input:text").each(function(){
        var val=$(this).val()
        if (val == ''){
            count ++;
            $(this).addClass('con_error')
        }
    });
    let class_exist=$('.con_error').length
    if (count == 0 && class_exist == 0){
        $('#wccflowid')[0].submit()
    }
})

$(document).on('change','.con_error',function(){
    $(this).removeClass('con_error')
    
})

$(document).on('change','.user_cls',function(){
    let current_value=$(this).find(':selected').val();
    let get_parent=$(this).parent().parent()
    let duplicate_count=0;
    get_parent.children().each(function(index,val){
        let value=$(val).find('.user_cls').find(':selected').val()
        if (value){
            if (current_value == value){
                duplicate_count ++;
            }
        }
    })
    if (duplicate_count > 1){
        $(this).addClass('con_error')
    }
})
    $(document).on('click','.draft-cls',function(e){
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 0}).appendTo("form");
        $("#wccflowid").submit();
    })
});
//validation ends here//