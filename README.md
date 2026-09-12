# Course Material Repository

This repository is a collaborative space for collecting, organising, and sharing notes and study material related to our course.

The goal is to keep both:

- **shared material**, curated and useful for everyone;
- **personal notes**, maintained individually by each student.

## Repository Structure

```text
course-material/
├── shared/
│   ├── core/
│   │   ├── advanced-software-engineering/
│   │   ├── machine-learning/
│   │   └── ...
│   │
│   └── elective/
│       ├── computer-vision/
│       └── ...
│
└── students/
    ├── bianchi-luca/
    │   ├── machine-learning/
    │   ├── artificial-intelligence/
    │   └── README.md
    │
    ├── rossi-mario/
    │   ├── machine-learning/
    │   └── ...
    │
    └── ...
```

## `shared/`

The `shared/` directory contains material intended to be useful for the whole class. It is divided into two categories:

- `core/`, for modules shared by all students;
- `elective/`, for optional modules.

Shared material may include:

- consolidated lecture notes;
- summaries;
- useful references and links;
- exercises and explanations;
- cheat sheets.

## `students/`

The `students/` directory contains personal notes from individual students.

Each student should have their own directory using the following naming convention:

```text
students/<surname>-<name>/
```

For example:

```text
students/rossi-mario/
├── machine-learning/
├── artificial-intelligence/
└── README.md
```

Inside your directory, you are free to organise your material however you prefer, although following the general module structure is encouraged.

Personal notes do not need to be polished or complete. They are primarily an archive of each student's own material that others may also find useful.

## Contributing

### Adding personal notes

Add or update files only inside your directory:

```text
students/<surname>-<name>/
```

Example:

```text
students/rossi-mario/machine-learning/week-03.md
```

### Adding shared material

Material that is intended for the whole class should be added to the appropriate directory under:

```text
shared/<category>/<module-name>/
```

For example:

```text
shared/core/machine-learning/linear-regression.md
```

Whenever possible, prefer Markdown (`.md`) for notes and documentation.

## Workflow

Please avoid pushing directly to the `main` branch.

The recommended workflow is:

1. Create a new branch from `main`.
2. Add or update your material.
3. Commit your changes with a clear message.
4. Push the branch.
5. Open a Pull Request.
6. Merge the Pull Request after review.

## File Naming

Use clear and consistent filenames.

Prefer:

```text
01-introduction.md
02-linear-regression.md
week-03.md
exam-summary.md
```

Avoid names such as:

```text
notes-final-final2.md
lecture-new.md
stuff.md
```

## Moving Personal Notes to Shared Material

If some personal notes are particularly complete or useful, they can be adapted and moved into the `shared/` directory through a Pull Request.

This allows personal notes to remain flexible while keeping the shared material curated.

## Guidelines

Please keep the following in mind:

- Respect other students' files and directories.
- Do not modify someone else's personal notes without discussing it with them first.
- Keep shared material organised and reasonably clear.
- Avoid unnecessary duplicate files.
- Prefer text-based formats such as Markdown whenever possible.
