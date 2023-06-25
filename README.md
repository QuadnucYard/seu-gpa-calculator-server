# seu-gpa-calculator server

The server for seu-gpa-calculator due to inaccessibility to SEU API of browser. It simply forwards user requests to SEU official API, and does not store any personal information. The tokens generated at runtime are automatically cleared when expiration.

You can safely review the codes to assure the security of the server.

Used packages:

- fastapi
- uvicorn
