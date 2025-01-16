import { ApiResponse, Hobby, UserProfile } from "./types.ts";

const API_BASE_URL = '/api';

class ApiService {
    private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
        try {
            // Get CSRF token from cookie
            const csrfToken = document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];

            const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || '', // Add CSRF token header
                ...options.headers,
            };

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers,
                credentials: 'include',
            });

            if (!response.ok) {
                try {
                    const error = await response.json();
                    return {
                        error: error.message || error.detail || 'An error occurred',
                        status: response.status,
                    };
                } catch {
                    return {
                        error: 'An error occurred',
                        status: response.status,
                    };
                }
            }

            const data = await response.json();
            return {
                data,
                status: response.status,
            };
        } catch (error) {
            return {
                error: error instanceof Error ? error.message : 'Network error',
                status: 500,
            };
        }
    }

    // Profile endpoints
    async getCurrentProfile(): Promise<ApiResponse<UserProfile>> {
        return this.request<UserProfile>('/profile/me/');
    }

    async updateProfile(data: Partial<UserProfile>): Promise<ApiResponse<UserProfile>> {
        return this.request<UserProfile>('/profile/update_profile/', {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    // Hobby endpoints
    async getAllHobbies(): Promise<ApiResponse<Hobby[]>> {
        return this.request<Hobby[]>('/hobbies/');
    }

    async addHobby(hobby_name: string, benefits: string, rating: number): Promise<ApiResponse<Hobby>> {
        return this.request<Hobby>('/hobbies/add_to_profile/', {
            method: 'POST',
            body: JSON.stringify({ hobby_name, benefits, rating }),
        });
    }

    // Auth endpoints
    async login(username: string, password: string): Promise<ApiResponse<void>> {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        return this.request<void>('/login/', {
            method: 'POST',
            body: formData,
            headers: {
                // Don't set Content-Type for FormData
                'Content-Type': undefined as any,
            },
        });
    }

    async logout(): Promise<ApiResponse<void>> {
        return this.request<void>('/logout/', {
            method: 'POST',
        });
    }

    async register(userData: {
        username: string;
        email: string;
        password1: string;
        password2: string;
    }): Promise<ApiResponse<void>> {
        const formData = new FormData();
        Object.entries(userData).forEach(([key, value]) => {
            formData.append(key, value);
        });

        return this.request<void>('/register/', {
            method: 'POST',
            body: formData,
            headers: {
                // Don't set Content-Type for FormData
                'Content-Type': undefined as any,
            },
        });
    }
}

export const apiService = new ApiService();
