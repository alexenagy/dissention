---
title: The Impact of Judicial Selection Mechanisms on Opinion Writing Behavior
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
  - \usepackage{rotating}
abstract: |
  Insert abstract here
link-citations: false
---

## Introduction

The United States is undergoing a profound transformation in its judicial landscape. In a period marked by rising polarization and a more openly majoritarian conservative constitutional order, the Supreme Court of the United States has delegated responsibility for resolving many contentious national issues to the states by narrowing federal oversight in areas such as campaign finance, partisan gerrymandering, abortion, and voting rights. As the stakes of state-level adjudication have increased, the expected policy payoff of controlling state supreme courts has risen as well. State legislatures and partisan actors have responded by restructuring judicial selection systems to allow for greater direct political influence, most prominently by replacing nonpartisan judicial elections with explicitly partisan contests through the inclusion of party affiliations on ballots. In 2025, Montana’s legislature advanced five proposals to introduce partisan judicial contests [@Montana2025]. Although these measures were ultimately defeated in Montana, comparable reforms have succeeded elsewhere. Ohio enacted Senate Bill 80 in 2021; North Carolina passed Session Law 2016-125 in 2016; West Virginia adopted Senate Bill 521 in 2025.^[See Ohio S.B. 80 (2021); N.C. Sess. Law 2016-125 (2016); W. Va. S.B. 521 (2025).] Each of these laws requires candidates to list party affiliation on both primary and general election ballots, thereby formalizing partisanship in state supreme court elections.

Against this backdrop, scholars remain divided over whether the shift toward partisan judicial selection effectively balances judicial independence and accountability, two principles that are inherently in tension^[See @Hall2001 for an overview of the scholars involved in this debate]. Judicial independence allows courts to decide cases based on law and free from external pressures, while accountability requires them to remain responsive to public values and societal needs. Reform advocates tend to argue that partisan elections place too much emphasis on party loyalty and electoral considerations, undermining independence and risking decisions driven more by politics than by legal reasoning. They generally favor nonpartisan elections or merit-based retention systems, such as the Missouri Plan, to prioritize professional qualifications and preserve judicial autonomy. In contrast, opponents of reform contend that partisan elections enhance democratic accountability without necessarily eroding independence, as electoral competition incentivizes judges to remain attentive to voter concerns. This debate highlights how different selection mechanisms structure judicial incentives and shape the potential for systematic bias in judicial decision-making.

This study extends scholarship on judicial independence in state supreme courts by examining the institutional shift from nonpartisan to partisan judicial elections. Prior research has employed a range of empirical strategies to estimate how selection mechanisms influence dissent rates, which are frequently used as a behavioral proxy for judicial independence [@Canon1970; @HallAndWindett2013; @Renberg2020]. These approaches include manual data collection, automated web scraping using Python, and quasi-experimental techniques such as the synthetic control method (SCM). Despite these advances, dissent rates remain an imperfect measure and are vulnerable to concerns about data completeness, reproducibility, and construct validity. As language modeling techniques advance, computational textual analysis of judicial opinions offers a more complete understanding of judicial behavior than dissent rates alone. By distinguishing evidence-based reasoning from intuition-driven language, this approach provides insight into how institutional design shapes judicial rhetoric. This study therefore evaluates whether partisan and nonpartisan selection mechanisms influence patterns of opinion writing and considers what these differences imply for the measurement of judicial independence in state supreme courts.

## Literature Review

To explore concerns about judicial independence and selection mechanisms, scholars often use dissent rates as a proxy for behavioral independence. A justice’s decision to write a dissent reflects a willingness to challenge the majority opinion, advance alternative legal interpretations, and resist political or institutional pressures [@Renberg2020]. Scholarly research on judicial dissent has identified several factors that influence a justice's opinion-writing behavior on state supreme courts. These include environmental conditions that reflect broader political and social contexts, institutional structures that govern court operations, electoral systems that determine how judges are selected and retained, internal court dynamics that shape collegial relations. Understanding these mechanisms is essential for evaluating how reforms to judicial selection systems affect judicial independence and accountability.

Environmental factors reflecting broader political and social contexts have been found to influence dissent rates. Brace and Hall find that higher urbanization, greater political competition, and increased state spending are all associated with elevated dissent rates [@Brace1990]. Similarly, Epstein, Landes, and Posner show that judges appointed by presidents of different parties exhibit systematically divergent ideological preferences, increasing the likelihood of disagreement on mixed panels, and that dissent becomes more frequent as ideological divisions widen, panel sizes grow, and dissent aversion declines [@Epstein2011]. These findings indicate that courts operating in more heterogeneous and competitive political contexts are more likely to experience higher dissent rates, reflecting the combined effects of structural and ideological pressures on judicial behavior.

Building on the influence of environmental factors, scholars have found that institutional features governing court structures and internal rules have been found to exert an even greater effect on dissent rates. Brace and Hall find that these factors are the primary drivers for dissent, accounting for roughly six times more explanatory power than environmental variables [@Brace1990]. They identify four key institutional features that shape dissent: the method of judicial selection, the presence of intermediate appellate courts, random opinion assignment, and sanctioning rules [@Brace1990]. Intermediate appellate courts increase dissent by filtering routine cases, leaving higher courts to decide more complex and controversial disputes. Random case assignment promotes dissent by limiting the Chief Justice’s ability to reward or punish colleagues through discretionary assignments. Conversely, procedures such as opinion assignment, conference discussion by seniority, and voting in reverse seniority encourage consensus by creating incentives that discourage open disagreement. Similarly, Jaros and Canon show that states with intermediate appellate courts experience higher dissent rates in their supreme courts, with the likelihood of dissent rising as court size increases and judicial terms shorten [@Canon1970].

Beyond formal structures, scholars have examined how internal dynamics shape the extent to which courts generate consensus or permit dissent. Jaros and Canon identify factors that cultivate consensus, including strong task leadership by the Chief Justice, high social integration among members, and a “norm of unanimity” that incentivizes judges to reach a single collective decision [@Canon1970]. Hall and Windett demonstrate that Chief justices frequently prioritize consensus to foster collegiality, reinforce precedent, and bolster public confidence, actively discouraging dissent because it imposes costs on colleagues, risks weakening precedent, generates confusion in the law, encourages future appeals, and can produce dissatisfaction within the court [@HallAndWindett2013]. Some justices, however, resist consensus and issue dissents to preserve individual expression or influence future courts. At the same time, Epstein, Landes, and Posner emphasize that judges may suppress dissent in a phenomenon they term 'dissent aversion' to avoid imposing costs on themselves or colleagues [@Epstein2011]. These competing incentives limit the chief’s capacity to enforce agreement, with Hall and Windett finding that dissent rates are lower on courts where the chief possesses greater formal powers and where members have fewer institutional resources, such as staff, pay, docket control, time, or insulation from electoral pressures [@HallAndWindett2013]. Conversely, abundant member resources encourage dissent by undermining the chief’s authority and reducing the effectiveness of formal powers on resource-rich courts.

Lastly, the method of judicial selection represents one of the most consequential institutional factors shaping dissent rates. Brace and Hall find that judges appointed by governors or legislatures tend to promote consensus, while elected judges are associated with higher dissent rates [@Brace1990]. Jaros and Canon similarly report that popularly elected courts exhibit higher dissent rates than appointed courts [@Canon1970]. Hall and Windett provide a systematic comparison of dissent across four selection systems: gubernatorial or legislative appointment, the Missouri Plan (appointment followed by retention elections), nonpartisan elections, and partisan elections [@HallAndWindett2016]. Courts with appointed judges and Missouri Plan courts exhibit highly stable dissent rates, which the authors attribute to longer judicial tenures, greater professionalization, and insulation from electoral pressures, although cross-state variation is substantial in Missouri Plan states. States with nonpartisan elections display significantly higher dissent rates, roughly four percentage points above Missouri Plan states, suggesting that electoral incentives shape judicial behavior even in the absence of party labels. The most pronounced and unstable patterns appear in states with partisan elections, where dissent rates rise sharply from under 20 percent in the mid-1990s to over 40 percent by the early 2000s, accompanied by dramatic increases in cross-state variation. Hall and Windett conclude that this volatility reflects influences beyond judicial interpretation, including potential pressures related to reelection concerns. Renberg uses a synthetic control approach to analyze the relationship between judicial selection mechanisms and dissent rates, finding that removing partisan labels from voter guides and ballots increases dissenting opinions [@Renberg2020]. This suggests that justices strategically moderate dissent under partisan constraints. Thus, eliminating party identifiers allows justices to signal their legal ideology more freely. However, no studies conducted have analysed the opposite transition using the synthetic controls method (SCM), which the present study aims to do.

While dissent rates provide a quantitative measure of disagreement on the bench, they offer limited insight into the underlying substance of judicial reasoning. Computational textual analysis has emerged as a powerful methodological tool for examining the content of judicial opinions, with recent advances in natural language processing (NLP) enabling systematic analysis of how judges express their ideological positions and respond to external pressures. Bergam, Allaway, and McKeown develop two textual indicators of Supreme Court justice ideology: issue-specific stance (ISS), which evaluates positions relative to representative political topics, and holistic political stance (HPS), which directly classifies political affiliation expressed in language [@Bergam2022]. They find that justices responsive to public opinion exhibit significantly stronger correlations between the ideology expressed in their language and their voting behavior, highlighting the influence of broader socio-political forces on judicial opinion-writing behavior.

However, ISS and HPS may not capture the broader quality of judicial reasoning due to their focus on political ideology. Rather, Lewandowsky introduces the Evidence Minus Intuition (EMI) framework to distinguish between evidence- and intuition-based language [@Lewandowksy2025]. This methodological approach offers substantial promise for research on state supreme courts, as it can be adapted to quantify the extent to which judicial opinions rely on empirical, evidence-based legal reasoning versus normative, abstract, and personal or political rhetoric, providing insight into how selection mechanisms affect judicial independence. Therefore, the present study adapts this EMI methodology by training a Word2Vec model on a corpus of state supreme court opinions to assess how partisan versus nonpartisan judicial selection mechanisms influence the rhetoric in judicial opinions.

Martin-Quinn (MQ) scores, which measure judicial ideology on a liberal-conservative spectrum based on voting records, are primarily developed for U.S. Supreme Court justices, not state supreme court justices. While they are the gold standard for analyzing the federal high court (from 1937 to the present), there is no comprehensive, widely cited Martin-Quinn database that covers state-level supreme courts. Instead, CFScores.

Sudies like those depicted in fi gures 20.1 and 20.7 seek to identify a direct link between the judges’ ideologies and their votes. A landmark study conducted by Sheldon Goldman in 1966 indicated that federal circuit court judges affi liated with the Democratic Party were, relative to Republican judges, far more likely to vote for unions in labor-management disputes and against corporations charged with antitrust violations. But Goldman found no statistically signifi cant differences between Democratic and Republican judges in the areas of criminal law and civil liberties, nor in challenges to government regulations brought by businesses. For example, judges appointed by Lyndon Johnson were no more likely to rule in favor of criminal defendants than judges appointed by Dwight Eisenhower. More recent work by Cass Sunstein and his colleagues (2006) confi rms Goldman’s (mixed) fi ndings. To be sure, their examination of more than 19,000 votes cast by Court of Appeals judges unearthed strong evidence of partisan voting in many areas of the law. In affi rmative action suits, for example, judges appointed by Republican presidents rarely voted to uphold the plan at issue, doing so in less than 50% of disputes. By contrast, Democratic appointees supported the plan in three out of every four cases. Yet in 5 of the 24 areas of the law analyzed, the party of the appointing president was not an especially good predictor of the judge’s vote. In criminal cases, Democratic appointees were no more or less favorable toward defendants than Republican appointees. Likewise, for all but abortion and capital punishment, the judge’s vote was affected not only by his ideology but also by the ideology of the colleagues with whom he sat. All-Democratic panels vote to uphold affi rmative action plans in 81% of the cases, but when a Democratic appointee sits with two Republicans he votes to support the plan only 60% of the time. Likewise, all-Republican panels vote to strike plans in 66% of the cases, but a Republican sitting with two Democrats opposes them in only 30% of the cases. According to Sunstein and his collaborators (2006), both are clear examples of “ideological dampening.”  Extant research also has considered ideological patterns in other choices judges make, such as the decision to overrule a precedent. Perhaps not surprisingly, scholars have shown that conservative justices are more likely to vote to overrule precedents that liberals favor, such as  Roe v. Wade , and liberal justices to overrule conservative precedents, such as  Bowers v. Hardwick  (Hansford & Spriggs, 2006; Brenner & Spaeth, 1995). The justices’ votes to overturn federal, state, and local laws seem equally ideological. Segal and Spaeth (2002) unearthed a consistent pattern in their examination of opinions in which at least one justice stated his desire to strike an act of government. Liberals vote to strike laws that liberal litigants (defendants in criminal cases, women and minorities in civil rights cases, etc.) want struck, while conservatives vote to strike laws that conservative litigants (the government in criminal cases, those opposed to women and minorities in civil rights cases, etc.) want struck. Even accounting for measurement error, though, the fi ndings are likely to remain relatively mixed for courts below the Supreme Court. This should not be altogether surprising. On one hand, we would not expect ideology or partisanship to play absolutely  no  role in judging on the appellate bench. If this were the case, no one would care much whether a Democrat or Republican won the presidency, at least not with regard to judicial selection. Their judicial nominees would be essentially fungible, which the literature tells us is not the case. On the other hand, the lack of ideological voting in some areas is not diffi cult to explain: lower court judges face greater constraints in attempting to etch their ideology into law. Part 1 mentioned the threat of reversal by judicial superiors, but many other constraints exist, including the desire for promotion to a higher judicial offi ce. For ambitious appellate court judges, it may not be in their best interest to ignore organizational norms such as  stare decisis  and decide purely on the basis of their ideology. These analyses may reach similar conclusions, but to some scholars, they suffer from a nontrivial problem: they tend to treat judges as operating within an ideological vacuum of sorts, making decisions without considering the preferences and likely actions of their colleagues. Recognizing that that may be unrealistic for collegial courts, social scientists have turned their attention to how judges serving on the same panel or court may affect one another.  One strand of this research focuses less on the ideology of the individual judges and more on how their ideology works to affect their colleagues. Recall that for most areas of the law they examined, Sunstein and colleagues (2006) found some evidence of ideological dampening, which occurs when a judge sits with two judges who do not share his partisan affi liation. They also found evidence of  ideological amplifi cation , such that judges sitting on homogeneous Democratic or Republican panels tend to be extremely ideological. Sunstein and colleagues (2006) point out that litigants defending affi rmative action programs have a one-in-three chance of prevailing when the panel is full of Republican appointees. The odds increase to four in fi ve when three Democrats sit on the panel. Finding that similar panel effects pervade many other areas of the law, they conclude that the “political party of the presidents who appointed the other two judges on the panel is at least as good a predictor of how individual judges will vote” as the party affi liation of that individual judge’s appointing president (p.10). There are also studies that examine whether judges who must stand for reelection attend to their constituents’ preferences when they make their decisions. Substantial evidence now suggests that they do. 

## Methods

This study adopts a mixed-methods research design that integrates statistical modeling with computational textual analysis to assess the effects of institutional reform on judicial opinion writing. The first component employs the synthetic control method (SCM), originally developed by Alberto Abadie and Javier Gardeazabal and later extended by Abadie, Alexis Diamond, and Jens Hainmueller, to estimate the causal effects of aggregate institutional interventions. [@abadieEconomicCostsConflict2003; @abadieSyntheticControlMethods2010]. The second component employs a computational textual analysis that proceeds in four stages: first, a Word2Vec model trained on preprocessed opinion text generated the vector space for all subsequent analyses; second, the Wordscores method produced initial ideological and non-ideological seed-word dictionaries; third, these dictionaries were expanded and refined using Word2Vec; and fourth, an Evidence Minus Intuition (EMI) framework produced rhetoric scores for each opinion, interpreted in terms of ideological versus non-ideological rhetoric.

### Synthetic Controls Method 

SCM constructs a valid counterfactual by creating a weighted composite of control units, or donor pool, that closely replicate the treated unit’s pre-intervention characteristics. The synthetic control then projects how the treated unit would have evolved had the intervention not occurred. The institutional intervention of interest in the present study is the transition from nonpartisan to partisan judicial elections. The treated unit is the North Carolina Supreme Court, which adopted partisan elections following a statutory reform in 2017 and held its first partisan contest on November 6, 2018. The donor pool consists of seven state supreme courts that have historically maintained nonpartisan judicial elections: Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. Pretreatment covariates from these courts are weighted to construct a synthetic North Carolina Supreme Court, providing a counterfactual trajectory of dissent rates had the reform not occurred. Renberg finds that SCM reliably estimates the causal effects of institutional changes in judicial selection mechanism on opinion-writing behavior [@Renberg2020]. 

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

Each donor court is represented by a vector of pretreatment covariates capturing political, legal, and institutional context, measured annually from 2012 to 2024. Structural features of judicial selection systems, including term length, number of justices, single- versus multimember election districts, and electoral competitiveness, were obtained from Ballotpedia [@StateSupremeCourts]. Campaign finance data, defined as the total funds raised by candidates in the most recent election for each year, were collected from Follow the Money Institute [@HomeFollowTheMoneyorg]. Court professionalization scores were drawn from Squire and Butcher’s updated 2019 index, incorporating staff size, judicial pay, and docket control based on the Court Statistics Project’s classification of mandatory and discretionary jurisdiction [@squireUpdateSquireState2021]; due to their relative stability, 2019 values are assumed unchanged through 2024. Caseload characteristics, including the number of published opinions, capital punishment appeals reviewed, capital cases resolved by lower courts the prior year, and the proportion of the docket devoted to criminal procedure, were obtained from LexisNexis [@LexisNexis]. Court ideological spread was measured using Bonica’s common-space campaign finance scores (CFscores), continuous measures of ideology derived from donation patterns in the 2024 Database on Ideology, Money in Politics, and Elections (DIME)[@DatabaseIdeologyMoney]. Because state-level citizen and government ideology measures from Berry et al. [@Berry1998] are unavailable for 2012–2024, state citizen ideology was approximated using aggregated responses from the 2024 ANES Time Series Study, reporting mean state-level ideological self-placement every four years. State government ideology was operationalized as the average first-dimension NOMINATE score of all congressional members in each state, providing a spatially comparable measure strongly correlated with Berry et al.’s original index [@Berry2010; @Voteview2026].

### Computational Textual Analysis Preprocessing and Word2Vec Training

While the synthetic control analysis investigates potential associations between the shift to partisan elections and dissent rates from 2012–2024, the computational textual analysis examines rhetoric within judicial opinions over a longer period from 1897–2026. This analysis draws on a corpus from the Collaborative Open Legal Data (COLD) Cases dataset, a comprehensive collection of 8.3 million U.S. legal decisions maintained by the Harvard Library Innovation Lab in collaboration with the Free Law Project. The dataset consolidates opinion text, head matter, and substantive metadata from CourtListener’s bulk data into standardized records. This data was further filtered to retain only state supreme court opinions, identified by year and court jurisdiction, and opinion text was extracted from each record. Text was preprocessed using spaCy’s large English language model, including tokenization, lemmatization, lowercasing, removal of non-alphabetic tokens, and exclusion of standard English stopwords. A Word2Vec model was trained on the preprocessed COLD corpus using a skip-gram architecture with 300-dimensional vectors, a context window of five words, and a minimum word frequency of 20. Word2Vec is a neural word embedding model used in natural language processing (NLP) that learns vector representations by predicting surrounding context words, placing words that occur in similar contexts near one another in the vector space. As a result, Word2Vec captures semantic relationships beyond the capabilities of bag-of-words approaches. The trained Word2Vec model provides the vector space for all downstream analyses.

### Wordscores

To identify seed-words representing ideological and non-ideological judicial rhetoric, the Wordscores method was applied to the preprocessed opinion corpus. Originally developed to estimate the policy positions of political party manifestos, Wordscores is a supervised text-scaling procedure that requires reference texts with known positions on a dimension of interest, constructs a word–document frequency matrix, and calculates word scores based on the association between words and reference positions.

Because Wordscores is a supervised method, it was anchored using justices' CFscores from DIME. CFscores estimate ideological position based on campaign finance networks, including contributions received, contributions made, and the ideology of the appointing authority where relevant. Negative CFscores indicate more liberal ideological alignment and positive CFscores indicate more conservative alignment. Justices with extreme CFscores tend to attract support from ideologically-aligned donors, whereas those with scores near zero receive fewer contributions and from far more ideologically diffuse sources. Prior scholarship validates CFscores as anchors for text scaling, as Taddy and colleagues computed Text Partisan Scores (TPS) from legislators' public rhetoric and found these correlate with CFscores at r = 0.92. Although this validation was conducted using legislative texts, anchoring judicial rhetoric to donation-based ideological measures provides a theoretically grounded mechanism for detecting the imprint of partisan influence on judicial language. This study does not claim to analyse the relationship between donor ideology and judicial language; rather, the documented correspondence between CFscores and rhetorical positioning justifies their use as anchors for systematic measurement. Because CFscore coverage spans 1979–2024, seed-word dictionary construction was restricted to opinions authored during this period, with the resulting dictionaries subsequently expanded and applied to the full historical corpus.

Two reference corpora were constructed. The first consisted of opinions authored by justices in the most ideologically extreme quartile of the sample, and the second consisted of opinions authored by justices in the least ideologically extreme quartile. Word scores were computed separately for each reference group as the frequency-weighted average of the absolute CFscores of the reference texts in which each word appeared:
$$W_w = \frac{\sum_{d \in R} f_{wd} \cdot |s_d|}{\sum_{d \in R} f_{wd}}$$
where $W_w$ is the score for word $w$, $R$ is the set of reference texts, $f_{wd}$ is the TF-IDF weighted frequency of word $w$ in document $d$, and $|s_d|$ is the absolute CFscore of the authoring justice. A shared vocabulary of up to 500 terms was constructed across both reference groups, filtered to words appearing in at least 10 documents and containing at least three characters, with standard English stopwords removed. Words were then ranked by the difference between their ideological group score and their non-ideological group score. Words with high difference scores appeared disproportionately in opinions from ideologically extreme justices and were treated as candidates for the ideological rhetoric seed dictionary; words with low or negative difference scores appeared disproportionately in opinions from non-ideological justices and were treated as candidates for the non-ideological rhetoric seed dictionary. The resulting ranked vocabulary was reviewed manually to exclude terms ambiguous in legal context before the two seed dictionaries were finalized.

### Rhetoric Scores

Rhetoric scores were operationalized following the Evidence Minus Intuition (EMI) method, originally developed by Taddy, Gentzkow, and Shapiro to quantify the extent to which congressional speeches employed partisan versus moderate language. For each opinion, all tokens that matched the Word2Vec vocabulary learned during model training were used to construct a document vector by averaging their embeddings. Concept vectors representing ideological and non-ideological rhetoric were then constructed by averaging the embeddings of all words in the opinion that appeared in the respective expanded dictionaries. Cosine similarity between the document vector and each concept vector yielded an ideological rhetoric score and a non-ideological rhetoric score for each opinion. To account for variation in opinion length, opinions were grouped into deciles based on token count. Within each decile, the mean score was subtracted from each opinion and divided by the decile standard deviation to produce a Z-score. This prevented longer or shorter texts from artificially inflating or deflating rhetoric scores. Length-adjusted scores were averaged across multiple opinions in cases with more than one opinion. The final rhetoric score was calculated by subtracting the ideological score from the non-ideological score, such that positive values indicate greater prevalence of non-ideological rhetoric and negative values indicate greater prevalence of ideological rhetoric.

## Analysis

The synthetic control analysis follows Renberg's methodological approach but arrives at a different conclusion. While Renberg finds that moving from partisan to nonpartisan elections encourages dissent, the results of this study suggest no detectable impact of judicial electoral reform on dissenting opinion rates in the North Carolina Supreme Court. Complete data for all variables and courts analyzed in this study are available in the replication code.

### Data Quality and Reproducability

Before presenting the results, two preliminary issues bear on the credibility of the analysis: the reproducibility of prior findings and the quality of available data. Rather than presenting numerical data and explicitly reporting baseline dissent rates, Renberg relies on graphical depictions with unclear measurement conventions. Moreover, in Figure 1, the y-axis is labeled "Percent of Opinions," yet the scale displays decimal values ranging from 0.05 to 0.25. This formatting creates uncertainty as to whether the values represent proportions (e.g., 0.15 = 15%) or percentages (0.15%). If interpreted as proportions, the implied dissent rates range from approximately 14–19% on the Arkansas Supreme Court (1997–2012), 5–22% on the Tennessee Supreme Court (1985–2002), and 8–46% on the Mississippi Supreme Court (1986–2000). Multiple strategies were implemented attempting to replicate these implied rates using CourtListener and LexisNexis. In CourtListener, searches were restricted by court and refined using advanced opinion-type operators, including combined-opinion, unanimous-opinion, lead-opinion, plurality-opinion, concurrence-opinion, in-part-opinion, dissent, addendum, remittitur, rehearing, on-the-merits, and on-motion-to-strike. Searches in LexisNexis employed the OpinionBy and DissentBy fields as well as the "find by source" function. Across databases and search configurations, the resulting dissent rate estimates did not approximate the figures implied by Renberg's graphs.

Replication efforts also followed the approach outlined in Hall and Windett's 2013 study [@HallAndWindett2013]. Table \ref{tab:opinions_dissents} reports three sets of dissent rate estimates generated using distinct LexisNexis query strategies. The first set shows the values reported in the original published table. The second set was constructed using LexisNexis's OpinionBy and DissentBy fields, querying the names of all justices serving on each court between 1995 and 2010. The third set reflects a more restrictive operationalization. Because Hall and Windett state that their analysis focuses on "the subset of data most likely to interest judicial politics scholars: those cases in which a state supreme court rendered a final judgment with a full written opinion," this query excluded entries containing terms such as "dismiss!," "petition for review," and "motion for," using AND NOT operators to narrow the dataset to decisions more likely to constitute full merits opinions. Despite implementing these strategies, the resulting dissent rates did not replicate those reported by Hall and Windett. Moreover, the variation across query constructions is nontrivial. In jurisdictions such as Oregon and West Virginia, estimated dissent rates shift substantially depending on the search logic employed. This sensitivity to query design across the literature suggests that dissent rate estimates are highly contingent on operational definitions and database filtering decisions. Absent precise documentation of coding rules, inclusion criteria, and database parameters, the reported baseline dissent rates cannot be independently verified.

\begin{table}[htbp]
\centering
\caption{Comparison of Dissent Rate Measurement Methods Across Courts (1995-2010)}
\label{tab:opinions_dissents}
\begin{sideways}
\small
\begin{tabular}{l*{9}{r}}
& \multicolumn{3}{c}{\textbf{Hall \& Windett (2013)}} & \multicolumn{3}{c}{\textbf{OpinionBy \& DissentBy}} & \multicolumn{3}{c}{\textbf{AND NOT Method}} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10}
\textbf{Court} & Opinions & Dissents & Rate & Opinions & Dissents & Rate & Opinions & Dissents & Rate \\
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
\end{tabular}
\end{sideways}
\end{table}

Data availability further constrains replication efforts. The State Supreme Court Data Project, widely regarded as the principal archival resource for state supreme court research, covers only four years between 1995 and 1998 [@StateSupremeCourtProject]. Hall and Windett introduced a dataset described as publicly available, yet the data are not accessible and the associated Python code relies on web scraping practices prohibited by LexisNexis's terms of service [@HallAndWindett2013]. Although LexisNexis provides relatively comprehensive coverage of published opinions, its proprietary structure limits transparency and reproducibility for researchers without bulk-access subscriptions, while CourtListener offers substantially less complete coverage. The FAIR principles digital access guidelines emphasize that scientific data should be findable, accessible, interoperable, and reusable through persistent identifiers, standardized retrieval protocols, shared formats, and clear documentation of provenance and licensing [@wilkinsonFAIRGuidingPrinciples2016]. Neither Hall and Windett's nor Renberg's datasets and replication code meet these standards, preventing independent verification and limiting cumulative knowledge in the study of judicial opinion writing and dissent rates.

### Data Preparation

North Carolina's dissent rate remained consistently low from 2012 to 2017, never exceeding 1%. The rate increased notably in 2018 to 1.9% and reached 4.5% in 2020. Coinciding with periodic court closures across the United States related to the onset of the COVID-19 pandemic, dissent rates declined to 2.2% in 2021. Subsequently, the rate rose to a recorded maximum of 5.6% in 2022 before declining to approximately 3.1% by 2023 and 2024. In contrast, other courts in the sample exhibited more variable patterns. Wisconsin consistently maintained the highest dissent rates throughout the period, with rates frequently exceeding 50% and reaching 88% in 2016. This could be due to a high volume of cases with unpublished opinions not captured in the data collection process, resulting in an artificially inflated dissent rate when calculated against only published opinions. Arkansas also showed considerable volatility, with dissent rates ranging from 7.7% in 2012 to peaks above 50% in 2018-2020. States such as Georgia and Minnesota maintained relatively stable and low dissent rates throughout the observation period, typically remaining below 10%.

![Dissent Rates in North Carolina Supreme Court](/Users/alexnagy/Coding/dissention/reports/figures/nc_dissent_rate.png)

### Results

The synthetic control method constructs a counterfactual North Carolina Supreme Court using only the supreme court of Minnesota, which receives 100% of the weight, to match North Carolina's pretreatment characteristics. All other donor courts are assigned zero weight, indicating that the supreme court of Minnesota is the closest match to the supreme court of North Carolina. The estimated treatment effect on dissents is 0.000%, showing no detectable change in dissenting behavior after North Carolina adopted partisan elections in 2018.

![Estimated impact of judicial reform on dissenting behavior](/Users/alexnagy/Coding/dissention/reports/figures/scm.png)

### Model Fit and Parallel Trends Assumption

Mean Squared Prediction Error (MSPE) measures the average squared difference between the treated unit's actual outcome and the synthetic control's predicted outcome. SCM rests on the parallel trends assumption that the treated and synthetic units would have continued on the same trajectory absent treatment. The pretreatment MSPE from 2012–2017 is 0.0007, indicating that Minnesota's dissent trajectory closely tracked North Carolina's before treatment. The post-treatment MSPE from 2018–2024 is 0.0002, representing a substantial decrease. The post-to-pre ratio of 0.29 indicates that the synthetic control's predictive ability actually improved after 2018. This improvement in post-treatment fit suggests that changes occurring in North Carolina following electoral reform also occurred in Minnesota, yielding a near-zero treatment effect estimate.

### Pretreatment Covariate Balance

Pretreatment covariate balance is essential for establishing the validity and robustness of the counterfactual because it determines whether the synthetic control unit credibly represents the counterfactual outcome for the treated unit. The fundamental logic of SCM rests on the assumption that, if a weighted combination of control units closely matches the treated unit on observable characteristics prior to treatment, it will also approximate how the treated unit would have behaved in the absence of treatment.

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
Court Professionalization (2019) & 0.609 & 0.610 & 0.612 \\
Capital Appeals         & 0.167 & 0.333 & 2.548 \\
Lower Court Capital Appeals (Lag 1) & 1.000 & 0.500 & 1.548 \\
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
\end{tabular}%
}
\end{table}

The synthetic control achieves near-perfect balance on court professionalization (0.610 vs. 0.609) and exactly matches both the number of justices and the election structure. Term length shows reasonable balance, differing by only two years. However, substantial imbalances persist on key covariates. Campaign finance exhibits a 660% difference (1.35 million vs. 177,336), criminal procedure dockets diverge markedly (0.458 vs. 0.129), and capital appeals also differ notably (0.167 vs. 0.333). Most critically, electoral competition demonstrates complete imbalance: North Carolina's value of 0.667 reflects highly competitive elections, whereas Minnesota's 0.000 indicates no competitive elections during the study period. This discrepancy directly undermines the theoretical mechanism under investigation, as competitive elections are hypothesized to drive dissenting behavior. Standardized difference calculations further highlight these issues: 11 of 14 covariates exhibit imbalances exceeding the 0.25 threshold. The most severe imbalances occur in published opinions (3.59 SD), campaign finance (2.12 SD), ideological spread (1.59 SD), electoral competitiveness (1.33 SD), dissent rate (-0.78 SD), and capital appeals (-0.67 SD). Only three covariates can be considered balanced: lagged lower court capital appeals (-0.18 SD), citizen ideology (-0.09 SD), and court professionalization (-0.03 SD).

### Sensitivity Analysis

A robust causal estimate should remain stable across reasonable variations in model specification. Conducted by systematically excluding each donor court one at a time and recalculating the treatment effect, the leave-one-out analysis reveals severe instability that undermines confidence in the estimate. Excluding each potential donor produces treatment effects ranging from -0.1887 (Minnesota excluded) to -0.0875 (Wisconsin excluded), with a mean of -0.1617 and standard deviation of 0.0382. Every leave-one-out specification produces a negative treatment effect, yet the optimal weighted combination yields exactly zero. This pattern indicates that the zero treatment effect is an artifact of the specific weighting scheme rather than a robust finding. Several additional robustness checks illuminate the fragility of causal inference in this setting. Comparing optimal synthetic control weights to equal weights reveals no difference; both produce an estimated average treatment effect (ATE) of 0.00, indicating that the sophisticated weighting algorithm provides no advantage over a simple average of control courts. Placebo tests applying SCM to pre-treatment years (2014, 2015, 2016, 2017) as if each were the treatment year reveal systematic differences between North Carolina and its synthetic version, with estimated placebo effects ranging from -2.62 to -3.78%, averaging -2.92%. The actual 2018 treatment effect of 0.00% differs significantly from these pre-treatment placebo effects (p = 0.042), suggesting a possible discontinuity in 2018, though this should be interpreted with caution given low baseline dissent rates and small absolute magnitudes. Year-by-year treatment effects further reflect this instability, ranging from -0.015 to +0.027 with a standard deviation of 0.0152, nearly as large as the effects themselves.

### Limitations

The covariate imbalances and sensitivity analysis results collectively raise fundamental questions about whether the synthetic control adequately captures the institutional factors shaping judicial opinion-writing in North Carolina. The analysis cannot overcome the absence of a suitable counterfactual court that simultaneously reflects North Carolina's competitive elections, campaign finance environment, ideological composition, and caseload characteristics.
The importance of covariate balance becomes clearer when comparing the imbalances in Renberg's analysis with those in the present study. In Renberg's analysis, structural and institutional covariates are generally well-balanced, with minimal differences in term length, closely matched single-member election districts, near-identical professionalization scores, and reasonably aligned ideological measures. However, substantial imbalances emerge in operational and caseload variables. Synthetic controls overestimate published opinions by 92–494%, producing two to six times more opinions than the treated courts. Criminal procedure dockets are underestimated by approximately 50% in Arkansas and Mississippi, and capital punishment caseloads diverge sharply. Because these variables directly reflect judicial workload and case composition, such imbalances undermine the validity of Renberg's synthetic controls, a point not addressed at length in her paper.

The algorithm's reliance on Minnesota as the sole donor court further compounds this concern. Minnesota is merely the least unsuitable option among courts that are otherwise incomparable. While the pretreatment MSPE of 0.0007 may suggest a close fit, it obscures the reality that no available donor court adequately reflects North Carolina's institutional characteristics. By assigning full weight to a single court, the algorithm abandons the method's core advantage of combining multiple control units to construct a robust counterfactual. This comparability problem likely stems from structural features that distinguish North Carolina's judicial system. Unlike most states, North Carolina's Supreme Court exercises both mandatory and discretionary jurisdiction over certain cases that bypass the Court of Appeals entirely, and the state constitution grants direct appellate jurisdiction over constitutional questions, decisions striking down state statutes, and other matters of substantial public importance. This bifurcated structure may inflate North Carolina's published opinion volume; the court produced 1,057 opinions annually during the pretreatment period, compared to Minnesota's 657 and a sample mean of 224, yielding a standardized difference of 3.59 standard deviations. COVID-19 disruptions beginning in 2020, including court closures, delayed proceedings, and shifts in case composition, may also have introduced temporal shocks that affect the analysis independently of electoral reform. These findings raise broader concerns about the application of SCM to judicial opinion-writing behavior in state supreme courts, where institutional characteristics vary so widely across states that they may routinely violate SCM assumptions.

### Textual Analysis

Because SCM findings suggest that dissent rates may not constitute an adequate proxy for either judicial independence or the behavioral effects of electoral institutions, and that the synthetic control method is ill-suited for modeling Supreme Court opinion-writing given the substantial institutional variation across courts. Moreover, dissent rates alone offer limited insight into how electoral reform shapes judicial behavior, as the prevalence of dissent merely captures whether justices disagree with the majority, rather than the depth, substance, or reasoning underlying those disagreements. A more promising approach lies in examining the full text of judicial opinions to assess how electoral reform influences the political tenor and substantive content of judicial reasoning. This textual analysis can reveal whether justices elected in partisan systems are more likely to invoke partisan considerations in their written justifications.

### Wordscores and Word2Vec

The seed-words and expanded dictionaries for each construct: (Table \ref{tab:emi_dictionaries}).

\begin{table}[htbp]
\caption{Expanded Evidence and Intuition Dictionaries}
\label{tab:emi_dictionaries}
\centering
\small
\begin{tabular}{ll}
\toprule
\textbf{Evidence-Based Dictionary} & \textbf{Intuition-Based Dictionary} \\
\midrule
\multicolumn{2}{l}{\textit{Seed-words:}} \\
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

\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{/Users/alexnagy/Coding/dissention/reports/figures/semantic_corner_plot.png}
\caption{Semantic Space Around "Evidence"}
\label{fig:evidence_semantic}
\end{figure}

Figure \ref{fig:evidence_semantic} visualizes the 30 words most semantically similar to "evidence" in the Word2Vec model, projected into two-dimensional space using Principal Component Analysis (PCA). The semantic cluster reveals that "evidence" associates primarily with technical legal terminology related to evidentiary procedures ("admissible," "testimony," "witness"), factual determination ("fact," "prove," "show"), and evidence quality ("probative," "credible," "corroborative"). The inset map (top right) situates this semantic cluster within the full embedding space of all words in the model, demonstrating that the model successfully captures the technical legal context in which evidence-based language appears in judicial opinions. This clustering pattern validates the model's ability to distinguish evidence-based reasoning from other forms of judicial discourse.

### Rhetoric Scores



### Discussion of Rhetoric Scores



## Conclusion

Synthetic controls results indicate no significant change in dissent following the partisan reform; however, extensive replication and robustness checks reveal substantial measurement and reproducibility challenges. These instabilities suggest that institutional heterogeneity across state courts undermines the credibility of causal inference based on dissent frequency alone, calling into question its use as a proxy for judicial independence in prior scholarship. Preliminary textual analyses indicate that examining the use of evidence- versus intuitionbased language in judicial opinions provides a more robust measure of judicial independence in opinion-writing across selection mechanisms. Overall, the study highlights the methodological limits of existing approaches and advances an alternative framework for assessing how state supreme court selection mechanisms shape judicial opinion-writing behavior.

\newpage

## References
\begingroup
\setstretch{1}