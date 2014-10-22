 $(document).ready(function() {


    $('form[name="send_form"]').submit( function () {

       //  var prog = $('div [name="prog"]');$(this)[0]
       var form_data = new FormData();
       var sfile = $('input[type="file"]')[0].files[0];
       var ftype = $('select[name="content_type"] :selected').val();
       var sfname = $('input[name="s_file_name"]').val();
       form_data.append('send_file', sfile);
       form_data.append('content_type', ftype);
       form_data.append('file_name', sfname);
       var s_form = $.ajax({
        url: "/upload_content",
        type: "POST",
        data: form_data,
        xhr: function(){
            var mxhr = $.ajaxSettings.xhr();
            if (mxhr.upload)
            {
                mxhr.upload.addEventListener('progress', function(e){
                    if(e.lengthComputable)
                    {
                        $('div[name="prog"]').html((e.loaded /  e.total)*100 + "%");
                        console.log((e.loaded /  e.total)*100 + "%" );
                    }

                }, false);
            }
            return mxhr;
        },
        success: function(data) {
            if ("success" in data){
                    $('div[name="prog"]').html("100%");
                    //location.reload(true);// <!-- relocate to home  -->
                    console.log("access to reloaded; new link: " + data['success']);
                }
                else {
                    var mes = "Other error";
                    if ("error" in data)  mes = data["error"];
                    alert(mes);
                }
            },

            processData: false,
            cache: false,
            contentType: false,
            dataType: 'json'
        });

       s_form.fail(
        function() {
            alert("Request error");
        });
        s_form.complete(
        function() {
            $('div[name="prog"]').html("100%");
        });
       return false;
   });
});
