// script.js file
function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}
var ajax = require('web.ajax');//To define ajaxvar

domReady(function () {
    // If found you qr code
    function onScanSuccess(decodeText, decodeResult) {
        // Make an ajax call to the Odoo controller to confirm the scan

        ajax.jsonRpc('/my_shuttle/confirm_onboard', 'call', {'decodeText' : decodeText,
        });//json Rpc Call
        .then(function (data) {});
        //To receive data from python(non-mandatory)
                alert("Your QR Code is: " + decodeText);
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbox: 250 }  // Fixed typo: `qrbox`
    );
    htmlscanner.render(onScanSuccess);
});
