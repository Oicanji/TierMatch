quizzes = {
    delete_quiz: function(id){
        data = {
            id: id
        }
        data = JSON.stringify(data);
        $.ajax({
            url: '/quiz/delete/',
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
                    $(`#quiz_${id}`).remove();
                }
            }, error: function (error) {
                swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    icon: 'error',
                    title: 'Erro ao deletar quiz',
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                });
            }
        });
    },
    add_quiz: function (quiz) {
        botao_editar = '';
        botao_deletar = '';
        adicional = '';
        if(quiz.is_owner){
            botao_editar = `
            <a href="./quiz/${quiz.id}">
                <button type="button" class="btn btn-primary"><i class="fas fa-edit"></i></button>
            </a>`;
            botao_deletar = `
            <button type="button" class="btn btn-danger" onclick="quizzes.delete_quiz(${quiz.id})"><i class="fas fa-trash"></i></button>`;
            adicional = `
            <br />
            <hr>`;
        }
        html = `
        <div class="col-12 col-sm-6 col-md-3 col-xl-2 p-1" id="quiz_${quiz.id}">
            <div class="card">
                <div class="card-header text-center">
                    ${quiz.name}
                </div>
                <div class="card-body text-center">
                    <img src="${quiz.image}" class="rounded mb-3" height="200px" width="100%">
                    ${botao_editar}
                    ${botao_deletar}
                    ${adicional}
                    <a href="./play/${quiz.id}">
                        <button type="button" class="btn btn-success">Jogar <i class="fas fa-play"></i></button>
                    </a>
                </div>
            </div>
        </div>`;
        $('#todos_os_quizzes').append(html);
    },
    init: function(values) {
        for (const value of values) {
            quizzes.add_quiz(value);
        }
    }
}
window.onload = function () {
    quizzes.init(JSON.parse($('#edit_url').val()));
}