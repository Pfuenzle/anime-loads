String.prototype.b = function() {
    var a = 0;
    if (0 == this.length) return a;
    for (var curChar = 0; curChar < this.length; curChar++) {
        a = ((a << 5) - a + this.charCodeAt(curChar));
        console.log(this.charCodeAt(curChar));
//        a &= a;
    }
    return Math.abs(a);
}
 
 c = function() {
             Date.now || (Date.now = function() {
                 return (new Date).getTime()
             });
             var rand1 = Math.random();
             console.log("R1: " + rand1);
             var first = ("" + Math.abs(rand1)).b();
             console.log("1: " + first);

             var date = Date.now();
             console.log("T1: " + date);
             var sec = ("" + date).b();
             console.log("2: " + sec);
             
             var rand3 = Math.random();
             console.log("R3: " + rand3);
             var third = ("" + Math.abs(rand3)).b();
             console.log("3: " + third);
             
             return first + "" + sec + third
         }
 console.log(c())