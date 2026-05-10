<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
    </h2>

    <div class="outer-card card">
      <div class="row justify-content-center">
        <div class="col-md-8">

          <!-- Название -->
          <InputBox
            v-bind="validateOptions.name"
            :modelValue="test.name"
            :error="entityErrors.name"
            @update:modelValue="onNameChange"
          />

          <!-- Даты -->
          <DateBox
            label="Даты прохождения теста"
            :future="true"
            :modelValue="dateRange"
            @update:modelValue="handleDateChange"
          />

          <!-- Вопросы -->
          <div
            v-for="(question, qIndex) in test.questions"
            :key="qIndex"
            class="question-card card"
          >
            <div class="card-body">

              <TextAreaBox
                :modelValue="question.text"
                label="Текст вопроса"
                @update:modelValue="(v: string) => onQuestionChange(qIndex, v)"
              />

              <div v-if="entityErrors.questions[qIndex]?.text" class="alert alert-danger">
                {{ entityErrors.questions[qIndex].text }}
              </div>

              <ButtonBox
                color="outline-danger"
                title="Удалить вопрос"
                @click="removeQuestion(qIndex)"
              />

              <!-- Ответы -->
              <div
                v-for="(answer, aIndex) in question.choices"
                :key="aIndex"
                class="answer-card card-body"
              >
                <TextAreaBox
                  :modelValue="answer.text"
                  label="Текст ответа"
                  @update:modelValue="(v: any) => onAnswerChange(qIndex, aIndex, v)"
                />

                <div v-if="entityErrors.questions[qIndex]?.choices[aIndex]?.text" class="alert alert-danger">
                  {{ entityErrors.questions[qIndex].choices[aIndex].text }}
                </div>

                <CheckBoxC
                  label="Правильный ответ?"
                  :modelValue="answer.is_correct"
                  @update:modelValue="(v) => onCorrectChange(qIndex, aIndex, v)"
                />

                <ButtonBox
                  color="outline-danger"
                  title="Удалить ответ"
                  @click="removeAnswer(qIndex, aIndex)"
                />
              </div>

              <div v-if="entityErrors.questions[qIndex]?.correctChoiceRequired" class="alert alert-danger">
                {{ entityErrors.questions[qIndex].correctChoiceRequired }}
              </div>

              <ButtonBox
                color="outline-primary"
                title="Добавить ответ"
                @click="addAnswer(qIndex)"
              />

            </div>
          </div>

          <ButtonBox
            color="outline-primary"
            title="Добавить вопрос"
            @click="addQuestion"
          />

          <div class="p-2">
            <ButtonBox
              color="outline-success"
              title="Создать"
              @click="createTest"
            />
          </div>

        </div>
      </div>

      <Notify />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import InputBox from '../../fields/InputBox.vue';
import TextAreaBox from '../../fields/TextAreaBox.vue';
import DateBox from '../../fields/DateBox.vue';
import ButtonBox from '../../fields/ButtonBox.vue';
import CheckBoxC from '../../fields/CheckBoxC.vue';
import Notify from '../../modals/Notify.vue';

import { notificationService } from '../../../api/notify';
import { tests } from '../../../api';
import { validateTest } from '../../../utils/test_validate';
import { formatOnlyDate } from '../../../utils/date_formatter';


type Choice = {
  text: string;
  is_correct: boolean;
};

type Question = {
  text: string;
  choices: Choice[];
};

type Test = {
  id: number | null;
  name: string;
  date_from: string;
  date_to: string;
  questions: Question[];
};

type ChoiceError = {
  text: string;
};

type QuestionError = {
  text: string;
  correctChoiceRequired: string;
  choices: ChoiceError[];
};

type TestErrors = {
  name: string;
  questions: QuestionError[];
};


const route = useRoute();
const router = useRouter();

const pageTitle = computed<string>(() => route.meta.name as string);


const dateRange = ref<[Date, Date]>([
  new Date(new Date().getFullYear(), new Date().getMonth(), 1),
  new Date()
]);

const validateOptions = { name: { label: "Название теста", validate: { required: true }, }, date_from: { label: "Дата начала", validate: { required: true }, }, date_to: { label: "Дата окончания", validate: { required: true }, }, questions: { validate: { minCount: 1 }, }, };

const test = ref<Test>({
  id: null,
  name: '',
  date_from: '',
  date_to: '',
  questions: [
    {
      text: '',
      choices: [{ text: '', is_correct: false }]
    }
  ]
} as Test);

const entityErrors = reactive<TestErrors>({
  name: '',
  questions: [
    {
      text: '',
      correctChoiceRequired: '',
      choices: [{ text: '' }]
    }
  ]
});


const onNameChange = (value: string) => {
  test.value.name = value;
  entityErrors.name = '';
};

const onQuestionChange = (qIndex: number, value: string) => {
  test.value.questions[qIndex].text = value;
  entityErrors.questions[qIndex].text = '';
};

const onAnswerChange = (qIndex: number, aIndex: number, value: string) => {
  test.value.questions[qIndex].choices[aIndex].text = value;
  entityErrors.questions[qIndex].choices[aIndex].text = '';
};

const onCorrectChange = (qIndex: number, aIndex: number, value: any) => {
  test.value.questions[qIndex].choices[aIndex].is_correct = value;
  entityErrors.questions[qIndex].correctChoiceRequired = '';
};

const handleDateChange = (range: [Date, Date]) => {
  dateRange.value = range;
};


const addQuestion = () => {
  test.value.questions.push({
    text: '',
    choices: [{ text: '', is_correct: false }]
  });

  entityErrors.questions.push({
    text: '',
    correctChoiceRequired: '',
    choices: [{ text: '' }]
  });
};

const removeQuestion = (index: number) => {
  test.value.questions.splice(index, 1);
  entityErrors.questions.splice(index, 1);
};

const addAnswer = (qIndex: number) => {
  test.value.questions[qIndex].choices.push({
    text: '',
    is_correct: false
  });

  entityErrors.questions[qIndex].choices.push({
    text: ''
  });
};

const removeAnswer = (qIndex: number, aIndex: number) => {
  test.value.questions[qIndex].choices.splice(aIndex, 1);
  entityErrors.questions[qIndex].choices.splice(aIndex, 1);
};


const createTest = async () => {
  if (!(await validateTest(test, entityErrors))) return;

  const data = {
    name: test.value.name,
    date_from: formatOnlyDate(dateRange.value[0]),
    date_to: `${formatOnlyDate(dateRange.value[1])} 23:59:00`,
    questions: test.value.questions.map(q => ({
      text: q.text,
      choices: q.choices
    }))
  };

  try {
    await tests.createTest(data);

    notificationService.addNotification({
      title: 'Тест успешно создан',
      message: '',
      type: 'success'
    });

    setTimeout(() => router.push('/tests'), 1500);

  } catch (error: any) {
    if (error?.response?.status === 409) {
      notificationService.addNotification({
        title: 'Ошибка',
        message: 'Тест с таким названием уже существует',
        type: 'error'
      });
    } else {
      notificationService.addNotification({
        title: 'Ошибка',
        message: error?.message || 'Неизвестная ошибка',
        type: 'error'
      });
    }
  }
};

onMounted(() => {
  document.title = pageTitle.value;
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
  padding: 10px;
  gap: 20px;
  background-color: #e9ecef;
}
</style>