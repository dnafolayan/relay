# Relay

**Publish once. Deliver reliably.**

Relay is a school information delivery system designed to make communicating announcements to students, parents, and staff more reliable.

Instead of manually sending the same announcement across different groups and channels, an administrator publishes it once, selects the intended audience, and Relay handles recipient resolution, message delivery, retries, and delivery tracking.

> **Status:** In development

---

## Problem

School communication is often fragmented and manual.

An administrator may need to:

- Write the same announcement multiple times
- Find the correct students or parents
- Send messages across different groups
- Follow up with people who missed the message
- Determine whether important messages were actually delivered

Relay aims to turn this into a single workflow.

---

## How It Works

```text
Administrator
      │
      ▼
Web Dashboard
      │
      ▼
FastAPI Backend
      │
      ├── Authentication & Authorization
      │
      ├── Announcement Service
      │
      ▼
PostgreSQL
      │
      ▼
Message Queue
      │
      ▼
Notification Worker
      │
      ▼
Messaging Provider
      │
      ▼
Students / Parents / Staff
      │
      ▼
Delivery Status
      │
      ▼
PostgreSQL
```

An announcement follows a lifecycle such as:

```text
CREATED → QUEUED → PROCESSING → SENT → DELIVERED
                              ↘ FAILED → RETRY
```

---

## Example

An administrator needs to notify all SS3 students:

> "The Mathematics mock examination has been moved to Thursday at 10:00 AM."

Instead of manually locating and messaging every recipient:

1. The administrator creates the announcement.
2. Selects **SS3** as the audience.
3. Relay resolves the appropriate recipients.
4. The announcement is stored in PostgreSQL.
5. Delivery jobs are placed onto the queue.
6. Workers process the jobs asynchronously.
7. Messages are sent through the configured messaging provider.
8. Delivery results are recorded.
9. The administrator can see which messages succeeded or failed.

---

## Architecture

### Backend

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **Pydantic / Pydantic Settings**

### Frontend

- **React**
- **TypeScript**
- **Vite**
- **Tailwind CSS**

### Infrastructure

- Message queue
- Background workers
- Messaging provider API
- Webhooks
- Containerized/deployed services

The exact queue and messaging provider will be selected as the system develops.

---

## Project Structure

```text
relay/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── workers/
│   │   └── main.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Development

### Backend

The backend uses [`uv`](https://docs.astral.sh/uv/) for Python dependency and environment management.

From `backend/`:

```bash
uv sync
```

Run the development server:

```bash
uv run uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Frontend

From `frontend/`:

```bash
npm install
npm run dev
```

---

## Development Principles

Relay is being built around a few principles:

### Reliability over convenience

A message should not disappear simply because an external service temporarily failed.

### Asynchronous processing

Sending potentially thousands of notifications should not block the API request.

### Idempotency

Retrying a job should not accidentally send the same notification multiple times.

### Observability

Administrators should be able to determine what happened to an announcement after publishing it.

### Separation of concerns

API routes, business logic, database models, and background processing should have clear responsibilities.

---

## Planned Features

### Core

- [ ] Authentication
- [ ] Role-based access control
- [ ] Student/parent/staff management
- [ ] Class and audience management
- [ ] Announcement creation
- [ ] Recipient resolution
- [ ] Message queue
- [ ] Background workers
- [ ] Delivery tracking
- [ ] Retry handling
- [ ] Idempotency

### Dashboard

- [ ] Announcement dashboard
- [ ] Delivery statistics
- [ ] Recipient management
- [ ] Class management
- [ ] Failed delivery inspection
- [ ] Audit logs

### Messaging

- [ ] Fake notification provider for development
- [ ] WhatsApp Business integration
- [ ] Delivery webhooks
- [ ] Scheduled announcements
- [ ] Multiple notification channels

---

## Engineering Challenges

Relay is intentionally designed to explore real backend engineering problems rather than being a simple CRUD application.

The project will involve:

- Asynchronous job processing
- Queues and workers
- Retry strategies
- Exponential backoff
- Idempotency
- Rate limiting
- Database transactions
- Authentication and authorization
- External API integration
- Webhooks
- Failure handling
- Observability
- Auditability

---

## Success Metrics

If deployed in a real school environment, Relay will be evaluated using measurable outcomes such as:

- Number of active administrators
- Number of recipients
- Number of announcements delivered
- Delivery success rate
- Failed message rate
- Average delivery time
- Number of successful retries
- Reduction in manual communication work
- Administrator/user feedback

---

## Project Goal

Relay is not intended to be another notification CRUD application.

The goal is to build and deploy a system that solves a real communication problem in a real school environment while providing a practical exploration of reliable backend architecture.

**Publish once. Deliver reliably.**
