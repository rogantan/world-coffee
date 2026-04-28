// test_validate.ts

export interface Answer {
  text: string;
  is_correct: boolean;
}

export interface Question {
  text: string;
  answer_options: Answer[];
}

export interface Test {
  id?: number;
  name: string;
  date_from: string;
  date_to: string;
  result_resets?: boolean;
  questions?: Array<{
    text?: string;
    answer_options?: Array<{
      text?: string;
      is_correct?: boolean
    }>;
  }>;
}

export interface TestErrors {
  name?: string;
  date_from?: string;
  date_to?: string;
  questions: Array<{
    text?: string;
    answer_options?: Array<{
      text?: string;
      is_correct?: boolean;
    }>;
    correctAnswerRequired?: string;
  }>;
}