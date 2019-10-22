$(function() {
    /* Enable datatable by default */
    $('.datatable').DataTable({
        initComplete: function() {
            $('.dataTables_filter, .dataTables_paginate')
                .parent()
                .css('text-align', 'right');
        }
    });
});