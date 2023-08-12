
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
                
                if (is_empty($("#sdf_file_input")[0].files[0]) || is_empty($("#sdf_molecule_name").val())){
                    /*
                     * FIXME
                     * Need to make the missing thing flash red here or something 
                     */
                    console.log("EMPTY PATH TAKEN\n")
                    return; 
                }

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


                var code  = is_empty($("#add_code").val()); 
                var name  = is_empty($("#add_name").val()); 
                var red   = is_empty($("#add_r").val()); 
                var green = is_empty($("#add_g").val()); 
                var blue  = is_empty($("#add_b").val()); 
                var rad   = is_empty($("#add_rad").val()); 

                if (!code || !name || !red || !green || !blue || !rad){
                    console.log("NEED TO FILL ALL ELEMENTS\n")
                    /* FIXME
                     * Need to fill all elements. Make missing one flash red or something. 
                     */
                    return; 
                }
                
                $.ajax(
                    {
                        url: "/add-form", 
                        type: "POST",
                        data: {
                            code:  $("#add_code").val(), 
                            name:  $("#add_name").val(), 
                            red:   $("#add_r").val(), 
                            green: $("#add_g").val(), 
                            blue:  $("#add_b").val(), 
                            rad:   $("#add_rad").val()
                        }
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
                
                var code = is_empty($("#del_code")); 
                var name = is_empty($("#del_name")); 
                var red = is_empty($("#del_r")); 
                var green = is_empty($("#del_g")); 
                var blue = is_empty($("#del_b")); 
                var rad = is_empty($("#del_rad")); 

                if (code && name && red && green && blue && rad){
                    console.log("NO INPUTS\n"); 
                    /* FIXME
                     * Need to do something when user doesn't input everything but presses delete
                     */
                    return; 
                }
                
                $.ajax(
                    {
                        url: "/delete-form", 
                        type: "POST",
                        data: {
                            code:  $("#del_code").val(),  
                            name:  $("#del_name").val(), 
                            red:   $("#del_r").val(), 
                            green: $("#del_g").val(), 
                            blue:  $("#del_b").val(), 
                            rad:   $("#del_rad").val()
                        },
                        processData: false, 
                        contentType: false
                    }
                );
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




