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

For easier deployment, use the provided script:

```bash
# Show help and available options
./scripts/run-scenario.sh help

# Start web interface (recommended)
./scripts/run-scenario.sh web

# Start CLI interface
./scripts/run-scenario.sh cli
```

## Available Profiles

### Default (No Profile)
```bash
# Run default VHACK CLI interface
docker compose up
```

### Web Interface
```bash
# Default web interface on port 5000 with dynamic security levels
docker compose --profile web up
```

## Service Types

| Service | Profile | Description | Access |
|---------|---------|-------------|--------|
| `vhack` | default | CLI interface | Terminal only |
| `vhack-web` | web | Web interface with dynamic security levels | HTTP port 5000 |

*Note: Individual scenario profiles are not currently implemented. All scenario testing is done through the main web interface by switching security levels dynamically.*

## Port Mapping

| Service | Profile | Access Method | Port |
|---------|---------|---------------|------|
| `vhack` | default | Terminal only | No HTTP port |
| `vhack-web` | web | HTTP REST API | 5000 |

> **Note**: Only CLI and web profiles are available. Individual scenario testing is done through the web interface by switching security levels.

## Running Multiple Instances

You can run both CLI and web interfaces simultaneously:

```bash
# Run web interface in background
docker compose --profile web up -d

# Run CLI interface in separate terminal
docker compose run --rm vhack
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