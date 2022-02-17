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

# Example page implementation

```

class ExamplePage(PageBasic):
    def __init__(self):
        super().__init__()

        self.set_page_contents("""<p>List page</p>""")

````

This allows to write simple HTML code:

```
        add_form = self.form()

        art1 = self.label("link_name", "link_name")
        inp1 = self.form_input("text", "link_name")

        art2 = self.label("artist", "artist")
        inp2 = self.form_input("text", "artist")

        art3 = self.label("album", "album")
        inp3 = self.form_input("text", "album")

        art4 = self.label("song", "song")
        inp4 = self.form_input("text", "song")

        inp5 = self.form_input_submit()

        add_form.add_action(self.get_path_relative())

        add_form.add_input(art1)
        add_form.add_input(self.br())
        add_form.add_input(inp1)
        add_form.add_input(self.br())
        add_form.add_input(art2)
        add_form.add_input(self.br())
        add_form.add_input(inp2)
        add_form.add_input(self.br())
        add_form.add_input(art3)
        add_form.add_input(self.br())
        add_form.add_input(inp3)
        add_form.add_input(self.br())
        add_form.add_input(art4)
        add_form.add_input(self.br())
        add_form.add_input(inp4)
        add_form.add_input(self.br())
        add_form.add_input(inp5)

        return add_form
```
