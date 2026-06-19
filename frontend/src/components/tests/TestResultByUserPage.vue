<template>
  <div class="mt-2">
    <div class="outer-card card">
      <div class="row">
        <div class="row justify-content-center">
          <div class="col-md-10">
            <div class="card-body mt-4">
              <h2>Сотрудник: {{ employeeName }} Тест: {{ test.name }}</h2>
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
                    >
                      <div
                        v-if="question.multiple_answer"
                        :class="{
                          'correct-answer':
                            answer.is_correct && answer.selected,
                          'incorrect-answer':
                            (!answer.is_correct && answer.selected) ||
                            (answer.is_correct && !answer.selected),
                        }"
                      >
                        <CheckBox
                          :label="answer.text"
                          :value="answer.selected"
                          :modelValue="answer.selected ? answer.id : null"
                          :disabled="true"
                        />
                      </div>
                      <div
                        v-else
                        :class="{
                          'correct-answer':
                            (answer.is_correct && !answer.selected) ||
                            (answer.is_correct && answer.selected),
                          'incorrect-answer':
                            !answer.is_correct && answer.selected,
                        }"
                      >
                        <RadiobuttonBox
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
              </div>
              <ButtonBox title="К тестам" @click="toTests" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted, computed, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import ButtonBox from "../fields/ButtonBox.vue";
import CheckBox from "../fields/CheckBox.vue";
import RadiobuttonBox from "../fields/RadiobuttonBox.vue";
import { tests } from "../../api/index";

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

export default {
  name: "TestsShowResultByUserPage",
  components: {
    ButtonBox,
    CheckBox,
    RadiobuttonBox,
  },
  props: {
    employeeId: {
      type: String,
      require: true,
    },
    testId: {
      type: Number,
      require: true,
    },
    employeeName: {
      type: String,
      require: true,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const pageTitle = computed(() => route.meta.name);
    // const testId = ref<number | null>(null);

    const test = ref({
      name: "",
      questions: [],
    });

    const getData = async () => {
      console.log(props.testId, props.employeeId)
      const response = await tests.getResultByUser(
        props.testId,
        props.employeeId
      );
      // @ts-ignore
      test.value = response;
    };

    const toTests = () => {
      router.push("/tests/result");
    };

    onMounted(async () => {
      document.title = pageTitle.value as string;
      await getData();
    });


    return {
      pageTitle,
      test,
      toTests,
      employeeName: props.employeeName,
    };
  },
};
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
  padding: 10px;
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

.correct-answer {
  background-color: #d4edda;
}

.incorrect-answer {
  background-color: #f8d7da;
}
</style>
