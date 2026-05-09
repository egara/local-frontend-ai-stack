# Local Frontend AI Stack 🚀

A self-hosted, privacy-focused local AI infrastructure designed to run entirely on your machine. This stack integrates **Open WebUI** with a powerful local LLM backend (**FastFlowLM** for my particular case), a semantic search engine (**SearXNG**), and a high-performance caching layer (**Valkey**).

All components communicate via `host.docker.internal`, ensuring seamless connectivity between containers and the host's native services without requiring complex port forwarding or network bridging.

## 🏗️ Architecture Overview

This stack is built using **Docker Compose** to orchestrate three primary microservices:

1. **Open WebUI**: The user interface for interacting with AI models.
2. **FastFlowLM (Host Service)**: A local Large Language Model running on the host machine, exposed via a specific API endpoint to the containerized UI.
3. **SearXNG**: An open-source meta-search engine that aggregates results from various search providers locally.
4. **Valkey**: A high-performance in-memory data store (compatible with Redis) used for caching and session management within the stack.

## 📋 Service Details

### `open-webui`
The central interface for this AI ecosystem. It connects to local models via an OpenAI-compatible API endpoint running on the host.
- **Image**: `ghcr.io/open-webui/open-webui:main`
- **Port Mapping**: Exposed globally (`0.0.0.0`) on port `3000`.
- **Key Configuration**: Uses `OPENAI_API_BASE_URL` pointing to `http://host.docker.internal:52625/v1`, allowing the container to reach the FastFlowLM service running on the host network interface.

### `searxng`
A privacy-respecting search engine that indexes local and remote content.
- **Image**: `docker.io/searxng/searxng:${SEARXNG_VERSION:-latest}` (Version is configurable via env var).
- **Port Mapping**: Exposed on port `3001`.
- **Persistence**: Config files are mounted from `./data/searxng/core-config/`, and search data/cache resides in `./data/searxng/data`.

### `valkey`
Provides a fast, reliable key-value store for the application stack.
- **Image**: `docker.io/valkey/valkey:9-alpine`
- **Configuration**: Runs with specific persistence settings (`--save 30 1`) and reduced logging verbosity.
- **Persistence**: Data is stored in `./valkey/data`.

## 🛠️ Prerequisites

Before running this stack, ensure the following are installed on your system:
- Docker with Docker Compose plugin enabled.
- A AI backend. For this particular case, local instance of **FastFlowLM** running and listening on port `52625` (accessible via `0.0.0.0`).

## 🚀 Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone git@github.com:egara/local-frontend-ai-stack.git
    cd local-frontend-ai-stack
    ```

2.  **Create Data Directories** (if they don't exist):
    Ensure the paths defined in `volumes` exist to avoid permission errors:
    ```bash
    mkdir -p ./data/open-webui/data ./data/searxng/core-config ./data/searxng/data ./valkey/data
    ```

3. **Configure**:
    Edit the **docker-compose.yaml** and adapt its configuration to your needs:

    - Versions of the images.
    - Volumes.
    - AI Backend (For my particular case, FastFlowLM has been used but you can configure Ollama for instance).

4. **Start the Services**:
    Navigate to the project directory and run:
    ```bash
    docker-compose up -d
    ```

5. **Access the Applications**:
    Once started, open your browser:
    - **Open WebUI**: `http://localhost:3000` (or your host IP if not on localhost).
    - **SearXNG**: `http://localhost:3001`.

## ⚙️ Configuration Notes

- **Network Binding**: The port mapping `"0.0.0.0:3xxx"` allows access from any network interface, which is useful for remote development or multi-monitor setups, though standard Docker practice often defaults to the container's internal IP unless explicitly needed externally.
- **Host Communication**: The `extra_hosts` entry ensures that services inside the containers can resolve `host.docker.internal`, a critical feature for accessing host-based services like FastFlowLM without exposing them directly to the public internet.

## 🛡️ Security Considerations

- Since this stack relies on local communication (`host.docker.internal`), ensure your host machine's firewall is configured correctly if you plan to access these services remotely.
- `WEBUI_AUTH: "false"` disables authentication for development/testing; in production, enable authentication by setting `WEBUI_AUTH: "true"`.

## 📝 License

This project is open source and available under the [GNU GENERAL PUBLIC LICENSE Version 3](LICENSE).
