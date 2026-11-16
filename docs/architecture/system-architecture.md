# System Architecture

Current phase: Next.js App Router UI with local fixtures and client-side state only. Framer-derived workspaces are isolated under src/features; route files select and render a feature screen. Shared navigation and layout live under src/components/layout. A reserved API client exists but is disabled and is not called by any screen.

Future integration direction: route page → feature component/hook → feature service → shared API client → FastAPI. Backend domain services and database behavior remain authoritative.
