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

        question.init(type);
        category.init(type);
    },
    submit: function (params = false) {
        //categorias = $('.categoria_canva .categoria_div');
        categorias = document.querySelectorAll('.categoria_canva .categoria_div');
        categorias_list = [];
        if (params == false) {
            for (const categoria of categorias) {
                if (categoria.classList.contains('active')) {
                    va = categoria.attributes.value;
                    categorias_list.push(va.value);
                }
            }
            data = {
                name: $('#name').val(),
                description: $('#description').val(),
                super_allow_allias: $('#super_allow_alias').val(),
                super_allow_color: $('#super_allow_color').val(),
                allow_allias: $('#allow_alias').val(),
                allow_color: $('#allow_color').val(),
                deny_allias: $('#deny_alias').val(),
                deny_color: $('#deny_color').val(),
                categories: categorias_list,
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
                    quiz.pos_create(response.data.json());
                }
            }, error: function (error) {
                console.log(error);
            }
        });
    },
    pos_create: function (data) {
        attributes.quiz_init();
        listQuestions = data.questions ? data.questions : [];
        quiz.init('edit');
    }
}