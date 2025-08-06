'use server'

export async function pingAPI(): Promise<String> {
    const res = await fetch('http://localhost:8000/ping')
    const json = await res.json()
    return json.status
}