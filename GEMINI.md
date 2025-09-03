# GEMINI.md - NFL Game Schedule Backend

## Project Context

You are an AI agent tasked with implementing a Python backend service for NFL game schedules. This project has two companion documents that contain detailed requirements and implementation guidance:

- **PRD.md**: Contains complete functional requirements, API specifications, and technical constraints
- **CHECKLIST.md**: Provides step-by-step development tasks organized in phases

## Your Role

Follow the development checklist systematically, referring to the PRD for detailed specifications. Complete each checklist item fully before proceeding to the next one.

## Key Implementation Guidelines

### Development Philosophy

- Standard library first, third-party packages only when necessary
- Small, focused commits that align with checklist items
- Test each component as you build it
- Prioritize simplicity and reliability over performance

### ESPN API Integration Strategy

When implementing ESPN API calls:

1. Start with sample API calls to understand the response structure
2. Focus on the `competitions` array for game data
3. Map ESPN's nested structure to our flat game format
4. Handle timezone conversion carefully (venue local time → UTC)

### Error Handling Approach

Implement defensive programming:

- Assume ESPN API responses may have missing fields
- Provide meaningful error messages for debugging
- Log failures but don't crash the application
- Return empty arrays rather than errors when possible

### Commands (very important)

- You **must** use the virtual environment before running any commands. This can be done by running `. ./.venv/bin/activate`
- After activating the virtual environment, you can install dependencies with `just install`
- Run tests with `just test`

### Testing Strategy

Write tests that verify:

- ESPN API response parsing with real sample data
- Timezone conversions across different venues
- Cache behavior and expiration
- All endpoint response formats
- Error scenarios and edge cases
- Logging during unit tests is acceptable and can be left in the test output.

## File Organization

Create a clean, logical structure:

```
src/
├── app.py              # Main Starlette app
├── espn_client.py      # ESPN API calls
├── models.py           # Data structures
├── cache.py            # Caching logic
└── config.py           # Settings
tests/
requirements.txt
README.md
```

## Development Sequence

1. **Phase 1**: Build core ESPN API integration and data parsing
2. **Phase 2**: Implement the three main endpoints
3. **Phase 3**: Add caching and error resilience
4. **Phase 4**: Production readiness (logging, config, docs)
5. **Phase 5**: Comprehensive testing and quality assurance

## Success Indicators

- All checklist items completed and tested
- Application meets all requirements specified in PRD.md
- Code is clean, documented, and follows Python best practices
- Service runs reliably and handles errors gracefully

## Questions or Clarifications

If any requirements are unclear, refer back to the PRD.md for detailed specifications. The checklist provides the implementation order and specific technical tasks.
