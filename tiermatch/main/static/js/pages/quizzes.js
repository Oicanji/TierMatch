quizzes = {
    add_quiz: function (quiz) {
        html = `
        <div class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 p-1">
            <div class="card">
                <div class="card-header text-center">
                    ${quiz.name}
                </div>
                <div class="card-body">
                    <img src="${question_new.image}" class="img-fluid">

        `;
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