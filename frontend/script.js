
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
                    }
                );
            }
        );
    },

    function(){
        $("#add_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("code", $("#ele_code").val()); 
                form_data.append("name", $("#ele_name").val()); 
                form_data.append("red",  $("#ele_r").val()); 
                form_data.append("green",$("#ele_g").val()); 
                form_data.append("blue", $("#ele_b").val()); 
                form_data.append("rad",  $("#ele_rad").val()); 
                
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
        );
    }, 

    function(){
        $("#delete_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData(); 
                form_data.append("code", $("#rm_code").val()); 
                form_data.append("name", $("#rm_name").val()); 
                form_data.append("red",  $("#rm_r").val()); 
                form_data.append("green",$("#rm_g").val()); 
                form_data.append("blue", $("#rm_b").val()); 
                form_data.append("rad",  $("#rm_rad").val()); 
                
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
        );
    } 
); 




