import { API_BASE_URL, API_PATHS } from '../api/config'
export async function fetchInfo() {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.info}`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        // const { phone } = await res.json()
        // setPhone(phone)
      } catch (err) {
        console.error('Error loading info:', err)
      }
    }