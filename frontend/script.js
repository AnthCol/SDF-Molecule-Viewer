
$("#sdf_form").on("submit", 
    function(event)
    {
        event.preventDefault(); 
        const form_data = new FormData(this); 

        form_data.append("sdf_file", $("#sdf_file_input")[0].files[0]);
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




