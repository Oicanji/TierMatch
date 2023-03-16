ui_to_logic = {
    'left': 'deny',
    'right': 'allow',
    'top': 'super_allow'
};

quiz.logic = {
    respost : [],
    actual_question : 0,
    total_questions : 0,
    question: {},
    next: function () {
        quiz.logic.question = quiz.data.quiz.questions[quiz.logic.actual_question];
        quiz.logic.render();
    },
    render: function () {
        quiz.ui.setQuestion();
    },
    init: function () {
        quiz.logic.total_questions = quiz.data.quiz.questions.length;
        quiz.logic.next();
        quiz.ui.setNextQuestion();
    },
    answer: function (answer) {
        answer = ui_to_logic[answer];

        event.preventDefault();
        event.stopPropagation();
        
        quiz.ui.block();
        
        // console.log(answer);
        new_respost = {
            'id': quiz.logic.question.id,
            'name': quiz.logic.question.name,
            'answer': answer,
            'stats': quiz.logic.question.stats,
            'image': quiz.logic.question.image,
        }
        quiz.logic.respost.push(new_respost);

        
        if (quiz.logic.actual_question >= quiz.logic.total_questions-1) {
            quiz.logic.end();
            return;
        }

        setTimeout(function () {
            quiz.logic.actual_question++;
            quiz.logic.next();
            quiz.ui.update_fade("");
            setTimeout(function () {
                quiz.ui.resetPosition();
                quiz.ui.setNextQuestion();
                quiz.ui.unblock();
            }, 200);
        }, 200);
    },
    end: function () {
        console.log(quiz.logic.respost);

        //remove all the elements for body
        document.querySelector('body div.cloud-container').innerHTML = "";
        //create a new div for the results
        quiz.result.init(quiz.logic.respost);
    }
    
}