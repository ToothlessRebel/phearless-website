/**
 * Created by ToothlessRebel on 8/30/2015.
 */

$(function () {
    var item_not_found = '';
    var $item_dropdown = $('.item.dropdown');
    var lookup_fired = false;
    var $quantity_input = $('.quantity.input');

    $item_dropdown.dropdown({
        allowAdditions: true,
        onNoResults: function (searched_for) {
            item_not_found = searched_for;
        }
    });

    $item_dropdown.on('change', function () {
        if (item_not_found.length > 0 && !lookup_fired) {
            $item_dropdown.addClass('loading');
            lookup_fired = true;
            $.ajax({
                url: '/ajax/name_to_id/' + item_not_found
            }).always(function () {
                $item_dropdown.removeClass('loading error');
                lookup_fired = false;
            }).success(function (response) {
                console.log(response);
                if (response.typeName === "bad item") {
                    $item_dropdown.addClass('error');
                } else {
                    $item_dropdown.find('input[name="item_id"]').val(response.typeID)
                }
            }).error(function () {
                $item_dropdown.addClass('error');
            });
        }
    });

    $quantity_input.on('keypress', function (event) {
        if (event.which == 13) {
            // AJAX the new entry and load the new table
            var $row = $(event.currentTarget).closest('.row');
            $row.dimmer('show');
            var item = $item_dropdown.find('input[name="item_id"]').val();
            var quantity = $quantity_input.find('input').val();
            var fleet = $('input[name="fleet"]').val();
            console.log('Item', item, 'Qty', quantity);
            $.ajax({
                url: '/ajax/add_drop_to_fleet/' + fleet + '/' + item + '/' + quantity
            }).always(function () {
                $row.dimmer('hide')
            }).success(function (response) {
                $item_dropdown.dropdown('clear');
                $item_dropdown.find('input').focus();
                $quantity_input.find('input').val('');
                // Load new table
                $('.loadable').html(response);
            }).fail(function (response) {
                console.log('Something went wrong!', response);
                $row.find('input').addClass('error');
            });
        }
    });
});
