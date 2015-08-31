/**
 * Created by ToothlessRebel on 8/30/2015.
 */

$(function () {
    var item_not_found = '';
    var item_dropdown = $('.item.dropdown');
    var lookup_fired = false;

    item_dropdown.dropdown({
        allowAdditions: true,
        onNoResults: function (searched_for) {
            item_not_found = searched_for;
        }
    });

    item_dropdown.on('change', function () {
        if (item_not_found.length > 0 && !lookup_fired) {
            item_dropdown.addClass('loading');
            lookup_fired = true;
            $.ajax({
                url: '/ajax/name_to_id/' + item_not_found
            }).always(function () {
                item_dropdown.removeClass('loading error');
                lookup_fired = false;
            }).success(function (response) {
                console.log(response);
                if (response.typeName === "bad item") {
                    item_dropdown.addClass('error');
                } else {
                    item_dropdown.find('input[name="item_id"]').val(response.typeID)
                }
            }).error(function () {
                item_dropdown.addClass('error');
            });
        }
    });
});
