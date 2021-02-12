([function(f, c, e) {
    var a = e(0);
    (function() {
        var b = new a,
            oldcash = b.get("adcashufpv3");
        b.set("adcashufp", "", -1);
        b.set("adcashufpv1", "", -1);
        b.set("adcashufpv2",
            "", -1);
        "" == oldcash && (String.prototype.b = function() {
            var a = 0;
            if (0 == this.length) return a;
            for (var b = 0; b < this.length; b++) a = (a << 5) - a + this.charCodeAt(b), a &= a;
            return Math.abs(a)
        }, c = function() {
            Date.now || (Date.now = function() {
                return (new Date).getTime()
            });
            return ("" + Math.abs(Math.random())).b() + "" + ("" + Date.now()).b() + ("" + Math.abs(Math.random())).b()
        }());
        b.set("adcashufpv3", c);
        try {
            window.top.postMessage && window.top.postMessage({
                call: "ufpCached",
                ufp: c
            }, "*")
        } catch (d) {}
    })()
}]);