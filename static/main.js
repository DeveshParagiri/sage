$(document).ready(function() {
    $("#messageArea").on("submit", function(event) {
        const date = new Date()
        const hour = date.getHours();
        const minute = (date.getMinutes()<10?'0':'') + date.getMinutes()
        const str_time = hour+":"+minute;

        var rawText = $("#text").val();

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_container_send">' + rawText + '<span class="msg_time_send">'+ str_time + '</span></div>';
        
        $("#text").val("");
        $("#messageFormeight").append(userHtml);
        $("#messageFormeight").animate({ scrollTop: 2000000000 }, "slow");
        $.ajax({
            data: {
                msg: rawText,	
            },
            type: "POST",
            url: "/get",
        }).done(function(data) {
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="msg_container">' + data + '<span class="msg_time">' + str_time + '</span></div></div>';
            $("#messageFormeight").append($.parseHTML(botHtml));
            $("#messageFormeight").animate({ scrollTop: 2000000000 }, "slow");
        });
        event.preventDefault();
    });
});