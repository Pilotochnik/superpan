import { createContext, useState, useEffect, ReactNode } from 'react'

interface AuthContextType {
  user: string | null
  token: string | null
  login: (token: string, user: string) => void
  logout: () => void
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<string | null>(null)

  useEffect(() => {
    const t = localStorage.getItem('token')
    const u = localStorage.getItem('user')
    if (t) setToken(t)
    if (u) setUser(u)
  }, [])

  const login = (tok: string, usr: string) => {
    setToken(tok)
    setUser(usr)
    localStorage.setItem('token', tok)
    localStorage.setItem('user', usr)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
