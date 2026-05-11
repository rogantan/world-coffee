// test_validate.ts
import type { Ref } from 'vue';
import type { Test, TestErrors } from '../models/test_validate';

export async function validateTest(
    test: Ref<Test>,
    entityErrors: TestErrors
): Promise<boolean> {
    let isValid = true;

    entityErrors.name = "";
    entityErrors.questions = [];

    if (!test.value.name) {
        entityErrors.name = "Название теста обязательно к заполнению";
        isValid = false;
    }


    if (test.value.questions && Array.isArray(test.value.questions)) {
        test.value.questions.forEach((question, qIndex) => {
            let hasCorrectAnswer = false;
            
            // Инициализация объекта ошибок для вопроса
            if (!entityErrors.questions[qIndex]) {
                entityErrors.questions[qIndex] = { 
                    text: "", 
                    choices: [],
                    correctChoiceRequired: ""
                };
            }

            // Валидация текста вопроса
            if (!question.text) {
                entityErrors.questions[qIndex].text = "Текст вопроса обязателен к заполнению";
                isValid = false;
            }

            // Проверка ответов
            if (!question.choices || question.choices.length === 0) {
                if (!entityErrors.questions[qIndex].choices) {
                    entityErrors.questions[qIndex].choices = [];
                }
                entityErrors.questions[qIndex].choices.push({ text: "Должен быть хотя бы один ответ" });
                isValid = false;
            } else {
                question.choices.forEach((answer, aIndex) => {
                    if (!entityErrors.questions[qIndex].choices) {
                        entityErrors.questions[qIndex].choices = [];
                    }
                    
                    if (!entityErrors.questions[qIndex].choices[aIndex]) {
                        entityErrors.questions[qIndex].choices[aIndex] = { text: "" };
                    }

                    if (!answer.text) {
                        entityErrors.questions[qIndex].choices[aIndex].text = "Текст ответа обязателен к заполнению";
                        isValid = false;
                    }

                    if (answer.is_correct) {
                        hasCorrectAnswer = true;
                    }
                });
            }

            // Проверка наличия правильного ответа
            if (!hasCorrectAnswer && question.choices && question.choices.length > 0) {
                entityErrors.questions[qIndex].correctChoiceRequired = "Выберите хотя бы один правильный ответ";
                isValid = false;
            }
        });
        if (test.value.questions.length < 3) {
            entityErrors.name = "Должно быть не менее трёх вопросов";
            isValid = false;
        }
    }

    return isValid;
}