# wiki2rst

## About 

`wiki2rst` is for converting files in a `media wiki` format to `rst` format.
I wrote this as oart of a task to migrate docs from wiki to Sphinx.
The majority of the heavy work is done by [`Pandoc`](https://pandoc.org/), 
however I found a few niggling issues with the resultant format, so I have tried
to automate the fixes where ever possible.

## Requirements

* Python
* [Pandoc](https://pandoc.org/)

## Use

* In the top directory of your project:

```
python wiki2rst.py
```

This will produce `.rst` files in all directories containing `.wiki` files.

* Variables - these are set at the top of `rst2wiki.py`
  * `rootdir` : the root directory of the project
  * `imagedir`: the directory containing images - this is relative to the `rootdir`
  * `exceptions`: these are words that should not be capitalised in heading case

## What it does

* Runs `pandoc` conversion
* Sets up the image and figure paths correctly
* Removes ugly figure captions
* Creates a label for the referencing of created files
* Creates `index.rst` files based on the labels

## ToDo

* Make lables unique where two files in the toctree have the same name
* Fix up interal hyperlinks

