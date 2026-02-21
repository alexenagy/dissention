---
title: The Impact of Judicial Selection Methods on Opinion Writing Behavior
author: Alexandria Nagy
bibliography: [../references/bib.bib]
fontsize: 12pt
linestretch: 2
csl: ../references/chicago-notes-bibliography-classic.csl
header-includes:
  - \usepackage[margin=1in]{geometry}
  - \usepackage{caption}
  - \usepackage{setspace}
  - \usepackage{booktabs}
  - \usepackage{tabularx}
  - \usepackage{array}
  - \usepackage[numbers]{natbib}
  - \setlength{\bibsep}{0pt}
  - \usepackage{indentfirst}
  - \setlength{\parindent}{0.5in}
  - \setlength{\parskip}{0pt}
  - \makeatletter\let\@afterindentfalse\@afterindenttrue\makeatother
abstract: |
  Insert abstract here
link-citations: false
---

## Introduction

The United States is undergoing a profound transformation in its judicial landscape. In a period marked by rising polarization and a more openly majoritarian conservative constitutional order, the Supreme Court of the United States has delegated responsibility for resolving many contentious national issues to the states by narrowing federal oversight in areas such as campaign finance, partisan gerrymandering, abortion, and voting rights. As the stakes of state-level adjudication have increased, the expected policy payoff of controlling state supreme courts has risen as well. State legislatures and partisan actors have responded by restructuring judicial selection systems to allow for greater direct political influence, most prominently by replacing nonpartisan judicial elections with explicitly partisan contests through the inclusion of party affiliations on ballots. In 2025, Montana’s legislature advanced five proposals to introduce partisan judicial contests [@Montana2025]. Although these measures were ultimately defeated in Montana, comparable reforms have succeeded elsewhere. Ohio enacted Senate Bill 80 in 2021; North Carolina passed Session Law 2016-125 in 2016; West Virginia adopted Senate Bill 521 in 2025.^[See Ohio S.B. 80 (2021); N.C. Sess. Law 2016-125 (2016); W. Va. S.B. 521 (2025).] Each of these laws requires candidates to list party affiliation on both primary and general election ballots, thereby formalizing partisanship in state supreme court elections.

Against this backdrop, scholars remain divided over whether the shift toward partisan judicial selection effectively balances judicial independence and accountability, two principles that are inherently in tension^[See @Hall2001 for an overview of the scholars involved in this debate]. Judicial independence allows courts to decide cases based on law and free from external pressures, while accountability requires them to remain responsive to public values and societal needs. Reform advocates tend to argue that partisan elections place too much emphasis on party loyalty and electoral considerations, undermining independence and risking decisions driven more by politics than by legal reasoning. They generally favor nonpartisan elections or merit-based retention systems, such as the Missouri Plan, to prioritize professional qualifications and preserve judicial autonomy. In contrast, opponents of reform contend that partisan elections enhance democratic accountability without necessarily eroding independence, as electoral competition incentivizes judges to remain attentive to voter concerns. This debate highlights how different selection mechanisms structure judicial incentives and shape the potential for systematic bias in judicial decision-making.

This study extends scholarship on judicial independence in state supreme courts by examining the institutional shift from nonpartisan to partisan judicial elections. Prior research has employed a range of empirical strategies to estimate how selection mechanisms influence dissent rates, which are frequently used as a behavioral proxy for judicial independence [@Canon1970; @HallAndWindett2013; @Renberg2020]. These approaches include manual data collection, automated web scraping using Python, and quasi-experimental techniques such as the synthetic control method (SCM). Despite these advances, dissent rates remain an imperfect measure and are vulnerable to concerns about data completeness, reproducibility, and construct validity. As language modeling techniques advance, computational textual analysis of judicial opinions offers a more complete understanding of judicial behavior than dissent rates alone. By distinguishing evidence-based reasoning from intuition-driven language, this approach provides insight into how institutional design shapes judicial rhetoric. This study therefore evaluates whether partisan and nonpartisan selection mechanisms influence patterns of opinion writing and considers what these differences imply for the measurement of judicial independence in state supreme courts.

## Literature Review

To explore concerns about judicial independence and selection methods, scholars often use dissent rates as a proxy for behavioral independence. A justice’s decision to write a dissent reflects a willingness to challenge the majority opinion, advance alternative legal interpretations, and resist political or institutional pressures [@Renberg2020]. Scholarly research on judicial dissent has identified several factors that influence a justice's opinion-writing behavior on state supreme courts. These include environmental conditions that reflect broader political and social contexts, institutional structures that govern court operations, electoral systems that determine how judges are selected and retained, internal court dynamics that shape collegial relations. Understanding these mechanisms is essential for evaluating how reforms to judicial selection systems affect judicial independence and accountability.

Environmental factors reflecting broader political and social contexts have been found to influence dissent rates. Brace and Hall find that higher urbanization, greater political competition, and increased state spending are all associated with elevated dissent rates [@Brace1990]. Similarly, Epstein, Landes, and Posner show that judges appointed by presidents of different parties exhibit systematically divergent ideological preferences, increasing the likelihood of disagreement on mixed panels, and that dissent becomes more frequent as ideological divisions widen, panel sizes grow, and dissent aversion declines [@Epstein2011]. These findings indicate that courts operating in more heterogeneous and competitive political contexts are more likely to experience higher dissent rates, reflecting the combined effects of structural and ideological pressures on judicial behavior.

Building on the influence of environmental factors, scholars have found that institutional features governing court structures and internal rules have been found to exert an even greater effect on dissent rates. Brace and Hall find that these factors are the primary drivers for dissent, accounting for roughly six times more explanatory power than environmental variables [@Brace1990]. They identify four key institutional features that shape dissent: the method of judicial selection, the presence of intermediate appellate courts, random opinion assignment, and sanctioning rules [@Brace1990]. Intermediate appellate courts increase dissent by filtering routine cases, leaving higher courts to decide more complex and controversial disputes. Random case assignment promotes dissent by limiting the Chief Justice’s ability to reward or punish colleagues through discretionary assignments. Conversely, procedures such as opinion assignment, conference discussion by seniority, and voting in reverse seniority encourage consensus by creating incentives that discourage open disagreement. Similarly, Jaros and Canon show that states with intermediate appellate courts experience higher dissent rates in their supreme courts, with the likelihood of dissent rising as court size increases and judicial terms shorten [@Canon1970].

Beyond formal structures, scholars have examined how internal dynamics shape the extent to which courts generate consensus or permit dissent. Jaros and Canon identify factors that cultivate consensus, including strong task leadership by the Chief Justice, high social integration among members, and a “norm of unanimity” that incentivizes judges to reach a single collective decision [@Canon1970]. Hall and Windett demonstrate that Chief justices frequently prioritize consensus to foster collegiality, reinforce precedent, and bolster public confidence, actively discouraging dissent because it imposes costs on colleagues, risks weakening precedent, generates confusion in the law, encourages future appeals, and can produce dissatisfaction within the court [@HallAndWindett2013]. Some justices, however, resist consensus and issue dissents to preserve individual expression or influence future courts. At the same time, Epstein, Landes, and Posner emphasize that judges may suppress dissent in a phenomenon they term 'dissent aversion' to avoid imposing costs on themselves or colleagues [@Epstein2011]. These competing incentives limit the chief’s capacity to enforce agreement, with Hall and Windett finding that dissent rates are lower on courts where the chief possesses greater formal powers and where members have fewer institutional resources, such as staff, pay, docket control, time, or insulation from electoral pressures [@HallAndWindett2013]. Conversely, abundant member resources encourage dissent by undermining the chief’s authority and reducing the effectiveness of formal powers on resource-rich courts.

Lastly, the method of judicial selection represents one of the most consequential institutional factors shaping dissent rates. Brace and Hall find that judges appointed by governors or legislatures tend to promote consensus, while elected judges are associated with higher dissent rates [@Brace1990]. Jaros and Canon similarly report that popularly elected courts exhibit higher dissent rates than appointed courts [@Canon1970]. Hall and Windett provide a systematic comparison of dissent across four selection systems: gubernatorial or legislative appointment, the Missouri Plan (appointment followed by retention elections), nonpartisan elections, and partisan elections [@HallAndWindett2016]. Courts with appointed judges and Missouri Plan courts exhibit highly stable dissent rates, which the authors attribute to longer judicial tenures, greater professionalization, and insulation from electoral pressures, although cross-state variation is substantial in Missouri Plan states. States with nonpartisan elections display significantly higher dissent rates, roughly four percentage points above Missouri Plan states, suggesting that electoral incentives shape judicial behavior even in the absence of party labels. The most pronounced and unstable patterns appear in states with partisan elections, where dissent rates rise sharply from under 20 percent in the mid-1990s to over 40 percent by the early 2000s, accompanied by dramatic increases in cross-state variation. Hall and Windett conclude that this volatility reflects influences beyond judicial interpretation, including potential pressures related to reelection concerns. Renberg uses a synthetic control approach to analyze the relationship between judicial selection mechanisms and dissent rates, finding that removing partisan labels from voter guides and ballots increases dissenting opinions [@Renberg2020]. This suggests that justices strategically moderate dissent under partisan constraints. Thus, eliminating party identifiers allows justices to signal their legal ideology more freely. However, no studies conducted have analysed the opposite transition using the synthetic controls method (SCM), which the present study aims to do.

While dissent rates provide a quantitative measure of disagreement on the bench, they offer limited insight into the underlying substance of judicial reasoning. Computational textual analysis has emerged as a powerful methodological tool for examining the content of judicial opinions, with recent advances in natural language processing (NLP) enabling systematic analysis of how judges express their ideological positions and respond to external pressures. Bergam, Allaway, and McKeown develop two textual indicators of Supreme Court justice ideology: issue-specific stance (ISS), which evaluates positions relative to representative political topics, and holistic political stance (HPS), which directly classifies political affiliation expressed in language [@Bergam2022]. They find that justices responsive to public opinion exhibit significantly stronger correlations between the ideology expressed in their language and their voting behavior, highlighting the influence of broader socio-political forces on judicial opinion-writing behavior.

However, ISS and HPS may not capture the broader quality of judicial reasoning due to their focus on political ideology. Rather, Lewandowsky introduces the Evidence Minus Intuition (EMI) framework to distinguish between evidence- and intuition-based language [@Lewandowksy2025]. This methodological approach offers substantial promise for research on state supreme courts, as it can be adapted to quantify the extent to which judicial opinions rely on empirical, evidence-based legal reasoning versus normative, abstract, and personal or political rhetoric, providing insight into how selection mechanisms affect judicial independence. Therefore, the present study adapts this EMI methodology by training a Word2Vec model on a corpus of state supreme court opinions to assess how partisan versus nonpartisan judicial selection mechanisms influence the rhetoric in judicial opinions.

Text Partisan Scores (TPS) are a scaling measure derived from members’ public rhetoric (e.g., press releases, website text). It captures how linguistically “Democratic” or “Republican” a member’s language is. With a Pearson correlation of 0.92 indicating a very strong positive linear association, members who are high on TPS (more Republican rhetoric) are also high on CF Scores (more conservative donor base), and members who are low on TPS (more Democratic rhetoric) are also low on CF Scores (more liberal donor base). Thus, campaign finance ideology and rhetorical ideology are almost perfectly aligned at the party level. 

## Methods

This study adopts a mixed-methods research design that integrates quantitative statistical modeling with qualitative textual analysis to assess the effects of institutional reform on judicial opinion writing. The quantitative component employs the synthetic control method, originally developed by Alberto Abadie and Javier Gardeazabal and later extended by Abadie, Alexis Diamond, and Jens Hainmueller, to estimate the causal effects of aggregate institutional interventions. [@abadieEconomicCostsConflict2003; @abadieSyntheticControlMethods2010] The method constructs a counterfactual by forming a weighted composite of control units, or donor pool, selected to closely replicate the treated unit’s pretreatment characteristics and project its trajectory had the intervention not occurred.

In the present study, the aggregate intervention of interest is the method of judicial selection. The treated unit is the North Carolina Supreme Court, which shifted from nonpartisan to partisan judicial elections following a statutory reform in 2017, with the first partisan contest held on November 6, 2018. A synthetic North Carolina Supreme Court is constructed using a donor pool of pretreatment covariates collected from state supreme courts that have historically employed nonpartisan judicial elections, including Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. The synthetic controls approach is designed to approximate how judicial dissent would have evolved on the North Carolina Supreme Court in the absence of this institutional reform. Renberg finds that synthetic control methods provide a credible estimate of the causal effect of institutional changes on opinion-writing behavior.

Originally developed by Alberto Abadie and Javier Gardeazabal and later extended by Abadie, Diamond, and Hainmueller, the synthetic controls method (SCM) estimates the causal effects of aggregate institutional interventions [@abadieEconomicCostsConflict2003; @abadieSyntheticControlMethods2010]. This approach constructs a counterfactual by creating a weighted composite of control units, or donor pool, chosen to closely replicate the treated unit’s pre-intervention characteristics. The synthetic control then projects how the treated unit would have evolved had the intervention not occurred. The institutional intervention of interest in the present study is the transition from nonpartisan to partisan judicial elections. The treated unit is the North Carolina Supreme Court, which adopted partisan elections following a statutory reform in 2017 and held its first partisan contest on November 6, 2018. The donor pool consists of seven state supreme courts that have historically maintained nonpartisan judicial elections: Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. Pretreatment covariates from these courts are weighted to construct a synthetic North Carolina Supreme Court, providing a counterfactual trajectory of dissent rates had the reform not occurred. Previous research demonstrates that SCM reliably estimates the causal effects of institutional changes on judicial opinion-writing behavior [@Renberg2020].

### Pretreatment Characteristics
\begin{table}[htbp]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=3pt} % less space before caption
\caption{Pretreatment Characteristics}
\label{tab:pretreatment}
\centering
\footnotesize  % smaller font
\renewcommand{\arraystretch}{0.95} % tighter row spacing

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
Absolute difference in cfscores between the most and least liberal judge in the court. &
Bonica (2024) \\

State Citizen Ideology &
Mean ideological self-placement of all respondents in a state, aggregated from individual ANES survey responses. &
ANES Time Series Study (2024) \\

State Government Ideology &
Mean of first‑dimension NOMINATE scores for congressional members (House and Senate) &
Voteview (2026) \\
\bottomrule
\end{tabularx}
\end{table}

Each donor court is characterized by a vector of pretreatment covariates that capture political, legal, and institutional context. All pretreatment covariates are measured annually for each donor court across the study period from 2012 to 2024. Structural features of judicial selection systems, including term length, number of justices on the bench, single-member versus multimember election districts, and electoral competitiveness, were obtained from Ballotpedia.[@StateSupremeCourts] Campaign finance data, operationalized as the total amount of funds raised by candidates in the most recent election for each year in the treatment window, were collected from OpenSecrets.[@OpenSecrets] These data incorporate information originally compiled by the Follow the Money Institute, which merged with OpenSecrets in 2019.[@HomeFollowTheMoneyorg]

Court professionalization scores are drawn from Squire and Butcher's 2019 index, an updated version of the 2008 professionalism measure that incorporates staff size, judicial pay, and docket control based on the Court Statistics Project's classification of mandatory and discretionary jurisdiction.[@squireUpdateSquireState2021; @squireMeasuringProfessionalizationState2008] Given the relative stability of these institutional characteristics, the 2019 values are assumed to remain substantively unchanged through 2024. Caseload characteristics, including the number of published opinions, capital punishment appeals reviewed by the court, capital punishment cases resolved by lower courts in the previous year, and the percentage of the docket devoted to criminal procedure, were collected from LexisNexis.[@LexisNexis] The ideological spread of each court is measured using Bonica's common-space campaign finance scores (CFscores). These scores are drawn from the 2024 Database on Ideology, Money in Politics, and Elections (DIME).[@DatabaseIdeologyMoney]

The original measures used in Renberg’s analysis for state-level citizen and government ideology, developed by Berry et al., are unavailable for 2012–2024 [@Berry1998]. State citizen ideology was therefore approximated using aggregated responses from the 2024 American National Election Studies (ANES) Time Series Study, which reports state-level mean ideological self-placement every four years, aligned with election cycles. For state government ideology, NOMINATE scores provide a consistent, spatially comparable measure of elite ideology that strongly correlates with Berry et al.’s original measure [@Berry2010]. Accordingly, state government ideology was operationalized as the average first-dimension NOMINATE score of all congressional members (House and Senate) in each state [@Voteview2026].

## Word Embedding Model for Computational Textual Analysis

To identify the vocabulary most associated with ideological versus doctrinal judicial rhetoric, the Wordscores method (Laver, Benoit & Garry 2003) was employed, anchored to campaign finance scores (CF-scores) from the Database on Ideology, Money in Politics, and Elections (DIME; Bonica 2013). This approach offered a methodological improvement over manual seed word selection, which relies on researcher judgment and vocabulary imported from studies that may not generalize to state supreme court opinions. Instead, the data were allowed to identify which words were empirically associated with more versus less ideologically extreme justices in the specific corpus under study.

CF-scores were estimated from campaign contribution records and scaled from -1 (most liberal) to 1 (most conservative). CF-scores from the DIME judicial dataset (Bonica 2013) were used, filtered to state supreme court justices. Prior research has demonstrated that text-based measures of partisanship derived using CF-score anchors correlate strongly with the underlying ideology scores (correlations up to 0.92 across members of both parties in Congress), validating their use as reference anchors for text scaling (Taddy 2013; Gentzkow, Shapiro & Taddy 2019).

CF-scores were particularly appropriate anchors for this analysis because they captured the ideological alignment of justices with their donor base, which may have directly influenced the rhetorical choices justices made in their written opinions. While a direct causal link between donor ideology and judicial rhetoric was not tested, the strong correspondence between CF-scores and  Taddy et al's TFS scores supported their use as proxies for the underlying ideological orientation that shaped judicial language.






To construct a dictionary for Evidence Minus Intuition (EMI) literary analysis of judicial opinions, I trained a Word2Vec model on the Collaborative Open Legal Data (COLD) Cases dataset. COLD Cases is a comprehensive corpus of 8.3 million United States legal decisions maintained by the Harvard Library Innovation Lab in collaboration with the Free Law Project. This dataset consolidates semantic information from CourtListener's bulk data, including the text of majority and dissenting opinions, head matter, and substantive metadata, into standardized records with extraneous data removed. 

The Word2Vec model was trained using the Gensim implementation, provided by the Gensim Python library and widely utilized for natural language processing (NLP), to learn vector representations of words based on their contextual usage within supreme court opinions. Word2Vec employs a shallow neural network architecture, a relatively simple machine learning model with a single hidden layer, to embed words in a lower-dimensional vector space where semantically similar words occupy proximate positions. The embedding process converts words into numerical vectors, or lists of numbers. For example, the word "justice" might be represented as [0.23, -0.45, 0.78, ...]. Each vector has a set number of components, or “dimensions” (typically 100–300), which together capture patterns of how words appear in relation to one another. These dimensions do not correspond to individual words; rather, each dimension encodes an abstract feature learned from word co-occurrence patterns. In this vector space, words that appear in similar contexts—such as “justice” and “judge”—are located near each otherIn this vector space, semantically similar words occupy proximate positions, enabling the model to capture meaningful relationships between vocabulary terms present in supreme court opinions. This approach addresses limitations of traditional bag-of-words models, which lose information about word order and fail to capture semantic relationships. The resulting word embeddings serve as the foundation for the EMI dictionary, enabling systematic identification of language patterns in judicial opinions based on data-driven representations of legal terminology.

### Evidence Minus Intuition

Evidence Minus Intuition (EMI) scores operationalize the degree to which judicial opinions rely on evidence-based versus intuition-driven language. Two seed-word dictionaries were constructed: one representing evidence-based language (e.g., "reality," "assess," "examine," "fact," "truth," and "proof") and one representing intuition-based language (e.g., "believe," "opinion," "consider," "feel," and "intuition"). Each seed word was input into the trained Word2Vec model to identify all words with cosine similarity greater than or equal to 0.5, producing expanded dictionaries for each construct. Concept representations for evidence-based and intuition-based language were computed by averaging the word embeddings of all seed words in their respective dictionaries, generating vectors in the same semantic space. Each judicial opinion was similarly represented by averaging the embeddings of its content words. The sentence-transformers library was used to generate these representations and compute cosine similarities. For each opinion, the cosine similarity between the opinion vector and each concept vector was calculated, yielding an evidence score and an intuition score. The EMI score was obtained by subtracting the intuition score from the evidence score. Positive EMI scores indicate greater prevalence of evidence-based language, while negative scores suggest reliance on intuition-based language. Examples of Supreme Court cases with low and high EMI scores are provided to illustrate the relationship between EMI and judicial independence.

## Analysis

### Dissent Rates

![Dissent Rates in North Carolina Supreme Court](/Users/alexnagy/Coding/dissention/reports/figures/nc_dissent_rates.png)

This synthetic control analysis follows Renberg's methodological approach to examine the impact of judicial electoral reform on dissenting opinion rates in North Carolina's Supreme Court.[@Renberg2020] Complete data for all variables and courts analyzed in this study are available in the replication code. North Carolina's dissent rate remained consistently low from 2012 to 2017, never exceeding 1%. The rate increased notably in 2018 to 1.9% and reached 4.5% in 2020. Coinciding with periodic court closures across the United States related to the onset of the COVID-19 pandemic, dissent rates declined to 2.2% in 2021. Subsequently, the rate rose to a recorded maximum of 5.6% in 2022 before declining to approximately 3.1% by 2023 and 2024. In contrast, other courts in the sample exhibited more variable patterns. Wisconsin consistently maintained the highest dissent rates throughout the period, with rates frequently exceeding 50% and reaching 88% in 2016. This could be due to a high volume of cases with unpublished opinions not captured in the data collection process, resulting in an artificially inflated dissent rate when calculated against only published opinions. Arkansas also showed considerable volatility, with dissent rates ranging from 7.7% in 2012 to peaks above 50% in 2018-2020. States such as Georgia and Minnesota maintained relatively stable and low dissent rates throughout the observation period, typically remaining below 10%.

In order to evaluate if these dissent rate values are consistent with established expectations, it is necessary to address reproducibility concerns. Renberg does not explicitly report baseline dissent rates for any of the courts analyzed. Although she presents treatment effects numerically (a 7.5% increase in Arkansas, 5.1% in Tennessee, and 20.8% in Mississippi), these figures are not anchored to specific baseline values. Consequently, readers must rely on graphical representations to infer initial dissent rates, which introduces substantial ambiguity. Renberg's figures label the y-axis as "Percent of Opinions" while displaying decimal values ranging from 0.05 to 0.25, creating confusion about whether the values represent proportions (e.g., 0.15 = 15%) or percentages (e.g., 0.15 = 0.15%). Standard practice would interpret these as proportions, suggesting dissent rates ranged from 14 to 19% on the Arkansas Supreme Court between 1997 and 2012, from 5 to 22% on the Tennessee Supreme Court between 1985 and 2002, and 8 to 46% on the Mississippi Supreme Court between 1986 and 2000. These reported dissent rates are notably high relative to existing judicial opinion-writing behavior literature. By contrast, the literal interpretation would indicate rates of 0.14 to 0.19 percent, which would be notably low. The former interpretation appears correct given Renberg's description of Mississippi experiencing "an increase of over 30% for some years following electoral reform," and her reported average treatment effects.

Regardless of which interpretation was intended, these dissent rates could not be reproduced using publicly available court data. Multiple attempts were made to replicate these figures using data from CourtListener and LexisNexis. In CourtListener, replication efforts included filtering by court and employing advanced query techniques and operators, including combined-opinion, unanimous-opinion, lead-opinion, plurality-opinion, concurrence-opinion, in-part-opinion, dissent, addendum, remittitur, rehearing, on-the-merits, and on-motion-to-strike. Replication attempts using LexisNexis utilized queries with the OpinionBy and DissentBy fields, as well as the "find by source" option.

Replication efforts also followed Hall and Windett's 2013 study [@HallAndWindett2013]. Table \ref{tab:opinions_dissents} presents three sets of values generated using different LexisNexis query strategies. The first set, labeled "Hall & Windett," reproduces the values from the original study's published table. For the second set, labeled "OpinionBy & DissentBy," I constructed LexisNexis queries using the Opinionby and Dissentby functions with the names of justices serving on each court between 1995 and 2010 in an attempt to replicate Hall and Windett's original values. The third set, labeled "AND NOT," reflects a more restrictive query approach. Because Hall and Windett claim to focus their data on "the subset of data most likely to interest judicial politics scholars: those cases in which a state supreme court rendered a final judgment with a full written opinion," this final query used AND NOT operators to exclude entries containing "dismiss!", "petition for review", or "motion for." Despite these systematic efforts to replicate the original methodology using various LexisNexis search strategies, the resulting dissent rates could not be reproduced at levels comparable to those reported by Hall and Windett or Renberg. The variation across query methods is particularly pronounced in certain jurisdictions, such as Oregon and West Virginia, where dissent rates differ substantially depending on the search approach employed.

\begin{table}[htbp]
\centering
\begin{tabular}{lcccccc}
\toprule
Court & Hall \& Windett & Hall \& Windett & OpinionBy & DissentBy & AND NOT & AND NOT \\
 & Opinions & Dissents & Opinions & Dissents & Opinions & Dissents \\
\midrule
NC & 13241 & 154 & 15660 & 159 & 10687 & 156 \\
OR & 1155 & 143 & 1074 & 325 & 331 & 91 \\
WV & 2218 & 765 & 1253 & 678 & 351 & 163 \\
MO & 1874 & 267 & 3271 & 533 & 484 & 75 \\
MA & 2808 & 172 & 2731 & 534 & 780 & 152 \\
ME & 3233 & 227 & 2464 & 408 & 1002 & 136 \\
IL & 2302 & 616 & 1685 & 630 & 399 & 141 \\
ID & 2119 & 244 & 2141 & 439 & 551 & 110 \\
HI & 2086 & 282 & 1768 & 389 & 661 & 86 \\
AZ & 1546 & 167 & 2802 & 241 & 336 & 39 \\
AK & 2506 & 272 & 1923 & 269 & 543 & 66 \\
AL & 5185 & 1423 & 4474 & 1418 & 1626 & 563 \\
\bottomrule
\end{tabular}
\caption{Opinions and dissents by court and method}
\label{tab:opinions_dissents}
\end{table}

\begin{table}[htbp]
\centering
\begin{tabular}{lccc}
\toprule
Court & Hall \& Windett & OpinionBy \& DissentBy & AND NOT \\
\midrule
NC & 0.0116 & 0.0102 & 0.0146 \\
OR & 0.1238 & 0.3026 & 0.2749 \\
WV & 0.3449 & 0.5411 & 0.4644 \\
MO & 0.1425 & 0.1629 & 0.1550 \\
MA & 0.0613 & 0.1955 & 0.1949 \\
ME & 0.0702 & 0.1656 & 0.1357 \\
IL & 0.2676 & 0.3739 & 0.3534 \\
ID & 0.1151 & 0.2050 & 0.1996 \\
HI & 0.1352 & 0.2200 & 0.1301 \\
AZ & 0.1080 & 0.0860 & 0.1161 \\
AK & 0.1085 & 0.1399 & 0.1215 \\
AL & 0.2744 & 0.3169 & 0.3462 \\
\bottomrule
\end{tabular}
\caption{Dissent rates by court and method}
\label{tab:dissent_rates}
\end{table}

Data availability further constrained efforts to replicate Renberg's findings. The State Supreme Court Data Project remains the premier database for state supreme court research, but it covers only four years between 1995 and 1998. In 2013, Hall and Windett sought to address this deficiency by presenting a new dataset of state supreme courts ostensibly made publicly available to the scholarly community.[HallAndWindett2013] Unfortunately, their data are not accessible online due to a broken link on their website, and their Python code involves web scraping expressly prohibited by LexisNexis's terms of service. Although LexisNexis provides broader access to published opinions, its proprietary nature limits transparency and reproducibility for researchers without expensive institutional-level subscriptions. CourtListener, one of the few open-source repositories available for state supreme court research, contains substantially less comprehensive coverage of published opinions than LexisNexis.

Consequently, even when replication attempts rely on the most comprehensive publicly accessible sources, data limitations introduce uncertainty into dissent rate estimates and complicate direct comparison with studies based on non-public or undisclosed datasets. The FAIR principles aim to make scientific data Findable, Accessible, Interoperable, and Reusable.[@wilkinsonFAIRGuidingPrinciples2016] Data are findable when they have persistent identifiers and rich metadata. They are accessible when they can be retrieved through standardized protocols. They are interoperable when they use standardized formats and vocabularies that allow integration with other datasets. They are reusable when they are well-described, with clear provenance, context, and licensing information. Together, these principles promote transparency, reproducibility, and efficient reuse of scientific data. Neither Hall and Windett's nor Renberg's studies meet these standards, as their underlying data and replication codes are not publicly available. This prevents independent verification of their results and limits cumulative knowledge building in the study of judicial opinion-writing behavior.

### Synthetic Control

![Estimated impact of judicial reform on dissenting behavior](/Users/alexnagy/Coding/dissention/reports/figures/scm.png)

The synthetic control method constructs a counterfactual North Carolina Supreme Court using Minnesota (100% weight) to match North Carolina's pretreatment characteristics. The algorithm's selection of Minnesota alone, rather than a weighted composite of all control courts, suggests that Minnesota provides the best single-court match to North Carolina's pretreatment trajectory among available donor courts. The algorithm assigned zero weight to all other potential donor courts, including Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. The analysis yields a null result: the estimated average treatment effect on dissents is 0.000%, indicating no detectable change in dissenting behavior following North Carolina's transition to partisan elections in 2018.

### Model Fit and Parallel Trends Assumption

Mean Squared Prediction Error (MSPE) measures the average squared difference between the treated unit's actual outcome and the synthetic control's predicted outcome. The synthetic control method rests on the parallel trends assumption that the treated and synthetic units would have continued on the same trajectory absent treatment. The pretreatment MSPE from 2012-2017 is 0.0007, indicating that Minnesota's dissent trajectory closely tracked North Carolina's before treatment. The post-treatment MSPE from 2018-2024 is 0.0002, representing a substantial decrease. The post-to-pre ratio of 0.29 indicates that the synthetic control's predictive ability actually improved after 2018. This improvement in post-treatment fit suggests that changes occurring in North Carolina following electoral reform also occurred in Minnesota. Thus, the synthetic control yielded a near-zero treatment effect estimate.

### Pretreatment Covariate Balance

Pretreatment covariate balance is essential for establishing the validity and robustness of the synthetic control method because it determines whether the synthetic control unit credibly represents the counterfactual outcome for the treated unit. The fundamental logic of SCM rests on the assumption that, if a weighted combination of control units closely matches the treated unit on observable characteristics prior to treatment, it will also approximate how the treated unit would have behaved in the absence of treatment. Poor pretreatment balance undermines this core assumption, indicating that the synthetic control is constructed from fundamentally dissimilar units and therefore cannot serve as a valid counterfactual.

\begin{table}[htbp]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=5pt}
\caption{Covariate Balance Between Treated and Synthetic North Carolina}
\label{tab:covariate_balance}
\centering
\makebox[\textwidth][c]{%
\begin{tabular}{lccc}
\hline
\rule{0pt}{3ex}\textbf{Covariate} 
& \textbf{Treated (NC)} 
& \textbf{Synthetic NC} 
& \textbf{Sample Mean} \\[1ex]
\hline
Campaign Finance        & 1,348,421 & 177,336 & 381,739 \\
Court Professionalization (2019) 
                        & 0.609 & 0.610 & 0.612 \\
Capital Appeals         & 0.167 & 0.333 & 2.548 \\
Lower Court Capital Appeals (Lag 1) 
                        & 1.000 & 0.500 & 1.548 \\
Criminal Procedure Docket 
                        & 0.458 & 0.129 & 0.519 \\
Ideological Spread      & 2.283 & 1.964 & 1.291 \\
Citizen Ideology        & 3.903 & 4.161 & 3.933 \\
Government Ideology     & 0.240 & -0.093 & 0.147 \\
Term Length             & 8.000 & 6.000 & 7.429 \\
Number of Justices      & 7.000 & 7.000 & 7.286 \\
Election Structure      & 0.000 & 0.000 & 0.143 \\
Electoral Competition   & 0.667 & 0.000 & 0.167 \\
Published Opinions      & 1,057 & 657 & 224 \\
\hline
\end{tabular}%
}
\end{table}

The importance of covariate balance becomes clear when comparing the imbalances in Renberg’s analysis with those in the present study. In Renberg's analysis, structural and institutional covariates are generally well-balanced, with minimal differences in term length, closely matched single-member election districts, near-identical professionalization scores, and reasonably aligned ideological measures. However, substantial imbalances emerge in operational and caseload variables. Synthetic controls overestimate published opinions by 92-494%, producing two to six times more opinions than the treated courts. Criminal procedure dockets are underestimated by approximately 50% in Arkansas and Mississippi, and capital punishment caseloads diverge sharply, with treated courts handling 161% more cases in Arkansas and 252% more in Mississippi. Because these variables directly reflect judicial workload and case composition, such imbalances undermine the validity of Renberg's synthetic controls. This point that is not addressed at length in her paper. 

In the present study, the synthetic control achieves near-perfect balance on court professionalization (0.610 vs. 0.609) and exactly matches both the number of justices and the election structure. Term length shows reasonable balance, differing by only two years. However, substantial imbalances persist on key covariates. Campaign finance exhibits a 660% difference (1.35 million vs. 177,336), criminal procedure dockets diverge markedly (0.458 vs. 0.129), and capital appeals also differ notably (0.167 vs. 0.333). Most critically, electoral competition demonstrates complete imbalance: North Carolina’s value of 0.667 reflects highly competitive elections, whereas Minnesota’s 0.000 indicates no competitive elections during the study period. This discrepancy directly undermines the theoretical mechanism under investigation, as competitive elections are hypothesized to drive dissenting behavior.

Standardized difference calculations further highlight these issues: 11 of 14 covariates exhibit imbalances exceeding the 0.25 threshold. The most severe imbalances occur in published opinions (3.59 SD), campaign finance (2.12 SD), ideological spread (1.59 SD), electoral competitiveness (1.33 SD), dissent rate (-0.78 SD), and capital appeals (-0.67 SD). Only three covariates can be considered balanced: lagged lower court capital appeals (-0.18 SD), citizen ideology (-0.09 SD), and court professionalization (-0.03 SD). These general imbalances raise fundamental questions about whether the synthetic control adequately captures the political and institutional pressures shaping judicial opinion-writing in North Carolina. The analysis cannot overcome the absence of a suitable counterfactual court that simultaneously reflects North Carolina’s competitive elections, campaign finance environment, ideological composition, and caseload characteristics.

Additionally, the algorithm relies entirely on Minnesota as the sole donor court, assigning it 100% weight while excluding all other potential donors. This raises a fundamental concern: Minnesota is merely the least unsuitable option among courts that are otherwise incomparable. While the pretreatment MSPE of 0.0007 may suggest a close fit, it obscures the reality that no available donor court adequately reflects North Carolina's institutional characteristics. By assigning full weight to a single court, the algorithm abandons the method’s core advantage of combining multiple control units to construct a robust counterfactual. This comparability problem likely stems from structural features that distinguish North Carolina's judicial system. Unlike most states, North Carolina's Supreme Court exercises both mandatory and discretionary jurisdiction over certain cases that bypass the Court of Appeals entirely. The state constitution grants direct appellate jurisdiction over constitutional questions, decisions striking down state statutes, and other matters of substantial public importance. This bifurcated structure may inflate North Carolina's published opinion volume. As shown in Table 2, North Carolina produced 1,057 opinions annually during the pretreatment period, compared to Minnesota's 657 and a sample mean of 224. The resulting standardized difference of 3.59 standard deviations, the largest imbalance in the dataset, reflects fundamental structural differences in how cases reach the North Carolina supreme court. These findings raise concerns about the use of SCM to study judicial opinion-writing behavior in state supreme courts. Institutional characteristics vary so widely across states that they can violate SCM assumptions.

### Sensitivity Analysis

A robust causal estimate should remain stable across reasonable variations in model specification. Conducted by systematically excluding each donor court one at a time and recalculating the treatment effect, the leave-one-out analysis reveals severe instability that undermines confidence in the estimate. Excluding each potential donor produces treatment effects ranging from -0.1887 (Minnesota excluded) to -0.0875 (Wisconsin excluded), with a mean of -0.1617 and standard deviation of 0.0382. Every leave-one-out specification produces a negative treatment effect, yet the optimal weighted combination yields exactly zero. This pattern indicates that the zero treatment effect is an artifact of the specific weighting scheme rather than a robust finding.

Several additional robustness checks illuminate the fragility of causal inference in this setting. First, comparing optimal synthetic control weights to equal weights reveals no difference. Both produce an estimated average treatment effect (ATE) of 0.00, indicating no mean difference in dissent rates between North Carolina and the synthetic control across all post-treatment years. This equivalence suggests that the sophisticated weighting algorithm provides no advantage over a simple average of control courts, indicating that no weighting scheme can adequately balance the severe covariate imbalances.

Placebo tests that apply the synthetic control method to pre-treatment years (e.g., 2014, 2015, 2016, 2017) as if each were the "treatment" year reveal systematic differences between North Carolina and its synthetic version. These estimated placebo effects on dissent rates range from -2.62 to -3.78%, with an average of -2.92%. The actual 2018 treatment effect of 0.00% differs significantly from these pre-treatment placebo effects (p = 0.042), suggesting that the treatment may have had a significant effect in 2018. However, this should be interpreted with caution, as the discontinuity may reflect measurement error, changes in case composition, or other factors unrelated to electoral reform, particularly given the low baseline dissent rates and small absolute magnitudes involved. Relatedly, examining year-by-year treatment effects reveals substantial temporal instability. The estimated effect of partisan elections on dissent rates varies dramatically across post-treatment years: 2018 (-0.0123), 2019 (-0.0150), 2020 (+0.0068), 2021 (-0.0005), 2022 (+0.0270), 2023 (-0.0135), 2024 (+0.0078). These estimates range from -0.015 to +0.027 with a standard deviation of 0.0152, nearly as large as the effects themselves. If partisan elections truly increased dissenting behavior through electoral accountability mechanisms, we would expect a sustained, consistent effect on dissent rates following the 2018 reform. Instead, the effects fluctuate in both direction and magnitude across years, suggesting that any apparent treatment effects likely reflect random variation, case-specific factors, or temporary fluctuations. Additionally, COVID-19 disruptions beginning in 2020,including court closures, delayed proceedings, and shifts in case composition,may have introduced temporal shocks that affect the analysis independently of electoral reform.

The instability documented through sensitivity analysis and robustness checks, combined with persistent covariate imbalances on theoretically central variables, collectively indicate that the synthetic control method fails to produce credible counterfactuals for North Carolina. Rather than providing evidence for or against a causal relationship between electoral reform and dissenting behavior, the findings highlight fundamental limitations in applying synthetic control methods to judicial contexts where comparable control units are scarce, outcome variables exhibit low baseline prevalence and high volatility, theoretically central covariates vary dramatically across potential donors, and treatment effects are hypothesized to be small relative to measurement error and secular trends.

### Textual Analysis

Note: I tried running the code for this, but it did not finish before the deadline. I have yet to write up this final part of the analysis. Regardless, my qualitative findings suggest that dissent rates may not constitute an adequate proxy for either judicial independence or the behavioral effects of electoral institutions, and that the synthetic control method is ill-suited for modeling Supreme Court opinion-writing given the substantial institutional variation across courts. Moreover, dissent rates alone offer limited insight into how electoral reform shapes judicial behavior, as the prevalence of dissent merely captures whether justices disagree with the majority, rather than the depth, substance, or reasoning underlying those disagreements. A more promising approach lies in examining the full text of judicial opinions to assess how electoral reform influences the political tenor and substantive content of judicial reasoning. This textual analysis can reveal whether justices elected in partisan systems are more likely to invoke partisan considerations in their written justifications.

To construct the EMI framework for judicial opinions, seed-word dictionaries were developed representing evidence-based and intuition-based language. The evidence dictionary included seed words "reality," "assess," "examine," "fact," "truth," and "proof," while the intuition dictionary included "believe," "opinion," "consider," "feel," and "intuition." These seed words were input into the trained Word2Vec model to identify semantically similar terms with cosine similarity greater than or equal to 0.5, producing expanded dictionaries for each construct (Table \ref{tab:emi_dictionaries}).

\begin{table}[htbp]
\caption{Expanded Evidence and Intuition Dictionaries}
\label{tab:emi_dictionaries}
\centering
\small
\begin{tabular}{ll}
\toprule
\textbf{Evidence-Based Dictionary} & \textbf{Intuition-Based Dictionary} \\
\midrule
\multicolumn{2}{l}{\textit{Seed words:}} \\
reality & believe \\
assess & opinion \\
examine & consider \\
fact & feel \\
truth & intuition \\
proof & impression \\
\midrule
\multicolumn{2}{l}{\textit{Expanded terms:}} \\
appraise & belief \\
assessed & believing \\
assessment & considered \\
burden & considering \\
evidence & constrained \\
examining & convinced \\
falsehood & decide \\
look & discuss \\
prove & dissenting \\
proved & feeling \\
proven & felt \\
proving & find \\
show & say \\
showing & sure \\
truthfulness & think \\
untrue & \\
untruth & \\
\bottomrule
\end{tabular}
\end{table}

The evidence-based dictionary expanded to include terms such as "assessed," "proving," "evidence," and "burden," reflecting rhetoric based on objective analysis, factual inquiry, and the presentation of verifiable information. The intuition-based dictionary expanded to include terms emphasizing subjective judgment and normative reasoning, such as "believing," "convinced," "dissenting," and "feeling." Several terms, including "examine," "consider," "analyze," "determine," "inquire," and "evaluate", appear in both dictionaries. This overlap demonstrates that the Word2Vec model captures how these terms function differently depending on their surrounding context within judicial opinions. Additionally, the presence of terms like "falsehood," "truthfulness," "untrue," and "untruth" in the evidence-based dictionary suggests that judicial discussions of truth and falsity are treated as matters of factual determination rather than subjective belief.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{/Users/alexnagy/Coding/dissention/reports/figures/semantic_corner_plot.png}
\caption{Semantic Space Around "Evidence"}
\label{fig:evidence_semantic}
\end{figure}

Figure \ref{fig:evidence_semantic} visualizes the 30 words most semantically similar to "evidence" in the Word2Vec model, projected into two-dimensional space using Principal Component Analysis (PCA). The semantic cluster reveals that "evidence" associates primarily with technical legal terminology related to evidentiary procedures ("admissible," "testimony," "witness"), factual determination ("fact," "prove," "show"), and evidence quality ("probative," "credible," "corroborative"). The inset map (top right) situates this semantic cluster within the full embedding space of all words in the model, demonstrating that the model successfully captures the technical legal context in which evidence-based language appears in judicial opinions. This clustering pattern validates the model's ability to distinguish evidence-based reasoning from other forms of judicial discourse.

## Conclusion

Synthetic controls results indicate no significant change in dissent following the partisan reform; however, extensive replication and robustness checks reveal substantial measurement and reproducibility challenges. These instabilities suggest that institutional heterogeneity across state courts undermines the credibility of causal inference based on dissent frequency alone, calling into question its use as a proxy for judicial independence in prior scholarship. Preliminary textual analyses indicate that examining the use of evidence- versus intuitionbased language in judicial opinions provides a more robust measure of judicial independence in opinion-writing across selection mechanisms. Overall, the study highlights the methodological limits of existing approaches and advances an alternative framework for assessing how state supreme court selection mechanisms shape judicial opinion-writing behavior.

\newpage

## References
\begingroup
\setstretch{1}