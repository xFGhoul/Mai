"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from .console import console


class ASCII:
    def error():
        console.print(
            """[red]

                        ███████╗██████╗ ██████╗  ██████╗ ██████╗         ██╗
                        ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╗██╔╝
                        █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ╚═╝██║
                        ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ██╗██║
                        ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ╚═╝╚██╗
                        ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝        ╚═╝

        [/red]""",
            justify="full",
        )

    def line():
        console.print(
            "[red]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/red]"
        )
