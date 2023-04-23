const question = {
    init: function (type) {
        if (type == 'edit') {
            question.edit();
        }
    },
    edit: function () {
        question.open();
        question.build();
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
                if (response.code == 200) {
                    data = JSON.parse(response.data);
                    console.log(data);
                    question.add_question({name: data.name, image: data.image, id: data.id});
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
        console.log(question_new);
        const $listItem = `
            <div class="col-md-4 col-sm-6 text-center position-relative question-div" id="${question_new.id}" onClick="openQuestion(this)">
                <p class="text-muted">${question_new.name}</p>
                <img src="${question_new.image}" class="img-fluid">
                <input type="hidden" id="attributes" name="attributes" value="${question_new.attributes}">
                <button class="close" type="button" onClick="delQuestion(this)">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;

        $('#lista_cadastrados').append($listItem);
    },
    open: function () {
        $('#question_div_container').slideDown('slow');
        $('#question_not_allow').slideUp('slow');
    },
    build: function () {
        data = {
            id: quiz_atual.id,
        }
        data = JSON.stringify(data);
        $.ajax({
            url: '/question/get/all',
            method: 'GET',
            data: data,
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log(response);
                if (response.code == 200) {
                    data = JSON.parse(response.data);
                    for (const question of data) {
                        question.remove_all();
                        question.add_question(question);
                    }
                }
            }, error: function (error) {
                console.log(error);
            }
        });
    },
    remove_all: function () {
        $('#lista_cadastrados').empty();
    }
}

function openQuestion(valores) {
    question.open(valores);
}
$('#question_cadastrar').on('click', function () {
    $(this).attr('disabled', true);
    question.add();
    setTimeout(() => {
        $(this).attr('disabled', false);
    }, 1000);
});

$('#question_image').on('change', function () {
    $('#question_image_preview').attr('src', $(this).val());
    $('#question_image_preview').show();
});