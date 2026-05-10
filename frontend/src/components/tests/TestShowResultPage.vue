<template>
  <div class="mt-2">

    <h2 class="header-container">
      {{ pageTitle }}
    </h2>

    <div class="outer-card card">

      <div class="row justify-content-center">
        <div class="col-md-10">

          <div class="card-body mt-4">

            <h2>Тест: {{ test.name }}</h2>

            <div
              v-for="question in test.questions"
              :key="question.id"
              class="question-card card"
            >
              <div class="card-body">

                <h3>Вопрос: {{ question.text }}</h3>

                <div class="answer-card card">

                  <h4>Варианты:</h4>

                  <div
                    v-for="answer in question.choices"
                    :key="answer.id"
                    :class="getAnswerClass(question.multiple_answer, answer)"
                    class="answer-item"
                  >

                    <CheckBox
                      v-if="question.multiple_answer"
                      :label="answer.text"
                      :value="answer.selected"
                      :disabled="true"
                    />

                    <RadiobuttonBox
                      v-else
                      :name="`question-${question.id}`"
                      :label="answer.text"
                      :value="answer.id"
                      :modelValue="answer.selected ? answer.id : null"
                      :disabled="true"
                    />

                  </div>

                </div>
              </div>
            </div>

            <ButtonBox
              title="К тестам"
              @click="toTests"
            />

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import ButtonBox from '../fields/ButtonBox.vue';
import CheckBox from '../fields/CheckBox.vue';
import RadiobuttonBox from '../fields/RadiobuttonBox.vue';

import { test_user } from '../../api';
import { notificationService } from '../../api/notify';

interface Choice {
  id: number;
  text: string;
  is_correct: boolean;
  selected: boolean;
}

interface Question {
  id: number;
  text: string;
  multiple_answer: boolean;
  choices: Choice[];
}

interface TestResult {
  name: string;
  questions: Question[];
}

const route = useRoute();
const router = useRouter();

const pageTitle = computed<string>(() =>
  String(route.meta.name ?? ''),
);

const testId = ref<number | null>(null);

const test = ref<TestResult>({
  name: '',
  questions: [],
});

const getData = async (): Promise<void> => {

  if (!testId.value) {
    return;
  }

  try {

    const response = await test_user.getResult(
      testId.value,
    ) as TestResult;

    test.value = response;

  } catch (error) {

    notificationService.addNotification({
      title: 'Ошибка',
      message: `Не удалось загрузить результат теста: ${error}`,
      type: 'error',
    });
  }
};

const getAnswerClass = (
  multipleAnswer: boolean,
  answer: Choice,
): string => {

  if (multipleAnswer) {

    if (
      (answer.is_correct && answer.selected) ||
      (answer.is_correct && !answer.selected)
    ) {
      return 'correct-answer';
    }

    if (!answer.is_correct && answer.selected) {
      return 'incorrect-answer';
    }

    return '';
  }

  if (answer.is_correct) {
    return 'correct-answer';
  }

  if (!answer.is_correct && answer.selected) {
    return 'incorrect-answer';
  }

  return '';
};

const toTests = (): void => {
  router.push('/tests');
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
  margin-top: 10px;
  border: 1px solid #dee2e6;
  background-color: #f8f9fa;
}

.answer-card {
  margin-top: 10px;
  padding: 10px;
  background-color: #e9ecef;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;

  padding: 10px;

  background-color: #e9ecef;
}

.answer-item {
  margin-bottom: 8px;
  padding: 6px;

  border-radius: 6px;
}

.correct-answer {
  background-color: #d4edda;
}

.incorrect-answer {
  background-color: #f8d7da;
}
</style>