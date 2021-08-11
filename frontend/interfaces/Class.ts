import { Assignment } from "./Assignment";
import { User } from "./User";
import { SimpleWordSet } from "./WordSet";

export interface Class {
  /** Resource url. */
  url: string;

  pk: number;

  name: string;

  code: string;

  teacher: string;
}

// TODO : class short and class complete
export interface FullClass extends Class {
  students: User[];
  student_ids: number[];
  assignements: SimpleWordSet[];
}
