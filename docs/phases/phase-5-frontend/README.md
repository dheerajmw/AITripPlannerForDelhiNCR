# Phase 5: Frontend Application

**Status:** Complete  
**Code:** `frontend/` — Next.js 15 App Router, dark theme

## Routes

| Route | Page |
|-------|------|
| `/` | Landing + API status |
| `/plan` | `PlanForm` |
| `/itinerary` | Timeline, map, summary |

## Run locally

```bash
make dev-backend   # :8000
make dev-frontend  # :3000
```

Set `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## References

- [architecture.md § Phase 5](../../project/architecture.md)
- [implementationPlan.md § 10](../../project/implementationPlan.md)
- [frontend-stitch-prompt-guide.md](../../frontend-stitch-prompt-guide.md)
