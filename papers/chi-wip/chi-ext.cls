% CHI Extended Abstracts template.
% Tested with a clean LaTeX installation on Windows XP, Ubuntu 9.04 and above (should work in normal LaTeX environments)
% 
% Filename: chi-ext.cls
% 
% Features:
%	- simpler design, two 'real' columns, better handling of footnotes/marginal notes
%	- adheres to ACM archival format, so you don't need to change your LaTeX markup significantly from other ACM templates
%	- font sizes, spacing between paragraphs, and look&feel more according to CHI's Ext. Abstracts template (MS Word)
%	- supports an optional ACM teaser image on first page
%	- improved PDF bookmarking
%
% CHANGELOG:
%   2010-12-01   Luis A. Leiva      A lot of refactorization.
%   2010-10-18   Manas Tungare      Restored support for \figures.
%   2010-08-09   Manas Tungare      Updated copyright info for CHI 2011
%   2009-12-04   Stephen Voida      Updated copyright info for CHI 2010
%   2009-11-17   Manas Tungare      Refactored the title & author sections.
%   2008-11-25   Manas Tungare      Initial create.
% 
% LICENSE:
%   Public domain: You are free to do whatever you want with this template.
%   If you improve this in any way, please drop me a note <llt@acm.org>,
%   so we can share the updates with everyone.


\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{chi-ext}[2010/12/01, Luis A. Leiva]

\typeout{CHI Extended Abstracts template, original design by Manas Tungare, modified and refactored by Luis A. Leiva}
\typeout{Available at http://personales.upv.es/luileito/chiext/}

\LoadClass[10pt,letterpaper,landscape]{article}[1996/10/31]

% -----------------------------------------------------------------------------
% Set paper and margin sizes

\setlength{\paperheight}{8.5in}
\setlength{\paperwidth}{11in}

\setlength{\textwidth}{7.25in}
\setlength{\textheight}{6in}

\setlength{\oddsidemargin}{1.5in}
\setlength{\topmargin}{0.25in}

\setlength{\columnsep}{0.5in}

\setlength{\voffset}{-0.2in}

\setlength{\parindent}{0pt}
\setlength{\footskip}{0.5in}

\setlength{\marginparsep}{15pt}
\setlength{\marginparwidth}{1.8in}

\setlength{\itemsep}{0pt}
\setlength{\parsep}{0pt}
\setlength{\topsep}{0pt}
\setlength{\parskip}{9pt}

% -----------------------------------------------------------------------------
% Set paper columns and avoid justifying text, according to CHI's MS Word template

\twocolumn
\raggedright

% Use LaTeX standard sans-serif fonts
\renewcommand*\familydefault{\sfdefault}

% -----------------------------------------------------------------------------
% Allowed environments and commands

\renewenvironment{table}{\def\@captype{table}}{}
\renewenvironment{figure}{\def\@captype{figure}}{}
\renewcommand{\thanks}[1]{} % No thanks in this template
\pagestyle{empty} % No page numbers

% -----------------------------------------------------------------------------
% Paper Metadata

\newcommand*{\copyrightinfo}[1]{\gdef\@copyrightinfo{\raggedright#1}}

\def\keywords{
\section*{Author Keywords}
}

\def\terms{
\section*{General Terms}
}

% -----------------------------------------------------------------------------
% ACM Classification - Gerry/Georgia November 2nd. 1999

\newcount\catcount
\global\catcount=1

\def\category#1#2#3{%
\ifnum\catcount=1
  \section*{ACM Classification Keywords}
  \advance\catcount by 1\else{\unskip; }%
\fi
\@ifnextchar [{\@category{#1}{#2}{#3}}{\@category{#1}{#2}{#3}[]}%
}

\def\@category#1#2#3[#4]{%
  \begingroup
    \let\and\relax
%    #1 [\textbf{#2}]%
    #1 [#2]% 
    \if!#4!%
      \if!#3!\else : #3\fi
    \else
     :\space
     \if!#3!\else #3\kern\z@---\hskip\z@\fi
     \textit{#4}%
    \fi
  \endgroup
}

% -----------------------------------------------------------------------------
% Typeset titles of chapters and sections in sans-serif

\def\@makeschapterhead#1{
  \vspace*{50\p@}
  {\parindent \z@ \raggedright
    \sffamily
    \interlinepenalty\@M
    \Huge\bfseries #1\par\nobreak
    \vskip 20\p@
  }
}

\def\sectionsindent{\z@}
\def\sectionsbeforeskip{-3.5ex \@plus -0.1ex \@minus -0.2ex}
\def\sectionsafterskip{0.2ex \@plus 0.01ex}
% LaTeX scheme is {name}{level}{indent}{beforeskip}{afterskip}{style}
\renewcommand\section{
  \@startsection{section}{1}{\sectionsindent}{\sectionsbeforeskip}{\sectionsafterskip}%
  {\sffamily\large\bfseries\phantomsection}
}
\renewcommand\subsection{
  \@startsection{subsection}{2}{\sectionsindent}{\sectionsbeforeskip}{\sectionsafterskip}%
  {\sffamily\normalsize\itshape\phantomsection}
}
\renewcommand\subsubsection{
  \@startsection{subsubsection}{3}{\sectionsindent}{\sectionsbeforeskip}{\sectionsafterskip}%
  %{\sffamily\MakeUppercase\small\itshape\phantomsection}
  {\sffamily\normalsize\itshape\phantomsection}
}
     
% Now remove vertical space after sections (same as class' font size)
\usepackage[compact]{titlesec}
\titlespacing{\section}{0pt}{*0}{-9pt}
\titlespacing{\subsection}{0pt}{*0}{-9pt}
\titlespacing{\subsubsection}{0pt}{*0}{-9pt}                              

% Add references to TOC
\let\myrefname\refname
\renewcommand\refname{\addcontentsline{toc}{section}{\myrefname}\myrefname}

% Typeset captions
\usepackage[small,bf,sf]{caption}
\captionsetup{font={small,sf},textfont=sf,justification=raggedright}

% Typeset URLs
\usepackage{url}
% Define a (compact) global style for URLs, rather than the default one
\def\url@leostyle{\@ifundefined{selectfont}{\def\UrlFont{\sf}}{\def\UrlFont{\small\bf\ttfamily}}}
\urlstyle{leo}

% Set footones ALWAYS at the bottom of the pages
\usepackage[bottom]{footmisc}

% Optionally save space in lists (place this command after a list environment (e.g., itemize, enumerate, description)
\newcommand{\compresslist}{
  \vspace{-1em}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}
}

% -----------------------------------------------------------------------------
% Hyperref for fancy typesetting, PDF metadata, and PDF bookmarks

\RequirePackage[
  colorlinks,
  citecolor=red,
  linkcolor=blue,
  menucolor=blue,
  %urlcolor=blue, % use hyperref defaults
  linktocpage,
  naturalnames,
  plainpages,
  final
]{hyperref}

% Numbering is not allowed for any {sub{sub}}sections
\setcounter{secnumdepth}{-1}

% -----------------------------------------------------------------------------
% Text enhancements

\doublehyphendemerits=9999        % No consecutive line hyphens
\brokenpenalty=9999               % No broken words across pages
\widowpenalty=9999                % Almost no widows at bottom of page
\clubpenalty=9999                 % Almost no orphans at top of page
\interfootnotelinepenalty=9999    % Almost never break footnotes

% -----------------------------------------------------------------------------
% Allow placing an optional teaser image below author(s) name

\newcommand{\acm@empty}{}
\newcommand{\acm@teaser}{}
\newcommand{\teaser}[1]{\renewcommand{\acm@teaser}{#1}}

% -----------------------------------------------------------------------------
% Authors handling

\gdef\numberofauthors#1{}
\newcommand{\alignauthor}[1]{%
  \parbox[t]{0.5\linewidth}{\raggedright#1}%
}
\newcommand{\affaddr}[1]{#1}
\newcommand{\email}[1]{#1}

% -----------------------------------------------------------------------------
% Typeset first page

\renewcommand{\maketitle}{
  % allocate paper title
  \begin{minipage}[t]{0.19\textwidth}\mbox{}\end{minipage}%
  \begin{minipage}[b]{0.81\textwidth}
    \rule{1.03\textwidth}{3pt}
  	\renewcommand\baselinestretch{0.75}
    \usefont{OT1}{phv}{bc}{n}\selectfont
    \raggedright\Huge\bfseries\@title\par
  \end{minipage}

  \vfil

  % allocate authors, optional teaser, ...
  \begin{minipage}[b][0.74\textheight][b]{\linewidth}
    \ifx\acm@teaser\acm@empty 
      \begin{minipage}[t][0.6\textheight][t]{\linewidth}{\small\@author}\end{minipage}
    \else
      \small\@author\par
      \vfill
      \begingroup
        \def\@captype{figure}
        \acm@teaser
      \endgroup\par
    \fi

    \vfil
    
    % ... and ACM copyright
    \rule{\columnwidth}{0.5pt}
    {\small\@copyrightinfo}
  \end{minipage}

  % avoid title overlapping with abstract 
  \begin{minipage}[t][0.2\textheight][t]{\linewidth}\mbox{}\end{minipage}
}

\endinput
% That's all folks!