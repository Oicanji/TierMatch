listQuestions = [];
quiz_atual = null; // mandar aqui o objeto do quiz atual se for editar

$(document).ready(function () {
    if (quiz_atual != null) {
        listQuestions = quiz_atual.questions;
    }else{
        attributes.quiz_init();
    }
});

quiz = {
    init: function (type){
        if(type == 'edit'){
            quiz.edit();
        }
    },
    edit: function () {
        $('#title-quiz').text('Editar Quiz ' + quiz_atual.name + ".");
        $('#name').val(quiz_atual.name);
        $('#description').val(quiz_atual.description);
        $('#super_allow_alias').val(quiz_atual.super_allow_alias);
        $('#super_allow_color').val(quiz_atual.super_allow_color);
        $('#allow_alias').val(quiz_atual.allow_alias);
        $('#allow_color').val(quiz_atual.allow_color);
        $('#deny_alias').val(quiz_atual.deny_alias);
        $('#deny_color').val(quiz_atual.deny_color);

        $('#question_not_allow').remove()
        $('#question_div_container').slideDown();
        $('#lista_cadastrados').html('');

        $('#botao_cadastar_editar').html('Editar');
    },
    get_categories_active: function () {
        for (const categoria of categorias) {
            if (categoria.classList.contains('active')) {
                va = categoria.attributes.value;
                categorias_list.push(va.value);
            }
        }
        return categorias_list;
    },
    submit: function (params = false) {
        //categorias = $('.categoria_canva .categoria_div');
        categorias = document.querySelectorAll('.categoria_canva .categoria_div');
        categorias_list = [];
        if (params == false) {
            categorias_list = quiz.get_categories_active();
            data = {
                name: $('#name').val(),
                description: $('#description').val(),
                super_allow_allias: $('#super_allow_alias').val() ? $('#super_allow_alias').val() : 'Super Gostei',
                super_allow_color: $('#super_allow_color').val() ? $('#super_allow_color').val() : '#f9c74f',
                allow_allias: $('#allow_alias').val() ? $('#allow_alias').val() : 'Gostei',
                allow_color: $('#allow_color').val() ? $('#allow_color').val() : '#ff595e',
                deny_allias: $('#deny_alias').val() ? $('#deny_alias').val() : 'Não Gostei',
                deny_color: $('#deny_color').val() ? $('#deny_color').val() : '#00b4d8',
                categories: categorias_list,
            }
            //casoum dos campos esteja vazio
            for (const key in data) {
                if (key != 'description' && key != 'categories'){
                    if (data[key] == '' || data[key] == null) {
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            showConfirmButton: false,
                            timer: 3000,
                            icon: 'error',
                            title: 'Preencha todos os campos',
                            timerProgressBar: true,
                            didOpen: (toast) => {
                                toast.addEventListener('mouseenter', Swal.stopTimer)
                                toast.addEventListener('mouseleave', Swal.resumeTimer)
                            }
                        });
                        return;
                    }
                }
            }
        }else{
            data = params;
        }
        data = JSON.stringify(data);

        $.ajax({
            url: '/quiz/create/',
            method: 'POST',
            data: data,
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.code == 200) {
                    Swal.fire({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        icon: 'success',
                        title: response.message,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                            toast.addEventListener('mouseenter', Swal.stopTimer)
                            toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                    });
                    quiz.pos_create(JSON.parse(response.data));
                }
            }, error: function (error) {
                console.log(error);
            }
        });
    },
    quiz_edit: function (quiz_atual) {
        categorias_list = quiz.get_categories_active();
        data = {
            id: quiz_atual.id,
            name: $('#name').val(),
            description: $('#description').val(),
            super_allow_allias: $('#super_allow_alias').val(),
            super_allow_color: $('#super_allow_color').val(),
            allow_allias: $('#allow_alias').val(),
            allow_color: $('#allow_color').val(),
            deny_allias: $('#deny_alias').val(),
            deny_color: $('#deny_color').val(),
            //categories: categorias_list,
        }
        data = JSON.stringify(data);
        $.ajax({
            url: '/quiz/edit/',
            method: 'POST',
            data: data,
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.code == 200) {
                    Swal.fire({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        icon: 'success',
                        title: response.message,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                            toast.addEventListener('mouseenter', Swal.stopTimer)
                            toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                    });
                    quiz.pos_create(JSON.parse(response.data));
                }
            }, error: function (error) {
                console.log(error);
            }
        });
    },
    pos_create: function (data) {
        attributes.quiz_init();
        listQuestions = data.questions ? data.questions : [];
        quiz_atual = data;
        quiz.init('edit');
    }
}

$('#botao_cadastar_editar').on('click', function () {
    event.preventDefault();
    console.log(quiz_atual);
    if (quiz_atual == null) {
        //submit
        quiz.submit();
    }else{
        //edit
        quiz.quiz_edit(quiz_atual);
    }
});