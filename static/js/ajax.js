$(document).ready(function(){
    $('#origin').select(function(){
        $.ajax({
            method:"GET",
            url:'/',
            data:{
                "flight_origin":$('#origin').val(),
            },
            success:selectsuccess,
            dataType:'html'
        });
    });
    function selectsuccess(data, textStatus, jqXHR){
        $('#destination').html(data)

    }
})