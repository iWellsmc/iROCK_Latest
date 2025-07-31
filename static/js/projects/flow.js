$(document).ready(function(){
    $(document).on("change",".level_type_id", function(){   
        var level_type=$(this).attr('data_level')
        var level_id=$(this).attr('data_id')
        let that=$(this)
        let sub_level=$(this).attr('sub_level') || ''
        let check_val=$(this).attr('check_val') || ''
        if($(this).prop('checked')==true){
            $.ajax({
                type: "GET",
                url:"/projectflow/getprocess_byflow",
                data: {
                    "flow_id":flow,
                },
                cache: false,
                success: function(data)
                {

                    html=''
                    data.process.forEach(element => {
                        html +='<div class="row">'
                            html +='<div class="col-3 process-name">'
                                html +='<p>'+element.process_name+'</p>'
                            html +='</div>'
                            html +='<div class="col-9">'
                                html +='<div class="row">'
                                if (sub_level){
                                    html +='<div class="col-2 mt-2 mb-2 input-center">'
                                    html +='<input type="text" name="wellbased_type_stations_'+level_id+'_'+element.id+'" class="form-control no_of_stations" data_id='+level_id+' data_level='+level_type+' sub_level='+sub_level+'><input type="hidden" name="wellbased_type_process_id_'+level_id+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                    html +='<input type="hidden" name="wellbased_type_originalprocess_id_'+level_id+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                }
                                else{
                                    html +='<div class="col-2 mt-2 mb-2 input-center">'
                                    html +='<input type="text" name="stations_'+level_id+'_'+element.id+'" class="form-control no_of_stations" data_id='+level_id+' data_level='+level_type+'><input type="hidden" name="process_id_'+level_id+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                    html +='<input type="hidden" name="originalprocess_id_'+level_id+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                }
                                    html +='</div>'
                                    html +='<div class="col-10">'
                                        html +='<div class="row">'
                                        if (sub_level){
                                            html +='<div class="col-12  wellbased_type_module_'+level_id+'_'+element.id+'">'
                                        }
                                        else{
                                            html +='<div class="col-12  module_'+level_id+'_'+element.id+'">'
                                        }
                                            html +='</div>'
                                        html +='</div>'
                                    html +='</div>'
                                html +='</div>'
                                
                            html +='</div>'
                        html +='</div>'
                    });
                    if (sub_level){
                        $('.wellbased_type_process_'+level_type+'_'+level_id).html(html)
                    }
                    else{
                        $('.process_'+level_type+'_'+level_id).html(html)
                    }

                if (check_val){
                    if ($('.well_dis_id'+check_val+':checked').length > 0){
                        if ($('.check_val'+check_val+'').is(':checked') ==  false){
                            $('.check_val'+check_val+'').prop('checked',true)
                            html=''
                            data.process.forEach(element => {
                                html +='<div class="row">'
                                    html +='<div class="col-3 process-name">'
                                        html +='<p>'+element.process_name+'</p>'
                                    html +='</div>'
                                    html +='<div class="col-9">'
                                        html +='<div class="row">'
                                            html +='<div class="col-2 mt-2 input-center">'
                                                html +='<input type="text" name="wellbased_type_stations_'+check_val+'_'+element.id+'" class="form-control no_of_stations" data_id='+check_val+' sub_level="discipline" data_level='+level_type+' get_process='+element.process_id+'><input type="hidden" name="wellbased_type_process_id_'+check_val+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                                html +='<input type="hidden" name="wellbased_type_originalprocess_id_'+check_val+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                            html +='</div>'
                                            html +='<div class="col-10">'
                                                html +='<div class="row">'
                                                html +='<div class="col-12 wellbased_type_module_'+check_val+'_'+element.id+'">'
                                                    html +='</div>'
                                                html +='</div>'
                                            html +='</div>'
                                        html +='</div>'
                                    html +='</div>'
                                html +='</div>'
                            });
                            $('.check_val'+check_val+'').closest('div').next('div').append(html);
                        }
                    }
                }
                }
            })

        }else{
            if (sub_level){
                if ($('.well_dis_id'+level_id+':checked').length > 0){
                    $('.check_val'+level_id+'').prop('checked',true)
                }
                else{
                    $('.wellbased_type_process_'+level_type+'_'+level_id).html('')

                }
            }
            else{
                $('.process_'+level_type+'_'+level_id).html('')
                // console.log('ad',$('.well_dis_id'+check_val+':checked').length)
                if ($('.well_dis_id'+check_val+':checked').length == 0){
                    $('.check_val'+check_val+'').prop('checked',false)
                    $('.wellbased_type_process_'+level_type+'_'+check_val).html('')
                }
            }
        }
    })
    $(document).on("keyup",".no_of_stations", function(){   
        var no_of_stations=$(this).val();
        var level_type=$(this).attr('data_level')
        var level_id=$(this).attr('data_id')
        var process_id=$(this).closest('div').find('.process_id').val();
        var originalprocess_id=$(this).closest('div').find('.originalprocess_id').val();
        let sub_level=$(this).attr('sub_level') || ''
        let that=$(this)
        // console.log("process_id"+process_id)
        // console.log("level_type"+level_type)
        // console.log("level_id"+level_id)
        if(no_of_stations){
            $.ajax({
                type: "GET",
                url:"/projectflow/getmodule_byprocess",
                data: {
                    "process_id":originalprocess_id,
                },
                cache: false,
                success: function(data)
                {
                    console.log(data.modules)
                    console.log("level_id"+level_id)
                    console.log("process_id"+process_id)
                    
                    var modulerow=''
                     if (sub_level){
                        for(var i=0;i<no_of_stations;i++){
                            modulerow +="<div class='justify-content-end mt-2 mb-2 row module_row_"+level_id+"_"+process_id+"_"+i+"'>"
                                modulerow +="<div class='col-3 modules'>"
                                    modulerow +='<select class="form-control modules" name="wellbased_type_module_'+level_id+'_'+process_id+'_'+i+'" process_id='+process_id+' data_id='+level_id+' module_index='+i+' sub_level='+sub_level+'>'
                                        modulerow +='<option value="">--Select--</option>'
                                        data.modules.forEach(element => {
                                            modulerow +='<option value='+element.id+' data-module_id='+element.module_id+'>'+element.module_name+'</option>'
                                        })
                                    modulerow +='</select>'
                                modulerow +="</div>"
                                modulerow +="<div class='col-2 nos-users wellbased_type_module_row_"+level_id+"_"+process_id+"_"+i+"_noof_users'>"
                                modulerow +="</div>"
                                modulerow +="<div class='col-6'>"
                                    modulerow +="<div class='row justify-content-end'>"
                                        modulerow +="<div class='col-4 roles-data wellbased_type_module_row_"+level_id+"_"+process_id+"_"+i+"_roles'>"
                                        modulerow +="</div>"
                                        modulerow +="<div class='col-8 users-data wellbased_type_module_row_"+level_id+"_"+process_id+"_"+i+"_station_users'>"
                                        modulerow +="</div>"
                                    modulerow +="</div>"
                                modulerow +="</div>"
                            modulerow +="</div>"
                        }
                        $('.wellbased_type_module_'+level_id+'_'+process_id).html(modulerow)
                    }
                    else{
                        for(var i=0;i<no_of_stations;i++){
                            modulerow +="<div class='justify-content-end mt-2 mb-2 row module_row_"+level_id+"_"+process_id+"_"+i+"'>"
                                modulerow +="<div class='col-3 modules'>"
                                    modulerow +='<select class="form-control modules" name="module_'+level_id+'_'+process_id+'_'+i+'" process_id='+process_id+' data_id='+level_id+' module_index='+i+'>'
                                        modulerow +='<option value="">--Select--</option>'
                                        data.modules.forEach(element => {
                                            modulerow +='<option value='+element.id+' data-module_id='+element.module_id+'>'+element.module_name+'</option>'
                                        })
                                    modulerow +='</select>'
                                modulerow +="</div>"
                                modulerow +="<div class='col-2 nos-users module_row_"+level_id+"_"+process_id+"_"+i+"_noof_users'>"
                                modulerow +="</div>"
                                modulerow +="<div class='col-6'>"
                                    modulerow +="<div class='row justify-content-end'>"
                                        modulerow +="<div class='col-4 roles-data module_row_"+level_id+"_"+process_id+"_"+i+"_roles'>"
                                        modulerow +="</div>"
                                        modulerow +="<div class='col-8 users-data module_row_"+level_id+"_"+process_id+"_"+i+"_station_users'>"
                                        modulerow +="</div>"
                                    modulerow +="</div>"
                                modulerow +="</div>"
                            modulerow +="</div>"
                        }
                        $('.module_'+level_id+'_'+process_id).html(modulerow)
                    }
                }
            })

        }
    })

    $(document).on("change",".modules", function(){   
        var process_module_id=$(this).find(':selected').val()
        var process_id=$(this).attr('process_id')
        var level_id=$(this).attr('data_id')
        var module_id=$('option:selected', this).data('module_id');
        var module_index=$(this).attr('module_index')
        let sub_level=$(this).attr('sub_level') || ''
        if($(this).val()){
            var html=''
            if (module_id == '5'){
                $.ajax({
                    type: "GET",
                    url:"/projectflow/get_signatories",
                    data: {
                        "project_id":project_id,
                        "module_id":module_id,
                        "projectname":projectname
                    },
                    cache: false,
                    success: function(data)
                    {
                        console.log(data)
                        user_count=data.users_list.length
                        html +='<input type="text" readonly class="form-control" value='+user_count+'>'
                        $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_noof_users').html(html)
                        var roles=JSON.parse(data.roles_data)
                        var roles_dropdown=''
                        if (sub_level){
                            roles_dropdown +='<select class="form-control" name="wellbased_type_role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                        }
                        else{
                            roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                        }
                        roles_dropdown +='<option value="">--Select--</option>'
                        roles.forEach(element => {
                            roles_dropdown +='<option value='+element.pk+'>'+element.fields.role_name+'</option>'
                        })
                        roles_dropdown +='</select>'
                        $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)
                        let users=''
                        data.users_list.forEach(element => {
                            users +='<input type="text" readonly class="form-control" value="'+element.user__name+' '+element.user__lastname+' '+element.signatory__currency__currency_symbol+'"><br>'
                        })
                        $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(users)
                    }})
            }
            else{
                if (sub_level){
                    html +='<input type="text" name="wellbased_type_nouser_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'" class="form-control nousers" module_id='+module_id+' data_id='+level_id+' process_id='+process_id+' process_module_id='+process_module_id+' module_index='+module_index+' sub_level='+sub_level+'>'
                    $('.wellbased_type_module_row_'+level_id+'_'+process_id+'_'+module_index+'_noof_users').html(html)
                    $('.wellbased_type_module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(' ')
                    $('.wellbased_type_module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(' ')
                }
                else{
                    html +='<input type="text" name="nouser_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'" class="form-control nousers" module_id='+module_id+' data_id='+level_id+' process_id='+process_id+' process_module_id='+process_module_id+' module_index='+module_index+'>'
                    $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_noof_users').html(html)
                    $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(' ')
                    $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(' ')
                }
            }
        }
    })

    $(document).on("change",".nousers", function(){   
        var no_users=$(this).val()
        // console.log(no_users)
        var module_id=$(this).attr('module_id')
        var level_id=$(this).attr('data_id')
        var process_id=$(this).attr('process_id')
        var module_index=$(this).attr('module_index')
        var process_module_id=$(this).attr('process_module_id')
        let sub_level=$(this).attr('sub_level') || ''

        $.ajax({
            type: "GET",
            url:"/projectflow/getroles_and_projectusers",
            data: {
                "project_id":project_id,
                "module_id":module_id
            },
            cache: false,
            success: function(data)
            {
                // console.log(data)
                var project_users=data.projectusers_data
                var roles=JSON.parse(data.roles_data)
                console.log(project_users)
                var roles_dropdown=''
                if (sub_level){
                    roles_dropdown +='<select class="form-control" name="wellbased_type_role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                }
                else{
                    roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                }
                roles_dropdown +='<option value="">--Select--</option>'
                roles.forEach(element => {
                    roles_dropdown +='<option value='+element.pk+'>'+element.fields.role_name+'</option>'
                })
                roles_dropdown +='</select>'
                if (sub_level){
                    $('.wellbased_type_module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)
                    var user_dropdown=''
                    for(var i=1;i<=no_users;i++){
                        // console.log(i)

                        user_dropdown +='<select class="form-control user_cls" name="wellbased_type_moduleusers_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                        user_dropdown +='<option value="">--Select--</option>'
                        project_users.forEach(element => {
                            user_dropdown +='<option value='+element.id+'>'+element.user_name+' '+element.user_lastname+'-'+element.user_designation_role+'</option>'
                        })
                        user_dropdown +='</select>'
                    }
                    $('.wellbased_type_module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(user_dropdown)
                }
                else{
                    $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)

                    var user_dropdown=''
                    for(var i=1;i<=no_users;i++){
                        user_dropdown +='<select class="form-control user_cls" name="moduleusers_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                        user_dropdown +='<option value="">--Select--</option>'
                        project_users.forEach(element => {
                            user_dropdown +='<option value='+element.id+'>'+element.user_name+' '+element.user_lastname+'-'+element.user_designation_role+'</option>'
                        })
                        user_dropdown +='</select>'
                    }
                    $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(user_dropdown)
                }
                
            }
        })
})
})

$(document).on('change','.user_cls',function(){
    let current_value=$(this).find(':selected').val();
    let get_parent=$(this).parent()
    let duplicate_count=0;
    get_parent.children().each(function(index,val){
        let value=$(val).find(':selected').val()
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

$('#save_id').click(function(e){
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
    $("checkbox").each(function(){
            $(this).removeClass('con_error')
    });
    let class_exist=$('.con_error').length
    if (count == 0 && class_exist == 0){
        $('#wccflowid')[0].submit()
    }
})

$(document).on('change','.con_error',function(){
    $(this).removeClass('con_error')
    
})

$(document).ready(function () {
     
    $('.Sav1').prop('disabled', true);
  
     
    $('.level_type_id').on('change', function () {
    if($('.level_type_id:checked').length == 0){
      $('.level_type_id').each(function () {
        if (!$(this).prop('checked')) {
             $(this).addClass('con_error');
             $(this).next('label').addClass('con_error');
          } else {
             $(this).removeClass('con_error');
             $(this).next('label').removeClass('con_error');
          }
      });
    }
  
     
      $('.Sav1').prop('disabled', $('.level_type_id:checked').length === 0);
    });
  });

 