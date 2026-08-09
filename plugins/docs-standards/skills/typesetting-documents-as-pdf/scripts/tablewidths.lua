--[[
  Give every table proportional, wrapping columns.

  Why this is needed: pandoc's gfm reader carries no column-width information
  (GFM pipe tables have none to carry), so the LaTeX writer emits `@{}llll@{}`.
  An `l` column never wraps, so a wide table runs straight off the paper. In
  this document the citation-map rows reach 587 characters and the section-2
  summary rows reach 331, and both overflowed the A4 page edge before this
  filter existed, cutting words in half at the trim.

  What it does: measures the longest rendered cell in each column, compresses
  the range with a square root, and normalises to relative widths. Setting a
  width is what makes pandoc emit `>{\raggedright\arraybackslash}p{...}`
  instead of `l`, which is what makes the cell wrap.

  Why the square root rather than the raw length: the citation map is a 3-char
  column beside a 587-char one. Raw proportions give the narrow column 0.5% of
  the text block, which is narrower than the word "page" and forces a ragged
  one-character-per-line result. sqrt(3) : sqrt(587) is about 8 : 92, which
  leaves the page-number column legible while still giving the prose column
  nearly all the width.

  CAP exists so a single very long cell cannot starve every other column; it is
  applied before the square root, so it bounds the widest column's share rather
  than rescaling everything.
]]

local CAP = 400        -- characters; longer cells count as this many
local USABLE = 0.97    -- leave a little slack for inter-column padding

local function measure(rows, maxlen)
  for _, row in ipairs(rows) do
    for i, cell in ipairs(row.cells) do
      local s = pandoc.utils.stringify(cell.content)
      local n = utf8.len(s) or #s
      if n > (maxlen[i] or 0) then maxlen[i] = n end
    end
  end
end

function Table(t)
  local ncol = #t.colspecs
  if ncol == 0 then return nil end

  local maxlen = {}
  for i = 1, ncol do maxlen[i] = 1 end

  measure(t.head.rows, maxlen)
  for _, body in ipairs(t.bodies) do
    measure(body.body, maxlen)
    measure(body.head, maxlen)
  end
  measure(t.foot.rows, maxlen)

  local weights, total = {}, 0
  for i = 1, ncol do
    local n = math.min(maxlen[i], CAP)
    weights[i] = math.sqrt(n)
    total = total + weights[i]
  end

  for i = 1, ncol do
    t.colspecs[i][2] = (weights[i] / total) * USABLE
  end
  return t
end
