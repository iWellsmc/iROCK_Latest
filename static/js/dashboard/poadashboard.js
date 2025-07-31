$(document).ready(function(){
    var country_wise_chart
    $.ajax({
        type:"GET",
        url:'/dashboard/getcountry_wise_project',
        data:{'is_poa':true},
        success: function(data){
            country_wise_chart=Highcharts.chart('country_wise_projects', {
                chart: {
                    height: '100%'
                },
                series: [{
                    type: 'sunburst',
                    data: data,
                    allowDrillToNode: true
                }],
                title: {
                    text: 'Projects per Country'
                }
            });
          
        }
    })

});
