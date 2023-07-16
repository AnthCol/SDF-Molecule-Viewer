
$(document).ready(
    function(){
        $("#sdf_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("sdf_file", $("#sdf_file_input")[0].files[0]); 
                form_data.append("molecule_name", $("#sdf_molecule_name").val())
                $.ajax(
                    {
                        url: "/sdf-form", 
                        type: "POST",
                        data: form_data, 
                        processData: false,
                        contentType: false
                    }
                );

            }
        );
    }
); 




