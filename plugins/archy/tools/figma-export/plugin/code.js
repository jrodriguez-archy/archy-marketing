// Paper Import - rebuilds a Paper artboard in Figma as real nodes.
//
// Nothing here knows anything about a particular project. The payload declares
// which colours and fonts it uses; the plugin looks at whatever Figma file it
// is running in, proposes a mapping, and lets the person importing change it
// before anything is created.

figma.showUI(__html__, { width: 460, height: 620 })

const WEIGHT_TO_STYLE = {
  100: 'Thin', 200: 'ExtraLight', 300: 'Light', 400: 'Regular',
  500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black',
}
// What to try, in order, when a weight has no exact style in the chosen family.
const WEIGHT_FALLBACKS = {
  100: ['Thin', 'ExtraLight', 'Light', 'Regular'],
  200: ['ExtraLight', 'Thin', 'Light', 'Regular'],
  300: ['Light', 'ExtraLight', 'Regular'],
  400: ['Regular', 'Book', 'Normal', 'Medium'],
  500: ['Medium', 'Regular', 'SemiBold'],
  600: ['SemiBold', 'Demi', 'Bold', 'Medium'],
  700: ['Bold', 'SemiBold', 'Black'],
  800: ['ExtraBold', 'Bold', 'Black'],
  900: ['Black', 'Heavy', 'ExtraBold', 'Bold'],
}

let warnings = []
const warn = (m) => { if (warnings.indexOf(m) === -1) warnings.push(m) }

// ------------------------------------------------------------------ colour

function parseColor(value) {
  if (!value) return null
  let v = String(value).trim()

  let m = v.match(/^#?([0-9a-fA-F]{3})$/)
  if (m) v = '#' + m[1].split('').map((c) => c + c).join('')
  m = v.match(/^#?([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$/)
  if (m) {
    return {
      color: {
        r: parseInt(m[1].slice(0, 2), 16) / 255,
        g: parseInt(m[1].slice(2, 4), 16) / 255,
        b: parseInt(m[1].slice(4, 6), 16) / 255,
      },
      opacity: m[2] ? parseInt(m[2], 16) / 255 : 1,
    }
  }
  m = v.match(/^rgba?\(([^)]+)\)$/)
  if (m) {
    const p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number)
    return {
      color: { r: p[0] / 255, g: p[1] / 255, b: p[2] / 255 },
      opacity: p.length > 3 ? p[3] : 1,
    }
  }
  return null
}

const rgbToHex = (c) => '#' + [c.r, c.g, c.b]
  .map((n) => Math.round(n * 255).toString(16).padStart(2, '0')).join('').toUpperCase()

// ---------------------------------------------------------------- analysis

/**
 * Everything the target file already has, so the UI can propose a mapping
 * instead of dumping a fresh copy of someone else's design system into it.
 */
async function analyze(payload) {
  const collections = await figma.variables.getLocalVariableCollectionsAsync()
  const localVars = await figma.variables.getLocalVariablesAsync('COLOR')

  const existing = []
  for (const v of localVars) {
    const col = collections.filter((c) => c.id === v.variableCollectionId)[0]
    if (!col) continue
    const value = v.valuesByMode[col.modes[0].modeId]
    existing.push({
      id: v.id,
      name: v.name,
      collection: col.name,
      hex: value && typeof value === 'object' && 'r' in value ? rgbToHex(value) : null,
    })
  }

  const norm = (s) => String(s).toLowerCase().replace(/[^a-z0-9]/g, '')

  const tokens = Object.keys(payload.tokens || {}).map((name) => {
    const hex = payload.tokens[name]
    // Prefer a name match, then a value match, then create it.
    let match = existing.filter((e) => norm(e.name) === norm(name))[0]
    if (!match) match = existing.filter((e) => norm(e.name.split('/').pop()) === norm(name))[0]
    if (!match && hex) match = existing.filter((e) => e.hex && e.hex === hex.toUpperCase())[0]
    return {
      name: name,
      hex: hex,
      suggestion: match ? match.id : (hex ? '__create__' : '__pick__'),
      reason: match ? (norm(match.name).indexOf(norm(name)) !== -1 ? 'name' : 'value') : null,
    }
  })

  const available = await figma.listAvailableFontsAsync()
  const families = {}
  for (const f of available) {
    families[f.fontName.family] = families[f.fontName.family] || []
    families[f.fontName.family].push(f.fontName.style)
  }

  const fonts = Object.keys(payload.fonts || {}).map((family) => ({
    family: family,
    weights: payload.fonts[family],
    available: !!families[family],
    suggestion: families[family] ? family : null,
  }))

  return {
    tokens: tokens,
    fonts: fonts,
    existingVariables: existing,
    collections: collections.map((c) => ({ id: c.id, name: c.name })),
    families: Object.keys(families).sort(),
    familyStyles: families,
  }
}

// ------------------------------------------------------------------- build

/** name -> { paint } resolved once from the mapping the user confirmed. */
let paintByToken = {}
let fontByFamily = {}
let familyStyles = {}

async function resolveTokens(payload, mapping) {
  paintByToken = {}
  const collections = await figma.variables.getLocalVariableCollectionsAsync()
  const localVars = await figma.variables.getLocalVariablesAsync('COLOR')

  let newCollection = null
  const ensureCollection = () => {
    if (newCollection) return newCollection
    const target = mapping.collectionId
      ? collections.filter((c) => c.id === mapping.collectionId)[0]
      : null
    newCollection = target || figma.variables.createVariableCollection(mapping.collectionName || 'Paper')
    return newCollection
  }

  for (const name of Object.keys(payload.tokens || {})) {
    const choice = mapping.tokens[name]
    if (!choice || choice === '__raw__') {
      const parsed = parseColor(payload.tokens[name])
      if (parsed) paintByToken[name] = { type: 'SOLID', color: parsed.color, opacity: parsed.opacity }
      else warn('"' + name + '" has no colour and was left unpainted')
      continue
    }
    if (choice === '__create__') {
      const parsed = parseColor(payload.tokens[name])
      if (!parsed) { warn('cannot create "' + name + '" without a value'); continue }
      const col = ensureCollection()
      const modeId = col.modes[0].modeId
      let v = localVars.filter((x) => x.name === name && x.variableCollectionId === col.id)[0]
      if (!v) v = figma.variables.createVariable(name, col, 'COLOR')
      v.setValueForMode(modeId, parsed.color)
      paintByToken[name] = figma.variables.setBoundVariableForPaint(
        { type: 'SOLID', color: parsed.color, opacity: parsed.opacity }, 'color', v)
      continue
    }
    // bound to an existing variable in this file
    const v = await figma.variables.getVariableByIdAsync(choice)
    if (!v) { warn('variable for "' + name + '" no longer exists'); continue }
    const col = collections.filter((c) => c.id === v.variableCollectionId)[0]
    const value = col ? v.valuesByMode[col.modes[0].modeId] : null
    const base = value && typeof value === 'object' && 'r' in value
      ? { r: value.r, g: value.g, b: value.b }
      : { r: 0, g: 0, b: 0 }
    paintByToken[name] = figma.variables.setBoundVariableForPaint(
      { type: 'SOLID', color: base }, 'color', v)
  }
}

async function resolveFonts(payload, mapping) {
  fontByFamily = {}
  const available = await figma.listAvailableFontsAsync()
  familyStyles = {}
  for (const f of available) {
    familyStyles[f.fontName.family] = familyStyles[f.fontName.family] || []
    familyStyles[f.fontName.family].push(f.fontName.style)
  }

  for (const family of Object.keys(payload.fonts || {})) {
    const target = mapping.fonts[family] || family
    const styles = familyStyles[target]
    if (!styles) { warn('"' + target + '" is not available \u2014 text using it stays unstyled'); continue }
    fontByFamily[family] = target
    for (const weight of payload.fonts[family]) {
      const style = pickStyle(target, weight)
      if (style) await figma.loadFontAsync({ family: target, style: style })
    }
  }
}

/** Closest available style for a CSS weight in a given family. */
function pickStyle(family, weight) {
  const styles = familyStyles[family] || []
  const wanted = WEIGHT_TO_STYLE[weight] || 'Regular'
  if (styles.indexOf(wanted) !== -1) return wanted
  for (const alt of WEIGHT_FALLBACKS[weight] || ['Regular']) {
    if (styles.indexOf(alt) !== -1) {
      warn('"' + family + '" has no ' + wanted + ' \u2014 using ' + alt)
      return alt
    }
  }
  warn('"' + family + '" has no weight near ' + weight + ' \u2014 using ' + styles[0])
  return styles[0]
}

function paintFor(style, tokenKey, rawKey) {
  const token = style[tokenKey]
  if (token && paintByToken[token]) return paintByToken[token]
  const parsed = parseColor(style[rawKey])
  if (parsed) return { type: 'SOLID', color: parsed.color, opacity: parsed.opacity }
  return null
}

function applyBorder(figNode, s) {
  const side = s.borderBottomWidth ? 'bottom' : s.borderTopWidth ? 'top' : null
  if (!side) return
  const width = side === 'bottom' ? s.borderBottomWidth : s.borderTopWidth
  const token = side === 'bottom' ? s.borderBottomColor : s.borderTopColor
  const dashed = (side === 'bottom' ? s.borderBottomStyle : s.borderTopStyle) === 'dashed'
  const paint = token && paintByToken[token] ? paintByToken[token] : parseSolid(token)
  if (!paint) return
  figNode.strokes = [paint]
  figNode.strokeAlign = 'INSIDE'
  figNode.strokeTopWeight = side === 'top' ? width : 0
  figNode.strokeBottomWeight = side === 'bottom' ? width : 0
  figNode.strokeLeftWeight = 0
  figNode.strokeRightWeight = 0
  // CSS never states the dash length, so this is the plugin's own convention.
  if (dashed) figNode.dashPattern = [width * 2, width * 2.5]
}

function parseSolid(v) {
  const p = parseColor(v)
  return p ? { type: 'SOLID', color: p.color, opacity: p.opacity } : null
}

function makeText(node) {
  const t = figma.createText()
  const s = node.style
  t.name = node.name || 'Text'
  const family = fontByFamily[s.fontFamily] || fontByFamily[Object.keys(fontByFamily)[0]]
  if (family) {
    const style = pickStyle(family, s.fontWeight || 400)
    if (style) t.fontName = { family: family, style: style }
  }
  t.characters = node.characters || ''
  if (s.fontSize) t.fontSize = s.fontSize
  if (s.lineHeight) t.lineHeight = { value: s.lineHeight, unit: 'PIXELS' }
  if (s.letterSpacingEm) t.letterSpacing = { value: s.letterSpacingEm * 100, unit: 'PERCENT' }
  if (s.textAlign) t.textAlignHorizontal = s.textAlign
  if (s.textCase) t.textCase = s.textCase
  const paint = paintFor(s, 'color', 'colorRaw')
  if (paint) t.fills = [paint]
  t.textAutoResize = s.w ? 'HEIGHT' : 'WIDTH_AND_HEIGHT'
  if (s.w) t.resize(s.w, t.height)
  return t
}

/**
 * Figma text has no padding, and auto-layout has no per-child counter-axis
 * alignment. Both get a one-child frame carrying the intent instead.
 */
function needsWrapper(node) {
  const p = node.style.padding
  const padded = p && (p.top || p.right || p.bottom || p.left)
  return node.kind === 'TEXT' && (padded || node.style.selfAlign)
}

function buildNode(node) {
  const s = node.style
  let fig

  if (node.kind === 'SVG') {
    try {
      fig = figma.createNodeFromSvg(node.svg)
    } catch (e) {
      warn('could not import the vector "' + node.name + '": ' + e.message)
      fig = figma.createFrame()
      fig.fills = []
    }
    fig.name = node.name || 'Vector'
    if (s.w && s.h) fig.resize(s.w, s.h)
    return fig
  }

  if (node.kind === 'TEXT') {
    fig = makeText(node)
    if (!needsWrapper(node)) return fig
    const wrap = figma.createFrame()
    wrap.name = node.name + ' (box)'
    wrap.fills = []
    wrap.layoutMode = 'VERTICAL'
    wrap.paddingTop = s.padding.top
    wrap.paddingBottom = s.padding.bottom
    wrap.paddingLeft = s.padding.left
    wrap.paddingRight = s.padding.right
    wrap.appendChild(fig)
    wrap.layoutSizingHorizontal = 'HUG'
    wrap.layoutSizingVertical = 'HUG'
    return wrap
  }

  fig = figma.createFrame()
  fig.name = node.name || 'Frame'
  const fill = paintFor(s, 'fill', 'fillRaw')
  fig.fills = fill ? [fill] : []
  if (s.fillGradient) warn('"' + node.name + '" had a gradient fill, which is not supported yet')
  if (s.radius) fig.cornerRadius = s.radius
  if (s.clip !== undefined) fig.clipsContent = !!s.clip
  if (s.opacity !== undefined) fig.opacity = s.opacity
  if (s.w && s.h) fig.resize(s.w, s.h)
  applyBorder(fig, s)

  for (const child of node.children || []) fig.appendChild(buildNode(child))

  // Auto-layout only after the children exist, or Figma lays out an empty
  // frame and the sizing calls below have nothing to act on.
  if (s.flex) {
    fig.layoutMode = s.direction === 'VERTICAL' ? 'VERTICAL' : 'HORIZONTAL'
    fig.itemSpacing = s.gap || 0
    fig.paddingTop = s.padding.top
    fig.paddingBottom = s.padding.bottom
    fig.paddingLeft = s.padding.left
    fig.paddingRight = s.padding.right
    fig.primaryAxisAlignItems = s.primaryAlign || 'MIN'
    fig.counterAxisAlignItems = s.counterAlign || 'MIN'
    if (s.w) fig.layoutSizingHorizontal = 'FIXED'
    if (s.h) fig.layoutSizingVertical = 'FIXED'
    for (let i = 0; i < fig.children.length; i++) {
      sizeChild(fig.children[i], node.children[i], s)
    }
  } else {
    for (let i = 0; i < fig.children.length; i++) {
      const cs = node.children[i].style
      if (cs.x !== undefined) fig.children[i].x = cs.x
      if (cs.y !== undefined) fig.children[i].y = cs.y
    }
  }
  return fig
}

/** flex grow / shrink / stretch -> Figma HUG / FILL / FIXED. */
function sizeChild(childFig, childNode, parentStyle) {
  const cs = childNode.style
  const vertical = parentStyle.direction === 'VERTICAL'

  if (cs.position === 'absolute') {
    try { childFig.layoutPositioning = 'ABSOLUTE' } catch (e) { /* not in auto-layout */ }
    if (cs.x !== undefined) childFig.x = cs.x
    if (cs.y !== undefined) childFig.y = cs.y
    return
  }

  const primary = vertical ? 'layoutSizingVertical' : 'layoutSizingHorizontal'
  const counter = vertical ? 'layoutSizingHorizontal' : 'layoutSizingVertical'
  const primaryFixed = vertical ? cs.h : cs.w
  const counterFixed = vertical ? cs.w : cs.h

  try {
    if (cs.grow) childFig[primary] = 'FILL'
    else if (primaryFixed) childFig[primary] = 'FIXED'
    else childFig[primary] = 'HUG'

    // No items-* on the parent is CSS stretch, so the child fills the counter
    // axis. An explicit alignment means it hugs instead.
    if (counterFixed) childFig[counter] = 'FIXED'
    else if (!parentStyle.counterAlign) childFig[counter] = 'FILL'
    else childFig[counter] = 'HUG'
  } catch (e) {
    warn('could not size "' + childNode.name + '": ' + e.message)
  }
}

// -------------------------------------------------------------------- main

let held = null // payload kept between the analyse and build steps

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'analyze') {
    warnings = []
    let payload
    try {
      payload = JSON.parse(msg.json)
    } catch (e) {
      figma.ui.postMessage({ type: 'error', message: 'That is not valid JSON: ' + e.message })
      return
    }
    if (!payload.document) {
      figma.ui.postMessage({ type: 'error', message: 'No "document" in this payload. Build it with build.js.' })
      return
    }
    held = payload
    try {
      const report = await analyze(payload)
      report.type = 'analysis'
      report.meta = payload.meta || {}
      figma.ui.postMessage(report)
    } catch (e) {
      figma.ui.postMessage({ type: 'error', message: e.message })
    }
    return
  }

  if (msg.type === 'build') {
    if (!held) { figma.ui.postMessage({ type: 'error', message: 'Load a payload first.' }); return }
    warnings = []
    try {
      await resolveTokens(held, msg.mapping)
      await resolveFonts(held, msg.mapping)

      const doc = held.document
      const root = buildNode(doc)
      root.x = Math.round(figma.viewport.center.x - (doc.style.w || 0) / 2)
      root.y = Math.round(figma.viewport.center.y - (doc.style.h || 0) / 2)
      figma.currentPage.appendChild(root)
      figma.viewport.scrollAndZoomIntoView([root])
      figma.currentPage.selection = [root]

      let count = 0
      ;(function tally(n) { count++; (n.children || []).forEach(tally) })(doc)
      figma.ui.postMessage({ type: 'done', count: count, warnings: warnings })
    } catch (e) {
      figma.ui.postMessage({ type: 'error', message: e.message, warnings: warnings })
    }
  }
}
