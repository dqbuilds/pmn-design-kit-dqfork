/*
 * render.js — manifest + data + brand → filled asset (the render pipeline)
 * ========================================================================
 * The inverse of export_manifest.js. Generic, manifest-driven: it works for ANY
 * template whose manifest follows the contract, so new templates need no new
 * render code — only a component + a manifest.
 *
 * Slot kinds handled: text, bar, arc (donut), linechart, delta (sign-driven
 * triangle+value), list (variable-length), image, logo, plus brand-mode reskin.
 *
 * Architecture (v3):
 *   - Chrome is a shared Header/Footer component instanced in every card. The
 *     renderer detaches those chrome instances after the top-level detach so
 *     their logos/source become editable/swappable (detachInstance unwraps one
 *     level only). Chrome instances are tagged pmn:role=chrome.
 *   - The field is a Background component instance whose gradient stops are bound
 *     to color/field/* — so it reskins automatically on the brand mode switch
 *     (no code-set field needed; manifest.field is null for v3 cards).
 *   - Lists clone the row component AND detach each clone, because instance
 *     sublayers cannot be resized (bar widths) — only detached nodes can.
 *
 * HOW TO RUN (on-demand / agent-triggered):
 *   Paste this file into a use_figma call, then append:
 *       const MANIFEST = <paste templates/<name>.manifest.json>;
 *       const CTX = { card: <fill data>, brand: { logos: {...} } };
 *       return await renderCard(MANIFEST, CTX, "PMN", { x: 9000, y: 0 });
 */
function get(o, p) {
  return p.split(".").reduce((a, k) => (a == null ? a : a[/^\d+$/.test(k) ? +k : k]), o);
}
function fmt(v, slot) {
  if (slot.transform === "uppercase") v = String(v).toUpperCase();
  return slot.format ? slot.format.replace("{}", v) : String(v);
}

// Redraw a line chart into a plot frame from a series [[label, value], ...].
// Geometry is code-generated (an arbitrary polyline can't be a static slot).
function drawLineChart(plot, series, env) {
  plot.children.slice().forEach((c) => c.remove());
  const W = plot.width, H = plot.height, padL = 52, padT = 14, padB = 42;
  const plx = padL, ply = padT, plw = W - padL, plh = H - padT - padB;
  const X = (i) => plx + plw * i / (series.length - 1);
  const Y = (v) => ply + plh * (1 - v / 100);
  for (const g of [0, 50, 100]) {
    const gy = Y(g);
    const r = figma.createRectangle(); r.resize(plw, g === 50 ? 2 : 1.5); r.x = plx; r.y = gy;
    r.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: g === 50 ? 0.16 : 0.09 }]; plot.appendChild(r);
    const l = figma.createText(); l.fontName = { family: "IBM Plex Mono", style: "Medium" }; l.fontSize = 16; l.characters = g + "%";
    l.fills = [{ type: "SOLID", color: env.muted }]; plot.appendChild(l); l.x = plx - l.width - 10; l.y = gy - l.height / 2;
  }
  const pts = series.map((s, i) => [X(i), Y(s[1])]);
  const path = pts.map((p) => p[0] + " " + p[1]).join(" L ");
  const area = figma.createVector(); plot.appendChild(area);
  area.vectorPaths = [{ windingRule: "NONZERO", data: `M ${plx} ${ply + plh} L ${path} L ${plx + plw} ${ply + plh} Z` }];
  area.fills = [{ type: "SOLID", color: env.accent, opacity: 0.16 }]; area.strokes = [];
  const line = figma.createVector(); plot.appendChild(line);
  line.vectorPaths = [{ windingRule: "NONE", data: `M ${path}` }];
  line.strokes = [figma.variables.setBoundVariableForPaint({ type: "SOLID", color: { r: 0, g: 0, b: 0 } }, "color", env.V["color/accent"])];
  line.strokeWeight = 5; line.strokeCap = "ROUND"; line.strokeJoin = "ROUND"; line.fills = []; line.name = "ts.line";
  const last = pts[pts.length - 1];
  const dot = figma.createEllipse(); dot.resize(18, 18); dot.x = last[0] - 9; dot.y = last[1] - 9;
  dot.fills = [{ type: "SOLID", color: env.accent }]; dot.strokes = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }]; dot.strokeWeight = 3; plot.appendChild(dot);
  for (const i of [0, Math.floor(series.length / 2), series.length - 1]) {
    if (!series[i][0]) continue;
    const l = figma.createText(); l.fontName = { family: "IBM Plex Mono", style: "Medium" }; l.fontSize = 16; l.characters = series[i][0];
    l.fills = [{ type: "SOLID", color: env.muted }]; plot.appendChild(l);
    l.x = Math.min(Math.max(X(i) - l.width / 2, plx), plx + plw - l.width); l.y = ply + plh + 12;
  }
}

async function fillSlot(root, slot, scope, max, env) {
  const node = root.findOne((n) => n.name === slot.name);
  if (!node) return;
  if (slot.kind === "bar") {
    const v = Number(get(scope, slot.bind)) || 0;
    const ratio = slot.scale === "ratio-of-max" ? (max ? v / max : 0) : v / 100;
    node.resize(Math.max(Math.round(node.parent.width * ratio), 10), node.height);
  } else if (slot.kind === "arc") {
    const v = Number(get(scope, slot.bind)) || 0;
    const a = node.arcData;
    node.arcData = { startingAngle: a.startingAngle, endingAngle: a.startingAngle + 2 * Math.PI * (v / 100), innerRadius: a.innerRadius };
  } else if (slot.kind === "linechart") {
    drawLineChart(node, get(scope, slot.bind) || [], env);
  } else if (slot.kind === "image") {
    // Photos are placed OUT OF BAND: the Figma plugin sandbox can't fetch URLs.
    // The orchestration layer fetches the URL → bytes → POSTs to an upload_assets
    // submitUrl bound to this node. renderCard returns image-slot node ids.
    return;
  } else if (slot.kind === "logo") {
    // per-brand logo swap: replace the instance's main component with the active
    // brand's logo (publisher/sponsor/show), then re-fit width to the new aspect.
    const logos = (scope.brand && scope.brand.logos) || {};
    let role = slot.bind ? slot.bind.split(".").pop() : null;
    if (role === "footerLogo") role = "show";
    const entry = logos[role];
    if (!entry || node.type !== "INSTANCE") return;
    const comp = await figma.getNodeByIdAsync(entry.id);
    if (!comp) return;
    const h = node.height;
    node.swapComponent(comp);
    node.resize(h * (comp.width / comp.height), h);
    return;
  } else if (slot.kind === "delta") {
    // Sign-driven delta: toggle the up/down triangle SHAPES (no dropping glyphs)
    // and color the value green/red by sign. Container holds tri.up, tri.down, val.
    const v = Number(get(scope, slot.bind)) || 0;
    const up = v >= 0;
    const tU = node.findOne((n) => n.name === "tri.up");
    const tD = node.findOne((n) => n.name === "tri.down");
    const vv = node.findOne((n) => n.name === "val");
    if (tU) tU.visible = up;
    if (tD) tD.visible = !up;
    if (vv) {
      const body = slot.format ? slot.format.replace("{}", Math.abs(v)) : String(Math.abs(v));
      vv.characters = (up ? "+" : "−") + body;
      vv.fills = [{ type: "SOLID", color: up ? env.up : env.down }];
    }
  } else {
    const v = get(scope, slot.bind);
    if (v == null) return;
    node.characters = fmt(v, slot);
  }
}

async function renderCard(manifest, ctx, brandMode, pos) {
  const comp = await figma.getNodeByIdAsync(manifest.figma.componentNodeId);
  const frame = comp.createInstance().detachInstance();
  frame.x = pos.x; frame.y = pos.y;
  frame.name = `render:${manifest.template}:${brandMode}`;

  // Flatten shared chrome (Header/Footer) so their logos/source become editable
  // — detachInstance unwraps only one level, leaving nested chrome instances locked.
  for (const inst of frame.children.filter((c) => c.type === "INSTANCE" && c.getSharedPluginData("pmn", "role") === "chrome")) {
    try { inst.detachInstance(); } catch (e) {}
  }

  const V = {};
  for (const v of await figma.variables.getLocalVariablesAsync()) V[v.name] = v;
  for (const fam of ["Inter", "Roboto"]) for (const st of ["Bold", "Medium", "Regular", "Black"]) { try { await figma.loadFontAsync({ family: fam, style: st }); } catch (e) {} }
  for (const st of ["Bold", "SemiBold", "Medium", "Regular"]) { try { await figma.loadFontAsync({ family: "IBM Plex Mono", style: st }); } catch (e) {} }
  // load every font already present in the detached frame — switching the brand
  // mode or editing text re-measures all of them (incl. any fallback families).
  const used = new Set();
  for (const t of frame.findAll((n) => n.type === "TEXT")) for (const seg of t.getStyledTextSegments(["fontName"])) used.add(JSON.stringify(seg.fontName));
  for (const f of used) { try { await figma.loadFontAsync(JSON.parse(f)); } catch (e) {} }

  const env = { V, accent: { r: 0.18, g: 0.36, b: 1 }, muted: { r: 0.6, g: 0.65, b: 0.79 }, up: { r: 0.086, g: 0.78, b: 0.518 }, down: { r: 0.918, g: 0.224, b: 0.263 } };
  if (manifest.brand) {
    const coll = (await figma.variables.getLocalVariableCollectionsAsync()).find((c) => c.name === manifest.brand.collection);
    const mode = coll.modes.find((m) => m.name === brandMode);
    if (mode) {
      frame.setExplicitVariableModeForCollection(coll, mode.modeId);
      const cv = (name) => { const c = V[name].valuesByMode[mode.modeId]; return { r: c.r, g: c.g, b: c.b }; };
      env.accent = cv("color/accent"); env.muted = cv("color/muted");
      try { env.up = cv("color/up"); env.down = cv("color/down"); } catch (e) {}
      // v3 cards bind the field gradient to variables (reskins via the mode switch);
      // legacy manifests with a code-set "field" node are still honoured below.
      if (manifest.field) {
        const fn = frame.findOne((n) => n.name === manifest.field.node);
        if (fn) {
          const g = (c) => ({ r: c.r, g: c.g, b: c.b });
          const p3 = [0, 0.55, 1];
          fn.fills = [{ type: "GRADIENT_LINEAR", gradientTransform: [[0.707, -0.707, 0.5], [0.707, 0.707, -0.207]],
            gradientStops: manifest.field.stops.map((s, i) => ({ position: p3[i], color: { ...g(V[s].valuesByMode[mode.modeId]), a: 1 } })) }];
        }
      }
    }
  }

  for (const slot of manifest.slots) await fillSlot(frame, slot, ctx, null, env);

  for (const list of manifest.lists || []) {
    const listNode = frame.findOne((n) => n.name === list.node);
    const items = get(ctx, list.bind) || [];
    // clear example rows (detached frames or instances), keep any source text
    listNode.children.filter((c) => c.type !== "TEXT").forEach((c) => c.remove());
    const rowComp = figma.currentPage.findOne((n) => n.type === "COMPONENT" && n.name === list.item.component);
    const barSlot = list.item.slots.find((s) => s.kind === "bar");
    const max = barSlot ? Math.max(...items.map((it) => Number(get(it, barSlot.bind)) || 0)) : 0;
    const source = listNode.children.find((c) => c.type === "TEXT");
    for (const item of items) {
      // DETACH each clone — instance sublayers cannot be resized (bar widths).
      const r = rowComp.createInstance().detachInstance();
      listNode.appendChild(r); r.layoutSizingHorizontal = "FILL";
      for (const s of list.item.slots) await fillSlot(r, s, item, max, env);
    }
    if (source) listNode.appendChild(source);
  }

  // image slots: return their node ids + the data URL so the orchestration can
  // fetch the bytes and POST them to an upload_assets submitUrl bound to each node.
  const imageSlots = (manifest.slots || []).filter((s) => s.kind === "image").map((s) => {
    const n = frame.findOne((x) => x.name === s.name);
    return { slot: s.name, nodeId: n ? n.id : null, url: get(ctx, s.bind) || null };
  });
  const shot = await frame.screenshot();
  return { nodeId: frame.id, imageSlots, shot };
}
