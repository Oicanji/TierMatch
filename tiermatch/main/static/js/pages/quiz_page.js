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
        if (params == false) {
            var name = $('#name').val();
            var description = $('#description').val();
            var super_allow_alias = $('super_allow_alias').val();
            var super_allow_color = $('super_allow_color').val();
            var allow_alias = $('allow_alias').val();
            var allow_color = $('allow_color').val();
            var deny_alias = $('deny_alias').val();
            var deny_color = $('deny_color').val();
            data = {
                name,
                description,
                super_allow_allias,
                super_allow_color,
                allow_allias,
                allow_color,
                deny_allias,
                deny_color,
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
                console.log(response);
            }, error: function (error) {
                console.log(error);
            }
        });
        
    }
}