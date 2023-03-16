const eventIniquiz = new Event('iniquiz');
var quiz = {
    data: {},
    super_allow: 'Super Aprovado',
    allow: 'Aprovado',
    deny: 'Recusado',
    start : function(json) {
        quiz.data = json;

        quiz.allow = json.quiz.allow_alias;
        quiz.deny = json.quiz.deny_alias;
        quiz.super_allow = json.quiz.super_allow_alias;

        quiz.ui.loader();
        callback = () => {
            document.dispatchEvent(eventIniquiz)
        }
        quiz.ui.create('quiz', callback);
        
        //set initial question
        quiz.logic.init();
        quiz.ui.setQuestion();
    },
}