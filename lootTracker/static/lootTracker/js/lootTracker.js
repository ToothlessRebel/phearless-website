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
            // Hit up Fuzzworks to get the ID.
            lookup_fired = true;
            $.ajax({
                url: 'https://www.fuzzwork.co.uk/api/typeid.php',
                data: {
                    typename: item_not_found
                }
            }).always(function () {
                lookup_fired = false;
            }).success(function (response) {
                console.log(response);
                
            }).error(function () {
                // @todo
            });
        }
    });
});
