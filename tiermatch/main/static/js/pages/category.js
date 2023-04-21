var headers = {
    'Content-type': 'application/json',
    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
};
const category = {
    send: function (data = false) {
        if (!data) {
            data = {
                name: $('#categories_name').val(),
                color: $('#categories_color').val(),
            };
        }
        fetch('/category/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch((error) => {
            console.error(error.json());
        });
    },
    get: function (id = false) {
        data = {};
        if (typeof id === 'array') {
            data = { 'ids': id };
        }else if(typeof id === 'number'){
            data = { 'id': [id] };
        }
        $.ajax({
            url: '/category/get/',
            type: 'POST',
            data: JSON.stringify(category),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    },
}