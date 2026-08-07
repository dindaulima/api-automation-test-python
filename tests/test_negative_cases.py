#TC1 - Missing API key → 401.
#TC2 - Missing token → 401.
#TC3 - Invalid key/token combo → 401.
#TC4 - Malformed board ID (not 24-hex-char) → 400.
#TC5 - Wrong HTTP method on an endpoint (e.g., DELETE on a read-only path) → 405 (if applicable).
#TC6 - Exceeding rate limits (optional, harder to simulate reliably) → 429.
#TC7 - SQL/script injection-style strings in name fields → verify safely rejected or escaped, not executed.