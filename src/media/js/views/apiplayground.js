define('views/apiplayground',
    ['z', 'requests', 'urls', 'l10n'],
    function(z, requests, urls, l10n) {
    'use strict';

    var gettext = l10n.gettext;

    function buildUrl(url, args) {
        var arg = null;
        var val = '';
        var matches;
        var regex = /\/\(.+?\)\//g;

        var i = 0;
        url = url.replace(regex, function() {
            return '/' + args[i++] + '/';
        });

        return url;
    }

    z.page.on('click', '.api-endpoint', function(e) {
        var $this = $(this);
        $('.options').hide();
        var html = $this.parent().siblings('.options').html();
        $('.playfield .replace').html(html);
    });
    z.page.on('click', '.api-name', function() {
        $('.endpoints-container').addClass('hidden');
        $(this).closest('.api-container').find('.endpoints-container')
                                         .removeClass('hidden');
    });

    z.page.on('click', 'input[name="view-selector"]', function() {
        var $this = $(this);
        var $toolbox = $this.closest('.toolbox');
        $toolbox.siblings('.view').hide();
        $toolbox.siblings('.' + $this.val() + '-view').show();
    });

    z.page.on('click', '.send-request', function() {
        var $this = $(this);
        var url = $this.data('url');
        var method = $this.data('method');
        var $toolbox = $this.closest('.toolbox');
        var params = {};

        var $requestView = $toolbox.siblings('.request-view');
        $requestView.find('.request-params input').each(function() {
            var $_this = $(this);
            var val = $_this.val();
            if (val.length > 0) {
                params[$_this.data('name')] = val;
            }
        });

        var args = [];
        $requestView.find('.url-args input').each(function() {
            var $_this = $(this);
            args.push($_this.val());
        });

        function progressHandler() {
            $toolbox.siblings('.response-view').html('<p class="spinner spaced alt"></p>');
        }

        function errorHandler(err) {
            var $pre = $('<pre>');
            $pre.text(err.responseText);
            $toolbox.siblings('.response-view').html('<div><p class="error">' +
                gettext('Erroneous response') + '</p><pre>' + $pre.text() + '</pre></div>');
        }

        function responseHandler(data) {
            var $pre = $('<pre>');
            $pre.text(JSON.stringify(data, null, '  '));
            $toolbox.siblings('.response-view').html('').append($pre);
        }

        url = buildUrl(url, args);
        url = urls.absolutifyApiUrl(url, params);
        $this.closest('.toolbox').find('.response-selector').trigger('click');
        progressHandler();
        if (method == 'delete') {
            requests[method](url).done(responseHandler).fail(errorHandler);
        } else {
            requests[method](url, params).done(responseHandler).fail(errorHandler);
        }
    });

    return function(builder) {
        builder.start('playground.html');
    };
});
