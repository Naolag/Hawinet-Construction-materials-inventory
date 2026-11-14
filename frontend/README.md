# Hawinet Frontend

Responsive Next.js App Router UI recreated from the Hawinet Framer prototype. This is a design-only implementation using illustrative local sample data. It intentionally makes no API calls and does not persist changes.

## Run
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Pages
Dashboard, Products, Inventory Management, Transactions, Measurement Units, Unit Conversions, Reports, Categories, Settings and Employee Management.

## Design system
- Canvas: #F8FAFC
- Deep Charcoal sidebar/structure: #1E293B
- Muted Cobalt: #2563EB
- Supporting border: #E2E8F0; secondary text: #64748B
- Dark persistent desktop/tablet sidebar; mobile drawer closes after page selection.

This is an initial responsive recreation. Pixel-perfect parity requires iterative comparison against Framer at matched viewport sizes. No backend, authentication, API client or persistence is included.

Design documentation is maintained under /docs: design system, page specifications and deferred API mapping.
