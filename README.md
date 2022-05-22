# gameboy-logo
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a code repo for [this blog post](https://dodslaser.com/blog/almost-booting-the-gameboy-with-a-custom-logo/).

Converts a 48x8 pixel white on black logo and converts it to a valid-ish gameboy ROM. Aside from the logo the header/rom is empty, so the bootloder will scroll the logo (di-ding!) and then freeze. Even if you were to replace the header in a real rom it won't boot past validation on real hardware.

Can also extract the boot logo from a gameboy rom. This isn't really useful, as all roms should just encode the nintendo logo.