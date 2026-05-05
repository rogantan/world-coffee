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
    name?: string | undefined;
    date_from?: string | undefined;
    date_to?: string | undefined;
    questions: Array<{
      text?: string | undefined;
      choices?: Array<{
        text?: string | undefined;
        is_correct?: boolean | undefined;
      }>;
      correctChoiceRequired?: string | undefined;
    }> | undefined;
  }