# Libreverse

Libreverse is a self-hosted alternative to the well-known large hosted collections of models for 3D printing, laser cutting, etc. (the stuff makers are interested in typically). It's a sort of static-site generator with an interactive server for development.

Originally, this repository was meant to be a collection of 3D models only. The majority was designed for 3D printing, using appropriate [design guidelines](design-guidelines.md). However, the website generator quickly turned out to be usable as a general-purpose self-hosted solution.


## File Formats

Most of the models are created in [FreeCAD](https://freecadweb.org). A few of them, especially more simple ones or models which allow for parametrization, are written in [OpenSCAD](https://openscad.org).

The models are stored in categories, and normally only by their source file. The README in the subdirectories reveal which version of which tool was used to create the models.

`.stl` files for 3D printing need to be exported by the users of this repository using these tools. They're not shipped in the Git repository, as storing generated files is bad practice. I would consider generating the files and uploading them somewhere, though, if users request such a feature.
