<div align="center">

# Krib - AI-Powered Rental Platform

(Intelligent agents for property rentals and bookings)

![Krib Screenshot](frontend/public/banner.png)

Krib is a comprehensive AI-powered rental platform that revolutionizes both short-term and long-term property rental experiences. Through intelligent agents, Krib automates the entire rental process from search to contract signing, making property rentals as simple as having a conversation with your AI assistant.

**For Short-Term Rentals (Airbnb-style)**: AI agents handle property search, booking coordination, payment processing, and guest services - essentially booking your perfect vacation rental for you automatically.

**For Long-Term Rentals (Real Estate)**: AI agents manage property viewings, rental applications, contract generation, DocuSign integration, and commission processing - streamlining the entire tenant acquisition process for real estate companies.

[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](./license)
[![GitHub Repo stars](https://img.shields.io/github/stars/mahmoudomarus/Kribz)](https://github.com/mahmoudomarus/Kribz)
[![Issues](https://img.shields.io/github/issues/mahmoudomarus/Kribz)](https://github.com/mahmoudomarus/Kribz/labels/bug)

</div>

## Table of Contents

- [Krib Architecture](#project-architecture)
  - [Backend API](#backend-api)
  - [Frontend](#frontend)
  - [Agent System](#agent-system)
  - [Database](#database)
- [Use Cases](#use-cases)
- [Tech Stack](#tech-stack)
- [Self-Hosting](#self-hosting)
- [Contributing](#contributing)
- [License](#license)

## Project Architecture

![Architecture Diagram](docs/images/diagram.png)

Krib consists of four main components:

### Backend API

FastAPI service deployed on **Heroku** that handles REST endpoints, agent orchestration, and integrations with property management systems, payment processors, and DocuSign.

### Frontend

Next.js/React application deployed on **Vercel** providing responsive interfaces for guests, hosts, real estate companies, and property managers.

### Agent System

Intelligent AI agents that automate:
- **Property Search & Booking** for short-term rentals
- **Viewing Scheduling & Applications** for long-term rentals  
- **Contract Generation & DocuSign Integration**
- **Commission Processing & Property Management**

### Database

**Supabase** (PostgreSQL) with authentication, user management, property listings, booking history, contract storage, and real-time synchronization.

## Use Cases

### Short-Term Rentals (Vacation/Airbnb Style)
1. **Automated Booking Agent** - _"Find and book a 2-bedroom apartment in Barcelona for next weekend under €150/night with good reviews and close to the beach"_
2. **Trip Planning Assistant** - _"Book accommodation, transportation, and activities for a 5-day business trip to London including airport transfers"_
3. **Guest Concierge** - _"Handle check-in procedures, provide local recommendations, and coordinate any issues during my stay"_

### Long-Term Rentals (Real Estate Companies)
1. **Viewing Coordinator** - _"Schedule property viewings for interested tenants based on their availability and preferences"_
2. **Application Processor** - _"Collect tenant applications, verify references, and generate comprehensive reports for landlords"_
3. **Contract Automation** - _"Generate tenancy agreements, send via DocuSign to both parties, and process commission payments once signed"_
4. **Property Management** - _"Remove rented properties from listings, update availability, and coordinate handover procedures"_

## Tech Stack

- **Backend**: FastAPI on Heroku with Redis
- **Frontend**: Next.js/React on Vercel  
- **Database & Auth**: Supabase (PostgreSQL)
- **AI Agents**: Custom orchestration with LLM integration
- **Contracts**: DocuSign API integration
- **Payments**: Stripe for commission processing
- **Real-time**: WebSocket connections for live updates

## Self-Hosting

Krib AI can be self-hosted on your own infrastructure using our comprehensive setup wizard. For a complete guide to self-hosting Krib AI, please refer to our [Self-Hosting Guide](./docs/SELF-HOSTING.md).

The setup process includes:
- Supabase project configuration
- Heroku backend deployment  
- Vercel frontend deployment
- DocuSign API setup
- Payment processor integration

### Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/mahmoudomarus/Kribz.git
cd Kribz
```

2. **Run Setup Wizard**
```bash
python setup.py
```

3. **Deploy Services**
- Backend: Deploy to Heroku
- Frontend: Deploy to Vercel  
- Database: Configure Supabase

The wizard will guide you through all necessary steps to get your Krib AI instance up and running. For detailed instructions, troubleshooting tips, and advanced configuration options, see the [Self-Hosting Guide](./docs/SELF-HOSTING.md).

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes Krib better for everyone.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Setting up your development environment
- Submitting pull requests  
- Reporting issues
- Code style and standards

## Deployment Architecture

- **Backend**: Heroku with Redis add-on
- **Frontend**: Vercel with automatic deployments
- **Database**: Supabase with row-level security
- **File Storage**: Supabase Storage for documents/contracts
- **Monitoring**: Built-in analytics and error tracking

## License

Krib AI is licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for the full license text.
