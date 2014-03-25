$(document).ready(function() {
    $('.formAjax').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: searchSuccess,
                $().html(response); // update the DIV
            }
        });
        return false;
    });
});