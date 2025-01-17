export interface Hobby {
    id: number;
    name: string;
    user_has_hobby: boolean;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  date_of_birth?: string | null;
  hobbies: Hobby[];
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}