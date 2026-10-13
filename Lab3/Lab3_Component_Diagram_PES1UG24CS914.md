# UML Component Diagram — Local Sports Tournament & Bracket Manager

**PES1UG24CS914 | Kshitij Prabhu | Section 5B**

## Components (5)

| Component | Role |
|---|---|
| User Interface | Interaction layer for all four actors (Team Captain, Tournament Director, Scorekeeper, Spectator) |
| Tournament Manager | Core business logic — coordinates the full tournament workflow |
| Bracket & Scoring Service | Generates seeded brackets, records match results, applies elimination rules |
| Notification Service | Dispatches alerts to followers when match results are published |
| Database | Persists team registrations, brackets, match records, and standings |

## Interfaces (4)

| Interface | Connected Components | Direction |
|---|---|---|
| Request Interface | User Interface → Tournament Manager | Required → Provided |
| Bracket & Scoring Interface | Tournament Manager → Bracket & Scoring Service | Required → Provided |
| Notification Dispatch Interface | Tournament Manager → Notification Service | Required → Provided |
| Data Persistence Interface | Tournament Manager → Database | Required → Provided |

## Diagram

See `Lab3_Component_Diagram_PES1UG24CS914.png` for the full UML component diagram with ball-and-socket notation.

## Architecture Choice: Layered Architecture

The Tournament Manager sits at the centre of all four interfaces, acting as the single business-layer coordinator. The User Interface never touches the Database or services directly — every request passes through the Tournament Manager, enforcing role-based access and consistent tournament rules across all use cases.
