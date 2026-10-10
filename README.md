# AI Agent Colab Starter

This project is a first controlled base for a Colab-based AI work agent.

It is designed to:

- run from Google Colab
- connect to Google Drive for persistent state, logs, data, and checkpoints
- connect to GitHub for code versioning
- execute allowed local tools
- keep a task log and restart state
- grow later into a multi-tool coding, game-building, map-building, and training agent

It is not a full ChatGPT replacement. The practical path is to combine a strong base model or API with tools, memory, project state, and later fine-tuning.

## Structure

```text
ai-agent-colab/
  notebooks/
    colab_start.ipynb
  src/
    agent_core/
      agent.py
      config.py
      memory.py
      tools.py
  training/
    train_placeholder.py
  config/
    agent_config.yaml
  projects/
  memory/
  logs/
  requirements.txt
```

## First Colab Run

1. Upload this folder to GitHub as a repository.
2. Open `notebooks/colab_start.ipynb` in Google Colab.
3. Set the repository URL in the notebook.
4. Run all cells.
5. Give the agent a first small task, for example:

```text
Create a tiny Python text adventure game in projects/text_adventure.
```

## GitHub Authentication

For private repositories or push access, use a GitHub token through Colab secrets or a temporary environment variable. Do not hard-code tokens in notebooks.

## Google Drive Usage

Drive is used for durable files:

- `memory/state.json`
- `logs/agent.log`
- model checkpoints
- generated datasets
- project outputs

## Current Safety Model

The first version only includes basic local tools:

- read file
- write file
- list directory
- run Python script
- append log entry

Potentially destructive actions such as deleting files, installing packages, or pushing to GitHub should be added only behind explicit confirmation.

## Next Development Steps

1. Add a stronger model backend.
2. Add a task planner.
3. Add GitHub commit/push tool.
4. Add game project templates.
5. Add map generation tools.
6. Add evaluation and test execution.
7. Add training data collection.
8. Add LoRA/fine-tuning pipeline.

