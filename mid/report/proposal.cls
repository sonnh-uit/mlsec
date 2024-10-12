% ========= Config paper and font =============
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{proposal}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{memoir}}
\ProcessOptions\relax
\LoadClass[14pt,a4paper]{memoir}
% ========== Require package to setup paper, link, language
\RequirePackage{anyfontsize,mathptmx}
\RequirePackage[T5]{fontenc}
\RequirePackage{geometry,graphicx,indentfirst,setspace}
\RequirePackage{tikz}
\RequirePackage[center]{caption}
\RequirePackage{fancyhdr,hyperref}
\RequirePackage[vietnamese,english]{babel}
\RequirePackage{listings}
\RequirePackage{graphicx}
\RequirePackage{chngcntr}
\usetikzlibrary{calc}
\hypersetup{urlcolor=blue,linkcolor=black,citecolor=black,colorlinks=true} 

% ===========Set command to provide param ===========
\newcommand{\@upperuniname}{}
\newcommand{\upperuniname}[1]{\renewcommand{\@upperuniname}{#1}}
\newcommand{\@uniname}{}
\newcommand{\uniname}[1]{\renewcommand{\@uniname}{#1}}
\newcommand{\@titleen}{}
\newcommand{\titleen}[1]{\renewcommand{\@titleen}{#1}}
\newcommand{\@defcouncil}{Council}
\newcommand{\defcouncil}[1]{\renewcommand{\@defcouncil}{#1}}
\newcommand{\@supervisorname}{}
\newcommand{\supervisorname}[1]{\renewcommand{\@supervisorname}{#1}}
\newcommand{\@stuname}{}
\newcommand{\stuname}[1]{\renewcommand{\@stuname}{#1}}

% =========== Overwrite exist command to custom project ============
\renewcommand{\@title}{}
\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\footrulewidth}{0pt}
\renewcommand{\large}{\fontsize{14}{14}\selectfont}
\renewcommand{\Large}{\fontsize{20}{20}\selectfont}
\renewcommand{\arraystretch}{1.2}
\renewcommand*{\lstlistingname}{Đoạn mã}
\renewcommand\lstlistlistingname{Danh sách đoạn mã}
\newcommand{\@proposaltype}{}
\newcommand{\proposaltype}[1]{\renewcommand{\@proposaltype}{#1}}
\newcommand{\@reportplace}{}
\newcommand{\reportplace}[1]{\renewcommand{\@reportplace}{#1}}


\renewcommand{\subsectionmark}[1]{\markright{\thesubsection.\ #1}}

\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}
\renewcommand{\thefigure}{\arabic{section}.\arabic{figure}}

% ==========Setup paper margin and footer==========
\geometry{
  paper=a4paper,
  left=3cm,
  right=2cm,
  vmargin=2cm,
  includeheadfoot=true,
  headheight=30pt
}
\OnehalfSpacing
\raggedbottom

% Set depth of numbering for sections and table of contents
\setsecnumdepth{subsubsection}
\settocdepth{subsubsection}

% Set numwidths
\setlength{\cfttablenumwidth}{3em}
\setlength{\cftfigurenumwidth}{3em}
\AtBeginDocument{\renewcommand*\bibname{References}}

% ==========Setup corlor for link and url==========
\hypersetup{
  colorlinks=true,
  linkcolor=black,
  citecolor=blue,
  urlcolor=blue
}

% ========== Start create cover page, fancy is package to draw line, paper..==========
\pagestyle{empty}
\fancyhf{}

% Header box

\def\headerbox {
    \begin{tikzpicture}[remember picture,overlay]
        \draw[line width=3pt](
        $(current page.north west) + (0.7cm,-0.7cm)$
        ) rectangle (
        $(current page.south east) + (-0.7cm,0.7cm)$
        );
        \draw[line width=1pt](
        $(current page.north west) + (1cm,-1cm)$
        ) rectangle (
        $(current page.south east) + (-1cm,1cm)$
        );
      \end{tikzpicture}
}

\geometry{top=1cm, bottom=1cm, left=0.7cm, right=1cm}
\def\vnproposalheader{
    \pagestyle{empty}
    \begin{center}
        \begin{tabular}{ccc}
            \includegraphics[width=0.12\textwidth]{imgs/vnu_logo.png} &
            \begin{minipage}[b]{0.73\textwidth}
                \centering
                \large\textbf{\MakeUppercase{\@upperuniname}} \\
                \large\textbf{\MakeUppercase{\@uniname}}
            \end{minipage} &
            \includegraphics[width=0.1\textwidth]{imgs/UIT-logo.png} \\
        \end{tabular}
    \end{center}
    \vspace{2cm}
    
    
}

\geometry{paper=a4paper,top=2cm, bottom=2cm, left=2cm, right=2cm}
\def\proposalname {
    \begin{center}
        \Large\textbf{BÁO CÁO GIỮA KỲ} \\
        \vspace{0.5cm}
        \large\MakeUppercase{\textbf{\@proposaltype}} \\
        \vspace{3cm}
        {\large{\centering\MakeUppercase{\textbf{Tên đề tài: \@title}}}} \\
        % \vspace{1cm}
        % {\large{\centering\MakeUppercase{\textbf{Tên đề tài tiếng Anh: \@titleen}}}}
        \vfill
        {\large{\centering\MakeUppercase{\textbf{Giảng viên hướng dẫn \\ \@supervisorname}}}} \\
        \vfill
        {\large{\centering\MakeUppercase{\textbf{Học viên thực hiện}}}} \\
        \vspace{0.5cm}
        {\large{\centering\MakeUppercase{\textbf{ \@stuname}}}}
        \vfill
        \uppercase{\@reportplace \the\year{}}
    \end{center}

    % \pagestyle{fancy}
}


\geometry{paper=a4paper,top=2cm, bottom=2cm, left=3cm, right=2cm}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}