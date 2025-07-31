// $(document).on('change', 'input[type="checkbox"][name="Assign_Cost_Codeview"]', function() {
//    if($(this).closest('tr').find('input[type="checkbox"][name="Assign_Cost_Codecreate"]').is(':checked',true) || $(this).closest('tr').find('input[type="checkbox"][name="Assign_Cost_Codeedit"]').is(':checked',true)){
//     $(this).prop('checked',true)
//    }else{
//     $(this).prop('checked',false)
//    }
// })
$(document).on('change', 'input[type="checkbox"][name="Assign_Cost_Codecreate"],input[type="checkbox"][name="Assign_Cost_Codeedit"]', function() {
    $(this).closest('tr').find('input[type="checkbox"][name="Assign_Cost_Codeview"]').prop('checked',true)
})