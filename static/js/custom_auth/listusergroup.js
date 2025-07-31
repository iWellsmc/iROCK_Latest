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