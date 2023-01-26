def calculate_score(attempt):
    score = 0
    for answer in attempt.answers.all():
        question = answer.question

        if question.question_type == 'SCQ':
            selected = answer.selected_options.all()
            if len(selected) == 0:
                continue

            selected = selected[0]
            if selected.option.answer:
                score += question.positive_marking
            else:
                score -= question.negative_marking

        elif question.question_type == 'MCQ':
            selected = answer.selected_options.all()
            correct_opts = question.options.filter(answer=True)

            neg = 0
            for option in selected:
                if option.option.answer == False:
                    score -= question.negative_marking
                    neg = 1
                    break

            if neg:
                continue

            if len(selected) == len(correct_opts):
                score += question.positive_marking

        elif question.question_type == 'NUM':
            if not answer.num_answer is None:
                if answer.num_answer == question.num_answer:
                    score += question.positive_marking
                else:
                    score -= question.negative_marking

        else:
            if not answer.bool_answer is None:
                if answer.bool_answer == question.bool_answer:
                    score += question.positive_marking
                else:
                    score -= question.negative_marking

    return score