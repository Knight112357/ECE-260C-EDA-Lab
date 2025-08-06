# ECE-260C EDA LAB

## ECE 260C Overview

**ECE 260C**, offered during Spring 2025 at UC San Diego, is an advanced graduate-level course that explores physical design using open-source EDA tools. It focuses on leveraging the **OpenROAD** flow and the **IHP130 PDK**, enabling students to build real digital chips from RTL to GDSII.

Unlike traditional VLSI courses, ECE 260C encourages students to go beyond the standard RTL-to-GDS2 flow. The course emphasizes complex scripting and tool customization, allowing students to deeply understand and modify the internals of EDA tools. With a strong focus on practical skills, students apply these methodologies in the context of modern SoC design.

The course was presented at both the **62DAC Open-Source EDA Birds-of-a-Feather (BoF)** and **FSiC 2025**, where it received attention for its open-source approach and educational impact.

More information can be found at:

- [Course website](https://abkcourses.github.io/ece260c/)
- [62DAC Open-Source EDA BoF](https://open-source-eda-birds-of-a-feather.github.io/)

## ECOS Graduate Admission Evaluation

This project serves as the qualification assessment for receiving a master's offer from the ECOS team.

In this project, I was responsible for:

- Independently implementing the design flow from the selected lab.
- Conducting rigorous experimental validation of the results.

The evaluation focused on three core areas:

1. **Technical Proficiency**
   - Mastery of open-source physical design tools (e.g. OpenROAD, Yosys etc.)
   - Algorithmic thinking for solving design and optimization problems
   - Debugging and tool integration flows
2. **Scientific Rigor**
   - Careful planning and setup of experiments
   - Accurate and in-depth analysis of placement, routing, timing closure, and power estimation
   - Critical thinking applied to problem diagnosis and solution development
3. **Learning Potential**
   - Ability to self-learn and explore beyond the course materials
   - Reflections on emerging trends in open-source EDA

## Project Structure & Submission

```bash
# Project Structure
├── Lab 0
│   ├── ECE 260C Lab 0.docx
│   ├── ECE 260C SP25 Software Setup Guide.pdf
│   ├── Lab 0-note.md
│   ├── pic
│   └── submitting
├── Lab 1
│   ├── ECE 260C Lab 1.docx
│   ├── ECE 260C Lab 1.pdf
│   ├── ece260c-lab1-ShijieSun
│   ├── Lab 1-note.md
│   ├── pic
│   └── RTFSC.md
├── Lab 2
│   ├── ECE 260C Lab 2.docx
│   ├── ECE 260C Lab 2.pdf
│   ├── ece260c-lab2-ShijieSun
│   ├── Lab 2-note.md
│   └── pic
├── Lab Report.md
└── README.md
```

The experiment requirements are detailed in the official project slide: [**Markarian Redistribution Project Requirements**](https://github.com/open-source-eda-birds-of-a-feather/open-source-eda-birds-of-a-feather.github.io/blob/main/doc/slides_2025/dac25_markarian_redist.md)

ECE 260C OpenROAD-based Course Contents (Licensed under CC-BY 4.0)

- [Lab Report Templates for Labs 0, 1, and 2 + Software Setup Guide ](https://drive.google.com/drive/folders/1MrlXrB3YWksrl2f39SWJWSwLcT9NGsXm?usp=sharing)
- GitHub Starters templates for the Labs (Licensed under Apache 2): [Lab 1](https://github.com/UDXS/ece260c-lab1-starter), [Lab 2](https://github.com/UDXS/ece260c-lab2-starter)

### Lab 0

[Lab 0 report](./Lab%200/submitting/ECE%20260C%20Lab%200.pdf)

[Lab 0 Submission](./Lab%200/submitting/):

```bash
config.mk
6_finish.rpt
cts_core_clock_layout.webp.png
6_report.json
6_final.gds
```

### Lab 1

[Lab 1 report](./Lab%201/ECE%20260C%20Lab%201.pdf)

[Lab 1 Submission](./Lab%201/ece260c-lab1-ShijieSun)

```bash
Lab 1/ece260c-lab1-ShijieSun/
├── LICENSE
├── README.md
├── section1
│   ├── gcd.v
│   ├── sg13g2_stdcell_typ_1p20V_25C.lib
│   └── sub
├── section2
│   ├── analysis.tcl
│   ├── dse.analysis.json
│   ├── dse.png
│   ├── dse.postmap.v
│   ├── dse.stat.json
│   ├── dse.table.json
│   ├── explore.py
│   ├── rtl
│   ├── sg13g2_stdcell_typ_1p20V_25C.lib
│   └── synth.tcl
└── section3
    ├── config.mk
    ├── constraint.sdc
    ├── logs
    ├── objects
    ├── reports
    ├── results
    └── rtl
```

### Lab 2

[Lab 2 report](./Lab%202/ECE%20260C%20Lab%202.pdf)

[Lab 2 Submission](./Lab%202/ece260c-lab2-ShijieSun)

```bash
Lab 2/ece260c-lab2-ShijieSun/
├── LICENSE
├── README.md
├── section1
│   ├── area.py
│   ├── design
│   ├── section1.odb
│   └── template.py
├── section2
│   ├── design
│   ├── move.odb
│   ├── move.py
│   ├── section2.odb
│   ├── swaps.odb
│   ├── swaps.py
│   └── template.py
├── section3
│   ├── design
│   ├── placer.odb
│   ├── placer.py
│   └── section3.odb
└── sg13g2_stdcell_typ_1p20V_25C.lib
```

### Final Report

[Lab report](./Lab%20Report.md)

## Academic Integrity Statement

I affirm that all reports and code submitted for this project were **independently completed by myself** in accordance with the principles of [academic integrity](https://integrity.mit.edu).

In the process of completing this project, I adhered to the spirit of **RTFM** (Read The Friendly Manual), **RTFSC** (Read The Friendly Source Code), and **STFW** (Search The Friendly Web).

Some notes and explanations were organized or summarized with AI assistance under the guideline of **ATFAI** (Ask The Friendly AI), with the permitted scope defined by [jyy's advice](https://jyywiki.cn/OS/2025/labs/Labs.md).

