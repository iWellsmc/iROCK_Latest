
// when search box is empty then remove search query string from url
$('input').on('change', function () {
    const queryString = window.location.search;
    const parameters = new URLSearchParams(queryString);
    const value = parameters.get('q');
    if (value != null && $(this).val() == '') {
        window.location.href = `scheme://gethost/invoiceguard/listprocess/`
    }
});



$(document).on('input', "#myInput", function () {
    let query = $(this).val()
    let pageperdata = $('#datafilters').val()
    setTimeout(function () {
        searchProcess(query,1,pageperdata)
    }, 100);
});


$(document).on('click','.pg-circle',function(e){
    e.preventDefault();
    let query = $('#myInput').val();
    let page = $(this).attr('data-id')
    let pageperdata = $('#datafilters').val()
    searchProcess(query,page,pageperdata)
})

$(document).on('change','#datafilters',function(e){
    let query = $('#myInput').val();
    let pageperdata = $('#datafilters').val()
    searchProcess(query,1,pageperdata)
});

function searchProcess(query,page,pageperdata) {
   $.ajax({
        url: "/projects/userlist",
        headers: { 'X-CSRFToken': csrf_token },
        data: {
            'q': query,
            'page':page,
            'pageperdata':pageperdata
        },
        type: 'POST',
        success: function (response) {
            if (response.status) {
                console.log('right')
                console.log(response)
                $('section').replaceWith(response.html)
                let focusElement = $(document).find('#myInput')
                let elementLength = focusElement.val().length;
                focusElement[0].focus();
                focusElement[0].setSelectionRange(elementLength,elementLength);
                $('#datafilters').val($('.entries').val())
            } else {
                console.log('wrong')
            }
        },
        error: function () {
            // Error message
        }
    });
}
$(document).ready(function() {
    $('.filter-btn').click(function() {
        var table = $(this).closest('table');
        var rows = table.find('tbody > tr').get();
        var idx = $(this).closest('th').index();
        var filter = $(this).data('filter');
        var icon = $(this).find('i');

        // Remove active class from other filter buttons
        $('.filter-btn').not(this).removeClass('active');

        // Toggle active class for the clicked filter button
        $(this).toggleClass('active');

        rows.sort(function(a, b) {
            var A, B;

            switch (filter) {
                case 'Sno':
                    A = $(a).children('td').eq(0).text().toUpperCase();
                    B = $(b).children('td').eq(0).text().toUpperCase();
                    break;
                case 'first-name':
                    A = $(a).children('td').eq(1).text().toUpperCase();
                    B = $(b).children('td').eq(1).text().toUpperCase();
                    break;
                case 'last-name':
                    A = $(a).children('td').eq(2).text().toUpperCase();
                    B = $(b).children('td').eq(2).text().toUpperCase();
                    break;
                case 'designation':
                    A = $(a).children('td').eq(3).text().toUpperCase();
                    B = $(b).children('td').eq(3).text().toUpperCase();
                    break;
                case 'dept':
                    A = $(a).children('td').eq(4).text().toUpperCase();
                    B = $(b).children('td').eq(4).text().toUpperCase();
                    break;
                case 'group':
                    A = $(a).children('td').eq(6).text().toUpperCase();
                    B = $(b).children('td').eq(6).text().toUpperCase();
                    break;
                case 'email':
                    A = $(a).children('td').eq(6).text().toUpperCase();
                    B = $(b).children('td').eq(6).text().toUpperCase();
                    break;
                case 'mobile':
                    A = $(a).children('td').eq(7).text().toUpperCase();
                    B = $(b).children('td').eq(7).text().toUpperCase();
                    break;
                default:
                    break;
            }

            // Determine sorting order based on the presence of 'fa-sort-up' or 'fa-sort-down' class
            if (icon.hasClass('fa-sort-up')) {
                return (A < B) ? 1 : -1;
            } else {
                return (A > B) ? 1 : -1;
            }
        });

        $.each(rows, function(index, row) {
            table.children('tbody').append(row);
        });

        // Toggle between 'fa-sort-up' and 'fa-sort-down' classes for the icon
        icon.toggleClass('fa-sort-up fa-sort-down');
        $(this).closest('th').siblings().find('i').removeClass('fa-sort-up fa-sort-down').addClass('fa-sort');
    });
});