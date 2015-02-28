 $(document).ready(function() {


    $('form[name="send_form"]').submit( function () {

       //  var prog = $('div [name="prog"]');$(this)[0]
       var form_data = new FormData();
       var sfile = $('input[type="file"]')[0].files[0];
       var ftype = $('select[name="content_type"] :selected').val();
       var fsecure = $('select[name="secure"] :selected').val();
       var sfname = $('input[name="s_file_name"]').val();
       console.log(fsecure);
       form_data.append('send_file', sfile);
       form_data.append('content_type', ftype);
       form_data.append('file_name', sfname);
       form_data.append('secure', fsecure);
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
                        if(e.loaded<e.total)
                        {
                            $('div[name="prog"]').html((e.loaded /  e.total)*100 + "%");
                        }
                        else
                        {
                            $('div[name="prog"]').html("Waiting for server....");
                        }
                        console.log((e.loaded /  e.total)*100 + "%" );
                    }

                }, false);
            }
            return mxhr;
        },
        success: function(data) {
            if ("success" in data){
                $('div[name="prog"]').html('Done!<br>Link:<a href="' + data['success'] + '">New file</a>');
                    //location.reload(true);// <!-- relocate to home  -->
                }
                else {
                    var mes = "Other error";
                    if ("error" in data)  mes = data["error"];
                    $('div[name="prog"]').html("Error: " + mes);
                }
            },

            processData: false,
            cache: false,
            contentType: false,
            dataType: 'json'
        });

 s_form.fail(
    function() {
        $('div[name="prog"]').html("Request error");
    });
 s_form.complete(
    function() {

    });
 return false;
});
});
