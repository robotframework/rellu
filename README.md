# 🛠️ rellu – Utilities to Ease Creating Releases

This project provides **tooling and templates** to ease the creation of releases on **GitHub** and their publication on **PyPI**. It is primarily designed for **Robot Framework** and the tools and libraries in its ecosystem, but can naturally be used by other projects as well.

To successfully adopt this project, you should be familiar with at least the **basics of Python packaging**.

## ✨ Main Features

The core features of `rellu` are organized into reusable utilities and generic `Invoke` tasks:

### 1. **Utilities (`rellu` module)**

These utilities can be used by custom `Invoke` tasks and are directly importable from the `rellu` module:

* **Setting the project version**, including automatically setting it to the next suitable **development version**.
* **Setting common labels** in the issue tracker.
* **Generating release notes** based on issues in the tracker. This requires the project to use predefined labels.

### 2. **Generic `Invoke` Tasks (`rellu.tasks` module)**

* **Cleaning up** temporary files and directories.
* **`tasks.py`:** An example file implementing `Invoke` tasks using the aforementioned utilities. Other projects can use it as an **example or template**.
* **`BUILD.rst`:** A file containing **step-by-step instructions** for creating releases using the `Invoke` tasks defined in `tasks.py`, Git, and other tools. This file can also be used as a **template**.
* **`setup.py`:** A file that follows general good practices and can also serve as a **template**. A very simple **`MANIFEST.in`** file is also included, though this project does not require a **`setup.cfg`**.

## 🔗 Dependencies

`Rellu` is designed to be used **together with `Invoke`**, which is also utilized internally. All project dependencies are listed in the **`requirements.txt`** and **`requirements-build.txt`** files.

### System Requirements:

* **Python:** `Rellu` itself works only with **Python 3.10 or newer**. Projects that use it can, of course, also support older Python releases.
* **Operating System:** It is developed and tested on **Linux**, but ought to work just fine on **OSX**. Using it on **Windows** may work, but this is **neither tested nor officially supported**.



## ⚙️ Required Project Setup

To be able to **automatically generate release notes**, the project's issue tracker must be configured using these rules:

1.  **Milestones** must match project versions and use the format **`v1.2`** or **`v1.2.1`**.
2.  **Labels** must be configured using the provided utility.
3.  **Milestones and labels** must be used consistently:
    * Valid issues must have their **type** defined as a label: **`bug`**, **`enhancement`**, or **`task`**. Issues with the `task` type are **not** included in the release notes.
    * Issues should have their **priority** set using either the organization level **Priority** issue field or the appropriate **`priority:`** labels. If both are set, the field wins. Field options are mapped to rellu priorities by default as `Urgent` → `critical`, `High` → `high`, `Medium` → `medium` and `Low` → `low`. Use the `priority_mapping` argument of `ReleaseNotesGenerator` to map other options. It extends the default mapping and overrides it for options given in both, for example `priority_mapping={"P0": "critical"}`. Other issue fields, such as **Effort**, are ignored.
    * Issues belonging to a certain milestone should have that **milestone set**.
    * Issues included in certain preview releases should have a **matching label** set (e.g., **`a1`**, **`b2`**, **`rc3`**).