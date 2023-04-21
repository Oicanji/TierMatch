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
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao criar Categoria.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Categoria criada com sucesso.');
        })
        .catch(error => {
            console.error(error);
        });
    },
    get: function () {
        return $.ajax({
            url: '/get/category',
            type: 'GET',
            dataType: 'json',
            error: function (xhr, status, error) {
                console.log(error);
            },
            success: function (data) {
                return data;
            }
        });
    },
    get_all: function () {
        return $.ajax({
            url: '/get/categories',
            type: 'GET',
            dataType: 'json',
            error: function (xhr, status, error) {
                console.log(error);
            },
            success: function (data) {
                return data;
            }
        });
    },
    delete: function (id) {
        return $.ajax({
            url: '/remove/category',
            type: 'POST',
            data: { 'id': id },
            dataType: 'json',
            error: function (xhr, status, error) {
                console.log(error);
                return false;
            },
            success: function (data) {
                return true;
            }
        });
    }
}