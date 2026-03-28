# API Testing with HTTP Files

HTTP request files under `backend/http/` let you send requests directly from your IDE without leaving the editor.

## VSCode — REST Client extension

Install the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension (`humao.rest-client`).

Open any `.http` file. A **Send Request** link appears above each `###` block — click it to execute the request. The response opens in a split panel.

```
backend/http/
└── meta.http    ← health check & meta endpoints
```

### Variable

Each `.http` file declares `@baseUrl` at the top:

```
@baseUrl = http://localhost:8000
```

Change this value to target a different environment (staging, production).

## JetBrains IDEs (PyCharm, IntelliJ, WebStorm…)

HTTP file support is built in — no plugin needed.

Open a `.http` file and click the green **Run** arrow next to any `###` block.

To switch environments, use the environment dropdown in the gutter or define named environments in `http-client.env.json` at the same level (see [JetBrains docs](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html#environment-variables)).

## Adding new request files

Create one `.http` file per domain/router (e.g. `listings.http`, `pricing.http`). Define `@baseUrl` at the top of each file. Group related requests with `###` separators and add a comment line describing each one.

```http
@baseUrl = http://localhost:8000

### List listings
GET {{baseUrl}}/listings
Accept: application/json

### Get listing by id
GET {{baseUrl}}/listings/123
Accept: application/json
```
