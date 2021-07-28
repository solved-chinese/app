export interface User {
  /** Resource url. */
  url: string;

  username: string;

  email: string;

  displayName: string;

  isTeacher: boolean;

  isStudent: boolean;
}

export type UserType = "teacher" | "student";
