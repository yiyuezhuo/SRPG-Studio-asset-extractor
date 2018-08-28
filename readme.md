# SRPG Studio asset extractor

The script is written to free too many `Save to file` click in SRPG Studio 
when you want to export assets in runtime.

## Usage 

```
$ python CLI.py asset_path
```

Example:

In powershell, if the script is in `E:\agent\rts_analysis`:

```
PS E:\agent\rts_analysis> python CLI.py "E:\steam\steamapps\common\SRPG Studio\english\runtime.rts"
```

Options:

* `output`: Output directory
* `raw`: Raw mode(loss file structure but may work on assets othen than runtime)