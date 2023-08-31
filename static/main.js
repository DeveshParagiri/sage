$(document).ready(function() {
    $("#messageArea").on("submit", function(event) {
        const date = new Date()
        const hour = date.getHours();
        const minute = (date.getMinutes()<10?'0':'') + date.getMinutes()
        const str_time = hour+":"+minute;
        var rawText = $("#text").val();
        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_container_send"><p id="h7">' + rawText + '</p><span class="msg_time_send">'+ str_time + '</span></div>';
        $("#text").val("");
        $("#messageFormeight").append(userHtml);
        $("#messageFormeight").animate({ scrollTop: 2000000000 }, "slow");
        var loadingHTML = '<div class="d-flex justify-content-start mb-4"><div class="typing-indicator" id="typing"><span></span><span></span><span></span></div></div>';
        $("#messageFormeight").append($.parseHTML(loadingHTML));
        $.ajax({
            data: {
                msg: rawText,	
            },
            type: "POST",
            url: "/get",
        }).done(function(data) {
            const date_done = new Date()
            const hour_done = date.getHours();
            const minute_done = (date_done.getMinutes()<10?'0':'') + date_done.getMinutes()
            const str_time_done = hour_done+":"+minute_done;
            document.getElementById("typing").style.display = 'none';
            console.log(data)
            data = data.split("\n").join("<br/>");          
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="msg_container"><p id="h7">' + data + '</p><span class="msg_time">' + str_time_done + '</span></div></div>';
            $("#messageFormeight").append($.parseHTML(botHtml));
            $("#messageFormeight").animate({ scrollTop: 2000000000 }, "slow");
        });
        event.preventDefault();
    });
});

// var i = 0;
// var txt = 'Lorem ipsum dummy text blabla.';
var speed = 50;

function typeWriter(data, str_time) {
    
    $("#messageFormeight").append($.parseHTML('<div class="d-flex justify-content-start mb-4"><div class="msg_container"><p id="h7"></p></div></div>'))
    if (i < data.length) {
        $("#messageFormeight").append($.parseHTML(data.charAt(i)));
        i++;
        setTimeout(typeWriter, speed);
    }
    $("#messageFormeight").append($.parseHTML('</p><span class="msg_time">' + str_time_done + '</span></div></div>'))
}
