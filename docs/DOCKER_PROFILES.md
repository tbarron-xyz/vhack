# VHACK Docker Compose Profiles

This document explains how to use the different Docker Compose profiles to run specific VHACK vulnerability scenarios.

## Service Types Overview

### CLI Services (Terminal Access Only)
- **No HTTP endpoints** - Cannot be accessed with curl or web browsers
- **Interactive terminal interface** - Use `docker attach` or `docker exec`
- **Examples**: `vhack`, `vhack-research`, `vhack-creative`, etc.

### Web Services (HTTP API Access)
- **REST API endpoints** - Can be accessed with curl, web browsers, or API clients
- **JSON responses** - Structured data for programmatic access
- **Examples**: `vhack-web`, `vhack-research-web`, `vhack-creative-web`, etc.

## Quick Start with Convenience Script

For easier scenario management, use the provided script:

```bash
# Show help and available scenarios
./scripts/run-scenario.sh help

# Run specific scenarios (web mode by default)
./scripts/run-scenario.sh research    # Research scenario on port 5001
./scripts/run-scenario.sh creative    # Creative scenario on port 5002
./scripts/run-scenario.sh finance cli # Finance scenario in CLI mode
```

## Available Profiles

### Default (No Profile)
```bash
# Run default VHACK with general vulnerabilities (CLI)
docker compose up
```

### Web Interface
```bash
# Default web interface on port 5000
docker compose --profile web up
```

### Individual Scenarios (CLI)
```bash
# Research scenario (Information Disclosure)
docker compose --profile research up

# Creative scenario (Jailbreaking)  
docker compose --profile creative up

# System Admin scenario (Command Injection)
docker compose --profile sysadmin up

# Finance scenario (PII Exposure)
docker compose --profile finance up

# Medical scenario (HIPAA Violations)
docker compose --profile medical up
```

### Individual Scenarios (Web Interface)
```bash
# Research scenario web interface (port 5001)
docker compose --profile research-web up

# Creative scenario web interface (port 5002)
docker compose --profile creative-web up

# System Admin scenario web interface (port 5003)
docker compose --profile sysadmin-web up

# Finance scenario web interface (port 5004)
docker compose --profile finance-web up

# Medical scenario web interface (port 5005)
docker compose --profile medical-web up
```

## Port Mapping

| Scenario | CLI Profile (Terminal) | Web Profile (HTTP API) | Port |
|----------|------------------------|--------------------------|------|
| Default | `vhack` (no port) | `web` | 5000 |
| Research | `research` (no port) | `research-web` | 5001 |
| Creative | `creative` (no port) | `creative-web` | 5002 |
| System Admin | `sysadmin` (no port) | `sysadmin-web` | 5003 |
| Finance | `finance` (no port) | `finance-web` | 5004 |
| Medical | `medical` (no port) | `medical-web` | 5005 |

> **Note**: CLI profiles have no HTTP endpoints and cannot be accessed via curl or web browsers.

## Multiple Scenarios

You can run multiple scenarios simultaneously:

```bash
# Run research and finance scenarios together
docker compose --profile research --profile finance up

# Run all web interfaces
docker compose --profile research-web --profile creative-web --profile sysadmin-web --profile finance-web --profile medical-web up
```

## Building and Background Running

```bash
# Build and run in background
docker compose --profile research-web up --build -d

# Stop specific profile
docker compose --profile research-web down

# View logs
docker compose --profile research-web logs -f
```

## Environment Variables

Make sure to set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENROUTER_API_KEY=your-api-key-here
```

## Interactive CLI Access

For CLI scenarios, you can interact with the running container:

```bash
# Start research scenario
docker compose --profile research up -d

# Access the container
docker exec -it vhack-research bash

# Or attach to see the interactive prompt
docker attach vhack-research
```

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the port
ss -tlnp | grep :5004

# Stop conflicting services or use different ports
docker compose --profile finance-web down
```

**API Key Not Set:**
```bash
# Verify .env file exists and has API key
cat .env | grep OPENROUTER_API_KEY

# Or set environment variable directly
export OPENROUTER_API_KEY="your-key-here"
```

**Container Won't Start:**
```bash
# Check container logs
docker compose --profile research-web logs

# Rebuild if needed
docker compose --profile research-web up --build
```

**Permission Denied:**
```bash
# Make sure scripts are executable
chmod +x ./scripts/run-scenario.sh
```

**Cannot Access with curl:**
```bash
# CLI services don't have HTTP endpoints
# ❌ This won't work: curl http://localhost:5000 (when using vhack CLI)
# ✅ Use web profile instead:
docker compose --profile web up -d
curl http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"message": "test"}'
```