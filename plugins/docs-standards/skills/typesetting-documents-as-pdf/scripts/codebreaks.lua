--[[
  Make long inline-code spans breakable, without inserting any character.

  Why this is needed: pandoc renders inline code `git clone --depth 1 https://x`
  as \texttt{git\ clone\ -\/-depth\ 1\ https://x}. Every space becomes a control
  space, which is unbreakable, and \texttt offers no break points of its own, so
  the whole span is one rigid box. If that box is wider than the text column,
  TeX reports an Overfull \hbox and the text runs off the paper. In this
  document three pages overflowed by 43-68 pt for exactly this reason.

  Why not hyphenation: \usepackage[htt]{hyphenat} would fix the overflow by
  hyphenating the span, but it inserts a visible hyphen. In a document full of
  paths, flags and identifiers -- `--depth`, `naecon2023-fpga-re`, `segbits_opt`
  -- a reader cannot tell an inserted hyphen from one that belongs to the token.
  That trades a layout defect for a correctness defect, which is the worse of
  the two.

  What this does instead: emits the same \texttt, with \allowbreak after each
  natural boundary. \allowbreak is a zero-width legal break point, so the line
  may break there and nothing is added to the text. Short spans are left alone,
  because a break opportunity inside a five-character identifier only invites an
  ugly break that was never needed.
]]

-- 14 rather than a larger number: measured, not guessed. At 24 the span
-- `fuzzers/Makefile:105` (20 characters) stayed rigid, landed at a line end
-- and protruded 43 pt into the right margin. Anything past roughly a dozen
-- characters can fail to fit the tail of a line, so the threshold has to sit
-- below that. Shorter spans are left rigid because a break opportunity inside
-- a short identifier only invites a break that was never needed.
local MIN_LEN = 14
local BREAK_AFTER = "/-_.:,;=&?" -- natural boundaries in paths, URLs and flags

-- LaTeX specials, longest-first so \ is handled before the others reuse it.
local function escape(s)
  s = s:gsub("\\", "\1")
  s = s:gsub("([{}$&#%%_])", "\\%1")
  s = s:gsub("%^", "\\^{}")
  s = s:gsub("~", "\\textasciitilde{}")
  s = s:gsub("\1", "\\textbackslash{}")
  return s
end

function Code(el)
  local text = el.text
  if (utf8.len(text) or #text) < MIN_LEN then return nil end

  local out = {}
  for i = 1, #text do
    local c = text:sub(i, i)
    if c == " " then
      -- a real space, then a break opportunity after it
      out[#out + 1] = "\\ \\allowbreak{}"
    else
      out[#out + 1] = escape(c)
      if BREAK_AFTER:find(c, 1, true) then
        out[#out + 1] = "\\allowbreak{}"
      end
    end
  end

  return pandoc.RawInline("latex", "\\texttt{" .. table.concat(out) .. "}")
end
