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
    get: function (id = false, callback = false) {
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
                if (callback) {
                    callback(response);
                }
                return response;
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    },
    delete: function (id) {
        $.ajax({
            url: '/category/remove/',
            type: 'POST',
            data: JSON.stringify({ 'id': id }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function(response) {
                return response;
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    },
    build: async function () {
        const response = await category.get(false, category.draw);
    },
    draw: function (response) {
        console.log('asdsdaasd');
        $('#categoria_list').html('');
        categories = response.data;
        console.log(categories);
        for (let i = 0; i < categories.length; i++) {
            const item = categories[i];
            console.log(item);
            $('#categoria_list').append(
                `<div class="col-1 p-1" id="${item.id}">
                    <span class="badge badge-primary categoria_div">
                        ${item.name}
                        <button type="button" class="close add">
                            <span aria-hidden="true">+</span>
                        </button>
                        <button type="button" class="close" onclick="category.delete(${item.id})">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </span>
                </div>`);
        }
    }
}
window.onload = function () {
    category.build();
}