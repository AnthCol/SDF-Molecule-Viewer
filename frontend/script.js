
$(document).ready(
    function(){
        $("#sdf_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("sdf_file", $("#sdf_file_input")[0].files[0]); 
                form_data.append("molecule_name", $("#sdf_molecule_name").val());
                
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
        ), 
        $("#add_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("code", $("#add_code").val()); 
                form_data.append("name", $("#add_name").val()); 
                form_data.append("red",  $("#add_r").val()); 
                form_data.append("green",$("#add_g").val()); 
                form_data.append("blue", $("#add_b").val()); 
                form_data.append("rad",  $("#add_rad").val()); 
                
                $.ajax(
                    {
                        url: "/add-form", 
                        type: "POST",
                        data: form_data, 
                        processData: false, 
                        contentType: false
                    }
                );
            }
        ), 
        $("#delete_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("code", $("#del_code").val()); 
                form_data.append("name", $("#del_name").val()); 
                form_data.append("red",  $("#del_r").val()); 
                form_data.append("green",$("#del_g").val()); 
                form_data.append("blue", $("#del_b").val()); 
                form_data.append("rad",  $("#del_rad").val()); 
                
                $.ajax(
                    {
                        url: "/delete-form", 
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




