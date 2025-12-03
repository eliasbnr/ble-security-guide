---
sidebar_position: 2
title: "Report Templates"
---

# Report Templates

## Security Assessment Report Template

```latex
\documentclass[a4paper,11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{hyperref}

\title{BLE Security Assessment Report\\
       \large [Gerätename]}
\author{[Analyst Name]}
\date{\today}

\begin{document}
\maketitle

\section{Executive Summary}
% Kurze Zusammenfassung...

\section{Scope \& Methodology}
% Was wurde getestet, wie...

\section{Findings}
\subsection{V-001: [Vulnerability Name]}
\textbf{CVSS:} 9.8 (Critical)\\
\textbf{Description:} ...

\section{Remediation}
% Empfehlungen...

\end{document}
```

## Disclosure Template

```markdown
# Vulnerability Report

**Product**: [Name]
**Vendor**: [Hersteller]
**Severity**: Critical
**CVSS**: 9.8

## Summary
[Kurze Beschreibung]

## Timeline
- YYYY-MM-DD: Discovery
- YYYY-MM-DD: Vendor Contact
- YYYY-MM-DD: Public Disclosure (planned)

## Contact
[E-Mail]
```
