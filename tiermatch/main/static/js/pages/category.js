const category = {
    in_edit_mode: false,
    init: function (type) {
        if (type == 'edit') {
            category.in_edit_mode = true;
        }
    },
    send: function (data = false) {
        $('#cadastrar_categoria_button').attr('disabled', true);
        if (!data) {

            console.log("aQUII");
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
            //refresh
            category.build();
            $('#modalCadastrarCategoria').modal('hide');
            setTimeout(() => {
                $('#cadastrar_categoria_button').attr('disabled', false);
            }, 1000);
        })
        .catch((error) => {
            console.error(error.json());
            $('#cadastrar_categoria_button').attr('disabled', false);
        });
    },
    get: function (id = [], callback = false) {
        data = {};
        if (id.length != 0) {
            data.categories = id;
        }
        data = JSON.stringify(data);
        console.log(data);
        $.ajax({
            url: '/category/get/',
            type: 'POST',
            data: data,
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
        $('#categoria_div_'+id).remove();
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
                //refresh
                category.build();
                return response;
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    },
    active: function (id) {
        if($('#categoria_div_'+id+' .categoria_div').hasClass('active')){
            $('#categoria_div_'+id+' .categoria_div').removeClass('active');
            $('#categoria_div_'+id+' .categoria_div button.close.delete').show();
            $('#categoria_div_'+id+' .categoria_div button.close.add span').html('<i class="fa-regular fa-square-plus"></i>');
        }else{
            $('#categoria_div_'+id+' .categoria_div').addClass('active');
            $('#categoria_div_'+id+' .categoria_div button.close.delete').hide();
            $('#categoria_div_'+id+' .categoria_div button.close.add span').html('<i class="fa-regular fa-square-minus"></i>');
        }
    },
    desative_all: function () {
        for (let i = 0; i < categories.length; i++) {
            const item = categories[i];
            $('#categoria_div_'+item.id+' .categoria_div').removeClass('active');
            $('#categoria_div_'+item.id+' .categoria_div button.close.delete').show();
            $('#categoria_div_'+item.id+' .categoria_div button.close.add span').html('<i class="fa-regular fa-square-plus"></i>');
        }
    },
    build: async function () {
        await category.get([], category.draw);
    },
    draw: function (response) {
        $('#categoria_list').html('');
        categories = response.data;
        for (let i = 0; i < categories.length; i++) {
            const item = categories[i];
            // cut more than 20 chars
            if (item.name.length > 20) {
                item.name = item.name.substring(0, 20) + '...';
            }

            $('#categoria_list').append(
                `<div class="p-1 categoria_canva" id="categoria_div_${item.id}">
                    <span class="badge badge-primary categoria_div" style="background-color: ${item.color};"  value="${item.id}">
                        ${item.name}
                        <button type="button" class="close add" onclick="category.active(${item.id})">
                            <span aria-hidden="true"><i class="fa-regular fa-square-plus"></i></span>
                        </button>
                        <button type="button" class="close delete" onclick="category.delete(${item.id})">
                            <span aria-hidden="true"><i class="fa-solid fa-trash"></i></span>
                        </button>
                    </span>
                </div>`);
        }
        category.draw_edit();
    },
    draw_edit: function () {
        if (category.in_edit_mode) {
            for ( const cat of quiz_atual.categories) {
                category.active(cat);
            }
        }
    }
}
window.onload = function () {
    category.build();
}