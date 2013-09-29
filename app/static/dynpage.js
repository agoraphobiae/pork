$(function() {

    if (Modernizr.history) {

        // set up vars
        var $maincontent = $("#main-content"),
            $pageWrap = $("#wrap"),
            baseHeight = 0,
            $el;

        $pageWrap.height($pageWrap.height());
        baseHeight = $pageWrap.height() - $maincontent.height();


        $("#cmd").submit( function(event) {
            _href = "/play/" + $("#cmdi").val();

            history.pushState(null, null, _href);

            loadContent(_href);
        });

        function loadContent(href) {
            $maincontent.find("#contents").fadeOut(200, function() {
                $maincontent.hide().load(href + " #contents", function() {
                    $pageWrap.animate({ height: baseHeight + $maincontent.height() + "px" });
                });
            });
        }

        $(window).bind('popstate', function(){
            _link = location.pathname.replace(/^.*[\\\/]/, ''); //get filename only
            loadContent(_link);
        });
    } else {

    }
});