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
import { onMounted, reactive, computed, ref, type Ref } from 'vue';
import { useRoute } from 'vue-router';
import InputBox from '../../fields/InputBox.vue';
import DateBox from '../../fields/DateBox.vue';
import TextAreaBox from '../../fields/TextAreaBox.vue'
import ButtonBox from '../../fields/ButtonBox.vue';
import CheckBoxC from '../../fields/CheckBoxC.vue';
import Notify from '../../modals/Notify.vue'
import { notificationService } from '../../../api/notify';
import { tests } from '../../../api/index'
import { formatOnlyDate } from '../../../utils/date_formatter'
import { validateTest } from '../../../utils/test_validate';
import type { Test, TestErrors } from '../../../models/test_validate'

const route = useRoute();
const pageTitle = computed(() => route.meta.name as string);

const dateRange = ref<Date[]>([
  new Date(new Date().getFullYear(), new Date().getMonth(), 1),
  new Date()
]);
const testId = ref<number | null>(null);
const test: Ref<Test> = ref({
  id: null,
  result_resets: false,
  date_from: '',
  date_to: '',
  name: '',
  questions: [  // Инициализируем questions как массив
    {
      text: '',
      choices: [
        { text: '', is_correct: false }
      ]
    }
  ]
});

// Определяем интерфейсы для ошибок
interface QuestionError {
  text: string;
  choices: ChoiceError[];
  correctAnswerRequired?: string;
  correctChoiceRequired?: string;
}

interface ChoiceError {
  text: string;
  is_correct: boolean;
}

const entityErrors = reactive<TestErrors>({
  name: "",
  date_from: "",
  date_to: "",
  questions: [{
    text: '',
    choices: [
      { text: '', is_correct: false }
    ],
    correctChoiceRequired: ''
  }]
});

const validateOptions = {
  name: {
    label: "Название теста",
    validate: { required: true },
  },
  questions: {
    validate: { minCount: 1 },
  },
};

const handleDateChange = (newRange: Date[]) => {
  dateRange.value = newRange;
  test.value.date_from = formatOnlyDate(dateRange.value[0])
  test.value.date_to = formatOnlyDate(dateRange.value[1])
};

const getData = async () => {
  if (!testId.value) return;
  
  const response = await tests.getTest(testId.value);
  test.value = response;
  
  // Гарантируем, что questions существует
  if (!test.value.questions) {
    test.value.questions = [];
  }
  
  if (test.value.date_from && test.value.date_to) {
    dateRange.value = [new Date(test.value.date_from), new Date(test.value.date_to)]
    test.value.date_from = formatOnlyDate(dateRange.value[0])
    test.value.date_to = formatOnlyDate(dateRange.value[1])
  }
  
  // Сбрасываем entityErrors с правильной структурой
  entityErrors.questions = test.value.questions.map(() => ({
    text: '',
    choices: [],
    correctAnswerRequired: '',
    correctChoiceRequired: ''
  }));
  
  // Инициализируем choices для каждого вопроса
  test.value.questions.forEach((question, qIndex) => {
    if (entityErrors.questions[qIndex] && question.choices) {
      entityErrors.questions[qIndex].choices = question.choices.map(() => ({
        text: '',
        is_correct: false
      }));
    }
  });
};

const addQuestion = () => {
  // Гарантируем, что questions существует
  if (!test.value.questions) {
    test.value.questions = [];
  }
  test.value.questions.push({ text: '', choices: [{ text: '', is_correct: false }] });
  
  if (!entityErrors.questions) {
    entityErrors.questions = [];
  }
  entityErrors.questions.push({
    text: '',
    choices: [{ text: '', is_correct: false }],
    correctChoiceRequired: ''
  });
};

const removeQuestion = (qIndex: number) => {
  if (test.value.questions) {
    test.value.questions.splice(qIndex, 1);
  }
  if (entityErrors.questions) {
    entityErrors.questions.splice(qIndex, 1);
  }
};

const addAnswer = (qIndex: number) => {
  // Проверяем существование questions
  if (!test.value.questions) return;
  if (!test.value.questions[qIndex]) return;
  if (!test.value.questions[qIndex].choices) {
    test.value.questions[qIndex].choices = [];
  }
  
  test.value.questions[qIndex].choices.push({ text: '', is_correct: false });
  
  // Проверяем существование errors
  if (entityErrors.questions && 
      entityErrors.questions[qIndex] && 
      entityErrors.questions[qIndex].choices) {
    entityErrors.questions[qIndex].choices.push({ text: '', is_correct: false });
  }
};

const removeAnswer = (qIndex: number, aIndex: number) => {
  // Проверяем существование questions
  if (!test.value.questions) return;
  if (!test.value.questions[qIndex]) return;
  if (test.value.questions[qIndex].choices) {
    test.value.questions[qIndex].choices.splice(aIndex, 1);
  }
  
  // Проверяем существование errors
  if (entityErrors.questions && 
      entityErrors.questions[qIndex] && 
      entityErrors.questions[qIndex].choices) {
    entityErrors.questions[qIndex].choices.splice(aIndex, 1);
  }
};

const saveTest = async () => {
  if (!testId.value) return;
  
  // Гарантируем, что questions существует перед валидацией
  if (!test.value.questions) {
    test.value.questions = [];
  }
  
  test.value.date_to = test.value.date_to;

  if (!(await validateTest(test, entityErrors))) {
    return;
  }
  const response = await tests.editTest(testId.value, test.value);
  if (response === null) {
    notificationService.addNotification({
      title: 'Тест успешно отредактирован',
      message: ``,
      type: 'success',
    });
    await getData();
  } else {
    notificationService.addNotification({
      title: 'Ошибочка',
      message: ``,
      type: 'error',
    });
  }
};

onMounted(async () => {
  document.title = pageTitle.value as string
  const rawTestId = route.query.test_id;
  if (typeof rawTestId === 'string') {
    testId.value = parseInt(rawTestId, 10);
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