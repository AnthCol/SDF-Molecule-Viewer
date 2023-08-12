
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
                
                //if (is_empty($("#sdf_file_input")[0].files[0]) || is_empty($("#sdf_molecule_name").val())){
                    /*
                     * FIXME
                     * Need to make the missing thing flash red here or something 
                     */
                 //   console.log("EMPTY PATH TAKEN\n")
                  //  return; 
               // }

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
                
                var code  = $("#add_code").val(); 
                var name  = $("#add_name").val(); 
                var red   = $("#add_r").val(); 
                var green = $("#add_g").val(); 
                var blue  = $("#add_b").val(); 
                var rad   = $("#add_rad").val(); 

                if (is_empty(code)  || is_empty(name) || is_empty(red) || 
                    is_empty(green) || is_empty(blue) || is_empty(rad)){
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
                            code:  code, 
                            name:  name, 
                            red:   red,
                            green: green, 
                            blue:  blue, 
                            rad:   rad
                        },
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
                
                var code  = $("#del_code").val(); 
                var name  = $("#del_name").val(); 
                var red   = $("#del_r").val(); 
                var green = $("#del_g").val(); 
                var blue  = $("#del_b").val(); 
                var rad   = $("#del_rad").val(); 

                if (is_empty(code)  && is_empty(name) && is_empty(red) && 
                    is_empty(green) && is_empty(blue) && is_empty(rad)){
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
                            code:  code,
                            name:  name,
                            red:   red,
                            green: green,
                            blue:  blue,
                            rad:   rad
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




