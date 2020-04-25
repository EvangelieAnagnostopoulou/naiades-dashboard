/**
 * Created by dimitris on 25/5/2017.
 */
$(function() {
    $('form .form-group input:not([type="checkbox"]), form .form-group textarea')
        .addClass('form-control border-input');

    $('form select').select2();
});