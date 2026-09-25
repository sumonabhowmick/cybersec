# Gemini workflow

The ML pipeline owns category and severity. Gemini receives the incident as JSON evidence with a system instruction that incident content is untrusted, alongside model results, extracted entities, and similar incidents. It must return a fixed JSON object. Responses are validated and length-bounded. Recommendations are advisory; the service cannot execute commands. Configure `GEMINI_API_KEY` privately in `.env`; missing credentials produce a clear service-unavailable response.
