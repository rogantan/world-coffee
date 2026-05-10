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
                    class="card-body p-0"
                  >

                    <CheckBox
                      v-if="question.multiple_answer"
                      :label="answer.text"
                      :value="selectedAnswers.includes(answer.id)"
                      @change="handleAnswerChange(question.id, answer.id, true)"
                    />

                    <RadiobuttonBox
                      v-else
                      :name="`question-${question.id}`"
                      :label="answer.text"
                      :value="answer.id"
                      :modelValue="getSelectedAnswer(question.id)"
                      @update:modelValue="handleAnswerChange(question.id, $event, false)"
                    />

                  </div>
                </div>

              </div>
            </div>

            <ButtonBox
              title="Завершить"
              :disabled="isTestFinished"
              @click="finishTest"
            />

          </div>
        </div>
      </div>

      <Notify />
    </div>
  </div>
</template>

<script lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import ButtonBox from '../fields/ButtonBox.vue';
import CheckBox from '../fields/CheckBox.vue';
import RadiobuttonBox from '../fields/RadiobuttonBox.vue';
import Notify from '../modals/Notify.vue';

import { notificationService } from '../../api/notify';
import { tests } from '../../api';

interface Choice {
  id: number;
  text: string;
}

interface Question {
  id: number;
  text: string;
  multiple_answer: boolean;
  choices: Choice[];
}

interface Test {
  name: string;
  questions: Question[];
}

export default {
  name: 'TestStartedPage',

  components: {
    ButtonBox,
    CheckBox,
    RadiobuttonBox,
    Notify,
  },

  setup() {
    const route = useRoute();
    const router = useRouter();

    const pageTitle = computed(() => route.meta.name as string);

    const testId = ref<number | null>(null);

    const isTestFinished = ref(false);

    const test = ref<Test>({
      name: '',
      questions: [],
    });

    const selectedAnswers = ref<number[]>([]);

    const getStartedTests = async (): Promise<void> => {
      if (!testId.value) {
        return;
      }

      try {
        const response: Test = await tests.startTest(testId.value);

        test.value = response;
      } catch (error) {
        notificationService.addNotification({
          title: 'Ошибка',
          message: `Не удалось загрузить тест: ${error}`,
          type: 'error',
        });
      }
    };

    const handleAnswerChange = (
      questionId: number,
      answerId: number,
      multipleAnswer: boolean,
    ): void => {

      if (multipleAnswer) {
        if (selectedAnswers.value.includes(answerId)) {
          selectedAnswers.value = selectedAnswers.value.filter(
            id => id !== answerId,
          );
        } else {
          selectedAnswers.value.push(answerId);
        }

        return;
      }

      const question = test.value.questions.find(
        q => q.id === questionId,
      );

      if (!question) {
        return;
      }

      const questionAnswerIds = question.choices.map(
        choice => choice.id,
      );

      selectedAnswers.value = selectedAnswers.value.filter(
        id => !questionAnswerIds.includes(id),
      );

      selectedAnswers.value.push(answerId);
    };

    const getSelectedAnswer = (
      questionId: number,
    ): number | null => {

      const question = test.value.questions.find(
        q => q.id === questionId,
      );

      if (!question) {
        return null;
      }

      return (
        selectedAnswers.value.find(answerId =>
          question.choices.some(
            choice => choice.id === answerId,
          ),
        ) ?? null
      );
    };

    const finishTest = async (): Promise<void> => {

      const isEveryQuestionAnswered = test.value.questions.every(
        question =>
          question.choices.some(choice =>
            selectedAnswers.value.includes(choice.id),
          ),
      );

      if (!isEveryQuestionAnswered) {
        notificationService.addNotification({
          title: 'Ошибка',
          message: 'Пожалуйста, ответьте на все вопросы.',
          type: 'error',
        });

        return;
      }

      if (!testId.value) {
        return;
      }

      try {
        isTestFinished.value = true;

        await tests.finishTest(
          testId.value,
          selectedAnswers.value,
        );

        notificationService.addNotification({
          title: 'Тест завершён',
          message: '',
          type: 'success',
        });

        setTimeout(() => {
          router.push({
            name: 'TestsShowResult',
            query: {
              test_id: String(testId.value),
            },
          });
        }, 1500);

      } catch (error) {

        isTestFinished.value = false;

        notificationService.addNotification({
          title: 'Ошибка',
          message: `${error}`,
          type: 'error',
        });
      }
    };

    onMounted(async () => {

      document.title = pageTitle.value;

      const rawTestId = route.query.test_id;

      if (typeof rawTestId === 'string') {
        testId.value = Number(rawTestId);
      }

      await getStartedTests();
    });

    return {
      pageTitle,
      test,
      testId,
      selectedAnswers,
      isTestFinished,
      finishTest,
      handleAnswerChange,
      getSelectedAnswer,
    };
  },
};
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
</style>