import type { Metadata } from "next"
import "./globals.css"
export const metadata: Metadata = { title: "Hawinet | Construction Material Inventory", description: "Construction material inventory management workspace." }
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html> }
