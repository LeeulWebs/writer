# Young Adult Novel Generator

## Overview
This is a **Young Adult Novel Generator** application built with Streamlit that uses OpenAI's API to generate complete YA novels. The application provides an intuitive interface for creating compelling young adult stories with AI assistance.

## Recent Changes (2025-09-29)
- Successfully imported from GitHub
- Configured all Python dependencies using UV package manager
- Set up Streamlit configuration for Replit environment (host 0.0.0.0:5000)
- Created workflow "Novel Generator App" to run the application
- Configured deployment settings for production using autoscale
- Application is fully functional and ready for use

## Project Architecture

### Core Components
- **app.py**: Main Streamlit application interface
- **novel_generator.py**: Core novel generation logic using OpenAI API
- **db_service.py**: SQLite database service for storing novels, series, and generated content
- **utils.py**: Utility functions for file operations and text processing

### Key Features
- **Single Novel Mode**: Create standalone novels with detailed character development
- **Series Mode**: Create up to 5 connected novels with consistent character arcs
- **AI-Powered Generation**: Uses OpenAI models (GPT-4, GPT-3.5) for content creation
- **Database Storage**: SQLite database stores all generated content
- **Multiple Output Formats**: Export novels in various formats (HTML, Markdown, TXT)

### Dependencies
- **Streamlit**: Web application framework
- **OpenAI**: AI content generation
- **Anthropic**: Alternative AI provider
- **SQLite**: Local database storage

### Database Schema
The application uses SQLite with tables for:
- `novels`: Main novel records
- `series`: Series information
- `chapter_outlines`: Chapter structure
- `scenes`: Individual scene content
- `novel_formats`: Exported formats
- Additional tables for premises, character profiles, keywords, etc.

### Configuration
- **Streamlit Config**: `.streamlit/config.toml` - Configured for Replit environment
- **Dependencies**: `pyproject.toml` - UV-managed Python dependencies
- **Virtual Environment**: `.pythonlibs/` - Contains all installed packages

## User Preferences
- No specific user preferences documented yet

## Current State
- ✅ Application is running successfully on port 5000
- ✅ All dependencies installed and configured
- ✅ Database service operational
- ✅ Deployment configuration complete
- ⚠️ Requires OpenAI API key for full functionality