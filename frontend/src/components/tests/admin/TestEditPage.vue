<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
    </h2>
    <div class="card outer-card">
      <div class="row">
        <div class="row justify-content-center">
          <div class="col-md-8">
            <InputBox v-bind="validateOptions.name" :modelValue="test.name" :error="entityErrors.name"
              @update:modelValue="(value: any) => { test.name = value; entityErrors.name = ''; }" />
            <DateBox label="Даты прохождения теста" placeholder="" :future="true" :modelValue="dateRange"
              @update:modelValue="handleDateChange" />
            <div v-for="(question, qIndex) in test.questions" :key="qIndex" class="card mt-2 question-card">
              <div class="card-body">
                <TextAreaBox :modelValue="question.text"
                  @update:modelValue="(value: any) => { question.text = value; if (entityErrors.questions[qIndex]) entityErrors.questions[qIndex].text = ''; }"
                  label="Текст вопроса" />
                <div v-if="entityErrors.questions[qIndex]?.text" class="alert alert-danger" role="alert">
                  {{ entityErrors.questions[qIndex]?.text }}
                </div>
                <ButtonBox color="outline-danger" title="Удалить вопрос" @click="removeQuestion(qIndex)" />
                <div v-for="(answer, aIndex) in question.choices" :key="aIndex" class="card mt-2 answer-card">
                  <div class="card-body">
                    <TextAreaBox v-model="answer.text"
                      @update:modelValue="(value: any) => { answer.text = value; if (entityErrors.questions[qIndex]?.choices[aIndex]) entityErrors.questions[qIndex].choices[aIndex].text = ''; }"
                      label="Текст ответа" />
                    <div v-if="entityErrors.questions[qIndex]?.choices[aIndex]?.text" class="alert alert-danger"
                      role="alert">
                      {{ entityErrors.questions[qIndex]?.choices[aIndex]?.text }}
                    </div>
                    <CheckBoxC label="Правильный ответ?"
                      @update:modelValue="(value: any) => { answer.is_correct = value; if (entityErrors.questions[qIndex]) entityErrors.questions[qIndex].correctChoiceRequired = '' }"
                      :modelValue="answer.is_correct" />
                    <div v-if="entityErrors.questions[qIndex]?.correctChoiceRequired" class="alert alert-danger"
                      role="alert">
                      {{ entityErrors.questions[qIndex]?.correctChoiceRequired }}
                    </div>
                    <div>
                      <ButtonBox color="outline-danger" title="Удалить ответ" @click="removeAnswer(qIndex, aIndex)" />
                    </div>
                  </div>
                </div>
                <ButtonBox color="outline-primary" title="Добавить ответ" @click="addAnswer(qIndex)" />
              </div>
            </div>
            <ButtonBox color="outline-primary" title="Добавить вопрос" @click="addQuestion" />
            <div class="p-2">
              <ButtonBox color="outline-success" title="Сохранить изменения" @click="saveTest" />
            </div>
          </div>
        </div>
      </div>
      <Notify />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

import InputBox from '../../fields/InputBox.vue';
import DateBox from '../../fields/DateBox.vue';
import TextAreaBox from '../../fields/TextAreaBox.vue';
import ButtonBox from '../../fields/ButtonBox.vue';
import CheckBoxC from '../../fields/CheckBoxC.vue';
import Notify from '../../modals/Notify.vue';

import { notificationService } from '../../../api/notify';
import { tests } from '../../../api';

import { formatOnlyDate } from '../../../utils/date_formatter';
import { validateTest } from '../../../utils/test_validate';

import type { Test, TestErrors } from '../../../models/test_validate';
import router from '../../../router';

interface Choice {
  text: string;
  is_correct: boolean;
}

interface Question {
  text: string;
  choices: Choice[];
}

const route = useRoute();

const pageTitle = computed<string>(() =>
  String(route.meta.name ?? ''),
);

const testId = ref<number | null>(null);

const dateRange = ref<Date[]>([
  new Date(new Date().getFullYear(), new Date().getMonth(), 1),
  new Date(),
]);

const createEmptyChoice = (): Choice => ({
  text: '',
  is_correct: false,
});

const createEmptyQuestion = (): Question => ({
  text: '',
  choices: [createEmptyChoice()],
});

const test = ref<Test>({
  id: null,
  result_resets: false,
  date_from: '',
  date_to: '',
  name: '',
  questions: [createEmptyQuestion()],
});

const entityErrors = reactive<TestErrors>({
  name: '',
  date_from: '',
  date_to: '',
  questions: [
    {
      text: '',
      choices: [
        {
          text: '',
          is_correct: false,
        },
      ],
      correctChoiceRequired: '',
    },
  ],
});

const validateOptions = {
  name: {
    label: 'Название теста',
    validate: {
      required: true,
    },
  },
};

const createQuestionErrors = (choicesCount = 1) => ({
  text: '',
  choices: Array.from(
    { length: choicesCount },
    () => ({
      text: '',
      is_correct: false,
    }),
  ),
  correctChoiceRequired: '',
});

const handleDateChange = (
  newRange: Date | Date[] | undefined,
): void => {

  if (!newRange) {
    return;
  }

  if (!Array.isArray(newRange)) {
    return;
  }

  if (newRange.length < 2) {
    return;
  }

  const [from, to] = newRange;

  if (!from || !to) {
    return;
  }

  dateRange.value = newRange;

  test.value.date_from = formatOnlyDate(from);
  test.value.date_to = formatOnlyDate(to);
};

const syncErrors = (): void => {

  entityErrors.questions = test.value.questions.map(
    question =>
      createQuestionErrors(question.choices.length),
  );
};

const getData = async (): Promise<void> => {

  if (!testId.value) {
    return;
  }

  try {

    const response = await tests.getTest(
      testId.value,
    ) as Test;

    test.value = response;

    if (
      test.value.date_from &&
      test.value.date_to
    ) {

      dateRange.value = [
        new Date(test.value.date_from),
        new Date(test.value.date_to),
      ];
    }

    syncErrors();

  } catch (error) {

    notificationService.addNotification({
      title: 'Ошибка',
      message: `Не удалось загрузить тест: ${error}`,
      type: 'error',
    });
  }
};

const addQuestion = (): void => {

  test.value.questions.push(
    createEmptyQuestion(),
  );

  entityErrors.questions.push(
    createQuestionErrors(),
  );
};

const removeQuestion = (qIndex: number): void => {

  test.value.questions.splice(qIndex, 1);

  entityErrors.questions.splice(qIndex, 1);
};

const addAnswer = (qIndex: number): void => {

  test.value.questions[qIndex].choices.push(
    createEmptyChoice(),
  );

  entityErrors.questions[qIndex].choices.push({
    text: '',
    is_correct: false,
  });
};

const removeAnswer = (
  qIndex: number,
  aIndex: number,
): void => {

  test.value.questions[qIndex].choices.splice(
    aIndex,
    1,
  );

  entityErrors.questions[qIndex].choices.splice(
    aIndex,
    1,
  );
};

const saveTest = async (): Promise<void> => {

  if (!testId.value) {
    return;
  }

  const isValid = await validateTest(
    test,
    entityErrors,
  );

  if (!isValid) {
    return;
  }

  try {

    const res = await tests.editTest(
      testId.value,
      test.value,
    );

    notificationService.addNotification({
      title: 'Тест успешно отредактирован',
      message: '',
      type: 'success',
    });

    await getData();

  } catch (error) {

    notificationService.addNotification({
      title: 'Ошибка',
      message: "Тест нельзя изменить",
      type: 'error',
    });
    router.push("/tests")
  }
};

onMounted(async () => {

  document.title = pageTitle.value;

  const rawTestId = route.query.test_id;

  if (typeof rawTestId === 'string') {
    testId.value = Number(rawTestId);
  }

  await getData();
});
</script>

<style scoped>
.outer-card {
  margin-bottom: 20px;
}

.question-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  margin-top: 10px;
}

.answer-card {
  background-color: #e9ecef;
  margin-top: 10px;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: start;
  padding: 10px;
  gap: 20px;
  background-color: #e9ecef;
}
</style>