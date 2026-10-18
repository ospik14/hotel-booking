import { api } from './client'

export interface Room {
  id: number
  name: string
  description: string | null
  capacity: number
  price_per_night: number | string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface RoomFilters {
  name_contains?: string
  capacity_gte?: number
  capacity_lte?: number
  price_gte?: number
  price_lte?: number
  guests?: number
  is_active?: boolean
  check_in?: string
  check_out?: string
  limit?: number
  offset?: number
}

export interface RoomCreationRequest {
  name: string
  description?: string | null
  capacity: number
  price_per_night: number
  is_active?: boolean
}

export interface RoomUpdateRequest {
  name?: string
  description?: string | null
  capacity?: number
  price_per_night?: number
  is_active?: boolean
}

export async function fetchRooms(filters: RoomFilters = {}): Promise<Room[]> {
  const response = await api.get<Room[]>('/rooms/', { params: filters })
  return response.data
}

export async function fetchAvailableRooms(
  filters: RoomFilters & { check_in: string; check_out: string },
): Promise<Room[]> {
  const response = await api.get<Room[]>('/rooms/available/', { params: filters })
  return response.data
}

export async function fetchRoomById(id: number): Promise<Room> {
  const response = await api.get<Room>(`/rooms/${id}/`)
  return response.data
}

export async function createRoom(payload: RoomCreationRequest): Promise<Room> {
  const response = await api.post<Room>('/rooms/', payload)
  return response.data
}

export async function updateRoom(id: number, payload: RoomUpdateRequest): Promise<Room> {
  const response = await api.patch<Room>(`/rooms/${id}/`, payload)
  return response.data
}

export async function deactivateRoom(id: number): Promise<Room> {
  const response = await api.delete<Room>(`/rooms/${id}/`)
  return response.data
}
