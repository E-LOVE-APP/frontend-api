````markdown
# 💖 E-Love

Welcome to **E-Love**! 🎮❤️ This app is designed to help young gamers who play online games like Valorant and Dota
meet new people and find meaningful relationships.

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed for this backend service:

- Python (version >= 3.10)
- Poetry

### Why Use Poetry?

Poetry is a dependency management and packaging tool for Python. It provides a more comprehensive and user-friendly approach compared to pip,
by handling dependencies in a lock file, managing virtual environments, and simplifying the publishing process.

### Installing Poetry

To install Poetry, follow these steps:

1. Using the official installer script:
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
````

2. Or, using pip:
   ```sh
   pip install poetry
   ```

### Installation

1. Clone the repo:

   ```sh
   git clone https://github.com/yourusername/e-love.git
   ```

2. Navigate to the project directory:

   ```sh
   cd e-love-frontend-api
   ```

3. Install dependencies:

   ```sh
   poetry install
   ```

### Development

To run the app in development mode:

1. Activate the virtual environment:

   ```sh
   poetry shell
   ```

2. Run the FastAPI server:

   ```sh
   poetry run uvicorn main:app --reload
   ```

This will start the FastAPI development server on `http://127.0.0.1:8000`.

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

To use Taskfile:

1. Define tasks in a `Taskfile.yml`:

   ```yaml
   version: "3"

   tasks:
     run:
       cmds:
         - poetry run uvicorn main:app --reload
       desc: "Run the FastAPI server in development mode"
     test:
       cmds:
         -  # Add test commands here
       desc: "Run tests"
   ```

2. Run a task:
   ```sh
   task run
   ```

## 🛠️ Technologies Used (add another later)

- **Python**: Programming language for the backend.
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **Poetry**: Dependency management and packaging tool for Python.
- **Taskfile**: Simplifies running complex project-specific tasks.
- **Dotenv**: Manage environment variables.
