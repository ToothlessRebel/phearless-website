/**
 * Created by ToothlessRebel on 8/30/2015.
 */

$(function () {
    var item_not_found = '';
    var $item_dropdown = $('.item.dropdown');
    var lookup_fired = false;
    var $quantity_input = $('.quantity.input');
    var $members_row = $('.loadable.members.row');
    var fleet_id = null;
    var $loot_table = $('.loadable.loot');
    loadFleets();

    $('.dropdown').dropdown();

    var selection = $('.default-character').val();
    $item_dropdown.dropdown({
        allowAdditions: true,
        onNoResults: function (searched_for) {
            item_not_found = searched_for;
        }
    });
    $('.character.dropdown').dropdown('set selected', selection);

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
            $.ajax({
                url: '/ajax/fleet/' + fleet + '/add_drop/' + item + '/' + quantity
            }).always(function () {
                $row.dimmer('hide')
            }).success(function () {
                $item_dropdown.dropdown('clear');
                $item_dropdown.find('input').focus();
                $quantity_input.find('input').val('');
                loadLootTable(fleet);
            }).fail(function (response) {
                console.log('Something went wrong!', response);
                $row.find('input').addClass('error');
            });
        }
    });

    $('.link.fleet.list').on('click', '.fleet.item', function () {
        var $this = $(this);
        fleet_id = $this.data('fleet_id');

        $this.closest('.list').find('.green.check.icon').remove();
        $this.append('<i class="ui green check icon"></i>');
        $('input[name="fleet"]').val(fleet_id);
        loadMembers();
    });

    $('.start.fleet.modal').modal({
            closable: false,
            onApprove: createAndSelectFleet
        });

    $('.fleet.list').on('click', '.start.fleet.button', function () {
        $('.start.fleet.modal').modal('show');
    });

    $loot_table.on('click', '.finalize.fleet.button', function () {
        console.log('Saving fleet ' + fleet_id + '.');
        $.ajax({
            url: '/ajax/fleet/' + fleet_id + '/finalize'
        }).fail(function (response) {
            console.log('Something went wrong!', response);
        });
        $members_row.empty();
        $loot_table.empty();
        loadFleets();
    });

    function loadLootTable(fleet_id) {
        fleet_id = fleet_id || 0;
        $.ajax({
            url: '/ajax/fleet/' + fleet_id + '/loot_table'
        }).success(function (response) {
            // Load new table
            $loot_table.html(response);
        }).fail(function (response) {
            console.log('Something went wrong!', response);
        });
    }

    function loadFleets(click_target) {
        click_target = click_target || null;
        $.ajax({
            url: '/ajax/fleets'
        }).success(function (response) {
            // Load the fleet list
            $('.loadable.fleet.list').html(response);
            if (click_target) {
                $('.fleet.item[data-fleet_id='+click_target+']').trigger('click');
            }
        }).fail(function (response) {
            console.log('Something went wrong!', response);
        });
    }

    function createAndSelectFleet(event) {
        var $modal = $(event).closest('.modal');
        var $modal_content = $modal.find('.content');
        var members = $modal_content.find('.character.dropdown').dropdown('get value');
        var $name_input = $modal_content.find('.name.input');
        var name = $name_input.val();
        if (! name.length > 0) {
            name = $name_input.find('input').attr('placeholder');
        }
        var type = $modal_content.find('.type.dropdown').dropdown('get value');
        var restriction = $modal_content.find('.restriction.dropdown').dropdown('get value');
        $.ajax({
            url: '/ajax/fleets/create',
            method: 'POST',
            dataType: 'json',
            data: {
                members: members,
                name: name,
                type: type,
                restriction: restriction
            }
        }).success(function (response) {
            loadFleets(response.fleet_id);
        }).fail(function (response) {
            console.log('Something went wrong!', response)
        });
    }

    function loadMembers() {
        $.ajax({
            url: '/ajax/fleet/' + fleet_id + '/member_icons'
        }).success(function (response) {
            $members_row.html(response);
            $('.add.member.dropdown').closest('.dropdown').dropdown({
                onChange: addMember
            });
            loadLootTable(fleet_id);
        }).fail(function (response) {
            console.log('Something went wrong!', response);
        });
    }

    function addMember(member_id) {
        console.log('Adding ' + member_id + ' to fleet.');
        $.ajax({
            url: '/ajax/fleet/' + fleet_id + '/add_member/' + member_id
        }).success(function (response) {
            console.log(response);
            loadFleets(response.fleet_id);
        }).fail(function (response) {
            console.log('Something went wrong!', response)
        });
    }
});
