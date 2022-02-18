# Overview

Simple Python Page server.

Write simple GUI as a web interface! You do not have to use pyqt or pygtk. You can write simple 'layouts' with HTML, with all benefits of it!

All actions are provided by server pages:
 - each page is a 'function' potentially with arguments
 - each page can lead to a different page

How to use:
 - Register pages in page builder
 - set builder in HTTP server
 - Start server

Each page should implement PageBasic object.

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
class AddItemPage(CommonUtilsPage):

    def write(self, args):

        self.set_title("Add Item Page")

        p = self.p()        # create paragraph
        p.add(self.get_menu())

        if len(args) == 0:
            p.add(self.get_form_new_song())
        else:
            link = args['link_name']
            artist = args['artist']

        self.set_page_contents(p.html() )       # sets the page contents

        super().write()         # writes the page for browser
```

Functions for HTML marks were provided:
 - p
 - div
 - form
 - link
 - form\_input
 - br
 - hr
 ....

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
