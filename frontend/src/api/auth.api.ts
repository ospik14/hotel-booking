import { api } from './client'

export type UserRole = 'admin' | 'user'

export interface UserProfile {
  id: number
  first_name: string
  last_name: string
  email: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UpdateProfileRequest {
  first_name?: string
  last_name?: string
}

export interface ChangePasswordRequest {
  current_password: string
  new_password: string
}

export async function loginUser(payload: LoginRequest): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>('/users/login', payload)
  return response.data
}

export async function registerUser(payload: RegisterRequest): Promise<UserProfile> {
  const response = await api.post<UserProfile>('/users/register', payload)
  return response.data
}

export async function getCurrentUser(): Promise<UserProfile> {
  const response = await api.get<UserProfile>('/users/me/')
  return response.data
}

export async function updateCurrentUser(payload: UpdateProfileRequest): Promise<UserProfile> {
  const response = await api.patch<UserProfile>('/users/me/', payload)
  return response.data
}

export async function changePassword(payload: ChangePasswordRequest): Promise<void> {
  await api.post('/users/change-password/', payload)
}
