# Next Steps

## Immediate Priority

Continue from the current handheld workflow foundation and make the operational UX narrower, safer, and more backend-driven.

## Recommended Sequence

1. Add server-driven filtering for task context.

- When a user selects an inbound line, constrain allowed locations and expose required lot/expiry behavior.
- When a user selects a pick task, show only the relevant task context and remaining pick quantity.
- When a user selects a count task, prefill or constrain the expected item set from task/result context.

2. Add richer detail endpoints only where needed.

- Avoid adding endpoints speculatively.
- Prefer extending existing serializers/viewsets when the frontend only needs more display context.
- Add detail-side computed fields for operational screens rather than forcing UI-side inference from IDs.

3. Improve handheld mutation UX.

- disable submit when validation fails
- show loading states during mutations
- clear success state after refresh
- render server validation failures consistently
- reset or advance forms intelligently after successful actions

4. Wire authentication and tenant-aware frontend session flow.

- login form
- JWT handling
- token refresh strategy
- tenant metadata in session/store
- protected routes

5. Connect desktop operations screens more deeply.

- receiving detail page
- outbound wave detail
- pick task monitoring
- count variance review
- shipment/manifest views

6. Stand up local runtime verification.

- fix PostgreSQL credentials for `nexoflow@localhost:5432`
- run migrations
- execute targeted Django tests
- validate core flows against a real database

7. Expand quality and operations coverage.

- add backend tests around the newest serializer/detail behaviors
- add frontend component and hook tests
- add seed/demo data for realistic manual QA

## Concrete First Task For Next Session

Start with constrained task-detail UX on the handheld pages.

Suggested order:

1. receiving: use selected inbound line metadata to drive location rules and lot/expiry inputs
2. picking: show status-aware action buttons and remaining quantity enforcement
3. counting: narrow selectable items based on task/result context instead of broad item lists

## Known Blockers

- PostgreSQL authentication is still not working for local test DB creation
- frontend is build-valid, but some runtime paths still rely on mock fallback data when backend data is absent
- authentication is not yet integrated end to end

## Verification Targets After Resume

Run at minimum:

- `python -m compileall backend`
- `cmd /c npm run build`

After database access is fixed, also run:

- `python manage.py migrate`
- `python manage.py test`

## Success Condition For The Next Phase

The next phase is successful when a handheld operator can:

- select a real task
- see only relevant operational context
- complete the action with clear validation and error handling
- rely on live backend responses instead of broad fallback assumptions
