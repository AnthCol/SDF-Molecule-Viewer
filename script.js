$(document).ready(
    function(){
        $("#sdf_form").submit(
            function(){
                $.post(
                    "/sdf_upload.html"
                    ,
                    {
                        filename: $("#sdf_file_input").val(),
                        molecule_name: $("#sdf_molecule_name").val()
                    }
                    ,
                    function(){
                      alert("Received .sdf file")
                    }
                )
            }
        )
    }
)