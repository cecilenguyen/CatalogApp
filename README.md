# Udacity Project 3 - Catalog Project

A simple Python project for Udacity's full-stack nanodegree program. This catalog application contains a list of items within a variety of categories as well as a Google user registration and authentication system. Registered users have the ability to post, edit and delete their own items.

## Download

The files for this program may be downloaded or cloned from https://github.com/cecilenguyen/CatalogApp.

Use the following command in the command terminal:

`$ git clone https://github.com/cecilenguyen/CatalogApp.git`

## System Requirements
Installation instructions can be found on their respective sites.

- [Python 3.6.3](https://www.python.org/downloads/) or later
- [Git](https://git-scm.com/downloads)
- [Vagrant](https://www.vagrantup.com)
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Quick Start

After downloading or cloning the program files, navigate to the directory folder.

`$ cd <C:\Directory\files\downloaded\to>`

**Environment set up**
Start Vagrant VM by running the command `vagrant up` and then log in using `vagrant ssh`

Then initialize the database by running `$ python3 database_init.py`

This will create a new file for you called catalog.db.

**Run the program using the following command:**

`python3 app.py`

## Copyright and License

Google authentication code provided by Udacity



