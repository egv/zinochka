# ZINOCHKA

## Description

This is a personal AI enabled assistant, that integrates with Plaud note pin using Zapier. Zapier basically invokes our webhook with data and we then process it in our own way

## Logic

- there should be a webserver waiting for a webhook call
- after getting a webhook call we should process `transcript` field to see if there is a activation phrase "зиночка" or "zinochka". This should be done without invoking llms since it is a fairly simple task
- if there is an activation phrase, we should extract task list from the transcript
- for each task in the list we should make new task in TickTick

## Requirements

- Whole thing should be done in Python
- Webserver should use FastAPI
- Task extraction should be done using AI Agent 
- TickTick thould be called using MCP 
- Write tests first. ALWAYS. Next write code to make tests pass. Use TDD.

## Libraries

- fastapi
- pydantic
- openai-agents

## Tools

- `uv` should be used for all python tasks. It is already installed.
- ALWAYS prefer `pyproject.toml` to `requirements.txt`
