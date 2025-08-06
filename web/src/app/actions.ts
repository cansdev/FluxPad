'use server'

import { API_ENDPOINTS } from '@/lib/config'

export async function pingAPI(): Promise<String> {
    const res = await fetch(API_ENDPOINTS.PING)
    const json = await res.json()
    return json.status
}