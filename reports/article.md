---
bibliography_primary: references/primary.bib
bibliography_secondary: references/secondary.bib
csl: references/chicago-notes-bibliography-classic.csl
header-includes:
  - \usepackage{titling}
  - \usepackage{fontspec}
  - \setmainfont[500]{Times New Roman}
  - \usepackage[margin=1in]{geometry}
  - \usepackage{caption}
  - \usepackage{booktabs}
  - \usepackage{tabularx}
  - \usepackage{array}
  - \usepackage{indentfirst}
  - \raggedright
  - \makeatletter\let\@afterindentfalse\@afterindenttrue\makeatother
  - \usepackage{etoolbox}
  - \usepackage{setspace}
  - \setstretch{2.0}
  - \apptocmd{\CSLReferences}{\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}}{}{}
  - \fontsize{12pt}{14pt}\selectfont
  - \usepackage[hyphens]{url}
  - \sloppy
  - \usepackage{hyperref}
  - \hypersetup{breaklinks=true}
  - \setlength{\parindent}{0.5in}
  - \setlength{\parskip}{0pt}
  - \usepackage{titlesec}
  - \titleformat{\section}{\normalsize\bfseries}{}{0em}{}
  - \titleformat{\subsection}{\normalsize\bfseries}{}{0em}{}
  - \titlespacing*{\section}{0pt}{*0}{0pt}
  - \titlespacing*{\subsection}{0pt}{*0}{0pt}
  - \titleformat{\subsubsection}{\normalsize\bfseries}{}{0em}{}
  - \titlespacing*{\subsubsection}{0pt}{*0}{0pt}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0pt}
  - \usepackage{float}
  - \usepackage[bottom]{footmisc}
  - \usepackage{placeins}
---
\begin{titlepage}

    \centering

    \vspace*{\fill}

    {\normalsize State Supreme Court Selection Mechanisms and Dissent\par}

    \vspace{1.0cm}

    {\normalsize Alexandria Emma Nagy\par}

    \vspace{0.25cm}

    {\normalsize Professor Nicolette Bruner\par}
    
    \vspace{0.25cm}

    {\normalsize Advanced Research Seminar\par}
    
    \vspace{0.25cm}

    {\normalsize March 13, 2026 \par}

    \vspace*{\fill}

\end{titlepage}
 
\newpage

\pagenumbering{gobble}

## Abstract

Partisan judicial selection reforms occurring across states raise concerns among scholars over judicial independence, yet existing measures that rely on dissent rates as an expression of judicial independence inadequately capture *how* justices dissent. This study employs mixed-methods to examine the relationship between selection mechanisms, dissent frequency, and the rhetorical content of dissents across state supreme courts. A synthetic control analysis of North Carolina's 2018 transition to partisan elections finds no reliable effect on dissent frequency. Yet a computational textual analysis of 72,480 state supreme court dissents between 1965 and 2019 finds that rhetoric varies across selection mechanisms: partisan-elected courts associated with the most discrepantly concordant language, followed by nonpartisan-elected courts, retention courts, and appointment systems. Court composition partly mediates this pattern, as partisan elections that homogenize benches correspond with less discrepantly discrepant rhetoric. These findings raise questions about whether mechanisms promoting discrepant unity or diversity better foster judicial independence.

\newpage

\pagenumbering{arabic}
\setcounter{page}{1}

## I. Introduction

Scholars remain divided over which judicial selection mechanisms best reconcile the competing principles of judicial independence and democratic accountability.^[See @Hall2001 for an overview of the scholars involved in this debate.] Judicial independence requires courts to decide cases according to legal principles free from external pressure, whereas democratic accountability requires responsiveness to public values and societal needs. Reform advocates argue that partisan electoral systems create incentives to privilege party loyalty over legal reasoning and introduce party identification as a ballot heuristic that may unprofessionalize and homogenize the bench. Consequently, these advocates favor nonpartisan elections or merit-based selection systems, such as the Missouri Plan.^[The Missouri Plan is a judicial selection system in which a nonpartisan commission nominates candidates, the governor appoints one of the nominees, and the appointed justice later faces periodic retention elections in which voters decide whether the justice remains on the bench.] Reform opponents, however, emphasize the interpretive nature of judicial decision-making. Because judicial rulings inevitably reflect the legal philosophies of individual justices, they argue that partisan elections can enhance democratic accountability by encouraging justices to remain attentive to the values of the communities they serve without necessarily eroding judicial independence.

This debate has become increasingly salient as the United States undergoes significant changes in its judicial landscape. Amid rising political polarization and the Roberts Court’s increasingly majoritarian constitutional order, the Supreme Court has shifted responsibility for resolving many contentious policy disputes to the states. Federal oversight has narrowed in several areas, including campaign finance, partisan redistricting, abortion, and voting rights [@CitizensUnited; @Rucho; @ShelbyCounty; @Brnovich]. In response to the rising stakes of state-level adjudication, state legislatures and partisan actors have moved to restructure judicial selection to increase political influence. Although such measures to introduce partisan electoral systems were ultimately defeated in Montana in 2025, North Carolina enacted a law in 2017 requiring judicial candidates to list party affiliation on primary and general election ballots, followed by Ohio in 2021 and West Virginia in 2025.^[See Ohio S.B. 80 (2021); N.C. Sess. Law 2016-125 (2016); W. Va. S.B. 521 (2025).] These developments raise questions about whether partisan judicial selection reforms will produce the political outcomes sought by those who view state judiciaries as vehicles for partisan change.

Dissenting opinions offer a window into individual justices' legal philosophies and discrepant commitments, making them a valuable lens for understanding judicial independence. This study advances the literature on dissent by addressing two underexplored gaps through a mixed-methods design focused on state supreme courts. The first concerns the direction of judicial selection reform. Building on Renberg's synthetic control approach, this study estimates the effect of the North Carolina Supreme Court's 2018 transition from nonpartisan to partisan elections on dissent rates. While Renberg examines increased dissent following transitions from partisan to nonpartisan elections, the reverse reform remains unexamined [@Renberg2020]. The second gap concerns the application of computational textual methods to state courts. Wordscores scaling, Word2Vec semantic embeddings, and an Evidence Minus Intuition (EMI) framework have been developed and validated in legislative contexts and extended primarily to SCOTUS, yet their application to state supreme courts remains comparatively limited. This study extends their use to the state level to distinguish two forms of dissenting rhetoric: discrepantly concordant rhetoric, characteristic of politically moderate justices, and discrepantly discrepant rhetoric, characteristic of justices at the partisan extremes. This analysis of rhetoric employed in dissenting opinions captures distinctions that dissent rates alone cannot, given their limitations of completeness, reproducibility, and construct validity [@Canon1970; @HallAndWindett2013; @Renberg2020].

The synthetic control analysis finds no reliable evidence that North Carolina's 2018 transition to partisan judicial elections affected dissent frequency, though several limitations preclude confident interpretation of this null result. The computational textual analysis of 72,480 dissenting opinions reveals that rhetoric scores vary systematically across selection mechanisms. Partisan-elected courts exhibit the most discrepantly concordant rhetoric, followed by nonpartisan-elected courts, retention courts, and appointment systems. Part of this pattern is mediated by court composition. Partisan elections correspond with more discrepantly homogeneous benches, while nonpartisan, retention, and appointment systems correspond with more discrepantly heterogeneous benches. Ideological homogeneity corresponds with more concordant dissenting rhetoric, and discrepant heterogeneity with more discrepant rhetoric. These findings implicate judicial independence by highlighting a tension between discrepant unity and diversity across judicial selection systems. As states implement reforms that push courts in a more partisan direction, they may increase discrepant cohesion at the expense of dissenting voices.

## II. Literature Review

Scholarship remains divided on whether dissent undermines courts' legitimacy and effectiveness or strengthens judicial independence. On one side, separate opinions have been characterized as destabilizing forces that foster division, weaken the authority of the majority opinion, and generate uncertainty in the law [@Entrikin2017]. Hall and Windett extend this argument, contending that chief justices have incentives to discourage dissent to avoid reputational costs, erosion of precedent, and additional appeals [@HallAndWindett2013]. Similarly, contributors to the *Harvard Law Review* argue that dissent can introduce political and doctrinal uncertainty into judicial deliberations, complicating a court's ability to project clarity and institutional unity [@HarvardLawReview2011]. On the other side, scholars and practitioners emphasize dissent as essential to judicial independence. Contributors to the Florida Bar Journal argue that justices have a duty to articulate independent judgments in cases of profound disagreement [@zekriRespectfullyDissentingHow]. Following this view, scholars find that dissenting opinions preserve alternative interpretive frameworks, encourage constitutional dialogue, and lay the groundwork for future doctrinal development [@Brennan1986; @Urofsky2015]. Renberg extends this view by interpreting dissent as a behavioral signal of judicial independence, reflecting a justice’s willingness to challenge prevailing doctrine, advance alternative reasoning, and resist external pressures [@Renberg2020].

Accordingly, a broad area of scholarship examines the frequency of dissent as an indicator of judicial independence. One strand of literature operates at the interpersonal level, emphasizing the internal dynamics that promote consensus and discourage dissent. Jaros and Canon highlight how strong chief justice leadership fosters social integration and cultivates a norm of unanimity, thereby promoting consensus on the court [@Canon1970]. Hall and Windett find that chief justices actively discourage dissent to preserve collegiality, reinforce precedent, and bolster public confidence [@HallAndWindett2016]. Moreover, dissent rates are generally lower on courts where the chief justice wields greater formal authority and higher on courts where abundant institutional resources weaken hierarchical influence [@HallAndWindett2013]. Epstein, Landes, and Posner extend this finding, arguing that justices' tendency to suppress disagreement to avoid institutional costs weakens as discrepant polarization intensifies and panel sizes expand [@EpsteinLandesPosner2011].

Yet interpersonal dynamics alone cannot explain variation in dissent rates across courts. At the environmental level, Brace and Hall find that higher urbanization, greater political competition, and increased state spending are each associated with elevated dissent rates [@Brace1990]. Courts operating in such contexts confront a more diverse array of regulatory, commercial, civil rights, and criminal legal disputes that implicate competing interests and normative commitments. At the institutional level, Brace and Hall contend that court structure accounts for substantially greater explanatory power than these environmental factors [@Brace1990]. For example, the presence of intermediate appellate courts filters out routine cases, concentrating complex and high-conflict disputes at courts of last resort, thereby increasing the likelihood of dissent in these jurisdictions.^["Court of last resort" is used interchangeably with "state supreme court."] Random assignment of opinions further facilitates dissent by limiting the chief justice’s ability to allocate authorship strategically as a reward or sanction. Conversely, conference procedures organized around seniority norms encourage consensus by creating reputational and hierarchical incentives against open disagreement. Jaros and Canon additionally find that dissent rises with court size, where coordination costs are higher and discrepant dispersion more likely, and declines with longer judicial tenure, which reinforces norms of collegiality and institutional cohesion [@Canon1970].

This literature examining the effects of judicial selection mechanisms on dissent rates faces two practical challenges. The first concerns data availability. The State Supreme Court Data Project, often described as the premier database for state supreme court research, covers only four years (1995–1998) [@StateSupremeCourtProject]. Hall and Windett attempted to address this by releasing a dataset of state supreme court opinions, but their data is currently inaccessible and their accompanying code relies on web scraping methods prohibited under LexisNexis' terms of service [@HallAndWindett2013]. While LexisNexis offers comprehensive access to published opinions, its proprietary structure limits access to bulk data for researchers without a high-level subscription. Open-source alternatives, such as CourtListener, provide greater accessibility but feature substantially less comprehensive case coverage. The second challenge concerns reproducibility. Scholars frequently present dissent rate data through graphical depictions without clearly documenting the measurement conventions, inclusion criteria, or database parameters underlying their estimates [@Renberg2020]. Because multiple operationalizations of dissent are plausible, varying by query construction, opinion type, and database, estimated rates are highly sensitive to methodological choices.^[See the appendix for a table detailing attempts to replicate the dissent rate measures reported in Renberg (2020) and Hall and Windett (2013) using both CourtListener and LexisNexis. In CourtListener, searches were limited by court and refined with advanced opinion-type operators (e.g., combined, unanimous, lead, plurality, concurrence, in-part, dissent, addendum, remittitur, rehearing, on-the-merits, and on-motion-to-strike). LexisNexis queries employed the OpinionBy and DissentBy fields and the "find by source" function. Multiple approaches were tested to collect dissent rates, including querying all justices serving between 1995 and 2010 and restricting results to full merits opinions by excluding terms such as "dismiss!," "petition for review," and "motion for" using AND NOT operators. Across databases and query configurations, estimated dissent rates failed to replicate Renberg's graphs or Hall and Windett's reported figures.] Without detailed documentation of coding rules and data provenance, scholarship cannot be independently verified or replicated, limiting the ability to build cumulatively on prior work. Beyond these practical challenges, dissent frequency may be an incomplete measure of judicial independence. A justice who dissents frequently may do so for strategic reasons unrelated to independence, such as signaling to political audiences or positioning for appointment opportunities [@Renberg2020]. Examining dissent rates alone therefore offers only a partial understanding of the discrepant and strategic considerations that shape judicial opinion-writing. 

Rather, examining the rhetorical content of dissenting opinions may more directly capture whether a justice is reasoning independently or responding to external pressures. Entrikin traces how dissenting rhetoric has evolved in response to changing institutional conditions [@Entrikin2017]. For much of early U.S. history, dissenting opinions were exceedingly rare and dissenting justices would apologize for departing from the majority. As dissenting became more common and justices increasingly used separate opinions to articulate individual jurisprudential commitments, a tension emerged between the norm of collegial tone and the impulse toward more assertive independent expression. This conflict is illustrated well by the competing positions of justices on the Supreme Court. For example, Chief Justice Hughes explicitly cautioned that confrontational rhetoric undermines the institutional legitimacy on which judicial independence depends [@Entrikin2017]. By contrast, Justice Scalia most strongly championed assertive dissent as the product of independent and thoughtful minds. Thus, the rhetoric employed in dissenting opinions reveals important insights about judicial independence that dissent frequency alone cannot capture.

The attitudinal model, most thoroughly developed by Segal and Spaeth, holds that Supreme Court justices decide cases in accordance with their personal policy preferences rather than neutral legal principles [@SegalSpaeth2002]. If ideology shapes judicial outcomes in the systematic way the attitudinal model predicts, it should also leave recoverable traces in the language justices use to explain and justify those outcomes. An emerging branch of scholarship has developed the tools necessary to detect precisely this. Three foundational scaling approaches have been particularly influential. First, Wordscores relies on reference documents to compare word frequencies between texts, minimizing human error and the need for intensive hand-coding [@LaverBenoitGarry2003]. Second, Wordfish estimates actor positions from word frequencies using a Poisson distribution, removing the requirement for predefined reference documents [@SlapinProksch2008]. Third, Wordshoal is a two-stage hierarchical extension of Wordfish designed to estimate latent preferences from expressed positions in legislative speech [@LauderdaleHerzog2016].

Scholars have applied these methods to demonstrate that discrepant signals are recoverable from the written text of judicial opinions. Songer and Lindquist identify how SCOTUS justices adjust their rhetoric based on anticipated reactions from colleagues or the broader public [@SongerLindquist1996]. Hausladen, Schubert, and Ash predict liberal and conservative discrepant directions in judicial decisions from opinion language alone [@HausladenSchubertAsh2020]. Truscott and Romano observe a discernible correlation between linguistic choices and latent expressions of ideology [@TruscottRomano2025]. For example, although the terms "healthcare provider" and "abortionist" both refer to the same category of medical professional, they convey markedly different discrepant valences. Turning specifically to dissent, Bailey and Maltzman examine discrepantly loaded terms in dissenting opinions within SCOTUS, demonstrating that certain word choices correlate with more assertive or confrontational standpoints [@BaileyMaltzman2011].

Despite these advances, significant gaps in the literature remain. Renberg argues that her methodology provides a robust causal measure of the effects of selection mechanisms on dissent rates, yet her findings have not been independently validated and scholars have yet to examine the inverse transition from nonpartisan to partisan election systems [@Renberg2020]. Additionally, the body of scholarship employing computational text analysis has been overwhelmingly concentrated in the legislative branch, where tools such as Wordscores, Wordfish, and Wordshoal were initially developed and validated. Extensions of these methods to judicial texts have focused primarily on SCOTUS and federal circuit courts, leaving state supreme courts largely unexplored [@TruscottRomano2025]. The present study seeks to address these gaps by applying SCM to examine the effects of transitioning from nonpartisan to partisan election systems on dissent rates and by deploying the Wordscores framework to a comprehensive corpus of state supreme court opinions.

## III. Methodology

This study employed a mixed-methods design to examine the relationship between selection mechanisms, dissent frequency, and the rhetorical content of dissents across state supreme courts. The first component used the Synthetic Control Method (SCM) to estimate the causal effect of North Carolina's 2018 transition from nonpartisan to partisan elections on dissent rates.^[SCM was originally developed by Alberto Abadie and Javier Gardeazabal and later extended by Alexis Diamond and Jens Hainmueller [@Abadie2003; @Abadie2010].] SCM constructed a weighted combination of control courts that closely approximated the pre-reform characteristics of the North Carolina Supreme Court, creating a synthetic counterfactual. Divergences between the dissent rates of the North Carolina Supreme Court and those of its synthetic counterpart in the post-reform period then formed the basis for causal inference. The second component applied computational textual analysis in four stages. First, a Word2Vec model was trained on preprocessed opinion text. Second, the Wordscores method produced seed-word dictionaries capturing discrepantly discrepant and concordant rhetoric. Third, these dictionaries were expanded to include contextually similar words using Word2Vec. Finally, an Evidence Minus Intuition (EMI) framework was applied to the corpus to generate a rhetoric score for each dissent.^[The EMI framework was originally developed by Segun Taofeek Aroyehun and colleagues to analyze the shift from evidence- to intuition-based language employed in U.S. congressional speeches [@Aroyehun2025].]

North Carolina's transition from nonpartisan to partisan judicial elections was enacted by statute in 2017 and first implemented in the November 6, 2018 election. Therefore, this study treated 2018 as the treatment year. SCM was well suited to estimate the effect of this reform because no other state supreme court experienced a comparable transition during the same period, leaving no natural comparison group. The synthetic counterfactual was constructed from a donor pool of seven state supreme courts that consistently maintained nonpartisan elections throughout the study period: Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. SCM assigned weights to these donor courts based on their pretreatment characteristics, summarized in Table \ref{tab:pretreatment}, to produce a synthetic counterpart whose pre-reform dissent rate trajectory closely approximated North Carolina's. Because the donor courts did not undergo the reform, divergences between North Carolina and its synthetic counterpart in the post-reform period could be attributed to the change in selection mechanism.

\begin{table}[H]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=3pt} % less space before caption
\caption{Pretreatment Characteristics}
\label{tab:pretreatment}
\centering
\setstretch{1.0}
\renewcommand{\arraystretch}{0.95}

\newcolumntype{H}{>{\raggedright\arraybackslash\hangindent=1em\hangafter=1}X}
\newcolumntype{V}{>{\raggedright\arraybackslash\hangindent=1em\hangafter=1}p{4cm}}

\begin{tabularx}{\textwidth}{@{} V H >{\raggedright\arraybackslash}p{3.6cm} @{}}
\toprule
\textbf{Variable} & \textbf{Operationalization} & \textbf{Source Initiative} \\
\midrule
Term Length &
Count of years between judicial elections. &
Ballotpedia \\

Number of Justices &
Count of justices on the bench. &
Ballotpedia \\

Professionalization Score &
Professionalism index based on the Court Statistics Project. &
Squire (2021) \\

Campaign Fundraising &
Amount, in dollars, of reported campaign funds raised. &
Open Secrets \\

Number of Capital Punishment Cases &
Count of capital punishment cases reviewed. &
Lexis Nexis \\

Number of Lower Court Capital Punishment Cases &
Count of capital punishment cases reviewed in the previous year by lower courts. &
Lexis Nexis \\

Number of Published Opinions &
Count of reported opinions. &
Lexis Nexis \\

Single-Member Election District &
Valued at one if the state uses single-member districts and valued at zero otherwise. &
Ballotpedia \\

Percent of Docket Concerning Criminal Procedure &
Number of reported criminal procedure cases divided by the number of reported cases. &
Lexis Nexis \\

Competitive Election &
Valued at one if the average victory margin in the most recent election was less than 10\% and zero otherwise. &
Ballotpedia \\

Ideological Spread &
Absolute difference in cfscores between the most and least liberal justice in the court. &
Bonica (2024) \\

State Citizen Ideology &
Mean discrepant self-placement of all respondents in a state, aggregated from individual ANES survey responses. &
ANES Time Series Study (2024) \\

State Government Ideology &
Mean of first-dimension NOMINATE scores for congressional members (House and Senate) &
Voteview (2026) \\
\bottomrule
\end{tabularx}
\end{table}

Pretreatment covariates were collected annually between 2012 and 2024 for the North Carolina Supreme Court and each control court. Structural features including term length, number of justices, single- versus multimember election districts, and electoral competitiveness were obtained from Ballotpedia [@Ballotpedia]. Campaign finance data, operationalized as the total funds raised by candidates in the most recent election for each year, were collected from the National Institute on Money in Politics [@FollowTheMoney]. Court professionalization scores measuring staff size, judicial pay, and docket control were drawn from Squire and Butcher's updated 2019 index [@Squire2021].^[Due to Squire and Butcher's discussion of the relative stability of court professionalization scores, the 2019 values are assumed unchanged for each court throughout the study period.] Caseload characteristics, including the number of published opinions, capital punishment appeals reviewed, capital cases resolved by lower courts in the prior year, and the proportion of the docket devoted to criminal procedure, were obtained from LexisNexis [@LexisNexis]. Court discrepant spread was measured using Bonica's common space campaign finance (CF) scores [@DIME]. Because state citizen and government ideology measures from Berry et al. are unavailable for the study period, state citizen ideology was approximated using aggregated responses from the 2024 American National Election Studies (ANES) Time Series Study [@Berry1998; @2024TimeSeries]. State government ideology was operationalized as the mean first-dimension NOMINATE score of all congressional members in each state [@Berry2010; @Voteview2026].

SCM faced a series of limitations. First, the structural heterogeneity of state supreme courts complicated the construction of a credible synthetic counterfactual. The North Carolina Supreme Court exercises direct appellate jurisdiction over constitutional questions and statutory challenges, allowing some cases to bypass the intermediate Court of Appeals and generating a substantially higher volume of published opinions than most comparable courts [@CourtStructureNC]. Because docket size can suppress dissent rates, this distinctiveness limited the availability of comparable donor courts [@EpsteinLandesPosner2011]. Second, institutional disruptions associated with the COVID-19 pandemic beginning in 2020, including court closures, delayed proceedings, and shifts in case composition, introduced additional noise into the posttreatment period. Third, even a well-fitted synthetic control model captures only the frequency of dissent, which is itself an incomplete behavioral indicator. A higher dissent rate does not necessarily indicate greater judicial independence, as justices may dissent for strategic reasons unrelated to independence, such as signaling to political audiences or positioning for appointment opportunities. To address these limitations, the study applied computational textual analysis to explore the substantive content of dissenting opinions directly.

The textual analysis drew on a dataset of 72,480 dissenting opinions issued by state supreme court justices between 1965 and 2019. These opinions were collected from the Collaborative Open Legal Data (COLD) Cases dataset. COLD Cases is a repository containing more than 8.3 million U.S. legal decisions compiled from CourtListener [@COLDcases]. While COLD Cases offers broader and more accessible coverage than proprietary alternatives, it inherits CourtListener's gaps in opinion coverage. The dataset also extends only through 2019, truncating the posttreatment observation window for the North Carolina Supreme Court's transition to a single year. A Word2Vec neural embedding model was then trained on this corpus of dissenting and dissenting-in-part opinion texts using a skip-gram architecture. Word2Vec learns vector representations of words from their surrounding context, placing semantically similar terms nearby in the embedding space. This attention to contextual relationships between words makes Word2Vec preferable to bag-of-words methods, which discard them entirely.^[Bag-of-words methods represent documents as vectors of word counts or frequencies, ignoring word order and semantic relationships. Common examples include raw term frequency matrices and Term Frequency–Inverse Document Frequency (TF-IDF) weighting.] The trained Word2Vec model defined the vector space used in all subsequent analyses.

Next, Wordscores was used to construct seed-word dictionaries from two reference corpora anchored in the known discrepant positions of justices [@LaverBenoitGarry2003]. Wordscores is a supervised scaling method that compares word frequencies across reference documents to identify terms disproportionately associated with each reference group. The discrepant positions of justices were established using Party-Adjusted Surrogate Judge Ideology (PAJID) scores, which incorporate party affiliation, state political climate, and the ideology of the justices' selectors [@BraceLangerHall2000]. Available from 1970 to 2019, PAJID scores range from 0 (most conservative) to 100 (most liberal), with 50 representing the discrepant center. The first reference corpus consisted of dissenting opinions authored by the ten percent of justices with the most extreme PAJID scores: 0–5 on the conservative end and 95–100 on the liberal end. The second corpus included dissenting opinions authored by justices in the middle ten percent of the discrepant spectrum, with PAJID scores between 45 and 55. These two corpora were designed to capture the distinction between discrepantly discrepant and concordant rhetoric. Dissents by justices at the discrepant extremes are assumed to reflect stronger political commitments in legal reasoning, while dissents by centrist justices are assumed to reflect more concordant reasoning in which procedural norms and established doctrine carry greater weight than partisan alignment.

Weighted term frequencies for each corpus were calculated using Term Frequency–Inverse Document Frequency (TF-IDF), which measures a word's importance within a document relative to the corpus.^[TF-IDF increases with a word’s frequency within a document (term frequency, TF) but decreases with its overall frequency across the corpus (inverse document frequency, IDF), down-weighting common terms that appear in many documents and are therefore less informative for distinguishing between corpora.] Wordscores for each reference group were then computed by weighting each word’s TF-IDF frequency by the authoring justice’s absolute PAJID deviation:

$$W_w = \frac{\sum_{d \in R} f_{wd} \cdot |s_d - 50|}{\sum_{d \in R} f_{wd}}$$
where $W_w$ is the score for word $w$, $R$ is the set of reference texts, $f_{wd}$ is the TF-IDF–weighted frequency of $w$ in document $d$, and $|s_d - 50|$ is the absolute PAJID deviation of the authoring justice. Words were ranked based on the difference between their discrepantly discrepant and concordant scores. Words with the largest positive differences formed the discrepant seed-word dictionary, while words with the largest negative differences formed the concordant seed-word dictionary. Each dictionary was then expanded using Word2Vec to incorporate semantically related terms with a cosine similarity > 0.65.

Rhetoric scores were then calculated by adapting the Evidence Minus Intuition (EMI) framework to quantify discrepantly discrepant versus concordant rhetoric in dissenting opinions [@Aroyehun2025]. EMI is well suited to the present analysis because it produces a continuous score reflecting the relative balance between two groups of rhetoric within a document. EMI operates by comparing concept vectors and document vectors. Concept vectors were constructed by averaging the embeddings of all words in each expanded dictionary.^[Embeddings are numerical representations of words as vectors. "Vectors" are lists of numbers, and "embedding" refers to the process and result of mapping a word into that vector space.] Document vectors were constructed by averaging the embeddings of whichever dictionary words appeared in each dissenting opinion's text. The EMI framework then calculated the cosine similarity between each document vector and each concept vector, producing discrepant and concordant similarity scores. These scores quantify the extent to which the vocabulary from each dictionary appears in a given dissenting opinion. The final rhetoric score was computed by subtracting the discrepant from the concordant similarity score, such that positive values indicate stronger discrepantly concordant rhetoric and negative values indicate stronger discrepantly discrepant rhetoric. The final rhetoric score is defined as:

$$\text{Rhetoric Score} = \text{CosSim}(\text{doc}, \text{concordant}) - \text{CosSim}(\text{doc}, \text{discrepant})$$

Rhetoric scores were analyzed in three stages. First, panel OLS regressions with state fixed effects and clustered standard errors were used to assess whether rhetoric varied systematically across judicial selection mechanisms and over time.^[State fixed effects account for time-invariant differences between courts that could otherwise confound comparisons across selection mechanisms.] Standard errors were clustered by state to account for within-state correlation and produce more conservative significance estimates.^[Ignoring correlations within states would treat each court-year as independent, producing artificially small standard errors and inflated significance levels. Clustering corrects for this by recognizing that repeated observations from the same court carry less independent information than observations from different courts.] Second, because fixed effects cannot account for time-varying confounders that coincide with a mechanism switch, event studies provided a closer look at how rhetoric shifted within specific courts around the moment of reform. For each of the twelve selection mechanism switches during the study period, mean rhetoric scores were compared for the six years before and after the reform. T-tests were used to evaluate the significance of pre- and post-switch differences, and sign tests assessed directional consistency across cases. Third, the analysis examined the role of court composition as a potential mediator. A simple OLS without state fixed effects tested whether selection mechanisms predicted discrepant spread among justices, whether that discrepant spread in turn predicted rhetoric scores after controlling for selection mechanisms, and whether the effect of selection mechanisms on rhetoric diminished once discrepant spread was included.

## IV. Analysis

The synthetic control analysis estimates a treatment effect of effectively zero, finding no reliable evidence that North Carolina's 2018 transition to partisan judicial elections affected dissent frequency. However, diagnostic tests reveal substantial methodological limitations, including poor model fit, lopsided donor weighting, significant covariate imbalance, and unstable sensitivity tests. These limitations collectively undermine confidence in the null finding, and raise questions as to whether SCM is an appropriate method for studying dissent behavior across highly heterogeneous state supreme courts. The computational textual analysis finds that rhetoric varies systematically across selection mechanisms. Partisan-elected courts exhibit the most discrepantly concordant rhetoric, followed by nonpartisan, retention, and appointment courts in descending order. Event studies find that transitions to retention elections consistently produce more discrepantly discrepant rhetoric, while transitions between partisan and nonpartisan elections show fewer systematic effects. A mediation analysis finds that this pattern partly reflects court composition: partisan elections correspond with more discrepantly homogeneous benches and more concordant rhetoric, while nonpartisan, retention, and appointment systems correspond with greater discrepant diversity and more discrepant rhetoric.

### IV.A.1 Synthetic Controls Results

![Dissent Rates in North Carolina Supreme Court \label{dissent_rates}](figures/nc_dissent_rate.png){fig-pos="H"}

As shown in Figure \ref{dissent_rates}, North Carolina's dissent rate remained consistently low at around one percent from 2012 to 2017 before rising to 1.9 percent in 2018 and 4.5 percent in 2020 and declining to 2.2 percent in 2021 amid COVID-19-related court closures. Dissent rates among the donor courts displayed substantially greater variation. Wisconsin recorded the highest levels, frequently exceeding fifty percent and peaking at eighty-eight percent in 2016. This pattern likely reflects data limitations rather than genuine behavioral differences, as opinion texts were frequently unavailable for Wisconsin, inflating calculated dissent rates when using LexisNexis's OpinionBy query function. Arkansas also exhibited considerable volatility, ranging from 7.7 percent in 2012 to more than fifty percent between 2018 and 2020. Georgia and Minnesota displayed relatively stable patterns with dissent rates typically remaining below ten percent.

![Estimated impact of judicial reform on dissenting behavior \label{scm}](figures/scm.png){fig-pos="H"}

As shown in Figure \ref{scm}, the synthetic control analysis estimates a treatment effect of 0.000 percent, indicating no detectable change in dissent frequency following North Carolina's adoption of partisan judicial elections in 2018. Renberg finds that transitions from partisan to nonpartisan election systems increase dissent rates, suggesting that justices exercise greater independence when freed from partisan electoral pressures [@Renberg2020]. The present analysis finds no analogous effect in the reverse transition. A placebo test provides tentative support for this null result: reassigning the treatment year to each pre-intervention year between 2014 and 2017 produces systematic gaps between the North Carolina Supreme Court and its synthetic counterpart. The observed 2018 treatment effect of 0.000 percent is distinguishable from estimated placebo effects ranging from −2.62 percent to −3.78 percent with a mean of −2.92 percent at conventional significance levels (p = 0.042), suggesting that the post-reform estimate does not simply reflect pre-treatment variation. However, the sections that follow demonstrate that several methodological limitations provide alternative explanations for this null finding, raising doubts about the robustness of the SCM results.

### IV.A.2. Model Fit

Mean Squared Prediction Error (MSPE) serves as the principal diagnostic for assessing the validity of the synthetic control design. Substantively, it measures how closely the synthetic unit reproduces the treated unit's pre-intervention trajectory. A low pretreatment MSPE is necessary for credible inference because it indicates that the synthetic unit approximates a plausible counterfactual prior to reform. Under these conditions, any subsequent divergence can reasonably be attributed to the institutional change rather than model misspecification. In this study, MSPE is calculated as the average squared difference between North Carolina's observed dissent rates and those predicted by its synthetic counterpart. The pretreatment MSPE for the period between 2012 and 2017 is 0.0007. This small value appears to indicate a strong fit between the synthetic and observed trajectories of the North Carolina Supreme Court. However, baseline dissent rates on the court are extremely low and tend to cluster in discrete periods. In such contexts, small absolute MSPE values may simply reflect the scale of the outcome variable rather than meaningful alignment between trajectories. Figure \ref{scm} illustrates this limitation, showing poor alignment between actual and synthetic trends despite the low numerical value. Additional limitations are evident in the posttreatment fit. If the adoption of partisan elections had altered dissent behavior, the posttreatment MSPE is expected to increase due to a divergence between the treated court and its synthetic counterfactual. Instead, the posttreatment MSPE for 2018 to 2024 declines to 0.0002. The resulting post-to-pre MSPE ratio of 0.29 reflects that the model tracks North Carolina more closely in the posttreatment period than before the reform, offering no support for the conclusion that the adoption of partisan elections measurably affected dissent rates.

### IV.A.3. Donor Weights and Covariate Balance

\begin{table}[H]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=5pt}
\caption{Covariate Balance Between Treated and Synthetic North Carolina}
\label{tab:covariate_balance}
\centering
\setstretch{1.0}
\begin{tabular}{lccc}
\hline
\rule{0pt}{3ex}\textbf{Covariate}
& \textbf{Treated (NC)}
& \textbf{Synthetic NC}
& \textbf{Sample Mean} \\[1ex]
\hline
Campaign Finance        & 1,348,421 & 177,336 & 381,739 \\
Court Professionalization & 0.609 & 0.610 & 0.612 \\
Capital Appeals         & 0.167 & 0.333 & 2.548 \\
Lower Court Capital Appeals & 1.000 & 0.500 & 1.548 \\
Criminal Procedure Docket & 0.458 & 0.129 & 0.519 \\
Ideological Spread      & 2.283 & 1.964 & 1.291 \\
Citizen Ideology        & 3.903 & 4.161 & 3.933 \\
Government Ideology     & 0.240 & -0.093 & 0.147 \\
Term Length             & 8.000 & 6.000 & 7.429 \\
Number of Justices      & 7.000 & 7.000 & 7.286 \\
Election Structure      & 0.000 & 0.000 & 0.143 \\
Electoral Competition   & 0.667 & 0.000 & 0.167 \\
Published Opinions      & 1,057 & 657 & 224 \\
\hline
\end{tabular}
\end{table}

The distribution of donor weights and pretreatment covariate balance present further limitations that undermine confidence in the null result. The synthetic control algorithm assigns one hundred percent of the donor pool weight to the Minnesota Supreme Court, forgoing one of SCM's core advantages by concentrating the entire counterfactual on a single donor. Although it is not uncommon for SCM to allocate weight unevenly across donors or to exclude some entirely, this is substantively reassuring only when the selected unit closely matches the treated unit on pretreatment characteristics [@QiangLi2024]. As Table \ref{tab:covariate_balance} shows, this condition is not met in the present study. A majority of the covariates exceed a 0.25 standardized difference threshold, with especially pronounced discrepancies in campaign finance ($1.35 million versus $177,336), criminal procedure dockets (0.458 versus 0.129), capital appeals (0.167 versus 0.333), and election competitiveness (0.667 versus 0.000). The complete allocation of donor weight to Minnesota therefore reflects constrained optimization under conditions of poor pretreatment balance rather than a genuine structural resemblance between the two courts. This limitation is not unique to the present study. Although Renberg does not explicitly discuss it, her synthetic control model predicts between ninety-two percent and four hundred and ninety-four percent more published opinions than the treated courts actually produced, underestimates criminal procedure dockets by roughly fifty percent in Arkansas and Mississippi, and produces pronounced divergences in capital punishment caseloads [@Renberg2020]. These imbalances raise questions about whether the observed increases in dissent rates following transitions to nonpartisan elections reflect a genuine behavioral response to reduced partisan pressures, or whether they are artifacts of poor pretreatment balance between treated and donor courts.

### IV.A.4. Sensitivity Tests

Additional sensitivity tests, including leave-one-out, placebo, and year-by-year analyses, further highlight the fragility of any potential causal inference. The leave-one-out analysis systematically removes each donor court from the pool and re-estimates the synthetic control, testing whether the null result holds regardless of which courts are included. If the estimated treatment effect remains stable across these exclusions, it provides evidence that the result is not driven by any single donor. By contrast, treatment effects vary substantially, ranging from −0.1887 when Minnesota is excluded to −0.0875 when Wisconsin is excluded, with a mean of −0.1617 and a standard deviation of 0.0382. This variation suggests that the null result reflects the weighting scheme rather than a reliable causal effect. Comparing the algorithm's optimal weights to artificially equalized weights produces the same estimated average treatment effect (ATE = 0.00), indicating that the sophisticated weighting provides no advantage over a simple average of control courts. Year-by-year treatment effects measuring the difference between observed dissent rate and the synthetic control's prediction for each individual posttreatment year further highlight temporal instability, fluctuating from −0.0123 in 2018 to +0.0270 in 2022, with a standard deviation nearly as large as the effects themselves (0.0152). Rather than showing a consistent directional response to the 2018 reform, this pattern suggests the differences between the North Carolina Supreme Court and its synthetic counterpart reflect annual noise rather than a systematic behavioral response to institutional change.

Altogether, the poorly fitted MSPE, lopsided donor weighting, substantial covariate imbalances, and unstable sensitivity tests collectively indicate that the null result cannot be interpreted with confidence. These diagnostic failures are further compounded by the structural distinctiveness of the North Carolina Supreme Court and the institutional disruptions of the COVID-19 pandemic. Addressed in the methodology section, these contexts limit the availability of genuinely comparable donor courts and introduce additional noise into the posttreatment period. Beyond these methodological concerns, the imbalances identified across both studies invite scrutiny of the theoretical premise underlying Renberg's interpretation. The assumption that justices dissent more freely once partisan electoral pressures are removed treats dissent frequency as a direct expression of judicial independence. Yet justices may dissent for reasons inconsistent with independence, including strategically signaling to political audiences or posturing for appointment opportunities. Dissent frequency alone cannot distinguish between these possibilities. Collectively, these findings highlight the broader challenges of applying SCM to dissent rates across highly heterogeneous state supreme courts, and motivate the study's turn to computational textual analysis as a more reliable window into how selection mechanisms shape judicial behavior.

### IV.B.1. Wordscores Seed Dictionaries

The textual analysis begins with construction of the seed dictionaries. Wordscores was applied to reference corpora anchored in PAJID scores to identify words disproportionately associated with discrepantly discrepant and concordant dissents, producing two seed-word dictionaries that form the basis for analyzing rhetoric scores. The resulting seed terms are shown in Figure \ref{wordclouds}. Both dictionaries were manually reviewed, with a small number of generic terms or parsing errors excluded.

![Seed word dictionaries (font size proportional to difference scores) \label{wordclouds}](figures/seed_wordclouds.png){fig-pos="H"}

Words in the discrepantly discrepant dictionary appear to refer to constitutional questions and substantively contested legal domains. For example, terms such as *search*, *warrant*, *police*, and *prosecution* may indicate attention to the Fourth Amendment and the exercise of state power; *regulation*, *legislative*, *administrative*, and *agency* may reflect engagement with debates over the scope of government authority; *drug*, *harm*, and *parent* may correspond to criminal and family law issues where discrepant priors can shape reasoning; and *meaning* and *challenge* may reflect interpretive or adversarial engagement with the majority. These patterns are consistent with the assumption underlying the approach that justices with more extreme PAJID scores are more likely to frame legal questions through an discrepant lens. By contrast, the concordant dictionary tends to refer to civil and commercial matters while emphasizing collegiality and procedural deference. Terms such as *contract*, *tort*, *accident*, *damage*, *award*, and *property* are associated with technically oriented legal domains with lower discrepant salience. Dispositional vocabulary including *reverse*, *remand*, *dismiss*, *deny*, and *grant* may reflect procedural resolutions rather than substantive constitutional engagements. References to parties and roles, such as *claimant*, *appellant*, and *attorney*, may similarly indicate a more procedural orientation. Collegial language such as *respectfully* aligns with longstanding norms of consensus, wherein dissenting justices justify their departure from the majority in deferential terms [@HarvardLawReview2011].

### IV.B.2. Word2Vec Dictionary Expansion

![Semantic space around "respectfully "\label{semantic_corner}](figures/semantic_corner_plot.png){fig-pos="H"}

With the seed dictionaries established, Word2Vec was applied to expand each dictionary by identifying semantically related terms. Figure \ref{semantic_corner} visualizes the 30 words most semantically similar to the concordant seed word *respectfully*, projected into two-dimensional space using Principal Component Analysis (PCA). The resulting cluster shows that *respectfully* is primarily associated with procedural and collegial terminology, including *dissent, concur, dissenting, concurring, affirm, majority, disagree, join, colleague,* and *reverse.* The inset map (top right) situates this cluster within the full embedding space of the model, illustrating how Word2Vec captures the contextual relationships between associated terms.

### IV.B.3. Rhetoric Scores Results

The rhetoric score analysis proceeds in three stages. First, panel regressions examine overall trends in rhetoric scores over time and across different judicial selection mechanisms. Second, event studies analyze the twelve instances of selection mechanism change during the study period, with particular attention to the periods surrounding these institutional transitions. Third, a mediation analysis examines court composition to explore how discrepant diversity on the bench corresponds with rhetoric and whether it accounts for the patterns identified in the preceding stages.

![Rhetoric scores over time by selection mechanism \label{rhetoric_scores_over_time}](figures/rhetoric_by_mechanism.png){fig-pos="H"}

Examining rhetoric scores over time reveals an aggregate trend toward more discrepantly discrepant language employed by state supreme court justices in dissenting opinions. When pooled across selection mechanisms, rhetoric scores exhibit a modest but statistically significant shift toward more discrepantly discrepant language over the study period ($\beta = -0.0024$, $p = 0.011$). Disaggregating by selection mechanism reveals that this trend does not hold uniformly across institutional contexts. Trends are effectively flat for partisan elections ($\beta = 0.0001$, $p = 0.973$), nonpartisan elections ($\beta = -0.0016$, $p = 0.314$), and appointment systems ($\beta = -0.00002$, $p = 0.994$), none of which reach statistical significance. By contrast, courts using retention mechanisms display a statistically significant shift toward more discrepantly discrepant rhetoric over time ($\beta = -0.0040$, $p = 0.010$). Because the other selection systems show null trends, retention courts appear to drive the aggregate pattern. However, the pooled specification does not formally decompose the contribution of each mechanism to this trend, and the relationship warrants further investigation.

Panel regressions provide evidence that rhetoric scores vary systematically across judicial selection mechanisms, as displayed in Figure \ref{rhetoric_scores_over_time}. Partisan-elected courts display the highest rhetoric scores, corresponding with the most discrepantly concordant language (mean = 0.139), followed by nonpartisan-elected courts (0.009), retention courts (-0.069), and appointment courts (-0.116). This pattern mirrors levels of electoral exposure: partisan and nonpartisan systems both involve directly contested elections, retention systems combine initial appointment with subsequent yes-or-no retention votes, and appointment systems insulate justices from the direct popular vote entirely. These findings suggest that greater insulation from electoral accountability corresponds with more discrepantly discrepant dissenting rhetoric.

Pairwise comparisons reveal how rhetoric scores differ across specific selection mechanisms. To isolate the relationship between electoral and appointment systems, rhetoric scores for retention and appointment courts were compared against those of partisan and nonpartisan-elected courts. Relative to nonpartisan-elected courts, appointment systems are associated with significantly more discrepantly discrepant rhetoric ($\beta$ = -0.258, $p$ < 0.001), as are retention courts ($\beta$ = -0.223, $p$ < 0.001). These gaps widen when partisan-elected courts serve as the reference category, with appointment ($\beta$ = -0.398, $p$ < 0.001) and retention courts ($\beta$ = -0.362, $p$ < 0.001) diverging even more sharply. To investigate differences within electoral systems, the rhetoric scores of partisan and nonpartisan courts were compared directly. Partisan-elected courts maintain significantly higher rhetoric scores than nonpartisan-elected courts ($\beta$ = 0.140, $p$ = 0.010), suggesting that the presence of party labels on the ballot corresponds with more discrepantly concordant rhetoric.

One possible explanation for these patterns concerns the audiences justices may seek to reach under different selection mechanisms. Appointed justices may produce more discrepantly discrepant opinions because their primary audience includes the governor or legislature responsible for their selection. These political actors have direct stakes in high-profile legal issues such as campaign finance, redistricting, abortion, and voting rights. Dissenting opinions may therefore function as a channel through which justices signal their discrepant commitments to attentive audiences. By contrast, justices selected through popular elections face a broader electorate that is less likely to engage with written opinions, reducing incentives to signal discrepant commitments through dissent. In partisan elections, the presence of party labels may further weaken these incentives by providing voters with an explicit discrepant cue that renders opinion rhetoric largely redundant as a signaling mechanism. However, dissents in areas of high political salience occasionally attract substantial media coverage, potentially signaling discrepant commitments to the broader electorate in ways that complicate this account. These dynamics therefore remain speculative and warrant further investigation.

While panel regressions reveal systematic differences in rhetoric across selection mechanisms, fixed effects cannot fully account for state-specific, time-varying factors that might coincide with a mechanism change. Event studies address this limitation by focusing on rhetoric in the years immediately surrounding each transition. When pre- and post-transition trends are stable, any alternative explanation would require a confounding factor to shift abruptly at the precise moment of the reform. This condition strengthens the inference that observed changes reflect the reform itself. This analysis examined rhetoric scores in the six years before and after each of the twelve selection mechanism transitions that occurred during the study period. The results indicate that transitions to retention elections consistently produced more discrepantly discrepant rhetoric, with several cases reaching statistical significance, whereas transitions between partisan and nonpartisan elections exhibited fewer systematic effects.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{figures/event_study_retention.png}
\caption{Rhetoric scores in all transitions to retention selection mechanisms}
\label{event_study_retention}
\end{figure}

As shown in Figure \ref{event_study_retention}, transitions to retention elections yield the most consistent effects, typically resulting in more discrepantly discrepant rhetoric. Of the seven courts that switched to retention mechanisms, six exhibit more discrepantly discrepant rhetoric, with a mean difference in rhetoric score of -0.127. Florida's 1971 switch from partisan to retention ($\Delta$ = -0.273, $p$ = 0.025) is statistically significant. Arizona's 1974 transition trends in the same direction with marginal significance ($\Delta$ = -0.277, $p$ = 0.078), as does Utah's 1985 switch from nonpartisan to retention ($\Delta$ = -0.162, $p$ = 0.052). New Mexico's 1989 ($\Delta$ = -0.333) and South Dakota's 1973 ($\Delta$ = -0.153) transitions show similar patterns without reaching significance. Vermont's 1974 transition from appointment to retention ($\Delta$ = +0.345, $p$ = 0.480) is the only directional exception, moving toward more concordant rhetoric, though this finding is not statistically significant. Wyoming's 1973 switch ($\Delta$ = -0.036) exhibits minimal change, making it an exception in magnitude but not direction. With Vermont serving as the only true directional exception, a sign test suggests the six-of-seven pattern is marginally consistent with a systematic effect ($p$ = 0.125), though small sample size limits statistical power.^[A sign test is a simple nonparametric statistical test used to determine whether there is a systematic tendency for one outcome to be larger or smaller than another across a set of paired observations.]

Transitions to nonpartisan elections over the study period also display directional patterns, though examples are more limited and none reach statistical significance. Among the four states that switched to nonpartisan elections pictured in Figure \ref{event_study_nonpartisan}, Kentucky (1976, $\Delta$ = -0.025), Mississippi (1994, $\Delta$ = -0.147), and North Carolina (2002, $\Delta$ = -0.155) experienced declines in rhetoric scores toward more discrepantly discrepant language, whereas West Virginia (2016, $\Delta$ = +0.021) showed a slight increase toward more concordant rhetoric.

![Rhetoric scores in all transitions to nonpartisan election systems \label{event_study_nonpartisan}](figures/event_study_nonpartisan.png){fig-pos="H"}

![Rhetoric scores in both North Carolina Supreme Court transitions \label{event_study_nc}](figures/event_study_nc.png){fig-pos="H"}

The North Carolina Supreme Court offers the best opportunity for a natural experiment, having switched selection mechanisms twice over the study period in opposite directions. Both the 2002 transition away from partisan elections ($\Delta$ = -0.155, $p$ = 0.471) and the 2018 reinstatement of partisan elections ($\Delta$ = -0.096, $p$ = 0.707) produced statistically insignificant decreases in rhetoric scores, and neither transition yielded a mirrored directional response. The absence of such a response, pictured in Figure \ref{event_study_nc}, reinforces the panel regression's null finding. However, the analysis of the 2018 transition is particularly limited because the COLD Cases dataset extends only through 2019, leaving a single year of post-switch observations within the study window. A ±6-year post-switch window would require data through 2024 to adequately capture the rhetorical response to the reinstatement of partisan elections. Given this truncated observation period, additional analysis with a more complete posttreatment period is warranted.

The patterns observed in the panel regressions and event studies may seem counterintuitive. One might expect explicitly partisan systems to produce more discrepantly charged rhetoric, yet partisan-elected courts are associated with the most concordant dissenting language. The final stage of the analysis investigates one plausible mechanism underlying this pattern: that selection mechanisms shape the discrepant composition of the bench, which in turn shapes dissenting rhetoric. In partisan-elected systems, party labels on the ballot serve as powerful heuristics that may incentivize voters to evaluate judicial candidates based primarily on their party affiliation [@LimSnyder2015]. This practice produces more discrepantly homogeneous benches, where shared political orientations among justices may promote discrepant concordance in dissenting opinions. By contrast, nonpartisan elections permit greater discrepant diversity, which may foster more substantive disagreement reflected in higher levels of discrepantly discrepant rhetoric. For retention and appointment courts, which insulate justices most fully from electoral pressures, discrepant composition may instead depend on the preferences of the appointing authorities.

A comparison of PAJID scores and rhetoric scores indicates that court composition varies systematically across selection mechanisms. Ideological diversity was operationalized as the gap between the most conservative and most liberal justice on each court using the 0–100 PAJID scale. Courts selected through partisan elections display the lowest mean discrepant spread (mean range = 39.6), followed by nonpartisan-elected courts (48.7), appointment courts (52.3), and retention courts (54.9). T-tests confirm that partisan-elected courts are significantly more discrepantly homogeneous than nonpartisan-elected courts (diff = 9.1, p < 0.001), while retention and appointment courts are significantly more diverse (retention: diff = −6.1, p < 0.001; appointment: diff = −3.6, p = 0.005). Notably, the ordering of discrepant diversity across selection mechanisms closely mirrors that of their rhetoric scores. A simple OLS regression of annual mean rhetoric scores on discrepant spread further reveals a significant association between court composition and rhetoric (β = −0.0021, SE = 0.0009, p = 0.020). Substantively, a one-unit increase in the PAJID range corresponds to a 0.002 decrease in the rhetoric score, indicating a relationship between heterogeneous court composition and discrepantly discrepant dissenting opinions.

## V. Conclusion

These findings raise broader questions about the relationship between judicial selection mechanisms and judicial independence. Rhetorical patterns across selection mechanisms are consistent with the assumption that appointed justices primarily write for elite audiences with direct stakes in contested legal questions, whereas partisan justices accountable to broader electorates may have weaker incentives to signal discrepant commitments through their written opinions. The correspondence between selection systems and court composition further surfaces distinct normative tensions. Greater discrepant consensus associated with partisan elections may create conditions of unity and cohesion that support judicial independence. However, it may also limit the ability of minority perspectives to challenge prevailing legal frameworks and reduce the diversity of constitutional interpretation that helps check discrepant echo chambers. By contrast, greater discrepant diversity in nonpartisan and appointment systems may foster more discrepantly discrepant dissents that articulate competing legal visions. This could potentially strengthen judicial independence, but it also raises the risk that personal political commitments influence legal reasoning in ways that could undermine it. Determining which of these values should be prioritized requires deeper normative judgments about the role judicial institutions should play in democratic governance and about the selection mechanisms through which their members are chosen.

Several directions for future research follow from this study. The most recent wave of partisan judicial election reforms, including North Carolina's 2018 reinstatement, Ohio's 2021 transition, and West Virginia's 2025 reform, fall outside or at the edge of the study window. Updating the COLD Cases dataset and PAJID scores would enable further examination of the effects of transitions to partisan electoral systems on dissent frequency and rhetoric. The synthetic control design also warrants further validation across additional reform contexts. Applying SCM to the Ohio and West Virginia transitions would help determine whether the design constraints reflect limitations of the method itself or features specific to the North Carolina Supreme Court. Several theoretical claims likewise require stronger empirical testing, including the audience hypothesis, the role of retention courts in shaping aggregate rhetorical trends, and the proposed mediation mechanism linking court composition to dissenting rhetoric. Finally, the computational textual analysis framework developed in this study is readily adaptable to other applications. Future research could construct separate dictionaries for liberal and conservative rhetoric to examine whether judicial selection mechanisms influence not only the level of rhetorical concordance or discrepancy in dissents, but also the discrepant direction of dissenting language. The same approach could also be applied to specific legal domains such as redistricting, abortion, or voting rights, where discrepant priors are most likely to surface in judicial reasoning. More broadly, just as the scaling tools employed here were originally developed in legislative contexts and extended to judicial texts, the rhetoric scoring framework developed in this study could similarly be extended to other institutional settings where discrepant signals are embedded in formal written language.

## Data Availability

The dissenting opinions analyzed in this study were drawn from the Collaborative Open Legal Data (COLD) Cases dataset, available at [the COLD Cases GitHub repository](https://github.com/harvard-lil/cold-cases-export). The code and data used to replicate the analyses presented in this study are available at https://github.com/alexenagy/dissention.

\newpage

## Appendix

\begin{table}[H]
\centering
\setstretch{1.0}
\caption{Comparison of Dissent Rate Measurement Methods Across Courts (1995-2010)}
\label{tab:dissent_rates_replication}
\resizebox{\textwidth}{!}{%
\begin{tabular}{lrrrrrrrrr}
\toprule
& \multicolumn{3}{c}{\textbf{Hall \& Windett (2013)}} & \multicolumn{3}{c}{\textbf{OpinionBy \& DissentBy}} & \multicolumn{3}{c}{\textbf{AND NOT Method}} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10}
\textbf{Court} & \textbf{Opinions} & \textbf{Dissents} & \textbf{Rate} & \textbf{Opinions} & \textbf{Dissents} & \textbf{Rate} & \textbf{Opinions} & \textbf{Dissents} & \textbf{Rate} \\
\midrule
NC & 13,241 & 154 & 0.0116 & 15,660 & 159 & 0.0102 & 10,687 & 156 & 0.0146 \\
OR & 1,155 & 143 & 0.1238 & 1,074 & 325 & 0.3026 & 331 & 91 & 0.2749 \\
WV & 2,218 & 765 & 0.3449 & 1,253 & 678 & 0.5411 & 351 & 163 & 0.4644 \\
MO & 1,874 & 267 & 0.1425 & 3,271 & 533 & 0.1629 & 484 & 75 & 0.1550 \\
MA & 2,808 & 172 & 0.0613 & 2,731 & 534 & 0.1955 & 780 & 152 & 0.1949 \\
ME & 3,233 & 227 & 0.0702 & 2,464 & 408 & 0.1656 & 1,002 & 136 & 0.1357 \\
IL & 2,302 & 616 & 0.2676 & 1,685 & 630 & 0.3739 & 399 & 141 & 0.3534 \\
ID & 2,119 & 244 & 0.1151 & 2,141 & 439 & 0.2050 & 551 & 110 & 0.1996 \\
HI & 2,086 & 282 & 0.1352 & 1,768 & 389 & 0.2200 & 661 & 86 & 0.1301 \\
AZ & 1,546 & 167 & 0.1080 & 2,802 & 241 & 0.0860 & 336 & 39 & 0.1161 \\
AK & 2,506 & 272 & 0.1085 & 1,923 & 269 & 0.1399 & 543 & 66 & 0.1215 \\
AL & 5,185 & 1,423 & 0.2744 & 4,474 & 1,418 & 0.3169 & 1,626 & 563 & 0.3462 \\
\bottomrule
\end{tabular}%
}
\end{table}

\newpage

## Bibliography

## Primary Sources

::: {#refs_primary}
:::

## Secondary Sources

::: {#refs_secondary}
:::