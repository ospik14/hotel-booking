import { api } from './client'
import type { Room } from './rooms.api'

export type BookingStatus = 'CONFIRMED' | 'CANCELLED' | 'COMPLETED'

export interface Booking {
  id: number
  user_id: number
  room_id: number
  check_in_date: string
  check_out_date: string
  guests: number
  status: BookingStatus
  price_per_night: number | string
  total_price: number | string
  created_at: string
  updated_at: string
  room: Room
}

export interface BookingCreateRequest {
  room_id: number
  check_in_date: string
  check_out_date: string
  guests: number
}

export interface BookingStatusUpdateRequest {
  status: BookingStatus
}

export async function createBooking(payload: BookingCreateRequest): Promise<Booking> {
  const response = await api.post<Booking>('/booking/', payload)
  return response.data
}

export async function fetchMyBookings(): Promise<Booking[]> {
  const response = await api.get<Booking[]>('/booking/my/')
  return response.data
}

export async function fetchBookingById(id: number): Promise<Booking> {
  const response = await api.get<Booking>(`/booking/${id}/`)
  return response.data
}

export async function cancelBooking(id: number): Promise<void> {
  await api.delete(`/booking/${id}/`)
}

export async function fetchAllBookings(): Promise<Booking[]> {
  const response = await api.get<Booking[]>('/booking/')
  return response.data
}

export async function updateBookingStatus(
  id: number,
  payload: BookingStatusUpdateRequest,
): Promise<Booking> {
  const response = await api.patch<Booking>(`/booking/${id}/status/`, payload)
  return response.data
}
