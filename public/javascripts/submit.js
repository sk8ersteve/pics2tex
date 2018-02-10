/*$(function() {
    alert('hello');
    function setupGoForm() {
        $('#go-btn').bind('click', function () {
            var pic = $('#pic').val();
            var obj=new Object();
            obj.pic = pic;
            $.ajax('http://pics2tex.eastus.cloudapp.azure.com/process/image', {
                type:'POST',
                data: obj,
                datatype: 'json',
                complete: function (data) {
                    alert(JSON.stringify(data));
                    //$('#result').val(data);
                }
            })
            alert("hi");
            return false;
        });
    }
    setupGoForm();
});*/