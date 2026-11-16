# Hawinet Frontend

Next.js App Router implementation of the Hawinet Framer workspace.

Run with `npm install` then `npm run dev` from this directory.

This phase is a visual prototype: all forms and interactions use local client state and sample records. No FastAPI calls, database access, authentication, or real stock processing are connected. The Products, Transactions, Inventory and Reports workspaces are direct ports of the Framer code components with Framer-only property-control declarations removed. Dashboard is recreated from the native Framer canvas. Future API integration infrastructure is reserved but disabled.
