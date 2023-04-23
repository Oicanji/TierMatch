quizzes = {
    add_quiz: function (quiz) {
        botao_editar = '';
        if(quiz.is_owner){
            botao_editar = `
                <button type="button" class="btn btn-primary" href="/quiz/${quiz.id}">Editar <i class="fas fa-edit"></i></button>
            `;
        }
        html = `
        <div class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 p-1">
            <div class="card">
                <div class="card-header text-center">
                    ${quiz.name}
                </div>
                <div class="card-body text-center">
                    <img src="${quiz.image}" class="rounded" height="200px" width="100%">
                    <div class="btn-group mt-2" role="group" aria-label="opcoes">
                        ${botao_editar}
                        <button type="button" class="btn btn-danger" href="/play/${quiz.id}">Jogar <i class="fas fa-play"></i></button>
                    </div>
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