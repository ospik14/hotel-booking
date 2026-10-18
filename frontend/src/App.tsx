import { type FormEvent, type ReactNode, createContext, useContext, useEffect, useMemo, useState } from 'react'
import {
  BrowserRouter,
  Link,
  NavLink,
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from 'react-router-dom'
import { QueryClient, QueryClientProvider, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  ArrowRight,
  BedDouble,
  Building2,
  CalendarDays,
  ChevronRight,
  CircleDollarSign,
  LogOut,
  Menu,
  Search,
  ShieldCheck,
  Sparkles,
  UserRound,
  Users,
  X,
} from 'lucide-react'
import {
  type ChangePasswordRequest,
  type LoginRequest,
  type RegisterRequest,
  type UpdateProfileRequest,
  type UserProfile,
  changePassword,
  getCurrentUser,
  loginUser,
  registerUser,
  updateCurrentUser,
} from './api/auth.api'
import {
  type Booking,
  type BookingCreateRequest,
  type BookingStatus,
  cancelBooking,
  createBooking,
  fetchAllBookings,
  fetchMyBookings,
  updateBookingStatus,
} from './api/bookings.api'
import {
  type Room,
  type RoomCreationRequest,
  type RoomFilters,
  createRoom,
  deactivateRoom,
  fetchAvailableRooms,
  fetchRoomById,
  fetchRooms,
  updateRoom,
} from './api/rooms.api'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 30,
      retry: 1,
    },
  },
})

type AuthContextValue = {
  user: UserProfile | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (payload: LoginRequest) => Promise<void>
  register: (payload: RegisterRequest) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function getDefaultSearch() {
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(today.getDate() + 1)

  return {
    check_in: formatDateInput(today),
    check_out: formatDateInput(tomorrow),
    guests: 2,
  }
}

function formatDateInput(value: Date) {
  const offset = value.getTimezoneOffset()
  const adjusted = new Date(value.getTime() - offset * 60 * 1000)
  return adjusted.toISOString().slice(0, 10)
}

function formatCurrency(value: number | string): string {
  const amount = typeof value === 'string' ? Number(value) : value
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2,
  }).format(amount)
}

function getNightCount(checkIn: string, checkOut: string): number {
  if (!checkIn || !checkOut) {
    return 0
  }

  const start = new Date(checkIn)
  const end = new Date(checkOut)
  const difference = end.getTime() - start.getTime()

  if (Number.isNaN(difference) || difference <= 0) {
    return 0
  }

  return Math.round(difference / (1000 * 60 * 60 * 24))
}

function getRoomImage(id: number): string {
  const images = [
    'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',
  ]

  return images[id % images.length]
}

function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('stayora_token'))
  const [user, setUser] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(Boolean(token))

  useEffect(() => {
    if (!token) {
      setUser(null)
      setIsLoading(false)
      return
    }

    let isMounted = true

    const loadUser = async () => {
      try {
        const profile = await getCurrentUser()
        if (isMounted) {
          setUser(profile)
        }
      } catch {
        if (isMounted) {
          setToken(null)
          setUser(null)
          localStorage.removeItem('stayora_token')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    void loadUser()

    return () => {
      isMounted = false
    }
  }, [token])

  useEffect(() => {
    if (token) {
      localStorage.setItem('stayora_token', token)
    } else {
      localStorage.removeItem('stayora_token')
    }
  }, [token])

  const login = async (payload: LoginRequest) => {
    const response = await loginUser(payload)
    setToken(response.access_token)
    const profile = await getCurrentUser()
    setUser(profile)
  }

  const register = async (payload: RegisterRequest) => {
    await registerUser(payload)
    await login({ email: payload.email, password: payload.password })
  }

  const refreshUser = async () => {
    if (!token) {
      return
    }

    const profile = await getCurrentUser()
    setUser(profile)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
  }

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(token) && Boolean(user),
      isLoading,
      login,
      register,
      logout,
      refreshUser,
    }),
    [token, user, isLoading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }

  return context
}

function AppShell({ children }: { children: ReactNode }) {
  const { user, isAuthenticated, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="container nav-shell">
          <Link to="/" className="brand" aria-label="STAYORA home">
            <span className="brand-mark">S</span>
            STAYORA
          </Link>

          <nav className={`nav ${menuOpen ? 'open' : ''}`} aria-label="Main navigation">
            <NavLink to="/" onClick={() => setMenuOpen(false)}>
              Home
            </NavLink>
            <NavLink to="/rooms" onClick={() => setMenuOpen(false)}>
              Rooms
            </NavLink>
            <NavLink to="/account/bookings" onClick={() => setMenuOpen(false)}>
              My bookings
            </NavLink>
            {user?.role === 'admin' ? (
              <NavLink to="/admin" onClick={() => setMenuOpen(false)}>
                Admin
              </NavLink>
            ) : null}
          </nav>

          <div className="nav-actions">
            {isAuthenticated ? (
              <>
                <Link to="/profile" className="button button-ghost">
                  <UserRound size={16} />
                  {user?.first_name}
                </Link>
                <button type="button" className="button button-secondary" onClick={logout}>
                  <LogOut size={16} />
                  Sign out
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="button button-ghost">
                  Sign in
                </Link>
                <Link to="/register" className="button button-primary">
                  Join
                </Link>
              </>
            )}

            <button type="button" className="menu-toggle" onClick={() => setMenuOpen((value) => !value)} aria-label="Toggle menu">
              {menuOpen ? <X size={18} /> : <Menu size={18} />}
            </button>
          </div>
        </div>
      </header>

      <main>{children}</main>

      <footer className="footer">
        <div className="container footer-grid">
          <div>
            <div className="brand brand-footer">
              <span className="brand-mark">S</span>
              STAYORA
            </div>
            <p className="muted">Thoughtful stays for slower mornings and better travels.</p>
          </div>

          <nav className="footer-links" aria-label="Footer navigation">
            <Link to="/">Home</Link>
            <Link to="/rooms">Rooms</Link>
            <Link to="/account/bookings">Bookings</Link>
            <Link to="/profile">Profile</Link>
          </nav>

          <div className="muted">
            <p>hello@stayora.com</p>
            <p>Available 24/7</p>
          </div>
        </div>
        <div className="container copyright">© 2026 STAYORA. All rights reserved.</div>
      </footer>
    </div>
  )
}

function SearchForm({ defaultValues }: { defaultValues?: { check_in: string; check_out: string; guests: number } }) {
  const navigate = useNavigate()
  const initial = defaultValues ?? getDefaultSearch()
  const [values, setValues] = useState(initial)
  const [error, setError] = useState('')

  useEffect(() => {
    setValues(initial)
  }, [initial.check_in, initial.check_out, initial.guests])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const start = new Date(values.check_in)
    const end = new Date(values.check_out)

    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
      setError('Please provide valid dates.')
      return
    }

    if (end <= start) {
      setError('Check-out must be later than check-in.')
      return
    }

    if (start < new Date(new Date().setHours(0, 0, 0, 0))) {
      setError('Check-in cannot be in the past.')
      return
    }

    setError('')
    const query = new URLSearchParams({
      check_in: values.check_in,
      check_out: values.check_out,
      guests: String(values.guests),
    })

    navigate(`/rooms?${query.toString()}`)
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="field"><label htmlFor="check_in">Check-in</label><input id="check_in" type="date" value={values.check_in} onChange={(event) => setValues((current) => ({ ...current, check_in: event.target.value }))} /></div>
      <div className="field"><label htmlFor="check_out">Check-out</label><input id="check_out" type="date" value={values.check_out} onChange={(event) => setValues((current) => ({ ...current, check_out: event.target.value }))} /></div>
      <div className="field"><label htmlFor="guests">Guests</label><input id="guests" min={1} max={10} type="number" value={values.guests} onChange={(event) => setValues((current) => ({ ...current, guests: Number(event.target.value) || 1 }))} /></div>
      <button type="submit" className="button button-primary search-button">
        <Search size={16} />
        Search
      </button>
      {error ? <p className="field-error">{error}</p> : null}
    </form>
  )
}

function RoomCard({ room }: { room: Room }) {
  return (
    <article className="room-card">
      <img src={getRoomImage(room.id)} alt={room.name} loading="lazy" />
      <div className="room-card-body">
        <div className="room-card-head">
          <div>
            <p className="eyebrow">Private suite</p>
            <h3>{room.name}</h3>
          </div>
          <span className="price-tag">{formatCurrency(room.price_per_night)}</span>
        </div>

        <p className="muted room-description">{room.description ?? 'Thoughtfully designed room for slow, restorative stays.'}</p>

        <div className="meta-row">
          <span><Users size={14} /> Up to {room.capacity} guests</span>
          <span><BedDouble size={14} /> {room.is_active ? 'Available now' : 'Unavailable'}</span>
        </div>

        <div className="card-actions">
          <Link to={`/rooms/${room.id}`} className="button button-primary button-inline">
            View details
            <ChevronRight size={16} />
          </Link>
        </div>
      </div>
    </article>
  )
}

function HomePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['featured-rooms'],
    queryFn: () => fetchRooms({ limit: 4, offset: 0 }),
  })

  return (
    <div className="page page-home">
      <section className="hero-section container">
        <div className="hero-copy">
          <span className="eyebrow accent">Curated stays for modern travelers</span>
          <h1>Stay somewhere worth remembering.</h1>
          <p>
            Discover serene rooms, elevated hospitality, and a booking experience designed to feel effortless from the first click.
          </p>
          <SearchForm />
        </div>

        <div className="hero-visual" aria-label="Featured hotel room">
          <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80" alt="Luxurious hotel room" />
        </div>
      </section>

      <section className="container section-block">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Featured rooms</span>
            <h2>Designed for days that feel slower and richer.</h2>
          </div>
          <Link to="/rooms" className="text-link">
            Explore all rooms <ArrowRight size={16} />
          </Link>
        </div>

        {isLoading ? <p className="status-text">Loading featured rooms…</p> : null}
        {isError ? <p className="status-error">We couldn't load rooms right now. Please try again.</p> : null}

        {data ? (
          <div className="room-grid">
            {data.slice(0, 4).map((room) => (
              <RoomCard key={room.id} room={room} />
            ))}
          </div>
        ) : null}
      </section>

      <section className="container section-block feature-band">
        <div className="feature-item">
          <Sparkles size={18} />
          <div>
            <h3>Designed for unwinding</h3>
            <p>Every room balances comfort, atmosphere, and freedom.</p>
          </div>
        </div>
        <div className="feature-item">
          <ShieldCheck size={18} />
          <div>
            <h3>Verified experiences</h3>
            <p>Simple booking flows with transparent room details.</p>
          </div>
        </div>
        <div className="feature-item">
          <Building2 size={18} />
          <div>
            <h3>Effortless planning</h3>
            <p>Search by dates and guests to find the right stay.</p>
          </div>
        </div>
      </section>
    </div>
  )
}

function RoomsPage() {
  const [searchParams] = useSearchParams()
  const checkIn = searchParams.get('check_in') ?? getDefaultSearch().check_in
  const checkOut = searchParams.get('check_out') ?? getDefaultSearch().check_out
  const guests = Number(searchParams.get('guests') ?? '2') || 2

  const filters = useMemo<RoomFilters>(() => {
    const base: RoomFilters = { limit: 12, offset: 0, is_active: true }

    if (checkIn && checkOut) {
      return {
        ...base,
        guests,
        check_in: checkIn,
        check_out: checkOut,
      }
    }

    return base
  }, [checkIn, checkOut, guests])

  const { data, isLoading, isError } = useQuery({
    queryKey: ['rooms', checkIn, checkOut, guests],
    queryFn: () => {
      if (checkIn && checkOut) {
        return fetchAvailableRooms({
          ...filters,
          check_in: checkIn,
          check_out: checkOut,
          guests,
          limit: 12,
        })
      }

      return fetchRooms({ ...filters, limit: 12 })
    },
  })

  return (
    <div className="page container content-stack">
      <div className="content-header">
        <div>
          <span className="eyebrow">Rooms</span>
          <h1>Book your next stay</h1>
        </div>
        <div className="search-summary">
          <span><CalendarDays size={16} /> {checkIn} → {checkOut}</span>
          <span><Users size={16} /> {guests} guests</span>
        </div>
      </div>

      <SearchForm defaultValues={{ check_in: checkIn, check_out: checkOut, guests }} />

      <div className="results-toolbar">
        <p>{data ? `${data.length} rooms available` : 'Loading results...'}</p>
      </div>

      {isLoading ? <p className="status-text">Searching for available rooms…</p> : null}
      {isError ? <p className="status-error">No rooms could be loaded for this search.</p> : null}
      {!isLoading && !isError && data && data.length === 0 ? (
        <div className="empty-state">
          <h3>No rooms match your dates</h3>
          <p>Try a different check-in window or a larger guest count.</p>
        </div>
      ) : null}

      {data ? (
        <div className="room-grid">
          {data.map((room) => (
            <RoomCard key={room.id} room={room} />
          ))}
        </div>
      ) : null}
    </div>
  )
}

function BookingPanel({ room, initialSearch }: { room: Room; initialSearch?: { check_in: string; check_out: string; guests: number } }) {
  const { isAuthenticated, user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const queryClient = useQueryClient()
  const [form, setForm] = useState(initialSearch ?? getDefaultSearch())
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (initialSearch) {
      setForm(initialSearch)
    }
  }, [initialSearch])

  const totalNights = getNightCount(form.check_in, form.check_out)
  const nightlyPrice = Number(room.price_per_night)
  const estimatedTotal = totalNights > 0 ? nightlyPrice * totalNights : 0

  const bookingMutation = useMutation({
    mutationFn: (payload: BookingCreateRequest) => createBooking(payload),
    onSuccess: () => {
      setMessage('Booking confirmed. Your reservation is ready to review.')
      void queryClient.invalidateQueries({ queryKey: ['my-bookings'] })
    },
    onError: () => {
      setMessage('We could not create this booking. Please review the dates and try again.')
    },
  })

  const handleReserve = () => {
    if (!isAuthenticated || !user) {
      navigate(`/login?redirect=${encodeURIComponent(location.pathname)}`)
      return
    }

    if (!form.check_in || !form.check_out || totalNights <= 0) {
      setMessage('Please choose valid dates before booking.')
      return
    }

    bookingMutation.mutate({
      room_id: room.id,
      check_in_date: form.check_in,
      check_out_date: form.check_out,
      guests: form.guests,
    })
  }

  return (
    <aside className="booking-panel">
      <div className="booking-header">
        <p className="eyebrow">Reserve</p>
        <div className="booking-price">
          <strong>{formatCurrency(room.price_per_night)}</strong>
          <span>/ night</span>
        </div>
      </div>

      <div className="booking-fields">
        <label>
          Check-in
          <input type="date" value={form.check_in} onChange={(event) => setForm((current) => ({ ...current, check_in: event.target.value }))} />
        </label>
        <label>
          Check-out
          <input type="date" value={form.check_out} onChange={(event) => setForm((current) => ({ ...current, check_out: event.target.value }))} />
        </label>
        <label>
          Guests
          <input type="number" min={1} value={form.guests} onChange={(event) => setForm((current) => ({ ...current, guests: Number(event.target.value) || 1 }))} />
        </label>
      </div>

      <div className="pricing-box">
        <div>
          <span>{formatCurrency(room.price_per_night)}</span>
          <small> × {totalNights || 0} nights</small>
        </div>
        <strong>{formatCurrency(estimatedTotal)}</strong>
      </div>

      <button type="button" className="button button-primary full-width" onClick={handleReserve} disabled={bookingMutation.isPending}>
        {bookingMutation.isPending ? 'Processing…' : 'Reserve'}
      </button>

      {message ? <p className="status-text booking-message">{message}</p> : null}
    </aside>
  )
}

function RoomDetailsPage() {
  const { id } = useParams()
  const roomId = Number(id)
  const { data, isLoading, isError } = useQuery({
    queryKey: ['room', roomId],
    queryFn: () => fetchRoomById(roomId),
    enabled: Number.isFinite(roomId),
  })

  if (isLoading) {
    return <div className="container page"><p className="status-text">Loading room details…</p></div>
  }

  if (isError || !data) {
    return <div className="container page"><p className="status-error">This room could not be found.</p></div>
  }

  return (
    <div className="page container content-stack">
      <div className="room-page-header">
        <div>
          <span className="eyebrow">Room details</span>
          <h1>{data.name}</h1>
        </div>
        <Link to="/rooms" className="text-link">Back to rooms <ArrowRight size={16} /></Link>
      </div>

      <div className="room-detail-layout">
        <div className="room-detail-main">
          <img className="detail-image" src={getRoomImage(data.id)} alt={data.name} />
          <div className="detail-content">
            <div className="detail-meta">
              <span><Users size={16} /> Up to {data.capacity} guests</span>
              <span><CircleDollarSign size={16} /> {formatCurrency(data.price_per_night)} / night</span>
            </div>
            <p>{data.description ?? 'A refined space that blends comfort and intention.'}</p>
          </div>
        </div>

        <BookingPanel room={data} initialSearch={getDefaultSearch()} />
      </div>
    </div>
  )
}

function LoginPage() {
  const { login, isAuthenticated } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const location = useLocation()

  const redirectPath = new URLSearchParams(location.search).get('redirect') ?? '/'

  if (isAuthenticated) {
    return <Navigate to={redirectPath} replace />
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')

    try {
      await login({ email, password })
      navigate(redirectPath)
    } catch {
      setError('Incorrect email or password.')
    }
  }

  return (
    <div className="auth-shell container">
      <div className="auth-card">
        <span className="eyebrow">Welcome back</span>
        <h1>Sign in</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Email
            <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
          </label>
          {error ? <p className="field-error">{error}</p> : null}
          <button type="submit" className="button button-primary full-width">Continue</button>
        </form>
        <p className="muted auth-footer">
          Need an account? <Link to="/register">Create one</Link>
        </p>
      </div>
      <div className="auth-visual" aria-label="Hotel lobby photography">
        <img src="https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80" alt="Luxurious hotel lobby" />
      </div>
    </div>
  )
}

function RegisterPage() {
  const { register, isAuthenticated } = useAuth()
  const [values, setValues] = useState({ first_name: '', last_name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')

    try {
      await register(values)
      navigate('/')
    } catch {
      setError('Please check the form and try again.')
    }
  }

  return (
    <div className="auth-shell container">
      <div className="auth-card">
        <span className="eyebrow">Create an account</span>
        <h1>Join STAYORA</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="inline-two">
            <label>
              First name
              <input value={values.first_name} onChange={(event) => setValues((current) => ({ ...current, first_name: event.target.value }))} required />
            </label>
            <label>
              Last name
              <input value={values.last_name} onChange={(event) => setValues((current) => ({ ...current, last_name: event.target.value }))} required />
            </label>
          </div>
          <label>
            Email
            <input type="email" value={values.email} onChange={(event) => setValues((current) => ({ ...current, email: event.target.value }))} required />
          </label>
          <label>
            Password
            <input type="password" minLength={8} value={values.password} onChange={(event) => setValues((current) => ({ ...current, password: event.target.value }))} required />
          </label>
          {error ? <p className="field-error">{error}</p> : null}
          <button type="submit" className="button button-primary full-width">Register</button>
        </form>
        <p className="muted auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
      <div className="auth-visual" aria-label="Modern room interior">
        <img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Modern room styling" />
      </div>
    </div>
  )
}

function MyBookingsPage() {
  const { isAuthenticated } = useAuth()
  const { data, isLoading, isError } = useQuery({
    queryKey: ['my-bookings'],
    queryFn: fetchMyBookings,
    enabled: isAuthenticated,
  })

  if (!isAuthenticated) {
    return <Navigate to="/login?redirect=/account/bookings" replace />
  }

  return (
    <div className="page container content-stack">
      <div className="content-header">
        <div>
          <span className="eyebrow">Bookings</span>
          <h1>My stays</h1>
        </div>
      </div>

      {isLoading ? <p className="status-text">Loading your bookings…</p> : null}
      {isError ? <p className="status-error">We couldn't load your bookings right now.</p> : null}

      {data && data.length === 0 ? <div className="empty-state"><h3>No bookings yet</h3><p>Start with a search and reserve your next stay.</p></div> : null}

      {data ? (
        <div className="booking-list">
          {data.map((booking) => (
            <BookingSummaryCard key={booking.id} booking={booking} />
          ))}
        </div>
      ) : null}
    </div>
  )
}

function BookingSummaryCard({ booking }: { booking: Booking }) {
  const queryClient = useQueryClient()
  const [cancelled, setCancelled] = useState(false)
  const mutation = useMutation({
    mutationFn: () => cancelBooking(booking.id),
    onSuccess: () => {
      setCancelled(true)
      void queryClient.invalidateQueries({ queryKey: ['my-bookings'] })
    },
  })
  const isPastStay = new Date(booking.check_in_date) <= new Date(new Date().setHours(0, 0, 0, 0))

  return (
    <article className="booking-card">
      <div className="booking-card-top">
        <div>
          <span className="eyebrow">Reservation #{booking.id}</span>
          <h3>{booking.room.name}</h3>
        </div>
        <span className={`status-badge ${booking.status.toLowerCase()}`}>{booking.status}</span>
      </div>

      <div className="booking-meta">
        <span><CalendarDays size={14} /> {booking.check_in_date} → {booking.check_out_date}</span>
        <span><Users size={14} /> {booking.guests} guests</span>
        <span><CircleDollarSign size={14} /> {formatCurrency(booking.total_price)}</span>
      </div>

      <div className="booking-actions">
        <Link to={`/rooms/${booking.room_id}`} className="text-link">View room details</Link>
        {booking.status === 'CONFIRMED' && !isPastStay && !cancelled ? (
          <button type="button" className="button button-secondary" onClick={() => mutation.mutate()} disabled={mutation.isPending}>
            {mutation.isPending ? 'Cancelling…' : 'Cancel booking'}
          </button>
        ) : null}
      </div>
    </article>
  )
}

function ProfilePage() {
  const { user, isAuthenticated, refreshUser } = useAuth()
  const [form, setForm] = useState({ first_name: user?.first_name ?? '', last_name: user?.last_name ?? '' })
  const [passwords, setPasswords] = useState({ current_password: '', new_password: '' })
  const [profileMessage, setProfileMessage] = useState('')
  const [passwordMessage, setPasswordMessage] = useState('')

  useEffect(() => {
    if (user) {
      setForm({ first_name: user.first_name, last_name: user.last_name })
    }
  }, [user])

  const handleProfileSave = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setProfileMessage('')

    const payload: UpdateProfileRequest = { first_name: form.first_name, last_name: form.last_name }
    await updateCurrentUser(payload)
    await refreshUser()
    setProfileMessage('Profile updated.')
  }

  const handlePasswordChange = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setPasswordMessage('')

    const payload: ChangePasswordRequest = {
      current_password: passwords.current_password,
      new_password: passwords.new_password,
    }

    await changePassword(payload)
    setPasswordMessage('Password updated successfully.')
    setPasswords({ current_password: '', new_password: '' })
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login?redirect=/profile" replace />
  }

  return (
    <div className="page container content-stack">
      <div className="content-header">
        <div>
          <span className="eyebrow">Profile</span>
          <h1>{user.first_name} {user.last_name}</h1>
        </div>
      </div>

      <div className="profile-grid">
        <form className="panel-card" onSubmit={handleProfileSave}>
          <h2>Account details</h2>
          <div className="inline-two">
            <label>
              First name
              <input value={form.first_name} onChange={(event) => setForm((current) => ({ ...current, first_name: event.target.value }))} />
            </label>
            <label>
              Last name
              <input value={form.last_name} onChange={(event) => setForm((current) => ({ ...current, last_name: event.target.value }))} />
            </label>
          </div>
          {profileMessage ? <p className="status-text">{profileMessage}</p> : null}
          <button type="submit" className="button button-primary">Save changes</button>
        </form>

        <form className="panel-card" onSubmit={handlePasswordChange}>
          <h2>Change password</h2>
          <label>
            Current password
            <input type="password" value={passwords.current_password} onChange={(event) => setPasswords((current) => ({ ...current, current_password: event.target.value }))} />
          </label>
          <label>
            New password
            <input type="password" value={passwords.new_password} onChange={(event) => setPasswords((current) => ({ ...current, new_password: event.target.value }))} />
          </label>
          {passwordMessage ? <p className="status-text">{passwordMessage}</p> : null}
          <button type="submit" className="button button-secondary">Update password</button>
        </form>
      </div>
    </div>
  )
}

function AdminPage() {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [roomForm, setRoomForm] = useState({ name: '', description: '', capacity: 2, price_per_night: 120, is_active: true })

  const roomsQuery = useQuery({
    queryKey: ['admin-rooms'],
    queryFn: () => fetchRooms({ limit: 50, offset: 0 }),
    enabled: Boolean(user) && user?.role === 'admin',
  })
  const bookingsQuery = useQuery({
    queryKey: ['admin-bookings'],
    queryFn: fetchAllBookings,
    enabled: Boolean(user) && user?.role === 'admin',
  })

  const createRoomMutation = useMutation({
    mutationFn: (payload: RoomCreationRequest) => createRoom(payload),
    onSuccess: () => {
      setRoomForm({ name: '', description: '', capacity: 2, price_per_night: 120, is_active: true })
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] })
    },
  })

  if (!user || user.role !== 'admin') {
    return (
      <div className="page container content-stack">
        <div className="empty-state">
          <h3>Admin access required</h3>
          <p>Sign in with an administrator account to access the dashboard.</p>
        </div>
      </div>
    )
  }

  const toggleRoom = async (room: Room) => {
    if (room.is_active) {
      await deactivateRoom(room.id)
    } else {
      await updateRoom(room.id, { is_active: true })
    }
    void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] })
  }

  const handleRoomSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    createRoomMutation.mutate({
      name: roomForm.name,
      description: roomForm.description || null,
      capacity: roomForm.capacity,
      price_per_night: roomForm.price_per_night,
      is_active: roomForm.is_active,
    })
  }

  return (
    <div className="page container content-stack">
      <div className="content-header">
        <div>
          <span className="eyebrow">Dashboard</span>
          <h1>Administration</h1>
        </div>
      </div>

      <div className="admin-grid">
        <form className="panel-card" onSubmit={handleRoomSubmit}>
          <h2>Create room</h2>
          <label>
            Name
            <input value={roomForm.name} onChange={(event) => setRoomForm((current) => ({ ...current, name: event.target.value }))} required />
          </label>
          <label>
            Description
            <textarea value={roomForm.description} onChange={(event) => setRoomForm((current) => ({ ...current, description: event.target.value }))} rows={4} />
          </label>
          <div className="inline-two">
            <label>
              Capacity
              <input type="number" min={1} value={roomForm.capacity} onChange={(event) => setRoomForm((current) => ({ ...current, capacity: Number(event.target.value) || 1 }))} />
            </label>
            <label>
              Price per night
              <input type="number" min={0} step="0.01" value={roomForm.price_per_night} onChange={(event) => setRoomForm((current) => ({ ...current, price_per_night: Number(event.target.value) || 0 }))} />
            </label>
          </div>
          <label className="checkbox-row">
            <input type="checkbox" checked={roomForm.is_active} onChange={(event) => setRoomForm((current) => ({ ...current, is_active: event.target.checked }))} />
            Active
          </label>
          <button type="submit" className="button button-primary" disabled={createRoomMutation.isPending}>
            {createRoomMutation.isPending ? 'Creating…' : 'Create room'}
          </button>
        </form>

        <div className="panel-card">
          <h2>Rooms</h2>
          {roomsQuery.isLoading ? <p className="status-text">Loading rooms…</p> : null}
          {roomsQuery.data ? (
            <div className="stack-list">
              {roomsQuery.data.map((room) => (
                <div key={room.id} className="admin-row">
                  <div>
                    <strong>{room.name}</strong>
                    <small>{room.is_active ? 'active' : 'inactive'}</small>
                  </div>
                  <button type="button" className="button button-secondary" onClick={() => void toggleRoom(room)}>
                    {room.is_active ? 'Deactivate' : 'Activate'}
                  </button>
                </div>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      <div className="panel-card">
        <h2>Bookings</h2>
        {bookingsQuery.isLoading ? <p className="status-text">Loading bookings…</p> : null}
        {bookingsQuery.data ? (
          <div className="stack-list">
            {bookingsQuery.data.map((booking) => (
              <div key={booking.id} className="booking-admin-row">
                <div>
                  <strong>{booking.room.name}</strong>
                  <small>{booking.check_in_date} → {booking.check_out_date}</small>
                </div>
                <select
                  value={booking.status}
                  onChange={async (event) => {
                    await updateBookingStatus(booking.id, { status: event.target.value as BookingStatus })
                    void queryClient.invalidateQueries({ queryKey: ['admin-bookings'] })
                  }}
                >
                  <option value="CONFIRMED">CONFIRMED</option>
                  <option value="CANCELLED">CANCELLED</option>
                  <option value="COMPLETED">COMPLETED</option>
                </select>
              </div>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  )
}

function ProtectedApp() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/rooms" element={<RoomsPage />} />
        <Route path="/rooms/:id" element={<RoomDetailsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/account/bookings" element={<MyBookingsPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </AppShell>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <ProtectedApp />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
