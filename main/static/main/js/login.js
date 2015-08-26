/**
 * Created by ToothlessRebel on 8/25/2015.
 */

$(function () {
    $('.help.icon').popup({
        inline: true,
        hoverable: true,
        position: 'top center'
    });

    $('.choose-username').on('change', function () {
        var $this = $(this);
        $this.closest('.input').addClass('loading');
    });
});