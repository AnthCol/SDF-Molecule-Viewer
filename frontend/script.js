
function is_empty(html_element) {
    return !$.trim(html_element)
}

$(document).ready(
    function(){
        $("#sdf_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                var form_data = new FormData();
                
                var file = $("#sdf_file_input")[0].files[0]; 
                var name = $("#sdf_molecule_name").val(); 
               
                var err_colour = "lightcoral"; 

                if (is_empty(file) && is_empty(name))
                {
                    $("#sdf_file_input").css("background-color", err_colour); 
                    $("#sdf_molecule_name").css("background-color", err_colour); 
                }
                else if (is_empty(file))
                {
                    $("#sdf_file_input").css("background-color", err_colour); 
                    $("#sdf_molecule_name").css("background-color", "white"); 
                }
                else if (is_empty(name))
                {
                    $("#sdf_file_input").css("background-color", "unset"); 
                    $("#sdf_molecule_name").css("background-color", err_colour); 
                }
                else
                {
                    $("#sdf_file_input").css("background-color", "unset"); 
                    $("#sdf_molecule_name").css("background-color", "white"); 

                    form_data.append("sdf_file", file); 
                    form_data.append("molecule_name", name); 
                
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
            }
        ), 
        $("#add_form").on("submit", 
            function(event)
            {
                event.preventDefault();

                var err_colour = "lightcoral";
                var bad_flag = 0; 
                
                var form_data = new FormData(); 
                const map = new Map(); 
                map.set("#add_code", $("#add_code").val()); 
                map.set("#add_name", $("#add_name").val()); 
                map.set("#add_r",    $("#add_r").val()); 
                map.set("#add_g",    $("#add_g").val()); 
                map.set("#add_b",    $("#add_b").val()); 
                map.set("#add_rad",  $("#add_rad").val()); 

                for (const [key, value] of map)
                {

                    form_data.append(value)

                    if (is_empty(value))
                    {
                        $(key).css("background-color", err_colour); 
                        bad_flag = 1; 
                    }
                    else
                    {
                        $(key).css("background-color", "white"); 
                    }

                }
                
                if (!bad_flag)
                {
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
            }
        ), 
        $("#delete_form").on("submit", 
            function(event)
            {
                event.preventDefault(); 
                
                err_colour = "lightcoral"; 
                bad_flag = 0; 
                
                var form_data = new FormData(); 
                const map = new Map(); 
                map.set("#del_code", $("#del_code").val()); 
                map.set("#del_name", $("#del_name").val()); 
                map.set("#del_r",    $("#del_r").val()); 
                map.set("#del_g",    $("#del_g").val()); 
                map.set("#del_b",    $("#del_b").val()); 
                map.set("#del_rad",  $("#del_rad").val()); 
                
                for (const [key, value] of map)
                {
                    var mod_key = key.replace("#del_", ""); 
                    form_data.append(mod_key, value); 

                    if (is_empty(value)) 
                    {
                        $(key).css("background-color", err_colour); 
                        bad_flag = 1
                    }
                    else
                    {
                        $(key).css("background-color", "white"); 
                    } 
                }
                
                if (!bad_flag)
                {
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
            }
        )/*, 
        $("#display_button").on("click", 
            function(event)
            {
                event.preventDefault(); 
                $.ajax(
                    {
                        url: "/svg-display", 
                        type: "POST"
                        data: // FIXME unfinished  
                        processData: false, 
                        contentType: false
                    }
                );
            }
        );*/ 
    }  
); 




