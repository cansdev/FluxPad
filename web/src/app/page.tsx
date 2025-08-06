import { pingAPI } from "./actions"

export default async function Home() {
    const apiStatus = await pingAPI()
    return (
        <main className="flex flex-col items-center justify-center min-h-screen p-8 bg-gray-100">
          <h1 className="text-4xl font-bold mb-4">Welcome to FluxPad</h1>
          <p className="text-lg">
            FastAPI says: <span className="font-mono text-green-600">{apiStatus}</span>
          </p>
        </main>
    )
}
