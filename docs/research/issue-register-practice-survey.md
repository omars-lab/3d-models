<!--
  Provenance: adversarial web-research report, produced 2026-07-30 by a
  background research agent (general-purpose, WebSearch + WebFetch).
  Feeds: docs/issue-register-evaluation.md §4.
  Preserved close to verbatim per .claude/skills/ground-design-doc/SKILL.md §3
  ("preserve the report"). The agent's own fidelity note is kept as its first
  section rather than being summarised away.
  Mandate given to the agent included: "Be adversarial — a report that only
  supports building it is a failed report."
-->

# Durable failure/issue registers, executable guards, and agent instruction files

## Fidelity note (from the research agent)

Every URL below was actually fetched. Quoted wording came back through a
summarizing fetch layer, so treat quotes as accurate-in-substance and verify
exact wording before republishing them verbatim elsewhere. Four intended sources
could not be retrieved and are **not** cited as evidence: Etsy/`codeascraft`
"Blameless PostMortems" (403/404), HBR "Why Organizations Don't Learn"
(paywalled stub), a PMI lessons-learned paper (403), and Bugzilla resolution
definitions (not present in the fetched page). WebSearch budget was exhausted
early, so source discovery was by known canonical URL plus link-following from
the Adaptive Capacity Labs index.

---

## Q1. Do durable failure registers work, and when do they decay into write-only archives?

**Headline:** the literature is consistent and blunt — a register's value is
proportional to whether it is *re-read and cited*, not whether it is *written*.
Every primary source names the same decay path: writing is cheap, review is
expensive, so review is what gets dropped first; once reports go unread the
quality drops, which makes them even less read. The documented preconditions for
success are almost all *social* (reviewers, audience, incentives, psychological
safety), not structural.

- [Google SRE Book — Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/)
  — the decisive precondition, stated as a rule: **"An unreviewed postmortem
  might as well never have existed."** Postmortem criteria must be defined
  *before* an incident ("so that everyone knows when a postmortem is
  necessary"), and the practice is sustained by explicit reward structures —
  peer bonuses, public recognition, leadership participation. Failure mode
  named: "If a culture of finger pointing and shaming... prevails, people will
  not bring issues to light."
- [Google SRE Workbook — Postmortem Culture: Beyond Blame](https://sre.google/workbook/postmortem-culture/)
  — **"To our users, a postmortem without subsequent action is
  indistinguishable from no postmortem."** On distribution: "The value of a
  postmortem is proportional to the learning it creates. The more people that
  can learn from past incidents, the less likely they are to be repeated."
  Named decay signals: action items "taking too long to close," "feature
  velocity trumping reliability fixes," people "disengaging from the postmortem
  process."
- [Adaptive Capacity Labs — What Progress In Learning From Incidents Actually Looks Like (Allspaw, 2025)](https://www.adaptivecapacitylabs.com/2025/02/28/what-progress-in-learning-from-incidents-actually-looks-like/)
  — the clearest statement of the death spiral: **"People don't read them
  because they're terrible. And why are they terrible? Because people don't put
  a lot of effort into them. People don't put a lot of effort into them because
  they don't think anybody's going to get anything out of it."** Rejects
  register-count metrics outright: "An absence of incidents is not evidence that
  learning is happening" / "The presence of incidents is not evidence that
  learning is not happening."
- [Adaptive Capacity Labs — Markers of Progress in Incident Analysis (Allspaw, 2019)](https://www.adaptivecapacitylabs.com/2019/11/20/markers-of-progress-incident-analysis/)
  — the concrete success test is *readership over time*: "The number of unique
  readers of post-incident analysis write-ups will grow over time," with
  documents getting fresh views months later carrying "comments, replies,
  highlights, tags"; and **"Explicit references to specific incident analysis
  documents will appear more frequently in company internal documents"** —
  roadmaps, runbooks, onboarding. This is the operational definition of "not
  write-only".
- [Adaptive Capacity Labs — Some Observations On the Messy Realities of Incident Reviews (Richard Cook, 2019)](https://www.adaptivecapacitylabs.com/2019/06/17/some-observations-on-the-messy-realities-of-incident-reviews/)
  — names the *mechanism* of decay: the organizational demand is "the reduction
  of an incident to a manageable discrete list of things to be done," which
  turns reviews into **"pallid, vapid, mechanical exercises"** producing "a
  defensible argument that management is occurring" rather than learning. Repair
  takes "at minimum something like a year of consistent and deliberate
  engagements."
- [GAO-02-195 — NASA: Better Mechanisms Needed for Sharing Lessons Learned](https://www.gao.gov/products/gao-02-195)
  — the canonical "lessons-learned database that isn't read" finding, from an
  audit body rather than a vendor: **"lessons are not routinely identified,
  collected, or shared by programs and project managers,"** and "there is no
  assurance that lessons are being applied toward future missions success."
  Barriers: "lack of time to capture or submit lessons" and "perception of
  intolerance for mistakes." Recommended fixes were mostly social: a named
  owner, linking sharing to "performance evaluations and awards", better
  *search*, and "mentoring and 'storytelling'".
- [Adaptive Capacity Labs — How Learning is Different Than Fixing (Allspaw, 2020)](https://www.adaptivecapacitylabs.com/2020/05/06/how-learning-is-different-than-fixing/)
  — argues the ROI ordering runs opposite to most register designs: focusing on
  "developing a richer understanding of the event" rather than "simply...
  identifying *fixes*" yields "a much greater ROI", and better fixes follow from
  understanding rather than the reverse.
- [The Infinite Hows (Allspaw, kitchensoap)](https://www.kitchensoap.com/2014/11/14/the-infinite-hows/)
  — why cause-shaped entries fail as durable knowledge: "why" questions lock you
  "into a causal chain, which is not how the world actually works", and easily
  answer "who?" instead. Replacement: "describing multiple conditions that allow
  an event to take place."
- [Understanding Incidents: Three Analytical Traps (Allspaw, 2021)](https://www.adaptivecapacitylabs.com/2021/01/11/understanding-incidents-three-analytical-traps/)
  — three named ways a written record becomes worthless even when it exists:
  counterfactual reasoning, normative language ("mismanaged", "insufficient"),
  and mechanistic reasoning (humans as broken parts). Usable as an entry-quality
  rubric.
- [Howie: The Post-Incident Guide (PagerDuty, formerly Jeli)](https://howie-guide.pagerduty.com/)
  — the industry has "over-indexed in the 'error reduction' part of the equation
  by emphasizing incident metrics like mean time to respond and not much on
  generating insights." *(Landing page only was fetched; no claim is made about
  the guide's deeper chapters.)*
- [Google SRE Book — Tracking Outages (Escalator/Outalator)](https://sre.google/sre-book/tracking-outages/)
  — the one source describing an actual *register* rather than a report. Built
  because postmortems miss "issues that have individually small impact but are
  frequent and widespread." Value comes from aggregation and *scheduled*
  re-reading ("report mode" in weekly production reviews), and from letting
  teams invent their own tags — "avoiding a predetermined list and allowing
  teams to find their own preferences" produced "a more useful tool and better
  data." **Note the justification is volume**; the argument does not transfer to
  a low-volume project.

**Extracted preconditions.** (1) a named reader other than the author; (2) a
*scheduled* re-read event, not ad-hoc recall; (3) retrieval that works at the
moment of need; (4) evidence of citation from forward-looking artifacts; (5)
entry-quality standards resisting counterfactual/normative prose; (6) an
incentive attached to writing well. Absent (1) and (2), all sources predict
decay.

---

## Q2. Is "must produce an executable guard, or close as a one-off" recognised practice?

**Headline:** the *regression-test-per-bug* half is thoroughly established and is
stated as a hard requirement in real project policies. The *classification* half
is much weaker: the classification standards claim only "insight", explicitly do
not prescribe outcomes, and one has been formally withdrawn.

- [Martin Fowler — Self Testing Code](https://martinfowler.com/bliki/SelfTestingCode.html)
  — **"The usual reaction of a team using self-testing code is to first write a
  test that exposes the bug, and only then to try to fix it."** Each bug
  indicates a gap in test coverage — evidence about the *guard set*, not just
  the code.
- [Django — Submitting patches](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/submitting-patches/)
  — a real enforced policy: **"A good fix should also include a regression test
  to validate the behavior that has been fixed and to prevent the problem from
  arising again,"** with the review checklist item "Is there a proper regression
  test (the test should fail before the fix is applied)?" and a "Needs tests"
  ticket flag. Note the *fails-first* requirement — the guard must be
  demonstrated to catch the thing.
- [Software Engineering at Google — Ch. 11, Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html)
  — narrower than the folklore: **"As soon as an exploratory test discovers an
  issue, an automated test should be added to prevent future regressions,"**
  plus "A test written once continues to pay dividends... through the lifetime
  of the project." No blanket "every bug gets a test" mandate was found in this
  chapter — the principle is there, the absolute rule is not.
- [Google SRE Workbook — Postmortem Culture](https://sre.google/workbook/postmortem-culture/)
  — the closest thing to "guard or it didn't happen": **"all postmortems which
  follow a user-affecting outage must have at least one P[01] bug associated
  with them,"** and action items require "a single point of contact", a
  priority, and **"a verifiable end state"** with measurable success criteria.
- [Orthogonal Defect Classification (Chillarege)](http://chillarege.com/odc/)
  — ODC is "a particular method of categorization that has properties of
  measurement." Claimed output is diagnostic — "an objective, dispassionate
  insight on the process", identification of "process characteristics and
  oversights", a common language across departments. It does not claim that
  classifying an entry changes any outcome by itself.
- [IEEE 1044-2009 — Standard Classification for Software Anomalies](https://standards.ieee.org/standard/1044-2009.html)
  — provides "a uniform approach to the classification of software anomalies",
  but **"does not prescribe specific procedural or format requirements."**
  Adversarially important: the standard is listed **"Inactive-Reserved"**
  (inactivated 5 March 2020).

**Net:** "the fix ships with a test that fails before and passes after" is
well-supported with enforcement precedent. "The entry gets a classification" is
supported only as a *measurement* practice for organisations with enough volume
to see statistical patterns — and its two flagship schemes claim insight, not
behaviour change.

---

## Q3. ADRs vs. failure records — is there a paired backward-looking record?

**Headline: no.** There is no established backward-looking counterpart to the
ADR. The ADR canon documents *forward* decisions only; the backward-looking
artifact in industry is the postmortem, which lives in a separate tradition with
different authors, formats and review rituals, and is nowhere described as an
ADR sibling.

- [Michael Nygard — Documenting Architecture Decisions (2011)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  — the original. Structure: Title / Context / Decision / Status / Consequences
  ("All consequences should be listed here, not just the 'positive' ones"). Two
  load-bearing lines: **"Large documents are never kept up to date. Small,
  modular documents have at least a chance at being updated,"** and **"Nobody
  ever reads large documents, either."** Plus supersede-don't-delete.
- [adr.github.io](https://adr.github.io/) — an ADR captures "a single AD and its
  rationale", scoped to Architecturally Significant Requirements. The only
  generalisation named is *sideways* — "any decision record" — not backward.
- [joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)
  — the largest variant catalogue: ADR, Architecture Decision Log, Important
  Technical Decisions, IBIS, QOC, DRL, Decision Reasoning Format. **No
  postmortem, incident, defect or failure record variant appears paired with
  ADRs.**
- [ThoughtWorks Technology Radar — Lightweight Architecture Decision Records](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
  — Ring: **Adopt**. "We recommend storing these details in source control,
  instead of a wiki or website, as then they can provide a record that remains
  in sync with the code itself."

**Implication.** A "dated decision ledger + issue register" pairing would be a
local invention rather than adoption of a pattern. Not automatically wrong, but
it removes "this is standard practice" from the argument, and the design gets no
free templates, tooling, or review norms.

---

## Q4. Failure modes of AI-agent working-memory files and reminder hooks

**Headline:** best-documented question of the five, and the guidance is
explicitly *against* accumulation. Anthropic's own docs state that added
instructions have a negative marginal effect past a point, give a hard size
target, and say the correct destination for "must happen every time" rules is a
**hook**, not another instruction file.

- [Claude Code — Best practices](https://code.claude.com/docs/en/best-practices)
  — **"Bloated CLAUDE.md files cause Claude to ignore your actual
  instructions!"** The per-line test: *"Would removing this cause Claude to make
  mistakes?" If not, cut it.* The diagnostic: **"If Claude keeps doing something
  you don't want despite having a rule against it, the file is probably too long
  and the rule is getting lost."** Named failure pattern — "The over-specified
  CLAUDE.md… Fix: Ruthlessly prune. **If Claude already does something correctly
  without the instruction, delete it or convert it to a hook.**" And: "Unlike
  CLAUDE.md instructions which are advisory, hooks are deterministic and
  guarantee the action happens."
- [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory)
  — **"target under 200 lines per CLAUDE.md file. Longer files consume more
  context and reduce adherence."** On conflicts: **"if two rules contradict each
  other, Claude may pick one arbitrarily"**. On enforcement: "Claude treats them
  as context, not enforced configuration. To block an action regardless of what
  Claude decides, use a PreToolUse hook instead." Auto-memory truncates hard —
  only the first 200 lines or 25 KB of `MEMORY.md` load — with explicit guidance
  to "keep one line per entry, move detail into topic files, and **merge or drop
  stale entries**." Directly relevant to a monotonically growing register.
- [Claude Code — Skills](https://code.claude.com/docs/en/skills)
  — skill *descriptions* are always in context and truncated: "the combined
  `description` and `when_to_use` text is truncated at 1,536 characters in the
  skill listing to reduce context usage." Once invoked, a skill's content "stays
  in context across turns, so **every line is a recurring token cost.**" On
  selection failure: "If a skill seems to stop influencing behavior after the
  first response, the content is usually still present and **the model is
  choosing other tools or approaches**" — remedies are a stronger description or
  "use hooks to enforce behavior deterministically."
- [Anthropic Engineering — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  — **"Context, therefore, must be treated as a finite resource with diminishing
  marginal returns... LLMs have an 'attention budget'."** Goal is "the smallest
  possible set of high-signal tokens". Explicitly against edge-case
  accumulation: prefer "a set of diverse, canonical examples" over stuffing
  cases into prompts. Names "context rot".
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172)
  — independent academic grounding: "performance can degrade significantly when
  changing the position of relevant information"; models do best when key
  content is at the beginning or end and degrade on retrieval from the middle —
  "a limitation that persists even in models specifically designed for extended
  contexts."

---

## Q5. Sampling, triage, expiry, and "close as one-off"

**Headline:** sources converge on analysing *fewer things more deeply*, defining
the trigger threshold in advance, and expecting the register itself to need
pruning. "Close as one-off" as a named disposition is **not** directly attested
in the sources successfully fetched; the adjacent, better-sourced idea is to
define in advance what does *not* cross the threshold, so most events never
become entries.

- [Google SRE Book — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
  — pre-declared triggers are the sampling mechanism: user-visible degradation
  past a threshold, any data loss, on-call intervention, resolution time over a
  limit, monitoring failure. "It is important to define postmortem criteria
  **before** an incident occurs."
- [Adaptive Capacity Labs — What's an incident? (Allspaw, 2025)](https://www.adaptivecapacitylabs.com/2025/08/26/whats-an-incident/)
  — the cost of crossing the threshold is the point: **"Declaring an incident
  would bring additional resources to bear, generate auditable documentary
  trails, and involve substantial future work."**
- [Cook — Messy Realities of Incident Reviews](https://www.adaptivecapacitylabs.com/2019/06/17/some-observations-on-the-messy-realities-of-incident-reviews/)
  — the highest-yield unit of analysis is not the individual entry: "groups of
  incidents can be compared and contrasted in order to extract themes and
  opportunities that are only dimly seen in the individual incident," yet "we
  seldom find any such activity present in organizations."
- [Google SRE Book — Tracking Outages](https://sre.google/sre-book/tracking-outages/)
  — a register earns its keep on *volume*: many small, frequent,
  individually-sub-postmortem events, reviewed on a fixed cadence, with
  organically-grown tags.
- [Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  — size discipline as a first-class design constraint; supersede rather than
  delete.
- [Claude Code — Memory](https://code.claude.com/docs/en/memory)
  — the only source giving an explicit *expiry* instruction, enforced by a hard
  200-line / 25 KB truncation.
- [GAO-02-195](https://www.gao.gov/products/gao-02-195)
  — among NASA's remedies was improving the Lessons Learned Information System's
  **search**. Capture cost was never the binding constraint; retrieval and
  incentive were.

---

## What this implies for the decision

Criteria a proposed register + skill would have to meet, each traceable above:

1. **It must name a scheduled re-read event, not just a write path.** Google
   SRE: *"An unreviewed postmortem might as well never have existed."* Without a
   recurring moment where entries are read as a set, every source predicts a
   write-only archive. **This is the hardest criterion for a solo project.**
2. **Success is measured by citation/read-back, not entry count.** Allspaw's
   markers are unique readers growing over time and explicit references
   appearing in forward-looking documents; he explicitly rejects incident counts
   as evidence of learning.
3. **The durable artifact must be the guard, not the prose.** Fowler and Django
   establish the executable-guard norm with a fails-before-the-fix proof; the
   SRE Workbook adds "a verifiable end state." A wired test protects behaviour
   without anyone re-reading anything — the only mechanism here that survives
   zero readership.
4. **Entry cost must be bounded and the threshold pre-declared.** Google SRE
   requires criteria before the incident; Allspaw warns that declaring one
   "involve[s] substantial future work."
5. **It must fit the agent context budget with a stated eviction rule** — under
   200 lines if it is an instruction/memory file, with an explicit "merge or
   drop stale entries" policy; read-on-demand rather than injected every
   session.
6. **A reminder must be a hook, not another instruction file or a third skill.**
   Anthropic: hooks "are deterministic and guarantee the action happens", and
   the prescribed fix for an ignored rule is "delete it or convert it to a
   hook." A skill whose job is to remind is the documented *anti*-pattern.

**Strongest sourced argument against building it.** Cook names the exact thing
this proposal is: **"the reduction of an incident to a manageable discrete list
of things to be done"** — identified not as the goal of incident review but as
the pressure that degrades reviews into *"pallid, vapid, mechanical exercises"*
producing *"a defensible argument that management is occurring."* Allspaw
reinforces from the other side: fixing is not learning, and prioritising fixes
yields lower ROI than understanding. So the register's core rule ("produce a
guard or close as a one-off") is, in the resilience literature, the signature of
the failure mode rather than a defence against it.

That compounds with three structural facts. **(a)** Every documented
precondition for a behaviour-changing register is social — an independent
reviewer, a growing readership, cross-document citation, incentives tied to
performance review. A solo repo has a readership of one, who already has the
memory the register is meant to supply. **(b)** GAO's finding is that capture
was never the bottleneck: NASA *had* the system and lessons still were "not
routinely identified, collected, or shared." Building the artifact does not
touch the actual constraint. **(c)** Q3 found no prior art for the paired
backward-looking record at all.

**Consequence — a clean dominance argument:** criterion 3 does all the work and
needs neither a register nor a skill. "A real defect ships with a test that
fails before the fix" is Django's policy, is enforceable by CI, protects the
codebase with zero re-reading, and costs zero context. The register and reminder
hook add ongoing context cost, add a third competing skill in a capped listing,
and buy only the cross-entry theme-spotting that Cook says organisations with
far more volume "seldom" actually perform.
