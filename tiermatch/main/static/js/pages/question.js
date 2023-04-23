const question = {
    init: function (type) {
        if (type == 'edit') {
            question.edit();
        }
    },
    edit: function () {
        question.open();

        $get_question = $('#get_question');
    },
    add: function () {
        var name = $('#question_name').val();
        var image = $('#question_image').val();
        var attribute = attributes.list_use;
        var quiz_id = quiz_atual.id;

        data = {
            name,
            image,
            attribute,
            quiz_id
        }
        data = JSON.stringify(data);
        $.ajax({
            url: '/question/create/',
            method: 'POST',
            data: data,
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.code != 200) {
                    question.add_question({name, image, id: response.id});
                    $('#modalCadastrarQuestion').modal('hide');
                } else {
                    Swal.fire({
                        title: 'Erro ao cadastrar!',
                        text: response.message,
                        icon: 'danger',
                        confirmButtonText: 'Ok'
                    });
                }
            }, error: function (error) {
                Swal.fire({
                    title: 'Erro ao cadastrar!',
                    text: error.responseJSON.message,
                    icon: 'danger',
                    confirmButtonText: 'Ok'
                });
            }
        });
    },
    get: function () {
        var quiz_id = quiz_atual.id;
        $.ajax({
            url: '/get/question',
            method: 'GET',
            data: {
                quiz_id
            },
            dataType: 'json',
            success: function (response) {
                for (const question of response) {
                    question.add_question(question);
                    attributes.quiz_init(question.attributes);
                }
            }, error: function (error) {
                Swal.fire({
                    title: 'Erro ao capturar as questões!',
                    text: error.responseJSON.message,
                    icon: 'danger',
                    confirmButtonText: 'Ok'
                });
            }
        });
    },
    show: function (div) {
        var question_id = div.id;
        var question_name = div.children[0].textContent;
        var question_image = div.children[1].src;
        
        $('#question_name').val(question_name);
        $('#question_image').val(question_image);
        $('#question_id').val(question_id);

        category.desative_all();
        for (const attribute of attributes.list_use) {
            category.active(attribute.category_id);
        }
        
        $('#modalCadastrarQuestion').modal('show');
    },
    add_question: function (question_new) {
        const $listItem = document.createElement("div");
        $listItem.classList.add('col-md-4 col-sm-6 text-center position-relative question-div');

        $listItem.setAttribute('id', question_new.id);
        $listItem.setAttribute('onClick', 'openQuestion(this)');

        var $name_char = document.createElement('p');
        $name_char.textContent = question_new.name;
        $name_char.classList.add('text-muted');

        $listItem.appendChild($name_char);

        var $image_char = document.createElement('img');
        $image_char.src = question_new.image;
        $image_char.classList.add('img-fluid');

        $listItem.appendChild($image_char);

        var $button_exclude = document.createElement('button');
        $button_exclude.classList.add('close');
        $button_exclude.type = 'button';
        var $ico_exlude = document.createElement('span');
        $ico_exlude.setAttribute('aria-hidden', 'true');
        $ico_exlude.innerHTML = '&times;';
        $button_exclude.createElement($ico_exlude);
        $button_exclude.setAttribute('onClick', 'delQuestion(this)');

        $listItem.appendChild($image_char);

        var $input_hidden = document.createElement('input');
        $input_hidden.type = 'hidden';
        $input_hidden.id = 'attributes';
        $input_hidden.name = 'attributes';
        $input_hidden.value = question_new.attributes;

        $listItem.appendChild($input_hidden);

        $listaCadastrados.appendChild($listItem);
    },
    open: function () {
        $('#question_div_container').slideDown('slow');
        $('#question_not_allow').slideUp('slow');
    },
}

function openQuestion(valores) {
    question.open(valores);
}

function delQuestion(button_click) {
    div_question = button_click.parentNode;
    //get input id from question_id
    id = div_question.querySelector('input[name="question_id"]').value;
    $.ajax({
        url: 'remove/question',
        method: 'POST',
        data: {
            id
        },
        dataType: 'json',
        success: function (response) {
            responde = response.json(); // caso venha dentro de outra var colocar .response
            if (responde.status == 'success') {
                div_question.remove();
            }
        },
        error: function (error) {
            const return_alert = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            });
            return_alert.fire({
                icon: 'danger',
                title: error.responseJSON.message,
            });
        }
    });
}
$('#question_cadastrar').on('click', function () {
    question.add();
});

$('#question_image').on('change', function () {
    $('#question_image_preview').attr('src', $(this).val());
    $('#question_image_preview').show();
});