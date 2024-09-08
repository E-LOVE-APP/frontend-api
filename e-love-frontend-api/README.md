# 💖 E-Love (Backend)

Welcome to **E-Love**! 🎮❤️ This app is designed to help young gamers who play online games like
Valorant and Dota meet new people and find meaningful relationships.

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed for this backend service:

- Python (version >= 3.10)
- Docker installed & Docker Desktop application
- Poetry

### Why Use Poetry?

Poetry is a dependency management and packaging tool for Python. It provides a more comprehensive and user-friendly approach compared to pip,
by handling dependencies in a lock file, managing virtual environments, and simplifying the publishing process.

### Installation

1. Clone the repo:

   ```sh
   git clone https://github.com/yourusername/e-love.git
   ```

2. Navigate to the project directory:

   ```sh
   cd e-love-frontend-api
   ```

3. Run dependencies installation & other stuff using Taskfile:

   ```sh
   poetry shell
   ```

   ```sh
   poetry install
   ```

   ```sh
   task compose-up
   ```

### Development

To run the app in development mode:

1. Open your Docker Desktop and search for e-love-frontend-api container.

2. Run e-love-frontend-api container.

This will start the FastAPI development server on `http://localhost:8000`.

### Building for Production

To build the app for production:

```sh
# Add instructions here when ready
```

### Running Tests

#### Unit Tests

```sh
# Add instructions here when ready
```

### Taskfile

Taskfile is a tool for defining and running project-specific tasks. It simplifies complex command sequences into simple task invocations.

To install Taskfile:

1. Install Taskfile using the official installation method:
   ```sh
   # Add instructions here when ready
   ```

## 🛠️ Technologies Used (add another later)

- **Python**: Programming language for the backend.
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **Poetry**: Dependency management and packaging tool for Python.
- **Taskfile**: Simplifies running complex project-specific tasks.
- **Dotenv**: Manage environment variables.
- **Docker**: Manage microservices environment, etc.
