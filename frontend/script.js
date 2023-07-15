
$("#sdf_form").on("submit", 
    function(event)
    {
        event.preventDefault(); 
        
        console.log("inside script\n")

        const form_data = 
        { 
            sdf_file: $("#sdf_file_input")[0].files[0], 
            molecule_name: $("#sdf_molecule_name").val()
        };
        $.ajax(
            {
                url: "/sdf-form", 
                type: "POST",
                data: JSON.stringify(form_data),
                contentType: "application/json"
            }
        );

    }
); 




