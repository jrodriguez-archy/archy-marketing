#!/usr/bin/env node
'use strict'

/**
 * Paper -> Figma payload builder.
 *
 * Reads the two things the Paper MCP can hand over for one artboard:
 *   <name>.jsx   get_jsx        structure, styles (as Tailwind classes), text, raw SVG
 *   <name>.tree  get_tree_summary(depth 10)   layer names + node ids, same traversal order
 *
 * and emits payloads/<name>.json for the Figma plugin to rebuild.
 *
 * Paper has already resolved the flex layout, so this never re-implements
 * layout: it reads the authored intent (flex direction, gap, padding,
 * alignment, grow/shrink) and hands Figma the equivalent auto-layout.
 *
 *   node build.js raw/<slug>.jsx raw/<slug>.tree --tokens=tokens/<slug>.json
 *
 * Paths. This file lives in the plugin folder, which is replaced on every update, so
 * nothing is ever written beside it. Reads, tokens and payloads live in a work directory:
 *
 *   --work=DIR (or --work DIR)  >  $ARCHY_WORK  >  BASE
 *
 * where BASE is $ARCHY_WORK_BASE, else ${CLAUDE_PLUGIN_DATA}/figma-export, else
 * ./archy-work/figma-export. Relative input paths are tried in the current directory,
 * then in the work directory. The payload is written to <work>/payloads/<name>.json.
 */

const fs = require('fs')
const path = require('path')

// ------------------------------------------------------------ work directory

const TOOL = 'figma-export'

function takeWorkArg() {
  const argv = process.argv
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--work=')) { const v = argv[i].slice(7); argv.splice(i, 1); return v }
    if (argv[i] === '--work' && i + 1 < argv.length) { const v = argv[i + 1]; argv.splice(i, 2); return v }
  }
  return null
}

function workDir() {
  const base = process.env.ARCHY_WORK_BASE ||
    (process.env.CLAUDE_PLUGIN_DATA
      ? path.join(process.env.CLAUDE_PLUGIN_DATA, TOOL)
      : path.join(process.cwd(), 'archy-work', TOOL))
  return path.resolve(takeWorkArg() || process.env.ARCHY_WORK || base)
}

function inputPath(work, p) {
  if (path.isAbsolute(p)) return p
  const here = path.resolve(p)
  return fs.existsSync(here) ? here : path.join(work, p)
}

// ---------------------------------------------------------------- Tailwind

const U = 4 // Paper emits Tailwind's default 4px spacing unit

/** "16" -> 64, "62.5" -> 250, "3.5" -> 14 */
const units = (n) => Number(n) * U

/** Pulls "40px" out of text-[40px], 0.02em out of tracking-[0.02em], etc. */
const arbitrary = (cls, prefix) => {
  const m = cls.match(new RegExp(`^${prefix}-\\[(.+)\\]$`))
  return m ? m[1] : null
}

const ALIGN = {
  start: 'MIN',
  'flex-start': 'MIN',
  center: 'CENTER',
  end: 'MAX',
  'flex-end': 'MAX',
  between: 'SPACE_BETWEEN',
  'space-between': 'SPACE_BETWEEN',
}

/**
 * Turns Paper's Tailwind class string into a normalised style object.
 * Anything unrecognised lands in `unknown` so the plugin can report it
 * rather than silently dropping a property.
 */
function parseClasses(classString) {
  const s = {
    unknown: [],
    padding: { top: 0, right: 0, bottom: 0, left: 0 },
  }
  if (!classString) return s

  for (const cls of classString.split(/\s+/).filter(Boolean)) {
    let m

    // --- layout mode -----------------------------------------------------
    if (cls === 'flex') { s.flex = true; continue }
    if (cls === 'flex-col') { s.flex = true; s.direction = 'VERTICAL'; continue }
    if (cls === 'flex-row') { s.flex = true; s.direction = 'HORIZONTAL'; continue }
    if (cls === 'flex-wrap') { s.wrap = true; continue }
    if (cls === 'absolute') { s.position = 'absolute'; continue }
    if (cls === 'relative') { s.position = 'relative'; continue }

    // --- alignment -------------------------------------------------------
    if ((m = cls.match(/^items-(.+)$/)) && ALIGN[m[1]]) { s.counterAlign = ALIGN[m[1]]; continue }
    if ((m = cls.match(/^justify-(.+)$/)) && ALIGN[m[1]]) { s.primaryAlign = ALIGN[m[1]]; continue }
    if (cls === 'items-stretch') { s.counterAlign = 'MIN'; s.stretchChildren = true; continue }
    if (cls === 'self-start') { s.selfAlign = 'MIN'; continue }
    if (cls === 'self-center') { s.selfAlign = 'CENTER'; continue }
    if (cls === 'self-end') { s.selfAlign = 'MAX'; continue }

    // --- sizing ----------------------------------------------------------
    if (cls === 'shrink-0') { s.shrink0 = true; continue }
    if (cls === 'grow') { s.grow = 1; continue }
    if (cls === 'w-full') { s.widthFill = true; continue }
    if (cls === 'h-full') { s.heightFill = true; continue }
    if (cls === 'w-fit') { s.widthHug = true; continue }
    if (cls === 'h-fit') { s.heightHug = true; continue }
    if ((m = cls.match(/^size-([\d.]+)$/))) { s.w = units(m[1]); s.h = units(m[1]); continue }
    if ((m = cls.match(/^w-([\d.]+)$/))) { s.w = units(m[1]); continue }
    if ((m = cls.match(/^h-([\d.]+)$/))) { s.h = units(m[1]); continue }
    if ((m = arbitrary(cls, 'w'))) { s.w = parseFloat(m); continue }
    if ((m = arbitrary(cls, 'h'))) { s.h = parseFloat(m); continue }

    // --- position --------------------------------------------------------
    if ((m = cls.match(/^left-([\d.]+)$/))) { s.x = units(m[1]); continue }
    if ((m = cls.match(/^top-([\d.]+)$/))) { s.y = units(m[1]); continue }
    if ((m = cls.match(/^-left-([\d.]+)$/))) { s.x = -units(m[1]); continue }
    if ((m = cls.match(/^-top-([\d.]+)$/))) { s.y = -units(m[1]); continue }
    if ((m = arbitrary(cls, 'left'))) { s.x = parseFloat(m); continue }
    if ((m = arbitrary(cls, 'top'))) { s.y = parseFloat(m); continue }

    // --- spacing ---------------------------------------------------------
    if ((m = cls.match(/^gap-([\d.]+)$/))) { s.gap = units(m[1]); continue }
    if ((m = cls.match(/^p-([\d.]+)$/))) {
      const v = units(m[1]); s.padding = { top: v, right: v, bottom: v, left: v }; continue
    }
    if ((m = cls.match(/^px-([\d.]+)$/))) {
      const v = units(m[1]); s.padding.left = v; s.padding.right = v; continue
    }
    if ((m = cls.match(/^py-([\d.]+)$/))) {
      const v = units(m[1]); s.padding.top = v; s.padding.bottom = v; continue
    }
    if ((m = cls.match(/^pt-([\d.]+)$/))) { s.padding.top = units(m[1]); continue }
    if ((m = cls.match(/^pr-([\d.]+)$/))) { s.padding.right = units(m[1]); continue }
    if ((m = cls.match(/^pb-([\d.]+)$/))) { s.padding.bottom = units(m[1]); continue }
    if ((m = cls.match(/^pl-([\d.]+)$/))) { s.padding.left = units(m[1]); continue }

    // --- type ------------------------------------------------------------
    if ((m = arbitrary(cls, 'text'))) {
      if (/px$/.test(m)) { s.fontSize = parseFloat(m); continue }
    }
    if ((m = cls.match(/^leading-([\d.]+)$/))) { s.lineHeight = units(m[1]); continue }
    if ((m = arbitrary(cls, 'leading'))) { s.lineHeight = parseFloat(m); continue }
    if ((m = arbitrary(cls, 'tracking'))) { s.letterSpacingEm = parseFloat(m); continue }
    if ((m = cls.match(/^font-\['([^']+)'/))) { s.fontFamily = m[1]; continue }
    if ((m = arbitrary(cls, 'font'))) { s.fontWeight = parseInt(m, 10); continue }
    if (cls === 'text-center') { s.textAlign = 'CENTER'; continue }
    if (cls === 'text-right') { s.textAlign = 'RIGHT'; continue }
    if (cls === 'text-left') { s.textAlign = 'LEFT'; continue }
    if (cls === 'italic') { s.italic = true; continue }
    if (cls === 'uppercase') { s.textCase = 'UPPER'; continue }

    // --- paint -----------------------------------------------------------
    // A Paper file that does not use tokens emits raw values instead, so both
    // shapes have to survive: bg-navy-panel and bg-[#001797].
    if ((m = arbitrary(cls, 'bg'))) {
      if (/^(linear|radial|conic)-gradient/.test(m)) { s.fillGradient = m }
      else s.fillRaw = m
      continue
    }
    if ((m = arbitrary(cls, 'text'))) { if (!/px$/.test(m)) { s.colorRaw = m; continue } }
    if ((m = cls.match(/^bg-(.+)$/))) { s.fill = m[1]; continue }
    if ((m = cls.match(/^border-b-(dashed|solid|dotted)$/))) { s.borderBottomStyle = m[1]; continue }
    if ((m = cls.match(/^border-b-(.+)$/))) { s.borderBottomColor = m[1]; continue }
    if ((m = cls.match(/^border-t-(dashed|solid|dotted)$/))) { s.borderTopStyle = m[1]; continue }
    if ((m = cls.match(/^border-t-(.+)$/))) { s.borderTopColor = m[1]; continue }
    if ((m = cls.match(/^\[border-bottom-width:([\d.]+)px\]$/))) { s.borderBottomWidth = parseFloat(m[1]); continue }
    if ((m = cls.match(/^\[border-top-width:([\d.]+)px\]$/))) { s.borderTopWidth = parseFloat(m[1]); continue }
    if ((m = cls.match(/^opacity-([\d.]+)$/))) { s.opacity = Number(m[1]) / 100; continue }

    // --- shape -----------------------------------------------------------
    if (cls === 'rounded-full') { s.radius = 9999; continue }
    if ((m = cls.match(/^rounded-([\d.]+)$/))) { s.radius = units(m[1]); continue }
    if ((m = arbitrary(cls, 'rounded'))) { s.radius = parseFloat(m); continue }
    if (cls === 'overflow-clip' || cls === 'overflow-hidden') { s.clip = true; continue }

    // --- text colour, after the bg/border rules so it cannot shadow them --
    if ((m = cls.match(/^text-(.+)$/))) { s.color = m[1]; continue }

    // --- cosmetics Paper always emits, and Figma has no equivalent for ----
    if (['antialiased', 'wrap-anywhere', '[font-synthesis:none]', 'flex-nowrap'].includes(cls)) continue

    s.unknown.push(cls)
  }
  return s
}

// ------------------------------------------------------------------- JSX

/**
 * Minimal tag walker. Paper's JSX is machine-generated and well formed,
 * so a tokeniser is enough - and it keeps this file dependency-free.
 */
function parseJsx(src) {
  // strip the wrapping parens Paper adds
  src = src.trim().replace(/^\(\s*/, '').replace(/\s*\)$/, '')

  let i = 0
  const readNode = () => {
    while (i < src.length && /\s/.test(src[i])) i++
    if (src[i] !== '<') return null

    const tagStart = i
    const nameMatch = /^<([a-zA-Z][\w-]*)/.exec(src.slice(i))
    if (!nameMatch) return null
    const tag = nameMatch[1]

    // find the end of the opening tag, respecting quotes and {} expressions
    let j = i + nameMatch[0].length
    let quote = null
    let brace = 0
    while (j < src.length) {
      const c = src[j]
      if (quote) { if (c === quote) quote = null }
      else if (c === '"' || c === "'") quote = c
      else if (c === '{') brace++
      else if (c === '}') brace--
      else if (c === '>' && brace === 0) break
      j++
    }
    const openTag = src.slice(i, j + 1)
    const selfClosing = /\/>$/.test(openTag)
    i = j + 1

    const node = { tag, raw: openTag, children: [], text: '' }
    const cn = openTag.match(/className="([^"]*)"/)
    node.className = cn ? cn[1] : ''

    // svg subtrees are handed to Figma verbatim, so capture the whole thing
    if (tag === 'svg') {
      const close = src.indexOf('</svg>', i)
      node.svg = src.slice(tagStart, close + 6)
      i = close + 6
      return node
    }

    if (selfClosing) return node

    // children + text until the matching close tag
    while (i < src.length) {
      while (i < src.length && /\s/.test(src[i])) i++
      if (src.startsWith(`</${tag}>`, i)) { i += tag.length + 3; break }
      if (src[i] === '<') {
        const child = readNode()
        if (child) node.children.push(child); else break
      } else {
        const next = src.indexOf('<', i)
        const chunk = src.slice(i, next === -1 ? src.length : next)
        node.text += chunk
        i = next === -1 ? src.length : next
      }
    }
    node.text = node.text.replace(/\s+/g, ' ').trim()
    return node
  }

  return readNode()
}

// ------------------------------------------------------------------ tree

/** Parses get_tree_summary into the same shape, for names and ids. */
function parseTree(src) {
  const lines = src.split('\n').filter((l) => l.trim())
  const root = { children: [] }
  const stack = [{ depth: -1, node: root }]

  for (const line of lines) {
    const depth = (line.match(/^ */)[0].length) / 2
    const m = line.trim().match(/^(\w+)\s+"(.*?)"\s+\(([\w-]+)\)(?:\s+([\d.]+)×([\d.]+))?/)
    if (!m) continue
    const node = { type: m[1], name: m[2], id: m[3], children: [] }
    if (m[4]) { node.w = parseFloat(m[4]); node.h = parseFloat(m[5]) }
    while (stack.length && stack[stack.length - 1].depth >= depth) stack.pop()
    stack[stack.length - 1].node.children.push(node)
    stack.push({ depth, node })
  }
  return root.children[0]
}

// --------------------------------------------------------------- combine

/**
 * Zips the two trees positionally. They come from the same traversal, so a
 * mismatch means one of the reads is stale - worth failing loudly rather
 * than emitting a payload with the wrong names attached.
 */
function combine(jsxNode, treeNode, warnings, pathStr = 'root') {
  const style = parseClasses(jsxNode.className)
  for (const u of style.unknown) warnings.push(`${pathStr}: unmapped class "${u}"`)

  // Paper writes SVG geometry as an inline style object, not classes
  const inline = jsxNode.raw.match(/style=\{\{([^}]*)\}\}/)
  if (inline) {
    const grab = (prop) => {
      const m = inline[1].match(new RegExp(`${prop}:\\s*'([-\\d.]+)px'`))
      return m ? parseFloat(m[1]) : undefined
    }
    const x = grab('left'), y = grab('top'), w = grab('width'), h = grab('height')
    if (x !== undefined) style.x = x
    if (y !== undefined) style.y = y
    if (w !== undefined) style.w = w
    if (h !== undefined) style.h = h
    if (/position:\s*'absolute'/.test(inline[1])) style.position = 'absolute'
  }

  const out = {
    name: treeNode ? treeNode.name : jsxNode.tag,
    id: treeNode ? treeNode.id : null,
    kind: jsxNode.svg ? 'SVG' : jsxNode.text ? 'TEXT' : 'FRAME',
    style,
  }
  if (jsxNode.svg) out.svg = jsxNode.svg
  if (jsxNode.text) out.characters = decode(jsxNode.text)

  if (treeNode && treeNode.children.length !== jsxNode.children.length && !jsxNode.svg) {
    warnings.push(
      `${pathStr} ("${out.name}"): tree has ${treeNode.children.length} children, ` +
      `jsx has ${jsxNode.children.length} \u2014 names below this point may be wrong`
    )
  }

  out.children = jsxNode.children.map((c, n) =>
    combine(c, treeNode && treeNode.children[n], warnings, `${pathStr}/${n}`)
  )
  return out
}

const decode = (s) =>
  s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
   .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ')

// ------------------------------------------------------------- validation

/**
 * The dangerous failure mode: when Paper's renderer is down, geometry comes
 * back unresolved and every child reports 0,0 with no error at all. A payload
 * built on that looks plausible and is garbage. The tell is a padded frame
 * whose first child still sits at the origin.
 */
function validate(node, problems, pathStr = 'root') {
  const s = node.style
  const padded = s.padding && (s.padding.top || s.padding.left)
  if (padded && node.children.length && !s.flex) {
    const first = node.children[0].style
    if (first.x === 0 && first.y === 0) {
      problems.push(`${pathStr} ("${node.name}"): padded frame reports its first child at 0,0 \u2014 Paper's layout is probably unresolved. Re-read after bringing the file to the front.`)
    }
  }
  node.children.forEach((c, n) => validate(c, problems, `${pathStr}/${n}`))
}

// ------------------------------------------------------------------ tokens

/**
 * Accepts whatever shape the token list arrives in, so it can be saved
 * straight out of the MCP without hand-editing:
 *
 *   { "navy": "#00005B" }                                  already right
 *   { "--color-navy": "#00005B" }                          CSS names
 *   { "items": [ { "name": "--color-navy", "value": … } ] } get_tokens verbatim
 *   { "tokens": { "items": [ … ] } }                        get_basic_info verbatim
 *
 * Paper writes the class as `bg-navy`, so the `--color-` prefix has to go.
 */
function normaliseTokens(raw) {
  let entries = []
  if (Array.isArray(raw)) entries = raw
  else if (raw && raw.items) entries = raw.items
  else if (raw && raw.tokens && raw.tokens.items) entries = raw.tokens.items
  else if (raw && typeof raw === 'object') {
    entries = Object.keys(raw).map((k) => ({ name: k, value: raw[k] }))
  }

  const out = {}
  for (const e of entries) {
    if (!e || !e.name) continue
    const key = String(e.name).replace(/^--(color-)?/, '')
    if (typeof e.value === 'string') out[key] = e.value
  }
  return out
}

// -------------------------------------------------------------------- run

function main() {
  const WORK = workDir()
  const [jsxArg, treeArg] = process.argv.slice(2).filter((a) => !a.startsWith('--'))
  const jsxPath = jsxArg && inputPath(WORK, jsxArg)
  const treePath = treeArg && inputPath(WORK, treeArg)
  if (!jsxPath || !treePath) {
    console.error('usage: node build.js <raw/name.jsx> <raw/name.tree> [--tokens=tokens/name.json] [--work=DIR]')
    process.exit(1)
  }

  const jsxRaw = fs.readFileSync(jsxPath, 'utf8')
  const treeRaw = fs.readFileSync(treePath, 'utf8')

  const warnings = []
  const tree = parseTree(treeRaw)
  const doc = combine(parseJsx(jsxRaw), tree, warnings)

  // Paper puts no size classes on the artboard itself; the tree summary is
  // the only place its dimensions appear. Only the root gets this fallback -
  // applying measured sizes further down would pin every text box to the
  // width it happened to have and kill hugging.
  if (doc.style.w === undefined && tree && tree.w) { doc.style.w = tree.w; doc.style.h = tree.h }

  const problems = []
  validate(doc, problems)
  if (problems.length) {
    console.error('\nREFUSING TO WRITE \u2014 the source geometry looks unresolved:')
    for (const p of problems) console.error('  ' + p)
    process.exit(2)
  }

  // Tokens come from whatever Paper file this artboard lives in - pass the
  // file written from get_tokens. Without one, colours still travel as raw
  // values and the plugin simply has nothing to offer for mapping.
  const tokensArg = process.argv.slice(2).find((a) => a.startsWith('--tokens='))
  const tokensPath = tokensArg ? inputPath(WORK, tokensArg.slice(9)) : path.join(WORK, 'tokens.json')
  const allTokens = fs.existsSync(tokensPath)
    ? normaliseTokens(JSON.parse(fs.readFileSync(tokensPath, 'utf8')))
    : {}

  // The payload carries only what this artboard actually uses, so someone
  // importing it into another file is not asked to map a whole design system.
  const tokens = {}
  const fonts = {}
  const gradients = []
  ;(function collect(n) {
    for (const key of ['fill', 'color', 'borderBottomColor', 'borderTopColor']) {
      const t = n.style[key]
      if (!t) continue
      tokens[t] = t in allTokens ? allTokens[t] : null
    }
    if (n.style.fillGradient) gradients.push(n.name)
    if (n.kind === 'TEXT') {
      const fam = n.style.fontFamily || '(inherited)'
      const w = n.style.fontWeight || 400
      fonts[fam] = fonts[fam] || []
      if (!fonts[fam].includes(w)) fonts[fam].push(w)
    }
    n.children.forEach(collect)
  })(doc)
  for (const f of Object.keys(fonts)) fonts[f].sort((a, b) => a - b)
  const unvalued = Object.keys(tokens).filter((t) => tokens[t] === null)
  if (unvalued.length) {
    warnings.push(
      `${unvalued.length} colour(s) have no value in ${path.basename(tokensPath)} ` +
      `(${unvalued.join(', ')}) \u2014 the plugin will ask for each one`
    )
  }
  for (const g of gradients) warnings.push(`"${g}" has a gradient fill \u2014 not supported yet, it will import unpainted`)

  const name = path.basename(jsxPath).replace(/\.jsx$/, '')
  const outPath = path.join(WORK, 'payloads', `${name}.json`)
  fs.mkdirSync(path.dirname(outPath), { recursive: true })
  fs.writeFileSync(outPath, JSON.stringify({
    meta: { name: doc.name, source: path.basename(jsxPath), generated: new Date().toISOString() },
    tokens, fonts, document: doc,
  }, null, 2))

  let count = 0
  ;(function tally(n) { count++; n.children.forEach(tally) })(doc)

  console.log(`${outPath}`)
  console.log(`  ${count} nodes · "${doc.name}" ${doc.style.w || '?'}×${doc.style.h || '?'}`)
  if (warnings.length) {
    console.log(`  ${warnings.length} warning(s):`)
    for (const w of warnings.slice(0, 20)) console.log('    ' + w)
  }
}

if (require.main === module) main()
module.exports = { parseClasses, parseJsx, parseTree, combine, validate }
