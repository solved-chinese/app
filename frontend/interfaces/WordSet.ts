export interface SimpleWordSet {
  url: string;

  pk: number;

  name: string;
}

export interface WordSet extends SimpleWordSet {
  words: Word[];

  IC_level: number;
}

export type Word = {
  pk: number;
  // status: "mastered" | "familiar" | "remaining";
  chinese: string;
  pinyin: string;
  full_definition: string;
  url: string;
};
