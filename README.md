# Overview

Simple Python Page server

Use:
 - Register page builder
 - Create server
 - Start server

Page builder provides pages for particular urls.

Each page should implement PageBasic object.

Therefore each request opens a different PageBasic registered for an URL.

# Example use

```
    logging.basicConfig(level=logging.INFO)

    superserver = SimplePythonPageSuperServer(host_name, port)

    builder = PageBuilder()
    builder.register_page("/download", ExamplePage() )
    builder.register_page("/download/index.xyz", ExamplePage() )
    set_page_builder(builder)

    superserver.start_server()
```
