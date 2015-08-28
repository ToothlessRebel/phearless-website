/**
 * Created by ToothlessRebel on 8/25/2015.
 */

$(function () {
    var login = {};
    login.username = false;
    login.api = false;
    login.parse = false;

    $('.help.icon').popup({
        inline: true,
        hoverable: true,
        position: 'top center'
    });

    $('.choose-username').on('change', function () {
        var $this = $(this);
        var $input = $this.closest('.input');
        var $icon = $this.siblings('i');

        $input.addClass('loading');

        $this.popup('hide');

        $.ajax({
            url: '/ajax/username_exists/' + $this.val()
        }).always(function () {
            $input.removeClass('loading');
        }).success(function (response) {
            if (response.result === false) {
                $icon.replaceWith('<i class="ui small green circular check icon"></i>');
                $input.popup('destroy');
                login.username = true;
                checkForm();
            } else {
                $icon.replaceWith('<i class="ui small red circular remove icon"></i>');
                $input.popup({
                    popup: '.popup.username-exists',
                    position: 'right center'
                }).show();
            }
        }).fail(function () {
            console.log('Failed to check username.');
        });
    });

    $('.api-field.key, .api-field.vcode').on('change', function () {
        var $api_fields = $('.api-field');
        var $key_field = $('.api-field.key');
        var $code_field = $('.api-field.vcode');
        var $inputs = $api_fields.closest('.input');
        var $icons = $api_fields.siblings('i');

        var key = $key_field.val();
        var vcode = $code_field.val();

        if ($key_field.val().length > 0 && $code_field.val().length > 0) {
            // Send EVE API Check.
            $inputs.addClass('loading');
            $.ajax({
                url: 'https://api.eveonline.com/account/APIKeyInfo.xml.aspx?keyID=' + key + '&vCode=' + vcode,
                dataType: 'text'
            }).always(function () {
                $inputs.removeClass('loading red remove');
                $icons.popup('destroy');
            }).success(function (response) {
                login.api = true;
                parse_api(response);
                checkForm();
                //console.log('win', response);
                $icons.removeClass('help remove').addClass('green check');
            }).fail(function (response) {
                $inputs.popup({
                    popup: '.popup.api-invalid',
                    position: 'right center'
                });
                //console.log('fail', response.responseText);
                $icons.removeClass('help').addClass('red remove');
            });
        }
    });

    $('.button.sign-up').closest('div').popup({
        inline: true,
        position: 'top center'
    });

    $('.password').on('change', function () {
        checkForm();
    });

    function parse_api(api_data) {
        $('.button.sign-up').addClass('loading');
        $.ajax({
            url: '/ajax/parse_api/',
            method: 'POST',
            data: {
                api: api_data
            }
        }).always(function () {
            $('.button.sign-up').removeClass('loading');
        }).success(function (response) {
            console.log('success', response);
            if (response.result === 'success') {
                console.log('allow button');
                login.parse = true;
                checkForm();
            }
        }).fail(function () {
            $('.error.message.api-parse-fail').removeClass('hidden');
        });
    }

    function checkForm() {
        var $all_inputs = $('.signup-form input');
        var $button = $('.button.sign-up');
        var complete = true;

        $all_inputs.each(function () {
            if ($(this).val().length < 1) {
                complete = false;
            }
        });

        if (complete && login.username === true && login.api === true && login.parse === true) {
            $button.removeClass('disabled');
            $button.closest('div').popup('destroy');
        }
    }
});