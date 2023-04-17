const category = {
    send : function () {
        data = {
            'name': $('#categories_name').val(),
            'color': $('#categories_color').val(),
        };
        return $.ajax({
            url: '/set/category',
            type: 'POST',
            data: data,
            dataType: 'json',
            error: function (xhr, status, error) {
                console.log(error);
            },
            success: function (data) {
                return data;
            }
        });
    },
    get : function () {
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
    get_all : function () {
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
    delete : function (id) {
        return $.ajax({
            url: '/remove/category',
            type: 'POST',
            data: {'id': id},
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