$(document).ready(function(){
    $(document).on("change",".check_well_dis", function(){   
        var level_type=$(this).attr('data_level')
        var level_id=$(this).attr('data_id')
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
                                    html +='<div class="col-2 mt-2 input-center">'
                                        html +='<input type="text" name="stations_'+level_id+'_'+element.id+'" class="form-control no_of_stations" data_id='+level_id+' data_level='+level_type+' get_process='+element.process_id+'><input type="hidden" name="process_id_'+level_id+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                        html +='<input type="hidden" name="originalprocess_id_'+level_id+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                    html +='</div>'
                                    html +='<div class="col-10">'
                                        html +='<div class="row">'
                                            html +='<div class="col-12  module_'+level_id+'_'+element.id+'">'
                                            html +='</div>'
                                        html +='</div>'
                                    html +='</div>'
                                html +='</div>'
                            html +='</div>'
                        html +='</div>'
                    });
                    $('.process_'+level_type+'_'+level_id).append(html)
                    //check below code
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
                                                    html +='<input type="text" name="stations_'+check_val+'_'+element.id+'" class="form-control no_of_stations" data_id='+check_val+' data_level='+level_type+' get_process='+element.process_id+'><input type="hidden" name="process_id_'+check_val+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                                    html +='<input type="hidden" name="originalprocess_id_'+check_val+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                                html +='</div>'
                                                html +='<div class="col-10">'
                                                    html +='<div class="row">'
                                                        html +='<div class="col-12  module_'+check_val+'_'+element.id+'">'
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
            if ($('.well_dis_id'+check_val+':checked').length == 0){
                $('.check_val'+check_val+'').prop('checked',false)
                $('.check_val'+check_val+'').closest('div').next('div').html(' ');
            }
            $('.process_'+level_type+'_'+level_id).html('')
        }
    })

    $(document).on("change",".well_discipline_cls", function(){  
        var level_type=$(this).attr('data_level')
        var level_id=$(this).attr('data_id')
        let sub_level=$(this).attr('sub_level') || ''
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
                                    html +='<div class="col-2 mt-2 input-center">'
                                        html +='<input type="text" name="stations_'+level_id+'_'+element.id+'" class="form-control no_of_stations" data_id='+level_id+' data_level='+level_type+' get_process='+element.process_id+'><input type="hidden" name="process_id_'+level_id+'_'+element.id+'" class="process_id" value='+element.id+'>'
                                        html +='<input type="hidden" name="originalprocess_id_'+level_id+'_'+element.id+'" class="originalprocess_id" value='+element.process_id+'>'
                                    html +='</div>'
                                    html +='<div class="col-10">'
                                        html +='<div class="row">'
                                            html +='<div class="col-12  module_'+level_id+'_'+element.id+'">'
                                            html +='</div>'
                                        html +='</div>'
                                    html +='</div>'
                                html +='</div>'
                            html +='</div>'
                        html +='</div>'
                    });
                    $('.process_'+level_type+'_'+level_id+'_well_dis').append(html)
                }
            })
        }else{
            if ($('.well_dis_id'+level_id+':checked').length == 0){
                $('.check_val'+level_id+'').prop('checked',false)
                $('.process_'+level_type+'_'+level_id+'_well_dis').html('')
            }
            else{
                $('.check_val'+level_id+'').prop('checked',true)
            }
        }
    })

    $(document).on("keyup",".no_of_stations", function(){    
        let count_row=$(this).closest('div').next().find('.module_count').length
        var no_of_stations=$(this).val();
        var level_id=$(this).attr('data_id')
        var level_type=$(this).attr('data_level')
        var process_id=$(this).closest('div').find('.process_id').val();
        var originalprocess_id=$(this).closest('div').find('.originalprocess_id').val();
        var page_type=$('#page_type').val();
        var get_process=$(this).attr('get_process')
        console.log("originalprocess_id"+originalprocess_id)
        let current=$(this)
        console.log(no_of_stations)
        if(no_of_stations){
            $.ajax({
                type: "GET",
                url:"/projectflow/checkprojectflow_level",
                data: {
                    "level_id":level_id,
                    "level_type":level_type,
                    'project_id':project_id,
                    'process_id':originalprocess_id,
                    'get_process':get_process
                },
                cache: false,
                success: function(data)
                {
                    if(data.status==true){
                        var projectleveldata = JSON.parse(data.projectflow_level);
                        if(projectleveldata.no_of_stations>no_of_stations){
                            Swal.fire({
                                title: 'Are you sure you want to delete',
                                showCancelButton: true,
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'Yes, I Confirm',
                                cancelButtonText: 'No',
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    $.ajax({
                                    type: "GET",
                                    url:'/projectflow/delete_level',
                                    data: {
                                    "level_id":level_id,
                                    "project_id":project_id,
                                    "level_type":level_type,
                                    },
                                    success: function(del_data)
                                    {
                                        $('.module_'+level_id+'_'+process_id).html(' ')
                                        // current.val('')
                                        start=0
                                        end=no_of_stations-1
                                        addmodule(process_id,level_id,start,end,data.modules,page_type)
                                        

                                    }
                                    });
                                // Swal.fire(projectname,'Deleted Successfully')
                                }
                            })
                        }
                        else{
                            console.log('else')
                            var remaining_count=no_of_stations-1
                            console.log(no_of_stations,projectleveldata.no_of_stations,remaining_count)
                            start=0
                            end=remaining_count
                            console.log({'start':start,'end':end})
                            if( start <= end){
                                addmodule(process_id,level_id,start,end,data.modules,page_type)
                            }
                            else{
                                deletemodule(end,start,current)
                                console.log('lowwww')
                            }

                        }
                    }
                    else{
                        $('.module_'+level_id+'_'+process_id).html(' ')
                        console.log('eeee')
                        start=0
                        end=no_of_stations-1
                        addmodule(process_id,level_id,start,end,data.modules)
                    }
                }
            })
        }
    })



    $(document).on("change",".modules_select", function(){   
        var process_module_id=$(this).val()
        var process_id=$(this).attr('process_id')
        var level_id=$(this).attr('data_id')
        var module_id=$('option:selected', this).data('module_id');
        var module_index=$(this).attr('module_index');
        // validation pending
        // let get_index=$(this).index('.modules_'+level_id+'_'+process_id)
        // let minus_index=get_index - 1
        // console.log(minus_index)
        // console.log($(".modules_select:eq("+get_index+")"))

        if($(this).val()){
            // console.log('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_noof_users')
            // console.log(project_id,'sad',module_id)
            // $.ajax({
            //     type: "GET",
            //     url:"/projectflow/getroles_and_projectusers",
            //     data: {
            //         "project_id":project_id,
            //         "module_id":module_id
            //     },
            //     cache: false,
            //     success: function(data)
            //     {
            //         var project_users=data.projectusers_data
            //         var roles=JSON.parse(data.roles_data)
    
            //         var roles_dropdown=''
            //         roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
            //         roles_dropdown +='<option value="">--Select--</option>'
            //         roles.forEach(element => {
            //             roles_dropdown +='<option value='+element.pk+'>'+element.fields.role_name+'</option>'
            //         })
            //         roles_dropdown +='</select>'
            //         $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)
            //     }
            // })
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
                        roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
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
                    },
                })
            }
            else{
                html +='<input type="text" name="nouser_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'" class="form-control nousers" module_id='+module_id+' data_id='+level_id+' process_id='+process_id+' process_module_id='+process_module_id+' module_index='+module_index+'>'
                $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_noof_users').html(html)
                $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(' ')
                $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(' ')
            }
        }
    })

    $(document).on("change",".nousers", function(){ 
        let old_data=$(this).attr('old_data') || ''
        let val=Number($(this).val()) || 0; 
        var no_users=$(this).val()
        // console.log(no_users)
        var module_id=$(this).attr('module_id')
        var level_id=$(this).attr('data_id')
        var process_id=$(this).attr('process_id')
        var module_index=$(this).attr('module_index')
        // console.log("module_index"+module_index)
        // console.log("level_id"+level_id)
        // console.log("process_id"+process_id)
        var process_module_id=$(this).attr('process_module_id')
        let that=$(this)
        if (old_data){
            if (val > Number(old_data)){
                let myDiv = $(this).parent('div').parent('div').find('.users-data');
                myDiv.find('.mod_usr_cls').each(function(index,value) {
                    let count=index+1
                    if (count > Number(old_data)){
                        $(value).remove()
                    }
                })
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
                        
                        var project_users=data.projectusers_data
                        var user_dropdown=''
                        for (let i = Number(old_data); i < val; i++) {
                                user_dropdown +='<select class="form-control mod_usr_cls" name="moduleusers_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                                user_dropdown +='<option value="">--Select--</option>'
                                project_users.forEach(element => {user_dropdown +='<option value='+element.id+'>'+element.user_name+' '+element.user_lastname+'-'+element.user_designation_role+'</option>'})
                                user_dropdown +='</select>'
                        };
                        that.parent('div').parent('div').find('.users-data').append(user_dropdown);
                    },})
                
            }
            else if (val == Number(old_data)){
                let myDiv = $(this).parent('div').parent('div').find('.users-data');
                myDiv.find('.mod_usr_cls').each(function(index,value) {
                    let count=index+1
                    if (count > Number(old_data)){
                        $(value).remove()
                    }
                })
            }
            else{
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
                        var project_users=data.projectusers_data
                        var roles=JSON.parse(data.roles_data)
        
                        var roles_dropdown=''
                        roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                        roles_dropdown +='<option value="">--Select--</option>'
                        roles.forEach(element => {
                            roles_dropdown +='<option value='+element.pk+'>'+element.fields.role_name+'</option>'
                        })
                        roles_dropdown +='</select>'
                        $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)
        
        
                        var user_dropdown=''
                        for(var i=1;i<=no_users;i++){
                            // console.log(i)
        
                            user_dropdown +='<select class="form-control" name="moduleusers_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                            user_dropdown +='<option value="">--Select--</option>'
                            project_users.forEach(element => {
                                user_dropdown +='<option value='+element.id+'>'+element.user_name+' '+element.user_lastname+'-'+element.user_designation_role+'</option>'
                            })
                            user_dropdown +='</select>'
                        }
        
                        console.log('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users')
                        $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(user_dropdown) 
                    }
                })
            }
        }
        else{
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
                var project_users=data.projectusers_data
                var roles=JSON.parse(data.roles_data)

                var roles_dropdown=''
                roles_dropdown +='<select class="form-control" name="role_id_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                roles_dropdown +='<option value="">--Select--</option>'
                roles.forEach(element => {
                    roles_dropdown +='<option value='+element.pk+'>'+element.fields.role_name+'</option>'
                })
                roles_dropdown +='</select>'
                $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_roles').html(roles_dropdown)


                var user_dropdown=''
                for(var i=1;i<=no_users;i++){
                    // console.log(i)

                    user_dropdown +='<select class="form-control" name="moduleusers_'+level_id+'_'+process_id+'_'+process_module_id+'_'+module_index+'">'
                    user_dropdown +='<option value="">--Select--</option>'
                    project_users.forEach(element => {
                        user_dropdown +='<option value='+element.id+'>'+element.user_name+' '+element.user_lastname+'-'+element.user_designation_role+'</option>'
                    })
                    user_dropdown +='</select>'
                }

                console.log(user_dropdown)


                $('.module_row_'+level_id+'_'+process_id+'_'+module_index+'_station_users').html(user_dropdown)



                
            }
        })

        }
        
    })

})

function addmodule(process_id,level_id,start,end,modules,page_type=''){
    var moduledivCount = $('.module_'+level_id+'_'+process_id+' .module_rows').length;

    var modulerow=''
    // if(page_type=='edit'){
    //     modulerow +='<input type="hidden" name="projectflowmodule_id_'+level_id+'_'+process_id+'_'+moduledivCount+'" value="">'
    // }
    let count=0;
    console.log('moduledivCount',moduledivCount)
    for(var i=start;i<=end;i++){
        if(page_type=='edit'){
            modulerow +='<input type="hidden" name="projectflowmodule_id_'+level_id+'_'+process_id+'_'+i+'" value="" class="project_flow_module_s">'
            
        }
        modulerow +="<div class=' justify-content-end mt-2 row row_variant  module_row_"+level_id+"_"+process_id+"_"+i+"'>"
            modulerow +="<div class='col-3 modules'>"
                modulerow +='<select class="form-control modules_select'+level_id+'_'+process_id+' module_count modules_select" name="module_'+level_id+'_'+process_id+'_'+i+'" process_id='+process_id+' data_id='+level_id+' module_index='+i+'>'
                    modulerow +='<option value="">--Select--</option>'
                    modules.forEach(element => {
                        modulerow +='<option value='+element.id+' data-module_id='+element.module_id+'>'+element.module_name+'</option>'
                    })
                modulerow +='</select>'
            modulerow +="</div>"
            modulerow +="<div class='nos-users col-2 module_row_"+level_id+"_"+process_id+"_"+i+"_noof_users'>"
            modulerow +="</div>"
            modulerow +="<div class='col-6'>"
                modulerow +="<div class='row justify-content-end'>"
                    modulerow +="<div class='roles-data col-4 module_row_"+level_id+"_"+process_id+"_"+i+"_roles'>"
                    modulerow +="</div>"
                    modulerow +="<div class='users-data col-8 module_row_"+level_id+"_"+process_id+"_"+i+"_station_users'>"
                    modulerow +="</div>"
                modulerow +="</div>"
            modulerow +="</div>"
        modulerow +="</div>"
        moduledivCount ++;
    }
    $('.module_'+level_id+'_'+process_id).append(modulerow)
}


function deletemodule(end,start,current){
    // console.log('current',current)
    let current_row=current.closest('div').next().find('.row_variant')
    let hidden_row=current.closest('div').next().find('.project_flow_module_s')
    // console.log('current_row',current_row)
    // console.log({'start':start,'end':end})
    for(var i=start;i>end+1;i--){
        var divToRemove = $(current_row[i-1]);
        divToRemove.remove();
        var del_hiddenrow =$(hidden_row[i-1]);
        del_hiddenrow.remove();
        // current_row.pop();
    }
    // console.log('current_row',current_row)
    // console.log('start',start)
    // console.log('end',end)
}

$(document).on("change",".mod_usr_cls", function(){ 
    let selected_val=$(this).find(':selected').val() || '';
    let get_parent_div=$(this).parent('div');
    let count=0;
    if (selected_val){
        get_parent_div.find('.mod_usr_cls').each(function(index,value) {
            let val=$(value).find(':selected').val();
            if (selected_val == val){
                count ++;
            }
        })
        if (count > 1){
            $(this).addClass('con_error')
        }
        else{
            $(this).removeClass('con_error')
        }
    }

})
