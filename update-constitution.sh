#!/bin/bash
git submodule init
git submodule update
pandoc constitution/constitution.md -o avery_website/templates/constitution-contents.html
