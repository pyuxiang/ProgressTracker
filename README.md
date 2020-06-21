# Progress Tracker

The one that I never got to finish, is starting again.

Required Python version: > 3.6

## Outline

### Data streams

There are several different sources for data streams:

1. **Excel file**

    1. *Updating*: User-friendly via Excel software, but becomes
    a lot more challenging when updating programmatically at the same
    time.
    2. *Reading*: Panda data frame, easy to work with. Many apps, including
    Dropbox, provide built-in viewing support.
    3. *Atomic updates*: Possible, but not intuitive. Will require a separate
    data store.


2. **SQLite database**

    1. *Updating*: Easy via SQL commands, but not directly intuitive. Cannot
    have visual overview of the database and past entries. May be circumvented
    with SQLite viewer software.
    2. *Reading*: Equally challenging.
    3. *Atomic updates*: Easy to query subset of data for updating.


3. **csv/text file**

    1. *Updating*: Requires user to manually adhere to formatting rules.
    2. *Reading*: Visually not appealing.
    3. *Atomic updates*: Separate data store.


4. **File properties**: Problem lies in cloning of files, mtime is modified
since git/sync libraries rely on diff.

### Design

Borrowing ideas from abstraction in the MVC model, we have:
1. Independent data streams
2. Updaters to modify data stream
3. Readers to parse into specified interchange format
4. Formatters to convert into required plot formats (JSON?)
5. Plotters to plot the graphs
6. Displayers to present as a dashboard

But honestly, until I have a substantial number of parsers, I can't be
bothered to do this abstraction for now.
