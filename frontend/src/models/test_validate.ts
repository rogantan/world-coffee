// test_validate.ts

export interface Choice {
    text: string;
    is_correct: boolean;
  }
  
export interface Question {
    text: string;
    choices: Choice[];
  }
  
export interface Test {
    id?: number | null;
    name: string;
    date_from: string;
    date_to: string;
    result_resets?: boolean;
    questions?: Array<{
      text?: string;
      choices?: Array<{
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
      choices?: Array<{
        text?: string;
        is_correct?: boolean;
      }>;
      correctChoiceRequired?: string;
    }>;
  }