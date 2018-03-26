# Goal

Simple add-on that sets the PATH environment variable inside Blender.

This add-on is probably only useful on **OS X**, and **is probably not compatible with Windows** (I haven't tested it on Windows and do not intend to do so).

This might be useful for other add-ons depending on PATH to execute shell commands.

You should probably search for other methods to globally set your path instead. For example with:

```
sudo launchctl config user path <user_path_setting>
```

# Installation

Click "Clone or download", then "Download ZIP", then use "Install Add-on from File…"in Blender’s preferences.

Or clone the repository in your "add_ons" directory.


# Usage

Install the add-on, then set a prefix and/or a suffix using the preferences.

If:

- your original path is `/usr/bin:/bin:/usr/sbin:/sbin`,
- you set prefix to `/usr/local/bin`,
- you set suffix to `/Users/myname/bin`,

then the final path will become `/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/myname/bin`.
