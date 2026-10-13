# Chat-explanation test (2026-10-13)

Question put to the agent (sonnet, fresh context, no tools): "In our GNSS anti-jam array
the weights are w = R⁻¹e. I'm told R⁻¹ 'attenuates each eigenmode by 1/λ'. Explain what an
eigenvector of the covariance matrix R is and why multiplying by R⁻¹ removes the jammer."
Asker described as an FPGA/DSP engineer new to adaptive arrays.

Scored by hand on four criteria from standards 2 and 12:

| criterion | control (no skill), 3 reps | with skill, 3 reps |
|---|---|---|
| A. kind of product named at first use (matrix × vector, dot, outer) | 0/3 | 3/3 |
| B. informal labels ("direction", "rotate", "subspace", "mode") built before use | 0/3 | 3/3 |
| C. one running numeric example carried through | 0/3 | 3/3 (all three chose two antennas, J = 100, σ² = 1, and reached the 40 dB null) |
| D. no unflagged letter reuse | 2/3 (rep 2 used c for data coefficients and for the expansion of e) | 2/3 (rep 2 named the projection coefficients a₁, a₂ beside the steering vector a; rep 3 flagged e versus Euler's e unprompted) |

Control rationalizations seen verbatim: "think of v as a specific spatial pattern",
"for almost any pattern, applying R rotates and rescales it" (no arrow or axis defined),
"the noise-only subspace" (never constructed), "R v = λ v" with no statement of what the
product is. All three were fluent and correct, and all three would have produced the
same six follow-up questions the session that motivated this test produced.

With-skill loophole closed after the run: the chat-mode recipe now asks for the list of
letters already taken before any coefficient is named, and the red flags carry the
`a₁` beside `a` case. Not re-run after that edit.

Not scored: all three with-skill replies still used em dashes as connectives (standard
10), the same as the controls; the runs were framed as chat replies and the dash rule is
unchanged by this edit.
